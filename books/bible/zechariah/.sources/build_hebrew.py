#!/usr/bin/env python3
"""oshb-zechariah.xml -> hebrew.tsv  (英文節號[和合本/NASB] <TAB> MT節號 <TAB> WLC text; maqqef -> space, '/' prefix marks removed)."""
import re, os
D = os.path.dirname(os.path.abspath(__file__))
x = open(f'{D}/oshb-zechariah.xml', encoding='utf-8').read()
verses = {}
for m in re.finditer(r'<verse osisID="Zech\.(\d+)\.(\d+)">(.*?)</verse>', x, re.S):
    c, v, body = int(m.group(1)), int(m.group(2)), m.group(3)
    ws = re.findall(r'<w (?![^>]*x-ketiv)[^>]*>(.*?)</w>', body)   # skip ketiv; the qere form follows inside <note>
    verses[(c, v)] = ' '.join(w.replace('/', '') for w in ws)
EN = {1: 21, 2: 13, 3: 10, 4: 14, 5: 11, 6: 15, 7: 14, 8: 23, 9: 17, 10: 12, 11: 17, 12: 14, 13: 9, 14: 21}
def eng_to_mt(c, v):
    if c == 1 and v >= 18: return (2, v - 17)       # Eng 1:18-21 = MT 2:1-4
    if c == 2: return (2, v + 4)                     # Eng 2:1-13  = MT 2:5-17
    return (c, v)
out = ['# 英文節號(和合本/NASB)\t希伯來文節號(MT)\t希伯來文(WLC via OSHB)']
cnt = {}
for c in range(1, 15):
    for v in range(1, EN[c] + 1):
        mt = eng_to_mt(c, v)
        cnt[mt] = 1
        out.append(f'{c}:{v}\t{mt[0]}:{mt[1]}\t{verses[mt]}')
assert len(cnt) == len(verses) == 211, (len(cnt), len(verses))
open(f'{D}/hebrew.tsv', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(len(out) - 1, 'verses')
