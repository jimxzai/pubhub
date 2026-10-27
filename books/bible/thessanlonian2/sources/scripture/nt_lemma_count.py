#!/usr/bin/env python3
"""NT-wide occurrences of a lemma in SBLGNT (morphgnt): python3 nt_lemma_count.py LEMMA..."""
import glob, os, sys, collections
BOOK = {61:'太',62:'可',63:'路',64:'約',65:'徒',66:'羅',67:'林前',68:'林後',69:'加',70:'弗',71:'腓',72:'西',73:'帖前',74:'帖後',75:'提前',76:'提後',77:'多',78:'門',79:'來',80:'雅',81:'彼前',82:'彼後',83:'約壹',84:'約貳',85:'約參',86:'猶',87:'啟'}
d = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sblgnt-nt')
hits = collections.defaultdict(list)
for f in sorted(glob.glob(os.path.join(d, '*.txt'))):
    for line in open(f):
        p = line.split()
        b, c, v = int(p[0][:2]) + 60, int(p[0][2:4]), int(p[0][4:6])
        hits[p[6]].append(f'{BOOK[b]}{c}:{v}')
for lemma in sys.argv[1:]:
    h = hits.get(lemma, [])
    print(f'{lemma}\t{len(h)}\t{" ".join(h)}')
