#!/usr/bin/env python3
"""Check every `> "English quote"` block in the given markdown files against ALL commentary source files.
Normalises case, quotes, dashes, punctuation, whitespace and OCR hyphenation. Prints OK / MISS per quote.
usage: check_frontmatter_quotes.py FILE.md [...]"""
import re, sys, glob, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../commentary/'
def norm(s):
    s = s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    s = re.sub(r'-\s*\n\s*', '', s)
    s = re.sub(r'[^a-z0-9]+', ' ', s.lower())
    return ' '.join(s.split())
corpus = ''
for f in glob.glob(D + '*.txt'):
    corpus += ' ' + norm(open(f, encoding='utf-8', errors='ignore').read())
bad = 0
for p in sys.argv[1:]:
    t = open(p, encoding='utf-8').read()
    for m in re.finditer(r'^> "(.+?)"?\s*\n> —', t, re.S | re.M):
        q = m.group(1)
        parts = [x for x in re.split(r'\s*(?:…|\.\.\.)\s*', q) if x.strip()]
        ok = all(norm(x) in corpus for x in parts)
        print(('OK   ' if ok else 'MISS ') + os.path.basename(p) + ': ' + q[:70].replace('\n', ' '))
        bad += (not ok)
sys.exit(1 if bad else 0)
