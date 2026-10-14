#!/usr/bin/env python3
"""
build-cv-pages.py — regenerate the CV, Publications, and Teaching pages from the Word CV.

Reads the section tables in assets/files/Nicholas_OMara_CV.docx and rewrites the
matching parts of:
  • cv.html          — Education / Experience / Honors timelines
  • publications.html — Peer-reviewed / In prep / Invited talks / Conference
                        presentations (each citation reproduced directly from the
                        CV: name bold, journal italic, DOI linked)
  • teaching.html     — the two Teaching-Assistant lists only (the mentoring /
                        outreach narrative is hand-written and left untouched)

Idempotent — safe to run repeatedly.  Needs python-docx:  pip3 install python-docx
    python3 tools/build-cv-pages.py
"""
import os, re
from docx import Document
from docx.text.run import Run
from docx.oxml.ns import qn
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.text.paragraph import Paragraph
from docx.table import Table

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCX = os.path.join(HERE, "assets", "files", "Nicholas_OMara_CV.docx")
R, HL = qn('w:r'), qn('w:hyperlink')
SUBHEAD = ("color:var(--ink-soft);font-family:var(--sans);font-weight:600;font-size:.95rem;"
           "text-transform:uppercase;letter-spacing:.06em;margin-top:1.6em;")

def norm(s): return re.sub(r"\s+", " ", s).strip().lower().rstrip(":").strip()
def esc(s):  return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# ---------- read CV tables ----------
def find_table(doc, pred):
    want = False
    for ch in doc.element.body.iterchildren():
        if isinstance(ch, CT_P):
            p = Paragraph(ch, doc)
            if p.text.strip() and any(r.bold for r in p.runs) and pred(norm(p.text)):
                want = True
        elif isinstance(ch, CT_Tbl):
            if want:
                return Table(ch, doc)
    raise SystemExit("ERROR: a CV section/table was not found")

def groups(doc, pred):
    """[(sublabel|None, [(when, cell), ...]), ...] for one section's table."""
    t = find_table(doc, pred)
    out, label, cur = [], None, []
    for row in t.rows:
        c = row.cells
        if c[0]._tc is c[1]._tc:                       # merged sub-label row
            if cur: out.append((label, cur)); cur = []
            label = c[0].text.strip().rstrip(":"); continue
        if not c[0].text.strip() and not c[1].text.strip():
            continue                                   # spacer row
        cur.append((c[0].text.strip(), c[1]))
    if cur: out.append((label, cur))
    return out

def rows(doc, pred):  return [r for _, rs in groups(doc, pred) for r in rs]

# ---------- inline run -> HTML ----------
def inline(p, keep_bold=True, want_links=False):
    out, href = [], None
    for ch in p._p.iterchildren():
        if ch.tag == R:
            run = Run(ch, p); t = esc(run.text)
            if not t: continue
            if run.italic:               t = f"<em>{t}</em>"
            elif keep_bold and run.bold: t = f"<b>{t}</b>"
            out.append(t)
        elif ch.tag == HL:               # hyperlink: grab href, drop the raw URL text
            if want_links:
                try: href = p.part.rels[ch.get(qn('r:id'))].target_ref
                except Exception: pass
    return "".join(out), href

def cite_html(cell):
    parts, doi = [], None
    for p in cell.paragraphs:
        h, d = inline(p, keep_bold=True, want_links=True)
        if d: doi = d
        if h: parts.append(h)
    body = " ".join(parts)
    body = re.sub(r"\(\s*\)", "", body)                # empty () left where the DOI url was
    body = re.sub(r"\s+", " ", body).strip().rstrip(" .;,")
    return body, doi

# ---------- item builders ----------
def tl_items(doc, pred):
    lis = []
    for when, cell in rows(doc, pred):
        ps = list(cell.paragraphs)
        title = inline(ps[0], keep_bold=False)[0] if ps else ""
        detail = "<br>".join(inline(p)[0] for p in ps[1:] if p.text.strip())
        span = f"<span>{detail}</span>" if detail else ""
        lis.append('        <li class="tl__item">\n'
                   f'          <div class="tl__when">{esc(when)}</div>\n'
                   f'          <div class="tl__what"><strong>{title}</strong>{span}</div>\n'
                   '        </li>')
    return "\n".join(lis)

def pub_items(entries):
    lis = []
    for when, cell in entries:
        body, doi = cite_html(cell)
        year = esc(when) if when else "—"
        links = (f'\n            <div class="pub__links"><a href="{esc(doi)}" '
                 f'target="_blank" rel="noopener">View article (DOI) →</a></div>') if doi else ""
        lis.append('        <li class="pub">\n'
                   f'          <div class="pub__year">{year}</div>\n'
                   '          <div>\n'
                   f'            <div class="pub__cite">{body}</div>{links}\n'
                   '          </div>\n'
                   '        </li>')
    return "\n".join(lis)

def tl_from(entries):
    """Timeline items for teaching/service: split 'Course, Profs: …' one-liners,
    otherwise first paragraph = title and the rest = grey detail. An entry whose
    title begins with a dash is a continuation, folded into the previous item."""
    items = []
    for when, cell in entries:
        ps = [p for p in cell.paragraphs if p.text.strip()]
        if not ps: continue
        m = re.split(r",\s*Profs?:\s*", cell.text.strip(), maxsplit=1)
        if len(ps) == 1 and len(m) > 1:
            title, detail = esc(m[0].strip()), f"Profs. {esc(m[1].strip())}"
        else:
            title = inline(ps[0], keep_bold=False)[0]
            detail = "<br>".join(inline(p)[0] for p in ps[1:] if p.text.strip())
        plain = re.sub(r"<[^>]+>", "", title).lstrip()
        if items and plain[:1] in "–—-":
            cont = ((esc(when) + " ") if when else "") + title.lstrip("–—- ").strip()
            items[-1][2] = (items[-1][2] + "<br>" + cont) if items[-1][2] else cont
            continue
        items.append([esc(when), title, detail])
    out = []
    for when, title, detail in items:
        span = f"<span>{detail}</span>" if detail else ""
        out.append(f'        <li class="tl__item"><div class="tl__when">{when}</div>'
                   f'<div class="tl__what"><strong>{title}</strong>{span}</div></li>')
    return "\n".join(out)

def grant_items(entries, limit=3):
    """Funding items: reproduce each grant from the CV (funder bold, project italic,
    amount bold via inline()); a year-less row is the grant's detail, folded above.
    Keeps only the most recent `limit` grants by year."""
    items = []
    for when, cell in entries:
        html = " ".join(inline(p)[0] for p in cell.paragraphs if p.text.strip())
        if not html: continue
        if items and not (when or "").strip():
            items[-1][1] += " " + html
            continue
        items.append([esc(when), html])
    def _y(it):
        m = re.search(r"\d{4}", it[0])
        return int(m.group()) if m else 0
    items = sorted(items, key=_y, reverse=True)[:limit]
    return "\n".join(
        f'        <li class="tl__item"><div class="tl__when">{w}</div>'
        f'<div class="tl__what">{h}</div></li>' for w, h in items)

# ---------- HTML section replacement ----------
def sub_h2(html, h2, replacement, label):
    pat = re.compile(r'(?P<h><h2[^>]*>' + re.escape(h2) + r'</h2>\s*)<ul class="[^"]*">.*?</ul>', re.DOTALL)
    html, n = pat.subn(lambda m: m.group("h") + replacement, html, count=1)
    if n != 1: raise SystemExit(f"ERROR: section not found: {label}")
    return html

def sub_h3(html, contains, items, label):
    pat = re.compile(r'(?P<h><h3[^>]*>[^<]*' + re.escape(contains) + r'[^<]*</h3>\s*)<ul class="tl">.*?</ul>', re.DOTALL)
    html, n = pat.subn(lambda m: m.group("h") + f'<ul class="tl">\n{items}\n      </ul>', html, count=1)
    if n != 1: raise SystemExit(f"ERROR: sub-section not found: {label}")
    return html

def sub_conf(html, inner, label):
    # Replace everything between the conference <h2> and the following <p> ("Full list
    # in CV" button). Region-based so it is idempotent even with h3 sub-headers present.
    pat = re.compile(r'(<h2>Selected conference presentations</h2>)\s*.*?<p\b', re.DOTALL)
    html, n = pat.subn(lambda m: m.group(1) + "\n      " + inner + "\n\n      <p", html, count=1)
    if n != 1: raise SystemExit(f"ERROR: section not found: {label}")
    return html

def write(path, html): open(path, "w", encoding="utf-8").write(html)
def read(path):        return open(path, encoding="utf-8").read()

is_edu   = lambda n: n == "education"
is_exp   = lambda n: "experience" in n and ("professional" in n or "research" in n)
is_hon   = lambda n: "honor" in n
is_pub   = lambda n: n == "publications"
is_inv   = lambda n: "invited" in n
is_conf  = lambda n: "conference" in n
is_grant = lambda n: "grant" in n
is_teach = lambda n: "teaching experience" in n
is_syn   = lambda n: "synergistic" in n

def main():
    doc = Document(DOCX)

    # ---- cv.html ----
    cv = read(os.path.join(HERE, "cv.html"))
    cv = sub_h2(cv, "Education", f'<ul class="tl">\n{tl_items(doc, is_edu)}\n      </ul>', "cv/education")
    cv = sub_h2(cv, "Professional &amp; research experience",
                f'<ul class="tl">\n{tl_items(doc, is_exp)}\n      </ul>', "cv/experience")
    cv = sub_h2(cv, "Academic honors &amp; awards",
                f'<ul class="tl">\n{tl_items(doc, is_hon)}\n      </ul>', "cv/honors")
    write(os.path.join(HERE, "cv.html"), cv)

    # ---- publications.html ----
    pb = read(os.path.join(HERE, "publications.html"))
    pg = groups(doc, is_pub)
    peer   = pg[0][1] if len(pg) > 0 else []
    inprep = pg[1][1] if len(pg) > 1 else []
    pb = sub_h2(pb, "Peer-reviewed articles",
                f'<ul class="pub-list">\n{pub_items(peer)}\n      </ul>', "pub/peer")
    pb = sub_h2(pb, "In review &amp; in preparation",
                f'<ul class="pub-list">\n{pub_items(inprep)}\n      </ul>', "pub/inprep")
    pb = sub_h2(pb, "Invited talks",
                f'<ul class="pub-list">\n{pub_items(rows(doc, is_inv))}\n      </ul>', "pub/invited")
    # the 3 most recent of each (talks + posters), under their sub-headers
    def _yr(e):
        m = re.search(r"\d{4}", e[0] or "")
        return int(m.group()) if m else 0
    conf = ""
    for label, entries in groups(doc, is_conf):
        recent = sorted(entries, key=_yr, reverse=True)[:3]
        if label:
            conf += f'<h3 style="{SUBHEAD}">{esc(label)}</h3>\n      '
        conf += f'<ul class="pub-list">\n{pub_items(recent)}\n      </ul>\n      '
    pb = sub_conf(pb, conf.rstrip(), "pub/conf")
    write(os.path.join(HERE, "publications.html"), pb)

    # ---- teaching.html (fully CV-driven) ----
    tc = read(os.path.join(HERE, "teaching.html"))
    for label, entries in groups(doc, is_teach):
        low = norm(label or "")
        if low.startswith("graduate teaching"):
            tc = sub_h3(tc, "Graduate Teaching Assistant", tl_from(entries), "teach/grad")
        elif low.startswith("undergraduate teaching"):
            tc = sub_h3(tc, "Undergraduate Teaching Assistant", tl_from(entries), "teach/undergrad")
        elif low.startswith("pedagogical"):
            tc = sub_h3(tc, "Pedagogical training", tl_from(entries), "teach/pedagogy")
    for label, entries in groups(doc, is_syn):
        low = norm(label or "")
        if low.startswith("leadership"):
            tc = sub_h2(tc, "Mentoring &amp; leadership",
                        f'<ul class="tl">\n{tl_from(entries)}\n      </ul>', "teach/mentoring")
        elif low.startswith("volunteering"):
            tc = sub_h2(tc, "Outreach &amp; service",
                        f'<ul class="tl">\n{tl_from(entries)}\n      </ul>', "teach/outreach")
        elif low.startswith("reviewer"):
            rev = " ".join(inline(p)[0] for p in entries[0][1].paragraphs if p.text.strip())
            tc = re.sub(r'(<p class="svc-review"[^>]*>).*?(</p>)',
                        lambda m: m.group(1) + f"<strong>Journal peer review:</strong> {rev}" + m.group(2),
                        tc, count=1, flags=re.DOTALL)
    write(os.path.join(HERE, "teaching.html"), tc)

    # ---- research.html (funding from CV) ----
    rs = read(os.path.join(HERE, "research.html"))
    for _, entries in groups(doc, is_grant):
        rs = sub_h2(rs, "Selected research funding",
                    f'<ul class="tl">\n{grant_items(entries)}\n      </ul>', "research/funding")
    write(os.path.join(HERE, "research.html"), rs)

    print("Regenerated: cv.html, publications.html, teaching.html, research.html from CV.docx")

if __name__ == "__main__":
    main()
