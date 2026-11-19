#!/usr/bin/env python3
"""Compose the 19 November 2026 front page from stories.json.

Reads stories.json, draws seven original engraving-style illustrations
in one shared sepia duotone, lays out the broadsheet at exactly
1024x1024, and writes entry.png next to this file. Deterministic:
the same input always produces the same bytes.
"""

import json
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
W, H = 1024, 1024

PAPER = (246, 239, 221)
INK = (28, 23, 18)
MID = (111, 90, 62)
FAINT = (201, 180, 138)
RED = (138, 42, 28)
SKY = (222, 205, 168)
SEA = (61, 90, 116)
ART_BG = (233, 220, 192)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DISPLAY = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
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


def para(draw, x, y, text, fnt, max_w, leading, max_lines=None, color=INK):
    """Draw wrapped text; returns the y just below the last line."""
    lines = wrap(draw, text, fnt, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def kicker(draw, x, y, text, size=11):
    fnt = font(SANS_B, size)
    draw.text((x, y), text, font=fnt, fill=RED)
    return y + size + 5


def rule(draw, x, y, w, weight=2, color=INK):
    draw.line([(x, y), (x + w, y)], fill=color, width=weight)


def skyline(draw, x, y, w, h, rng, color, base):
    """A jagged tower skyline across (x, y, w, h); base is the ground line."""
    px = x
    while px < x + w - 8:
        tw = rng.randint(14, 42)
        th = rng.randint(int(h * 0.25), h)
        draw.rectangle([px, base - th, px + tw, base], fill=color)
        if rng.random() < 0.5:
            draw.rectangle([px + tw // 3, base - th - 8, px + 2 * tw // 3, base - th], fill=color)
        px += tw + rng.randint(2, 8)


def figure(draw, cx, ground, scale, suit, skin=(214, 178, 138)):
    """A small suited figure: head, torso, legs. scale ~ height in px."""
    head_r = scale * 0.11
    draw.ellipse([cx - head_r, ground - scale, cx + head_r, ground - scale + 2 * head_r], fill=skin)
    draw.rectangle([cx - scale * 0.16, ground - scale * 0.72, cx + scale * 0.16, ground - scale * 0.28], fill=suit)
    draw.polygon([(cx - scale * 0.16, ground - scale * 0.28), (cx + scale * 0.16, ground - scale * 0.28),
                  (cx + scale * 0.10, ground), (cx - scale * 0.10, ground)], fill=INK)
    draw.line([(cx - scale * 0.16, ground - scale * 0.55), (cx - scale * 0.28, ground - scale * 0.42)], fill=suit, width=3)
    draw.line([(cx + scale * 0.16, ground - scale * 0.55), (cx + scale * 0.28, ground - scale * 0.42)], fill=suit, width=3)


def art_summit(d, x, y, w, h, rng):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.ellipse([x + w - 90, y + 8, x + w - 30, y + 68], fill=(226, 196, 120))
    skyline(d, x, y + h - 78, w, 52, rng, (96, 78, 54), y + h - 26)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(58, 46, 32))
    # three leaders standing behind the long table
    tx, ty, tw = x + w * 0.08, y + h - 34, w * 0.84
    for i, suit in enumerate([(36, 34, 60), (138, 42, 28), (40, 52, 44)]):
        figure(d, tx + tw * (0.2 + 0.3 * i), y + h, 80, suit)
    d.rectangle([tx, ty, tx + tw, ty + 12], fill=(74, 52, 30))
    d.rectangle([tx + 8, ty + 12, tx + 22, y + h], fill=(58, 40, 24))
    d.rectangle([tx + tw - 22, ty + 12, tx + tw - 8, y + h], fill=(58, 40, 24))
    # three small flags on the table
    for i, col in enumerate([(178, 52, 48), (200, 40, 36), (52, 84, 138)]):
        fx = tx + tw * (0.14 + 0.36 * i)
        d.line([(fx, ty - 22), (fx, ty)], fill=INK, width=2)
        d.polygon([(fx, ty - 22), (fx + 18, ty - 17), (fx, ty - 12)], fill=col)


def art_gta(d, x, y, w, h, rng):
    d.rectangle([x, y, x + w, y + h], fill=(52, 34, 58))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(214, 140, 74))
    d.ellipse([x + w * 0.44, y + 6, x + w * 0.56, y + 42], fill=(240, 196, 110))
    skyline(d, x, y + h - 66, w, 44, rng, (30, 20, 36), y + h - 22)
    for _ in range(46):
        wx = rng.randint(x + 4, x + w - 8)
        wy = rng.randint(y + h - 62, y + h - 26)
        d.rectangle([wx, wy, wx + 3, wy + 4], fill=(240, 196, 110))
    # palm silhouettes
    for px in (x + 18, x + w - 30):
        d.line([(px, y + h - 22), (px, y + h - 58)], fill=INK, width=3)
        for a in range(-2, 3):
            d.arc([px - 16 + a * 3, y + h - 74, px + 16 + a * 3, y + h - 46], 200, 340, fill=INK, width=2)
    # low car
    cx, cy = x + w * 0.36, y + h - 22
    d.polygon([(cx, cy), (cx + 14, cy - 12), (cx + 52, cy - 12), (cx + 66, cy), (cx, cy)], fill=INK)
    d.ellipse([cx + 10, cy - 5, cx + 22, cy + 5], fill=INK)
    d.ellipse([cx + 44, cy - 5, cx + 56, cy + 5], fill=INK)


def art_icj(d, x, y, w, h, rng):
    d.rectangle([x, y, x + w, y + h], fill=ART_BG)
    # Peace Palace: pediment, columns, steps
    cx = x + w / 2
    d.polygon([(cx - w * 0.34, y + 34), (cx, y + 6), (cx + w * 0.34, y + 34)], fill=(96, 78, 54))
    d.rectangle([x + w * 0.14, y + 34, x + w * 0.86, y + h - 22], fill=(214, 196, 160))
    for i in range(5):
        colx = x + w * (0.18 + 0.13 * i)
        d.rectangle([colx, y + 40, colx + 12, y + h - 30], fill=(246, 239, 221))
    d.rectangle([x + w * 0.10, y + h - 30, x + w * 0.90, y + h - 22], fill=(96, 78, 54))
    d.rectangle([x + w * 0.06, y + h - 22, x + w * 0.94, y + h - 14], fill=(74, 58, 40))
    # scales of justice in front
    sx, sy = cx, y + h - 52
    d.line([(sx, sy - 26), (sx, sy + 6)], fill=INK, width=3)
    d.line([(sx - 26, sy - 26), (sx + 26, sy - 26)], fill=INK, width=3)
    d.ellipse([sx - 3, sy - 30, sx + 3, sy - 24], fill=RED)
    for s in (-1, 1):
        d.line([(sx + 26 * s, sy - 26), (sx + 16 * s, sy - 8)], fill=INK, width=2)
        d.arc([sx + 16 * s - 9, sy - 12, sx + 16 * s + 9, sy + 2], 0, 180, fill=INK, width=2)


def art_gulf(d, x, y, w, h, rng):
    d.rectangle([x, y, x + w, y + h], fill=(222, 205, 168))
    d.ellipse([x + w - 70, y + 6, x + w - 18, y + 58], fill=(232, 200, 120))
    # sea
    d.rectangle([x, y + h * 0.52, x + w, y + h], fill=SEA)
    for i in range(4):
        wy = y + h * (0.60 + 0.10 * i)
        d.line([(x + 6, wy), (x + w - 6, wy)], fill=(120, 150, 175), width=1)
    # coastline
    d.polygon([(x, y + h * 0.52), (x + w * 0.30, y + h * 0.34), (x + w * 0.55, y + h * 0.44),
               (x + w * 0.80, y + h * 0.30), (x + w, y + h * 0.40), (x + w, y + h * 0.52)], fill=(150, 122, 82))
    # two ships
    for sx, sy in ((x + w * 0.16, y + h * 0.66), (x + w * 0.62, y + h * 0.80)):
        d.polygon([(sx, sy), (sx + 46, sy), (sx + 38, sy + 12), (sx + 8, sy + 12)], fill=INK)
        d.rectangle([sx + 16, sy - 12, sx + 26, sy], fill=INK)
    # missile arcs
    for ax in (x + w * 0.30, x + w * 0.55):
        d.arc([ax - 40, y + 8, ax + 40, y + 66], 200, 340, fill=RED, width=2)
        d.ellipse([ax - 3, y + 10, ax + 3, y + 16], fill=RED)


def art_chip(d, x, y, w, h, rng):
    d.rectangle([x, y, x + w, y + h], fill=(36, 40, 52))
    cx, cy = x + w / 2, y + h / 2
    s = min(w, h) * 0.30
    # pins
    for i in range(5):
        off = -s + i * s / 2
        d.line([(cx + off, cy - s - 12), (cx + off, cy - s)], fill=(214, 196, 140), width=3)
        d.line([(cx + off, cy + s), (cx + off, cy + s + 12)], fill=(214, 196, 140), width=3)
        d.line([(cx - s - 12, cy + off), (cx - s, cy + off)], fill=(214, 196, 140), width=3)
        d.line([(cx + s, cy + off), (cx + s + 12, cy + off)], fill=(214, 196, 140), width=3)
    d.rectangle([cx - s, cy - s, cx + s, cy + s], fill=(74, 96, 122), outline=(214, 196, 140), width=2)
    d.rectangle([cx - s * 0.55, cy - s * 0.55, cx + s * 0.55, cy + s * 0.55], fill=(214, 196, 140))
    # upward arrow
    d.line([(cx - s * 0.28, cy + s * 0.30), (cx + s * 0.28, cy - s * 0.30)], fill=RED, width=4)
    d.polygon([(cx + s * 0.28, cy - s * 0.30), (cx + s * 0.05, cy - s * 0.30), (cx + s * 0.28, cy - s * 0.08)], fill=RED)
    d.text((cx - 16, cy + s * 0.62), "H200", font=font(SANS_B, 11), fill=(240, 220, 180))
    d.line([(cx - 20, cy + s * 0.62), (cx + 20, cy + s * 0.80)], fill=RED, width=2)


def art_cyclone(d, x, y, w, h, rng):
    d.rectangle([x, y, x + w, y + h], fill=(214, 205, 178))
    cx, cy = x + w * 0.52, y + h * 0.46
    # spiral bands
    for r in range(8, 62, 9):
        d.arc([cx - r, cy - r * 0.8, cx + r, cy + r * 0.8], 20 + r * 3, 300 + r * 3, fill=SEA, width=4)
    d.ellipse([cx - 7, cy - 6, cx + 7, cy + 6], fill=RED)
    # coastline and rain
    d.polygon([(x, y + h), (x, y + h * 0.78), (x + w * 0.34, y + h * 0.86), (x + w * 0.30, y + h)], fill=(150, 122, 82))
    for _ in range(22):
        rx = rng.randint(x + 6, x + w - 6)
        ry = rng.randint(y + 4, y + h - 10)
        d.line([(rx, ry), (rx - 4, ry + 10)], fill=(90, 110, 130), width=1)


def art_gaza(d, x, y, w, h, rng):
    d.rectangle([x, y, x + w, y + h], fill=(226, 206, 164))
    d.ellipse([x + 12, y + 6, x + 52, y + 46], fill=(232, 200, 120))
    # skyline with a dome and a minaret
    d.rectangle([x, y + h - 40, x + w, y + h], fill=(58, 46, 32))
    skyline(d, x + 6, y + h - 62, w - 12, 26, rng, (96, 78, 54), y + h - 40)
    d.ellipse([x + w * 0.60, y + h - 66, x + w * 0.74, y + h - 48], fill=(96, 78, 54))
    d.rectangle([x + w * 0.80, y + h - 84, x + w * 0.84, y + h - 40], fill=(96, 78, 54))
    # smoke columns
    for sx in (x + w * 0.30, x + w * 0.52):
        for i in range(4):
            r = 5 + i * 3
            d.ellipse([sx - r, y + 14 + i * 12 - r, sx + r, y + 14 + i * 12 + r],
                      fill=(196, 186, 164))


ART = {"summit": art_summit, "gta": art_gta, "icj": art_icj, "gulf": art_gulf,
       "chip": art_chip, "cyclone": art_cyclone, "gaza": art_gaza}


def grain(img, seed=20261119):
    """A whisper of paper grain, seeded so the file is byte-stable."""
    rng = random.Random(seed)
    px = img.load()
    for _ in range(3500):
        px[rng.randint(0, W - 1), rng.randint(0, H - 1)] = (
            rng.choice([(238, 230, 212), (250, 244, 230), (242, 234, 216)]))


def build():
    data = json.loads((ROOT / "stories.json").read_text())
    rng = random.Random(20261119)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 26
    cw = W - 2 * mx  # 972

    # --- masthead ---
    y = 12
    mast = font(DISPLAY, 56)
    tw = d.textlength(data["masthead"], font=mast)
    d.text(((W - tw) / 2, y), data["masthead"], font=mast, fill=INK)
    y += 66
    rule(d, mx, y, cw, 3)
    y += 6
    d.text((mx, y), data["dateline"], font=font(SANS_B, 12), fill=INK)
    tag = data["tagline"]
    d.text((W - mx - d.textlength(tag, font=font(SANS_B, 12)), y), tag,
           font=font(SANS_B, 12), fill=RED)
    y += 20
    rule(d, mx, y, cw, 1)

    # --- lead ---
    y += 10
    y = kicker(d, mx, y, data["lead"]["kicker"], 12)
    y = para(d, mx, y, data["lead"]["headline"], font(DISPLAY, 46), cw, 50, max_lines=1)
    y = para(d, mx, y + 2, data["lead"]["deck"], font(SERIF, 16), cw, 21, max_lines=2)
    y += 6
    art_h = 120
    ART[data["lead"]["art"]](d, mx, y, cw, art_h, rng)
    d.rectangle([mx, y, mx + cw, y + art_h], outline=INK, width=2)
    y += art_h + 10
    rule(d, mx, y, cw, 2)

    # --- two big panels ---
    y += 10
    big_w = (cw - 10) // 2
    big_top = y
    for i, p in enumerate(data["panels_big"]):
        px = mx + i * (big_w + 10)
        ah = 92
        ART[p["art"]](d, px, y, big_w, ah, rng)
        d.rectangle([px, y, px + big_w, y + ah], outline=INK, width=2)
        py = y + ah + 6
        py = kicker(d, px, py, p["kicker"], 10)
        py = para(d, px, py, p["headline"], font(SERIF_B, 19), big_w, 23, max_lines=2)
        py = para(d, px, py + 1, p["deck"], font(SERIF, 12), big_w, 15, max_lines=3)
    y = big_top + 92 + 6 + 15 + 46 + 45 + 4
    rule(d, mx, y, cw, 2)

    # --- four small panels ---
    y += 10
    sm_w = (cw - 30) // 4
    sm_top = y
    for i, p in enumerate(data["panels_small"]):
        px = mx + i * (sm_w + 10)
        ah = 62
        ART[p["art"]](d, px, y, sm_w, ah, rng)
        d.rectangle([px, y, px + sm_w, y + ah], outline=INK, width=2)
        py = y + ah + 5
        py = kicker(d, px, py, p["kicker"], 9)
        py = para(d, px, py, p["headline"], font(SERIF_B, 14), sm_w, 17, max_lines=2)
        py = para(d, px, py + 1, p["deck"], font(SERIF, 11), sm_w, 13, max_lines=3)
    y = sm_top + 62 + 5 + 14 + 34 + 39 + 4
    rule(d, mx, y, cw, 2)

    # --- columns: 12 more stories ---
    y += 9
    col_w = (cw - 20) // 3
    for i, s in enumerate(data["columns"]):
        cx = mx + (i // 4) * (col_w + 10)
        cy = y + (i % 4) * 25
        # shrink the headline until it fits on one line
        size = 12
        while size > 9 and len(wrap(d, s["headline"], font(SERIF_B, size), col_w)) > 1:
            size -= 1
        para(d, cx, cy, s["headline"], font(SERIF_B, size), col_w, 14, max_lines=1)
        para(d, cx, cy + 13, s["deck"], font(SERIF, 10), col_w, 12, max_lines=1)
    y += 4 * 25 + 4
    rule(d, mx, y, cw, 1)

    # --- one-liners: 20 briefs in two columns ---
    y += 8
    half = (cw - 10) // 2
    for i, line in enumerate(data["one_liners"]):
        ox = mx + (i // 10) * (half + 10)
        oy = y + (i % 10) * 12
        d.text((ox, oy), "▪ " + line, font=font(SANS, 10), fill=INK)
    y += 10 * 12 + 6
    rule(d, mx, y, cw, 1)
    y += 5
    d.text((mx, y), data["footer"], font=font(SANS, 9), fill=MID)
    assert y + 12 < H - 8, f"layout overflow: footer at y={y}"

    # frame + grain
    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=2)
    grain(img)
    img.save(ROOT / "entry.png", optimize=True)


if __name__ == "__main__":
    build()
    print("wrote entry.png")
