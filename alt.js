// ============================================================
// Justin Durazzo — ALT landing (MLF-inspired) interactions
// ============================================================
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const isTouch = window.matchMedia('(hover: none), (pointer: coarse)').matches;

// ---------- Sound design (ported from justindurazzo.com) ----------
const SPEAKER_ON = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/></svg>';
const SPEAKER_OFF = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4z"/></svg>';

const SoundFX = {
    enabled: true,
    volume: 0.15,
    init() {
        try { this.audioContext = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) { this.audioContext = null; }
        const saved = localStorage.getItem('soundEnabled');
        if (saved !== null) this.enabled = saved === 'true';
        else localStorage.setItem('soundEnabled', 'true');
        this.updateToggle();
    },
    playTick(frequency = 800, duration = 0.03) {
        if (!this.audioContext) return;
        if (this.audioContext.state === 'suspended') this.audioContext.resume();
        if (!this.enabled) return;
        const osc = this.audioContext.createOscillator();
        const gain = this.audioContext.createGain();
        osc.connect(gain); gain.connect(this.audioContext.destination);
        osc.frequency.value = frequency; osc.type = 'sine';
        gain.gain.setValueAtTime(this.volume, this.audioContext.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.audioContext.currentTime + duration);
        osc.start(this.audioContext.currentTime);
        osc.stop(this.audioContext.currentTime + duration);
    },
    hover() { this.playTick(600, 0.02); },
    click() { this.playTick(800, 0.04); },
    navigate() { this.playTick(500, 0.06); },
    toggle() {
        this.enabled = !this.enabled;
        localStorage.setItem('soundEnabled', this.enabled);
        this.updateToggle();
        if (this.enabled) this.click();
    },
    updateToggle() {
        const btn = document.getElementById('soundToggle');
        if (btn) btn.innerHTML = this.enabled ? SPEAKER_ON : SPEAKER_OFF;
    }
};

// ---------- Lenis smooth scroll ----------
let lenis = null;
if (!reduce && typeof Lenis !== 'undefined') {
    lenis = new Lenis({
        duration: 1.15,
        easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
        smoothWheel: true,
    });
    const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); };
    requestAnimationFrame(raf);
}
function scrollTo(target) {
    const el = typeof target === 'string' ? document.querySelector(target) : target;
    if (!el) return;
    if (lenis) lenis.scrollTo(el, { offset: 0, duration: 1.2 });
    else el.scrollIntoView({ behavior: 'smooth' });
}
document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener('click', (e) => {
        const id = a.getAttribute('href');
        if (id.length < 2) return;
        const el = document.querySelector(id);
        if (el) { e.preventDefault(); scrollTo(el); }
    });
});

// ---------- Load wipe → reveal hero + sound + toggles ----------
window.addEventListener('DOMContentLoaded', () => {
    const wipe = document.getElementById('wipe');
    const reveal = () => {
        document.body.classList.add('loaded');
        if (wipe) wipe.classList.add('lift');
    };
    // Skip the "Justin Durazzo" intro on internal navigation (e.g. clicking the
    // logo / home) or once it's already been seen this session.
    const host = window.location.hostname;
    const internalNav = !!document.referrer && document.referrer.includes(host);
    const seenIntro = sessionStorage.getItem('introSeen') === 'true';
    if (reduce || !wipe || internalNav || seenIntro) {
        reveal();
        if (wipe) wipe.remove();
    } else {
        sessionStorage.setItem('introSeen', 'true');
        setTimeout(reveal, 1350);
    }

    // hero video: ensure it plays (autoplay can be blocked until interaction)
    const hero = document.getElementById('heroVideo');
    if (hero) { const p = hero.play(); if (p && p.catch) p.catch(() => {}); }

    // sound design
    SoundFX.init();
    const resumeAudio = () => {
        if (SoundFX.audioContext && SoundFX.audioContext.state === 'suspended') SoundFX.audioContext.resume();
        document.removeEventListener('mousemove', resumeAudio);
        document.removeEventListener('touchstart', resumeAudio);
    };
    document.addEventListener('mousemove', resumeAudio);
    document.addEventListener('touchstart', resumeAudio);
    document.querySelectorAll('a, button').forEach((el) => {
        el.addEventListener('mouseenter', () => SoundFX.hover());
        el.addEventListener('click', () => SoundFX.click());
    });

    // sound toggle
    const soundToggle = document.getElementById('soundToggle');
    if (soundToggle) soundToggle.addEventListener('click', () => SoundFX.toggle());

    // theme toggle (dark ⇆ light) — icon shows the mode you'll switch TO
    const SUN = document.querySelector('#themeToggle svg').outerHTML;
    const MOON = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M9 2c-1.05 0-2.05.16-3 .46 4.06 1.27 7 5.06 7 9.54 0 4.48-2.94 8.27-7 9.54.95.3 1.95.46 3 .46 5.52 0 10-4.48 10-10S14.52 2 9 2z"/></svg>';
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const light = document.body.classList.toggle('light');
            themeToggle.innerHTML = light ? MOON : SUN;
        });
    }
});

// ---------- Reveal on scroll ----------
// stagger the statement words
document.querySelectorAll('.statement-text .sw').forEach((w, i) => {
    w.style.setProperty('--wi', i);
});

const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add('in');
            revealObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.18, rootMargin: '0px 0px -8% 0px' });

document.querySelectorAll('[data-reveal], .card, .tile').forEach((el) => revealObserver.observe(el));

// ---------- MLF-style autoplay previews (lazy + in-view) ----------
// data-start = first-play in-point; data-loop-start = in-point on every loop;
// data-end = loop back once reached (so the preview loops just one section).
// The click-to-watch lightbox always plays the full film from 0.
const cardVideos = document.querySelectorAll('.card-media video[data-src]');
const firstStartOf = (v) => parseFloat(v.dataset.start) || 0;
const loopStartOf = (v) => (v.dataset.loopStart != null ? parseFloat(v.dataset.loopStart) : firstStartOf(v)) || 0;
const endOf = (v) => parseFloat(v.dataset.end) || 0;
const managed = (v) => firstStartOf(v) > 0 || v.dataset.loopStart != null || endOf(v) > 0;
const seekTo = (v, t) => { try { v.currentTime = t; } catch (e) {} };

const videoObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        const v = entry.target;
        if (entry.isIntersecting) {
            if (!v.src) v.src = v.dataset.src;   // lazy-load as it approaches
            // before the first playthrough finishes, hold the first-play in-point
            const start = firstStartOf(v);
            if (start > 0 && v.readyState >= 1 && !v.dataset.looped && v.currentTime < start) seekTo(v, start);
            const p = v.play();
            if (p && p.catch) p.catch(() => {});
        } else {
            if (v.src) v.pause();
        }
    });
}, { threshold: 0, rootMargin: '700px 0px 700px 0px' });   // preload & start a screen early

cardVideos.forEach((v) => {
    if (managed(v)) {
        v.loop = false; // we manage the loop so it returns to the chosen in-point
        v.addEventListener('loadedmetadata', () => seekTo(v, firstStartOf(v)));
        // loop back at the section end (data-end), otherwise at the real end
        v.addEventListener('timeupdate', () => {
            const end = endOf(v);
            if (end > 0 && v.currentTime >= end) {
                v.dataset.looped = '1';
                seekTo(v, loopStartOf(v));
            }
        });
        v.addEventListener('ended', () => {
            v.dataset.looped = '1';           // subsequent loops use loopStart
            seekTo(v, loopStartOf(v));
            const p = v.play();
            if (p && p.catch) p.catch(() => {});
        });
    }
    videoObserver.observe(v);
});

// ---------- Project lightbox — click a card/tile to watch + read ----------
const lightbox = document.getElementById('lightbox');
if (lightbox) {
    const lbMedia = document.getElementById('lightboxMedia');
    const lbCat = document.getElementById('lightboxCat');
    const lbTitle = document.getElementById('lightboxTitle');
    const lbDesc = document.getElementById('lightboxDesc');
    const lbClose = document.getElementById('lightboxClose');

    const open = (el) => {
        const titleEl = el.querySelector('.card-title, .tile-title');
        const catEl = el.querySelector('.card-cat, .tile-cat');
        const descEl = el.querySelector('.card-desc');
        const videoEl = el.querySelector('video[data-src]');
        const imgEl = el.querySelector('img');

        lbTitle.textContent = titleEl ? titleEl.textContent.trim() : '';
        lbCat.textContent = catEl ? catEl.textContent.trim() : '';
        lbDesc.textContent = descEl ? descEl.textContent.trim() : (el.dataset.full || '');

        lbMedia.innerHTML = '';
        if (videoEl && videoEl.dataset.src) {
            const v = document.createElement('video');
            v.src = videoEl.dataset.src;
            v.controls = true;
            v.autoplay = true;
            v.loop = true;
            v.playsInline = true;
            lbMedia.appendChild(v);
            const p = v.play();
            if (p && p.catch) p.catch(() => {});
        } else if (imgEl) {
            const img = document.createElement('img');
            img.src = imgEl.currentSrc || imgEl.src;
            img.alt = imgEl.alt || '';
            lbMedia.appendChild(img);
        }

        lightbox.classList.add('open');
        lightbox.setAttribute('aria-hidden', 'false');
        document.body.classList.add('lb-open');
        if (lenis) lenis.stop();
    };

    const close = () => {
        lightbox.classList.remove('open');
        lightbox.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('lb-open');
        setTimeout(() => { lbMedia.innerHTML = ''; }, 450); // stop playback after fade-out
        if (lenis) lenis.start();
    };

    document.querySelectorAll('.card, .tile').forEach((el) => {
        el.addEventListener('click', (e) => {
            e.preventDefault();
            open(el);
        });
    });
    lbClose.addEventListener('click', close);
    lightbox.addEventListener('click', (e) => { if (e.target === lightbox) close(); });
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && lightbox.classList.contains('open')) close();
    });
}

// ---------- Back to top ----------
const backToTop = document.getElementById('backToTop');
if (backToTop) {
    backToTop.addEventListener('click', (e) => {
        e.preventDefault();
        if (lenis) lenis.scrollTo(0, { duration: 1.2 });
        else window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// ---------- Side scroll indicator (featured work) ----------
const sideNav = document.getElementById('sideNav');
const featured = document.querySelectorAll('.card');
if (sideNav && featured.length) {
    featured.forEach((card, i) => {
        const dot = document.createElement('button');
        dot.type = 'button';
        dot.className = 'side-dot';
        dot.setAttribute('aria-label', 'Go to featured project ' + (i + 1));
        dot.addEventListener('click', () => {
            if (lenis) lenis.scrollTo(card, { offset: -80, duration: 1.2 });
            else card.scrollIntoView({ behavior: 'smooth' });
        });
        sideNav.appendChild(dot);
    });
    const dots = sideNav.querySelectorAll('.side-dot');

    // active dot = the card crossing the viewport's vertical center
    const activeObs = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                const idx = Array.prototype.indexOf.call(featured, entry.target);
                dots.forEach((d, j) => d.classList.toggle('active', j === idx));
            }
        });
    }, { rootMargin: '-50% 0px -50% 0px', threshold: 0 });
    featured.forEach((c) => activeObs.observe(c));

    // show the indicator only while the featured work section is on screen
    const work = document.querySelector('.work');
    if (work) {
        const visObs = new IntersectionObserver((entries) => {
            entries.forEach((e) => sideNav.classList.toggle('visible', e.isIntersecting));
        }, { rootMargin: '-8% 0px -8% 0px' });
        visObs.observe(work);
    }
}

