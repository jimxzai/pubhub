#!/usr/bin/env python3
"""Print cached CUV (fhl unv) and NASB 1995 (biblehub) verses of 1 Kings.
usage: scr.py CH [VERSES]   VERSES like 1-5,9,12-14 (default: all)
       scr.py CH --nasb|--cuv   only one version
Output uses ^n^ verse markers. Straight quotes for NASB (house style)."""
import sys, re, json, html, os
D = os.path.dirname(os.path.abspath(__file__))

def cuv(ch):
    f = f'{D}/cuvf/{ch}.json'
    if os.path.exists(f):
        return {int(k): v for k, v in json.load(open(f, encoding='utf8')).items()}
    return cuv_raw(ch)

def cuv_raw(ch):
    d = json.load(open(f'{D}/cuv/{ch}.json', encoding='utf8'))
    return {int(r['sec']): r['bible_text'].strip().replace('裡','裏') for r in d['record']}

def nasb(ch):
    s = open(f'{D}/nasb/{ch}.html', encoding='latin-1').read()
    s = s[s.find('class="chap"'):]
    s = s[:s.find('</div>')] if '</div>' in s else s
    parts = re.split(r'<span class="reftext"><a [^>]*><b>(\d+)</b></a></span>', s)
    out = {}
    for i in range(1, len(parts), 2):
        t = parts[i+1]
        t = re.sub(r'<font color="#000000"><b><i>.*?</i></b></font>', '', t, flags=re.S)  # headings
        t = re.sub(r'L<font size="1">ORD</font>', 'LORD', t)
        t = re.sub(r'G<font size="1">OD</font>', 'GOD', t)
        t = re.sub(r'<i>(.*?)</i>', r'*\1*', t, flags=re.S)
        t = re.sub(r'<[^>]+>', ' ', t)
        t = html.unescape(t).replace('\xa0', ' ')
        t = t.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
        t = re.sub(r'\s+', ' ', t).strip()
        out[int(parts[i])] = t
    return out

def rng(spec, allv):
    if not spec: return sorted(allv)
    r = []
    for p in spec.split(','):
        if '-' in p:
            a, b = p.split('-'); r += list(range(int(a), int(b)+1))
        else: r.append(int(p))
    return [v for v in r if v in allv]

if __name__ == '__main__':
    ch = int(sys.argv[1]); spec = None; which = 'both'
    for a in sys.argv[2:]:
        if a == '--nasb': which = 'nasb'
        elif a == '--cuv': which = 'cuv'
        else: spec = a
    if which in ('both', 'cuv'):
        c = cuv(ch); print('## CUV'); 
        for v in rng(spec, c): print(f'^{v}^{c[v]}')
    if which in ('both', 'nasb'):
        n = nasb(ch); print('## NASB')
        for v in rng(spec, n): print(f'^{v}^{n[v]}')
