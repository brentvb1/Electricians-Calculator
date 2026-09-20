"""Regenerate the app icons. Run from the repo root: python3 scripts/make_icons.py"""
from PIL import Image, ImageDraw
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BG = (13, 17, 23, 255)        # #0d1117
ACCENT = (232, 149, 47, 255)  # #e8952f
ACCENT_DARK = (196, 118, 22, 255)

def rounded_square(size, radius_ratio=0.22):
    img = Image.new("RGBA", (size, size), (0,0,0,0))
    d = ImageDraw.Draw(img)
    r = int(size * radius_ratio)
    d.rounded_rectangle([0, 0, size-1, size-1], radius=r, fill=BG)
    return img, d

def bolt_path(size, cx_ratio=0.5, scale=0.62):
    # classic lightning-bolt polygon, defined in a 100x100 box then scaled
    pts = [
        (58, 6), (22, 56), (46, 56), (40, 94),
        (80, 42), (54, 42), (58, 6)
    ]
    s = size * scale / 100.0
    off_x = size*0.5 - 50*s
    off_y = size*0.5 - 50*s
    return [(x*s+off_x, y*s+off_y) for x, y in pts]

def make_icon(size, filename, with_border=True):
    img, d = rounded_square(size)
    if with_border:
        r = int(size*0.22)
        d.rounded_rectangle([1,1,size-2,size-2], radius=r, outline=ACCENT_DARK, width=max(1,size//64))
    poly = bolt_path(size)
    d.polygon(poly, fill=ACCENT)
    img.save(filename)
    print("wrote", filename, size)

make_icon(192, os.path.join(ROOT, "icon-192.png"))
make_icon(512, os.path.join(ROOT, "icon-512.png"))

# apple touch icon: opaque, full bleed, no transparency, slightly less border emphasis
img = Image.new("RGB", (180,180), BG[:3])
d = ImageDraw.Draw(img)
poly = bolt_path(180, scale=0.6)
d.polygon(poly, fill=ACCENT[:3])
img.save(os.path.join(ROOT, "apple-touch-icon.png"))
print("wrote apple-touch-icon.png")

# favicon 32
make_icon(32, os.path.join(ROOT, "icon-32.png"), with_border=False)
