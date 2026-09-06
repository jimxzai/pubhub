#!/usr/bin/env python3
"""Standardise each chapter's 體例說明 (citation-convention notice) to match reality.

WHY THIS EXISTS
---------------
2026-08-31, Gospel of Luke: the notice box that opens every chapter's 歷代注疏
section existed in SEVEN different wordings across 24 chapters, and fourteen of
them declared 「帶引號引文均為編者自英文原著的中譯」 -- "anything in quotation marks is
the editor's Chinese rendering of the English original". That was written when
the chapters carried Chinese only. They now carry the English originals too, so
the notice told readers the opposite of what the page shows. One chapter still
said it had no verifiable transcript at all, several hundred words above two
verbatim quotes.

A notice about honesty that is itself out of date is worse than no notice. This
script derives the right notice from what the chapter actually contains, so the
two cannot drift apart again.

WHAT IT DOES
    For each chapter file, looks at the 歷代注疏 section and asks: does it
    contain any `> "English"` verbatim quote?
      yes -> notice states that Fathers/Reformed are summarised, and that
             anything in quotation marks with an English original is verbatim
             and has been checked against the source
      no  -> notice states the whole section is summary, nothing is verbatim
    Then rewrites the existing notice block in place.

USAGE
    python3 scripts/normalize-commentary-notice.py <book-dir> [--dry-run]
"""
import argparse
import re
import sys
from pathlib import Path

SECTION = "## 歷代注疏"

# The notice ends by telling the reader where the sources are listed. That
# cross-reference has to name the section this book actually contains: the
# shelf uses at least four titles for it -- 引用出處總表, 參考資料,
# 引用出處與核校說明, 參考資料與引文帳目 -- and a hardcoded one sent readers of
# every other book to a section that is not there. Derive it from the book's own
# appendix; fall back only when there is no appendix to read.
DEFAULT_APPENDIX_TITLE = "附錄：引用出處總表"


def appendix_title(book_dir):
    f = Path(book_dir) / "99-appendix-references.md"
    if f.exists():
        m = re.search(r"^# (.+?)(?:\s*\(.*\))?\s*$", f.read_text(encoding="utf-8"),
                      re.M)
        if m:
            return m.group(1).strip()
    return DEFAULT_APPENDIX_TITLE


def notices(title):
    ref = f"見卷末《{title}》。"
    with_quotes = (
        "> **體例說明**：教父與改革宗一節為解經者**立場的綜述**，不加引號、不作逐字引用；\n"
        "> 凡加引號並附英文原文者，均為**逐字引文**，已與原著或逐字講道稿核校，\n"
        f"> 中譯附於原文之後。各條出處與核校方式，{ref}"
    )
    summary_only = (
        "> **體例說明**：本節全為歷代解經者**立場的綜述**，不加引號、不作逐字引用；\n"
        "> 凡未能核校到可逐字引用之原文者，一律以綜述呈現，不以引號冒充原文。\n"
        f"> 各條出處與核校方式，{ref}"
    )
    return with_quotes, summary_only


def rewrite(text, with_quotes=None, summary_only=None):
    """Replace the notice block at the head of 歷代注疏. Returns (new_text, kind)."""
    WITH_QUOTES, SUMMARY_ONLY = (with_quotes, summary_only) if with_quotes \
        else notices(DEFAULT_APPENDIX_TITLE)
    i = text.find(SECTION)
    if i == -1:
        return text, None
    # section body ends at the next '## ' heading
    j = text.find("\n## ", i + 1)
    body_end = j if j != -1 else len(text)
    body = text[i:body_end]

    has_quote = bool(re.search(r'^> "', body, re.M))
    notice = WITH_QUOTES if has_quote else SUMMARY_ONLY
    kind = "verbatim" if has_quote else "summary-only"

    # the existing notice is the run of '>' lines immediately after the heading
    m = re.match(r"(## 歷代注疏[^\n]*\n\n)((?:>[^\n]*\n)+)", body)
    if not m:
        return text, None
    new_body = body[: m.end(1)] + notice + "\n" + body[m.end(2):]
    return text[:i] + new_body + text[body_end:], kind


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book_dir")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    title = appendix_title(args.book_dir)
    wq, so = notices(title)
    print(f"  sources appendix: 〈{title}〉")

    changed = 0
    for f in sorted(Path(args.book_dir).glob("[0-9][0-9]-*.md")):
        old = f.read_text(encoding="utf-8")
        new, kind = rewrite(old, wq, so)
        if kind is None:
            print(f"  {f.name}: no 歷代注疏 notice found — skipped")
            continue
        if new != old:
            changed += 1
            print(f"  {f.name}: -> {kind}")
            if not args.dry_run:
                f.write_text(new, encoding="utf-8")
        else:
            print(f"  {f.name}: already correct ({kind})")
    print(f"\n{changed} file(s) {'would be ' if args.dry_run else ''}updated")


if __name__ == "__main__":
    main()
