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
│   ├── img/             # web-optimized images (headshots)
│   └── files/           # downloadable CV PDF
└── source/              # original-resolution source files (CV, headshots, links)
```

## How to update the site

Everything is plain text, so edits are simple.

**Update your CV (PDF):** replace `assets/files/Nicholas_OMara_CV.pdf` with your new file,
keeping the same filename. The "Download CV" buttons will serve the new version automatically.

**Edit text** (bio, a publication, a date): open the relevant `.html` file, change the words,
save.

**Add a publication:** in `publications.html`, copy an existing `<li class="pub">…</li>`
block, paste it where you want it, and edit the year, title, authors, venue, and DOI link.

Then publish your changes:

```bash
git add .
git commit -m "Update publications"   # describe your change
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
