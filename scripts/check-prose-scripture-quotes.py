#!/usr/bin/env python3
"""Check Chinese Scripture quoted in running PROSE against the chapter's own
verified 經文 block.

Every other checker in this repo guards the ENGLISH commentary quotes
(verify-citations.py, verify-sermon-quotes.py, check-citation-ledger.py) or the
Scripture BLOCK itself (lint-scripture-text.py). Nothing looks at a Chinese
verse quoted inside a 「」 in ordinary prose — and that is where the Deuteronomy
volume was found (2026-09-06) carrying five verses that were not the verse they
claimed to be, each one contradicting the correct text printed 30-150 lines
above it in the same file.

The 經文 block is the trusted side: it has been machine-compared verse by verse
against bible.fhl.net. So a same-book quote can be checked with no network at
all — it must appear, contiguously, inside the verse it cites.

Usage:  check-prose-scripture-quotes.py <book-dir> [...]
Exit 1 if any MISMATCH is found (NOT-IN-BLOCK and cross-book refs are reported
for review but do not fail the run).
"""
import re, sys, glob, os, unicodedata

VERSE_RE = re.compile(r'\^(\d+(?:[-–]\d+)?)\^')
# 「…」 quote carrying a bare same-book reference either just before or just after:
#   12:8「…」   /   「…」（8:17）   /   「…」，9:19）  /  「…」(8:3)
QUOTE = r'[「『]([^」』]{6,120})[」』]'
# A bare N:M only refers to THIS book when no other book's name precedes it.
# 「弗2:8」「結36:26」「太4:4」 must not be read as chapter 2, 36, 4 of this book —
# that silently compares a New Testament quote against an Old Testament verse.
OTHER_BOOK = r'(?<![\u4e00-\u9fff0-9])'
REF_BEFORE = re.compile(OTHER_BOOK + r'(\d{1,2}):(\d{1,3})(?:[-–]\d{1,3})?\s*' + QUOTE)
REF_AFTER  = re.compile(QUOTE + r'\s*[，,]?\s*[（(]?\s*' + OTHER_BOOK + r'(\d{1,2}):(\d{1,3})(?:[-–]\d{1,3})?\s*[）)]')

# 和合本 prints the divine-name separator as ─ (U+2500) plus an ideographic space
# before 神; both are typography, not wording, and must not count as a difference.
PUNCT = '，。、；：？！「」『』（）()《》〈〉…—－-─―‧·　 ,.;:?!\'"'
def norm(s):
    s = unicodedata.normalize('NFKC', s)
    return ''.join(c for c in s if c not in PUNCT)

def unit_text(text):
    """All CUV verse text printed in this unit's 經文 section, as one string.

    An earlier version of this script keyed verses by (chapter, verse), inferring
    chapter boundaries from where verse numbers restart. That inference is wrong
    whenever a unit prints selected, non-contiguous verses, and a wrong inference
    compares a quote against the wrong verse — the very failure this script
    exists to prevent. So the question asked here is the weaker but sound one:
    IS THIS QUOTED TEXT ACTUALLY THE SCRIPTURE THIS UNIT PRINTS?

    Two limits, both deliberate and both worth knowing before trusting a clean run:
    (1) only quotes carrying a verse reference are examined. A 「」 that reads as
        Scripture but cites nothing is invisible here — 04-shema-and-love.md
        carried a non-CUV 示瑪 wording that way, found by eye, not by this script.
    (2) a quote whose words are real Scripture but whose verse number is wrong is
        not caught; see below.

    Consequence, stated plainly: a quote that is real Scripture but carries the
    wrong verse number is NOT caught. Altered or invented wording — the defect
    class that produced 「用腳踏轆轤澆灌」 and a 12:8 with its speaker flipped — is.
    """
    m = re.search(r'^## 經文.*?$(.*?)^## ', text, re.S | re.M)
    if not m:
        return ''
    sec = m.group(1)
    eng = re.search(r'^### (?:英文|English)', sec, re.M)
    if eng:
        sec = sec[:eng.start()]
    out = []
    for line in sec.split('\n'):
        if line.startswith('>'):
            out.append(VERSE_RE.sub('', line[1:]))
    return ' '.join(out)

def scan(path):
    text = open(path, encoding='utf-8').read()
    body = norm(unit_text(text))
    if not body:
        return []
    found, in_block = [], False
    for ln, line in enumerate(text.split('\n'), 1):
        if line.startswith('## '):
            in_block = line.startswith('## 經文')
        if in_block or line.startswith('>') or line.startswith('|'):
            continue
        for rx, order in ((REF_BEFORE, 'ref-first'), (REF_AFTER, 'quote-first')):
            for m in rx.finditer(line):
                q = m.group(3) if order == 'ref-first' else m.group(1)
                ref = (f'{m.group(1)}:{m.group(2)}' if order == 'ref-first'
                       else f'{m.group(2)}:{m.group(3)}')
                if '\u300e' in q or '\u300d' in q:
                    continue                  # regex ran past a nested quote
                pieces = [norm(x) for x in re.split(r'[\u2026]+|\.\.\.', q) if norm(x)]
                pos, ok = 0, True
                for pc in pieces:
                    i = body.find(pc, pos)
                    if i < 0:
                        ok = False
                        break
                    pos = i + len(pc)
                if not ok:
                    found.append((ln, ref, q))
    return found

def main(argv):
    paths = []
    for a in argv:
        paths += sorted(glob.glob(os.path.join(a, '[0-9]*.md'))) if os.path.isdir(a) else [a]
    bad = 0
    for p in paths:
        for ln, ref, q in scan(p):
            bad += 1
            print(f'[NOT-IN-UNIT] {p}:{ln}  {ref}')
            print(f'    prose : \u300c{q}\u300d')
    print(f'\n{len(paths)} file(s) scanned; {bad} quote(s) not found in the unit\u2019s printed Scripture.')
    return 1 if bad else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:] or ['.']))
