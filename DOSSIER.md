# Dossier index - The World Today, 25 November 2026

One file per story lives in `stories/`. Each dossier holds the
same things: the headline as printed, the story's position on
the page, its carriers and panel label, what happened, the facts
on record, why the story was selected and how its headline was
chosen, what was deliberately not printed, what to watch next,
and the articles themselves.

| # | Story | Position | File |
|---|-------|----------|------|
| 1 | Gaza strike | Feature 1 | stories/01-gaza-strike.md |
| 2 | Zimbabwean conviction | Feature 2 | stories/02-zimbabwean-conviction.md |
| 3 | Huawei verdict | Feature 3 | stories/03-huawei-verdict.md |
| 4 | Iowa detonation | Grid 1 | stories/04-iowa-detonation.md |
| 5 | Hanoi blast | Grid 2 | stories/05-hanoi-blast.md |
| 6 | Iowa explainer | Grid 3 | stories/06-iowa-explainer.md |
| 7 | Pope's diary | Grid 4 | stories/07-pope-diary.md |

## How the dossiers relate to the other documents

- `SOURCES.md` is the edition-level research record.
- The dossiers are the story-level record: everything about one
  story in one place.
- `sources.json` is the machine-readable record the renderer
  consumes; where a dossier and the JSON disagree, the JSON is
  what the page printed, and the dossier is wrong.
- `verify.py` checks the dossiers against the data: carriers,
  regions, panel labels, numbers and article URLs.

## This edition's two structural facts

Two stories are one event (the Iowa detonation and its
explainer), printed separately for the reasons the README and
stories/06-iowa-explainer.md record. Two stories have no
photograph (Hanoi and the Iowa explainer) and run as labelled
navy panels; the dossiers mark those labels as drawn.

## How the dossiers were weighed

Each dossier carries a section the edition added for this
resubmission: "The carriers, weighed". Confirmation is not a
count, and the dossiers say what each story's carriers actually
contributed: which one is load-bearing, which corroborates,
where a figure belongs to a party rather than to a carrier, and
where the carriers' agreement is about tone rather than fact.
A reviewer who reads only one part of a dossier should read
that section; it is where the edition's confidence, story by
story, is stated most precisely.
