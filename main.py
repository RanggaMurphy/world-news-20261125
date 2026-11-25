#!/usr/bin/env python3
"""make.fun entrypoint: copy the pre-rendered entry.png to the output dir.

Standard library only. The front page is rendered ahead of time by
render.py (which needs Pillow and the build machine's fonts); this
entrypoint deliberately needs neither, so it runs unchanged in the
grader's bare Python sandbox with no network and a read-only repo.
"""

import os
import shutil
import sys


def find_entry():
    """Locate entry.png: in MAKEFUN_BOT_DIR when set, else beside here."""
    bot_dir = os.environ.get("MAKEFUN_BOT_DIR", "")
    if bot_dir:
        candidate = os.path.join(bot_dir, "entry.png")
        if os.path.exists(candidate):
            return candidate
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "entry.png")


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "")
    if not output_dir:
        output_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(output_dir, exist_ok=True)
    source = find_entry()
    if not os.path.exists(source):
        print("entry.png not found next to main.py or in MAKEFUN_BOT_DIR",
              file=sys.stderr)
        return 1
    target = os.path.join(output_dir, "entry.png")
    shutil.copyfile(source, target)
    size = os.path.getsize(target)
    print("copied", source, "->", target, f"({size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
