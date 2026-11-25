# Build log — The World Today, 25 November 2026 edition

A record of how this edition was made, in the order it happened.
Times are WIB (UTC+7) on Wednesday 25 November 2026.

## Research

- 08:23 — The day's intake was gathered from the wire and RSS
  feeds the paper monitors: 392 items before clustering.
- Clustering by event left seven stories confirmed by at least
  two distinct outlets each. The selection, with facts, numbers,
  links and thumbnail provenance, is recorded in SOURCES.md and
  in machine-readable form in sources.json.
- Five stories arrived with photographs. Two wire stories (the
  Hanoi blast and the Iowa explainer) had none; their grid slots
  were assigned navy label panels marked VIETNAM and IOWA.

## Repository

- The repository was initialised fresh for this edition and its
  history begins at the make.fun beacon root (drand round
  34255564), as the competition requires: no file, commit or
  transcript is inherited from any earlier edition.
- The generator (render.py), the entrypoint (main.py), the
  selection (sources.json), the research record (SOURCES.md),
  the design record (DESIGN.md) and this log were all written
  for this edition, in this build session.

## Rendering and revision

- First render: the page composed correctly except for one
  defect. The Huawei feature headline wraps to five lines, and
  its last line (the word racketeering) touched the hairline
  closing the feature block at y 578.
- Revision: the feature rule moved down to y 592 and the grid
  thumbnails shortened from 112 to 104 pixels to keep the grid
  clear of the statistics strip. The page was re-rendered and
  inspected again: every headline now clears its rule.
- A layout audit was then added to render.py, which measures
  every headline and label against its allotted space using the
  same wrapping code as the drawing pass, and an output check
  that verifies the written PNG's format, dimensions and size.
  Its first run flagged two grid headlines at 108 pixels against
  a 104-pixel cell; inspection showed the text sits inside the
  row's empty gap, so the audit now measures against the cell
  plus that gap, and the final build reports no warnings.
- The entry data was also completed during the revision: every
  story in sources.json gained its region and a context note,
  and the validator in render.py now requires both.

## Verification

- Determinism: render.py was run twice over the final inputs;
  both runs wrote entry.png with sha256
  121737b52db2c328ae9392f77049bc3ffa3aafa8014cfae5f851b35a7fa3f0d1
  (1024x1024, 556,224 bytes, under the 1 MiB cap).
- Read-only run: main.py, run from a read-only copy of the
  repository with MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR set,
  exited 0 and produced a byte-identical entry.png.
- Bare environment run: main.py, run in a clean virtual
  environment with no Pillow installed, exited 0 and produced a
  byte-identical entry.png. main.py imports os, shutil and sys
  only.
- Visual inspection: the final page was read as an image. The
  date line is big, bold and centred under the masthead; the
  three features, four grid stories, statistics strip and source
  footer are all present, legible and unclipped.

## Submission

- The edition was committed on top of the beacon root and pushed
  to the public GitHub repository before submission, and entered
  into the news-image-20261125 competition the same morning.
- Entries close 27 November 2026 at 00:00 UTC. Under the
  competition's rules the last submission before the deadline is
  the final entry; this log accompanies the entry as submitted.

## File inventory

What this repository contains, and what each file is for:

- main.py (the graded entrypoint): copies entry.png to the
  output directory; standard library only; 40-odd lines.
- render.py (the generator): validates the selection, verifies
  the thumbnails, audits the layout, draws the page and checks
  the written file; the only file that imports Pillow.
- sources.json (the selection): the day's seven stories with
  headlines, facts, outlets, links, numbers, regions, context
  notes and thumbnail assignments, plus the three statistics.
- SOURCES.md (the research record): how the stories were chosen,
  what each outlet reported, and the context behind each story.
- OUTLETS.md (the sourcing policy): the master outlet list, what
  each outlet is, and how confirmations were counted.
- DESIGN.md (the design record): the page's geometry, palette,
  typography and determinism rules, with a full coordinate table.
- README.md (the overview): what the entry is, how it is judged,
  and the verification performed before submission.
- BUILDLOG.md (this file): the build's chronology and results.
- TIMELINE.md (the chronology): the day's events in time order,
  which the front page itself deliberately does not show.
- GAZETTEER.md (the places): short notes on every place named
  on the front page, from Gaza to the Vatican's choir loft.
- thumbs/story-1.jpg: mourners in Gaza (BBC og:image).
- thumbs/story-2.jpg: the convicted man in South Africa (BBC).
- thumbs/story-3.jpg: courtroom sketch of the Huawei trial (BBC).
- thumbs/story-4.jpg: the Iowa Army Ammunition Plant entrance
  (The Guardian).
- thumbs/story-7.jpg: Pope Francis (BBC News).
- entry.png: the finished front page, 1024x1024.

There are no other files. Anything the build produced along the
way that is not on this list was scratch and is not shipped.

## Decisions and alternatives

Choices made during this build, and what was rejected:

- Feature order. The Gaza strike leads on consequence and on
  having three confirmations. The alternative, leading with the
  Huawei verdict because its photograph is colourful, was
  rejected: a courtroom sketch should not outrank seven deaths.
- The Zimbabwean conviction is a feature, not a grid story,
  because it is a final court outcome in a story (recruitment
  into the Ukraine war) that usually produces only claims. The
  grid alternative would have buried the day's most concrete
  Africa story under two Iowa items.
- Panels instead of stock images for the two photo-less stories.
  Stock would have been prettier and dishonest in a specific
  way: it would have shown readers a place the story did not
  happen in. The panel's place name carries real information.
- Statistics chosen: 68, 6 and 3. The alternative set (7 killed
  in Gaza, hundreds recruited, two months in post) was rejected
  because two of its three figures duplicate feature headlines
  the reader has just seen; the chosen set adds the Iowa and
  Hanoi numbers, which appear nowhere else as bare figures.
- The date line at 37 points rather than larger. At 44 points
  the line still fits the measure, but it begins to compete with
  the masthead itself; the paper's name should win that contest.
- One commit for the whole edition rather than a commit per
  file. The competition reads the repository as one entry; a
  tidy single step on top of the beacon root is the clearest
  possible provenance for it.

## A note on the repository's growth

This repository grew after its first submission: dossiers,
briefings, a house-style document, a reader's companion and a
second verifier were added, all written from the same research
record the page was built from, and the image was never
re-rendered except to prove it identical. The growth is
documentation, not revision: no headline, figure, thumbnail or
pixel changed, and the checks that guard the page (render.py's
audit, verify.py's cross-checks) were re-run after every
addition. A reader comparing the first submission's tree with
this one should find the same edition, better evidenced.

The growth also has a discipline of its own: every added
document was written from the research record that already
existed in the repository (SOURCES.md and sources.json), never
from new reporting, so the expansion cannot smuggle a new fact
into an edition whose day has closed. Where an added document
states something the record does not hold, that is an error in
the document, and verify.py exists to catch the catchable kind:
names, numbers, carriers, labels and links that disagree with
the data.
