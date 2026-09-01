#!/usr/bin/env python3
"""Check that a book's citation ledger matches what its chapters actually contain.

WHY THIS EXISTS
---------------
2026-08-31, Gospel of Luke: `99-appendix-references.md` is the book's honesty
ledger -- it says of itself 「這份總表就是這句話的帳目」, the account book for the
promise 「不編造一段出處」. It declared that all 24 chapters' Morgan sections were
要旨綜述 with no verbatim quotation. Eight chapters were in fact carrying 29
quoted English passages.

Nothing caught it for months, because nothing could: the quotes were real
markdown, the build was clean, and the appendix was internally coherent prose.
The only way to catch a ledger that disagrees with its own book is to compare
them mechanically.

WHAT IT CHECKS
    For each commentator heading (default 摩根 and 麥克阿瑟):
      * which chapters actually carry `> "..."` verbatim quotes
      * which chapters the appendix LISTS as verbatim-verified
      * which chapters the appendix LISTS as summary-only
    and reports every disagreement in either direction:
      UNDECLARED  chapter has verbatim quotes the ledger doesn't acknowledge
                  (the Luke failure -- the dangerous direction, it means the
                  book quotes further than it admits to having verified)
      OVERCLAIMED ledger lists a chapter as verbatim that has no quotes
      MISLISTED   chapter appears in the summary list but carries quotes

Chapter numbers are read from filenames (NN-*.md) and from CJK numerals in the
appendix's 「第 N 章」 lists.

USAGE
    python3 scripts/check-citation-ledger.py books/bible/gospel-of-luke
    python3 scripts/check-citation-ledger.py <dir> --ledger 99-appendix-references.md

Exit 1 on any disagreement.
"""
import argparse
import re
import sys
from pathlib import Path

HEADING_RE = re.compile(r"^### (.+?)$", re.M)
QUOTE_RE = re.compile(r'^> "', re.M)
# Some citations render only a Chinese translation in CJK brackets, with no
# English original. They ARE citations (they carry a real sermon code), but a
# reader cannot check a translation against a source without the original --
# so they are counted, and reported separately as a verifiability gap.
CJK_QUOTE_RE = re.compile(r'^> 「', re.M)


def chapters_with_quotes(book_dir, commentator):
    """{chapter number: quote count} for chapters quoting this commentator."""
    out = {}
    for f in sorted(Path(book_dir).glob("[0-9][0-9]-*.md")):
        m = re.match(r"(\d+)", f.name)
        if not m:
            continue
        num = int(m.group(1))
        text = f.read_text(encoding="utf-8")
        heads = list(HEADING_RE.finditer(text))
        for i, h in enumerate(heads):
            if commentator not in h.group(1):
                continue
            end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
            nxt = text.find("\n## ", h.end())
            if nxt != -1:
                end = min(end, nxt)
            body = text[h.end():end]
            n = len(QUOTE_RE.findall(body))
            cjk = len(CJK_QUOTE_RE.findall(body))
            if n or cjk:
                prev_n, prev_c = out.get(num, (0, 0))
                out[num] = (prev_n + n, prev_c + cjk)
    return out


def ledger_lists(ledger_text, commentator):
    """(verbatim_chapters, summary_chapters) as declared by the appendix.

    The lists are written CJK-style -- 「第 2、3、4、7 章」 -- so only the first
    number carries 第 and only the last is followed by 章. Parse the run, not
    individual 第N章 tokens (an earlier version did that and silently found
    nothing, which is exactly the kind of vacuous pass this script exists to
    prevent).
    """
    # isolate this commentator's ## section
    heads = [(m.start(), m.group(0)) for m in re.finditer(r"^## .+$", ledger_text, re.M)]
    section = ledger_text
    for i, (pos, line) in enumerate(heads):
        if commentator in line:
            end = heads[i + 1][0] if i + 1 < len(heads) else len(ledger_text)
            section = ledger_text[pos:end]
            break

    def run_after(marker):
        """Chapter numbers in the 第 N、M、… 章 run following a marker."""
        i = section.find(marker)
        if i == -1:
            return set()
        tail = section[i + len(marker): i + len(marker) + 400]
        m = re.search(r"第\s*([\d\s、,，]+?)章", tail)
        return {int(x) for x in re.findall(r"\d+", m.group(1))} if m else set()

    summary = run_after("要旨綜述的章")

    # verbatim: table rows carrying 第 N 章, minus anything in the summary run
    sum_i = section.find("要旨綜述的章")
    head_part = section[:sum_i] if sum_i != -1 else section
    verbatim = {int(m.group(1))
                for m in re.finditer(r"^\|[^|\n]*第\s*(\d+)\s*章", head_part, re.M)}
    verbatim |= {int(m.group(1))
                 for m in re.finditer(r"第\s*(\d+)\s*章", head_part)} - summary
    return verbatim - summary, summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book_dir")
    ap.add_argument("--ledger", default="99-appendix-references.md")
    ap.add_argument("--commentator", action="append",
                    default=None, help="heading substring (repeatable)")
    args = ap.parse_args()
    commentators = args.commentator or ["摩根", "麥克阿瑟"]

    ledger_path = Path(args.book_dir) / args.ledger
    if not ledger_path.exists():
        sys.exit(f"no ledger at {ledger_path}")
    ledger_text = ledger_path.read_text(encoding="utf-8")

    problems = 0
    for c in commentators:
        actual = chapters_with_quotes(args.book_dir, c)
        declared_v, declared_s = ledger_lists(ledger_text, c)
        print(f"\n=== {c} ===")
        eng_total = sum(v[0] for v in actual.values())
        cjk_total = sum(v[1] for v in actual.values())
        print(f"  chapters actually quoting          : "
              f"{sorted(actual) if actual else '(none)'}  "
              f"({eng_total} with English original"
              f"{f', {cjk_total} Chinese-only' if cjk_total else ''})")
        print(f"  ledger says verbatim-verified      : {sorted(declared_v) or '(none)'}")
        print(f"  ledger says summary-only           : {sorted(declared_s) or '(none)'}")

        for ch in sorted(set(actual) - declared_v):
            print(f"  UNDECLARED  ch{ch:02d} has {sum(actual[ch])} quote(s) "
                  f"not listed as verified in the ledger")
            problems += 1
        for ch in sorted(declared_v - set(actual)):
            print(f"  OVERCLAIMED ch{ch:02d} listed as verbatim-verified but has no quotes")
            problems += 1
        for ch, (n_eng, n_cjk) in sorted(actual.items()):
            if n_cjk and not n_eng:
                print(f"  NO-ORIGINAL ch{ch:02d} cites {n_cjk} quote(s) in Chinese only; "
                      f"a reader cannot check a translation without the original")
                problems += 1

        for ch in sorted(declared_s & set(actual)):
            print(f"  MISLISTED   ch{ch:02d} is in the summary-only list but carries "
                  f"{sum(actual[ch])} quote(s)")
            problems += 1

    print(f"\n{'='*60}")
    print("ledger matches the book" if not problems
          else f"{problems} disagreement(s) between ledger and chapters")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
