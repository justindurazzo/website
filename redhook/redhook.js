// ============================================================
// The Red Hook Focacceria, interactions
// Vanilla JS, no dependencies. Guards every lookup so the same
// script is safe on any page. Respects reduced-motion.
// ============================================================
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---------- Reveal on load ----------
  document.body.classList.add('loaded');

  // ---------- Reveal on scroll ----------
  var revealEls = document.querySelectorAll('[data-reveal]');
  if (reduce || !('IntersectionObserver' in window)) {
    revealEls.forEach(function (el) { el.classList.add('in'); });
  } else {
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.16, rootMargin: '0px 0px -8% 0px' });
    revealEls.forEach(function (el) { revealObserver.observe(el); });
  }

  // ---------- Nav: scrolled border + smooth anchor scroll ----------
  var nav = document.getElementById('nav');
  var onScrollNav = function () {
    if (nav) nav.classList.toggle('scrolled', window.scrollY > 24);
  };
  onScrollNav();
  window.addEventListener('scroll', onScrollNav, { passive: true });

  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href');
      if (id.length < 2) return;
      var el = document.querySelector(id);
      if (!el) return;
      e.preventDefault();
      closeMenu();
      el.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    });
  });

  // ---------- Mobile menu ----------
  var toggle = document.getElementById('navToggle');
  function closeMenu() {
    document.body.classList.remove('menu-open');
    if (toggle) toggle.setAttribute('aria-expanded', 'false');
  }
  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = document.body.classList.toggle('menu-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeMenu();
    });
  }

  // ---------- Timeline: spine fill + light up each era ----------
  var timeline = document.getElementById('timeline');
  var fill = document.getElementById('timelineFill');
  var eras = Array.prototype.slice.call(document.querySelectorAll('.era'));

  if (timeline && fill) {
    var updateFill = function () {
      var rect = timeline.getBoundingClientRect();
      var vh = window.innerHeight;
      // progress of the timeline through the viewport middle
      var start = rect.top - vh * 0.62;
      var span = rect.height + vh * 0.24;
      var p = Math.min(1, Math.max(0, -start / span));
      fill.style.height = (p * 100) + '%';
    };
    updateFill();
    window.addEventListener('scroll', updateFill, { passive: true });
    window.addEventListener('resize', updateFill);
  }

  if (eras.length && 'IntersectionObserver' in window) {
    var eraObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) entry.target.classList.add('lit');
      });
    }, { threshold: 0.5, rootMargin: '0px 0px -20% 0px' });
    eras.forEach(function (el) { eraObserver.observe(el); });
  } else {
    eras.forEach(function (el) { el.classList.add('lit'); });
  }
})();
