# CLAUDE.md — nickomara.com

Project conventions for Dr. Nicholas O'Mara's personal academic website. Auto-loaded each
session. For the full story (people, decisions, history) read `PROJECT_HANDOFF.md`; for the
user-facing edit/deploy walkthroughs read `EDITING-GUIDE.md` and `DEPLOY.md`.

## What this is
A **static** academic site (About, Research, Publications, CV, Teaching) hosted **free on
GitHub Pages** at the custom domain **nickomara.com**. Plain HTML/CSS/JS — **no build step,
no framework, no package manager**. Keep it that way unless the user explicitly asks
otherwise. The user is comfortable with git/Terminal but is **not a web developer** —
prefer simple edits and explain any deploy/DNS steps plainly.

## Location note
The git repo and all site files live in the **`nomara_prof_website/`** subfolder (this
folder), not its parent. This is inside a Google Drive folder — harmless, but expect
occasional `.DS_Store`/Office lock-file noise. Remote: `github.com/nickomara/nomara_prof_website`.

## Structure
```
index.html  research.html  publications.html  cv.html  teaching.html   # the 5 pages
style.css        # shared styles + palette (CSS variables in :root)
main.js          # mobile nav toggle + footer year
CNAME            # nickomara.com — DO NOT delete (needed for custom domain)
assets/img/      # web images, grouped per page in about/ and research/ ("slots" — see photo rule)
assets/files/    # Nicholas_OMara_CV.pdf (the downloadable CV — keep this filename)
tools/optimize-photo.py   # resizes/orients/strips-EXIF a new photo into a slot
source/          # original-resolution originals (photos, CV, links docx) — not served
```
Nav and footer markup are **duplicated in each of the 5 HTML files** (no templating/includes).

## Conventions
- **Keep nav + footer identical across all 5 pages.** When editing either, change every page.
  Nav = brand `Nicholas <span>O'Mara</span>, Ph.D.` + 5 links (About/Research/Publications/CV/
  Teaching); mark the current page's link `class="active"`. Footer = year span + social icons.
- **Palette & fonts are locked** — don't change without being asked. Defined once as CSS
  variables in `style.css :root`:
  - `--accent` `#1d4533` (deep forest green — primary: links, buttons, eyebrows)
  - `--navy` `#16314c` (deep navy — secondary accent) · `--accent-dk`/`--navy-dk` for hovers
  - `--ink` `#141b18` text · `--ink-soft` `#51605a` · `--line` `#e2e8e4` · `--bg`/`--surface` `#fff`
  - `--surface-2` `#f1f5f2` (alt panels) · `--footer-bg` `#10171a`
  - `--serif` **Newsreader** (headings) · `--sans` **Inter** (body) — loaded via one Google
    Fonts `<link>` in each page's `<head>`. Use the variables, not raw hex.
- **Photo "slot" system:** every image is a fixed path under `assets/img/`, grouped by page
  (`assets/img/about/`, `assets/img/research/`); the HTML references these slots, not specific
  photos. To change a picture, replace the file of the same name. **Always route new photos
  through `python3 tools/optimize-photo.py <path> <slot>`**, where `<slot>` is the folder/name
  without `.jpg` (e.g. `about/banner`, `research/gallery-1`) — needs Pillow (`pip3 install pillow`) —
  so images stay web-optimized, EXIF-stripped, and correctly sized/oriented. The slots and their
  target widths are the `SLOTS` dict in that script; the where-it-appears table is in
  `EDITING-GUIDE.md`. Don't hand-add oversized images.
- **Adding a new photo slot / new page / structural change** = a real code edit (not a
  user self-serve edit): update the HTML, `style.css`, and the `SLOTS` dict together.

## Content facts (don't "correct" these)
- Name renders **Nicholas O'Mara, Ph.D.** Hero eyebrow: *"Paleoclimatologist, Paleoecologist,
  Organic/stable isotope geochemist."* Pronouns: he/him.
- Current role: **Postdoctoral Research Associate, Ecology & Evolutionary Biology, Princeton.**
- Office address uses **"Briger Hall"** — this spelling is correct and user-confirmed (do NOT
  change to "Bridger").
- The site's contact email is **nicholas.omara@princeton.edu** (institution address). The
  Yale address is only the user's login identity — never put it on the site.

## Preview & deploy
- **Preview locally:** `python3 -m http.server 8000` from this folder → http://localhost:8000
  (refresh after edits; `Ctrl+C` to stop). There is no private staging URL — iterate locally.
- **Publish:** `git add . && git commit -m "..." && git push`; Pages updates in ~1 min.
- **Do not deploy or push unless the user explicitly says so.** First-time deploy (enable
  Pages, point WordPress.com DNS at GitHub) is documented in `DEPLOY.md`.

## Current git state (verify with `git status` — this can drift)
As of the 2026-09-17 handoff, the last pushed commit contains an **early** version of the
site and **only the `headshot` image**. The complete current site — the other 15 web images,
`tools/`, `EDITING-GUIDE.md`, `PROJECT_HANDOFF.md`, and substantial edits to `index.html` /
`style.css` / `research.html` — is **local and uncommitted**. So a deploy today needs a full
`git add .` first, or the live site would be missing most images. (The `PROJECT_HANDOFF.md`
claim that "only the README is on GitHub" is out of date.)
