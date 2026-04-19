// ── File Upload ────────────────────────────────────────────
function updateFileName() {
    const file = document.getElementById('resumeFile').files[0];
    if (file) {
        document.getElementById('uploadText').textContent = '✅ ' + file.name;
        document.getElementById('uploadArea').style.borderColor = '#667eea';
        document.getElementById('uploadArea').style.boxShadow = '0 0 20px rgba(102,126,234,0.2)';
    }
}

// ── Main Analyzer ──────────────────────────────────────────
async function analyzeResume() {
    const file = document.getElementById('resumeFile').files[0];
    const jd   = document.getElementById('jobDesc').value;

    if (!file)      { showToast('Please upload a resume!', 'error'); return; }
    if (!jd.trim()) { showToast('Please paste a job description!', 'error'); return; }

    const btn = document.querySelector('.btn-primary');
    btn.textContent = '⏳ Analyzing with AI...';
    btn.disabled = true;

    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_description', jd);

    try {
        const res  = await fetch('/analyze', { method: 'POST', body: formData });
        const data = await res.json();

        // Role banner
        document.getElementById('roleBanner').innerHTML =
            `🎯 Detected Role: <strong>${data.detected_role}</strong> &nbsp;|&nbsp; 🤖 Powered by Gemini AI`;

        // Scores with animation
        animateScore('scoreNum', data.score);
        animateScore('strengthNum', data.strength_score);

        // Score colors
        const atsColor = data.score >= 70
            ? 'linear-gradient(135deg,#00e676,#00b0ff)'
            : data.score >= 40
            ? 'linear-gradient(135deg,#ffab40,#ff6d00)'
            : 'linear-gradient(135deg,#ff5252,#b71c1c)';

        document.getElementById('scoreCircle').style.background = atsColor;
        document.getElementById('scoreLabel').textContent = data.score >= 70
            ? '🟢 Strong Match — Good to apply!'
            : data.score >= 40
            ? '🟡 Average Match — Needs improvement'
            : '🔴 Weak Match — Major changes needed';

        const strColor = data.strength_color === 'green'
            ? 'linear-gradient(135deg,#00e676,#00b0ff)'
            : data.strength_color === 'orange'
            ? 'linear-gradient(135deg,#ffab40,#ff6d00)'
            : 'linear-gradient(135deg,#ff5252,#b71c1c)';

        document.getElementById('strengthCircle').style.background = strColor;
        document.getElementById('strengthLabel').textContent = data.strength_label || '';

        // Section breakdown bars
        const bars = document.getElementById('breakdownBars');
        bars.innerHTML = Object.entries(data.section_scores).map(([k, v]) => `
            <div class="bar-item">
                <div class="bar-label">
                    <span>${k.charAt(0).toUpperCase() + k.slice(1)}</span>
                    <span>${v}%</span>
                </div>
                <div class="bar-track">
                    <div class="bar-fill" style="width:0%" data-target="${v}"></div>
                </div>
            </div>
        `).join('');
        setTimeout(() => {
            document.querySelectorAll('.bar-fill').forEach(b => {
                b.style.width = b.dataset.target + '%';
            });
        }, 100);

        // Checklist
        const cl = document.getElementById('sectionChecklist');
        cl.innerHTML = Object.entries(data.section_breakdown).map(([k, v]) => `
            <div style="display:flex;align-items:center;gap:8px;padding:8px 12px;
                background:${v.includes('✔') ? 'rgba(0,230,118,0.08)' : 'rgba(255,82,82,0.08)'};
                border:1px solid ${v.includes('✔') ? 'rgba(0,230,118,0.2)' : 'rgba(255,82,82,0.2)'};
                border-radius:10px;font-size:0.82rem;">
                <span>${v.includes('✔') ? '✅' : '❌'}</span>
                <span style="color:var(--text);font-weight:500">${k}</span>
            </div>
        `).join('');

        // Keywords
        document.getElementById('matchedKeywords').innerHTML =
            (data.matched_keywords || []).map(k => `<span class="tag tag-matched">${k}</span>`).join('');
        document.getElementById('missingKeywords').innerHTML =
            (data.missing_keywords || []).map(k => `<span class="tag tag-missing">${k}</span>`).join('');

        // Suggestions
        const tips = (data.tips || []).map(t => `
            <div style="display:flex;gap:10px;align-items:flex-start;margin-bottom:10px;">
                <span style="color:#667eea;font-size:1rem;">→</span>
                <span class="suggestion-text" style="color:var(--subtext);font-size:0.88rem;line-height:1.6">${t}</span>
            </div>`).join('');
        document.getElementById('suggestionBox').innerHTML = `
            <p class="suggestion-main" style="color:var(--text);margin-bottom:12px;font-weight:500">${data.suggestion || ''}</p>
            <ul class="tips-list" style="list-style:none;padding:0">${(data.tips||[]).map(t=>`<li style="display:none">${t}</li>`).join('')}</ul>
            ${tips}`;

        document.getElementById('resultBox').style.display = 'block';
        document.getElementById('resultBox').scrollIntoView({ behavior: 'smooth' });

        // Toast + confetti
        if (data.score >= 70) {
            showToast('🎉 Great match! Score: ' + data.score + '%', 'success');
            launchConfetti();
        } else {
            showToast('Analysis complete! Score: ' + data.score + '%', 'info');
        }

        saveHistory(data);
        loadHistory();

    } catch (err) {
        showToast('Something went wrong. Please try again.', 'error');
        console.error(err);
    }

    btn.textContent = '🔍 Analyze My Resume';
    btn.disabled = false;
}

// ── Animate score counter ──────────────────────────────────
function animateScore(elId, target) {
    const el = document.getElementById(elId);
    if (!el) return;
    let current = 0;
    const step  = target / 40;
    const timer = setInterval(() => {
        current += step;
        if (current >= target) { current = target; clearInterval(timer); }
        el.textContent = Math.round(current) + '%';
    }, 30);
}

// ── Confetti ───────────────────────────────────────────────
function launchConfetti() {
    const colors = ['#667eea', '#764ba2', '#00d4ff', '#00e676', '#ffab40'];
    for (let i = 0; i < 80; i++) {
        const el = document.createElement('div');
        el.style.cssText = `
            position:fixed;
            left:${Math.random() * 100}vw;
            top:-10px;
            width:${Math.random() * 8 + 4}px;
            height:${Math.random() * 8 + 4}px;
            background:${colors[Math.floor(Math.random() * colors.length)]};
            border-radius:${Math.random() > 0.5 ? '50%' : '2px'};
            pointer-events:none;
            z-index:9999;
            animation:confettiFall ${Math.random() * 2 + 2}s linear forwards;
            animation-delay:${Math.random() * 0.5}s;
        `;
        document.body.appendChild(el);
        setTimeout(() => el.remove(), 4000);
    }
    if (!document.getElementById('confettiStyle')) {
        const style = document.createElement('style');
        style.id = 'confettiStyle';
        style.textContent = `@keyframes confettiFall { to { transform: translateY(105vh) rotate(720deg); opacity:0; } }`;
        document.head.appendChild(style);
    }
}

// ── History ────────────────────────────────────────────────
function saveHistory(data) {
    let history = JSON.parse(localStorage.getItem('resumeHistory') || '[]');
    history.unshift({
        date:     new Date().toLocaleDateString(),
        role:     data.detected_role,
        score:    data.score,
        strength: data.strength_score
    });
    history = history.slice(0, 5);
    localStorage.setItem('resumeHistory', JSON.stringify(history));
}

function loadHistory() {
    const history = JSON.parse(localStorage.getItem('resumeHistory') || '[]');
    const card    = document.getElementById('historyCard');
    const list    = document.getElementById('historyList');
    if (!card || !list) return;

    if (!history.length) { card.style.display = 'none'; return; }

    list.innerHTML = history.map(h => `
        <div style="display:flex;justify-content:space-between;align-items:center;
            padding:12px 16px;background:var(--input-bg);border-radius:10px;
            border:1px solid var(--border);margin-bottom:8px;">
            <div>
                <div style="font-weight:600;font-size:0.88rem">${h.role}</div>
                <div style="font-size:0.75rem;color:var(--subtext)">${h.date}</div>
            </div>
            <div style="display:flex;gap:10px;">
                <span class="tag tag-matched">ATS: ${h.score}%</span>
                <span style="padding:4px 12px;border-radius:20px;font-size:0.78rem;
                    background:rgba(0,212,255,0.1);color:#00d4ff;border:1px solid rgba(0,212,255,0.2)">
                    Str: ${h.strength}%
                </span>
            </div>
        </div>
    `).join('');
    card.style.display = 'block';
}

// ── Clean text for PDF ─────────────────────────────────────
function cleanText(text) {
    return (text || '').replace(/[^\x00-\x7F]/g, '').trim();
}

// ── Download PDF ───────────────────────────────────────────
function downloadReport() {
    showToast('Generating PDF report...', 'info');

    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    const score      = document.getElementById('scoreNum')?.textContent || '0%';
    const strength   = document.getElementById('strengthNum')?.textContent || '0%';
    const label      = cleanText(document.getElementById('scoreLabel')?.textContent || '');
    const role       = cleanText(document.getElementById('roleBanner')?.textContent || '');
    const matched    = [...document.querySelectorAll('.tag-matched')].map(t => t.textContent).join(', ');
    const missing    = [...document.querySelectorAll('.tag-missing')].map(t => t.textContent).join(', ');
    const suggestion = cleanText(document.querySelector('.suggestion-main')?.textContent || '');
    const tips       = [...document.querySelectorAll('.tips-list li')].map((t, i) => `${i+1}. ${cleanText(t.textContent)}`);

    // Header
    doc.setFillColor(102, 126, 234);
    doc.rect(0, 0, 220, 35, 'F');
    doc.setTextColor(255, 255, 255);
    doc.setFontSize(20);
    doc.setFont('helvetica', 'bold');
    doc.text('AI Resume Analyzer Report', 105, 22, { align: 'center' });
    doc.setFontSize(10);
    doc.setFont('helvetica', 'normal');
    doc.text(role, 105, 30, { align: 'center' });

    // Scores
    doc.setTextColor(50, 50, 50);
    doc.setFontSize(13);
    doc.setFont('helvetica', 'bold');
    doc.text('ATS Match Score', 20, 50);
    doc.text('Resume Strength', 110, 50);
    doc.setFontSize(30);
    doc.setTextColor(102, 126, 234);
    doc.text(score, 20, 65);
    doc.text(strength, 110, 65);
    doc.setFontSize(10);
    doc.setTextColor(100, 100, 100);
    doc.setFont('helvetica', 'normal');
    doc.text(label, 20, 73);

    // Divider
    doc.setDrawColor(220, 220, 220);
    doc.line(20, 78, 190, 78);

    // Matched Keywords
    doc.setFontSize(12);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(46, 125, 50);
    doc.text('Matched Keywords', 20, 88);
    doc.setFontSize(9);
    doc.setFont('helvetica', 'normal');
    doc.setTextColor(80, 80, 80);
    const matchedLines = doc.splitTextToSize(matched || 'None', 170);
    doc.text(matchedLines, 20, 96);

    // Missing Keywords
    const missingY = 96 + matchedLines.length * 5 + 8;
    doc.line(20, missingY - 3, 190, missingY - 3);
    doc.setFontSize(12);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(198, 40, 40);
    doc.text('Missing Keywords', 20, missingY);
    doc.setFontSize(9);
    doc.setFont('helvetica', 'normal');
    doc.setTextColor(80, 80, 80);
    const missingLines = doc.splitTextToSize(missing || 'None', 170);
    doc.text(missingLines, 20, missingY + 8);

    // Suggestions
    const suggY = missingY + 8 + missingLines.length * 5 + 10;
    doc.line(20, suggY - 3, 190, suggY - 3);
    doc.setFontSize(12);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(45, 58, 140);
    doc.text('Suggestions & Tips', 20, suggY);
    doc.setFontSize(9);
    doc.setFont('helvetic', 'normal');
    doc.setTextColor(80, 80, 80);
    doc.text(doc.splitTextToSize(suggestion || '', 170), 20, suggY + 8);
    tips.forEach((tip, i) => {
        doc.text(doc.splitTextToSize(tip, 165), 25, suggY + 17 + (i * 12));
    });

    // Footer
    doc.setFillColor(245, 245, 255);
    doc.rect(0, 278, 220, 20, 'F');
    doc.setFontSize(9);
    doc.setTextColor(150, 150, 150);
    doc.text('Generated by ResumeAI — Powered by Gemini AI', 105, 287, { align: 'center' });

    doc.save('Resume_Analysis_Report.pdf');
}

window.addEventListener('DOMContentLoaded', loadHistory);