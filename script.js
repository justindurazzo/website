// Intro animation and transition
document.addEventListener('DOMContentLoaded', () => {
    const intro = document.getElementById('intro');
    const body = document.body;

    // Skip intro if already seen this session or coming from internal link
    const hasSeenIntro = sessionStorage.getItem('hasSeenIntro');
    const isInternalNavigation = document.referrer.includes(window.location.hostname);

    if (intro && (hasSeenIntro || isInternalNavigation)) {
        // Skip intro animation
        intro.remove();
        body.classList.add('loaded');
        return;
    }

    if (intro) {
        // Mark that user has seen intro
        sessionStorage.setItem('hasSeenIntro', 'true');

        // After intro animations complete, fade out overlay and reveal main content
        setTimeout(() => {
            intro.classList.add('hidden');
            body.classList.add('loaded');
        }, 2000);

        // Remove intro from DOM after transition
        setTimeout(() => {
            intro.remove();
        }, 3000);
    } else {
        // No intro element, just show content
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

// Sound toggle
const soundToggle = document.getElementById('soundToggle');

// Initialize sound state (default: on)
let soundEnabled = localStorage.getItem('soundEnabled') !== 'false';

function updateSoundButton() {
    if (soundToggle) {
        soundToggle.innerHTML = soundEnabled 
            ? '🔊 On' 
            : '🔇 Off';
    }
}

function updateVideosMuted() {
    const videos = document.querySelectorAll('video');
    videos.forEach(video => {
        video.muted = !soundEnabled;
    });
}

// Set initial state
updateSoundButton();
updateVideosMuted();

if (soundToggle) {
    soundToggle.addEventListener('click', () => {
        soundEnabled = !soundEnabled;
        localStorage.setItem('soundEnabled', soundEnabled);
        updateSoundButton();
        updateVideosMuted();
    });
}

// Hamburger menu toggle
const hamburger = document.getElementById('hamburger');
const nav = document.querySelector('.nav');

if (hamburger && nav) {
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        nav.classList.toggle('active');
    });
}
