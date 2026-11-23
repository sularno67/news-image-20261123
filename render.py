#!/usr/bin/env python3
"""Render the front page for Monday 23 November 2026 as a 1024x1024 PNG.

Draws everything with PIL from scratch: masthead, lead story, three
supporting stories, two more stories and a briefs strip. All text and
art are drawn in code; no external images are used.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (17, 17, 17)
RED = (176, 42, 32)
BLUE = (31, 82, 128)
GREEN = (46, 110, 66)
GOLD = (184, 134, 11)
GREY = (90, 86, 78)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    """Draw wrapped paragraph, return y after last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_globe_crack(draw, cx, cy, r):
    """Earth with a jagged crack: the COP31 lead illustration."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(126, 178, 205),
                 outline=INK, width=4)
    # land masses (simple blobs)
    draw.ellipse([cx - r * 0.72, cy - r * 0.55, cx - r * 0.05, cy + r * 0.05],
                 fill=GREEN)
    draw.ellipse([cx + r * 0.05, cy + r * 0.05, cx + r * 0.7, cy + r * 0.62],
                 fill=GREEN)
    draw.ellipse([cx - r * 0.3, cy - r * 0.9, cx + r * 0.35, cy - r * 0.45],
                 fill=GREEN)
    # crack zig-zag across the globe
    pts = [(cx - r * 0.55, cy - r * 0.75), (cx - r * 0.2, cy - r * 0.35),
           (cx - r * 0.45, cy + r * 0.05), (cx - r * 0.05, cy + r * 0.4),
           (cx - r * 0.3, cy + r * 0.75)]
    draw.line(pts, fill=RED, width=7, joint="curve")
    # small smoke puffs above
    for sx, sy, sr in [(cx - r * 0.5, cy - r * 1.02, 11),
                       (cx - r * 0.28, cy - r * 1.12, 13),
                       (cx + r * 0.05, cy - r * 1.02, 10)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=GREY)


def draw_rubble(draw, x, y, s):
    """Collapsed building: grey blocks and a small red cross of rescue."""
    draw.rectangle([x, y + s * 0.55, x + s, y + s], fill=(120, 116, 108))
    draw.polygon([(x + s * 0.1, y + s * 0.55), (x + s * 0.45, y + s * 0.2),
                  (x + s * 0.8, y + s * 0.55)], fill=(150, 146, 136))
    draw.rectangle([x + s * 0.15, y + s * 0.65, x + s * 0.4, y + s * 0.9],
                   fill=(90, 86, 78))
    draw.rectangle([x + s * 0.6, y + s * 0.7, x + s * 0.85, y + s * 0.95],
                   fill=(90, 86, 78))
    # rescue ladder
    draw.line([(x + s * 0.55, y + s * 0.15), (x + s * 0.85, y + s * 0.6)],
              fill=RED, width=6)
    draw.line([(x + s * 0.6, y + s * 0.3), (x + s * 0.75, y + s * 0.38)],
              fill=RED, width=4)


def draw_chart(draw, x, y, s):
    """Falling market chart with a red down arrow."""
    draw.rectangle([x, y, x + s, y + s], outline=INK, width=2)
    pts = [(x + s * 0.12, y + s * 0.25), (x + s * 0.32, y + s * 0.35),
           (x + s * 0.5, y + s * 0.3), (x + s * 0.68, y + s * 0.55),
           (x + s * 0.88, y + s * 0.8)]
    draw.line(pts, fill=RED, width=6, joint="curve")
    draw.polygon([(x + s * 0.88, y + s * 0.8), (x + s * 0.72, y + s * 0.78),
                  (x + s * 0.86, y + s * 0.62)], fill=RED)


def draw_capitol(draw, x, y, s):
    """US Capitol dome silhouette."""
    draw.rectangle([x + s * 0.1, y + s * 0.75, x + s * 0.9, y + s], fill=BLUE)
    draw.rectangle([x + s * 0.2, y + s * 0.6, x + s * 0.8, y + s * 0.75],
                   fill=BLUE)
    draw.pieslice([x + s * 0.3, y + s * 0.2, x + s * 0.7, y + s * 0.65],
                  180, 360, fill=BLUE)
    draw.rectangle([x + s * 0.47, y + s * 0.05, x + s * 0.53, y + s * 0.22],
                   fill=BLUE)
    for i in range(4):
        cx = x + s * (0.22 + i * 0.18)
        draw.rectangle([cx, y + s * 0.8, cx + s * 0.06, y + s * 0.95],
                       fill=PAPER)


def draw_ball(draw, x, y, s):
    """Tennis ball with curved seams."""
    draw.ellipse([x, y, x + s, y + s], fill=(196, 214, 54), outline=INK,
                 width=3)
    draw.arc([x - s * 0.35, y + s * 0.1, x + s * 0.45, y + s * 0.9], 300, 60,
             fill=INK, width=4)
    draw.arc([x + s * 0.55, y + s * 0.1, x + s * 1.35, y + s * 0.9], 120, 240,
             fill=INK, width=4)


def draw_ship(draw, x, y, s):
    """Container ship: hull plus stacked boxes."""
    draw.polygon([(x, y + s * 0.55), (x + s, y + s * 0.55),
                  (x + s * 0.88, y + s * 0.95), (x + s * 0.12, y + s * 0.95)],
                 fill=BLUE)
    for i, col in enumerate([RED, GOLD, GREEN]):
        draw.rectangle([x + s * (0.15 + i * 0.24), y + s * 0.3,
                        x + s * (0.35 + i * 0.24), y + s * 0.52], fill=col,
                       outline=INK, width=2)
    draw.rectangle([x + s * 0.28, y + s * 0.08, x + s * 0.5, y + s * 0.28],
                   fill=RED, outline=INK, width=2)


def kicker(draw, x, y, text):
    f = font(SANS_B, 21)
    draw.text((x, y), text.upper(), font=f, fill=RED)
    return y + 28


def headline(draw, x, y, text, size, max_w, leading, fnt_path=SERIF_B):
    f = font(fnt_path, size)
    return para(draw, x, y, text, f, max_w, leading)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 30  # margin
    right = W - M

    # ---- masthead ----
    d.text((W // 2, 18), "THE WORLD IN ONE DAY", font=font(SERIF_B, 56),
           fill=INK, anchor="ma")
    rule(d, M, 92, right, 3)
    rule(d, M, 98, right, 1)
    # date band: black bar, white text -- the day, unmissable
    d.rectangle([M, 108, right, 156], fill=INK)
    d.text((W // 2, 117), "MONDAY  23  NOVEMBER  2026", font=font(SANS_B, 30),
           fill=(255, 255, 255), anchor="ma")

    # ---- lead story: COP31 ----
    y = 176
    y = kicker(d, M, y, "Climate  •  Antalya, Turkey")
    lead_w = 560
    y = headline(d, M, y, "COP31 ends with no deal", 47, lead_w, 54)
    y += 6
    y = para(d, M, y,
             "Climate talks in Antalya collapsed after two days of "
             "overtime. The EU and about 130 nations rejected a draft "
             "that left out fossil fuels — the first COP to fail to "
             "reach a deal since 2009.",
             font(SANS, 23), lead_w, 30)
    # lead illustration panel
    px0, py0, px1, py1 = 622, 176, right, 452
    d.rectangle([px0, py0, px1, py1], outline=INK, width=2)
    draw_globe_crack(d, (px0 + px1) // 2, 300, 92)
    d.text(((px0 + px1) // 2, 404), "NO DEAL IN ANTALYA",
           font=font(SANS_B, 22), fill=RED, anchor="ma")
    rule(d, M, 470, right, 2)

    # ---- three supporting stories ----
    col_w = (W - 2 * M - 2 * 24) // 3
    tops = 488
    stories = [
        ("Ukraine", "Boy, 7, pulled alive from rubble",
         "Rescuers freed a seven-year-old after 14 hours under a "
         "collapsed block in Dymer, north of Kyiv. Russian strikes "
         "killed at least 11 people.", draw_rubble),
        ("Markets", "AI sell-off rattles world markets",
         "Japan's Nikkei fell 5.06% and the S&P 500 slid 3.7% as "
         "fears grew that AI shares are overpriced. Gold rose as "
         "investors sought safety.", draw_chart),
        ("United States", "Democrats' biggest House win since 1992",
         "Democrats clinched at least 258 House seats after flipping "
         "a North Carolina seat in a recount — their largest "
         "majority in 34 years.", draw_capitol),
    ]
    for i, (kick, head, body, art) in enumerate(stories):
        x = M + i * (col_w + 24)
        yy = kicker(d, x, tops, kick)
        art(d, x, yy, 56)
        yy += 66
        yy = headline(d, x, yy, head, 24, col_w, 28)
        yy += 4
        para(d, x, yy, body, font(SANS, 17), col_w, 22)
        if i < 2:
            d.line([(x + col_w + 12, tops), (x + col_w + 12, 776)],
                   fill=GREY, width=1)
    rule(d, M, 790, right, 2)

    # ---- second row: sport + Asia ----
    half_w = (W - 2 * M - 24) // 2
    y2 = 806
    y2 = kicker(d, M, y2, "Sport  •  Turin")
    draw_ball(d, M, y2, 52)
    yy = headline(d, M + 66, y2 + 2, "Alcaraz wins first ATP Finals title",
                  20, half_w - 66, 26)
    para(d, M + 66, yy + 4,
         "Carlos Alcaraz beat world No. 1 Alexander Zverev 6–2, 7–6 "
         "to cap a comeback season.",
         font(SANS, 17), half_w - 66, 22)

    x2 = M + half_w + 24
    y3 = kicker(d, x2, 806, "Asia  •  Seoul")
    draw_ship(d, x2, y3, 52)
    yy = headline(d, x2 + 66, y3 + 2, "South Korea exports top $1 trillion",
                  20, half_w - 66, 26)
    para(d, x2 + 66, yy + 4,
         "Annual exports passed $1 trillion for the first time, "
         "driven by demand for AI chips.",
         font(SANS, 17), half_w - 66, 22)
    rule(d, M, 922, right, 2)

    # ---- briefs strip: two columns of two ----
    yb = 936
    d.text((M, yb), "IN BRIEF", font=font(SANS_B, 20), fill=RED)
    briefs_l = [
        "Israeli strike hits Beirut, killing a Hezbollah chief of staff.",
        "Magnitude 6.5 quake strikes off Vanuatu.",
    ]
    briefs_r = [
        "FBI fugitive 'El Chapo Isidro' captured in Mexico.",
        "FIFA to confirm UK as 2035 Women's World Cup host.",
    ]
    yb += 30
    for b in briefs_l:
        d.text((M + 14, yb), "•  " + b, font=font(SANS, 16), fill=INK)
        yb += 22
    yb = 966
    for b in briefs_r:
        d.text((W // 2 + 14, yb), "•  " + b, font=font(SANS, 16), fill=INK)
        yb += 22

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
