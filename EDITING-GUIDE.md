# Editing your website — a plain-English guide

You'll mostly do two things: **swap a photo** or **change some text**. Both are easy and
neither requires you to understand code. When you're done, you "publish" with three commands.

Always **preview locally first** (see the bottom of this guide), then publish.

---

## Part 1 — Swapping a photo

Every photo on the site lives in `assets/img/` and has a fixed, descriptive name called a
**slot**. To change a picture, you put your new picture into the right slot — the website
automatically shows whatever is in that slot.

### The easy way (recommended)

A helper script resizes your photo correctly, rotates sideways phone photos, and strips
hidden location data. From the project folder, run:

```bash
python3 tools/optimize-photo.py <path-to-your-photo> <slot-name>
```

For example, to replace the big banner image on the About/home page:

```bash
python3 tools/optimize-photo.py ~/Desktop/atlas-mountains.jpg about/banner
```

That's it — it overwrites `assets/img/about/banner.jpg` for you. (Run
`python3 tools/optimize-photo.py` with nothing after it to see the slot list. If it complains
about "Pillow", run `pip3 install pillow` once.)

### The manual way

You can also just drag your own image into the right page folder under `assets/img/` and
rename it to match the slot (e.g. put it at `assets/img/about/banner.jpg`, replacing the old
one). If you do it this way, try to keep roughly the same shape (wide vs. tall) and keep the
file under ~1–2 MB so the page stays fast.

### The photo slots

Photos are grouped by page in `assets/img/<page>/`. The **slot name** you pass to the script
is that path without the `.jpg` (e.g. `about/banner`).

| Slot (file under `assets/img/`) | Where it appears | Best shape |
|------------------------------|------------------|------------|
| `about/banner.jpg` | Large banner behind your name (About / home page) | wide landscape |
| `about/headshot.jpg` | Round portrait at the top of the home page | square-ish |
| `about/theme-paleohydrology.jpg` | 1st research-theme card — Paleo-hydrology and monsoons | landscape |
| `about/theme-paleofire.jpg` | 2nd research-theme card — Paleofire history | landscape |
| `about/theme-vegetation.jpg` | 3rd research-theme card — Ecosystem & vegetation change | landscape |
| `research/banner.jpg` | Wide banner strip on the Research page | wide landscape |
| `research/fieldwork-morocco.jpg` | Taforalt / Morocco card (Research) | landscape |
| `research/fieldwork-southafrica.jpg` | Kruger / South Africa card (Research) | landscape |
| `research/gallery-1.jpg` … `gallery-6.jpg` | The six photos in the Research "Field gallery" | landscape |

### Swapping the CV PDF

Replace `assets/files/Nicholas_OMara_CV.pdf` with your updated CV, **keeping the same file
name**. Every "Download CV" button will then serve the new version.

---

## Part 2 — Changing text

Each page is one file you can open in any text editor (TextEdit, VS Code, etc.):

| File | The page it controls |
|------|----------------------|
| `index.html` | Home — your tagline, bio, photo captions, contact details |
| `research.html` | Research — themes, fieldwork, gallery captions, funding |
| `publications.html` | Publications & presentations |
| `cv.html` | CV summary (education, experience, honors) |
| `teaching.html` | Teaching, mentoring & outreach |

### How to edit

1. Open the file in a text editor.
2. Find the words you want to change (your editor's **Find**, ⌘F, helps).
3. Change **only the words** — the visible text sits between a `>` and a `<`. For example:

   ```html
   <h2>Reading Earth's past to understand fire's future</h2>
   ```

   You can safely change `Reading Earth's past to understand fire's future` to anything.
   Leave the `<h2>` and `</h2>` parts alone — those are just labels that tell the browser
   "this is a heading."

4. Save the file.

### A few handy spots

- **Tagline under your name:** in `index.html`, the line starting `<p class="eyebrow">Paleoclimatologist…`
- **Bio paragraphs:** in `index.html`, the "About" section.
- **Photo captions:** the text inside `<figcaption>…</figcaption>` and the band headings.
- **Contact details:** near the bottom of `index.html`, the "Contact" section.
- **Add a publication:** in `publications.html`, copy one `<li class="pub"> … </li>` block,
  paste it, and edit the year, title, authors, and DOI link.

> Tip: change one thing, save, refresh your local preview to check it, then move on. Small
> steps are easy to undo if something looks off.

---

## Part 3 — Preview, then publish

### Preview locally (nobody else sees this)

From the project folder in Terminal:

```bash
python3 -m http.server 8000
```

Open **http://localhost:8000** in your browser. Refresh after each change. Press `Ctrl+C`
to stop.

### Publish your changes

When you're happy:

```bash
git add .
git commit -m "Describe what you changed"
git push
```

The live site updates within about a minute.

---

*If you ever want a new photo slot, a new page, or a bigger change, that's a code edit — but
everything above you can do yourself.*
