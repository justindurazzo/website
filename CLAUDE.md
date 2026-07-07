# CLAUDE.md, operating guide for justindurazzo.com

Read this first. For architecture context see **PROJECT.md**; for known issues
see **GAPS.md**.
- PROJECT.md = what the site is, how the two systems fit together, what is load-bearing.
- GAPS.md = ranked list of real weaknesses with small suggested fixes.

## What this is
A dependency-free **static portfolio site** (hand-written HTML/CSS/vanilla JS,
no framework, no build, no backend, no tests). Deployed on **Vercel**, which
**auto-deploys `main` to production** (justindurazzo.com) on push.

## Commands
There is no build/test/lint tooling. Practically:
- **Run locally**: serve the folder statically, e.g. `python3 -m http.server 8000`
  then open http://localhost:8000 (use a server, not `file://`, so clean paths and
  fetch behave). Vercel's `cleanUrls` maps `/about`->`about.html` in production;
  locally you may need the `.html`.
- **JS sanity check** (only real "lint" available): `node --check alt.js` and
  `node --check script.js` after editing JS.
- **Deploy**: `git push origin main` (Vercel builds and publishes automatically).
  There is no manual deploy step; do not add one.
- **Verify a change**: open the affected page in a browser and watch it. That is
  the only real test. There is no runner.

## The two systems (do not edit the wrong one)
- **LIVE / indexed site** = `index.html`, `about.html`, `work/*.html`, styled by
  **`alt.css`**, behavior in **`alt.js`**, plus `work.css` on case-study pages.
  This is what you almost always edit.
- **CLASSIC / archived** = `classic.html`, `classic-about.html`, styled by
  **`styles.css`**, behavior in **`script.js`**. `noindex`, footer-linked only.
  Treat as frozen unless explicitly told otherwise.
- `styles.css` and `script.js` are NOT the live site. `alt.css` and `alt.js` are.

## Conventions this codebase actually follows
- **Files/organization**: one HTML file per page; case studies live in `work/`.
  Per-project media in `images/projects/` (homepage) and `images/work/<slug>/`
  (case studies). Absolute asset paths (`/alt.css`, `/images/...`) inside
  `work/*.html`; relative paths on top-level pages.
- **CSS**: BEM-ish flat class names (`.card`, `.card-media`, `.card-meta`,
  `.cs-hero`, `.cs-media--full`). Theming via CSS custom properties on `:root`
  and overridden under `body.light`. Sections marked with `/* ---------- Name ---------- */`.
- **JS**: vanilla, no modules, no bundler. IIFE/top-level script executed at end
  of `<body>`. Feature-detect and guard every `getElementById`/`querySelector`
  before use (`if (el) {...}`), because the same script runs on pages that lack
  some elements. Wrap anything that can throw (AudioContext, `currentTime`) in
  try/catch. Reveal via a `.in` class added by IntersectionObserver.
- **State**: `localStorage.theme` (`light`/`dark`) and `localStorage.soundEnabled`
  (live site); `sessionStorage.introSeen` gates the one-time intro. Classic site
  does not persist theme.
- **DOM writes**: use `textContent` for any text; only assign `innerHTML` from
  hardcoded constant SVG strings. Never inject user/URL input as HTML.
- **Links**: internal links use clean URLs (`/about`, `/work/x`). External links
  get `target="_blank" rel="noopener"` and must be `https://`.

## Gotchas (things that do not work the way they look)
- **Content is hidden until JS reveals it.** `[data-reveal]`, `.card`, `.tile`,
  `[data-line]`, and `.nav` start at `opacity:0` and are shown when JS adds `.in`
  / `body.loaded`. If reveal does not run, the page is blank. Every live page has
  a `<noscript>` block and an inline `data-failsafe-reveal` `<script>` that key
  off `body.classList.contains('loaded')` as the backstop. If you rename the
  `loaded`/`in` classes or change the reveal mechanism, update the failsafe in
  **every** live HTML file (index, about, all 7 work pages).
- **The intro overlay shows only once per session** and is skipped on internal
  navigation. Use a fresh tab / clear sessionStorage to see it while testing.
- **`data-static` on a card disables its video preview** and currently leaves a
  blank box (GAPS.md H2). `data-start`/`data-end`/`data-loop-start` make a preview
  loop one section of a longer film; `data-src` is the lazy source; `data-poster`
  is shown only if autoplay is refused.
- **Tiles whose `href` starts with `/work/` navigate**; all other cards/tiles
  open the lightbox (their `href="#"` is intercepted).
- **`.gitattributes` claims mp4 = Git LFS, but LFS is NOT in use.** Do not rely
  on it. Committing a new mp4 from a machine with git-lfs installed can produce a
  broken pointer in production. See GAPS.md H1 (recommended: remove that line).
- **An external hook strips the em dash character** on save/commit (owner's hard
  rule). Never type an em dash in code, copy, or comments; it will be rewritten
  and may show files as "modified since read". Use a comma, colon, or hyphen.

## Rules (do not break these)
- **Never change the `loaded` / `in` reveal classes or the failsafe/`<noscript>`
  blocks without updating all live pages together** (blank-page risk).
- **Do not remove `cleanUrls` from `vercel.json`** or switch internal links back
  to `.html`; every internal link assumes clean URLs.
- **`main` is production and may be edited by another session at the same time.**
  `git fetch` before pushing. For anything nontrivial, work in an isolated
  `git worktree` off `origin/main` and fast-forward, rather than editing the
  shared checkout.
- **`lenis.min.js` is vendored/minified, do not hand-edit it.** The Google
  verification file (`google84b...html`) is intentional and public, leave it.
- **Keep `classic.html`/`classic-about.html` `noindex`.** They are archived.

## Adding a project card (the common task)
In `index.html`, copy an existing `<article class="card" data-reveal>` block.
Prefer a video preview with the **no-flash** pattern:
```html
<article class="card" data-reveal>
  <a class="card-media" href="#">
    <video muted loop playsinline preload="none"
           data-poster="images/projects/<slug>-poster.jpg"
           data-src="<local-or-r2-url>.mp4"></video>
  </a>
  <div class="card-meta">
    <span class="card-cat">Category</span>
    <h2 class="card-title">Title</h2>
    <p class="card-desc">One or two sentences.</p>
  </div>
</article>
```
Use `card--wide` for a full-width row. Always give a `data-poster` (GAPS.md M5/L5).
For an archive entry use a `.tile` in `.archive-grid`; if it has a full
case-study page, set `href="/work/<slug>"` (it will navigate instead of opening
the lightbox). New case-study pages: copy `work/hennessy-vsop.html`, keep the
`/alt.css` + `/work.css` + `/alt.js` + failsafe stack, and add the page to
`sitemap.xml`.
