#!/usr/bin/env python3
"""Widen markdown pipe-table separator rows past pandoc's --columns threshold.

Root cause (see .claude/skills/eat-bible/references/gotchas.md): pandoc decides
a pipe table's LaTeX column spec from the width of the *separator row*. A
separator row shorter than --columns (default 72) compiles to bare `l` columns,
which cannot wrap at all, so any long cell silently overflows the text block.
A separator row at or past the threshold compiles to p{} columns whose widths
are proportional to the dash counts — those wrap.

This rewrites only separator rows that are under the threshold, preserving any
alignment colons. Word Study tables (header contains 希臘文) get tuned widths
so the Greek and transliteration columns can hold a long unbreakable token;
every other table gets equal widths, which are safe because CJK wraps anywhere.
"""
import re, sys, pathlib

THRESHOLD = 72
TARGET = 84          # total dash budget, comfortably past the threshold
WORD_STUDY = {4: [22, 22, 14, 42], 5: [22, 22, 14, 10, 30]}

SEP = re.compile(r'^\|(?:\s*:?-{2,}:?\s*\|)+$')

def widths(ncol, word_study):
    if word_study and ncol in WORD_STUDY:
        return WORD_STUDY[ncol]
    base = max(6, TARGET // ncol)
    return [base] * ncol

def rewrite(path):
    lines = path.read_text(encoding="utf-8").split("\n")
    changed = 0
    for i, line in enumerate(lines):
        if not SEP.match(line.strip()) or len(line) >= THRESHOLD:
            continue
        cells = [c for c in line.strip().split("|")[1:-1]]
        header = lines[i-1] if i else ""
        w = widths(len(cells), "希臘文" in header)
        out = []
        for cell, n in zip(cells, w):
            c = cell.strip()
            left, right = c.startswith(":"), c.endswith(":")
            dashes = "-" * max(2, n - left - right)
            out.append((":" if left else "") + dashes + (":" if right else ""))
        lines[i] = "|" + "|".join(out) + "|"
        changed += 1
    if changed:
        path.write_text("\n".join(lines), encoding="utf-8")
    return changed

total = 0
for arg in sys.argv[1:]:
    p = pathlib.Path(arg)
    n = rewrite(p)
    total += n
    if n:
        print(f"  {p.name}: {n} separator row(s) widened")
print(f"total: {total}")
