#!/usr/bin/env python3
"""Check every `> "English quote"` line in chapter files against the local source text of the commentator named on the
`> — ...` line that follows it (Calvin, Henry, Morgan; MacArthur is left to scripts/verify-sermon-quotes.py).

  python3 sources/check_quotes.py books/bible/malachi/02-*.md [...]    # exit 1 on any MISS

Matching ignores case, punctuation, line breaks, CCEL footnote markers like [202] and OCR hyphenation at line ends.
A quote with '...' / '…' is checked piece by piece. Output per quote: OK / MISS (+ first words) / SKIP (other commentator).
"""
import re, sys, unicodedata
from pathlib import Path

SRC = Path(__file__).resolve().parent / 'commentary'
FILES = {
    'Calvin': 'calvin-malachi.txt',
    'Henry': 'henry-malachi.txt',
    'Morgan': 'morgan-living-messages-malachi-ocr1.txt',
    'Keil': 'keil-minor-prophets-vol2.txt',
}


def norm(t):
    t = unicodedata.normalize('NFKC', t)
    t = re.sub(r'\[\d+\]', ' ', t)                  # CCEL footnote markers
    t = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', t)    # OCR end-of-line hyphenation
    for a, b in [('’', "'"), ('‘', "'"), ('“', '"'), ('”', '"'), ('—', ' '), ('–', ' '), ('--', ' ')]:
        t = t.replace(a, b)
    t = re.sub(r'[^\w\s]', ' ', t)
    return re.sub(r'\s+', ' ', t).strip().lower()


CORPUS = {k: norm((SRC / f).read_text(encoding='utf-8')) for k, f in FILES.items()}
QUOTE = re.compile(r'^> "(.+?)"\s*$', re.M)
bad = 0
for path in sys.argv[1:]:
    text = Path(path).read_text(encoding='utf-8')
    lines = text.split('\n')
    for i, line in enumerate(lines):
        m = QUOTE.match(line)
        if not m:
            continue
        q = m.group(1)
        # the attribution is on the next '> —' line
        who = None
        for j in range(i + 1, min(i + 4, len(lines))):
            if lines[j].startswith('> —'):
                for k in FILES:
                    if k.lower() in lines[j].lower().replace('g. campbell ', ''):
                        who = k
                if who is None:
                    who = 'other'
                break
        if who is None:
            continue                       # a quote block that is not a commentator quote (e.g. hymn)
        if who == 'other':
            print(f'SKIP {Path(path).name}:{i+1}: {q[:60]}'); continue
        parts = [p for p in re.split(r'\.\.\.|…', q) if len(norm(p)) >= 8]
        ok = all(norm(p) in CORPUS[who] for p in parts)
        print(('OK   ' if ok else 'MISS ') + f'{Path(path).name}:{i+1} [{who}] {q[:70]}')
        bad += (not ok)
sys.exit(1 if bad else 0)
