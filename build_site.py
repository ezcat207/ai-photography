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

    for root, _, fns in os.walk(os.path.join(ROOT, "chapters")):
        for fn in sorted(fns):
            if not fn.endswith(".md") or fn == "image-prompts.md":
                continue
            src = os.path.join(root, fn)
            rel = os.path.relpath(src, os.path.join(ROOT, "chapters"))
            dst = os.path.join(OUT, "chapters", rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            s = open(src, encoding="utf-8").read()
            s = s.replace("../images/", "images/")  # site-root-relative
            open(dst, "w", encoding="utf-8").write(s)
            print("  md", rel)

    for fn in sorted(os.listdir(os.path.join(ROOT, "images"))):
        shutil.copy(os.path.join(ROOT, "images", fn), os.path.join(OUT, "images", fn))
        print("  img", fn)

    # disable Jekyll so raw .md files are served (the reader fetches them)
    open(os.path.join(OUT, ".nojekyll"), "w").write("")

    print("site built:", OUT)


if __name__ == "__main__":
    main()
