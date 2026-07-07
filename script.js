// ============================================================
// Sound Effects System
// ============================================================
const SoundFX = {
    enabled: true,
    volume: 0.15,

    init() {
        try { this.audioContext = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) { this.audioContext = null; }
        const savedPref = localStorage.getItem('soundEnabled');
        if (savedPref !== null) {
            this.enabled = savedPref === 'true';
        } else {
            // First-time visitor: explicitly set sound to ON
            localStorage.setItem('soundEnabled', 'true');
        }
        this.updateToggleButton();
    },

    playTick(frequency = 800, duration = 0.03) {
        // Resume AudioContext if suspended (browser autoplay policy)
        if (this.audioContext.state === 'suspended') {
            this.audioContext.resume();
        }
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
            const speakerOnSVG = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/></svg>';
            const speakerOffSVG = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4z"/></svg>';
            btn.innerHTML = this.enabled ? speakerOnSVG : speakerOffSVG;
        }
    }
};

// ============================================================
// Environment
// ============================================================
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const isTouch = window.matchMedia('(hover: none), (pointer: coarse)').matches;

// ============================================================
// Lenis smooth scroll  (buttery momentum, the core "aaru feel")
// ============================================================
let lenis = null;
function initLenis() {
    if (prefersReducedMotion || typeof Lenis === 'undefined') return;
    lenis = new Lenis({
        duration: 1.1,
        easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)), // expo-out
        smoothWheel: true,
        wheelMultiplier: 1,
        touchMultiplier: 1.6,
    });
    function raf(time) {
        lenis.raf(time);
        requestAnimationFrame(raf);
    }
    requestAnimationFrame(raf);
    window.lenis = lenis;
}

// Unified scroll helper, routes through Lenis when available
function scrollToTarget(target, offset = -80) {
    if (lenis) {
        lenis.scrollTo(target, { offset, duration: 1.2 });
    } else {
        const el = typeof target === 'string' ? document.querySelector(target) : target;
        const top = typeof target === 'number'
            ? target
            : el.getBoundingClientRect().top + window.pageYOffset + offset;
        window.scrollTo({ top, behavior: 'smooth' });
    }
}

// ============================================================
// Kinetic text reveals  (mask + rise + de-blur, staggered)
// ============================================================
function wrapWords(el) {
    const text = el.textContent.trim();
    const words = text.split(/\s+/);
    el.textContent = '';
    words.forEach((word, i) => {
        const mask = document.createElement('span');
        mask.className = 'line line--inline';
        const inner = document.createElement('span');
        inner.className = 'line-inner';
        inner.style.setProperty('--i', i);
        inner.textContent = word;
        mask.appendChild(inner);
        el.appendChild(mask);
        // preserve the space between words (masks are inline-block)
        if (i < words.length - 1) el.appendChild(document.createTextNode(' '));
    });
}

function wrapLine(el) {
    const text = el.textContent.trim();
    const mask = document.createElement('span');
    mask.className = 'line';
    const inner = document.createElement('span');
    inner.className = 'line-inner';
    inner.textContent = text;
    mask.appendChild(inner);
    el.textContent = '';
    el.appendChild(mask);
    return mask;
}

function setupReveals() {
    if (prefersReducedMotion) return;

    // Intro paragraph, word-by-word
    const introText = document.querySelector('.intro-text');
    if (introText) wrapWords(introText);

    // Project titles, single masked line
    document.querySelectorAll('.project-title').forEach((title) => {
        // skip if it wraps a link (keep the anchor intact)
        if (title.querySelector('a')) return;
        wrapLine(title);
    });
}

// ============================================================
// Project media, wrap for clip-reveal + enable hover-to-play
// ============================================================
function setupProjectMedia() {
    document.querySelectorAll('.project').forEach((project) => {
        const media = project.querySelector('.project-image');
        if (!media || media.closest('.project-media')) return;

        const wrapper = document.createElement('div');
        wrapper.className = 'project-media';
        media.parentNode.insertBefore(wrapper, media);
        wrapper.appendChild(media);

        if (media.tagName === 'VIDEO') {
            media.muted = true;
            media.loop = true;
            media.playsInline = true;
            if (!isTouch) {
                // hover-to-play
                wrapper.addEventListener('mouseenter', () => {
                    const p = media.play();
                    if (p && p.catch) p.catch(() => {});
                });
                wrapper.addEventListener('mouseleave', () => {
                    media.pause();
                });
            }
            // tap / click toggles playback (native controls removed)
            wrapper.addEventListener('click', () => {
                if (media.paused) {
                    const p = media.play();
                    if (p && p.catch) p.catch(() => {});
                } else {
                    media.pause();
                }
            });
        }
    });
}

// ============================================================
// Media cursor, a 'View / Play' bubble over project media only.
// The native system cursor is used everywhere else.
// ============================================================
function initMediaCursor() {
    if (isTouch || prefersReducedMotion) return;
    const cursor = document.getElementById('cursor');
    if (!cursor) return;
    const label = cursor.querySelector('.cursor-label');
    const PLAY_ICON = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>';
    document.body.classList.add('has-media-cursor');

    let targetX = 0, targetY = 0, curX = 0, curY = 0;
    let active = false;

    document.querySelectorAll('.project-media').forEach((media) => {
        const isVideo = !!media.querySelector('video');
        media.addEventListener('mouseenter', (e) => {
            // snap to entry point so the bubble doesn't fly in from a stale spot
            targetX = curX = e.clientX;
            targetY = curY = e.clientY;
            if (isVideo) label.innerHTML = PLAY_ICON;
            else label.textContent = 'View';
            cursor.style.transform = `translate3d(${curX}px, ${curY}px, 0)`;
            cursor.classList.add('is-media');
            active = true;
        });
        media.addEventListener('mousemove', (e) => {
            targetX = e.clientX;
            targetY = e.clientY;
        });
        media.addEventListener('mouseleave', () => {
            cursor.classList.remove('is-media');
            active = false;
        });
    });

    function render() {
        if (active) {
            curX += (targetX - curX) * 0.2;
            curY += (targetY - curY) * 0.2;
            cursor.style.transform = `translate3d(${curX}px, ${curY}px, 0)`;
        }
        requestAnimationFrame(render);
    }
    requestAnimationFrame(render);
}

// ============================================================
// Boot
// ============================================================
document.addEventListener('DOMContentLoaded', () => {
    const intro = document.getElementById('intro');
    const body = document.body;

    SoundFX.init();

    // Resume AudioContext on first user interaction (browser autoplay policy)
    const resumeAudio = () => {
        if (SoundFX.audioContext && SoundFX.audioContext.state === 'suspended') {
            SoundFX.audioContext.resume();
        }
        document.removeEventListener('mousemove', resumeAudio);
    };
    document.addEventListener('mousemove', resumeAudio);

    // Prepare motion features
    setupReveals();
    setupProjectMedia();
    initLenis();
    initMediaCursor();

    const revealIntro = () => {
        const introText = document.querySelector('.intro-text');
        if (introText) introText.classList.add('is-in');
    };

    const hasSeenIntro = sessionStorage.getItem('hasSeenIntro');
    const isInternalNavigation = document.referrer.includes(window.location.hostname);

    if (intro && (hasSeenIntro || isInternalNavigation)) {
        intro.remove();
        body.classList.add('loaded');
        revealIntro();
    } else if (intro) {
        sessionStorage.setItem('hasSeenIntro', 'true');
        setTimeout(() => {
            intro.classList.add('hidden');
            body.classList.add('loaded');
            revealIntro();
        }, 2000);
        setTimeout(() => {
            intro.remove();
        }, 3000);
    } else {
        body.classList.add('loaded');
        revealIntro();
    }

    // hover / click sounds
    document.querySelectorAll('a, button').forEach(el => {
        el.addEventListener('mouseenter', () => SoundFX.hover());
        el.addEventListener('click', () => SoundFX.click());
    });
});

// ============================================================
// Anchor smooth scroll (routed through Lenis)
// ============================================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href === '#') return; // handled by back-to-top
        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
            SoundFX.navigate();
            scrollToTarget(target, -80);
        }
    });
});

// ============================================================
// Theme toggle
// ============================================================
const themeToggle = document.getElementById('themeToggle');
if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        const isDark = document.body.classList.contains('dark-mode');
        const sunIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>';
        const moonIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M9 2c-1.05 0-2.05.16-3 .46 4.06 1.27 7 5.06 7 9.54 0 4.48-2.94 8.27-7 9.54.95.3 1.95.46 3 .46 5.52 0 10-4.48 10-10S14.52 2 9 2z"/></svg>';
        themeToggle.innerHTML = isDark ? sunIcon : moonIcon;
    });
}

// ============================================================
// Scroll Progress Indicator
// ============================================================
const scrollIndicator = document.getElementById('scrollIndicator');
const scrollTrack = document.getElementById('scrollTrack');
if (scrollIndicator && scrollTrack) {
    const projects = document.querySelectorAll('.project');
    projects.forEach((project, i) => {
        const dot = document.createElement('div');
        dot.classList.add('scroll-indicator-dot');
        dot.addEventListener('click', () => {
            SoundFX.navigate();
            scrollToTarget(project, -80);
        });
        dot.addEventListener('mouseenter', () => SoundFX.hover());
        scrollTrack.appendChild(dot);
    });

    scrollTrack.addEventListener('click', (e) => {
        if (e.target.classList.contains('scroll-indicator-dot')) return;
        const rect = scrollTrack.getBoundingClientRect();
        const ratio = (e.clientY - rect.top) / rect.height;
        const index = Math.min(Math.floor(ratio * projects.length), projects.length - 1);
        SoundFX.navigate();
        scrollToTarget(projects[index], -80);
    });

    const dots = scrollTrack.querySelectorAll('.scroll-indicator-dot');
    let ticking = false;
    let inWorkSection = false;
    let mouseTimeout = null;

    function showIndicator() {
        if (inWorkSection) scrollIndicator.classList.add('visible');
        clearTimeout(mouseTimeout);
        mouseTimeout = setTimeout(() => {
            scrollIndicator.classList.remove('visible');
        }, 2000);
    }

    document.addEventListener('mousemove', showIndicator);

    scrollIndicator.addEventListener('mouseenter', () => {
        clearTimeout(mouseTimeout);
        if (inWorkSection) scrollIndicator.classList.add('visible');
    });
    scrollIndicator.addEventListener('mouseleave', () => {
        mouseTimeout = setTimeout(() => {
            scrollIndicator.classList.remove('visible');
        }, 2000);
    });

    const onScroll = () => {
        if (!ticking) {
            requestAnimationFrame(() => {
                const scrollY = window.scrollY;
                const workSection = document.getElementById('work');
                if (workSection) {
                    const workTop = workSection.offsetTop - 200;
                    const workBottom = workSection.offsetTop + workSection.offsetHeight;
                    inWorkSection = scrollY >= workTop && scrollY < workBottom;
                }
                if (inWorkSection) {
                    showIndicator();
                } else {
                    scrollIndicator.classList.remove('visible');
                }
                dots.forEach((dot, i) => {
                    const project = projects[i];
                    const rect = project.getBoundingClientRect();
                    const inView = rect.top < window.innerHeight * 0.5 && rect.bottom > window.innerHeight * 0.3;
                    dot.classList.toggle('active', inView);
                });
                ticking = false;
            });
            ticking = true;
        }
    };
    window.addEventListener('scroll', onScroll);
    if (window.lenis) window.lenis.on('scroll', onScroll);
}

// ============================================================
// Project reveal on scroll (fade + clip + title mask)
// ============================================================
const projectObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            const titleLine = entry.target.querySelector('.project-title .line');
            if (titleLine) titleLine.classList.add('is-in');
            projectObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
document.querySelectorAll('.project').forEach(p => projectObserver.observe(p));

// ============================================================
// Sound toggle
// ============================================================
const soundToggle = document.getElementById('soundToggle');
if (soundToggle) {
    soundToggle.addEventListener('click', () => SoundFX.toggle());
}

// ============================================================
// Hamburger menu + Back to top
// ============================================================
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('nav');
if (hamburger && navMenu) {
    hamburger.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        SoundFX.click();
    });
}

const backToTop = document.querySelector('.back-to-top');
if (backToTop) {
    backToTop.addEventListener('click', (e) => {
        e.preventDefault();
        SoundFX.navigate();
        scrollToTarget(0, 0);
    });
}
