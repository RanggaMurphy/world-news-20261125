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
