#!/usr/bin/env python3
"""Build scripture/cuv-malachi.txt and scripture/nasb1995-malachi.txt and a two-source diff report.

CUV   primary = ai-eden.com (t=CUV, textZh), 裡→裏 per project policy; second witness = bible.fhl.net unv.
NASB  = biblehub.com/nasb/malachi/N.htm (header "NASB 1995"); italics kept as *...*; LORD kept as LORD.
        Cross-checked word-by-word against ai-eden's NASB-family text (punctuation/case ignored).
Verse numbering = English (和合本 / NASB): 4 chapters, 14 / 17 / 18 / 6 verses.
"""
import json, re, html, os
D = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(D, 'scripture')


def bh_verses(c):
    t = open(f'{S}/bh-nasb-{c}.html', encoding='utf-8').read()
    out = {}
    for m in re.finditer(r'<span class="reftext"><a[^>]*><b>(\d+)</b></a></span>(.*?)(?=<span class="reftext">|<p>\s*<span|</div>|$)', t, re.S):
        v = int(m.group(1)); s = m.group(2)
        s = re.sub(r'<font size="1">(.*?)</font>', r'\1', s)        # L<font>ORD</font> -> LORD
        s = re.sub(r'<i>(.*?)</i>', r'*\1*', s, flags=re.S)
        s = re.sub(r'<br ?/?>', ' ', s)
        s = re.sub(r'<[^>]+>', '', s)
        s = html.unescape(s)
        s = s.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
        s = re.sub(r'\s+', ' ', s).strip()
        # biblehub appends the next section heading (italic, Capitalised, no end punctuation) to the last verse of a section
        s = re.sub(r'(?<=[.!?"\'])\s+\*[A-Z][^*.,;:!?]*\*$', '', s)
        out[v] = s
    return out


def norm_en(s):
    s = s.replace('*', '').replace('[', '').replace(']', '')
    return re.findall(r"[a-z0-9]+", s.lower())


def norm_zh(s):
    s = s.replace('裡', '裏')
    return re.sub(r'[\s　，。、；：！？「」『』（）“”‘’\-—·]', '', s)


rep = []
cuv_lines, nasb_lines = [], []
for c in range(1, 5):
    ai = {v['verse']: v for v in json.load(open(f'{S}/aieden-malachi-{c}.json'))['data']['verses']}
    fh = {r['sec']: r['bible_text'] for r in json.load(open(f'{S}/fhl-unv-{c}.json'))['record']}
    bh = bh_verses(c)
    assert set(ai) == set(bh) == set(fh), (c, sorted(ai), sorted(bh), sorted(fh))
    for v in sorted(ai):
        zh = ai[v]['textZh'].replace('裡', '裏').replace('　', '')
        cuv_lines.append(f'{c}:{v}\t{zh}')
        nasb_lines.append(f'{c}:{v}\t{bh[v]}')
        if norm_zh(zh) != norm_zh(fh[v]):
            rep.append(f'CUV  {c}:{v}  ai-eden≠fhl\n   ai: {zh}\n  fhl: {fh[v]}')
        # NASB: compare word sequences (ai-eden text is NASB-family; differences are reported, not hidden)
        if norm_en(bh[v]) != norm_en(ai[v]['text']):
            rep.append(f'NASB {c}:{v}  biblehub≠ai-eden\n   bh: {bh[v]}\n   ai: {ai[v]["text"]}')
open(f'{S}/cuv-malachi.txt', 'w', encoding='utf-8').write('\n'.join(cuv_lines) + '\n')
open(f'{S}/nasb1995-malachi.txt', 'w', encoding='utf-8').write('\n'.join(nasb_lines) + '\n')
open(f'{S}/two-source-diff.txt', 'w', encoding='utf-8').write('\n\n'.join(rep) + '\n')
print(len(cuv_lines), 'verses;', len(rep), 'differences ->', f'{S}/two-source-diff.txt')
