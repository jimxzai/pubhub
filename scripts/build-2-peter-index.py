#!/usr/bin/env python3
"""Fill real printed page numbers into books/bible/2-peter/98-appendix-indices.md.

Why a script and not hand-maintenance: an index whose locators are chapter
names ("見 01 章") is not an index — in a 100+ page book the reader still has
to hunt. Real page numbers can only come from the built PDF, and the index
lives *inside* that PDF, so there is a chicken-and-egg problem.

The three-pass contract that makes it safe:

  pass 1  scripts/build-2-peter-consolidated.sh     (locator cells hold 「—」)
  pass 2  python3 scripts/build-2-peter-index.py    (「—」 → printed folios)
  pass 3  scripts/build-2-peter-consolidated.sh     (final PDF)

Substituting 「—」 for a short locator inside a narrow table cell cannot reflow
a CJK table row, so pass 3 keeps pass 1's pagination and the numbers written in
pass 2 stay true. Run driver.sh afterwards and confirm the page count is
unchanged; `--check` re-verifies the locators without writing.

TWO THINGS THIS GOT WRONG BEFORE — both silent, both worth keeping written down:

1. *Searching the whole PDF for each reference.* 「1:5-7」 then matched the
   contents page, the overview's 段落導讀 table, the infographic spread and the
   reading plan, so nearly every row listed the same handful of pages and no row
   pointed at the exposition. An index must locate discussion, not occurrences —
   hence OWNERS below, and a search scoped to the owning chapter.

2. *Finding chapter openings by heading substring.* Body text cross-references
   its own chapters ("見卷末〈附錄：參考資料〉"), so 「附錄：參考資料」 matched
   inside chapter 1 and the derived ranges came out scrambled and overlapping —
   with no error, just a wrong index. Chapter bounds now come from the PDF's own
   hyperref outline, which cannot be spoofed by prose.

Printed folio ≠ PDF page index (cover, copyright and contents are unnumbered),
so the offset is measured from the page furniture rather than assumed.
"""
import re
import subprocess
import sys
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "output" / "2-peter-consolidated.pdf"
INDEX_MD = ROOT / "books" / "bible" / "2-peter" / "98-appendix-indices.md"

# key -> distinctive substring of the chapter's outline title
CHAPTER_TITLES = {
    "000": "前言 (Preface)",
    "00": "彼得後書概覽",
    "00a": "使徒的遺言",
    "00b": "全書的骨幹",
    "study": "全書領受總綱",
    "01": "1 真知識的根基",
    "02": "2 假教師的警告",
    "03": "3 主的日子",
    "99": "永恆的日子——彼得後書的最後一句話",
    "98": "附錄：經文與主題索引",
    "96": "附錄：彼得後書讀經計劃",
    "ref": "附錄：參考資料",
    "999": "跋 (Afterword)",
}

# Which chapter(s) actually expound each entry. Carried over from the
# hand-built chapter column this index used before it carried page numbers.
OWNERS = {
    "1:1-21": ["01"], "1:1-2": ["01"], "1:3-4": ["01"], "1:5-7": ["01"],
    "1:8-11": ["01"], "1:12-15": ["01"], "1:16-18": ["01"], "1:19-21": ["01"],
    "2:1-22": ["02"], "2:1-3": ["02"], "2:4-10a": ["02"], "2:10b-16": ["02"],
    "2:17-22": ["02"],
    "3:1-18": ["03"], "3:1-2": ["03"], "3:3-7": ["03"], "3:8-9": ["03"],
    "3:10-13": ["03"], "3:14-16": ["03"], "3:17-18": ["03"],
    "彼前 1:3": ["study"], "彼前 4:11": ["99"],
    "猶 4": ["02", "00a"], "猶 6-11": ["02", "00a"], "猶 12-13": ["02"],
    "創 1:1-3, 9": ["99"], "詩 90:1-4, 12": ["03"], "詩 97:1-6": ["01"],
    "詩 119:105-112": ["01"], "詩 1": ["02"], "摩 8:11-12": ["01"],
    "賽 65:17": ["99"], "代上 29:10-11": ["99"],
    "太 17:1-8；可 9:2-8；路 9:28-36": ["01"],
    "太 24:43；帖前 5:2；啟 3:3, 16:15": ["03"],
    "太 26:72": ["00a"], "約 21:18-19": ["01", "00a"], "徒 20": ["00a"],
    "徒 27:15, 17": ["01"], "提後 3:16；4:6-8": ["01", "00a"],
    "提前 6:20": ["00b"], "啟 2:28；22:16": ["01"], "啟 21:1": ["99"],
}


def page_texts():
    out = subprocess.run(
        ["pdftotext", "-layout", str(PDF), "-"],
        capture_output=True, text=True, check=True,
    ).stdout
    return {i: t for i, t in enumerate(out.split("\f"), start=1)}


def outline_starts(reader):
    """{key: pdf_page} for each chapter, from the PDF's hyperref outline.

    Unnumbered front-matter chapters can carry a destination that resolves to
    page 1; when that happens the entry's first child section is the reliable
    anchor, so a level-1 entry's page is taken as min(own, first child) once
    the obviously-wrong page-1 case is excluded.
    """
    flat = []           # [(depth, title, page)]

    def walk(items, depth=0):
        for it in items:
            if isinstance(it, list):
                walk(it, depth + 1)
                continue
            try:
                pg = reader.get_destination_page_number(it) + 1
            except Exception:
                continue
            flat.append((depth, it.title, pg))

    walk(reader.outline)

    starts = {}
    for i, (depth, title, pg) in enumerate(flat):
        if depth != 0:
            continue
        for key, needle in CHAPTER_TITLES.items():
            if key in starts or needle not in title:
                continue
            if pg <= 1:
                # broken destination — use the first following child entry
                child = next((p for d, _, p in flat[i + 1:] if d > 0), None)
                pg = child if child else pg
            starts[key] = pg
    return starts


def folio_offset(pages):
    """printed folio = pdf_page - offset, measured from the page furniture."""
    for n in sorted(pages):
        head = "\n".join(pages[n].splitlines()[:2])
        m = re.search(r"(?:^|\s)(\d{1,3})(?:\s|$)", head)
        if m:
            folio = int(m.group(1))
            if 1 <= folio < n:
                return n - folio
    raise SystemExit("could not measure the folio offset from the page headers")


def ref_pattern(ref):
    r = re.sub(r"\s+", "", ref)
    parts = [re.escape(c).replace(re.escape("-"), "[-–—]") for c in r]
    return re.compile(r"\s*".join(parts))


def locate(ref, owners, pages, ranges):
    """(pages_with_the_reference_printed, chapter_opening_pages).

    Kept separate so the two can be typeset differently. A row whose passage
    the chapter expounds without ever printing that exact verse range (「2:4-10a」
    is discussed throughout chapter 2 but the body writes 「2:4-9」) still needs a
    locator — but presenting a chapter-opening fallback as though it were a
    precise hit would quietly mislead the reader, so it is marked 「起」.
    """
    pat = ref_pattern(ref)
    exact, opening = [], []
    for key in owners:
        if key not in ranges:
            continue
        lo, hi = ranges[key]
        found = [n for n in range(lo, min(hi, max(pages)) + 1)
                 if pat.search(pages.get(n, ""))]
        if found:
            exact += found
        else:
            opening.append(lo)
    return sorted(set(exact)), sorted(set(opening))


def main():
    check_only = "--check" in sys.argv
    if not PDF.exists():
        sys.exit(f"no PDF at {PDF} — run scripts/build-2-peter-consolidated.sh first")

    pages = page_texts()
    reader = PdfReader(str(PDF))
    starts = outline_starts(reader)
    missing = [k for k in CHAPTER_TITLES if k not in starts]
    if missing:
        sys.exit(f"chapter opening(s) absent from the PDF outline: {missing}")

    ordered = sorted(starts.items(), key=lambda kv: kv[1])
    ranges = {}
    for i, (k, s) in enumerate(ordered):
        end = ordered[i + 1][1] - 1 if i + 1 < len(ordered) else max(pages)
        ranges[k] = (s, end)

    off = folio_offset(pages)
    lines = INDEX_MD.read_text(encoding="utf-8").split("\n")
    filled = stale = skipped = 0

    for i, line in enumerate(lines):
        if not line.startswith("|") or line.startswith("|--"):
            continue
        cells = line.split("|")
        if len(cells) < 4:
            continue
        ref = cells[1].strip()
        owners = OWNERS.get(ref)
        if not owners:
            if re.search(r"\d", ref) and cells[2].strip() == "—":
                skipped += 1
                print(f"  no owner declared, left as 「—」: {ref}")
            continue
        exact, opening = locate(ref, owners, pages, ranges)
        ex = sorted({p - off for p in exact if p - off >= 1})
        op = sorted({p - off for p in opening if p - off >= 1})
        if not ex and not op:
            skipped += 1
            continue
        parts = ["、".join(str(f) for f in ex[:3]) + (" 等" if len(ex) > 3 else "")] if ex else []
        parts += [f"{f} 起" for f in op]
        locator = "；".join(parts)
        current = cells[2].strip()
        if check_only:
            if current != locator:
                stale += 1
                print(f"  stale: {ref}  記為「{current}」 實為「{locator}」")
            continue
        if current != locator:
            cells[2] = f" {locator} "
            lines[i] = "|".join(cells)
            filled += 1

    if check_only:
        print(f"{stale} stale locator(s)")
        sys.exit(1 if stale else 0)

    INDEX_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"  folio offset: pdf page − {off};  wrote {filled} locator(s), {skipped} skipped")


if __name__ == "__main__":
    main()
