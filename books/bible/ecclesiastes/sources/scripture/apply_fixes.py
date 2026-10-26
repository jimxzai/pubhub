#!/usr/bin/env python3
"""Build cuv.tsv from cuv.fhl-base.tsv (untouched FHL 'unv', house-normalised).

Choices where FHL modernises and ai-eden.com (project standard, aieden-N.json)
carries the 1919 reading:
  * 2:10  它 -> 他   (ai-eden 他; same pronoun policy as Ruth 2:14 fix)
  * 7:26  她 -> 他   (x3; ai-eden 他)
Left as FHL (ai-eden and cnbible CUVMPT both agree with FHL, or ai-eden has its own slip):
  * 7:1   ai-eden prints '美好的的膏油' (doubled 的) -- FHL/cnbible: 美好的膏油
  * 6:6 嗎/麼, 2:1 吧/罷 -- not changed (house books print 嗎, see apply_name_fixes in nehemiah)
7:27-28: FHL, ai-eden and cnbible all print the English 7:27-28 content together under
  7:27 and leave 7:28 as a placeholder ('a' / '0'); no source splits it, so we do not
  invent a split.  cuv.tsv carries the merged text at 7:27 and has no 7:28 row;
  inject_scripture.py labels it ^27-28^.
"""
log = []
out = []
for line in open('cuv.fhl-base.tsv', encoding='utf-8').read().splitlines():
    k, t = line.split('\t', 1)
    o = t
    if k == '2:10': t = t.replace('不給它的', '不給他的')
    if k == '7:26': t = t.replace('她', '他')
    if k == '7:28': continue
    if t != o: log.append(k)
    out.append(f'{k}\t{t}')
open('cuv.tsv', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(len(out), 'rows; changed:', ' '.join(log), '; dropped 7:28 (merged into 7:27)')
