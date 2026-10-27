#!/usr/bin/env python3
"""q.py <source-glob> <regex> [width]  — print matching sentences with file name, for picking verbatim quotes."""
import glob, re, sys
pat = re.compile(sys.argv[2], re.I)
for f in sorted(glob.glob(sys.argv[1])):
    t = open(f, encoding='utf-8', errors='replace').read()
    t = re.sub(r'\s+', ' ', t)
    sents = re.split(r'(?<=[.!?”"])\s+(?=[A-Z“"])', t)
    for s in sents:
        if pat.search(s):
            print(f'[{f}] {s}\n')
