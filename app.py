from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os
from analyzer import analyze_resume
from database import (
    init_db, save_analysis, get_user_analyses, get_user_by_email, create_user,
    update_last_login, get_user_stats, save_interview_session,
    save_salary_search, save_resume_build, get_user_interviews,
    get_user_salary_searches, get_user_resume_builds
)
from functools import wraps

app = Flask(__name__)
app.secret_key = 'resumeai_secret_key_2026'
app.config['UPLOAD_FOLDER'] = 'uploads'

init_db()

# ── Auth Guard ─────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to continue.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# ── Auth Routes ────────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        name     = request.form['name'].strip()
        email    = request.form['email'].strip()
        password = request.form['password']
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return render_template('register.html')
        hashed  = generate_password_hash(password)
        success = create_user(name, email, hashed)
        if success:
            flash('Account created! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Email already registered.', 'error')
            return render_template('register.html')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email    = request.form['email'].strip()
        password = request.form['password']
        user     = get_user_by_email(email)
        if user and check_password_hash(user['password'], password):
            session['user_id']    = user['id']
            session['user_name']  = user['name']
            session['user_email'] = user['email']
            update_last_login(user['id'])   # ← track last login
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

# ── Page Routes ────────────────────────────────────────────
@app.route('/')
def landing():
    user = None
    if 'user_id' in session:
        user = {'name': session.get('user_name'), 'email': session.get('user_email')}
    return render_template('landing.html', user=user)

@app.route('/analyzer')
@login_required
def analyzer():
    return render_template('index.html')

@app.route('/compare')
@login_required
def compare():
    return render_template('compare.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user_id  = session['user_id']
    analyses = get_user_analyses(user_id)
    stats    = get_user_stats(user_id)                  # ← real stats from all tables
    interviews    = get_user_interviews(user_id, 3)     # ← last 3 interview sessions
    salary_hist   = get_user_salary_searches(user_id, 3) # ← last 3 salary searches
    resume_builds = get_user_resume_builds(user_id, 3)  # ← last 3 resume builds
    return render_template('dashboard.html',
        analyses      = analyses,
        stats         = stats,
        interviews    = interviews,
        salary_hist   = salary_hist,
        resume_builds = resume_builds
    )

@app.route('/interview')
@login_required
def interview():
    return render_template('interview.html')

@app.route('/salary')
@login_required
def salary():
    return render_template('salary.html')

@app.route('/builder')
@login_required
def builder():
    return render_template('resume_builder.html')

@app.route('/tips')
def tips():
    return render_template('tips.html')

# ── API: Analyze ───────────────────────────────────────────
@app.route('/analyze', methods=['POST'])
@login_required
def analyze():
    resume_file     = request.files['resume']
    job_description = request.form['job_description']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
    resume_file.save(file_path)
    result = analyze_resume(file_path, job_description)
    save_analysis(
        session['user_id'],
        result.get('detected_role', 'Unknown'),
        result.get('score', 0),
        result.get('strength_score', 0),
        result.get('matched_keywords', []),
        result.get('missing_keywords', []),
        result.get('tips', []),           # ← now saving tips too
        result.get('suggestion', '')      # ← now saving suggestion too
    )
    return jsonify(result)

# ── API: Compare ───────────────────────────────────────────
@app.route('/analyze_compare', methods=['POST'])
@login_required
def analyze_compare():
    resume1         = request.files['resume1']
    resume2         = request.files['resume2']
    job_description = request.form['job_description']
    path1 = os.path.join(app.config['UPLOAD_FOLDER'], 'c1_' + resume1.filename)
    path2 = os.path.join(app.config['UPLOAD_FOLDER'], 'c2_' + resume2.filename)
    resume1.save(path1)
    resume2.save(path2)

    print("🤖 Comparing Resume 1 with Gemini AI...")
    result1 = analyze_resume(path1, job_description)

    print("🤖 Comparing Resume 2 with Gemini AI...")
    result2 = analyze_resume(path2, job_description)

    result1['total_matched'] = len(result1.get('matched_keywords', []))
    result2['total_matched'] = len(result2.get('matched_keywords', []))

    return jsonify({"resume1": result1, "resume2": result2})

# ── API: Salary ────────────────────────────────────────────
@app.route('/get_salary', methods=['POST'])
@login_required
def get_salary():
    from gemini_ai import estimate_salary_with_gemini
    from salary import estimate_salary

    jd = request.json.get('job_description', '')
    if not jd:
        return jsonify({"error": "No job description provided"})

    print("💰 Estimating salary with Gemini AI...")
    result = estimate_salary_with_gemini(jd)

    if result:
        print("✅ Gemini salary estimation successful!")
    else:
        print("⚠️ Gemini unavailable, using fallback salary data")
        result = estimate_salary(jd)

    # ── Save salary search to DB ──────────────────────────
    try:
        save_salary_search(
            session['user_id'],
            result.get('role', 'Unknown'),
            result.get('fresher', {}).get('min', 0),
            result.get('fresher', {}).get('max', 0),
            result.get('senior',  {}).get('max', 0),
            result.get('skill_bonus', 0)
        )
    except Exception as e:
        print(f"⚠️ Could not save salary search: {e}")

    return jsonify(result)

# ── API: Interview Questions ───────────────────────────────
@app.route('/get_interview_questions', methods=['POST'])
@login_required
def get_interview_questions():
    from gemini_ai import generate_questions_with_gemini
    from interviewer import generate_questions

    data       = request.json
    jd         = data.get('job_description', '')
    role       = data.get('role', 'General IT Role')
    domain     = data.get('domain', 'tech')
    experience = data.get('experience', 'fresher')

    if not jd:
        return jsonify({"error": "No job description provided"})

    print(f"💼 Generating interview questions with Gemini AI for: {role}")
    result = generate_questions_with_gemini(jd, role)

    if result:
        print("✅ Gemini interview questions generated!")
    else:
        print("⚠️ Gemini unavailable, using fallback questions")
        result = generate_questions(jd, role)

    # ── Save interview session to DB ──────────────────────
    try:
        tech_count  = len(result.get('technical', []))
        behav_count = len(result.get('behavioral', []))
        total       = tech_count + behav_count + \
                      len(result.get('situational', [])) + \
                      len(result.get('jd_specific', []))
        save_interview_session(
            session['user_id'],
            domain, role, experience,
            total, tech_count, behav_count
        )
    except Exception as e:
        print(f"⚠️ Could not save interview session: {e}")

    return jsonify(result)

# ── API: Resume Builder Summary ────────────────────────────
@app.route('/generate_summary', methods=['POST'])
@login_required
def generate_summary():
    from gemini_ai import generate_resume_summary

    data      = request.json
    job_title = data.get('job_title', '')
    skills    = data.get('skills', '')
    mode      = data.get('mode', 'summary')

    if not job_title:
        return jsonify({"error": "Job title required"})

    print(f"📝 Generating resume summary for: {job_title}")
    result = generate_resume_summary(job_title, skills, mode)

    return jsonify(result)

# ── API: Save Resume Build ─────────────────────────────────
@app.route('/save_resume_build', methods=['POST'])
@login_required
def save_resume_build_route():
    data = request.json
    try:
        save_resume_build(
            session['user_id'],
            data.get('full_name', ''),
            data.get('job_title', ''),
            data.get('template', 'classic'),
            data.get('completeness', 0)
        )
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# ── API: Skill Roadmap ─────────────────────────────────────
@app.route('/get_skill_roadmap', methods=['POST'])
@login_required
def get_skill_roadmap():
    from gemini_ai import generate_skill_roadmap

    missing = request.json.get('missing_keywords', [])
    role    = request.json.get('role', 'IT Professional')

    if not missing:
        return jsonify({"error": "No missing keywords provided"})

    print(f"🗺️ Generating skill roadmap with Gemini AI for: {role}")
    result = generate_skill_roadmap(missing, role)

    if result:
        print("✅ Gemini skill roadmap generated!")
    else:
        return jsonify({"error": "Could not generate roadmap"})

    return jsonify(result)

# ── API: User History ──────────────────────────────────────
@app.route('/get_user_history')
@login_required
def get_user_history():
    analyses = get_user_analyses(session['user_id'])
    return jsonify(analyses)

# ── API: User Stats ────────────────────────────────────────
@app.route('/get_user_stats')
@login_required
def get_user_stats_route():
    stats = get_user_stats(session['user_id'])
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)