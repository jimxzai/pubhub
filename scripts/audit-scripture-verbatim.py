#!/usr/bin/env python3
"""Audit a book's printed 和合本 Scripture against an independent source.

Why this exists
---------------
`lint-scripture-text.py` catches a fixed list of variant-character *classes*
inside Scripture blocks. It cannot tell you that a verse is simply wrong. In the
Acts pass (2026-08-31) this script found **91 character-level deviations** from
和合本 that every other check passed over — 擘餅 printed as 掰餅, 希奇 as 稀奇,
一分 as 一份, 鐵鍊 as 鐵鏈, 事奉 as 侍奉, 丟斯 as 宙斯, 革老丟 as 克勞迪, and
21 places where 作 had become 做. The cause was the original text having been
scraped from cnbible's CUVMP (modern-punctuation) edition, which differs from
和合本 systematically.

How to use it
-------------
    # 1. fetch the reference text once per book (cached to a json file)
    python3 scripts/audit-scripture-verbatim.py --fetch --book 徒 --chapters 28 \
        --out /tmp/cuv_acts.json

    # 2. diff the book's Scripture blocks against it
    python3 scripts/audit-scripture-verbatim.py --src /tmp/cuv_acts.json \
        books/bible/acts/[0-2][0-9]-*.md

Reading the output
------------------
Findings are CANDIDATES, never edits. Two traps, both hit in the Acts pass:

  * **fhl.net's `unv` mixes classic and modern renderings.** It gave 泰爾 for
    推羅, 尼亞坡里 for 尼亞波利, 衣索匹亞 for 埃提阿伯, 希臘話 for 希利尼話 —
    in every one of those the BOOK was right. Confirm each character class
    against ai-eden.com (this project's standard) verse by verse before
    changing anything, and never blanket-replace a character.
  * **和合本 is not internally consistent.** 做/作 is genuinely mixed: Acts 13:2
    really is 「去做我召他們所做的工」. Per-verse only.

Chapter-file convention assumed: filename starts with the chapter number
(`03-beautiful-gate.md`) and the Scripture block is headed
`### 中文 — 和合本 (CUV)`.
"""
import argparse, difflib, html, json, os, re, sys, time, unicodedata
import urllib.parse, urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

MARKUP = re.compile(r"\\jesus\{|\\textbf\{|\\textit\{|\}|\*\*|\*")
ANNOT = re.compile(r"（(?:或譯|或作|併於|原文|按|即)[^）]*）")
DROP = "\u3000\u2500"

# Characters this repo deliberately standardises (project style policy).
POLICY = [("裡", "裏"), ("什麼", "甚麼")]


# ---------------------------------------------------------------- fetching
def fetch_chapter(book_zh, chap):
    url = ("https://bible.fhl.net/new/read.php?VERSION1=unv&TABFLAG=1"
           f"&chineses={urllib.parse.quote(book_zh)}&chap={chap}")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8", errors="replace")


def parse_chapter(page, chap):
    verses = {}
    pat = r'<b>(\d+):(\d+)</b><a name="[^"]*"\s*/?></td><td[^>]*>(.*?)</td>'
    for m in re.finditer(pat, page, re.S):
        c, v, t = m.group(1), m.group(2), m.group(3)
        if int(c) != chap:
            continue
        t = re.sub(r"<[^>]+>", "", t)
        verses[v] = html.unescape(t).strip()
    return verses


def do_fetch(book_zh, chapters, out):
    data = {}
    for c in range(1, chapters + 1):
        for _ in range(3):
            try:
                v = parse_chapter(fetch_chapter(book_zh, c), c)
                if v:
                    data[str(c)] = v
                    print(f"  ch{c}: {len(v)} verses", file=sys.stderr)
                    break
            except Exception as e:
                print(f"  ch{c}: {e}", file=sys.stderr)
            time.sleep(2)
        time.sleep(1)
    json.dump(data, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"wrote {out} ({len(data)} chapters)", file=sys.stderr)


# ---------------------------------------------------------------- auditing
def normalise(s, policy=True):
    s = MARKUP.sub("", s)
    s = ANNOT.sub("", s)
    for ch in DROP:
        s = s.replace(ch, "")
    if policy:
        for a, b in POLICY:
            s = s.replace(a, b)
    return "".join(c for c in s
                   if not unicodedata.category(c).startswith("P") and not c.isspace())


def book_verses(path):
    text = open(path, encoding="utf-8").read()
    m = re.search(r"### 中文 — 和合本 \(CUV\)(.*?)(?=^### |^## )", text, re.S | re.M)
    if not m:
        return {}
    out = {}
    for line in m.group(1).split("\n"):
        if not line.startswith(">"):
            continue
        parts = re.split(r"\^(\d+(?:-\d+)?)\^", line[1:].strip())
        for i in range(1, len(parts), 2):
            out.setdefault(parts[i], "")
            out[parts[i]] += parts[i + 1]
    return out


def audit(paths, src):
    subs, other, checked = {}, [], 0
    for path in sorted(paths):
        m = re.match(r"(\d+)-", os.path.basename(path))
        if not m or str(int(m.group(1))) not in src:
            continue
        chap = str(int(m.group(1)))
        verses = src[chap]
        for marker, body in book_verses(path).items():
            if "-" in marker:
                a, b = marker.split("-")
                want = "".join(verses.get(str(v), "") for v in range(int(a), int(b) + 1))
            else:
                want = verses.get(marker)
                if want is None:
                    continue
            got_n, want_n = normalise(body), normalise(want)
            checked += 1
            if got_n == want_n:
                continue
            sm = difflib.SequenceMatcher(None, got_n, want_n, autojunk=False)
            single = True
            for tag, i1, i2, j1, j2 in sm.get_opcodes():
                if tag == "equal":
                    continue
                if tag == "replace" and (i2 - i1) == (j2 - j1) <= 3:
                    for k in range(i2 - i1):
                        a, b = got_n[i1 + k], want_n[j1 + k]
                        if a != b:
                            ctx = got_n[max(0, i1 + k - 6):i1 + k + 7]
                            subs.setdefault((a, b), []).append(
                                f"{os.path.basename(path)} {chap}:{marker}  …{ctx}…")
                else:
                    single = False
            if not single:
                other.append((os.path.basename(path), f"{chap}:{marker}", got_n, want_n))

    print(f"checked {checked} verses in {len(paths)} file(s)\n")
    print("== character substitutions (book -> source) ==")
    print("   each is a CANDIDATE: confirm against ai-eden.com per verse\n")
    for (a, b), where in sorted(subs.items(), key=lambda kv: -len(kv[1])):
        print(f"  「{a}」 vs 「{b}」   x{len(where)}")
        for w in where[:4]:
            print(f"      {w}")
        if len(where) > 4:
            print(f"      … and {len(where) - 4} more")
    print(f"\n== length/boundary differences (excerpting or edition split): {len(other)} ==")
    for f, ref, got, want in other[:15]:
        print(f"  {f} {ref}\n     book  : {got[:70]}\n     source: {want[:70]}")
    return len(subs) + len(other)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", help="chapter markdown files to audit")
    ap.add_argument("--fetch", action="store_true", help="fetch reference text instead of auditing")
    ap.add_argument("--book", help="Chinese book abbreviation for fhl.net, e.g. 徒 詩 彼後")
    ap.add_argument("--chapters", type=int, help="number of chapters to fetch")
    ap.add_argument("--out", help="json file to write (--fetch) ")
    ap.add_argument("--src", help="json file of reference text (audit mode)")
    a = ap.parse_args()

    if a.fetch:
        if not (a.book and a.chapters and a.out):
            ap.error("--fetch needs --book, --chapters and --out")
        do_fetch(a.book, a.chapters, a.out)
        return 0
    if not (a.src and a.paths):
        ap.error("audit mode needs --src and at least one chapter file")
    return 0 if audit(a.paths, json.load(open(a.src, encoding="utf-8"))) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
