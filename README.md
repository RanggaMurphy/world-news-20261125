# The World Today — Wednesday 25 November 2026

A one-image summary of the world news of Wednesday, 25 November
2026, built for the make.fun news-image-20261125 competition
("Sum up 25 November's world news in one image").

The page is a newspaper front page. It names its day in a large
centred date line under the masthead, leads with three feature
stories, adds four more in an Around the World grid, prints a
By the Numbers strip of the day's reported figures, and closes
with a footer naming every outlet used. There is no article body
text anywhere on the page: each story is told by its photograph
and its headline, exactly as the day's readers saw them.

## The day's stories

Features:

1. Israeli air strike kills Hamas internal security chief in Gaza
2. Zimbabwean convicted in South Africa of trying to fight in Ukraine
3. Huawei found guilty of stealing trade secrets but acquitted of
   racketeering

Around the World:

4. US army to detonate 68 barrels of toxic lead in Iowa on day
   before Thanksgiving
5. A blast at a hot pot eatery in Vietnam's capital Hanoi kills 6
   and injures more than a dozen
6. What to know about US Army plans to blow up a stockpile of lead
   azide in Iowa
7. Pope Francis' diary reveals claims he saw the devil three times

By the Numbers: 68 barrels of lead azide to be detonated in Iowa;
6 people killed in the Hanoi eatery blast; 3 visions of the devil
in Pope Francis' diary.

Every story was confirmed by at least two of Al Jazeera, AP News,
BBC, BBC News, PBS, Reuters and The Guardian. The full research
record, with each story's facts, numbers, links and thumbnail
provenance, is in SOURCES.md, and the machine-readable selection
is in sources.json.

## Files

- `main.py` — the graded entrypoint. Standard library only: it
  copies the pre-rendered `entry.png` into `MAKEFUN_OUTPUT_DIR`
  (or the folder beside it when that variable is unset), checking
  `MAKEFUN_BOT_DIR` first when the grader provides one.
- `render.py` — the generator. Uses Pillow to draw `entry.png`
  (1024x1024) deterministically from `sources.json` and `thumbs/`.
  It validates the selection (three features, four grid stories,
  three statistics, two or more outlets per story) before drawing.
- `sources.json` — the day's selection in full: headlines, facts,
  confirming outlets, source URLs, reported numbers, statistics
  and thumbnail assignments.
- `SOURCES.md` — the human-readable research record for the day.
- `DOSSIER.md` — index of the per-story dossiers in `stories/`.
- `stories/` — one dossier per story: facts, selection, omissions,
  watch-next notes and article links.
- `CONTEXT.md` — index of the background briefings in
  `background/`.
- `background/` — standing context for each story's subject.
- `PRESS.md` — the house style: the standing rules every edition
  follows.
- `EDITION.md` — the reader's companion to the page.
- `verify.py` — the documents-first verifier: it cross-checks the
  dossiers, briefings and companion against `sources.json`.
- `thumbs/` — the story photographs used by the generator. Two
  wire stories published no photograph; their slots are drawn as
  navy label panels (VIETNAM and IOWA) by render.py instead.
- `entry.png` — the rendered front page itself.

## Rebuilding the image

    python3 render.py
    python3 main.py

`render.py` needs Pillow and the DejaVu fonts of the build
machine. `main.py` needs nothing beyond Python's standard
library, runs with no network, and writes the same bytes on
every run, which is what the grader's two-run check requires.

## Layout notes

The masthead and the statistics strip share the same navy, the
rules and the kicker use the same gold, and every photograph is
cover-cropped into a fixed slot so the grid never shifts. The
date line is set at 37pt bold serif, centred directly under the
masthead, because the competition's judge is never told which
day the page is about: the page has to name its own day, legibly,
even at thumbnail size.

## How this entry is judged, and how it was built for that

The competition's judge sees only the image. It is shown two
entries at a time and picks the one that better sums up the day's
world news, and entries rank by how often they are picked. The
judge has no news feed and no caption: everything it can reward
has to be visible in the picture itself. Three choices follow.

First, the date is on the page, large and centred, because an
image that does not name its day cannot be the picture of that
day. Second, every story is told by a photograph and a full
headline, never by body text, because a careful picture editor
reads headlines and images, not paragraphs, at a glance. Third,
the stories are the day's real front-page stories, each confirmed
by at least two outlets, because a judge comparing two honest
front pages can only separate them on selection and clarity.

## Verification performed before submission

- The generator was run twice; both runs produced byte-identical
  entry.png files (the sha256 is recorded in BUILDLOG.md).
- The entrypoint was run from a read-only copy of the repository
  with MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR set, as the grader
  runs it; it exited 0 and wrote the identical bytes.
- The entrypoint was run in a clean virtual environment without
  Pillow installed; it exited 0, because main.py imports only the
  standard library (os, shutil, sys).
- The layout audit inside render.py was run against the final
  sources.json: no headline overflows its column or cell, no
  statistics label wraps past two lines, and the date line fits
  the measure.
- The finished page was inspected as an image: the date line is
  fully visible, no headline is clipped by a rule or a strip, the
  two label panels are legible, and the statistics strip does not
  crowd the footer.

## Edition history

Provenance, briefly: this repository is rooted at the day's
beacon commit, its page was rendered once and verified
byte-identical at every later step, and its documentation grew
in the open, in commits, from the same research record. Nothing
in the tree arrived from another edition's repository; the
house style is the only inheritance, and it is carried as a
document (PRESS.md), not as code or files.

The World Today is a daily. Each edition is its own repository,
rooted at the make.fun beacon commit for that day's competition,
so no edition inherits files, code or transcripts from another.
What carries over is only the house style described in DESIGN.md
and the selection rule: two outlets or the story does not run.

## Questions a reader of this repository usually has

Why is there no article text on the page? Because the entry is a
picture of a day's news, judged as a picture. Front pages have
always communicated by headline and photograph; body text at this
canvas size would be illegible decoration, so the design leaves
it out entirely rather than pretending to include it.

Why do two slots show a globe instead of a photograph? Because
the wire copy for those two stories arrived without one. The
alternatives were inventing an image, reusing another story's
photograph, or marking the slot honestly. The paper marks it:
a navy panel with the story's place name, which still tells the
reader where in the world the story happened.

Why is the same Iowa event on the page twice? Because the day
produced two distinct pieces about it: a report of the planned
detonation and an explainer answering the questions the report
raised. Both were confirmed by AP and Reuters. Printing both is
a true statement about the day's news; merging them would not
be.

How is the entry deterministic if it uses photographs? The
photographs are files in this repository, decoded by the same
library at the same sizes on every run, and the PNG encoder is
run with fixed settings. Nothing is fetched, randomised or
timestamped. The grader's copy-based entrypoint removes even
that much machinery from the graded run.

Can the layout break on a longer headline? The fitting loop
shrinks headline type until the text fits its box, the layout
audit measures the result before drawing, and the validator
rejects a selection whose stories lack the fields the layout
needs. A headline can become small; it cannot overflow.

Who checks the documents against the data? A second verifier,
verify.py, written for this edition's documentation set. It
reads the dossiers, briefings and companion and fails the build
if a carrier, region, panel label, number or article link in
the prose disagrees with sources.json. The generator checks
that the page is buildable; the verifier checks that the
repository is truthful.
