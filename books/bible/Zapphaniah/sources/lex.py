#!/usr/bin/env python3
"""lex.py <strong-number> [...]  — BDB short definition from openscriptures/HebrewLexicon
LexicalIndex.xml (hebrew/LexicalIndex.xml). Short glosses only; full BDB entries
are not located by this script. Strong numbers = the OSHB lemma numbers printed by
count_hebrew.py (a trailing letter, e.g. 859a, is dropped)."""
import re, sys
from pathlib import Path
x = (Path(__file__).resolve().parent / "hebrew" / "LexicalIndex.xml").read_text(encoding="utf-8")
for e in re.findall(r"<entry id=.*?</entry>", x, re.S):
    m = re.search(r'strong="(\d+)"', e)
    if not m or m.group(1) not in sys.argv[1:]:
        continue
    w = re.search(r"<w [^>]*>(.*?)</w>", e).group(1)
    pos = (re.search(r"<pos>(.*?)</pos>", e) or [None, ""])[1]
    d = (re.search(r"<def>(.*?)</def>", e) or [None, ""])[1]
    print(f"H{m.group(1):<5} {w}\t{pos}\t{d}")
