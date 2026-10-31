#!/usr/bin/env python3
"""Look up 和合本 (FHL unv) verses, house-normalised like cuv.tsv.

usage: python3 cuv.py 詩 66 10-12      (book abbreviation as FHL uses it)
       python3 cuv.py 太 13 20,21
Caches responses under sources/scripture/fhl-cache/ so repeated checks are free.
"""
import json, os, sys, urllib.parse, urllib.request

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fhl-cache')

def norm(t):
    return t.replace('　', '').replace('─', '').replace('裡', '裏').replace('‧', '·')

def chapter(book, chap):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, f'{book}-{chap}.json')
    if not os.path.exists(path):
        url = 'https://bible.fhl.net/json/qb.php?' + urllib.parse.urlencode(
            {'chineses': book, 'chap': chap, 'version': 'unv', 'gb': 0})
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        data = urllib.request.urlopen(req, timeout=30).read()
        open(path, 'wb').write(data)
    return {int(r['sec']): norm(r['bible_text']) for r in json.load(open(path))['record']}

def verses(spec):
    out = []
    for part in spec.split(','):
        a, _, b = part.partition('-')
        out.extend(range(int(a), int(b or a) + 1))
    return out

if __name__ == '__main__':
    book, chap, spec = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    ch = chapter(book, chap)
    for v in verses(spec):
        print(f'{book}{chap}:{v}\t{ch.get(v, "<<MISSING>>")}')
