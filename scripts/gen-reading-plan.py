#!/usr/bin/env python3
"""Generate a daily reading plan for one book (roadmap item 5.3).

Each day gets whole chapters of the book (never part of one), so the plan never invents a verse split.
Chapters are weighted by their passage's verse span when it can be read from the chapter's header line
(e.g. 「約翰福音 3:1-36」 -> 36), else by 1 unit, and handed out in order so each day carries about the same load.

    python3 scripts/gen-reading-plan.py books/bible/gospel-of-john --days 30 [--out docs/reading-plans]

Writes <out>/<book>-<days>.json (for the reader site) and <out>/<book>-<days>.md (printable).
If the book has fewer chapters than days, the plan has one chapter per day (days are NOT padded).
"""
import argparse
import json
import re
import sys
from pathlib import Path


def passage_of(t):
    lines = t.splitlines()
    h1 = next((i for i, l in enumerate(lines) if l.startswith("# ")), 0)
    return next((l.strip() for l in lines[h1 + 1:h1 + 6] if re.search(r"\d+[:：]\d+", l) and not l.startswith(("**", ">"))), "")


def span(passage):
    m = re.search(r"(\d+)[:：](\d+)\s*[-–—]\s*(?:(\d+)[:：])?(\d+)", passage)
    if not m:
        return 1
    c1, v1, c2, v2 = int(m.group(1)), int(m.group(2)), m.group(3), int(m.group(4))
    return max(1, (v2 - v1 + 1) if not c2 else (int(c2) - c1) * 30 + v2 - v1 + 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book_dir")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--out", default="docs/reading-plans")
    a = ap.parse_args()
    book = Path(a.book_dir)
    if not book.is_dir() or a.days < 1:
        sys.exit("need a book directory and --days >= 1")

    chs = []
    for p in sorted(book.glob("[0-9][0-9]*-*.md")):
        if p.name.startswith("00") or not re.match(r"\d{2}[a-z]?-", p.name):
            continue
        t = p.read_text(encoding="utf-8")
        if "## 基督焦點" not in t:
            continue
        title = next((l[2:].strip() for l in t.splitlines() if l.startswith("# ")), p.name)
        ps = passage_of(t)
        chs.append({"file": p.name, "title": title, "passage": ps, "weight": span(ps)})
    if not chs:
        sys.exit("no chapters found")

    days = min(a.days, len(chs))
    total = sum(c["weight"] for c in chs)
    plan, i = [], 0
    for d in range(days):
        left_days = days - d
        remaining = len(chs) - i
        target = sum(c["weight"] for c in chs[i:]) / left_days
        todays, load = [], 0
        while i < len(chs):
            must_leave = left_days - 1          # chapters needed for the days after this one
            if todays and (len(chs) - i <= must_leave or load + chs[i]["weight"] / 2 > target):
                break
            todays.append(chs[i]); load += chs[i]["weight"]; i += 1
            if len(chs) - i <= must_leave:
                break
        plan.append(todays)
    assert i == len(chs) and all(plan), "plan must use every chapter and leave no empty day"

    dest = Path(a.out)
    dest.mkdir(parents=True, exist_ok=True)
    stem = f"{book.name}-{len(plan)}d"
    data = {"book": book.name, "requestedDays": a.days, "days": [
        {"day": n + 1, "chapters": [{"file": c["file"], "title": c["title"], "passage": c["passage"]} for c in d]}
        for n, d in enumerate(plan)]}
    (dest / f"{stem}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    md = [f"# {book.name} 讀經計劃（{len(plan)} 天）", ""]
    if days < a.days:
        md += [f"> 本書只有 {len(chs)} 章，所以計劃為 {days} 天，每天一章；不拆章，也不補空天。", ""]
    for n, d in enumerate(plan, 1):
        md += [f"- **第 {n} 天** ☐　" + "；".join(f"{c['passage'] or c['title']}（{c['title']}）" for c in d)]
    (dest / f"{stem}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"{stem}: {len(chs)} chapters over {len(plan)} days; busiest day {max(sum(c['weight'] for c in d) for d in plan)} units "
          f"vs average {total / len(plan):.0f}")


if __name__ == "__main__":
    main()
