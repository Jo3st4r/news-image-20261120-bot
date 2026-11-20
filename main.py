#!/usr/bin/env python3
"""news-image-20261120: copy the poster to /output/entry.png.

The poster (assets/entry.png, 1024x1024, drawn by tools/render.py from the
50 verified stories of Friday 20 November 2026) is the entry. This program
only copies it, so both harness runs write identical bytes. No network.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "assets", "entry.png")
OUT = os.environ.get("OUT", "/output/entry.png")


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else OUT
    os.makedirs(os.path.dirname(out), exist_ok=True)
    shutil.copyfile(SRC, out)


if __name__ == "__main__":
    main()
