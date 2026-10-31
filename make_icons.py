"""
Generates the home-screen icons into ./icons/

  python make_icons.py                      -> draws a default emerald/gold 8-point star
  python make_icons.py favicon_open_quran.png   -> builds the icons from your own logo

Needs Pillow:  pip install pillow
"""
import math, sys, os
from PIL import Image, ImageDraw

EMERALD, DARK, GOLD = (15, 92, 77), (10, 69, 56), (184, 137, 58)
os.makedirs("icons", exist_ok=True)

def star(size, radius_frac):
    k = 4                                   # supersample for smooth edges
    S = size * k
    img = Image.new("RGB", (S, S), EMERALD)
    d = ImageDraw.Draw(img)
    cx = cy = S / 2
    R = S * radius_frac
    r = R * 0.7654                          # inner vertex of the 8-point star
    pts = []
    for i in range(16):
        ang = math.radians(i * 22.5 - 90)
        rad = R if i % 2 == 0 else r
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=DARK)
    d.line(pts + [pts[0], pts[1]], fill=GOLD, width=max(2, S // 70), joint="curve")
    # inner ring + centre dot
    ir = R * 0.52
    d.ellipse([cx - ir, cy - ir, cx + ir, cy + ir], outline=GOLD, width=max(2, S // 110))
    dr = R * 0.16
    d.ellipse([cx - dr, cy - dr, cx + dr, cy + dr], fill=GOLD)
    return img.resize((size, size), Image.LANCZOS)

def from_logo(path, size, content_frac):
    logo = Image.open(path).convert("RGBA")
    canvas = Image.new("RGB", (size, size), EMERALD)
    box = int(size * content_frac)
    logo.thumbnail((box, box), Image.LANCZOS)
    canvas.paste(logo, ((size - logo.width) // 2, (size - logo.height) // 2), logo)
    return canvas

src = sys.argv[1] if len(sys.argv) > 1 else None
make = (lambda s, f: from_logo(src, s, f)) if src else star

# "any" icons: content can fill most of the square
make(192, 0.76 if src else 0.38).save("icons/icon-192.png")
make(512, 0.76 if src else 0.38).save("icons/icon-512.png")
# iOS: full-bleed square, iOS rounds the corners itself
make(180, 0.76 if src else 0.38).save("icons/apple-touch-icon.png")
# maskable: Android may crop to a circle, so keep content inside the middle ~64%
make(512, 0.60 if src else 0.30).save("icons/icon-maskable-512.png")
print("Icons written to ./icons/")
