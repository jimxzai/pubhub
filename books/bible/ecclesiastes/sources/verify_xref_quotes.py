#!/usr/bin/env python3
"""Check every Chinese Scripture quotation in the editorial prose of a book directory,
whatever order the reference and the quote come in.

WHY THIS EXISTS
---------------
scripts/verify-prose-citations.py only sees the shape  「quote」（ref）  -- the reference
directly AFTER the quote.  This book's 全經連線 bullets and 你看見耶穌了嗎 paragraphs
usually put the reference BEFORE the quote  (**傳5:2 與 太6:7-9**——「…」), and several quotes
share one reference list.  Those quotes were never machine-checked.

METHOD
  For every prose line (not inside 經文 / 配詩 blocks, not a table row, not an English
  commentary quote), collect
      refs   : 太6:7-9, 羅15:3, 林後 1:3-4 ... and bare 5:1 / 5:2-3 (= this book, 傳)
      quotes : every 「…」 whose normalised text is >= MINLEN characters
  and require each quote (or each side of a 「A……B」 elision) to occur inside the
  concatenated verses of ANY ref on that line.
  OK        found
  UNMATCHED has refs on the line, but the quote is in none of them  -> a real finding
            (or a quote of a *translation*, e.g. NASB, or of Hebrew -- review by eye)
  NO-REF    no reference on the line; printed for review only

Ecclesiastes verses come from sources/scripture/cuv.tsv (the book's own text, with
7:27-28 merged); every other book from bible.fhl.net (unv), cached.

usage: python3 verify_xref_quotes.py <book-dir> [--minlen 8] [--no-ref]
"""
import argparse, json, re, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = Path('/Users/jimxiao/dev/pubhub/scripts/fhl-prose-cache')

BOOKS = ['創','出','利','民','申','書','士','得','撒上','撒下','王上','王下','代上','代下','拉','尼','斯','伯','詩',
         '箴','傳','歌','賽','耶','哀','結','但','何','珥','摩','俄','拿','彌','鴻','哈','番','該','亞','瑪',
         '太','可','路','約一','約二','約三','約壹','約貳','約參','約','徒','羅','林前','林後','加','弗','腓','西',
         '帖前','帖後','提前','提後','多','門','來','雅','彼前','彼後','猶','啟']
CODE = {'約壹': '約一', '約貳': '約二', '約參': '約三'}
BOOK_RE = '|'.join(sorted(BOOKS, key=len, reverse=True))
REF_RE = re.compile(rf'(?P<book>{BOOK_RE})?\s*(?P<ch>\d{{1,3}}):(?P<v1>\d{{1,3}})(?:[-–](?P<v2>\d{{1,3}}))?')
PUNCT = "，。；：、！？「」『』（）〔〕—…·　 　〈〉《》,.;:!?\"'“”‘’()[]"


def norm(s):
    s = s.replace('裡', '裏')
    s = s.replace('地', '的')  # fhl writes 地 where ai-eden/CUV 1919 writes 的 (NT adverbs)
    s = re.sub(r'【[^】]*】', '', s)
    s = re.sub(r'[（(](?:原文|或譯|或作|光明|野狗|尼提寧|後裔|有古卷|下同|同)[^）)]*[）)]', '', s)
    s = s.replace('祂', '他').replace('袮', '你')
    for c in PUNCT:
        s = s.replace(c, '')
    return re.sub(r'\s+', '', s)


_eccl = {}
for l in open(HERE / 'scripture' / 'cuv.tsv', encoding='utf-8'):
    k, t = l.rstrip('\n').split('\t', 1)
    c, v = k.split(':')
    _eccl[(int(c), int(v))] = t


def fhl(code, chap):
    CACHE.mkdir(exist_ok=True)
    safe = ''.join(f'{ord(c):04x}' for c in code)
    f = CACHE / f'{safe}-{chap}.json'
    if not f.exists() or f.stat().st_size < 200:
        from urllib.parse import quote
        subprocess.run(['curl', '-s', '-m', '40', '-A', 'Mozilla/5.0',
                        f'https://bible.fhl.net/json/qb.php?chineses={quote(code)}&chap={chap}&version=unv&gb=0',
                        '-o', str(f)], check=True)
        time.sleep(1.2)
    try:
        d = json.loads(f.read_text(encoding='utf-8'))
    except Exception:
        return {}
    return {int(r['sec']): r.get('bible_text', '') for r in d.get('record', [])} if d.get('status') == 'success' else {}


def verses(book, ch, v1, v2):
    v2 = v2 or v1
    if book in (None, '', '傳'):
        out = ''.join(_eccl.get((ch, v), '') for v in range(v1, v2 + 1))
        if ch == 7 and v1 <= 28 <= v2:      # 7:27-28 are printed together under 7:27 (see scripture/apply_fixes.py)
            out += _eccl.get((7, 27), '')
        return out
    d = fhl(CODE.get(book, book), ch)
    return ''.join(d.get(v, '') for v in range(v1, v2 + 1))


def refs_of(line):
    out = []
    for m in REF_RE.finditer(line):
        b = m.group('book')
        out.append((b, int(m.group('ch')), int(m.group('v1')), int(m.group('v2') or m.group('v1'))))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('book')
    ap.add_argument('--minlen', type=int, default=8)
    ap.add_argument('--no-ref', action='store_true')
    a = ap.parse_args()
    tot = ok = bad = noref = 0
    for f in sorted(Path(a.book).glob('[0-9]*.md')):
        sect = ''
        for i, line in enumerate(f.read_text(encoding='utf-8').split('\n'), 1):
            if line.startswith('## '):
                sect = line
            if re.match(r'^## (經文|配詩|詩篇與聖詩)', sect):
                continue
            if line.startswith('|') or line.startswith('> "') or line.startswith('> —') or line.startswith('> *'):
                continue
            if line.startswith('>') and '基督焦點' not in sect and '歷代注疏' not in sect:
                continue
            if line.startswith('>') and '歷代注疏' in sect:
                continue
            quotes = re.findall(r'「([^」]+)」', line)
            if not quotes:
                continue
            rs = refs_of(line)
            pool = norm(''.join(verses(*r) for r in rs)) if rs else ''
            for q in quotes:
                if q.startswith(('或譯', '原文')):   # CUV's own footnote text, not verse text
                    continue
                frags = [x for x in re.split(r'…+|\.{3,}', q) if len(norm(x)) >= 3]
                if sum(len(norm(x)) for x in frags) < a.minlen:
                    continue
                tot += 1
                if not rs:
                    noref += 1
                    if a.no_ref:
                        print(f'NO-REF    {f.name}:{i}  「{q[:40]}」')
                    continue
                if all(norm(x) in pool for x in frags):
                    ok += 1
                else:
                    bad += 1
                    print(f'UNMATCHED {f.name}:{i}  「{q[:60]}」\n            refs: ' +
                          ', '.join(f"{b or '傳'}{c}:{v1}" + (f'-{v2}' if v2 != v1 else '') for b, c, v1, v2 in rs))
    print(f'\n{tot} quotes (>= {a.minlen} chars) | {ok} OK | {bad} UNMATCHED | {noref} NO-REF')


main()
