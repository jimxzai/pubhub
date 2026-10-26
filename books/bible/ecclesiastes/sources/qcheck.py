#!/usr/bin/env python3
"""Check candidate quotes against the local corpora before writing them into a chapter.

usage: python3 qcheck.py <corpus: henry|bridges|morgan|gregory|gty|all> "quote one" "quote two" ...
Uses the same normalisation as scripts/verify-citations.py (case, quotes, dashes and
punctuation folded away; words must match exactly).  Prints OK, or the longest matching
prefix so a drifted quote can be fixed against the real wording.
"""
import re, sys, unicodedata, os
HERE = os.path.dirname(os.path.abspath(__file__))
def norm(text):
    text = unicodedata.normalize("NFKC", text)
    for a, b in [("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("—", " "), ("–", " "), ("…", "...")]:
        text = text.replace(a, b)
    text = re.sub(r'["\']', "", text)
    text = re.sub(r"[^\w\s.]", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()
src = open(f'{HERE}/commentary/corpus-{sys.argv[1]}.txt', encoding='utf-8').read()
hay = norm(src)
for q in sys.argv[2:]:
    n = norm(q)
    if n in hay:
        print('OK   ', q[:90])
        continue
    lo, hi = 0, len(n)
    while lo < hi:                       # longest matching prefix
        mid = (lo + hi + 1) // 2
        if n[:mid] in hay: lo = mid
        else: hi = mid - 1
    i = hay.find(n[:lo]) if lo else -1
    print('DRIFT' if lo > 25 else 'MISS ', q[:90], '| matched', lo, 'of', len(n))
    if i >= 0: print('       source continues:', hay[i + lo:i + lo + 120])
