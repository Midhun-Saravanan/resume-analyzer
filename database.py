import sqlite3
import os
from datetime import datetime

DB_PATH = 'users.db'

# ──────────────────────────────────────────────
# INIT — Creates all tables on first run
# ──────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # ── Users table ──────────────────────────
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT NOT NULL,
            email        TEXT UNIQUE NOT NULL,
            password     TEXT NOT NULL,
            created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login   TIMESTAMP,
            total_analyses INTEGER DEFAULT 0
        )
    ''')

    # ── Resume Analyses table ─────────────────
    c.execute('''
        CREATE TABLE IF NOT EXISTS analyses (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id          INTEGER NOT NULL,
            date             TEXT NOT NULL,
            role             TEXT,
            ats_score        INTEGER,
            strength_score   INTEGER,
            matched_keywords TEXT,
            missing_keywords TEXT,
            tips             TEXT,
            suggestion       TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # ── Interview Sessions table ──────────────
    c.execute('''
        CREATE TABLE IF NOT EXISTS interview_sessions (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id         INTEGER NOT NULL,
            date            TEXT NOT NULL,
            domain          TEXT,
            role            TEXT,
            experience      TEXT,
            total_questions INTEGER DEFAULT 0,
            tech_count      INTEGER DEFAULT 0,
            behav_count     INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # ── Salary Searches table ─────────────────
    c.execute('''
        CREATE TABLE IF NOT EXISTS salary_searches (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      INTEGER NOT NULL,
            date         TEXT NOT NULL,
            role         TEXT,
            fresher_min  TEXT,
            fresher_max  TEXT,
            senior_max   TEXT,
            skill_bonus  TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # ── Resume Builds table ───────────────────
    c.execute('''
        CREATE TABLE IF NOT EXISTS resume_builds (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      INTEGER NOT NULL,
            date         TEXT NOT NULL,
            full_name    TEXT,
            job_title    TEXT,
            template     TEXT,
            completeness INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database initialized — all tables ready!")


# ──────────────────────────────────────────────
# CONNECTION
# ──────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ──────────────────────────────────────────────
# USER FUNCTIONS
# ──────────────────────────────────────────────
def create_user(name, email, password_hash):
    """Register a new user. Returns True if success, False if email exists."""
    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
            (name, email, password_hash)
        )
        conn.commit()
        print(f"✅ New user created: {email}")
        return True
    except sqlite3.IntegrityError:
        print(f"⚠️ Email already exists: {email}")
        return False
    finally:
        conn.close()


def get_user_by_email(email):
    """Get user by email. Returns dict or None."""
    conn = get_db()
    row = conn.execute(
        'SELECT * FROM users WHERE email = ?', (email,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_id(user_id):
    """Get user by ID. Returns dict or None."""
    conn = get_db()
    row = conn.execute(
        'SELECT * FROM users WHERE id = ?', (user_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def update_last_login(user_id):
    """Update last login timestamp."""
    conn = get_db()
    conn.execute(
        'UPDATE users SET last_login = ? WHERE id = ?',
        (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_id)
    )
    conn.commit()
    conn.close()


def update_user_profile(user_id, name, email):
    """Update user name and email."""
    conn = get_db()
    try:
        conn.execute(
            'UPDATE users SET name = ?, email = ? WHERE id = ?',
            (name, email, user_id)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # email already taken
    finally:
        conn.close()


def get_user_stats(user_id):
    """Get full stats for dashboard."""
    conn = get_db()

    # Total analyses
    total = conn.execute(
        'SELECT COUNT(*) FROM analyses WHERE user_id = ?', (user_id,)
    ).fetchone()[0]

    # Average ATS score
    avg_ats = conn.execute(
        'SELECT AVG(ats_score) FROM analyses WHERE user_id = ?', (user_id,)
    ).fetchone()[0]

    # Best ATS score
    best_ats = conn.execute(
        'SELECT MAX(ats_score) FROM analyses WHERE user_id = ?', (user_id,)
    ).fetchone()[0]

    # Total interview sessions
    interviews = conn.execute(
        'SELECT COUNT(*) FROM interview_sessions WHERE user_id = ?', (user_id,)
    ).fetchone()[0]

    # Total salary searches
    salary_searches = conn.execute(
        'SELECT COUNT(*) FROM salary_searches WHERE user_id = ?', (user_id,)
    ).fetchone()[0]

    # Total resume builds
    resume_builds = conn.execute(
        'SELECT COUNT(*) FROM resume_builds WHERE user_id = ?', (user_id,)
    ).fetchone()[0]

    conn.close()

    return {
        'total_analyses':   total,
        'avg_ats_score':    round(avg_ats, 1) if avg_ats else 0,
        'best_ats_score':   best_ats or 0,
        'total_interviews': interviews,
        'salary_searches':  salary_searches,
        'resume_builds':    resume_builds
    }


# ──────────────────────────────────────────────
# ANALYSIS FUNCTIONS
# ──────────────────────────────────────────────
def save_analysis(user_id, role, ats_score, strength_score,
                  matched, missing, tips=None, suggestion=None):
    """Save a resume analysis result."""
    conn = get_db()
    conn.execute('''
        INSERT INTO analyses
        (user_id, date, role, ats_score, strength_score,
         matched_keywords, missing_keywords, tips, suggestion)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        datetime.now().strftime('%Y-%m-%d'),
        role,
        ats_score,
        strength_score,
        ','.join(matched) if isinstance(matched, list) else matched,
        ','.join(missing) if isinstance(missing, list) else missing,
        str(tips)        if tips       else '',
        suggestion       if suggestion else ''
    ))

    # Update total_analyses count on user
    conn.execute(
        'UPDATE users SET total_analyses = total_analyses + 1 WHERE id = ?',
        (user_id,)
    )

    conn.commit()
    conn.close()
    print(f"✅ Analysis saved — User {user_id} | Role: {role} | ATS: {ats_score}%")


def get_user_analyses(user_id, limit=10):
    """Get last N analyses for a user."""
    conn = get_db()
    rows = conn.execute('''
        SELECT * FROM analyses
        WHERE user_id = ?
        ORDER BY date DESC, id DESC
        LIMIT ?
    ''', (user_id, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_latest_analysis(user_id):
    """Get the most recent analysis."""
    conn = get_db()
    row = conn.execute('''
        SELECT * FROM analyses
        WHERE user_id = ?
        ORDER BY id DESC LIMIT 1
    ''', (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


# ──────────────────────────────────────────────
# INTERVIEW FUNCTIONS
# ──────────────────────────────────────────────
def save_interview_session(user_id, domain, role, experience,
                           total_questions, tech_count, behav_count):
    """Save an interview prep session."""
    conn = get_db()
    conn.execute('''
        INSERT INTO interview_sessions
        (user_id, date, domain, role, experience,
         total_questions, tech_count, behav_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        datetime.now().strftime('%Y-%m-%d'),
        domain, role, experience,
        total_questions, tech_count, behav_count
    ))
    conn.commit()
    conn.close()
    print(f"✅ Interview session saved — User {user_id} | Role: {role}")


def get_user_interviews(user_id, limit=5):
    """Get last N interview sessions."""
    conn = get_db()
    rows = conn.execute('''
        SELECT * FROM interview_sessions
        WHERE user_id = ?
        ORDER BY date DESC, id DESC
        LIMIT ?
    ''', (user_id, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ──────────────────────────────────────────────
# SALARY FUNCTIONS
# ──────────────────────────────────────────────
def save_salary_search(user_id, role, fresher_min, fresher_max,
                       senior_max, skill_bonus):
    """Save a salary search."""
    conn = get_db()
    conn.execute('''
        INSERT INTO salary_searches
        (user_id, date, role, fresher_min, fresher_max, senior_max, skill_bonus)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        datetime.now().strftime('%Y-%m-%d'),
        role, str(fresher_min), str(fresher_max),
        str(senior_max), str(skill_bonus)
    ))
    conn.commit()
    conn.close()
    print(f"✅ Salary search saved — User {user_id} | Role: {role}")


def get_user_salary_searches(user_id, limit=5):
    """Get last N salary searches."""
    conn = get_db()
    rows = conn.execute('''
        SELECT * FROM salary_searches
        WHERE user_id = ?
        ORDER BY date DESC, id DESC
        LIMIT ?
    ''', (user_id, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ──────────────────────────────────────────────
# RESUME BUILDER FUNCTIONS
# ──────────────────────────────────────────────
def save_resume_build(user_id, full_name, job_title,
                      template, completeness):
    """Save a resume build session."""
    conn = get_db()
    conn.execute('''
        INSERT INTO resume_builds
        (user_id, date, full_name, job_title, template, completeness)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        datetime.now().strftime('%Y-%m-%d'),
        full_name, job_title, template, completeness
    ))
    conn.commit()
    conn.close()
    print(f"✅ Resume build saved — User {user_id} | {job_title}")


def get_user_resume_builds(user_id, limit=5):
    """Get last N resume builds."""
    conn = get_db()
    rows = conn.execute('''
        SELECT * FROM resume_builds
        WHERE user_id = ?
        ORDER BY date DESC, id DESC
        LIMIT ?
    ''', (user_id, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ──────────────────────────────────────────────
# MIGRATION — Adds new columns to existing DB
# Run this ONCE if you already have a users.db
# ──────────────────────────────────────────────
def migrate_db():
    """Safely add new columns/tables to existing database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Add new columns to users if they don't exist
    new_user_cols = [
        ("last_login",      "TIMESTAMP"),
        ("total_analyses",  "INTEGER DEFAULT 0"),
    ]
    for col, col_type in new_user_cols:
        try:
            c.execute(f'ALTER TABLE users ADD COLUMN {col} {col_type}')
            print(f"✅ Added column: users.{col}")
        except sqlite3.OperationalError:
            pass  # Column already exists

    # Add new columns to analyses if they don't exist
    new_analysis_cols = [
        ("tips",       "TEXT"),
        ("suggestion", "TEXT"),
    ]
    for col, col_type in new_analysis_cols:
        try:
            c.execute(f'ALTER TABLE analyses ADD COLUMN {col} {col_type}')
            print(f"✅ Added column: analyses.{col}")
        except sqlite3.OperationalError:
            pass  # Column already exists

    conn.commit()
    conn.close()

    # Now create new tables
    init_db()
    print("✅ Migration complete!")


# ──────────────────────────────────────────────
# RUN MIGRATION on import
# ──────────────────────────────────────────────
migrate_db()