#!/usr/bin/env python3
"""Generate the 經文 blocks (CUV + NASB 1995) for each Zechariah unit.
CUV  : fhl 和合本 (unv), cross-checked vs ai-eden CUV (identical ignoring punctuation); 裡→裏 per project policy.
NASB : biblehub 1995 text; supplied (italic) words taken from ai-eden's [bracketed] words.
Verse markers use English (和合本/NASB) numbering; units crossing a chapter use ^c:v^.
"""
import json, re, os
D = os.path.dirname(os.path.abspath(__file__))
UNITS = {  # file prefix: [(chapter, v_from, v_to), ...]   (see PLAN.md)
    '01': [(1, 1, 6)], '02': [(1, 7, 17)], '03': [(1, 18, 21)], '04': [(2, 1, 13)],
    '05': [(3, 1, 10)], '06': [(4, 1, 14)], '07': [(5, 1, 11)], '08': [(6, 1, 8)], '09': [(6, 9, 15)],
    '10': [(7, 1, 14)], '11': [(8, 1, 23)],
    '12': [(9, 1, 8)], '13': [(9, 9, 17)], '14': [(10, 1, 12)], '15': [(11, 1, 17)],
    '16': [(12, 1, 14)], '17': [(13, 1, 9)], '18': [(14, 1, 11)], '19': [(14, 12, 21)],
}
# CUV = fhl 'unv' text (punctuation 「」) with the characters of the 1919 text as attested by ai-eden AND cnbible.com
# (fhl modernises: 嗎/她/它/牠/泰爾/黎巴嫩...). See cuv-crosscheck.md for the per-verse decisions.
OVR = {
    (1,5): [('嗎','麼')], (1,6): [('嗎','麼')], (3,2): [('嗎','麼')], (7,3): [('嗎','麼')], (7,5): [('嗎','麼')],
    (7,6): [('嗎','麼')], (7,7): [('嗎','麼')], (8,6): [('嗎','麼')],
    (4,2): [('頂上有燈盞','頂上有盞燈')],
    (5,9): [('她','他')], (5,10): [('她','他')], (5,11): [('它','他')], (6,7): [('牠','他')],
    (7,2): [('沙利色','沙利亞')], (8,2): [('她','他')], (9,4): [('她','他')],
    (9,1): [('大馬士革','大馬色')], (9,2): [('泰爾','推羅')], (9,3): [('泰爾','推羅')],
    (9,13): [('希臘','希利尼')], (10,10): [('黎巴嫩','利巴嫩')], (11,1): [('黎巴嫩','利巴嫩')],
    (11,3): [('約旦','約但')], (11,15): [('愚昧牧人','愚昧人')],
    # 14:12 deliberately NOT overridden: 1919 CUV digitisations read 吞(sic); fhl/CUVMPT/Hebrew לשׁונו = 舌. Decision flagged.
}
QUOTE = set('\'"‘’“”')
def load(c):
    ai = {v['verse']: v for v in json.load(open(f'{D}/aieden-zechariah-{c}.json'))['data']['verses']}
    fh = {r['sec']: r['bible_text'] for r in json.load(open(f'{D}/fhl-unv-{c}.json'))['record']}
    bh = open(f'{D}/bh-nasb-{c}.txt').read().split('\n')
    bh = {i + 1: re.sub(r'\s+', ' ', re.sub(r'NASB 1995 Copyright.*$', '', b)).strip() for i, b in enumerate(bh)}
    return ai, fh, bh
def nasb(ai_t, bh_t):
    ai_t = re.sub(r'\s+', ' ', ai_t.replace('--', '—')).strip()
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
        if ch == ' ' and j < len(bh_t) and bh_t[j] != ' ':
            continue
        if ch != ' ' and j < len(bh_t) and bh_t[j] == ' ' and bh_t[j+1:j+2] == ch:
            out.append(' '); j += 1
        if j < len(bh_t) and bh_t[j] == ch:
            out.append(ch); j += 1
        else:
            raise SystemExit(f'align fail at {ai_t[:60]!r} ch={ch!r} bh[j]={bh_t[j:j+10]!r}')
    out.append(bh_t[j:])
    s = ''.join(out)
    s = s.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
    s = re.sub(r'\x01\s*(.*?)\s*\x02', r'*\1*', s)
    return re.sub(r'\s+', ' ', s).strip()
def cuv(t, key=None):
    t = t.replace('裡', '裏').replace('　', '')
    for x, y in OVR.get(key, []):
        assert x in t, (key, x, t)
        t = t.replace(x, y)
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
data = {c: load(c) for c in range(1, 15)}
for u, spans in UNITS.items():
    zh, en = [], []
    multi = len({c for c, _, _ in spans}) > 1
    for c, a, b in spans:
        ai, fh, bh = data[c]
        for v in range(a, b + 1):
            mk = f'^{c}:{v}^' if multi else f'^{v}^'
            zh.append(mk + cuv(fh[v], (c, v))); en.append((mk, nasb(ai[v]['text'], bh[v])))
    open(f'{D}/scripture/{u}.md', 'w', encoding='utf-8').write(
        '### 中文 — 和合本 (CUV)\n\n> ' + ''.join(zh) + '\n\n### English — NASB 1995\n\n> ' + join_en(en) + '\n')
    print(u, 'ok')
