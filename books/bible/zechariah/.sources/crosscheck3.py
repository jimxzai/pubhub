#!/usr/bin/env python3
"""Three-way: ai-eden CUV / fhl unv / cnbible.com 和合本 (traditional, first column + spaced original column)."""
import json, re, os
D = os.path.dirname(os.path.abspath(__file__))
norm = lambda s: re.sub(r'[^一-鿿]', '', s.replace('裡', '裏'))
def cn(c):
    h = open(f'{D}/cnbible/{c}.htm', encoding='utf-8', errors='replace').read()
    t = re.findall(r'btext3">(.*?)</span>', h)
    assert len(t) % 2 == 0, (c, len(t))
    return {i + 1: t[2 * i] for i in range(len(t) // 2)}   # traditional original-CUV column (odd entries are simplified)
rows = []
for c in range(1, 15):
    ai = {v['verse']: v['textZh'] for v in json.load(open(f'{D}/aieden-zechariah-{c}.json'))['data']['verses']}
    fh = {r['sec']: r['bible_text'] for r in json.load(open(f'{D}/fhl-unv-{c}.json'))['record']}
    cc = cn(c)
    for v in sorted(ai):
        a, f, k = norm(ai[v]), norm(fh[v]), norm(cc.get(v, ''))
        if not k: rows.append((c, v, 'cnbible MISSING')); continue
        if a != f or a != k or f != k:
            w = 'ai=cn' if a == k else 'fhl=cn' if f == k else 'all differ'
            rows.append((c, v, w))
for r in rows: print(*r)
print(len(rows), 'rows')
