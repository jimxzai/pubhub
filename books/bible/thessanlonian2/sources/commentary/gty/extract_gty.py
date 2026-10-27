#!/usr/bin/env python3
"""Extract title, passage and transcript paragraphs from saved gty.org sermon pages."""
import glob, html, re
for f in sorted(glob.glob('53-*.html'), key=lambda x: int(x[3:-5])):
    s = open(f).read()
    code = f[:-5]
    title = html.unescape(re.search(r'<h1[^>]*>([^<]*)', s).group(1)).strip()
    paras = [html.unescape(re.sub(r'<[^>]+>', '', p)).strip()
             for p in re.findall(r'<p[^>]*>(.*?)</p>', s, re.S)]
    paras = [p for p in paras if len(p) > 120]
    with open(f'{code}.txt', 'w') as o:
        o.write(f'{title}\nJohn MacArthur, sermon {code}\n\n' + '\n\n'.join(paras) + '\n')
    print(code, title, len(paras), sum(map(len, paras)))
