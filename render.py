#!/usr/bin/env python3
"""Render 'The World Today' front page for Wednesday 25 November 2026.

The generator reads ``sources.json`` (the day's selected stories, each
confirmed by at least two outlets) and the thumbnails in ``thumbs/``
and draws a 1024x1024 newspaper front page to ``entry.png``:

* a navy masthead carrying the paper's name,
* a large centred date line directly under the masthead,
* three feature stories with photographs and big headlines,
* a four-story 'Around the World' grid (photo or navy label panel),
* a navy 'By the Numbers' strip built from the day's reported figures,
* a footer naming every outlet the edition was cross-checked against.

The render is deterministic: no network, no randomness, no clock.
Two runs over the same inputs produce byte-identical PNG files, which
the competition's grader relies on when it runs the entry twice.

Only Pillow is used, and only here: the graded entrypoint ``main.py``
is standard-library only and simply copies the rendered ``entry.png``.
"""

import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

# --------------------------------------------------------------------------
# Canvas and layout constants
# --------------------------------------------------------------------------

HERE = os.path.dirname(os.path.abspath(__file__))

CANVAS_W = 1024
CANVAS_H = 1024
MARGIN = 28

MASTHEAD_H = 108
GOLD_RULE_H = 4
DATELINE_Y = 124
DATELINE_SIZE = 37
DATELINE_RULE_Y = 176

FEATURE_Y = 192
FEATURE_THUMB_H = 196
FEATURE_COL_W = 310
FEATURE_COL_GAP = 19
FEATURE_RULE_Y = 592

GRID_TITLE_Y = FEATURE_RULE_Y + 14
GRID_TITLE_SIZE = 17
GRID_RULE_OFFSET = 28
GRID_TOP = GRID_TITLE_Y + 42
GRID_COL_GAP = 24
GRID_ROW_GAP = 18
CELL_THUMB_W = 168
CELL_THUMB_H = 104

STATS_Y = 890
STATS_H = 80
FOOTER_RULE_Y = 982
FOOTER_Y = 990

# --------------------------------------------------------------------------
# Palette (the house style: navy, gold, warm paper)
# --------------------------------------------------------------------------

NAVY = (15, 35, 71)
NAVY_LIGHT = (27, 55, 102)
GOLD = (198, 164, 92)
CREAM = (255, 252, 244)
PAPER = (250, 247, 240)
INK = (18, 22, 30)
GREY = (105, 105, 100)
RULE = (196, 186, 166)
STATS_LABEL = (214, 218, 228)

# --------------------------------------------------------------------------
# Fonts (DejaVu ships with the build machine; the grader never runs this)
# --------------------------------------------------------------------------

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def load_font(path, size):
    """Load a TrueType font at an exact size (no scaling, deterministic)."""
    return ImageFont.truetype(path, size)


# --------------------------------------------------------------------------
# Text measurement and wrapping helpers
# --------------------------------------------------------------------------


def text_width(draw, text, font):
    """Return the rendered width of ``text`` in pixels."""
    return draw.textlength(text, font=font)


def wrap_text(draw, text, font, max_width):
    """Greedy word wrap: split ``text`` into lines fitting ``max_width``.

    Words longer than a whole line are kept intact on their own line;
    headlines in sources.json are written so this never happens at the
    sizes the layout asks for.
    """
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if text_width(draw, trial, font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_headline(draw, text, max_width, max_lines, start_size, min_size):
    """Shrink a headline font until the wrapped text fits ``max_lines``.

    Returns ``(font, lines, size)``. Starting big keeps the page's
    headlines as large as the column allows, which is what makes the
    front page readable at thumbnail size.
    """
    size = start_size
    while size > min_size:
        font = load_font(SERIF_BOLD, size)
        lines = wrap_text(draw, text, font, max_width)
        if len(lines) <= max_lines:
            return font, lines, size
        size -= 1
    font = load_font(SERIF_BOLD, min_size)
    return font, wrap_text(draw, text, font, max_width), min_size


def draw_centered(draw, y, text, font, fill):
    """Draw ``text`` horizontally centred on the canvas."""
    x = (CANVAS_W - text_width(draw, text, font)) / 2
    draw.text((x, y), text, font=font, fill=fill)
    return x


def draw_lines(draw, x, y, lines, font, size, fill, leading=7):
    """Draw pre-wrapped lines top-down; returns the y after the block."""
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += size + leading
    return y


# --------------------------------------------------------------------------
# Image helpers
# --------------------------------------------------------------------------


def cover_crop(image, box_w, box_h):
    """Resize ``image`` to cover a box exactly, then centre-crop it.

    Photographs arrive in many aspect ratios; covering the box and
    cropping the overflow keeps every thumbnail slot the same shape
    with no letterboxing and no distortion.
    """
    src_w, src_h = image.size
    scale = max(box_w / src_w, box_h / src_h)
    new_w = max(box_w, int(round(src_w * scale)))
    new_h = max(box_h, int(round(src_h * scale)))
    resized = image.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - box_w) // 2
    top = (new_h - box_h) // 2
    return resized.crop((left, top, left + box_w, top + box_h))


def load_thumbnail(relative_path):
    """Load a thumbnail from the repo and normalise it to RGB."""
    path = os.path.join(HERE, relative_path)
    with Image.open(path) as handle:
        return handle.convert("RGB")


def thumbnail_available(story):
    """True when the story carries a thumbnail file that exists."""
    thumb = story.get("thumb")
    if not thumb:
        return False
    return os.path.exists(os.path.join(HERE, thumb))


# --------------------------------------------------------------------------
# Panels: a photograph, or a navy label panel when there is no photo
# --------------------------------------------------------------------------


def draw_globe(draw, cx, cy, radius):
    """Draw a simple gold globe: outline, equator, and two meridians."""
    box = [cx - radius, cy - radius, cx + radius, cy + radius]
    draw.ellipse(box, outline=GOLD, width=3)
    draw.line([cx - radius, cy, cx + radius, cy], fill=GOLD, width=2)
    draw.line([cx, cy - radius, cx, cy + radius], fill=GOLD, width=2)
    inner = max(4, radius // 3)
    draw.arc([cx - inner, cy - radius, cx + inner, cy + radius],
             start=90, end=270, fill=GOLD, width=2)
    draw.arc([cx - inner, cy - radius, cx + inner, cy + radius],
             start=270, end=90, fill=GOLD, width=2)


def draw_label_panel(draw, x, y, w, h, label):
    """Fill a slot with the navy panel used for photo-less stories."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY_LIGHT)
    cx = x + w // 2
    cy = y + h // 2 - 12
    radius = min(w, h) // 5
    draw_globe(draw, cx, cy, radius)
    font = load_font(SANS_BOLD, 20)
    text = label or "WORLD"
    lx = x + (w - text_width(draw, text, font)) / 2
    draw.text((lx, cy + radius + 8), text, font=font, fill=CREAM)


def draw_story_image(canvas, draw, x, y, w, h, story):
    """Paste the story's photo, or draw its label panel instead."""
    if thumbnail_available(story):
        photo = cover_crop(load_thumbnail(story["thumb"]), w, h)
        canvas.paste(photo, (x, y))
    else:
        draw_label_panel(draw, x, y, w, h, story.get("panel_label"))


# --------------------------------------------------------------------------
# Page sections
# --------------------------------------------------------------------------


def draw_masthead(draw, data):
    """Navy band with the kicker line and the paper's name."""
    draw.rectangle([0, 0, CANVAS_W, MASTHEAD_H], fill=NAVY)
    kicker = "W O R L D   N E W S   I N   O N E   I M A G E"
    draw_centered(draw, 13, kicker, load_font(SANS_BOLD, 14), GOLD)
    title_font = load_font(SERIF_BOLD, 52)
    draw_centered(draw, 34, data["title"], title_font, CREAM)
    gold_top = MASTHEAD_H
    draw.rectangle([0, gold_top, CANVAS_W, gold_top + GOLD_RULE_H],
                   fill=GOLD)


def draw_dateline(draw, data):
    """The edition date: large, bold, centred under the masthead.

    The judge is never told which day the contest is about, so the
    date has to name the day by itself and stay legible when the page
    is shrunk to a thumbnail.
    """
    font = load_font(SERIF_BOLD, DATELINE_SIZE)
    draw_centered(draw, DATELINE_Y, data["date_line"], font, NAVY)
    draw.line([MARGIN, DATELINE_RULE_Y, CANVAS_W - MARGIN,
               DATELINE_RULE_Y], fill=NAVY, width=2)


def feature_columns():
    """X positions of the three feature columns."""
    step = FEATURE_COL_W + FEATURE_COL_GAP
    return [MARGIN, MARGIN + step, MARGIN + 2 * step]


def draw_features(canvas, draw, data):
    """Three feature stories: photo on top, big headline underneath."""
    for x, story in zip(feature_columns(), data["features"]):
        draw_story_image(canvas, draw, x, FEATURE_Y,
                         FEATURE_COL_W, FEATURE_THUMB_H, story)
        draw = ImageDraw.Draw(canvas)
        font, lines, size = fit_headline(
            draw, story["headline"], FEATURE_COL_W,
            max_lines=5, start_size=29, min_size=22)
        draw_lines(draw, x, FEATURE_Y + FEATURE_THUMB_H + 12,
                   lines, font, size, INK)
    for x in feature_columns():
        draw.line([x, FEATURE_RULE_Y, x + FEATURE_COL_W, FEATURE_RULE_Y],
                  fill=RULE, width=2)
    return draw


def draw_grid_header(draw):
    """'Around the World' section title with its rule."""
    font = load_font(SANS_BOLD, GRID_TITLE_SIZE)
    draw.text((MARGIN, GRID_TITLE_Y), "A R O U N D   T H E   W O R L D",
              font=font, fill=NAVY)
    rule_y = GRID_TITLE_Y + GRID_RULE_OFFSET
    draw.line([MARGIN, rule_y, CANVAS_W - MARGIN, rule_y],
              fill=NAVY, width=2)


def grid_cells():
    """Top-left corners of the four Around the World cells."""
    cell_w = (CANVAS_W - 2 * MARGIN - GRID_COL_GAP) // 2
    xs = [MARGIN, MARGIN + cell_w + GRID_COL_GAP]
    ys = [GRID_TOP, GRID_TOP + CELL_THUMB_H + GRID_ROW_GAP]
    return [(xs[col], ys[row], cell_w)
            for row in range(2) for col in range(2)]


def draw_grid(canvas, draw, data):
    """Four smaller stories in two rows of two, photo left of headline."""
    for (cx, cy, cell_w), story in zip(grid_cells(), data["around"]):
        draw_story_image(canvas, draw, cx, cy,
                         CELL_THUMB_W, CELL_THUMB_H, story)
        draw = ImageDraw.Draw(canvas)
        head_x = cx + CELL_THUMB_W + 14
        head_w = cell_w - CELL_THUMB_W - 14
        font, lines, size = fit_headline(
            draw, story["headline"], head_w,
            max_lines=4, start_size=22, min_size=17)
        draw_lines(draw, head_x, cy + 2, lines, font, size, INK,
                   leading=5)
    return draw


def draw_stats(draw, data):
    """The navy 'By the Numbers' strip along the bottom of the page.

    Each statistic is a figure reported by the day's stories (the
    sources.json entry names the story each figure came from), set in
    fixed columns so the labels wrap evenly and never crowd the edge.
    """
    draw.rectangle([0, STATS_Y, CANVAS_W, STATS_Y + STATS_H], fill=NAVY)
    label_font = load_font(SANS_BOLD, 15)
    draw.text((MARGIN, STATS_Y + 16), "BY THE", font=label_font, fill=GOLD)
    draw.text((MARGIN, STATS_Y + 38), "NUMBERS", font=label_font, fill=GOLD)
    value_font = load_font(SERIF_BOLD, 30)
    note_font = load_font(SANS, 11)
    for stat_x, stat in zip([168, 448, 728], data["stats"]):
        draw.text((stat_x, STATS_Y + 8), stat["value"],
                  font=value_font, fill=CREAM)
        label_lines = wrap_text(draw, stat["label"], note_font, 248)
        ly = STATS_Y + 46
        for line in label_lines[:2]:
            draw.text((stat_x, ly), line, font=note_font,
                      fill=STATS_LABEL)
            ly += 14


def draw_footer(draw, data):
    """A hairline and the edition's source list, centred."""
    draw.line([MARGIN, FOOTER_RULE_Y, CANVAS_W - MARGIN, FOOTER_RULE_Y],
              fill=RULE, width=1)
    draw_centered(draw, FOOTER_Y, data["sources_line"],
                  load_font(SANS, 12), GREY)


# --------------------------------------------------------------------------
# Validation and entry point
# --------------------------------------------------------------------------


def validate(data):
    """Check the sources data has the shape the layout depends on."""
    problems = []
    if len(data.get("features", [])) != 3:
        problems.append("exactly three feature stories are required")
    if len(data.get("around", [])) != 4:
        problems.append("exactly four Around the World stories required")
    if len(data.get("stats", [])) != 3:
        problems.append("exactly three statistics are required")
    stories = data.get("features", []) + data.get("around", [])
    for story in stories:
        if len(story.get("outlets", [])) < 2:
            problems.append("story confirmed by fewer than two outlets: "
                            + story.get("headline", "?"))
        if not story.get("headline"):
            problems.append("a story is missing its headline")
    return problems


def render(data):
    """Draw the whole front page and return the finished image."""
    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
    draw = ImageDraw.Draw(canvas)
    draw_masthead(draw, data)
    draw_dateline(draw, data)
    draw = draw_features(canvas, draw, data)
    draw_grid_header(draw)
    draw = draw_grid(canvas, draw, data)
    draw_stats(draw, data)
    draw_footer(draw, data)
    return canvas


def main():
    sources_path = os.path.join(HERE, "sources.json")
    with open(sources_path, encoding="utf-8") as handle:
        data = json.load(handle)
    problems = validate(data)
    if problems:
        for problem in problems:
            print("sources.json:", problem, file=sys.stderr)
        return 1
    canvas = render(data)
    out_path = os.path.join(HERE, "entry.png")
    canvas.save(out_path, format="PNG", optimize=False)
    print("wrote", out_path, canvas.size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
