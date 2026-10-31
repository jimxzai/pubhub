#!/usr/bin/env python3
"""Emit the 經文 blocks of a chapter straight from the verified source files.

usage: scripture_block.py CH FROM-TO [GROUPS]   e.g.  scripture_block.py 1 1-8 "1;2-4;5-8"
Groups are ';'-separated verse ranges, one blockquote paragraph each.
"""
import sys, re
from pathlib import Path
here = Path(__file__).resolve().parent / "scripture"
def load(name):
    d = {}
    for l in (here / name).read_text(encoding="utf-8").splitlines():
        k, t = l.split("\t", 1); d[k] = t
    return d
cuv, nasb = load("cuv-nahum.txt"), load("nasb1995-nahum.txt")
ch = sys.argv[1]; a, b = map(int, sys.argv[2].split("-"))
groups = sys.argv[3].split(";") if len(sys.argv) > 3 else [f"{a}-{b}"]
def block(src, sep=""):
    out = []
    for g in groups:
        x, y = (g.split("-") + [g])[:2] if "-" in g else (g, g)
        x, y = int(x), int(y)
        out.append("> " + sep.join(f"^{n}^{src[f'{ch}:{n}']}" for n in range(x, y + 1)))
    return "\n>\n".join(out)
print("### 中文 — 和合本 (CUV)\n\n" + block(cuv) + "\n\n### English — NASB 1995\n\n" + block(nasb, " "))
