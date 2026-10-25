#!/usr/bin/env python3
"""verify_blocks.py CHAPTER.md [...] — check every ^n^ verse in the `### 中文 — 和合本 (CUV)` and
`### English — NASB` blocks against the local caches. Segment chapter comes from the bold sub-heading
`**…（CH:verses）**` / `**… (CH:verses)**`. `……` gaps are allowed between verses.
Exit 1 on any mismatch."""
import sys, re, os, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scr import cuv, nasb
def norm(s):
    s = unicodedata.normalize('NFKC', s)
    return re.sub(r'\s+', '', s).replace('　', '')
VERSE = re.compile(r'\^(\d+)\^')
def check(path):
    t = open(path, encoding='utf8').read()
    bad = n = 0
    for tag, loader, start, end in (('CUV', cuv, '### 中文 — 和合本 (CUV)', '### English'), ('NASB', nasb, '### English — NASB', '\n## ')):
        a = t.find(start)
        if a < 0: print(f'{path}: no {tag} block'); return 1
        b = t.find(end, a + len(start)); sec = t[a:b if b > 0 else None]
        cache = {}
        # split by bold headings carrying (CH:..)
        parts = re.split(r'\*\*[^*\n]*[（(](\d+):[^）)]*[）)]\*\*', sec)
        for i in range(1, len(parts), 2):
            ch = int(parts[i]); txt = parts[i + 1]
            ref = cache.setdefault(ch, loader(ch))
            pieces = VERSE.split(txt)
            for j in range(1, len(pieces), 2):
                v = int(pieces[j]); got = pieces[j + 1]
                got = re.split(r'\n\s*\n', got)[0]
                got = got.lstrip('> ').replace('\n>', '').replace('……', '')
                got = got.strip()
                n += 1
                if v not in ref: print(f'{path}: {tag} {ch}:{v} not in cache'); bad += 1; continue
                if norm(got) != norm(ref[v]):
                    print(f'{path}: {tag} {ch}:{v} MISMATCH\n   book : {got}\n   cache: {ref[v]}'); bad += 1
    print(f'{os.path.basename(path)}: {n} verses checked, {bad} bad')
    return 1 if bad else 0
sys.exit(max(check(p) for p in sys.argv[1:]))
