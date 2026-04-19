import PyPDF2
import docx
import re
from gemini_ai import analyze_with_gemini

# ── Text Extraction ────────────────────────────────────────
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return " ".join([para.text for para in doc.paragraphs])

def extract_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    return ""

# ── Fallback keyword matcher (if Gemini fails) ─────────────
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def extract_keywords(text):
    stop_words = {
        'and','the','for','with','you','are','have','has','will','this',
        'that','from','your','our','their','was','were','been','being',
        'can','could','would','should','may','might','shall','must','not',
        'but','also','into','about','such','more','most','any','all',
        'its','who','what','how','when','where','why','out','use','used',
        'work','well','good','new','one','two','job','role','team'
    }
    words = clean_text(text).split()
    return set(w for w in words if len(w) > 2 and w not in stop_words)

def fallback_analyze(resume_text, job_description):
    resume_keywords = extract_keywords(resume_text)
    jd_keywords     = extract_keywords(job_description)
    matched = resume_keywords & jd_keywords
    missing = jd_keywords - resume_keywords
    score   = min(round((len(matched) / max(len(jd_keywords), 1)) * 100), 95)

    return {
        "score":             score,
        "strength_score":    70,
        "detected_role":     "IT Professional",
        "matched_keywords":  sorted(list(matched))[:25],
        "missing_keywords":  sorted(list(missing))[:25],
        "total_matched":     len(matched),
        "total_jd_keywords": len(jd_keywords),
        "section_scores":    {"skills": score, "experience": score, "education": score},
        "section_breakdown": {
            "Contact Info":    "✔ Found",
            "Skills":          "✔ Found",
            "Education":       "✔ Found",
            "Experience":      "✔ Found",
            "Projects":        "✔ Found",
            "Summary":         "✔ Found",
            "Metrics/Numbers": "✘ Missing"
        },
        "suggestion":      "Analysis completed. Add more relevant keywords to improve your score.",
        "tips":            [
            "Mirror keywords from the job description.",
            "Quantify your achievements with numbers.",
            "Add a strong professional summary."
        ],
        "strength_label": "Good Resume",
        "strength_color": "orange"
    }

# ── Main Analyzer ──────────────────────────────────────────
def analyze_resume(file_path, job_description):
    resume_text = extract_text(file_path)
    if not resume_text:
        return {"error": "Could not read file"}

    # Try Gemini first
    print("🤖 Analyzing with Gemini AI...")
    ai_result = analyze_with_gemini(resume_text, job_description)

    if ai_result:
        print("✅ Gemini analysis successful!")
        # Normalize keys to match our frontend
        return {
            "score":             ai_result.get("ats_score", 0),
            "strength_score":    ai_result.get("strength_score", 0),
            "detected_role":     ai_result.get("detected_role", "IT Professional"),
            "matched_keywords":  ai_result.get("matched_keywords", [])[:25],
            "missing_keywords":  ai_result.get("missing_keywords", [])[:25],
            "total_matched":     len(ai_result.get("matched_keywords", [])),
            "total_jd_keywords": len(ai_result.get("matched_keywords", [])) + len(ai_result.get("missing_keywords", [])),
            "section_scores":    ai_result.get("section_scores", {}),
            "section_breakdown": ai_result.get("section_breakdown", {}),
            "suggestion":        ai_result.get("suggestion", ""),
            "tips":              ai_result.get("tips", []),
            "strength_label":    ai_result.get("strength_label", "Good Resume"),
            "strength_color":    ai_result.get("strength_color", "orange"),
        }
    else:
        # Fallback to keyword matching
        print("⚠️ Gemini unavailable, using fallback analysis")
        return fallback_analyze(resume_text, job_description)