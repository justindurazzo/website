# GAPS.md, honest weakness audit

Ordered by severity, most important first. Each entry: what it is, where it
lives, why it matters, and a small suggested fix. This is a static portfolio
site with no backend, so most risks are "the page looks broken to a visitor" or
"a future edit silently breaks something", not classic server security holes.

Severity is honest: there is currently **no Critical** item (the worst one, a
blank page on JS failure, is already mitigated by the `<noscript>` + failsafe).

---

## HIGH

### H1. Git LFS is declared but not used; new mp4s can deploy as broken pointer files
- **Where**: `.gitattributes` (`*.mp4 filter=lfs diff=lfs merge=lfs -text`). Verify
  with `git lfs ls-files` (returns nothing) and `git show HEAD:images/projects/forager.mp4 | head -c 20`
  (real mp4 bytes, not a `version https://git-lfs...` pointer).
- **Why it matters**: the existing mp4s are committed as normal git blobs, so the
  site works today. But the attribute tells any contributor whose machine has
  git-lfs installed to store the NEXT mp4 as an LFS pointer. Vercel's build does
  not run `git lfs` by default, so that pointer would be served as a tiny text
  file and the video would silently 404 in production. It also means large
  binaries (36 MB Thorne clip and others) are bloating normal git history.
- **Fix (small)**: since nothing is actually in LFS, delete the LFS line from
  `.gitattributes` so all mp4s (existing and future) are plain blobs and behave
  consistently. (The larger, optional alternative is to properly migrate to LFS
  and enable LFS checkout on Vercel, but that is a bigger task and not needed.)

### H2. The "In Her Head" featured card renders as a permanent blank box
- **Where**: `index.html:141-146` (the card `<video>` has `data-static` and
  `data-poster` but no `poster` and no `src`), and `alt.js:157` (`cardVideos`
  selector is `...video[data-src]:not([data-static])`, which EXCLUDES it).
- **Why it matters**: because the video is excluded from `cardVideos`, the
  observer never runs on it, so its `src` is never loaded AND its `data-poster`
  is never promoted to a real `poster`. The `<video>` has no frame and no poster,
  so the LPGA / In Her Head card shows as an empty placeholder rectangle on the
  homepage until a visitor clicks it (the lightbox still works). A featured
  project looks broken.
- **Fix (small)**: in `alt.js`, after the `cardVideos` block, add a one-time loop
  that gives static cards their poster:
  ```js
  document.querySelectorAll('.card-media video[data-static], .tile-media video[data-static]')
    .forEach((v) => { if (v.dataset.poster && !v.getAttribute('poster')) v.setAttribute('poster', v.dataset.poster); });
  ```
  (Alternatively, drop `data-static` from the card if a moving preview is wanted.)

### H3. Zero automated tests; every critical JS path is unverified
- **Where**: whole repo. There is no test file, runner, or CI.
- **Why it matters**: the load-bearing behaviors (wipe/reveal, the JS-failure
  failsafe, lightbox open/close scroll-lock, video section-looping, theme
  persistence) can only regress silently. A one-character change to a class name
  used by the failsafe (`loaded`) would blank the page and nothing would catch it.
- **Fix (small, first step)**: add a single Playwright smoke test that loads
  `index.html`, asserts the `#wipe` overlay is gone and `.hero-title` is visible
  after load, opens and closes the lightbox, toggles the theme and reloads to
  assert `body.light` persisted. One file, run manually or in CI. Even this
  covers the scariest regressions. (No package.json exists yet; adding a minimal
  one just for `@playwright/test` is acceptable and does not change the site.)

---

## MEDIUM

### M1. `SoundFX.playTick` dereferences `audioContext` before its null-check (classic site)
- **Where**: `script.js:20-25`. Line 22 reads `this.audioContext.state` but the
  `if (!this.enabled || !this.audioContext) return;` guard is on line 25.
- **Why it matters**: `init()` now sets `audioContext = null` on browsers that
  block Web Audio (correct). But the first hover/click then calls `playTick`,
  which throws `TypeError: Cannot read properties of null` on line 22 before
  reaching the guard. It does not break the page (it throws inside an event
  listener) but spams the console and means no graceful path. Classic pages only.
- **Fix (small)**: move the null check to the top of `playTick`:
  `if (!this.audioContext || !this.enabled) return;` and delete the later guard.

### M2. Two divergent, duplicated front-end systems that disagree with themselves
- **Where**: `alt.js`/`alt.css` (live) vs `script.js`/`styles.css` (classic).
  Both reimplement SoundFX, Lenis, and scroll reveals. Theme handling disagrees:
  live is dark-default with a persisted `body.light` (`localStorage.theme`);
  classic is light-default with a non-persisted `dark-mode` class.
- **Why it matters**: a fix or feature added to one is easily forgotten in the
  other, and the inconsistent theme model is confusing. It is genuine duplicated
  logic, not intentional variation.
- **Fix (small, incremental)**: this is mostly documented away in CLAUDE.md /
  PROJECT.md rather than refactored (the classic site is archived/noindex). If
  desired, one small task: make the classic theme persist too, mirroring
  `alt.js`, so behavior at least matches. Do NOT attempt a big merge of the two
  systems in one pass.

### M3. Sitemap is stale and points at a redirect; omits all case-study pages
- **Where**: `sitemap.xml`. Lists only `/` and `/about.html`, with
  `lastmod 2026-03-15`. Under `cleanUrls`, `/about.html` 308-redirects to
  `/about`, and the 7 `/work/*` pages are missing entirely.
- **Why it matters**: search engines are pointed at a redirect and never told
  about the case-study pages, hurting their indexing. Purely SEO, no user impact.
- **Fix (small)**: rewrite `sitemap.xml` to use clean URLs (`/`, `/about`,
  `/work/hennessy-vsop`, `/work/under-armour`, `/work/living-distance`,
  `/work/tree-vr`, `/work/sing-street`, `/work/d5x`, `/work/new-museum`) and a
  current `lastmod`. The classic pages are `noindex`, keep them out.

### M4. Five featured videos load from a Cloudflare R2 *dev* URL
- **Where**: `index.html` (Accenture, Defender, In Her Head, NYT, ProLiteracy
  `data-src` values) point at `pub-64f6de2de05f4983ac3f6267d52b3b72.r2.dev/...`.
- **Why it matters**: `pub-*.r2.dev` is Cloudflare's development endpoint,
  explicitly rate-limited and not recommended for production traffic. Under load
  or throttling these previews may fail to load. Autoplay-refusal now shows a
  poster, but a network *load failure* of the `src` is a different path and can
  still leave a blank card.
- **Fix (medium)**: put a custom domain in front of the R2 bucket and swap the
  host in those `data-src` values, or move these clips into `images/projects/`
  and serve them locally like the others.

### M5. The ProLiteracy card has no poster at all
- **Where**: `index.html:184-194`. Its `<video>` has neither `poster` nor
  `data-poster`.
- **Why it matters**: when autoplay is blocked (iOS Low Power Mode, Android Data
  Saver) this card is an empty box, the same class of bug the `data-poster`
  fallback exists to prevent. It is the one card that pattern misses.
- **Fix (small, needs an asset)**: grab a representative frame from the
  ProLiteracy mp4, save it to `images/projects/`, and add
  `data-poster="images/projects/proliteracy-poster.jpg"` to the video. (Frame
  extraction needs ffmpeg, which is not available in this environment.)

---

## LOW

### L1. 36 MB Thorne video committed and served locally
- **Where**: `images/projects/thorne-frontier-within.mp4`, referenced at
  `index.html:160`.
- **Why it matters**: heavy on mobile data even though it is lazy-loaded; also
  bloats the repo (see H1).
- **Fix**: compress to ~720p / a few MB and/or move to R2 (behind a real domain,
  see M4), matching the other clips.

### L2. No security headers in `vercel.json`
- **Where**: `vercel.json` (only `cleanUrls` + redirects).
- **Why it matters**: no `Content-Security-Policy`, `X-Frame-Options`, or
  `Referrer-Policy`. Low risk here (no forms, no auth, no injection sink, and DOM
  writes use `textContent` or hardcoded SVG), so this is defense-in-depth only.
- **Fix (small)**: add a `headers` block setting `X-Frame-Options: DENY`,
  `Referrer-Policy: strict-origin-when-cross-origin`, and a conservative CSP.
  Test that Google Fonts, R2, and Vimeo are allowlisted before shipping.

### L3. The `<noscript>` + failsafe block is copy-pasted into every live page
- **Where**: identical block in `index.html`, `about.html`, and all 7
  `work/*.html`.
- **Why it matters**: if the reveal mechanism or the `loaded` class changes, all
  ~9 copies must change together or some pages break. With no build step there is
  no clean way to share it, so this is a known cost, not a mistake.
- **Fix**: acceptable as-is; just remember to update all copies together. If a
  build step is ever added, factor it into a shared include.

### L4. `main` auto-deploys and is edited by multiple sessions
- **Where**: operational, not a file. Vercel deploys `main` on push; more than
  one agent/session has pushed concurrently.
- **Why it matters**: an in-progress or someone else's commit can go straight to
  production, and your push can be rejected or unexpectedly fast-forwarded.
- **Fix**: always `git fetch` before pushing; for nontrivial work use an isolated
  `git worktree` off `origin/main` and fast-forward. Documented in CLAUDE.md.

### L5. Duplicated per-card poster/`data-poster` conventions are inconsistent
- **Where**: `index.html` cards mix three patterns: `poster=` (atlassian,
  procession, google-paper-planes tile), `data-poster=` (most featured cards),
  and neither (ProLiteracy, M5). `data-poster` shows only on autoplay refusal;
  `poster` shows always (a brief flash before playback).
- **Why it matters**: inconsistent visual behavior between cards and easy to get
  wrong when adding a new one. Not a bug per se, but a footgun.
- **Fix**: pick one convention (prefer `data-poster`, the no-flash pattern) and
  document/apply it uniformly. See CLAUDE.md "Adding a project card".
