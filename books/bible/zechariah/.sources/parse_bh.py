#!/usr/bin/env python3
"""Parse biblehub.com/nasb/zechariah/N.htm (NASB 1995) -> bh-nasb-N.txt, one verse per line (curly quotes kept, as in Jonah)."""
import re, html, sys, os
D = os.path.dirname(os.path.abspath(__file__))
FIX = {0x91:'‘',0x92:'’',0x93:'“',0x94:'”',0x96:'–',0x97:'—',0x85:'…'}
for c in range(1, 15):
    h = open(f'{D}/bh-raw-{c}.html', encoding='utf-8', errors='replace').read()
    h = re.sub(r'&#(\d+);', lambda m: chr(int(m.group(1))) if int(m.group(1)) not in FIX and int(m.group(1)) < 128 or int(m.group(1)) > 159 else FIX.get(int(m.group(1)), ''), h)
    parts = re.split(r'<span class="reftext">.*?</span>', h)[1:]
    nums = re.findall(r'<span class="reftext">.*?<b>(\d+)</b>.*?</span>', h)
    assert len(parts) == len(nums), (c, len(parts), len(nums))
    out = []
    for n, p in zip(nums, parts):
        p = re.split(r'<font size="1"><br><br></font>|<p>\s*<font', p)[0]   # cut at next heading / end
        p = re.sub(r'<font size="1">(.*?)</font>', r'\1', p)               # L<font>ORD</font>
        p = re.sub(r'<i>(.*?)</i>', r'\1', p)
        p = re.sub(r'<br\s*/?>', ' ', p)
        p = re.sub(r'<[^>]+>', '', p)
        p = html.unescape(p).replace('\xa0', ' ')
        p = re.sub(r'NASB 1995 Copyright.*$', '', p)
        p = re.sub(r"NASB 1995 Copyright.*$", "", p, flags=re.S)
        out.append((int(n), re.sub(r'\s+', ' ', p).strip()))
    assert [n for n, _ in out] == list(range(1, len(out) + 1)), (c, [n for n, _ in out])
    open(f'{D}/bh-nasb-{c}.txt', 'w').write('\n'.join(t for _, t in out) + '\n')
    print(c, len(out))
