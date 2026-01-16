// Intro animation and transition
document.addEventListener('DOMContentLoaded', () => {
    const intro = document.getElementById('intro');
    const body = document.body;

    // After intro animations complete, fade out overlay and reveal main content
    setTimeout(() => {
        intro.classList.add('hidden');
        body.classList.add('loaded');
    }, 2000);

    // Remove intro from DOM after transition
    setTimeout(() => {
        intro.remove();
    }, 3000);
});

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));

        if (target) {
            const headerOffset = 80;
            const elementPosition = target.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// Theme toggle
const themeToggle = document.getElementById('themeToggle');

// Clear any old theme preference and default to light
localStorage.removeItem('theme');
document.body.classList.remove('dark-mode');
if (themeToggle) themeToggle.textContent = 'Dark';

if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        const isDark = document.body.classList.contains('dark-mode');
        themeToggle.textContent = isDark ? 'Light' : 'Dark';
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });
}
