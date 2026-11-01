#!/usr/bin/env python3
"""heb.py 1:1 1:2 ... → Hebrew (WLC) with cantillation marks stripped (niqqud kept), one word per token, for copying into 原文研讀 tables."""
import sys,re
rows={l.split('\t')[0]:l.split('\t')[2] for l in open(__file__.rsplit('/',1)[0]+'/hebrew.tsv',encoding='utf-8') if not l.startswith('#')}
for r in sys.argv[1:]:
    t=re.sub('[֑-ֽֿ֯]','',rows[r]).replace('־',' ')
    print(r,t)
