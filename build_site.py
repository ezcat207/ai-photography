#!/usr/bin/env python3
"""Build the static reading site into site/ from repo sources.

Usage: python3 build_site.py   (run from repo root)
- site/index.html        <- site-src/index.html
- site/introduction.md   <- introduction.md
- site/chapters/*.md     <- chapters/*.md  (image refs normalized to site-root-relative)
- site/images/*          <- images/*
"""
import os
import re
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "site-src")
OUT = os.path.join(ROOT, "docs")


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "chapters"))
    os.makedirs(os.path.join(OUT, "images"))

    shutil.copy(os.path.join(SRC, "index.html"), os.path.join(OUT, "index.html"))
    shutil.copy(os.path.join(ROOT, "introduction.md"), os.path.join(OUT, "introduction.md"))

    for fn in sorted(os.listdir(os.path.join(ROOT, "chapters"))):
        if not fn.endswith(".md") or fn == "image-prompts.md":
            continue
        src = os.path.join(ROOT, "chapters", fn)
        s = open(src, encoding="utf-8").read()
        s = s.replace("../images/", "images/")  # site-root-relative
        open(os.path.join(OUT, "chapters", fn), "w", encoding="utf-8").write(s)
        print("  md", fn)

    for fn in sorted(os.listdir(os.path.join(ROOT, "images"))):
        shutil.copy(os.path.join(ROOT, "images", fn), os.path.join(OUT, "images", fn))
        print("  img", fn)

    print("site built:", OUT)


if __name__ == "__main__":
    main()
