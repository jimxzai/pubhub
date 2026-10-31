#!/usr/bin/env python3
"""Check that every Hebrew phrase printed in a chapter file occurs in the downloaded
Sefaria text (hebrew/hos-N.json + hebrew/other/*.json).  Cantillation, meteg and maqaf are
ignored and combining marks are put in canonical order (NFD) before comparing, so a phrase
typed with the shin-dot and vowel in a different order still matches.

usage: python3 check_hebrew.py <file.md> [...]      prints NO for phrases not found
"""
import glob, json, os, re, sys, unicodedata
here = os.path.dirname(os.path.abspath(__file__))
S = lambda s: re.sub(r'<[^>]+>', '', s).replace('&nbsp;', ' ').replace('&thinsp;', ' ')
def norm(t):
    t = unicodedata.normalize('NFD', t.replace('־', ' ').replace('׀', ' '))
    t = re.sub(r'[֑-ֽ֯׀׃׆‍]', '', t)
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFD', t))
corpus = ''
for f in glob.glob(here + '/hebrew/hos-*.json') + glob.glob(here + '/hebrew/other/*.json'):
    for v in json.load(open(f)).get('he', []):
        corpus += S(v) + ' '
H = norm(corpus)
bad = 0
for path in sys.argv[1:]:
    text = open(path, encoding='utf8').read()
    for m in re.finditer(r'[ְ-ת][ְ-ת֑-ׇ ־]*[ְ-ת]', text):
        w = norm(m.group(0)).strip()
        if len(re.sub(r'[ְ-ׇ ]', '', w)) < 2: continue
        if not re.search('[\u05B0-\u05BC\u05C7]', w): continue   # bare consonant root names carry no vowel points
        if w not in H:
            # allow a phrase made of several corpus words listed one after another, joined by ' / ' etc.
            bad += 1
            print('NO ', os.path.basename(path), m.group(0))
print('hebrew phrases not found:', bad)
