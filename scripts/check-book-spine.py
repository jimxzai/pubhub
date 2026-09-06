#!/usr/bin/env python3
"""Check whether a study book has a spine — and whether the reader can see it.

WHY THIS EXISTS
---------------
Every other checker in this repo asks "is this correct?". None asks
"does this book say something, in an order a reader can follow?"

That gap shipped. The Job volume passed every lint, every citation check,
the ledger check and a full driver run, scored 9.6/10 on the house rubric,
and was still missing the thing the rubric never measured: God's side of
the book — in what order He reveals Himself, and why that order. A reader
could finish 359 pages without ever being told where the book was going.

Worse, the same class of hole was already sitting in books considered
finished. A survey on 2026-09-05 found:

    isaiah    0 of 26 chapters closed by returning to Christ
    roman     0 of 16 chapters told the reader where they were in the argument
    john      21/21 on both per-chapter checks — but 0 of 5 part dividers
              carried the spine forward

Of 33 books, ONE (gospel-of-john) passed both per-chapter checks, and ONE
(job, and only after this was written) carried the spine on its dividers.
No book passed all four. That is the state of the shelf, not a rhetorical
flourish — run it yourself.

Each of those books had been through multiple editorial rounds. Prose in a
skill file saying "remember the spine" would not have caught them — the same
way "check the other templates" left the same bug in 56 of 57 templates until
lint-templates.sh made it a script. So: a script.

WHAT IT CHECKS (the mechanical half — see the limits section below)

  1. ORIENTATION   Does the book have a front chapter that states the spine:
                   the order of revelation / God's plan, not just a map of
                   the contents?
  2. DIVIDERS      Do the part-divider pages carry that spine forward, so it
                   is visible at every part opening rather than only once?
  3. COORDINATE    Does each chapter locate itself in the book's argument
                   (the 座標 line in 基督焦點)?
  4. RETURN        Does each chapter close by returning to Christ? The
                   ask-elder-wong skill calls this 「永不缺席的句號」 — the
                   never-absent full stop. It is absent constantly.

USAGE
    python3 scripts/check-book-spine.py books/bible/job
    python3 scripts/check-book-spine.py --all          # every book
    python3 scripts/check-book-spine.py --all --brief  # one line per book

Exit 1 if any check is below threshold, 0 otherwise.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKS = ROOT / "books" / "bible"

# A chapter file: NN-name.md where NN is 01..97. Everything starting 00 is
# orientation (00-overview, 00a-position, 00b-spine, 00c-revelation-order);
# 98-/99-/000- are appendices, index and preface. Counting orientation files
# as chapters made the first run of this script report a coordinate-line gap
# in 00-overview.md, which is not a chapter and has no business carrying one.
CHAPTER_RE = re.compile(r"^(\d{2})-")
APPENDIX_PREFIXES = ("98-", "99-", "000-", "00-", "00a", "00b", "00c", "00d")

# 1. Orientation: a front chapter that states the spine. Books name this
#    differently (John: 啟示的次序與組織; Job: 啟示的次序與神的計劃), so match
#    on the concepts rather than on one title.
SPINE_TITLE_TERMS = ("啟示的次序", "啟示的順序", "神的計劃", "神的計畫",
                     "救恩計劃", "全書的骨幹", "骨幹")

# 2. Divider spine marker, as emitted by scripts/build-<slug>-consolidated.sh
DIVIDER_SPINE_TERMS = ("啟示的次序", "骨幹座標", "全書骨幹")

# 4. Per-chapter return-to-Christ close. Books legitimately vary the wording
#    (a chapter where Job only falls silent should not be forced to claim he
#    "saw"), so match the shape, not one sentence.
# Cheap anchors first: a plain substring test is a C-level scan, the regex is
# not. Running the regex on every file made one book (life-of-christ, 37
# chapters) take 105 s on its own; gating on the anchor drops the whole-repo
# run to a couple of seconds.
RETURN_ANCHORS = ("你看見", "摀口")
RETURN_RE = re.compile(r"你看見[^\n]{0,10}了嗎|你看見了甚麼|你也摀口了嗎|"
                       r"你看見[^\n]{0,10}的信實")


def has_return(text):
    if not any(a in text for a in RETURN_ANCHORS):
        return False
    return RETURN_RE.search(text) is not None

THRESHOLD = 0.90       # per-chapter checks: fraction of chapters that must pass


def chapters(book_dir):
    out = []
    for p in sorted(book_dir.glob("*.md")):
        if p.name.startswith(APPENDIX_PREFIXES):
            continue
        if CHAPTER_RE.match(p.name):
            out.append(p)
    return out


def orientation_files(book_dir):
    return sorted(book_dir.glob("00[a-z]-*.md")) + sorted(book_dir.glob("00-*.md"))


# A few books' build scripts are not named after their directory.
SLUG_ALIASES = {"gospel-of-john": "gospel", "roman": "romans"}


def build_script_for(book_dir):
    slug_guesses = [book_dir.name,
                    SLUG_ALIASES.get(book_dir.name, book_dir.name),
                    book_dir.name.replace("gospel-of-", "")]
    for slug in slug_guesses:
        for pat in (f"build-{slug}-consolidated.sh", f"build-{slug}.sh"):
            p = ROOT / "scripts" / pat
            if p.exists():
                return p
    return None


def check_book(book_dir, brief=False):
    name = book_dir.name
    chs = chapters(book_dir)
    if not chs:
        return None

    # 1. orientation
    spine_file = None
    for p in orientation_files(book_dir):
        head = p.read_text(encoding="utf-8")[:600]
        if any(t in head for t in SPINE_TITLE_TERMS):
            spine_file = p.name
            break

    # 2. dividers
    bs = build_script_for(book_dir)
    divider_total = divider_spined = 0
    if bs:
        text = bs.read_text(encoding="utf-8")
        # Parse line-wise rather than with one big regex: an earlier version
        # used a "((?:[^"\\]|\\.)*)" description group that backtracked
        # catastrophically on some build scripts and hung the run.
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if "add_volume" not in line or line.lstrip().startswith("#"):
                continue
            mt = re.search(r'add_volume\s+"([^"]*)"', line)
            if not mt:
                continue
            title = mt.group(1)
            # description is the next quoted string, on this line or the next
            rest = line[mt.end():]
            md = re.search(r'"([^"]*)"', rest)
            if not md and i + 1 < len(lines):
                md = re.search(r'"([^"]*)"', lines[i + 1])
            desc = md.group(1) if md else ""
            # 卷首/卷末/附錄 dividers front the apparatus, not the argument.
            # An appendix is not a step in the order of revelation, and asking
            # one to carry a 「啟示的次序·第 N 步」 line would only produce a
            # sentence written to satisfy this script.
            if title.startswith(("卷首", "卷末", "附錄")):
                continue
            divider_total += 1
            if any(t in desc for t in DIVIDER_SPINE_TERMS):
                divider_spined += 1

    # 3 & 4. per chapter
    no_coord, no_return = [], []
    for p in chs:
        t = p.read_text(encoding="utf-8")
        if "座標" not in t:
            no_coord.append(p.name)
        if not has_return(t):
            no_return.append(p.name)

    n = len(chs)
    coord_ok = (n - len(no_coord)) / n
    return_ok = (n - len(no_return)) / n
    div_ok = (divider_spined / divider_total) if divider_total else None
    div_note = ("找不到 build script" if bs is None
                else "這本書的 build script 沒有分卷扉頁（add_volume）")

    passed = (spine_file is not None
              and coord_ok >= THRESHOLD and return_ok >= THRESHOLD
              and (div_ok is None or div_ok >= THRESHOLD))

    if brief:
        d = "n/a" if div_ok is None else f"{divider_spined}/{divider_total}"
        print(f"{'ok ' if passed else 'GAP'} {name:22s} "
              f"spine-chapter={'yes' if spine_file else 'NO ':3s} "
              f"dividers={d:>5s} "
              f"coord={n-len(no_coord)}/{n} return={n-len(no_return)}/{n}")
        return passed

    print(f"\n=== {name} ({n} chapters) ===")
    if spine_file:
        print(f"  [ok ] 骨幹章：{spine_file}")
    else:
        print("  [GAP] 沒有一章卷首在講啟示的次序／神的計劃。"
              "\n        讀者拿不到「這卷書要往哪裏去」的答案。"
              "\n        參 books/bible/gospel-of-john/00a-revelation-order.md"
              "\n        或 books/bible/job/00c-revelation-order.md")
    if div_ok is None:
        print(f"  [--- ] 無法檢查分卷扉頁：{div_note}")
    elif div_ok >= THRESHOLD:
        print(f"  [ok ] 分卷扉頁帶骨幹標記：{divider_spined}/{divider_total}")
    else:
        print(f"  [GAP] 分卷扉頁帶骨幹標記：{divider_spined}/{divider_total}"
              "\n        骨幹只寫在卷首一章，讀者翻到第五卷時早忘了。"
              "\n        在 add_volume 的描述裏加一行「啟示的次序·第N步」。")
    if coord_ok >= THRESHOLD:
        print(f"  [ok ] 各章座標行：{n-len(no_coord)}/{n}")
    else:
        print(f"  [GAP] 各章座標行：{n-len(no_coord)}/{n}　缺：{', '.join(no_coord[:6])}"
              + (" …" if len(no_coord) > 6 else ""))
    if return_ok >= THRESHOLD:
        print(f"  [ok ] 章末回到基督：{n-len(no_return)}/{n}")
    else:
        print(f"  [GAP] 章末回到基督：{n-len(no_return)}/{n}　缺：{', '.join(no_return[:6])}"
              + (" …" if len(no_return) > 6 else "")
              + "\n        ask-elder-wong 明定這是「永不缺席的句號」。")
    return passed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book_dir", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--brief", action="store_true")
    args = ap.parse_args()

    if args.all:
        results = []
        for d in sorted(BOOKS.iterdir()):
            if d.is_dir():
                r = check_book(d, brief=args.brief)
                if r is not None:
                    results.append(r)
        print(f"\n{sum(results)}/{len(results)} books have a visible spine.")
        return 0 if all(results) else 1

    if not args.book_dir:
        ap.error("give a book dir or --all")
    r = check_book(Path(args.book_dir), brief=args.brief)
    if r is None:
        sys.exit(f"no chapter files found in {args.book_dir}")
    return 0 if r else 1


if __name__ == "__main__":
    sys.exit(main())
