# PROJECT.md, justindurazzo.com

The onboarding overview a senior engineer would give a new hire. For known
weaknesses see GAPS.md; for day-to-day commands and rules see CLAUDE.md.

## What this is and who it is for

A personal portfolio site for **Justin Durazzo** (AI & Immersive Design, Accenture
Song; formerly Droga5). It is a marketing/brand site whose job is to make a
strong first impression and show a curated body of creative work (VR, AR, AI,
interactive installations, films) to potential employers, collaborators, and
clients. Audience is human visitors on desktop and mobile, plus search-engine
and social crawlers. There is no app functionality: no accounts, no forms, no
user data. "Contact" is a `mailto:` link.

Live at https://justindurazzo.com (deployed on Vercel, auto-deploys from `main`).

## Tech stack and why

This is deliberately a **plain static site**: hand-written HTML, CSS, and vanilla
JS, no framework, no build step, no package manager, no dependencies to install.

- **HTML/CSS/vanilla JS**: the whole site is a handful of `.html` files sharing
  two `.css` files and two `.js` files. Chosen for zero build complexity and
  because the content is essentially static. You edit a file and it ships.
- **Lenis** (`lenis.min.js`, vendored, the only third-party JS): smooth-scroll
  library that gives the site its momentum/"cinematic" scroll feel. Vendored as
  a single minified file rather than an npm dependency to keep the no-build
  approach.
- **Google Fonts** (Fraunces display serif + Inter sans) loaded from the Google
  CDN. Fraunces is the signature look; Inter is the UI/body face.
- **Cloudflare R2** (`pub-64f6de2de05f4983ac3f6267d52b3b72.r2.dev`) hosts most of
  the featured project videos, keeping large media out of the page's critical
  path. NOTE: this is R2's *dev* URL (see GAPS.md, it is rate-limited and not
  meant for production).
- **Vimeo** embeds host the long-form case-study films on `/work/*` pages.
- **Vercel** for hosting: static file serving, `cleanUrls`, and simple redirects.
  Chosen because it deploys a static repo on git push with zero config.

## Repository map

```
index.html            Home / landing (the primary page). Hero + Selected Work + Archive + Lab + Contact.
about.html            About page.
work/*.html           7 case-study deep-dive pages (hennessy-vsop, under-armour,
                      living-distance, tree-vr, sing-street, d5x, new-museum).
classic.html          ARCHIVED older design of the home page (noindex).
classic-about.html    ARCHIVED older about page (noindex).

alt.css               Stylesheet for the LIVE site (index, about, work/*).
alt.js                Behavior for the LIVE site.
work.css              Extra styles for the /work/* case-study template (loaded alongside alt.css).
lenis.min.js          Vendored smooth-scroll library (used by the live site and classic.html).

styles.css            Stylesheet for the CLASSIC (archived) pages only.
script.js             Behavior for the CLASSIC (archived) pages only.

vercel.json           Hosting config: cleanUrls + 2 redirects.
robots.txt            Allows all; points at sitemap.
sitemap.xml           Sitemap (STALE, see GAPS.md).
google84b...html      Google Search Console verification file (public by design).
favicon.ico
.gitattributes        Declares *.mp4 as Git LFS (but LFS is NOT actually in use, see GAPS.md).
.gitignore            Ignores .DS_Store and .claude/.
images/               All media. images/projects/* = homepage art + local mp4s.
                      images/work/<project>/* = per-case-study assets. ~55 MB total.
```

There is **no package.json, no build tooling, no test suite, no CI config** in
the repo. What you see is what ships.

## The two design systems (the single most important thing to understand)

The repo contains **two independent front-end systems** that do not share code:

1. **The LIVE system** (`alt.css` + `alt.js` + `lenis.min.js`), used by
   `index.html`, `about.html`, and every `work/*.html`. This is the real,
   indexed site. Dark theme by default; light theme via a `body.light` class
   that is **persisted** in `localStorage` under key `theme`.

2. **The CLASSIC system** (`styles.css` + `script.js`), used only by
   `classic.html` and `classic-about.html`, which are `noindex` and linked only
   as a "Classic site" easter egg in the footer. Light theme by default; dark
   via a `dark-mode` class that is **not** persisted.

`alt.js` and `script.js` are largely parallel reimplementations of the same
ideas (sound effects, Lenis init, scroll reveals) targeting different DOM
(`.card`/`.tile` in the live system vs `.project` in classic). They disagree on
theme class names, defaults, and persistence. **When you change shared behavior,
decide which system you are in and do not assume a fix in one applies to the
other.** In practice you will almost always work in the LIVE system; treat the
classic files as frozen/archived unless explicitly asked.

## Architecture and data flow

There is no server-side logic and no runtime data. "Data flow" is: static files
-> Vercel CDN -> browser -> JS enhances the DOM and lazy-loads media.

```
  Browser requests justindurazzo.com
        |
        v
  Vercel static hosting  (cleanUrls: /about -> about.html, /work/x -> work/x.html)
        |
        v
  index.html  --loads-->  alt.css, Google Fonts (CDN), lenis.min.js, alt.js
        |
        |  alt.js runs (end of <body>):
        |    1. restore saved theme from localStorage
        |    2. on DOMContentLoaded: lift the #wipe load overlay, add body.loaded
        |    3. IntersectionObservers reveal sections and lazy-play card videos
        |    4. wire lightbox, side-nav dots, toggles, back-to-top
        v
  Media loads on demand:
     - hero + a few cards:  local mp4  (images/projects/*.mp4, in this repo)
     - most featured cards: Cloudflare R2 (pub-...r2.dev/*.mp4), set from data-src when in view
     - case-study films:    Vimeo <iframe> on /work/* pages
```

Navigation between pages is plain full-page loads (`<a href>`); there is no
client-side router. `alt.js` re-runs fresh on every page.

## How `alt.js` works (the load-bearing file for the live site)

Read top to bottom, it sets up, in order:

- **Theme restore** (top level): reads `localStorage.theme`; if `light`, adds
  `body.light` before paint so returning visitors do not flash the wrong theme.
- **SoundFX**: a Web Audio "tick" on hover/click. Persisted on/off in
  `localStorage.soundEnabled`. AudioContext creation is wrapped in try/catch so a
  browser that blocks Web Audio cannot break the page.
- **Lenis smooth scroll**: created unless `prefers-reduced-motion`. Exposed as
  the module-level `lenis`. Anchor links (`a[href^="#"]`) route through it.
- **Load wipe -> reveal** (on `DOMContentLoaded`): the full-screen `#wipe`
  overlay is lifted and `body.loaded` is added. The "Justin Durazzo" intro plays
  once per session (guarded by `sessionStorage.introSeen`) and is skipped on
  internal navigation and for reduced-motion users.
- **Scroll reveals**: an IntersectionObserver adds `.in` to `[data-reveal]`,
  `.card`, and `.tile` as they enter view. CSS animates from hidden to shown.
- **Lazy autoplay previews**: card/tile videos with `data-src` are loaded and
  played only when in view. Optional `data-start` / `data-end` / `data-loop-start`
  attributes make a preview loop just one section of a longer film. A card marked
  `data-static` opts OUT of preview playback. On autoplay refusal (e.g. iOS Low
  Power Mode) the code promotes `data-poster` to a real `poster` so the card is
  not an empty box.
- **Lightbox**: clicking a `.card`/`.tile` opens a modal with the full video
  (native controls, plays from 0) or the image. Tiles whose `href` starts with
  `/work/` navigate to the case-study page instead of opening the lightbox.
  Opening calls `lenis.stop()` and locks body scroll; closing reverses it and
  restores focus. Escape and backdrop click close it.
- **Side-nav dots**: a vertical indicator tracking the featured `.card`s, shown
  only while the Selected Work section is on screen.

At the very end of each live page, an inline **failsafe** `<script>` and a
`<noscript>` block guarantee the page is never left blank if `alt.js` fails to
load, is blocked, or JS is disabled (see "Critical paths" below).

## Key design decisions (inferred)

- **No build step on purpose.** The site is small and static; a framework would
  add complexity with no payoff. Cost: shared markup (nav, `<noscript>`,
  failsafe) is copy-pasted across pages instead of componentized.
- **Content is hidden until JS reveals it**, for the cinematic entrance. This is
  risky (a JS failure would blank the page), which is exactly why the
  `<noscript>` + inline failsafe safety net exists, and why reduced-motion CSS
  forces everything visible.
- **Videos are lazy and section-looped.** Previews only load in view and can
  loop a hero moment of a longer film (`data-start`/`data-end`), balancing "show
  motion" against bandwidth. Big/less-important media lives on R2 or Vimeo.
- **Graceful degradation is taken seriously**: reduced-motion path, autoplay-
  refused poster fallback, JS-failure failsafe, `rel="noopener"` on external
  links, `https` everywhere.
- **The classic site is kept but hidden** (`noindex`, footer-only link) rather
  than deleted, as an archive of the previous design.

## Critical paths (what is load-bearing vs safe to touch)

Load-bearing, change with care and test in a browser:

- **`alt.js` reveal + wipe logic** (`reveal()`, the `DOMContentLoaded` handler,
  `body.loaded`). If reveal never runs, the page is blank. The inline failsafe in
  each HTML file is the backstop and keys off `body.classList.contains('loaded')`;
  if you rename that class or the reveal mechanism, update the failsafe in EVERY
  live HTML file too.
- **The `<noscript>` + failsafe blocks** duplicated in `index.html`,
  `about.html`, and all `work/*.html`. They are the safety net for the "hidden
  until JS" design.
- **The lazy video observer** (`videoObserver`, `data-start`/`data-end` logic).
  The homepage's featured work depends on it.
- **`vercel.json` `cleanUrls`**: internal links use extensionless paths
  (`/about`, `/work/x`). Turning it off breaks every internal link.

Safer to change casually:

- Copy inside project cards/tiles and case-study pages (titles, descriptions,
  credits). Pure content.
- Adding a new Archive tile or Lab link (follow the existing pattern).
- `classic.html` / `classic-about.html` (archived, noindex, low traffic).
- CSS tuning within a section, as long as you keep the reveal-related properties
  (`opacity`, `transform`, `clip-path` on `[data-reveal]`/`.card`/`.tile`) intact.

## Surprises and non-obvious things that will trip you up

1. **Two systems, easy to edit the wrong one.** `styles.css`/`script.js` are the
   *classic* files, NOT the live site. The live site is `alt.css`/`alt.js`. See
   the section above.
2. **`.gitattributes` says mp4 is Git LFS, but LFS is not actually in use.** The
   mp4s are committed as normal git blobs. This is a trap for new mp4s. See
   GAPS.md #1.
3. **An external hook/linter strips em dashes** from files on save/commit (the
   owner's hard preference). Do not add the em dash character anywhere; it will
   be rewritten to a comma/colon/hyphen and may show as "file changed since read".
4. **`main` auto-deploys to production and is sometimes edited by more than one
   session at once.** Fetch before you push; a fast-forward you did not expect may
   have landed. Prefer working in an isolated worktree for anything nontrivial.
5. **The intro overlay only appears once per browser session** (sessionStorage)
   and is skipped on internal navigation, so you will often NOT see it while
   testing. Clear session storage / use a fresh tab to see it.
6. **`data-static` on a card disables its video preview.** The in-her-head card
   uses it and currently renders blank as a result (GAPS.md #2).
7. **No tests, no lint, no build.** "Verify" means opening the page in a browser.
