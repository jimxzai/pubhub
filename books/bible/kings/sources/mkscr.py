#!/usr/bin/env python3
"""mkscr.py — emit the `## 經文 (Scripture)` section of a chapter file from the local
CUV/NASB caches, so Scripture is never typed by hand.

usage:  mkscr.py "中文標題|English title|CH|verses" [...]
   verses: 1-6  or  1-2,5-6   (gaps get ……)
   e.g.   mkscr.py "智慧的請求|The Request for Wisdom|3|5-15" "兩個婦人|The Two Women|3|16-28"
Writes markdown to stdout. Verse text is copied verbatim from the cache (scr.py)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scr import cuv, nasb, rng

def label(ch, spec):
    return f'{ch}:{spec.replace(",", "，")}'.replace('，', ', ') if ',' in spec else f'{ch}:{spec}'

def body(ver, verses, sep=''):
    out, prev = [], None
    for v in verses:
        if prev is not None and v != prev + 1:
            out.append('……')
        out.append(f'^{v}^{ver[v]}')
        prev = v
    return sep.join(out)

if __name__ == '__main__':
    cu_cache, na_cache = {}, {}
    cu_out, na_out = [], []
    for seg in sys.argv[1:]:
        zh, en, ch, spec = seg.split('|')
        ch = int(ch)
        c = cu_cache.setdefault(ch, cuv(ch)); n = na_cache.setdefault(ch, nasb(ch))
        vs = rng(spec, c)
        lab = label(ch, spec)
        cu_out.append(f'**{zh}（{lab}）**\n\n> {body(c, vs)}\n')
        na_out.append(f'**{en} ({lab})**\n\n> {body(n, vs, ' ')}\n')
    print('## 經文 (Scripture)\n\n### 中文 — 和合本 (CUV)\n')
    print('\n'.join(cu_out))
    print('### English — NASB\n')
    print('\n'.join(na_out))
