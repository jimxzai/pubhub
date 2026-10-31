#!/usr/bin/env python3
"""Extract Hosea verse text from the downloaded sources.

cuv.tsv      — FHL 和合本 (unv), house-normalised: strip the full-width
               space before 神 and the ─ apposition dash, 裡→裏
               (same normalisation as books/bible/james)
cuvmpt.tsv   — cnbible 現代標點和合本, second source for the diff
nasb1995.tsv — biblehub NASB 1995; supplied words kept as *word*
"""
import html, json, re

def norm_cuv(t):
    return t.replace('　', '').replace('─', '').replace('裡', '裏').replace('‧', '·')

out = {k: [] for k in ('cuv', 'cuvmpt', 'nasb1995')}
for c in range(1, 15):
    for r in json.load(open(f'cuv-unv-{c}.json'))['record']:
        out['cuv'].append((c, int(r['sec']), norm_cuv(r['bible_text'])))

    s = open(f'cuvmpt-{c}.html', encoding='utf-8').read()
    s = s[s.find('class="chap"'):s.find('id="botbox"')]
    s = re.sub(r'<p class="heading">.*?</p>', '', s)
    parts = re.split(r'<a href="/hosea/\d+-(\d+)\.htm" class="reftext">\d+&#8239;</a>', s)
    for v, t in zip(parts[1::2], parts[2::2]):
        t = html.unescape(re.sub(r'<[^>]+>', '', t)).strip()
        out['cuvmpt'].append((c, int(v), norm_cuv(t)))

    s = open(f'nasb1995-{c}.html', encoding='utf-8', errors='replace').read()
    s = s[s.find('class="chap"'):]
    s = s[:s.find('</div>')]
    s = re.sub(r'<font color="#000000"><b><i>.*?</i></b></font>', '', s)
    s = re.sub(r'([LG])<font size="1">(ORD|OD)</font>', r'\1\2', s)
    parts = re.split(r'<span class="reftext"><a href="http://biblehub\.com/hosea/\d+-(\d+)\.htm" target="_top"><b>\d+</b></a></span>', s)
    for v, t in zip(parts[1::2], parts[2::2]):
        t = re.sub(r'<i>(.*?)</i>', r'*\1*', t)
        # supplied-word italics end before punctuation (biblegateway agrees)
        t = re.sub(r'\*([^*]*?)([,.;:])\*', r'*\1*\2', t)
        t = html.unescape(re.sub(r'<[^>]+>', ' ', t)).replace('\x92', '’').replace('\x93', '“').replace('\x94', '”')
        t = re.sub(r'\s+', ' ', t.replace('\xa0', ' ')).strip()
        out['nasb1995'].append((c, int(v), t))

for k, rows in out.items():
    with open(f'{k}.tsv', 'w') as f:
        for c, v, t in rows:
            f.write(f'{c}:{v}\t{t}\n')
    print(k, len(rows))

# Character diff, punctuation ignored: the words must agree.
P = re.compile(r'[\s，。、；：！？「」『』（）—…·,.;:!?"\'“”‘’]')
a = {f'{c}:{v}': P.sub('', t) for c, v, t in out['cuv']}
b = {f'{c}:{v}': P.sub('', t) for c, v, t in out['cuvmpt']}
for k in a:
    if a[k] != b.get(k):
        print('DIFF', k, '\n  unv   ', a[k], '\n  cuvmpt', b.get(k))
