#!/usr/bin/env python3
"""List every Hebrew word in each chapter's 原文研讀 table next to the BDB short gloss of the lemma(s) it matches in WLC.
For human review: does the book's 意義 column contradict the BDB short gloss?  python3 check_wordstudy.py [chapter files…]"""
import re, sys, glob, collections, unicodedata
from pathlib import Path
D = Path(__file__).resolve().parent
def cons(s):
    s = unicodedata.normalize('NFD', s)
    return ''.join(c for c in s if 'א' <= c <= 'ת')
gloss = collections.defaultdict(list)
for l in open(D / 'lexicon/bdb-short.tsv', encoding='utf-8'):
    if l.startswith('#'): continue
    k, n, w, p, d = l.rstrip('\n').split('\t')
    gloss[k].append(f'{d}')
surf = collections.defaultdict(set)
xml = open(D / 'hebrew/wlc-hab.xml', encoding='utf-8').read()
for lem, w in re.findall(r'<w lemma="([^"]*)"[^>]*>(.*?)</w>', xml):
    segs = w.split('/'); lems = lem.split('/')
    for i, s in enumerate(segs):
        k = re.sub(r'[a-z]$', '', lems[min(i, len(lems) - 1)].strip()).strip()
        if k.isdigit(): surf[cons(s)].add(k)
files = sys.argv[1:] or sorted(glob.glob(str(D.parent / '0[1-7]-*.md')))
for f in files:
    t = open(f, encoding='utf-8').read()
    m = re.search(r'## 原文研讀 \(Word Study\)\n(.*?)\n## ', t, re.S)
    if not m: print(f, 'NO WORD STUDY'); continue
    print('==', Path(f).name)
    for row in m.group(1).split('\n'):
        if not row.startswith('|') or '---' in row: continue
        cells = [c.strip() for c in row.strip('|').split('|')]
        if len(cells) < 3 or not re.search('[א-ת]', cells[0]): continue
        out = []
        for w in re.findall(r'[֑-״]+', cells[0]):
            ks = surf.get(cons(w), set())
            out.append(f"{cons(w)}→" + '/'.join(sorted({g for k in ks for g in gloss.get(k, [])})) if ks else f"{cons(w)}→?")
        print(f"  {cells[0][:22]:<22} | {cells[2][:60]} || BDB: {'; '.join(out)[:110]}")
