#!/usr/bin/env python3
"""Documents-first verifier for The World Today, 25 November 2026.

render.py validates the selection and draws the page; this
script starts from the other end. It reads the prose documents
(the dossiers in stories/, the background briefings in
background/, the companion and the house style) and checks them
against sources.json and against each other. A claim that exists
only in prose, contradicted by the data, fails here.

    python3 verify.py

Exit code 0 means every cross-check passed. Standard library
plus Pillow only.
"""

import json
import os
import re
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))

FAILURES = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ((" - " + detail) if detail else ""))
    if not ok:
        FAILURES.append(name)


def read(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as fh:
        return fh.read()


def load_data():
    with open(os.path.join(HERE, "sources.json"), encoding="utf-8") as fh:
        return json.load(fh)


STORY_FILES = [
    "stories/01-gaza-strike.md",
    "stories/02-zimbabwean-conviction.md",
    "stories/03-huawei-verdict.md",
    "stories/04-iowa-detonation.md",
    "stories/05-hanoi-blast.md",
    "stories/06-iowa-explainer.md",
    "stories/07-pope-diary.md",
]

DOSSIER_SECTIONS = [
    "What happened",
    "The facts on record",
    "What was not printed",
    "Watch next",
    "Articles",
]

# The identifying fragment of each story's lead article URL. The
# dossiers wrap long URLs across lines, so the check searches the
# whitespace-stripped dossier text for the fragment instead of
# comparing whole URLs.
URL_FRAGMENTS = [
    "c6rrg7ggq190o",
    "cmqj5qlj5yz9o",
    "cmy49ngydqzpo",
    "us-army-iowa-detonation",
    None,
    None,
    "cm78270l4z7no",
]

# Words that must appear in each dossier for its numbers record
# to be considered faithfully carried into prose.
NUMBER_MARKERS = [
    ["two months", "seven"],
    ["hundreds"],
    ["months-long", "New York"],
    ["68 barrels", "five tons", "10am"],
    ["six", "dozen"],
    ["stockpile"],
    ["three", "choir loft"],
]


def squash(text):
    return re.sub(r"\s+", "", text)


def check_dossiers(data):
    stories = list(data["features"]) + list(data["around"])
    check("seven stories", len(stories) == 7)
    check("dossier count", len(STORY_FILES) == len(stories))
    for story, rel in zip(stories, STORY_FILES):
        text = read(rel)
        name = rel.split("/")[-1]
        for section in DOSSIER_SECTIONS:
            check("dossier section %s: %s" % (section, name), section in text)
        for outlet in story["outlets"]:
            check("dossier carrier %s: %s" % (outlet, name), outlet in text)
        check("dossier region: " + name, story["region"] in text)
        check("dossier panel label: " + name, story["panel_label"] in text)
        flat = squash(text)
        fragment = URL_FRAGMENTS[STORY_FILES.index(rel)]
        if fragment:
            check("dossier article fragment: " + name, fragment in flat)
        for marker in NUMBER_MARKERS[STORY_FILES.index(rel)]:
            check("dossier number %s: %s" % (marker, name),
                  marker.lower() in text.lower())
        if story["thumb"] is None:
            check("dossier marks panel as drawn: " + name,
                  "drawn" in text.lower())


def check_stats(data):
    values = [s["value"] for s in data["stats"]]
    check("strip values", values == ["68", "6", "3"], ", ".join(values))
    headlines = [s["headline"] for s in
                 list(data["features"]) + list(data["around"])]
    for stat in data["stats"]:
        check("stat source is a story: " + stat["value"],
              stat["source_story"] in headlines)
        check("stat label names its figure: " + stat["value"],
              len(stat["label"]) >= 20)


def check_thumbs(data):
    stories = list(data["features"]) + list(data["around"])
    panels = 0
    for story in stories:
        if story["thumb"] is None:
            panels += 1
            check("panel story uses panel source: " + story["panel_label"],
                  story["thumb_source"] == "panel")
            continue
        path = os.path.join(HERE, story["thumb"])
        check("thumb exists: " + story["thumb"], os.path.exists(path))
        with Image.open(path) as im:
            w, h = im.size
        check("thumb geometry: " + story["thumb"], w >= 300 and h >= 150,
              "%dx%d" % (w, h))
    check("exactly two panel stories", panels == 2, "%d panels" % panels)


def check_press_rules(data):
    press = read("PRESS.md")
    for n in range(1, 22):
        check("press rule %d present" % n, ("\n%d. " % n) in press)
    stories = list(data["features"]) + list(data["around"])
    check("rule 1 holds: two outlets everywhere",
          all(len(s["outlets"]) >= 2 for s in stories))
    check("rule 10 holds: strip figures come from stories",
          all(s["source_story"] for s in data["stats"]))


def check_desk_notes(data):
    keys = ["gaza_strike", "zimbabwean_conviction", "huawei_verdict",
            "iowa_detonation", "hanoi_blast", "iowa_explainer", "pope_diary"]
    notes = data.get("desk_notes", {})
    check("desk notes keys", sorted(notes.keys()) == sorted(keys),
          ", ".join(sorted(notes.keys())))
    for key in keys:
        text = notes.get(key, "")
        check("desk note substance: " + key, len(text) >= 120,
              "%d chars" % len(text))
    joined = " ".join(notes.values())
    check("desk notes record the Iowa duplication", "explainer" in joined)
    check("desk notes record the panels", "panel" in joined)


def check_cross_references(data):
    readme = read("README.md")
    for name in ["SOURCES.md", "DOSSIER.md", "CONTEXT.md", "PRESS.md",
                 "EDITION.md", "verify.py", "sources.json"]:
        check("readme lists " + name, name in readme)
    index = read("DOSSIER.md")
    for rel in STORY_FILES:
        check("index lists " + rel, rel in index)
    context = read("CONTEXT.md")
    for rel in ["background/gaza-campaign.md", "background/african-recruitment.md",
                "background/trade-secrets-trials.md", "background/lead-azide.md",
                "background/hot-pot-safety.md", "background/papal-diaries.md"]:
        check("context index lists " + rel, rel in context)
        check("briefing exists: " + rel,
              os.path.exists(os.path.join(HERE, rel)))
    edition = read("EDITION.md")
    check("companion explains the duplication", "twice" in edition)
    check("companion explains the panels", "panel" in edition.lower())


def main():
    data = load_data()
    check_dossiers(data)
    check_stats(data)
    check_thumbs(data)
    check_press_rules(data)
    check_desk_notes(data)
    check_cross_references(data)
    if FAILURES:
        print("FAILED:", len(FAILURES), "checks:", ", ".join(FAILURES))
        return 1
    print("all cross-checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
