#!/usr/bin/env python3
"""Draw entry.png for the news-image-20261119 bounty.

One 1024x1024 infographic summing up Thursday 19 November 2026's world
news. Deterministic: fixed colours, fixed fonts, no timestamps, no random
numbers, so running it twice writes byte-identical output.

Run: python3 draw.py  ->  writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

# --- palette ---------------------------------------------------------------
BG = (13, 18, 38)          # dark navy
PANEL = (30, 38, 66)        # panel fill
PANEL_EDGE = (52, 62, 96)   # panel outline
WHITE = (245, 247, 255)
GREY = (178, 188, 214)      # sub-line text
GOLD = (255, 193, 60)       # subtitle / rules
DARK = (13, 18, 38)         # icon glyph colour

# --- fonts -----------------------------------------------------------------
def load_font(bold, size):
    names = ("DejaVuSans-Bold.ttf", "DejaVuSans.ttf") if bold else (
        "DejaVuSans.ttf", "DejaVuSans-Bold.ttf")
    for name in names:
        path = os.path.join("/usr/share/fonts/truetype/dejavu", name)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def fit_font(bold, text, start_size, max_w):
    """Largest font size (<= start_size) at which text fits max_w."""
    size = start_size
    while size > 24:
        f = load_font(bold, size)
        if ImageDraw.Draw(Image.new("RGB", (8, 8))).textlength(
                text, font=f) <= max_w:
            return f
        size -= 2
    return load_font(bold, 24)


F_TITLE = fit_font(True, "THURSDAY, 19 NOVEMBER 2026", 62, 960)
F_SUB = load_font(True, 26)
F_KICK = load_font(True, 23)
F_HEAD = load_font(True, 33)
F_BODY = load_font(False, 22)

# --- text helpers ----------------------------------------------------------
def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, y, text, font, fill):
    w = draw.textlength(text, font=font)
    draw.text(((W - w) / 2, y), text, font=font, fill=fill)
    return w


def letter_spaced(text, gap="  "):
    return gap.join(list(text.replace(" ", "   ")))


# --- icons (drawn with PIL shapes, one per panel) --------------------------
def icon_scales(d, cx, cy, r, colour):
    # scales of justice: vertical post, crossbar, two pans
    d.line([(cx, cy - r + 6), (cx, cy + r - 6)], fill=colour, width=4)
    d.line([(cx - r + 8, cy - r + 12), (cx + r - 8, cy - r + 12)],
           fill=colour, width=4)
    for sx in (-1, 1):
        px = cx + sx * (r - 10)
        d.line([(px, cy - r + 12), (px, cy + 2)], fill=colour, width=3)
        d.pieslice([px - 11, cy - 2, px + 11, cy + 12], 0, 180, fill=colour)
    d.ellipse([cx - 4, cy - r + 2, cx + 4, cy - r + 10], fill=colour)


def icon_summit(d, cx, cy, r, colour):
    # three leaders: three overlapping circles
    for dx, dy, rr in ((-13, 2, 11), (13, 2, 11), (0, -13, 11)):
        d.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr],
                  fill=colour)


def icon_chart(d, cx, cy, r, colour):
    # rising chart arrow
    pts = [(cx - r + 8, cy + 6), (cx - 6, cy - 8),
           (cx + 2, cy - 1), (cx + r - 8, cy - r + 9)]
    d.line(pts, fill=colour, width=5, joint="curve")
    d.polygon([(cx + r - 8, cy - r + 9), (cx + r - 8, cy - r + 22),
               (cx + r - 21, cy - r + 9)], fill=colour)
    d.line([(cx - r + 8, cy + r - 10), (cx + r - 8, cy + r - 10)],
           fill=colour, width=3)


def icon_flame(d, cx, cy, r, colour):
    # flame
    d.polygon([(cx, cy - r + 4), (cx + 12, cy - 2), (cx + 9, cy + 12),
               (cx + 14, cy + 4), (cx + 6, cy + r - 8), (cx - 8, cy + r - 8),
               (cx - 13, cy + 2), (cx - 6, cy - 6)], fill=colour)


def icon_gamepad(d, cx, cy, r, colour):
    # gamepad body + d-pad + buttons
    d.rounded_rectangle([cx - r + 4, cy - 12, cx + r - 4, cy + 14],
                        radius=12, fill=colour)
    d.line([(cx - r + 14, cy + 1), (cx - r + 24, cy + 1)], fill=DARK, width=4)
    d.line([(cx - r + 19, cy - 4), (cx - r + 19, cy + 6)], fill=DARK, width=4)
    for bx, by in ((cx + 12, cy - 4), (cx + 20, cy + 4)):
        d.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=DARK)


def icon_warning(d, cx, cy, r, colour):
    # warning triangle with exclamation
    d.polygon([(cx, cy - r + 6), (cx + r - 6, cy + r - 8),
               (cx - r + 6, cy + r - 8)], fill=colour)
    d.rectangle([cx - 2, cy - r + 16, cx + 2, cy + 4], fill=DARK)
    d.ellipse([cx - 3, cy + 9, cx + 3, cy + 15], fill=DARK)


# --- panels ----------------------------------------------------------------
# (accent colour, icon fn, kicker, headline, sub-line)
PANELS = [
    ((231, 76, 92), icon_scales, "JUSTICE",
     "WORLD COURT RULES",
     "ICJ finds Myanmar guilty of genocide against the Rohingya — first such "
     "ruling against a state."),
    ((46, 204, 178), icon_summit, "DIPLOMACY",
     "SHENZHEN SUMMIT",
     "Trump, Xi and Putin meet for the first time and issue a four-point "
     "peace declaration."),
    ((46, 204, 113), icon_chart, "MARKETS",
     "ANTHROPIC'S RECORD IPO",
     "Anthropic prices its IPO at $83 a share — a $1.5 trillion "
     "valuation."),
    ((255, 159, 28), icon_flame, "MIDDLE EAST",
     "GULF ATTACKS WIDEN",
     "Iran launches fresh strikes against Kuwait and Bahrain, widening "
     "attacks near the Strait of Hormuz."),
    ((255, 92, 138), icon_gamepad, "GAMING",
     "GTA 6 GOES ON SALE",
     "Grand Theft Auto VI goes on sale worldwide after 13 years of "
     "waiting."),
    ((147, 112, 255), icon_warning, "SOUTH ASIA",
     "BANGLADESH IN TURMOIL",
     "Violence hits 28 districts; Muhammad Yunus's ancestral home is set "
     "on fire."),
]


def draw_panel(d, x, y, w, h, accent, icon_fn, kicker, headline, body):
    d.rounded_rectangle([x, y, x + w, y + h], radius=18, fill=PANEL,
                        outline=PANEL_EDGE, width=2)
    # accent bar
    d.rounded_rectangle([x + 20, y + 16, x + 64, y + 22], radius=3,
                        fill=accent)
    # icon circle
    cx, cy, r = x + 52, y + 58, 30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=accent)
    icon_fn(d, cx, cy, r, DARK)
    # kicker
    d.text((x + 96, y + 44), kicker, font=F_KICK, fill=accent)
    # headline (1-2 lines)
    text_w = w - 40
    head_lines = wrap(d, headline, F_HEAD, text_w)
    hy = y + 104
    for line in head_lines:
        d.text((x + 20, hy), line, font=F_HEAD, fill=WHITE)
        hy += 40
    # body (2 lines max under a 2-line headline, else 3)
    max_body = 2 if len(head_lines) == 2 else 3
    body_lines = wrap(d, body, F_BODY, text_w)[:max_body]
    by = hy + 6
    for line in body_lines:
        d.text((x + 20, by), line, font=F_BODY, fill=GREY)
        by += 27


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # header
    draw_centered(d, 34, "THURSDAY, 19 NOVEMBER 2026", F_TITLE, WHITE)
    sub = " ".join(list("THE WORLD IN ONE DAY".replace(" ", "   ")))
    sw = d.textlength(sub, font=F_SUB)
    sx = (W - sw) / 2
    rule_y = 118
    gap = 16
    left_end = max(24, sx - gap)
    right_start = min(W - 24, sx + sw + gap)
    d.line([(24, rule_y), (left_end, rule_y)], fill=GOLD, width=3)
    d.line([(right_start, rule_y), (W - 24, rule_y)], fill=GOLD, width=3)
    d.text((sx, 104), sub, font=F_SUB, fill=GOLD)

    # panels: 2 columns x 3 rows
    margin, gutter = 32, 20
    pw = (W - 2 * margin - gutter) // 2
    ph = 261
    top = 172
    for i, panel in enumerate(PANELS):
        col, row = i % 2, i // 2
        x = margin + col * (pw + gutter)
        y = top + row * (ph + 16)
        draw_panel(d, x, y, pw, ph, *panel)

    img.save(OUT, format="PNG")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
