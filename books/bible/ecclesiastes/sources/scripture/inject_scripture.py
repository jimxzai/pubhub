#!/usr/bin/env python3
"""Replace the line `@@SCRIPTURE@@` in a chapter file with the full 經文 block
(CUV + NASB 1995) built from cuv.tsv / nasb1995.tsv, so no verse is ever typed
by hand.  Paragraph breaks follow biblehub's NASB paragraphing.

usage: python3 inject_scripture.py <chapter-number> <chapter-file.md>
"""
import re, sys, html

here = __import__('os').path.dirname(__import__('os').path.abspath(__file__))

def load(name):
    d = {}
    for l in open(f'{here}/{name}', encoding='utf-8'):
        k, t = l.rstrip('\n').split('\t', 1)
        c, v = k.split(':')
        d[(int(c), int(v))] = t
    return d

def para_starts(c):
    s = open(f'{here}/nasb1995-{c}.html', encoding='utf-8', errors='replace').read()
    s = s[s.find('class="chap"'):]
    s = s[:s.find('</div>')]
    starts = set()
    pieces = re.split(r'<p>', s)
    for piece in pieces[1:]:
        m = re.search(r'biblehub\.com/ecclesiastes/\d+-(\d+)\.htm', piece)
        if m:
            starts.add(int(m.group(1)))
    return starts

def block(c):
    cuv, nasb = load('cuv.tsv'), load('nasb1995.tsv')
    vs = sorted(v for (cc, v) in nasb if cc == c)
    starts = para_starts(c)
    def render(src):
        paras, cur = [], []
        for v in vs:
            if (c, v) not in src:
                continue
            if v in starts and cur and v != vs[0]:
                paras.append(cur); cur = []
            if src is cuv and (c, v) == (7, 27):
                label = '27-28'   # FHL / ai-eden / cnbible all print 7:27-28 together under 27
            else:
                label = str(v)
            cur.append(f'^{label}^{src[(c, v)]}')
        if cur: paras.append(cur)
        return '\n>\n'.join('> ' + ''.join(p) for p in paras)
    return (
        "## 經文 (Scripture)\n\n"
        "> 版本說明：中文採和合本（CUV，FHL和合本版），經 ai-eden.com 與 cnbible.com（現代標點和合本 CUVMPT）逐節核對；"
        "English 採 NASB 1995，經 biblehub.com 取得。\n\n"
        "### 中文 — 和合本 (CUV)\n\n" + render(cuv) + "\n\n"
        "### English — NASB 1995\n\n" + render(nasb) + "\n"
    )

if __name__ == '__main__':
    c, path = int(sys.argv[1]), sys.argv[2]
    t = open(path, encoding='utf-8').read()
    if '@@SCRIPTURE@@' not in t:
        sys.exit('no marker in ' + path)
    open(path, 'w', encoding='utf-8').write(t.replace('@@SCRIPTURE@@', block(c).rstrip('\n'), 1))
    print('injected', path)
