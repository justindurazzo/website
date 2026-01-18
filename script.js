// Sound Effects System
const SoundFX = {
        enabled: true,
        volume: 0.15,
        sounds: {},

        init() {
                    // Create subtle UI sounds using Web Audio API
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();

            // Load sound preference
            const savedPref = localStorage.getItem('soundEnabled');
                    if (savedPref !== null) {
                                    this.enabled = savedPref === 'true';
                    }
                    this.updateToggleButton();
        },

        // Generate a subtle tick sound
        playTick(frequency = 800, duration = 0.03) {
                    if (!this.enabled || !this.audioContext) return;

            const oscillator = this.audioContext.createOscillator();
                    const gainNode = this.audioContext.createGain();

            oscillator.connect(gainNode);
                    gainNode.connect(this.audioContext.destination);

            oscillator.frequency.value = frequency;
                    oscillator.type = 'sine';

            gainNode.gain.setValueAtTime(this.volume, this.audioContext.currentTime);
                    gainNode.gain.exponentialRampToValueAtTime(0.001, this.audioContext.currentTime + duration);

            oscillator.start(this.audioContext.currentTime);
                    oscillator.stop(this.audioContext.currentTime + duration);
        },

        hover() { this.playTick(600, 0.02); },
        click() { this.playTick(800, 0.04); },
        navigate() { this.playTick(500, 0.06); },

        toggle() {
                    this.enabled = !this.enabled;
                    localStorage.setItem('soundEnabled', this.enabled);
                    this.updateToggleButton();
                    if (this.enabled) this.click();
        },

        updateToggleButton() {
                    const btn = document.getElementById('soundToggle');
                    if (btn) {
                                    btn.textContent = this.enabled ? 'SOUND' : 'MUTE';
                                    btn.classList.toggle('muted', !this.enabled);
                    }
        }
};

// Initialize on first user interaction (required for Web Audio)
let audioInitialized = false;
document.addEventListener('click', () => {
        if (!audioInitialized) {
                    SoundFX.init();
                    audioInitialized = true;
        }
}, { once: true });

// Intro animation and transition
document.addEventListener('DOMContentLoaded', () => {
        const intro = document.getElementById('intro');
        const body = document.body;

                              setTimeout(() => {
                                          intro.classList.add('hidden');
                                          body.classList.add('loaded');
                              }, 2000);

                              setTimeout(() => {
                                          intro.remove();
                              }, 3000);

                              addSoundEffects();
});

function addSoundEffects() {
        document.querySelectorAll('a, button, .project').forEach(el => {
                    el.addEventListener('mouseenter', () => SoundFX.hover());
                    el.addEventListener('click', () => SoundFX.click());
        });

    document.querySelectorAll('a[href^="#"]').forEach(link => {
                link.addEventListener('click', () => {
                                setTimeout(() => SoundFX.navigate(), 100);
                });
    });
}

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
                    e.preventDefault();
                    const target = document.querySelector(this.getAttribute('href'));
                    if (target) {
                                    window.scrollTo({
                                                        top: target.getBoundingClientRect().top + window.pageYOffset - 80,
                                                        behavior: 'smooth'
                                    });
                    }
        });
});

// Theme toggle
const themeToggle = document.getElementById('themeToggle');
localStorage.removeItem('theme');
document.body.classList.remove('dark-mode');
if (themeToggle) themeToggle.textContent = 'DARK';

if (themeToggle) {
        themeToggle.addEventListener('click', () => {
                    document.body.classList.toggle('dark-mode');
                    const isDark = document.body.classList.contains('dark-mode');
                    themeToggle.textContent = isDark ? 'LIGHT' : 'DARK';
                    localStorage.setItem('theme', isDark ? 'dark' : 'light');
        });
}

// Sound toggle
const soundToggle = document.getElementById('soundToggle');
if (soundToggle) {
        soundToggle.addEventListener('click', () => SoundFX.toggle());
}
