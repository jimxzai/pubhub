#!/usr/bin/env python3
"""Cross-check ai-eden CUV (textZh) vs fhl unv, ignoring punctuation; prints differences."""
import json, re, os, difflib
D = os.path.dirname(os.path.abspath(__file__))
norm = lambda s: re.sub(r'[^一-鿿]', '', s.replace('裡', '裏'))
n = diff = 0
for c in range(1, 15):
    ai = {v['verse']: v['textZh'] for v in json.load(open(f'{D}/aieden-zechariah-{c}.json'))['data']['verses']}
    fh = {r['sec']: r['bible_text'] for r in json.load(open(f'{D}/fhl-unv-{c}.json'))['record']}
    assert set(ai) == set(fh), (c, set(ai) ^ set(fh))
    for v in sorted(ai):
        n += 1
        a, f = norm(ai[v]), norm(fh[v])
        if a != f:
            diff += 1
            sm = difflib.SequenceMatcher(None, a, f)
            ops = [(t, a[i1:i2], f[j1:j2]) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != 'equal']
            print(f'{c}:{v}\tai-eden vs fhl: ' + '；'.join(f'{x[1]!r}→{x[2]!r}' for x in ops))
print('verses', n, 'differing', diff)
