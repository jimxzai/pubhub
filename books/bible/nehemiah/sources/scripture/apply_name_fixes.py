#!/usr/bin/env python3
"""Apply the proper-name / character choices where FHL 'unv' modernises and
ai-eden.com (project standard, aieden-N.json) disagrees.

Rule (same as scripts/gen-ezra-scripture.py):
  * 毘->毗, 橫樑->橫梁, 泰爾->推羅, 米該亞->米該雅 (12:41), 6:1 stray 的:
        ai-eden AND cnbible (cuvmpt.tsv) both carry the other form.
  * 阿拉伯->亞拉伯 (2:19, 4:7, 6:1), 撒馬利亞->撒瑪利亞 (4:2), 西奈->西乃 (9:13):
        proper names, ai-eden decides (project standard).
  * 12:28-29: FHL and ai-eden merge the two verses and leave a bare 'a' at 12:29;
        split per cnbible.
  * 嗎/麼 and 吧/罷 are NOT changed: cnbible agrees with FHL and the house books
        print 嗎 (see 約21 你愛我嗎).
cuv.fhl-base.tsv is the untouched FHL text; cuv.tsv is rebuilt from it.
"""
import re
src = open('cuv.fhl-base.tsv', encoding='utf-8').read().splitlines()
log = []
out = []
for line in src:
    k, t = line.split('\t', 1)
    o = t
    t = t.replace('毘', '毗').replace('橫樑', '橫梁')
    if k == '13:16': t = t.replace('泰爾', '推羅')
    if k == '12:41': t = t.replace('米該亞', '米該雅')
    if k in ('2:19', '4:7', '6:1'): t = t.replace('阿拉伯', '亞拉伯')
    if k == '4:2': t = t.replace('撒馬利亞', '撒瑪利亞')
    if k == '9:13': t = t.replace('西奈', '西乃')
    if k == '6:1': t = t.replace('安門扇）的，', '安門扇），')
    # FHL and ai-eden both print 12:28 as the two verses merged and 12:29 as the
    # placeholder 'a'; cnbible splits them at the comma after 伯·吉甲.
    if k == '12:28': t = '歌唱的人從耶路撒冷的周圍和尼陀法的村莊與伯·吉甲，'
    if k == '12:29': t = '又從迦巴和押瑪弗的田地聚集，因為歌唱的人在耶路撒冷四圍為自己立了村莊。'
    if t != o: log.append(k)
    out.append(f'{k}\t{t}')
open('cuv.tsv', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(len(log), 'verses changed:', ' '.join(log))
