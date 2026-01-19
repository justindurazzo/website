// Intro animation and transition
document.addEventListener('DOMContentLoaded', () => {
    const intro = document.getElementById('intro');
    const body = document.body;

    const hasSeenIntro = sessionStorage.getItem('hasSeenIntro');
    const isInternalNavigation = document.referrer.includes(window.location.hostname);

    if (intro && (hasSeenIntro || isInternalNavigation)) {
        intro.remove();
        body.classList.add('loaded');
        return;
    }

    if (intro) {
        sessionStorage.setItem('hasSeenIntro', 'true');
        setTimeout(() => {
            intro.classList.add('hidden');
            body.classList.add('loaded');
        }, 2000);
        setTimeout(() => {
            intro.remove();
        }, 3000);
    } else {
        body.classList.add('loaded');
    }
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
if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
    });
}
