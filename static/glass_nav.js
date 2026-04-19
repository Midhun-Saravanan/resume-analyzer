// ── Profile Dropdown ───────────────────────────────────────
function initProfileDropdown() {
    const btn      = document.getElementById('profileBtn');
    const dropdown = document.getElementById('profileDropdown');
    if (!btn || !dropdown) return;

    btn.addEventListener('click', (e) => {
        e.stopPropagation();
        btn.classList.toggle('open');
        dropdown.classList.toggle('open');
    });

    document.addEventListener('click', () => {
        btn.classList.remove('open');
        dropdown.classList.remove('open');
    });
}

// ── Toast Notifications ────────────────────────────────────
function showToast(message, type = 'info', duration = 3000) {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const icons = { success: '✅', error: '❌', info: 'ℹ️', warning: '⚠️' };
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<span>${icons[type] || 'ℹ️'}</span><span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'toastOut 0.3s ease forwards';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

// ── Dark Mode (always dark for glass theme) ────────────────
function toggleDarkMode() {
    // Glass theme is always dark — button just for consistency
    showToast('Glass theme is always dark mode! 🌙', 'info');
}

// ── Init ───────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', initProfileDropdown);