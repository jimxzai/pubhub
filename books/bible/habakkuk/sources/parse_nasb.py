#!/usr/bin/env python3
"""biblehub NASB 1995 chapter HTML -> scripture/nasb1995-hab-N.txt  (one line per verse: 'v<TAB>text'; supplied words as *italic*)."""
import re, html, sys, os
D = os.path.dirname(os.path.abspath(__file__))
for c in (1, 2, 3):
    t = open(f'{D}/scripture/bh-nasb-{c}.html', encoding='utf-8').read()
    parts = re.split(r'<span class="reftext"><a [^>]*><b>(\d+)</b></a></span>', t)
    out = []
    for i in range(1, len(parts), 2):
        v, body = int(parts[i]), parts[i + 1]
        body = re.sub(r'<div align="right">(Selah\.)</div>', r' \1 ', body)
        body = re.split(r'<span class="(?:hdg|heading)|<div|<h\d|<!--', body)[0]
        body = re.sub(r'L<font size="1">ORD</font>', 'LORD', body)
        body = re.sub(r'G<font size="1">OD</font>', 'GOD', body)
        body = re.sub(r'<i>(.*?)</i>', lambda m: '*' + m.group(1).strip() + '*', body, flags=re.S)
        body = re.sub(r'<br\s*/?>|<p>|</p>', ' ', body)
        body = re.sub(r'<[^>]+>', '', body)
        body = html.unescape(body).replace('\xa0', ' ')
        body = re.sub(r'\s+', ' ', body).strip()
        body = body.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
        out.append((v, body))
    open(f'{D}/scripture/nasb1995-hab-{c}.txt', 'w').write(''.join(f'{v}\t{b}\n' for v, b in out))
    print(c, len(out))
