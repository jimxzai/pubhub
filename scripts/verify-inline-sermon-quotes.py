#!/usr/bin/env python3
"""Verify MacArthur quotes written INLINE in prose against the sermons the ledger names.

verify-sermon-quotes.py checks quotes laid out as `> "English"` blocks followed by a `> — ... sermon CODE`
line. Some books (Hebrews) instead quote him inside a paragraph:

    麥克阿瑟在 *Jesus Christ, the Perfect Priest* 的講章指出 ...："A priest must be a man, ..."

and name the sermons once, in a table in the ledger (99-appendix-references.md) that maps each chapter to
its sermon codes. This tool reads that table, takes every double-quoted English string of 25+ characters
in a chapter's MacArthur passage, and requires it to appear in at least one of THAT chapter's sermons
(a quote may join two passages with an ellipsis; each part must appear).

    python3 scripts/verify-inline-sermon-quotes.py books/bible/hebrews [--cache /tmp/sermon-cache]

Exit 1 if any quote is not found, or if a chapter quotes MacArthur but the ledger lists no sermon for it.
Transcripts are fetched from gty.org and cached; matching ignores case, punctuation and macron vowels.
"""
import argparse
import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("vsq", HERE / "verify-sermon-quotes.py")
vsq = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vsq)

MAC_BLOCK = re.compile(
    r"(?:^### [^\n]*(?:麥克阿瑟|MacArthur)[^\n]*|\*\*約翰·麥克阿瑟[^\n]*)\n(.*?)(?=^## |^### |\Z)", re.S | re.M
)
CODE_IN_URL = re.compile(r"/sermons(?:-library)?/(\d{2}-\d{1,3}|\d{3,5})/")


def ledger_map(text):
    """chapter -> [codes], and the set of sermon titles, from the MacArthur section's table."""
    start = re.search(r"^## [^\n]*(?:John MacArthur|麥克阿瑟)[^\n]*$", text, re.M)
    if not start:
        return {}, set()
    nxt = re.search(r"^## ", text[start.end():], re.M)
    sec = text[start.end(): start.end() + nxt.start()] if nxt else text[start.end():]
    chapters, titles = {}, set()
    for row in sec.splitlines():
        if not row.startswith("|"):
            continue
        codes = CODE_IN_URL.findall(row)
        if not codes:
            continue
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        chap = next((int(c) for c in (cells[-1], cells[0]) if re.fullmatch(r"0*\d{1,2}", c)), None)
        if chap is None:
            continue
        chapters.setdefault(chap, [])
        chapters[chap] += [c for c in codes if c not in chapters[chap]]
        titles |= {t.strip() for t in re.findall(r"\*([^*]+)\*", cells[0])}
    return chapters, titles


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book_dir")
    ap.add_argument("--ledger", default="99-appendix-references.md")
    ap.add_argument("--cache", default="/tmp/sermon-cache")
    args = ap.parse_args()

    book = Path(args.book_dir)
    ledger = book / args.ledger
    if not ledger.exists():
        print(f"no ledger at {ledger}")
        return 0
    chap_codes, titles = ledger_map(ledger.read_text(encoding="utf-8"))
    if not chap_codes:
        print("ledger has no MacArthur sermon table this tool can read")
        return 0

    ok = bad = 0
    for f in sorted(book.glob("[0-9][0-9]*-*.md")):
        n = int(re.match(r"(\d+)", f.name).group(1))
        text = f.read_text(encoding="utf-8")
        quotes = []
        for m in MAC_BLOCK.finditer(text):
            quotes += [q for q in re.findall(r'"([^"\n]{25,}?)"', m.group(1)) if q.strip() not in titles]
        if not quotes:
            continue
        codes = chap_codes.get(n, [])
        hays = [h for h in (vsq.fetch(c, args.cache) for c in codes) if h]
        for q in quotes:
            frags = [x for x in re.split(r"\.\.\.|…", q) if len(vsq.norm(x)) > 12] or [q]
            if hays and all(any(vsq.norm(fr) in h for h in hays) for fr in frags):
                ok += 1
            else:
                bad += 1
                why = f"not in {codes}" if codes else "the ledger lists no sermon for this chapter"
                print(f"  MISSING ch{n:02d} ({why}): {q[:90]}")
    print(f"\ninline MacArthur quotes: verified {ok}, missing {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
