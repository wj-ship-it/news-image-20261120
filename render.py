#!/usr/bin/env python3
"""Render the Friday 20 November 2026 front page as a 1024x1024 PNG.

Classic black-and-white broadsheet look: a big serif masthead, a bold
dateline, the Nvidia plunge as the dominant lead story, four stories
in two rows of two columns, the Senate energy bill as a closing strip,
and the date repeated in the footer. All drawing is done with PIL
shapes and text; nothing here is an AI-generated image.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "entry.png")

PAGE_W, PAGE_H = 1024, 1024
MARGIN = 44
COL_GAP = 24
CONTENT_W = PAGE_W - 2 * MARGIN

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

PAPER = (252, 250, 244)
INK = (12, 12, 12)
GREY = (74, 74, 74)
FAINT = (168, 162, 148)
RED = (178, 34, 34)
LEAD_BG = (243, 238, 226)


def load(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, font, width):
    """Greedy word wrap that never exceeds `width`."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def shrink_to_fit(draw, text, path, start_size, width, max_lines, min_size=12):
    """Lower the point size until the text wraps into at most max_lines."""
    size = start_size
    while size > min_size:
        font = load(path, size)
        lines = wrap_text(draw, text, font, width)
        if len(lines) <= max_lines:
            return font, lines
        size -= 2
    font = load(path, size)
    lines = wrap_text(draw, text, font, width)
    if len(lines) > max_lines:
        # Never cut a sentence off silently: mark the truncation.
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip() + " \u2026"
    return font, lines


def draw_lines(draw, lines, x, y, font, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, width=1, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# --- small pictograms, drawn from scratch with PIL primitives ---------

def pict_chart_down(draw, x, y, size, colour):
    """Falling line chart with an arrowhead."""
    draw.line([(x, y + size * 0.15), (x, y + size)], fill=colour, width=3)
    draw.line([(x, y + size), (x + size, y + size)], fill=colour, width=3)
    pts = [(x + size * 0.08, y + size * 0.30),
           (x + size * 0.38, y + size * 0.55),
           (x + size * 0.62, y + size * 0.45),
           (x + size * 0.92, y + size * 0.85)]
    draw.line(pts, fill=colour, width=5, joint="curve")
    tip = pts[-1]
    draw.polygon([(tip[0], tip[1] + 12), (tip[0] - 12, tip[1] - 2),
                  (tip[0] + 2, tip[1] - 12)], fill=colour)


def pict_burst(draw, x, y, size, colour):
    """Starburst: eight spokes from a centre dot."""
    cx, cy = x + size / 2, y + size / 2
    for i in range(8):
        import math
        ang = math.radians(i * 45)
        r0, r1 = size * 0.16, size * 0.5
        draw.line([(cx + r0 * math.cos(ang), cy + r0 * math.sin(ang)),
                   (cx + r1 * math.cos(ang), cy + r1 * math.sin(ang))],
                  fill=colour, width=5)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=colour)


def pict_rings(draw, x, y, size, colour):
    """Two interlinked rings."""
    r = size * 0.32
    draw.ellipse([x, y + size * 0.18, x + 2 * r, y + size * 0.18 + 2 * r],
                 outline=colour, width=5)
    draw.ellipse([x + size - 2 * r, y + size * 0.18,
                  x + size, y + size * 0.18 + 2 * r],
                 outline=colour, width=5)


def pict_thermo(draw, x, y, size, colour):
    """Thermometer: stem, bulb and three heat ticks."""
    draw.rectangle([x + size * 0.42, y + size * 0.05,
                    x + size * 0.58, y + size * 0.72], outline=colour, width=4)
    draw.ellipse([x + size * 0.28, y + size * 0.62,
                  x + size * 0.72, y + size * 0.98], fill=colour)
    for i, yy in enumerate((0.10, 0.28, 0.46)):
        draw.line([(x + size * 0.66, y + size * yy),
                   (x + size * 0.86, y + size * yy)], fill=colour, width=4)


def pict_spiral(draw, x, y, size, colour):
    """Cyclone swirl: two concentric arcs plus rain slashes."""
    draw.arc([x, y, x + size, y + size * 0.72], 200, 500, fill=colour, width=5)
    draw.arc([x + size * 0.22, y + size * 0.20,
              x + size * 0.78, y + size * 0.62], 20, 320, fill=colour, width=4)
    for i, xx in enumerate((0.12, 0.45, 0.78)):
        draw.line([(x + size * xx, y + size * 0.82),
                   (x + size * xx - 6, y + size * 0.98)], fill=colour, width=4)


def pict_dome(draw, x, y, size, colour):
    """Capitol dome: arc roof, drum, columns, base."""
    draw.arc([x + size * 0.18, y, x + size * 0.82, y + size * 0.55],
             180, 360, fill=colour, width=5)
    draw.line([(x + size * 0.5, y - 2), (x + size * 0.5, y + size * 0.12)],
              fill=colour, width=4)
    draw.rectangle([x + size * 0.22, y + size * 0.55,
                    x + size * 0.78, y + size * 0.66], fill=colour)
    for i in range(4):
        cx = x + size * (0.24 + i * 0.17)
        draw.rectangle([cx, y + size * 0.70, cx + 7, y + size * 0.92],
                       fill=colour)
    draw.rectangle([x + size * 0.14, y + size * 0.92,
                    x + size * 0.86, y + size], fill=colour)


PICTOGRAMS = {
    "chart": pict_chart_down,
    "burst": pict_burst,
    "rings": pict_rings,
    "thermo": pict_thermo,
    "spiral": pict_spiral,
    "dome": pict_dome,
}

LEAD = {
    "kicker": "MARKETS  \u2022  WALL STREET",
    "headline": "NVIDIA SINKS 14% AS SEC EXAMINES ITS ACCOUNTS",
    "body": ("SEC enforcement staff are reviewing Nvidia's accounting. "
             "Shares closed Friday at $125.53, down 14.01% on the day, "
             "with about $491 billion of market value wiped out \u2014 "
             "the worst week since 2008."),
    "stats": "$125.53   \u2022   \u221214.01%   \u2022   \u2212$491BN IN A DAY   \u2022   \u221223% THIS WEEK   \u2022   7TH STRAIGHT DOWN DAY",
    "picto": "chart",
}

MIDDLE = [
    {"kicker": "WAR  \u2022  KYIV",
     "headline": "KYIV HIT BY OVERNIGHT MISSILE AND DRONE ATTACK",
     "body": ("Russian missiles and drones struck overnight, killing eight "
              "people across Ukraine, six of them in Kyiv. The Austrian "
              "and Dutch embassies, St Volodymyr's Cathedral and a Dnipro "
              "bridge were damaged. France has asked the UN Security "
              "Council to meet."),
     "picto": "burst"},
    {"kicker": "DIPLOMACY  \u2022  BRUSSELS",
     "headline": "EU AND UK STRIKE LANDMARK THREE-PART AGREEMENT",
     "body": ("At the second EU-UK summit in Brussels, the two sides "
              "agreed deals on food trade, linking their carbon markets, "
              "and youth mobility, with up to 100,000 young people able "
              "to move in each direction."),
     "picto": "rings"},
    {"kicker": "CLIMATE  \u2022  ANTALYA",
     "headline": "COP31 DRAFT DROPS ALL FOSSIL-FUEL PHASE-OUT LANGUAGE",
     "body": ("A new draft text in Antalya deletes every reference to "
              "phasing out fossil fuels, while keeping a 35-by-35 "
              "electrification target and acknowledging that the world "
              "will overshoot 1.5\u00b0C."),
     "picto": "thermo"},
    {"kicker": "WEATHER  \u2022  ODISHA",
     "headline": "CYCLONE AKVAN MAKES LANDFALL; 372,000 EVACUATED",
     "body": ("Cyclone Akvan came ashore near Gopalpur in Odisha with "
              "winds of 70\u201380 km/h, gusting to 90. Some 372,000 people "
              "were moved to safety, and no major damage or casualties "
              "have been reported."),
     "picto": "spiral"},
]

CLOSER = {
    "kicker": "POLITICS  \u2022  WASHINGTON",
    "headline": "SENATE PASSES ENERGY PERMITTING BILL 62\u201333",
    "body": ("The bipartisan American Affordability and Jobs Act speeds up "
             "approvals for energy projects and requires data centres to "
             "pay their own power costs. It now goes to the House."),
    "picto": "dome",
}


def draw_story_block(draw, x, y, width, height, story, head_size,
                     body_size, picto_size):
    """One story inside a bordered box; returns the bottom y used."""
    draw.rectangle([x, y, x + width, y + height], fill=(255, 255, 255),
                   outline=FAINT, width=1)
    inner = x + 18
    text_w = width - 36 - picto_size - 14
    # kicker
    kfont = load(SANS_B, 15)
    draw.text((inner, y + 14), story["kicker"], font=kfont, fill=RED)
    # pictogram, top right
    PICTOGRAMS[story["picto"]](draw, x + width - 18 - picto_size, y + 14,
                               picto_size, INK)
    # headline, up to 2 lines
    hfont, hlines = shrink_to_fit(draw, story["headline"], SERIF_B,
                                  head_size, text_w, 2)
    hy = y + 38
    hy = draw_lines(draw, hlines, inner, hy, hfont, INK, head_size + 6)
    # body, up to 3 lines
    bfont, blines = shrink_to_fit(draw, story["body"], SERIF,
                                  body_size, width - 36, 3)
    by = hy + 6
    draw_lines(draw, blines, inner, by, bfont, GREY, body_size + 6)
    return y + height


def main():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    title_font = load(SERIF_B, 62)
    draw.text((PAGE_W // 2, 26), "The Morning Dispatch", font=title_font,
              fill=INK, anchor="ma")
    rule(draw, MARGIN, PAGE_W - MARGIN, 100, width=3)
    rule(draw, MARGIN, PAGE_W - MARGIN, 106, width=1)
    date_font = load(SANS_B, 27)
    draw.text((PAGE_W // 2, 116), "FRIDAY  20 NOVEMBER 2026",
              font=date_font, fill=RED, anchor="ma")
    rule(draw, MARGIN, PAGE_W - MARGIN, 152, width=3)
    rule(draw, MARGIN, PAGE_W - MARGIN, 156, width=1)

    # ---- lead story: dominant full-width panel -------------------------
    lx, ly = MARGIN, 172
    lw, lh = CONTENT_W, 236
    draw.rectangle([lx, ly, lx + lw, ly + lh], fill=LEAD_BG,
                   outline=INK, width=2)
    kfont = load(SANS_B, 16)
    draw.text((lx + 20, ly + 16), LEAD["kicker"], font=kfont, fill=RED)
    PICTOGRAMS["chart"](draw, lx + lw - 20 - 64, ly + 14, 64, RED)
    hfont, hlines = shrink_to_fit(draw, LEAD["headline"], SERIF_B, 42,
                                  lw - 40 - 84, 2)
    hy = ly + 42
    hy = draw_lines(draw, hlines, lx + 20, hy, hfont, INK, 48)
    bfont, blines = shrink_to_fit(draw, LEAD["body"], SERIF, 18,
                                  lw - 40, 2)
    by = hy + 8
    by = draw_lines(draw, blines, lx + 20, by, bfont, GREY, 23)
    # stat strip along the bottom of the lead panel
    sfont = load(SANS_B, 16)
    stat_y = ly + lh - 34
    rule(draw, lx + 20, lx + lw - 20, stat_y - 8, width=1, fill=FAINT)
    draw.text((lx + 20, stat_y), LEAD["stats"], font=sfont, fill=INK)

    # ---- middle stories: two rows of two columns ----------------------
    col_w = (CONTENT_W - COL_GAP) // 2
    row_h = 196
    top = 424
    for i, story in enumerate(MIDDLE):
        r, c = divmod(i, 2)
        x = MARGIN + c * (col_w + COL_GAP)
        y = top + r * (row_h + 14)
        draw_story_block(draw, x, y, col_w, row_h, story,
                         head_size=25, body_size=16, picto_size=52)

    # ---- closer: full-width strip --------------------------------------
    cx, cy = MARGIN, 844
    cw, ch = CONTENT_W, 104
    draw.rectangle([cx, cy, cx + cw, cy + ch], fill=(255, 255, 255),
                   outline=FAINT, width=1)
    draw.rectangle([cx, cy, cx + 6, cy + ch], fill=RED)
    kfont = load(SANS_B, 15)
    draw.text((cx + 22, cy + 12), CLOSER["kicker"], font=kfont, fill=RED)
    PICTOGRAMS["dome"](draw, cx + cw - 22 - 56, cy + 22, 56, INK)
    hfont, hlines = shrink_to_fit(draw, CLOSER["headline"], SERIF_B, 27,
                                  cw - 44 - 76, 1)
    draw_lines(draw, hlines, cx + 22, cy + 36, hfont, INK, 33)
    bfont, blines = shrink_to_fit(draw, CLOSER["body"], SERIF, 16,
                                  cw - 44, 1)
    draw_lines(draw, blines, cx + 22, cy + 72, bfont, GREY, 22)

    # ---- footer: date repeated -----------------------------------------
    rule(draw, MARGIN, PAGE_W - MARGIN, 968, width=3)
    ffont = load(SANS_B, 22)
    draw.text((PAGE_W // 2, 980),
              "20 NOVEMBER 2026  \u2022  THE MORNING DISPATCH",
              font=ffont, fill=INK, anchor="ma")

    img.save(OUT_PATH, format="PNG", optimize=True)
    print("wrote", OUT_PATH, os.path.getsize(OUT_PATH), "bytes")


if __name__ == "__main__":
    main()
