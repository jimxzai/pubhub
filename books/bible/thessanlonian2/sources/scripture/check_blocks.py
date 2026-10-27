#!/usr/bin/env python3
"""Verify every chapter's ## 經文 blocks against the downloaded sources.

CUV lines must equal cuv.tsv (FHL inline 或譯 notes removed); NASB lines must
equal nasb1995.tsv. Reports per verse: OK / DIFF / MISSING / EXTRA.
usage: python3 sources/scripture/check_blocks.py [chapter.md ...]
"""
import glob, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.dirname(os.path.dirname(HERE))

def load(name):
    d = {}
    for line in open(os.path.join(HERE, name)):
        k, t = line.rstrip('\n').split('\t')
        d[k] = re.sub(r'（[^）]*或譯[^）]*）', '', t)
    return d

CUV, NASB = load('cuv.tsv'), load('nasb1995.tsv')

def block(text, head):
    m = re.search(rf'^### {re.escape(head)}.*?\n(.*?)(?=^### |^---|^## )', text, re.S | re.M)
    return m.group(1) if m else ''

def verses(blk):
    body = ' '.join(l[1:].strip() for l in blk.splitlines() if l.startswith('>'))
    parts = re.split(r'\^(\d+)\^', body)
    return {int(v): t.strip() for v, t in zip(parts[1::2], parts[2::2])}

bad = 0
files = sys.argv[1:] or sorted(glob.glob(os.path.join(BOOK, '0[1-9]-*.md')))
for f in files:
    text = open(f).read()
    ref = re.search(r'^帖撒羅尼迦後書 (\d+):(\d+)-(\d+)', text, re.M)
    c, a, b = map(int, ref.groups())
    want = {f'{c}:{v}' for v in range(a, b + 1)}
    for head, src in (('中文', CUV), ('English', NASB)):
        got = {f'{c}:{v}': t for v, t in verses(block(text, head)).items()}
        for k in sorted(want | set(got), key=lambda x: int(x.split(':')[1])):
            if k not in got:
                print(f'MISSING {os.path.basename(f)} {head} {k}'); bad += 1
            elif k not in want:
                print(f'EXTRA   {os.path.basename(f)} {head} {k}'); bad += 1
            elif got[k] != src[k]:
                print(f'DIFF    {os.path.basename(f)} {head} {k}\n   book: {got[k]}\n   src:  {src[k]}'); bad += 1
    print(f'{os.path.basename(f)}: {len(want)} verses checked')
print('clean' if not bad else f'{bad} problem(s)')
sys.exit(1 if bad else 0)
