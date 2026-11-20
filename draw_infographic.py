#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news infographic (1024x1024 PNG).

Build-time only: run `python3 draw_infographic.py` to (re)generate entry.png.
Everything is hand-drawn with Pillow shapes and DejaVu fonts; no photos,
no network, no downloaded assets.
"""
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

W = H = 1024
NAVY = (13, 27, 46)
NAVY_SOFT = (24, 45, 70)
GOLD = (232, 184, 75)
INK = (18, 28, 40)
MUTED = (96, 110, 128)
CARD = (255, 255, 255)
PAGE = (238, 241, 245)
SUB = (185, 198, 214)
FOOT = (159, 176, 195)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap using real text widths."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_hourglass(d, x, y):
    d.polygon([(x + 16, y + 12), (x + 62, y + 12), (x + 39, y + 34)],
              fill=(255, 255, 255))
    d.polygon([(x + 39, y + 44), (x + 16, y + 66), (x + 62, y + 66)],
              fill=(255, 255, 255))
    d.rectangle([x + 12, y + 8, x + 66, y + 12], fill=(255, 255, 255))
    d.rectangle([x + 12, y + 66, x + 66, y + 70], fill=(255, 255, 255))
    d.rectangle([x + 37, y + 34, x + 41, y + 44], fill=(255, 255, 255))


def draw_flags(d, x, y):
    # Ukraine flag (left) and Russian flag (right), poles + a table line.
    d.rectangle([x + 8, y + 14, x + 36, y + 25], fill=(255, 255, 255))
    d.rectangle([x + 8, y + 14, x + 36, y + 19], fill=(70, 130, 200))
    d.rectangle([x + 8, y + 20, x + 36, y + 25], fill=(255, 215, 60))
    d.rectangle([x + 42, y + 14, x + 70, y + 25], fill=(255, 255, 255))
    d.rectangle([x + 42, y + 14, x + 70, y + 17], fill=(255, 255, 255))
    d.rectangle([x + 42, y + 18, x + 70, y + 21], fill=(60, 110, 200))
    d.rectangle([x + 42, y + 22, x + 70, y + 25], fill=(210, 60, 50))
    d.line([x + 6, y + 14, x + 6, y + 62], fill=(255, 255, 255), width=3)
    d.line([x + 72, y + 14, x + 72, y + 62], fill=(255, 255, 255), width=3)


def draw_voyager(d, x, y):
    for sx, sy in [(x + 8, y + 8), (x + 66, y + 12), (x + 12, y + 60),
                   (x + 70, y + 58)]:
        d.line([sx - 4, sy, sx + 4, sy], fill=(255, 255, 255), width=2)
        d.line([sx, sy - 4, sx, sy + 4], fill=(255, 255, 255), width=2)
    d.line([x + 39, y + 20, x + 39, y + 8], fill=(255, 255, 255), width=3)
    d.ellipse([x + 35, y + 4, x + 43, y + 12], fill=(255, 215, 60))
    d.polygon([(x + 39, y + 20), (x + 58, y + 54), (x + 20, y + 54)],
              fill=(255, 215, 60))
    d.ellipse([x + 44, y + 30, x + 62, y + 48], outline=(255, 255, 255),
              width=3)
    d.line([x + 47, y + 33, x + 39, y + 40], fill=(255, 255, 255), width=3)


def draw_capsule(d, x, y):
    d.rounded_rectangle([x + 10, y + 30, x + 68, y + 52], radius=11,
                        fill=(255, 255, 255))
    d.rounded_rectangle([x + 10, y + 30, x + 39, y + 52], radius=11,
                        fill=(31, 138, 107))
    d.rectangle([x + 28, y + 30, x + 39, y + 52], fill=(31, 138, 107))
    d.line([x + 39, y + 31, x + 39, y + 51], fill=(31, 138, 107), width=2)
    d.line([x + 58, y + 8, x + 58, y + 20], fill=(255, 255, 255), width=4)
    d.line([x + 52, y + 14, x + 64, y + 14], fill=(255, 255, 255), width=4)


def draw_leaf(d, x, y):
    d.polygon([(x + 39, y + 8), (x + 64, y + 28), (x + 58, y + 60),
               (x + 30, y + 64), (x + 14, y + 38)], fill=(255, 255, 255))
    d.line([x + 22, y + 58, x + 56, y + 16], fill=(199, 125, 31), width=3)
    d.polygon([(x + 60, y + 44), (x + 70, y + 60), (x + 50, y + 60)],
              fill=(255, 215, 60))


def draw_bag(d, x, y):
    d.arc([x + 28, y + 8, x + 50, y + 34], start=180, end=360,
          fill=(255, 255, 255), width=4)
    d.polygon([(x + 18, y + 28), (x + 60, y + 28), (x + 56, y + 68),
               (x + 22, y + 68)], fill=(255, 255, 255))
    d.line([x + 34, y + 40, x + 44, y + 52], fill=(163, 74, 110), width=4)
    d.line([x + 44, y + 40, x + 34, y + 52], fill=(163, 74, 110), width=4)


STORIES = [
    dict(tag="UNITED STATES", color=(179, 64, 46), icon=draw_hourglass,
         title="Trump: no Iran call until after 1 January",
         body=("The president says he is 'not rushing' a decision on new "
               "Iran strikes - and will 'see what happens' in the new year."),
         source="Reuters"),
    dict(tag="EUROPE", color=(46, 111, 176), icon=draw_flags,
         title="Europe ready for Ukraine peace talks",
         body=("At a Berlin summit, European allies say they hold a united "
               "position and are ready to negotiate with Moscow."),
         source="BBC"),
    dict(tag="SPACE", color=(91, 75, 138), icon=draw_voyager,
         title="Voyager 1: a full light-day from Earth",
         body=("NASA confirms the 1977 probe is now so far away that its "
               "radio signals take a whole day to reach Earth."),
         source="AP"),
    dict(tag="HEALTH", color=(31, 138, 107), icon=draw_capsule,
         title="Cancer pill 'wipes out' tumours in trial",
         body=("Daraxonrasib plus chemotherapy shrank or cleared tumours in "
               "61% of patients; in 1 in 12, they vanished."),
         source="The Times"),
    dict(tag="TECH & CLIMATE", color=(199, 125, 31), icon=draw_leaf,
         title="Meta rethinks its 2030 net-zero goal",
         body=("Its emissions rose 45% in 2025 as AI data centres grew; "
               "the pledge set in 2020 is now under review."),
         source="AP / Bloomberg"),
    dict(tag="ECONOMY", color=(163, 74, 110), icon=draw_bag,
         title="UK shoppers cheer up before Black Friday",
         body=("Consumer confidence rose to -22 in November as shoppers "
               "prepared for big purchases, the GfK survey says."),
         source="Reuters"),
]


def main():
    img = Image.new("RGB", (W, H), PAGE)
    d = ImageDraw.Draw(img)

    # Header band.
    d.rectangle([0, 0, W, 150], fill=NAVY)
    d.rectangle([0, 150, W, 154], fill=GOLD)
    d.text((24, 22), "THE WORLD IN ONE PICTURE",
           font=font(FONT_B, 21), fill=GOLD)
    d.text((24, 50), "Friday 20 November 2026",
           font=font(FONT_B, 54), fill=(255, 255, 255))
    d.text((24, 114), "Six stories that defined the day - from Washington "
                      "to the edge of the Solar System",
           font=font(FONT, 21), fill=SUB)

    # Story cards: 2 columns x 3 rows.
    cw, ch, gap, mx = 478, 236, 20, 24
    for i, s in enumerate(STORIES):
        cx = mx + (i % 2) * (cw + gap)
        cy = 170 + (i // 2) * (ch + gap)
        d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=16, fill=CARD)
        d.rounded_rectangle([cx, cy, cx + 10, cy + ch], radius=5,
                            fill=s["color"])
        # Icon tile.
        ix, iy = cx + 20, cy + 18
        d.rounded_rectangle([ix, iy, ix + 78, iy + 78], radius=14,
                            fill=s["color"])
        s["icon"](d, ix, iy)
        # Tag + headline.
        d.text((ix + 94, cy + 20), s["tag"], font=font(FONT_B, 16),
               fill=s["color"])
        lines = wrap(d, s["title"], font(FONT_B, 27), cw - 132)
        y = cy + 44
        for line in lines[:2]:
            d.text((ix + 94, y), line, font=font(FONT_B, 27), fill=INK)
            y += 32
        # Body.
        blines = wrap(d, s["body"], font(FONT, 20), cw - 40)
        y = cy + 112
        for line in blines[:3]:
            d.text((cx + 20, y), line, font=font(FONT, 20), fill=(52, 66, 84))
            y += 27
        # Source tag, bottom right.
        src = f"Source: {s['source']}"
        d.text((cx + cw - 20 - d.textlength(src, font=font(FONT, 15)),
                cy + ch - 26), src, font=font(FONT, 15), fill=MUTED)

    # Footer band.
    d.rectangle([0, 938, W, H], fill=NAVY)
    d.text((24, 954), "Sources: Reuters  |  Associated Press  |  BBC  |  "
                      "The Times  |  Bangkok Post",
           font=font(FONT, 18), fill=(255, 255, 255))
    d.text((24, 984), "Hand-drawn with Pillow - no photographs. Every story "
                      "first reported on 20 November 2026 (any time zone).",
           font=font(FONT, 16), fill=FOOT)

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} {OUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
