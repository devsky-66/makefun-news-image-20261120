#!/usr/bin/env python3
"""Copy the bundled entry image to the output directory.

The entry image is entry.png next to this file. This program only copies
bytes: it takes no input, uses no network, and writes the same bytes on
every run.
"""
import os
import shutil
import sys
from pathlib import Path


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    src = Path(__file__).resolve().parent / "entry.png"
    dst = Path(out_dir) / "entry.png"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
