# Design specification — The World Today front page

This document specifies the page that render.py draws, precisely
enough that the layout could be rebuilt from the description
alone. It is the design record for the 25 November 2026 edition;
the constants named here are the constants in render.py, and the
layout audit in render.py checks the rendered text against the
spaces this document assigns to it.

## Canvas

- The page is 1024 by 1024 pixels, the largest the competition
  accepts, because the judge compares entries as pictures and a
  bigger canvas keeps headlines legible when the page is shrunk.
- The side margin is 28 pixels on both sides, leaving a 968-pixel
  text measure. Every rule, column and strip aligns to it.
- The background is a warm paper tone (RGB 250, 247, 240), close
  to newsprint, so photographs sit on the page instead of floating
  over a screen-white void.

## Palette

- Navy (15, 35, 71) is the paper's colour: masthead, statistics
  strip, section titles and the date line all use it, so the eye
  reads the furniture as one system.
- A lighter navy (27, 55, 102) fills the label panels that stand
  in for missing photographs, close enough to belong to the same
  system, different enough not to be mistaken for the masthead.
- Gold (198, 164, 92) is used sparingly: the kicker line, the
  rule under the masthead, the globes on the label panels and the
  words BY THE NUMBERS. It never carries body information.
- Ink (18, 22, 30) is the headline colour, softer than pure black
  against the paper tone.
- Hairlines between sections use a warm rule grey (196, 186, 166),
  and the statistics labels use a pale blue-grey (214, 218, 228)
  that stays readable on navy at small sizes.

## Masthead

- The masthead is a full-width navy band 108 pixels tall.
- A gold rule 4 pixels tall sits directly beneath it.
- Inside the band, the kicker WORLD NEWS IN ONE IMAGE is set in
  14-point bold sans, letter-spaced by hand with spaces between
  words, centred, in gold, 13 pixels from the top.
- The name The World Today is set in 52-point bold serif, centred,
  in cream (255, 252, 244), 34 pixels from the top. The size is
  chosen so the name spans most of the measure without touching
  the margins: at 52 points it measures roughly 590 pixels wide.

## Date line

- The date line is the most important line on the page after the
  headlines, because the judge is never told which day the page
  summarises. It is set in 37-point bold serif, in navy, centred,
  124 pixels from the top, directly under the masthead.
- A 2-pixel navy rule at y 176 closes the header block. The rule
  is heavier than the section hairlines because it separates the
  paper's identity from the day's news.

## Feature stories

- Three columns, each 310 pixels wide, separated by 19-pixel
  gutters, starting at the left margin. The three columns and two
  gutters sum exactly to the 968-pixel measure.
- Each column opens with a photograph 310 by 196 pixels, cover
  cropped from the story's thumbnail: the image is scaled to cover
  the slot and centre-cropped, never letterboxed or distorted.
- The headline begins 12 pixels under the photograph. It is set in
  bold serif, starting at 29 points and shrinking one point at a
  time until the wrapped text fits five lines or the size reaches
  the 22-point floor. The fitting loop is what guarantees that a
  five-line headline and a two-line headline both look deliberate.
- A warm hairline at y 592 closes the feature block under all
  three columns, aligned even when the headlines differ in length.

## Around the World grid

- The section title is set in 17-point bold sans, letter-spaced,
  in navy, at y 606, with a 2-pixel navy rule 28 pixels below the
  title's baseline start.
- The grid starts at y 648. Two columns split the measure with a
  24-pixel gutter; each cell is 472 pixels wide.
- Each cell pairs a 168 by 104 pixel image slot on the left with
  the headline on the right. The headline starts 14 pixels right
  of the image and is fitted like the features: bold serif from
  22 points down to a 17-point floor, at most four lines.
- Rows are separated by 18 pixels. The second row ends at y 874,
  sixteen pixels above the statistics strip.
- When a story has no photograph, its slot is a navy label panel:
  a gold globe (an outline circle with an equator, a meridian line
  and two meridian arcs) above the story's place label in 20-point
  bold sans capitals. The panel says where the story happened, so
  even a photo-less wire story contributes information.

## By the Numbers strip

- The strip is a full-width navy band from y 890, 80 pixels tall.
- The words BY THE NUMBERS are set in 15-point bold sans in gold,
  stacked on two lines at the left margin.
- Three statistics stand in fixed columns starting at x 168, 448
  and 728. Fixed columns, rather than flowing text, keep the
  strip even when the labels differ in length.
- Each statistic is a value in 30-point bold serif cream, with its
  label beneath in 11-point sans, wrapped to at most two lines of
  248 pixels. The audit in render.py fails the build's checks if
  a label ever needs a third line.

## Footer

- A 1-pixel hairline at y 982 separates the page from its credits.
- The source line is set in 12-point sans grey, centred, at y 990:
  the outlets whose reporting the edition was cross-checked
  against, in one line, separated by hyphens.

## Typography

- Serif bold (DejaVu Serif Bold) carries the paper's name, the
  date and every headline: the voices that speak.
- Sans bold (DejaVu Sans Bold) carries the kicker, the section
  title, the panel labels and the strip's name: the furniture.
- Sans regular carries only the statistics labels and the footer,
  the two places where small quiet text is needed.
- No other faces or weights appear anywhere on the page.

## Determinism

- The generator uses no network, no randomness and no clock. Font
  files are loaded at exact sizes, photographs are decoded from
  files in the repository, and the PNG is written with fixed
  encoder settings, so two runs produce byte-identical output.
- The entrypoint the grader runs (main.py) does not render at
  all: it copies the committed entry.png, which is why the graded
  run cannot drift from the page this document describes.

## Coordinate table

Every element's position, as drawn. X grows right, Y grows down,
and all values are pixels from the top-left corner of the canvas.

- Masthead band: x 0 to 1024, y 0 to 108, navy fill.
- Kicker text: baseline row starts y 13, centred, 14pt sans bold.
- Paper name: starts y 34, centred, 52pt serif bold.
- Gold rule: y 108 to 112, full width.
- Date line: starts y 124, centred, 37pt serif bold.
- Header rule: y 176, from x 28 to x 996, 2px navy.
- Feature photographs: y 192 to 388, three slots of 310x196 at
  x 28, x 357 and x 686.
- Feature headlines: start y 400, inside their column's 310px.
- Feature rule: y 592, one 310px segment under each column.
- Grid title: starts y 606, x 28, 17pt sans bold.
- Grid title rule: y 634, from x 28 to x 996, 2px navy.
- Grid row 1: y 648 to 752. Grid row 2: y 770 to 874.
- Grid cells: left column x 28 to 500, right column x 524 to 996.
- Grid image slots: 168x104 at each cell's left edge.
- Grid headlines: start 14px right of each image slot, up to
  290px wide, fitted between 22pt and 17pt serif bold.
- Statistics strip: y 890 to 970, full width, navy fill.
- Strip title: x 28, lines at y 906 and y 928, 15pt sans bold.
- Statistic 1: value at x 168, y 898, 30pt serif bold; label
  beneath from y 936, up to two 11pt lines, 248px wide.
- Statistic 2: value at x 448, same rows as statistic 1.
- Statistic 3: value at x 728, same rows as statistic 1.
- Footer rule: y 982, from x 28 to x 996, 1px warm grey.
- Source line: starts y 990, centred, 12pt sans regular.

## Why the page is dense at the top and calm at the bottom

The features carry the day's weight, so they get the largest
photographs and the largest headlines, and they sit immediately
under the date where a reader's eye lands first. The grid is
deliberately quieter: smaller images, smaller headlines, more air
between rows. The statistics strip then changes the register
entirely, from pictures to numbers, which rests the eye before
the footer. A page that shouted at one volume throughout would
make its own headlines harder to rank, and ranking the day is
the page's whole job.

## What would change for a different kind of day

The layout is fixed, but the fitting rules absorb variety: a day
of short headlines simply sets them at the maximum size, and a
day of long ones shrinks them toward the floor. The two places
the design can genuinely strain are a feature story whose
headline still needs five lines at the floor size (the audit
warns, and the editors shorten the headline in sources.json
rather than moving the furniture) and a statistics label with a
long place name (the audit warns at three lines, and the label
is rewritten). Both failures are editorial, not structural, and
both are caught before the page is drawn.

## The fitting loop, worked through on a real headline

The Huawei feature headline is the longest of this edition:
"Huawei found guilty of stealing trade secrets but acquitted of
racketeering", eleven words, seventy-three characters. In its
310-pixel column the fitting loop tries sizes from the top:

- At 29 points the words wrap to five lines: "Huawei found" /
  "guilty of stealing" / "trade secrets but" / "acquitted of" /
  "racketeering". Five lines is the feature maximum, so 29
  points is accepted and the headline prints at full size.
- The block then occupies five times (29 + 7) pixels of leading,
  180 pixels from its start at y 400, ending at y 580, twelve
  pixels above the feature rule at y 592. That gap is the
  tightest on the page, and it is why the rule sits at 592 and
  not at the 578 of the first render, where the same headline's
  last line touched it.

The Gaza headline shows the opposite case: at 29 points it wraps
to four lines ("Israeli air strike" / "kills Hamas" / "internal
security" / "chief in Gaza"), ending at y 544 and leaving a
longer run of paper beneath it. The columns are not balanced
against each other; each headline simply gets the largest size
that fits, and the shared rule at the bottom is what unifies
them. Balancing the columns by shrinking the shorter headlines
to match the longest block was considered and rejected: it would
make two headlines smaller for the sake of a symmetry no reader
asked for.
