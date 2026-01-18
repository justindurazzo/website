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

// Sound toggle with Material Design icons
const soundToggle = document.getElementById('soundToggle');

// SVG icons (Material Design style - solid/filled)
const speakerOnSVG = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/></svg>';
const speakerOffSVG = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4z"/></svg>';

// Initialize sound state (default: on)
let soundEnabled = localStorage.getItem('soundEnabled') !== 'false';

function updateSoundButton() {
        if (soundToggle) {
                    soundToggle.innerHTML = soundEnabled 
                ? speakerOnSVG + ' On' 
                                    : speakerOffSVG + ' Off';
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

// Also update videos when they start playing (for dynamically loaded content)
document.addEventListener('play', (e) => {
        if (e.target.tagName === 'VIDEO') {
                    e.target.muted = !soundEnabled;
        }
}, true);

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
