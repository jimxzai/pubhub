#!/usr/bin/env python3
"""Re-generate the `## 經文` block of finished chapter files from the current
cuv.tsv / nasb1995.tsv (after apply_name_fixes.py), and normalise the few name
tokens the chapter prose shares with the Scripture text.

usage: python3 reinject.py <chapter-number> ...   (default: every chapter present)
"""
import glob, os, re, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import inject_scripture as inj
book = os.path.abspath(os.path.join(here, '..', '..'))
nums = [int(a) for a in sys.argv[1:]] or range(1, 14)
for c in nums:
    hits = glob.glob(f'{book}/{c:02d}-*.md')
    if not hits: continue
    p = hits[0]
    t = open(p, encoding='utf-8').read()
    new = inj.block(c).rstrip('\n')
    m = re.search(r'## 經文 \(Scripture\)\n.*?(?=\n\n---\n)', t, flags=re.S)
    if not m: print('NO 經文 block', p); continue
    t2 = t[:m.start()] + new + t[m.end():]
    t2 = t2.replace('毘', '毗').replace('橫樑', '橫梁')
    if t2 != t:
        open(p, 'w', encoding='utf-8').write(t2); print('updated', os.path.basename(p))
    else:
        print('unchanged', os.path.basename(p))
