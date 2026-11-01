#!/usr/bin/env python3
"""check-all — run every per-book check in one command.

    python3 scripts/check-all.py ruth                 # one book (directory name or build slug)
    python3 scripts/check-all.py books/bible/ruth jude
    python3 scripts/check-all.py --all                # every book that has a build script
    python3 scripts/check-all.py --all --include-unmapped   # ...plus legacy/alternate directories
    python3 scripts/check-all.py --all --status       # ...and rewrite docs/library-status.md

Each check is one of the repo's own scripts, run exactly as .claude/skills/eat-bible/SKILL.md
describes. Result per check:

    PASS    exit 0
    REVIEW  lint-scripture-text found *candidates*; its own output says each must be confirmed
            against a second source, so they are listed but do not fail the run
    FAIL    non-zero exit
    n/a     the check does not apply (e.g. no citation ledger in this book)

Exit status is 1 if any check FAILs. Checks that need per-book arguments (verify-citations
--source, verify-prose-citations --self, the PDF build) are not run here; they are listed at the
end so nobody believes "check-all passed" means "the book is done".
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKS = ROOT / "books" / "bible"
SCRIPTS = ROOT / "scripts"
SCORES = ROOT / "docs" / "scores"
BASELINES = ROOT / ".claude" / "skills" / "eat-bible" / "baselines.tsv"

# name, script, severity ("hard" fails the run; "review" is advisory)
CHECKS = [
    ("spine", "check-book-spine.py", "hard"),
    ("markup", "lint-chapter-markup.py", "hard"),
    ("scripture", "lint-scripture-text.py", "review"),
    ("sermons", "verify-sermon-quotes.py", "hard"),
    ("ledger", "check-citation-ledger.py", "hard"),
]
# check-citation-ledger checks Morgan and MacArthur by default. A book that uses other
# commentators must be checked against ITS commentators, or the default run reads another
# commentator's chapter list as Morgan's and reports every chapter as overclaimed. Each entry
# below was run and returns "ledger matches the book" against the named commentators. Only add a
# book here after running it by hand; never to silence a failure.
LEDGER_COMMENTATORS: dict[str, list[str]] = {
    "joshua": ["加爾文", "亨利", "梅爾", "司布真"],
    "leviticus": ["波納", "亨利", "麥克阿瑟"],
    "proverb": ["布祺斯", "亨利"],  # its ledger states MacArthur is cited in none of the 31 chapters
    "numbers": ["摩根"],  # its ledger states MacArthur is not used
}

NOT_RUN = [
    "verify-citations.py --source <work.txt>   (needs the commentary source file)",
    "verify-prose-citations.py --self <char>   (needs the book's self-reference character)",
    "driver.sh <slug>                          (builds the PDF; run it for layout, glyphs, fonts)",
    "reading the PDF pages                     (no script can see everything)",
]


def book_slug_map() -> dict[str, str]:
    """build-<slug>-consolidated.sh -> the books/bible/<dir> it assembles."""
    out: dict[str, str] = {}
    for sh in sorted(SCRIPTS.glob("build-*-consolidated.sh")):
        slug = sh.name[len("build-"):-len("-consolidated.sh")]
        for m in re.finditer(r"books/bible/([A-Za-z0-9_.\-]+)", sh.read_text(encoding="utf-8", errors="ignore")):
            if m.group(1) not in ("published", "sources"):
                out[slug] = m.group(1)
                break
    return out


def resolve(arg: str, slug_to_dir: dict[str, str]) -> Path | None:
    p = Path(arg)
    if p.is_dir():
        return p.resolve()
    if (BOOKS / arg).is_dir():
        return BOOKS / arg
    if arg in slug_to_dir and (BOOKS / slug_to_dir[arg]).is_dir():
        return BOOKS / slug_to_dir[arg]
    lower = {d.name.lower(): d for d in BOOKS.iterdir() if d.is_dir()}
    return lower.get(arg.lower())


def run_check(book: Path, name: str, script: str, severity: str) -> tuple[str, str, str]:
    extra: list[str] = []
    if name == "ledger":
        for c in LEDGER_COMMENTATORS.get(book.name.lower(), []):
            extra += ["--commentator", c]
    try:
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS / script), str(book), *extra],
            capture_output=True, text=True, timeout=300, cwd=ROOT,
        )
    except subprocess.TimeoutExpired:
        return name, "FAIL", "timed out after 300 s"
    text = (proc.stdout + proc.stderr).strip()
    last = next((l.strip() for l in reversed(text.splitlines()) if l.strip()), "")
    if proc.returncode != 0:
        # Prefer the line that says what was found over a trailing footnote.
        found = next((l.strip() for l in text.splitlines()
                      if re.search(r"\d+ finding|\[GAP|mismatch|missing|unresolved: [1-9]|DRIFT", l)), "")
        last = found or last
    low = text.lower()
    if "no chapter files found" in low:
        return name, "n/a", "no chapter files"
    if name == "ledger" and "no ledger" in low:
        return name, "n/a", "no citation ledger"
    if proc.returncode == 0:
        return name, "PASS", last
    return name, ("REVIEW" if severity == "review" else "FAIL"), last


def spine_counts(book: Path) -> tuple[int, int, int]:
    """ok, total checkable, unchecked — from check-book-spine's own output."""
    proc = subprocess.run([sys.executable, str(SCRIPTS / "check-book-spine.py"), str(book)],
                          capture_output=True, text=True, timeout=120, cwd=ROOT)
    lines = (proc.stdout + proc.stderr).splitlines()
    ok = sum(1 for l in lines if l.strip().startswith("[ok"))
    gap = sum(1 for l in lines if l.strip().startswith("[GAP"))
    unchecked = sum(1 for l in lines if l.strip().startswith("[---"))
    return ok, ok + gap, unchecked


def check_book(book: Path) -> dict:
    with ThreadPoolExecutor(max_workers=len(CHECKS)) as pool:
        results = list(pool.map(lambda c: run_check(book, *c), CHECKS))
    return {"book": book, "results": {n: (s, d) for n, s, d in results}}


# ---------------------------------------------------------------- status table

def read_baselines() -> dict[str, dict]:
    rows: dict[str, dict] = {}
    if not BASELINES.exists():
        return rows
    for line in BASELINES.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) >= 5:
            rows[parts[0]] = {"pages": parts[1], "glyphs": parts[2], "overfull": parts[3], "recorded": parts[4]}
    return rows


# Score files were named before the directory names settled; these are the only mismatches.
SCORE_ALIASES = {"gospel-of-john": "john"}

SCORE_RE = re.compile(r"(總分|總評|Total|合計|總計|Overall|綜合|平均)[^0-9\n]{0,30}(\d{1,2}\.\d+)")


def latest_score(names: list[str]) -> tuple[str, str]:
    """Newest docs/scores/<name>-<date>*.md that states an overall number, and that number.

    Several reports can share a date (a proofread, a spine check, a score); only some state a
    total, so take the newest one that does. '?' means files exist but none states a number.
    """
    found: list[tuple[str, str, str | None]] = []
    for f in SCORES.glob("*.md"):
        for n in names:
            m = re.fullmatch(rf"{re.escape(n)}-(\d{{4}}-\d{{2}}-\d{{2}}).*", f.stem, re.IGNORECASE)
            if m:
                hits = SCORE_RE.findall(f.read_text(encoding="utf-8", errors="ignore"))
                found.append((m.group(1), f.stem, hits[-1][1] if hits else None))
                break
    if not found:
        return "—", "—"
    found.sort(reverse=True)
    for when, _stem, number in found:
        if number:
            return number, when
    return "?", found[0][0]


def write_status(done: list[dict], out: Path, unmapped: list[str]) -> None:
    slug_to_dir = book_slug_map()
    dir_to_slug = {d.lower(): s for s, d in slug_to_dir.items()}
    base = read_baselines()
    lines = [
        "# Library status",
        "",
        f"_Generated by `python3 scripts/check-all.py --all --status` on {date.today().isoformat()}. "
        "Do not edit by hand._",
        "",
        "Scores are the book's own latest `docs/scores/` entry (AI-assigned, see the rubric in "
        "`.claude/skills/eat-bible/references/spine-and-score.md`); `?` means the file has no overall number the parser "
        "recognises. **Overfull** is the last recorded build, not today's. A check column shows P (pass), R (review "
        "candidates), F (fail), – (not applicable).",
        "",
        "| Book dir | Slug | Pages | Overfull | Spine | Markup | Scripture | Sermons | Ledger | Score | Scored |",
        "|---|---|---:|---:|:-:|:-:|:-:|:-:|:-:|---:|---|",
    ]
    totals = {"FAIL": 0, "REVIEW": 0}
    for r in sorted(done, key=lambda x: x["book"].name.lower()):
        book: Path = r["book"]
        slug = dir_to_slug.get(book.name.lower(), "")
        b = base.get(slug, {})
        ok, tot, unk = spine_counts(book)
        spine = f"{ok}/{tot}" + (f" (+{unk}?)" if unk else "") if tot else "—"
        sym = {"PASS": "P", "REVIEW": "R", "FAIL": "F", "n/a": "–"}
        cols = [sym[r["results"][n][0]] for n, _, _ in CHECKS[1:]]
        for n, _, _ in CHECKS:
            st = r["results"][n][0]
            if st in totals:
                totals[st] += 1
        names = [n for n in (slug, book.name) if n]
        names += [n.replace("gospel-of-", "") for n in names if n.startswith("gospel-of-")]
        names += [SCORE_ALIASES[book.name.lower()]] if book.name.lower() in SCORE_ALIASES else []
        score, when = latest_score(names)
        lines.append(
            f"| {book.name} | {slug or '—'} | {b.get('pages', '—')} | {b.get('overfull', '—')} | {spine} | "
            + " | ".join(cols) + f" | {score} | {when} |"
        )
    lines += [
        "",
        f"**{len(done)} book directories** · {totals['FAIL']} failing checks · {totals['REVIEW']} with review candidates.",
        "",
        "Directories under `books/bible/` with **no build script** (legacy, translation variants, drafts), not "
        "covered above: " + (", ".join(f"`{n}`" for n in unmapped) or "none") + ". Add them with `--include-unmapped`.",
        "",
        "Not run by check-all (they need per-book arguments or a build):",
        *[f"- `{n}`" for n in NOT_RUN],
        "",
    ]
    out.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("books", nargs="*", help="book directory, directory name, or build slug")
    ap.add_argument("--all", action="store_true", help="every book directory that has a build script")
    ap.add_argument("--include-unmapped", action="store_true",
                    help="with --all: also directories that have no build script (legacy, variants, drafts)")
    ap.add_argument("--status", nargs="?", const="docs/library-status.md", metavar="FILE",
                    help="also write the library status table (default docs/library-status.md)")
    ap.add_argument("-q", "--quiet", action="store_true", help="only print books with a FAIL or REVIEW")
    args = ap.parse_args()

    slug_to_dir = book_slug_map()
    mapped_dirs = {d.lower() for d in slug_to_dir.values()}
    all_dirs = sorted(d for d in BOOKS.iterdir() if d.is_dir() and not d.name.startswith("."))
    unmapped = [d.name for d in all_dirs if d.name.lower() not in mapped_dirs]
    if args.all:
        targets = all_dirs if args.include_unmapped else [d for d in all_dirs if d.name.lower() in mapped_dirs]
    else:
        targets = []
        for a in args.books:
            p = resolve(a, slug_to_dir)
            if p is None:
                print(f"unknown book: {a}", file=sys.stderr)
                return 2
            targets.append(p)
    if not targets:
        ap.print_usage()
        return 2

    with ThreadPoolExecutor(max_workers=4) as pool:
        done = list(pool.map(check_book, targets))

    failed = 0
    for r in done:
        states = [s for s, _ in r["results"].values()]
        bad = "FAIL" in states
        failed += bad
        if args.quiet and not bad and "REVIEW" not in states:
            continue
        print(f"\n{r['book'].name}")
        for name, (state, detail) in r["results"].items():
            print(f"  {state:<6} {name:<10} {detail[:110]}")

    if args.status:
        out = (ROOT / args.status) if not Path(args.status).is_absolute() else Path(args.status)
        write_status(done, out, [] if args.include_unmapped else unmapped)
        print(f"\nwrote {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}")

    print(f"\n{len(done)} book(s) checked, {failed} with at least one FAIL.")
    print("check-all does NOT run:")
    for n in NOT_RUN:
        print(f"  - {n}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
