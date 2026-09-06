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


# Two layouts are in use for 歷代注疏, and only one puts the commentator in the
# ### heading:
#
#   A. ### 摩根 (G. Campbell Morgan)          -- name in the heading
#   B. ### 教父時期                            -- heading is a PERIOD, and the
#      **貴格利一世 (Gregory the Great)**：       commentator is a bold run inside
#
# Reading only layout A made this script blind to every book using B. On the
# Job volume that produced 30 confident "disagreements" that were all false:
# it reported 亨利 in 16 chapters where the book has him in 31, and 貴格利 in 4
# where the book has him in 18 -- and chapter 29, reported as having no Morgan
# quotes at all, carries verbatim Gregory and Henry quotes on the page. A
# checker that cannot see half the shelf's markup is worse than no checker,
# because its output looks like evidence.
# A commentator marker in layout B is a bold name ALONE on its line, optionally
# followed by a colon. Both qualifiers are load-bearing. Matching any bold run
# broke two ways at once: 「**惡人為何存活**：亨利答21:7說…」 is a bold sub-heading
# with prose after it, and treating it as a new owner cut Henry's block off at
# zero quotes; and in books that use layout A, bold emphasis in ordinary prose
# started claiming quotes that belong to nobody (2-peter went from 1 reported
# disagreement to 5). The length cap keeps a bolded sentence from passing as a
# name.
BOLD_NAME_RE = re.compile(r"^\*\*([^*\n]{2,60}?)\*\*", re.M)
# What separates a commentator marker from a bold sub-heading is not its
# position on the line -- 「**馬太·亨利 (Matthew Henry)**：亨利答21:7說…」 runs on --
# but the house convention that a commentator is always given with the English
# form of the name. So: a marker's bold text contains a Latin letter, and a
# Chinese bold sub-heading such as 「**惡人為何存活**」 does not. Requiring the
# name to sit alone on its line instead lost four of Gregory's eighteen
# chapters; matching any bold run at all mis-attributed quotes in 2-peter.
LATIN_RE = re.compile(r"[A-Za-z]")
# Layout B only ever appears inside the 歷代注疏 section. Restricting to it also
# keeps 00-overview.md's bold field labels (**作者**, **主題**) out of the scan.
COMMENTARY_SECTION_RE = re.compile(r"^## .*歷代注疏.*$", re.M)


def _count(body):
    return len(QUOTE_RE.findall(body)), len(CJK_QUOTE_RE.findall(body))


def _add(out, num, n, cjk):
    if n or cjk:
        prev_n, prev_c = out.get(num, (0, 0))
        out[num] = (prev_n + n, prev_c + cjk)


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
        found_in_a = False
        for i, h in enumerate(heads):
            if commentator not in h.group(1):
                continue
            end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
            nxt = text.find("\n## ", h.end())
            if nxt != -1:
                end = min(end, nxt)
            n, cjk = _count(text[h.end():end])
            if n or cjk:
                found_in_a = True
            _add(out, num, n, cjk)
        # Fall through to layout B when a heading matched but held no quotes.
        # Chapter 4 of Job carries three verbatim Henry quotes under a layout-B
        # bold name, and also a section headed 「亨利對本章的總評」 -- commentary
        # ABOUT Henry, with no quotes in it. Treating any heading that contains
        # the name as proof of layout A let that empty section claim the
        # chapter, and the three quotes on the page went uncounted.
        if found_in_a:
            continue
        # Layout B: bold commentator names inside period-titled ### sections.
        sec = COMMENTARY_SECTION_RE.search(text)
        if not sec:
            continue
        sec_end = text.find("\n## ", sec.end())
        body_all = text[sec.end():sec_end if sec_end != -1 else len(text)]
        names = [b for b in BOLD_NAME_RE.finditer(body_all)
                 if LATIN_RE.search(b.group(1))]
        for j, b in enumerate(names):
            if commentator not in b.group(1):
                continue
            # the block runs to the next commentator marker, or the next ###
            end = names[j + 1].start() if j + 1 < len(names) else len(body_all)
            nxt = body_all.find("\n### ", b.end())
            if nxt != -1:
                end = min(end, nxt)
            n, cjk = _count(body_all[b.end():end])
            _add(out, num, n, cjk)
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
