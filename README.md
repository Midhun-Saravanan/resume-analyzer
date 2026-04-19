# 🧠 ResumeAI — AI-Powered Career Assistant

<div align="center">

![Python](https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask)
![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-orange?style=for-the-badge&logo=google)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightblue?style=for-the-badge&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**An intelligent full-stack web application that helps job seekers prepare smarter using Google Gemini AI.**

[Features](#-features) • [Demo](#-demo) • [Tech Stack](#-tech-stack) • [Installation](#-installation) • [Usage](#-usage) • [Project Structure](#-project-structure)

</div>

---

## 📸 Preview

> ResumeAI analyzes your resume against job descriptions, generates interview questions, estimates salaries, and builds resumes — all powered by Google Gemini AI.

---

## ✨ Features

### 🔍 Resume Analyzer
- Upload PDF or DOCX resume
- Paste any job description
- Get real ATS score (0–100) based on keyword matching
- **Company-specific ATS scoring** — select Cognizant, TCS, Infosys, Wipro, Accenture, Google, Amazon and more
- Each company uses their actual ATS engine (Taleo, iCIMS, Workday, gHire, CABS)
- Matched & missing keywords highlighted
- Resume sections checklist
- AI-generated improvement tips
- Download full PDF analysis report

### 🎤 Interview Prep Studio
- 12 domains — Technology, Data & AI, Finance, Marketing, HR, DevOps, Cybersecurity and more
- 80+ job roles to choose from
- Configure experience level, target company, skills
- Gemini AI generates Technical, Behavioral, Situational and HR questions
- Filter questions by category
- Difficulty badges (Easy / Medium / Hard)
- STAR method sidebar guide
- Domain-specific interview tips
- Download all questions as PDF

### 💰 Salary Estimator
- Enter any job role
- Get fresher, mid-level and senior salary ranges
- Premium skills that boost salary
- Top hiring companies for the role
- Skill bonus calculator

### 📝 Resume Builder
- Fill in your details section by section
- AI-generated professional summary (Gemini powered)
- Multiple templates
- Resume completeness tracker
- Save and download

### 🆚 Resume Comparison
- Upload two resumes side by side
- Gemini compares both against a job description
- Shows which resume is stronger and why

### 💡 Career Tips & Roadmap
- Enter any skill or role
- Get a full step-by-step learning roadmap
- Curated resources and milestones

### 📊 Personal Dashboard
- Animated gauge charts for ATS score, strength, average
- Full analysis history
- Interview sessions tracking
- Salary search history
- Resume builds history

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.14, Flask |
| **AI Engine** | Google Gemini 2.5 Flash |
| **Database** | SQLite (local) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Design System** | Custom glassmorphism (glass.css) |
| **Typography** | Syne + DM Sans (Google Fonts) |
| **Charts** | Chart.js |
| **PDF Export** | jsPDF |
| **Auth** | Flask Sessions + Werkzeug password hashing |
| **Deployment** | Render.com + Gunicorn |

---

## 🏢 Company-Specific ATS Models

| Company | ATS Software | Key Scoring Factor |
|---|---|---|
| Cognizant | Taleo by Oracle | Keyword Match (45%) |
| TCS | iCIMS | Education (25%) |
| Infosys | Meridian (Internal) | Project Relevance (20%) |
| Wipro | Workday | Experience Continuity (20%) |
| Accenture | Workday | Leadership Keywords (25%) |
| HCL | Taleo by Oracle | Keyword Density (45%) |
| Amazon | Custom CABS | Leadership Principles (35%) |
| Google | Custom gHire | Impact at Scale (30%) |
| Microsoft | Workday | Certifications (25%) |
| Zoho | Zoho Recruit | Skills Tags (40%) |

---

## 🗄 Database Schema

```
users.db
├── users              → id, name, email, password, last_login, total_analyses
├── analyses           → ats_score, strength, role, keywords, tips, suggestion
├── interview_sessions → domain, role, experience, question counts
├── salary_searches    → role, salary ranges, premium skills
└── resume_builds      → full_name, job_title, template, completeness
```

---

## 🚀 Installation

### Prerequisites
- Python 3.10+
- Google Gemini API key → [Get it here](https://aistudio.google.com)

### 1. Clone the repository
```bash
git clone https://github.com/Midhun-Saravanan/resume-analyzer.git
cd resume-analyzer
```

### 2. Create virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root folder:
```
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 5. Run the app
```bash
python app.py
```

### 6. Open in browser
```
http://127.0.0.1:5000
```

---

## 📁 Project Structure

```
resume-analyzer/
│
├── app.py                  ← Flask app, all routes
├── database.py             ← All database functions (5 tables)
├── gemini_ai.py            ← All Google Gemini AI logic & prompts
├── analyzer.py             ← Resume analysis helpers
├── interviewer.py          ← Interview question generation
├── salary.py               ← Salary estimation logic
│
├── static/
│   ├── glass.css           ← Full custom design system (glassmorphism)
│   ├── glass_nav.js        ← Navbar dropdown + toast notifications
│   ├── script.js           ← Analyzer page JS
│   ├── dashboard.js        ← Dashboard charts & stats
│   ├── builder.js          ← Resume builder logic
│   ├── salary.js           ← Salary page JS
│   ├── compare.js          ← Resume comparison JS
│   └── ...other css files
│
├── templates/
│   ├── navbar.html         ← Shared navbar (Jinja include)
│   ├── landing.html        ← Home / marketing page
│   ├── login.html
│   ├── register.html
│   ├── index.html          ← Resume Analyzer
│   ├── dashboard.html      ← User dashboard
│   ├── interview.html      ← Interview Prep Studio
│   ├── salary.html         ← Salary Estimator
│   ├── resume_builder.html ← Resume Builder
│   ├── compare.html        ← Resume Comparison
│   └── tips.html           ← Career Tips
│
├── requirements.txt        ← Python dependencies
├── Procfile                ← Render/Heroku start command
└── .gitignore
```

---

## 🔐 Environment Variables

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | Your Google Gemini API key from aistudio.google.com |

---

## 🌐 Deployment (Render.com)

1. Push code to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your GitHub repository
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Environment:** Python 3
5. Add environment variable: `GEMINI_API_KEY`
6. Deploy ✅

---

## 📊 How ATS Scoring Works

ATS (Applicant Tracking System) is software companies use to automatically filter resumes before any human sees them. **75% of resumes are rejected by ATS before reaching HR.**

ResumeAI simulates this by analyzing:

| Factor | Weight |
|---|---|
| Keyword Match | 40–45% |
| Job Title Alignment | 20% |
| Experience Relevance | 20% |
| Education Match | 10% |
| Resume Format | 5–10% |

**Score Ranges:**
- 🟢 90–100 → Excellent — Very likely to pass ATS
- 🟢 70–89 → Good — Should pass most ATS systems
- 🟡 50–69 → Average — Will pass some ATS systems
- 🟠 30–49 → Weak — Likely rejected by most ATS
- 🔴 0–29 → Poor — Almost certainly auto-rejected

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Developer

**Midhun Saravanan**
- 2nd Year B.Tech Information Technology
- GitHub: [@Midhun-Saravanan](https://github.com/Midhun-Saravanan)

---

<div align="center">
  <p>Built with ❤️ using Python, Flask and Google Gemini AI</p>
  <p>⭐ Star this repo if you found it helpful!</p>
</div>
