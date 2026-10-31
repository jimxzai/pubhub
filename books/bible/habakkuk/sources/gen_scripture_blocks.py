#!/usr/bin/env python3
"""Generate the 經文 blocks (CUV + NASB 1995) for each Habakkuk unit -> scripture/NN.md
CUV  : ai-eden.com 和合本（本書底本；與 fhl 的差異見 README），裡→裏 per project policy.
NASB : biblehub 1995 (supplied words in *italics*), identical to ai-eden NASB ignoring punctuation/italics.
Verse markers use 和合本/NASB numbering; a unit crossing a chapter uses ^c:v^."""
import json, re, os
D = os.path.dirname(os.path.abspath(__file__))
UNITS = {
    '01': [(1, 1, 4)], '02': [(1, 5, 11)], '03': [(1, 12, 17), (2, 1, 1)], '04': [(2, 2, 5)],
    '05': [(2, 6, 20)], '06': [(3, 1, 15)], '07': [(3, 16, 19)],
}
def load(c):
    ai = {v['verse']: v['textZh'] for v in json.load(open(f'{D}/scripture/aieden-hab-{c}.json'))['data']['verses']}
    bh = {int(l.split('\t')[0]): l.split('\t')[1] for l in open(f'{D}/scripture/nasb1995-hab-{c}.txt').read().strip().split('\n')}
    return ai, bh
def cuv(t): return t.replace('裡', '裏').replace('　', '')
def nasb(t):
    t = t.replace('Selah.', 'Selah.')
    return re.sub(r'\*\s+\*', ' ', t)
data = {c: load(c) for c in (1, 2, 3)}
os.makedirs(f'{D}/scripture/units', exist_ok=True)
for u, spans in UNITS.items():
    zh, en = [], []
    multi = len({c for c, _, _ in spans}) > 1
    for c, a, b in spans:
        ai, bh = data[c]
        for v in range(a, b + 1):
            mk = f'^{c}:{v}^' if multi else f'^{v}^'
            zh.append(mk + cuv(ai[v])); en.append(mk + nasb(bh[v]))
    open(f'{D}/scripture/units/{u}.md', 'w').write(
        '### 中文 — 和合本 (CUV)\n\n> ' + ''.join(zh) + '\n\n### English — NASB 1995\n\n> ' + ' '.join(en) + '\n')
    print(u, 'ok')
