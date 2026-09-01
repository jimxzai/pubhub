#!/usr/bin/env python3
"""Verify each quoted sermon citation against the transcript it is attributed to.

WHY THIS EXISTS
---------------
The companion to scripts/verify-citations.py, which checks quotes against a
local copy of a book. Sermon quotes have no single local text: each chapter
cites several sermons, each with its own code, so a quote can only be checked
against the ONE transcript it claims to come from.

2026-08-31, Gospel of Luke: the appendix asserted every MacArthur quote had been
verified word-for-word against gty.org. Spot-checking four found two that had
drifted -- a fragment recast as a standalone sentence, and a clause whose
grammar had been smoothed into parallel form ("forget your own mortality" for
"and he forgot his own mortality"). Separately, a research pass that asked a
model to "find the quote" produced four confident, fully fabricated sentences.
So: fetch the transcript, match the string, trust neither memory nor a summariser.

HOW IT MAPS QUOTES TO SERMONS
Within a commentator section, quotes are attributed by the `> — ... sermon CODE`
line that FOLLOWS them. A section may hold several such groups. Lines reading
「同上講章」 (same sermon as above) inherit the previous code.

USAGE
    python3 scripts/verify-sermon-quotes.py <book-dir> [--heading 麥克阿瑟]
                                            [--cache <dir>] [--only ch01,ch05]

Exit 1 if any quote is missing from its own transcript.
"""
import argparse
import html
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

CODE_RE = re.compile(r"(?:sermon\s+|/\s*)([0-9]{2}-[0-9]{1,3})", re.I)
URL_RE = re.compile(r"https://www\.gty\.org/\S+?/([0-9]{2}-[0-9]{1,3})/([a-z0-9\-]+)")
QUOTE_RE = re.compile(r'^> "(.+?)"', re.M)
SRC_RE = re.compile(r"^> — .*$", re.M)


def norm(text):
    text = unicodedata.normalize("NFKC", text)
    for a, b in [("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'),
                 ("—", " "), ("–", " "), ("…", "...")]:
        text = text.replace(a, b)
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def fetch(code, cache_dir):
    """Transcript text for a gty.org sermon code, cached on disk."""
    cache = Path(cache_dir) / f"gty-{code}.txt"
    if cache.exists() and cache.stat().st_size > 5000:
        return norm(cache.read_text(encoding="utf-8", errors="replace"))
    url = f"https://www.gty.org/library/sermons-library/{code}/"
    try:
        raw = subprocess.run(["curl", "-sL", "--max-time", "90", url],
                             capture_output=True, text=True, timeout=120).stdout
    except Exception as e:                                   # noqa: BLE001
        print(f"    ! fetch failed for {code}: {e}")
        return None
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    text = re.sub(r"\s+", " ", text)
    if len(text) < 5000:
        print(f"    ! transcript for {code} looks empty ({len(text)} chars)")
        return None
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(text, encoding="utf-8")
    return norm(text)


def groups(section):
    """[([codes], [quotes])] -- quotes attributed to the source line following them."""
    out, pending, last_code = [], [], None
    for line in section.splitlines():
        q = re.match(r'^> "(.+?)"', line)
        if q:
            pending.append(q.group(1))
            continue
        if line.startswith("> —") or "出處" in line:
            codes = CODE_RE.findall(line) or [g[0] for g in URL_RE.findall(line)]
            if not codes and "同上" in line and last_code:
                codes = [last_code]
            if codes:
                last_code = codes[-1]
            if pending:
                out.append((codes or [None], pending))
                pending = []
    if pending:
        out.append(([last_code] if last_code else [None], pending))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book_dir")
    ap.add_argument("--heading", default="麥克阿瑟")
    ap.add_argument("--cache", default="/tmp/sermon-cache")
    ap.add_argument("--only", default=None, help="comma-separated file prefixes")
    args = ap.parse_args()

    only = set(args.only.split(",")) if args.only else None
    sources, ok, bad, unknown = {}, 0, [], []

    for f in sorted(Path(args.book_dir).glob("[0-9][0-9]-*.md")):
        if only and f.name[:2] not in {o[-2:] for o in only}:
            continue
        text = f.read_text(encoding="utf-8")
        m = re.search(rf"^### [^\n]*{args.heading}[^\n]*\n.*?(?=^## |^### )", text, re.S | re.M)
        if not m:
            continue
        print(f"\n{f.name}")
        for codes, quotes in groups(m.group(0)):
            code = codes[0]
            if not code:
                for q in quotes:
                    print(f"  NOCODE {q[:70]}")
                    unknown.append((f.name, q))
                continue
            for c in codes:
                if c not in sources:
                    sources[c] = fetch(c, args.cache)
            hays = [sources[c] for c in codes if sources.get(c)]
            label = "/".join(codes)
            for q in quotes:
                if not hays:
                    print(f"  UNFETCHED [{label}] {q[:66]}")
                    unknown.append((f.name, q))
                    continue
                # a quote may join two passages with an ellipsis; each part must
                # appear (possibly in different sermons of the same citation)
                # split the RAW quote on ellipses BEFORE normalising -- norm()
                # strips punctuation, which would erase the split points and
                # make an elided quote look like one unbroken run that is not
                # in the transcript (a false MISS that cost a debugging round).
                parts = [norm(x) for x in re.split(r"\.\.\.|…", q)]
                frags = [x for x in parts if len(x) > 12] or [norm(q)]
                if all(any(fr in h for h in hays) for fr in frags):
                    ok += 1
                    print(f"  OK     [{label}] {q[:66]}")
                else:
                    bad.append((f.name, label, q))
                    print(f"  MISS   [{label}] {q[:66]}")

    print(f"\n{'='*60}\nverified: {ok}   missing from own transcript: {len(bad)}   "
          f"unresolved: {len(unknown)}")
    for fn, code, q in bad:
        print(f"  {fn} [{code}] {q[:88]}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
