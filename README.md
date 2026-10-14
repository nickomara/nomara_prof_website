# nickomara.com — personal academic website

A fast, static website for Dr. Nicholas O'Mara, hosted free on **GitHub Pages** with the
custom domain **nickomara.com**. No build step, no frameworks — just HTML, CSS, and a few
lines of JavaScript, so anyone can edit it.

## Pages

| File | Page |
|------|------|
| `index.html` | Home / About + contact |
| `research.html` | Research themes, fieldwork, funding |
| `publications.html` | Publications & presentations |
| `cv.html` | CV summary + PDF download |
| `teaching.html` | Teaching, mentoring & outreach |

## Project structure

```
.
├── index.html / research.html / publications.html / cv.html / teaching.html
├── style.css            # shared styling (colors, layout, type)
├── main.js              # mobile menu toggle + footer year
├── CNAME                # custom domain (nickomara.com) — do not delete
├── assets/
│   ├── img/             # web images, named by "slot" (hero.jpg, portrait.jpg, gallery-1.jpg…)
│   └── files/           # downloadable CV PDF
├── tools/
│   └── optimize-photo.py  # resizes a new photo into a slot
├── EDITING-GUIDE.md     # how to swap photos & edit text (start here)
├── DEPLOY.md            # first-time deployment steps
└── source/              # original-resolution source files (CV, headshots, links)
```

## How to update the site

**See [`EDITING-GUIDE.md`](EDITING-GUIDE.md) for a full, plain-English walkthrough** of
swapping photos and editing text. In short:

**Swap a photo:** every image is a named "slot" in `assets/img/` (e.g. `hero.jpg`,
`portrait.jpg`, `theme-fire.jpg`, `gallery-1.jpg`). Drop in a replacement with the helper
script, which sizes it correctly:

```bash
python3 tools/optimize-photo.py ~/Desktop/new-photo.jpg hero
```

**Update your CV (PDF):** replace `assets/files/Nicholas_OMara_CV.pdf`, keeping the filename.

**Edit text:** open the relevant `.html` file, change the words (the visible text between
`>` and `<`), save.

Then publish:

```bash
git add .
git commit -m "Describe your change"
git push
```

The live site refreshes within ~1 minute.

## Deploying (first-time setup)

1. Push this repo to GitHub.
2. On GitHub: **Settings → Pages → Build and deployment → Source: "Deploy from a branch"**,
   branch `main`, folder `/ (root)`. Save.
3. Under the same **Pages** settings, set the **Custom domain** to `nickomara.com`
   (the `CNAME` file already declares it) and enable **Enforce HTTPS**.
4. Point the domain's DNS at GitHub Pages (see DEPLOY.md).

---
© Nicholas O'Mara. Built as a static site for GitHub Pages.
