#!/usr/bin/env python3
"""
optimize-photo.py — drop a new photo into a website "slot".

It resizes your photo to the right width for where it appears, fixes sideways
phone photos, strips location/EXIF data, and saves it as the correct file under
assets/img/ — so the layout stays fast and looks right.

Photos are grouped by page in assets/img/<page>/, so a slot name includes its
folder, e.g. "about/banner" or "research/gallery-1".

USAGE
    python3 tools/optimize-photo.py <your-photo> <slot>

EXAMPLES
    python3 tools/optimize-photo.py ~/Desktop/new_headshot.jpg about/headshot
    python3 tools/optimize-photo.py ~/Pictures/atlas.jpg about/banner
    python3 tools/optimize-photo.py ~/Pictures/kruger-fire.jpg research/gallery-3

Run with no arguments to see the list of slots.
After running, commit and push:
    git add . && git commit -m "Update photo" && git push
"""

import sys, os

# slot name (folder/name) -> width in pixels (height scales automatically)
SLOTS = {
    # About / home page  ->  assets/img/about/
    "about/banner":               2200,  # big banner photo behind your name
    "about/headshot":              900,  # round portrait photo
    "about/theme-paleohydrology": 1200,  # research-theme card: Paleo-hydrology and monsoons
    "about/theme-paleofire":      1200,  # research-theme card: Paleofire history
    "about/theme-vegetation":     1200,  # research-theme card: Ecosystem & vegetation change
    # Research page  ->  assets/img/research/
    "research/banner":                1800,  # wide banner strip
    "research/fieldwork-morocco":     1100,  # Taforalt / Morocco card
    "research/fieldwork-southafrica": 1100,  # Kruger / South Africa card
    "research/gallery-1": 1200, "research/gallery-2": 1200, "research/gallery-3": 1200,
    "research/gallery-4": 1200, "research/gallery-5": 1200, "research/gallery-6": 1200,
}

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(HERE, "assets", "img")


def usage_and_exit():
    print(__doc__)
    print("AVAILABLE SLOTS:")
    for name in SLOTS:
        print("   ", name)
    sys.exit(1)


def main():
    if len(sys.argv) != 3:
        usage_and_exit()

    src, slot = sys.argv[1], sys.argv[2].strip().lower()
    if slot.endswith(".jpg"):
        slot = slot[:-4]
    if slot not in SLOTS:
        print(f"Unknown slot: '{slot}'\n")
        usage_and_exit()
    if not os.path.isfile(src):
        print(f"Can't find that photo: {src}")
        sys.exit(1)

    try:
        from PIL import Image, ImageOps
    except ImportError:
        print("This script needs the Pillow library. Install it once with:")
        print("    pip3 install pillow")
        sys.exit(1)

    width = SLOTS[slot]
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)))
    out = os.path.join(OUTDIR, slot + ".jpg")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out, "JPEG", quality=82, optimize=True)

    kb = os.path.getsize(out) // 1024
    print(f"Saved {slot}.jpg  ({im.width}x{im.height}, {kb} KB)")
    print("Preview locally, then:  git add . && git commit -m \"Update photo\" && git push")


if __name__ == "__main__":
    main()
