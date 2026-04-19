import re

SALARY_DATA = {
    'Python Developer':     {'fresher': (3.5, 6),   'mid': (6, 12),   'senior': (12, 25),  'currency': 'LPA'},
    'Web Developer':        {'fresher': (3, 5.5),   'mid': (5, 10),   'senior': (10, 20),  'currency': 'LPA'},
    'Java Developer':       {'fresher': (3.5, 6.5), 'mid': (6, 14),   'senior': (14, 28),  'currency': 'LPA'},
    'Data Analyst':         {'fresher': (3, 5.5),   'mid': (5.5, 11), 'senior': (11, 20),  'currency': 'LPA'},
    'Data Scientist':       {'fresher': (5, 9),     'mid': (9, 18),   'senior': (18, 35),  'currency': 'LPA'},
    'DevOps Engineer':      {'fresher': (4, 7),     'mid': (7, 16),   'senior': (16, 30),  'currency': 'LPA'},
    'Android Developer':    {'fresher': (3, 5.5),   'mid': (5, 11),   'senior': (11, 22),  'currency': 'LPA'},
    'UI/UX Designer':       {'fresher': (3, 5),     'mid': (5, 10),   'senior': (10, 18),  'currency': 'LPA'},
    'Database Engineer':    {'fresher': (3.5, 6),   'mid': (6, 12),   'senior': (12, 22),  'currency': 'LPA'},
    'AI/ML Engineer':       {'fresher': (5, 10),    'mid': (10, 20),  'senior': (20, 40),  'currency': 'LPA'},
    'General IT Role':      {'fresher': (2.5, 5),   'mid': (5, 10),   'senior': (10, 18),  'currency': 'LPA'},
}

SKILL_BONUSES = {
    'aws': 1.5, 'azure': 1.5, 'gcp': 1.5,
    'kubernetes': 2, 'docker': 1,
    'machine learning': 2, 'deep learning': 2.5,
    'react': 1, 'node': 1, 'typescript': 1,
    'spark': 1.5, 'kafka': 1.5,
    'microservices': 1.5, 'system design': 2,
}

TOP_COMPANIES = {
    'Python Developer':  ['Google', 'Microsoft', 'Amazon', 'Flipkart', 'Swiggy'],
    'Web Developer':     ['Infosys', 'TCS', 'Wipro', 'Zoho', 'Freshworks'],
    'Data Scientist':    ['Amazon', 'Google', 'Microsoft', 'Mu Sigma', 'Fractal'],
    'Data Analyst':      ['Deloitte', 'Accenture', 'TCS', 'Infosys', 'IBM'],
    'Java Developer':    ['TCS', 'Infosys', 'Wipro', 'HCL', 'Cognizant'],
    'DevOps Engineer':   ['Amazon', 'Microsoft', 'IBM', 'ThoughtWorks', 'Razorpay'],
    'AI/ML Engineer':    ['Google', 'Microsoft', 'Amazon', 'NVIDIA', 'Samsung'],
    'General IT Role':   ['TCS', 'Infosys', 'Wipro', 'HCL', 'Cognizant'],
}

def detect_role_from_jd(jd_text):
    from analyzer import detect_job_role
    return detect_job_role(jd_text)

def estimate_salary(jd_text):
    jd_lower = jd_text.lower()
    role = detect_role_from_jd(jd_text)
    data = SALARY_DATA.get(role, SALARY_DATA['General IT Role'])

    # Calculate skill bonus
    bonus = 0
    found_premium = []
    for skill, b in SKILL_BONUSES.items():
        if skill in jd_lower:
            bonus += b
            found_premium.append(skill)

    bonus = min(bonus, 5)

    fresher_min = round(data['fresher'][0] + bonus * 0.3, 1)
    fresher_max = round(data['fresher'][1] + bonus * 0.5, 1)
    mid_min     = round(data['mid'][0] + bonus * 0.5, 1)
    mid_max     = round(data['mid'][1] + bonus, 1)
    senior_min  = round(data['senior'][0] + bonus, 1)
    senior_max  = round(data['senior'][1] + bonus * 1.5, 1)

    companies = TOP_COMPANIES.get(role, TOP_COMPANIES['General IT Role'])

    # Experience hints from JD
    exp_hint = "Not specified"
    exp_match = re.search(r'(\d+)\+?\s*(?:to\s*(\d+))?\s*years?', jd_lower)
    if exp_match:
        exp_hint = exp_match.group(0).title()

    return {
        "role": role,
        "currency": data['currency'],
        "fresher":  {"min": fresher_min, "max": fresher_max, "label": "0–2 years"},
        "mid":      {"min": mid_min,     "max": mid_max,     "label": "2–5 years"},
        "senior":   {"min": senior_min,  "max": senior_max,  "label": "5+ years"},
        "premium_skills": found_premium,
        "skill_bonus": round(bonus, 1),
        "top_companies": companies,
        "experience_required": exp_hint,
    }