// ── Dark Mode ──────────────────────────────────────────────
function toggleDarkMode() {
    const html = document.documentElement;
    const btn = document.querySelector('.theme-toggle');
    if (html.getAttribute('data-theme') === 'dark') {
        html.setAttribute('data-theme', 'light');
        btn.textContent = '🌙 Dark Mode';
        localStorage.setItem('theme', 'light');
    } else {
        html.setAttribute('data-theme', 'dark');
        btn.textContent = '☀️ Light Mode';
        localStorage.setItem('theme', 'dark');
    }
}

window.addEventListener('DOMContentLoaded', () => {
    const saved = localStorage.getItem('theme');
    if (saved === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        document.querySelector('.theme-toggle').textContent = '☀️ Light Mode';
    }
});

function updateName(inputId, labelId) {
    const file = document.getElementById(inputId).files[0];
    if (file) document.getElementById(labelId).textContent = '✅ ' + file.name;
}

// ── Score Color ────────────────────────────────────────────
function scoreColor(score) {
    if (score >= 70) return 'linear-gradient(135deg, #2e7d32, #43a047)';
    if (score >= 40) return 'linear-gradient(135deg, #e65100, #f57c00)';
    return 'linear-gradient(135deg, #b71c1c, #c62828)';
}

// ── Render Mini Circle ─────────────────────────────────────
function renderCircle(id, score, label) {
    const el = document.getElementById(id);
    el.innerHTML = `<div class="circle-score" style="background:${scoreColor(score)}">${score}%</div><div class="circle-label">${label}</div>`;
}

// ── Render Bars ────────────────────────────────────────────
function renderBars(id, sections) {
    const el = document.getElementById(id);
    el.innerHTML = Object.entries(sections).map(([k, v]) => `
        <div class="bar-item">
            <div class="bar-label">
                <span>${k.charAt(0).toUpperCase() + k.slice(1)}</span>
                <span>${v}%</span>
            </div>
            <div class="bar-track">
                <div class="bar-fill" style="width:${v}%;background:${v>=70?'#43a047':v>=40?'#f57c00':'#c62828'}"></div>
            </div>
        </div>
    `).join('');
}

// ── Render Keywords ────────────────────────────────────────
function renderKeywords(matchedId, missingId, matched, missing) {
    document.getElementById(matchedId).innerHTML =
        matched.slice(0,12).map(k => `<span class="tag tag-matched">${k}</span>`).join(' ');
    document.getElementById(missingId).innerHTML =
        missing.slice(0,12).map(k => `<span class="tag tag-missing">${k}</span>`).join(' ');
}

// ── Main Compare ───────────────────────────────────────────
async function compareResumes() {
    const r1 = document.getElementById('resume1').files[0];
    const r2 = document.getElementById('resume2').files[0];
    const jd = document.getElementById('jobDesc').value;

    if (!r1) { alert('Please upload Resume 1!'); return; }
    if (!r2) { alert('Please upload Resume 2!'); return; }
    if (!jd.trim()) { alert('Please paste a job description!'); return; }

    const btn = document.querySelector('.analyze-btn');
    btn.textContent = '⏳ Comparing...';
    btn.disabled = true;

    const formData = new FormData();
    formData.append('resume1', r1);
    formData.append('resume2', r2);
    formData.append('job_description', jd);

    try {
        const res = await fetch('/analyze_compare', { method: 'POST', body: formData });
        const data = await res.json();
        const d1 = data.resume1;
        const d2 = data.resume2;

        const name1 = r1.name.replace(/\.[^/.]+$/, '');
        const name2 = r2.name.replace(/\.[^/.]+$/, '');

        // ── Names
        document.getElementById('r1name').textContent = '📄 ' + name1;
        document.getElementById('r2name').textContent = '📄 ' + name2;
        document.getElementById('th1').textContent = name1;
        document.getElementById('th2').textContent = name2;

        // ── Roles
        document.getElementById('r1role').textContent = '🎯 ' + d1.detected_role;
        document.getElementById('r2role').textContent = '🎯 ' + d2.detected_role;

        // ── Circles
        renderCircle('r1ats', d1.score, 'ATS Score');
        renderCircle('r1str', d1.strength_score, 'Strength');
        renderCircle('r2ats', d2.score, 'ATS Score');
        renderCircle('r2str', d2.strength_score, 'Strength');

        // ── Bars
        renderBars('r1bars', d1.section_scores);
        renderBars('r2bars', d2.section_scores);

        // ── Keywords
        renderKeywords('r1matched', 'r1missing', d1.matched_keywords, d1.missing_keywords);
        renderKeywords('r2matched', 'r2missing', d2.matched_keywords, d2.missing_keywords);

        // ── Highlight winner card
        const card1 = document.getElementById('card1');
        const card2 = document.getElementById('card2');
        card1.classList.remove('winner', 'loser');
        card2.classList.remove('winner', 'loser');

        if (d1.score > d2.score) {
            card1.classList.add('winner');
            card2.classList.add('loser');
        } else if (d2.score > d1.score) {
            card2.classList.add('winner');
            card1.classList.add('loser');
        }

        // ── Winner Banner
        const diff = Math.abs(d1.score - d2.score);
        let winnerHTML = '';
        if (d1.score > d2.score) {
            winnerHTML = `🏆 <strong>${name1}</strong> wins with a ${d1.score}% ATS score — ${diff}% higher than Resume 2!`;
        } else if (d2.score > d1.score) {
            winnerHTML = `🏆 <strong>${name2}</strong> wins with a ${d2.score}% ATS score — ${diff}% higher than Resume 1!`;
        } else {
            winnerHTML = `🤝 It's a tie! Both resumes scored <strong>${d1.score}%</strong>`;
        }
        document.getElementById('winnerBanner').innerHTML = winnerHTML;

        // ── Comparison Table
        const rows = [
            ['ATS Match Score',     d1.score + '%',          d2.score + '%',          d1.score, d2.score],
            ['Resume Strength',     d1.strength_score + '%', d2.strength_score + '%', d1.strength_score, d2.strength_score],
            ['Skills Score',        d1.section_scores.skills + '%',     d2.section_scores.skills + '%',     d1.section_scores.skills, d2.section_scores.skills],
            ['Experience Score',    d1.section_scores.experience + '%', d2.section_scores.experience + '%', d1.section_scores.experience, d2.section_scores.experience],
            ['Education Score',     d1.section_scores.education + '%',  d2.section_scores.education + '%',  d1.section_scores.education, d2.section_scores.education],
            ['Keywords Matched',    d1.total_matched,        d2.total_matched,        d1.total_matched, d2.total_matched],
        ];

        document.getElementById('compareTable').innerHTML = rows.map(([label, v1, v2, n1, n2]) => `
            <tr>
                <td>${label}</td>
                <td class="${n1 > n2 ? 'cell-win' : n1 < n2 ? 'cell-lose' : ''}">${v1} ${n1 > n2 ? '✔' : ''}</td>
                <td class="${n2 > n1 ? 'cell-win' : n2 < n1 ? 'cell-lose' : ''}">${v2} ${n2 > n1 ? '✔' : ''}</td>
            </tr>
        `).join('');

        // ── Verdict
        const winner = d1.score >= d2.score ? name1 : name2;
        const loser  = d1.score >= d2.score ? name2 : name1;
        const wData  = d1.score >= d2.score ? d1 : d2;
        const lData  = d1.score >= d2.score ? d2 : d1;

        document.getElementById('verdictText').innerHTML = `
            <div class="verdict-winner">
                <strong>${winner}</strong> is the better resume for this job with an ATS score of <strong>${wData.score}%</strong>
                and resume strength of <strong>${wData.strength_score}%</strong>.
            </div>
            <div class="verdict-tips">
                <p>💡 To improve <strong>${loser}</strong>:</p>
                <ul>
                    <li>Add these missing keywords: <strong>${lData.missing_keywords.slice(0,5).join(', ')}</strong></li>
                    <li>Current ATS score is ${lData.score}% — aim for 70%+ by tailoring to the job description</li>
                    <li>Focus on improving the weakest section to close the gap</li>
                </ul>
            </div>
        `;

        document.getElementById('compareResults').style.display = 'block';
        document.getElementById('compareResults').scrollIntoView({ behavior: 'smooth' });

    } catch(err) {
        alert('Something went wrong. Please try again.');
    }

    btn.textContent = '⚖️ Compare Now';
    btn.disabled = false;
}