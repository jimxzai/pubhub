#!/usr/bin/env python3
"""heb.py <consonantal-regex> — find words in hebrew.tsv ignoring niqqud/cantillation; prints English-numbered refs.
usage: python3 heb.py 'זכר'   (substring match inside a word)  |  heb.py '^ו?זכר' --word"""
import re, sys, unicodedata
def strip(s):
    s = s.replace('־', ' ')
    return ''.join(ch for ch in s if not unicodedata.category(ch).startswith('M'))
rows = [l.rstrip('\n').split('\t', 1) for l in open(__file__.replace('heb.py', 'hebrew.tsv'), encoding='utf-8')]
def find(pat):
    r = re.compile(pat)
    hits = []
    for k, t in rows:
        for w in strip(t).split():
            if r.search(w): hits.append((k, w))
    return hits
if __name__ == '__main__':
    h = find(sys.argv[1])
    print(len(h), ' '.join(f'{k}:{w}' for k, w in h))
