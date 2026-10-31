#!/usr/bin/env python3
"""Replace the line `@@SCRIPTURE a:b-c:d@@` in a chapter file with the full 經文 block
(CUV + NASB 1995) built from cuv.tsv / nasb1995.tsv, so no verse is ever typed
by hand.  Paragraph breaks follow biblehub's NASB paragraphing.  A range that
crosses a chapter boundary prints `^c:v^` at the first verse of each new chapter.

usage: python3 inject_scripture.py <chapter-file.md>
marker examples:  @@SCRIPTURE 1:1-19@@   @@SCRIPTURE 2:1-3:5@@   @@SCRIPTURE 31:31-40@@
"""
import re, sys, os

here = os.path.dirname(os.path.abspath(__file__))

def load(name):
    d = {}
    for l in open(f'{here}/{name}', encoding='utf-8'):
        k, t = l.rstrip('\n').split('\t', 1)
        c, v = k.split(':')
        d[(int(c), int(v))] = t
    return d

_starts = {}
def para_starts(c):
    if c in _starts: return _starts[c]
    s = open(f'{here}/nasb1995-{c}.html', encoding='utf-8', errors='replace').read()
    s = s[s.find('class="chap"'):]
    s = s[:s.find('</div>')]
    out = set()
    for piece in re.split(r'<p>', s)[1:]:
        m = re.search(r'biblehub\.com/lamentations/\d+-(\d+)\.htm', piece)
        if m: out.add(int(m.group(1)))
    _starts[c] = out
    return out

def parse(spec):
    m = re.fullmatch(r'(\d+):(\d+)-(?:(\d+):)?(\d+)', spec.strip())
    if not m: sys.exit('bad range ' + spec)
    c1, v1, c2, v2 = int(m[1]), int(m[2]), int(m[3] or m[1]), int(m[4])
    return c1, v1, c2, v2

def block(spec):
    cuv, nasb = load('cuv.tsv'), load('nasb1995.tsv')
    c1, v1, c2, v2 = parse(spec)
    keys = sorted(k for k in cuv if (k[0], k[1]) >= (c1, v1) and (k[0], k[1]) <= (c2, v2))
    def render(src, merge=False):
        paras, cur = [], []
        i = 0
        while i < len(keys):
            c, v = keys[i]
            if v in para_starts(c) and cur and i > 0:
                paras.append(cur); cur = []
            label = f'{c}:{v}' if (v == 1 and i > 0) else str(v)
            # CUV folds a few verses into the previous one; FHL/ai-eden leave the
            # placeholder 'a' in the next verse.  Print the pair as one verse (^8-9^).
            if merge and i + 1 < len(keys) and keys[i + 1][0] == c and cuv[keys[i + 1]] == 'a':
                label = f'{label}-{keys[i + 1][1]}'
                i += 1
            cur.append(f'^{label}^{src[(c, v)]}')
            i += 1
        if cur: paras.append(cur)
        return '\n>\n'.join('> ' + ''.join(p) for p in paras)
    return (
        "## 經文 (Scripture)\n\n"
        "> 版本說明：中文採和合本（CUV，FHL和合本版），經 cnbible.com（現代標點和合本 CUVMPT）與 ai-eden.com 逐節核對，和合本原有小注以括號保留；"
        "English 採 NASB 1995，經 biblehub.com 取得。\n\n"
        "### 中文 — 和合本 (CUV)\n\n" + render(cuv, merge=True) + "\n\n"
        "### English — NASB 1995\n\n" + render(nasb) + "\n"
    )

if __name__ == '__main__':
    path = sys.argv[1]
    t = open(path, encoding='utf-8').read()
    m = re.search(r'^@@SCRIPTURE ([0-9:\-]+)@@\s*$', t, re.M)
    if not m: sys.exit('no marker in ' + path)
    open(path, 'w', encoding='utf-8').write(t[:m.start()] + block(m[1]).rstrip('\n') + t[m.end():])
    print('injected', path, m[1])
