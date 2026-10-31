#!/usr/bin/env python3
"""Generate the 經文 blocks (CUV + NASB 1995) for each Jonah unit.
CUV  : fhl 和合本 (unv), cross-checked vs ai-eden CUV (identical ignoring punctuation); 裡→裏 per project policy.
NASB : biblehub 1995 text; supplied (italic) words taken from ai-eden's [bracketed] words.
Verse markers use English (和合本/NASB) numbering; units crossing a chapter use ^c:v^.
"""
import json, re, os
D = os.path.dirname(os.path.abspath(__file__))
UNITS = {  # file prefix: [(chapter, v_from, v_to), ...]
    '01': [(1, 1, 3)], '02': [(1, 4, 10)], '03': [(1, 11, 16)],
    '04': [(1, 17, 17), (2, 1, 10)],
    '05': [(3, 1, 4)], '06': [(3, 5, 10)], '07': [(4, 1, 4)], '08': [(4, 5, 11)],
}
QUOTE = set('\'"‘’“”')
def load(c):
    ai = {v['verse']: v for v in json.load(open(f'{D}/aieden-jonah-{c}.json'))['data']['verses']}
    fh = {r['sec']: r['bible_text'] for r in json.load(open(f'{D}/fhl-unv-{c}.json'))['record']}
    bh = open(f'{D}/bh-nasb-{c}.txt').read().split('\n')
    bh = {i + 1: re.sub(r'\s+', ' ', re.sub(r'NASB 1995 Copyright.*$', '', b)).strip() for i, b in enumerate(bh)}
    return ai, fh, bh
def nasb(ai_t, bh_t):
    ai_t = re.sub(r'\s+', ' ', ai_t.replace('-- ', '—').replace('--', '—')).strip()
    out, j = [], 0
    for ch in ai_t:
        if ch in '[]':
            out.append('\x01' if ch == '[' else '\x02'); continue
        if ch in QUOTE:
            if j < len(bh_t) and bh_t[j] in QUOTE:
                out.append(bh_t[j]); j += 1
            continue
        # advance over whitespace/quote mismatches in bh
        while j < len(bh_t) and bh_t[j] in QUOTE and ch not in QUOTE:
            out.append(bh_t[j]); j += 1
        if j < len(bh_t) and bh_t[j] == ch:
            out.append(ch); j += 1
        else:
            raise SystemExit(f'align fail at {ai_t[:60]!r} ch={ch!r} bh[j]={bh_t[j:j+10]!r}')
    out.append(bh_t[j:])
    s = ''.join(out)
    s = s.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
    s = re.sub(r'\x01\s*(.*?)\s*\x02', r'*\1*', s)
    return re.sub(r'\s+', ' ', s).strip()
def cuv(t):
    t = t.replace('裡', '裏').replace('　', '')
    return t
def join_en(items):
    # NASB re-opens the quotation mark at each verse of continuing speech; keep only
    # the opening and closing marks (layout, not text).
    out, depth = [], 0
    for mk, t in items:
        if depth % 2 == 1 and t.startswith('"'):
            t = t[1:]
        depth += t.count('"')
        out.append(mk + t)
    return ' '.join(out)
data = {c: load(c) for c in range(1, 5)}
for u, spans in UNITS.items():
    zh, en = [], []
    multi = len({c for c, _, _ in spans}) > 1
    for c, a, b in spans:
        ai, fh, bh = data[c]
        for v in range(a, b + 1):
            mk = f'^{c}:{v}^' if multi else f'^{v}^'
            zh.append(mk + cuv(fh[v])); en.append((mk, nasb(ai[v]['text'], bh[v])))
    open(f'{D}/scripture/{u}.md', 'w').write(
        '### 中文 — 和合本 (CUV)\n\n> ' + ''.join(zh) + '\n\n### English — NASB 1995\n\n> ' + join_en(en) + '\n')
    print(u, 'ok')
