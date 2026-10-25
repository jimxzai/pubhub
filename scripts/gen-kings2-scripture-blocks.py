#!/usr/bin/env python3
"""Fill the `## 經文` block of each 2 Kings chapter from .sources/scripture/.

CUV (和合本) and NASB 1995 texts live as per-verse JSON in
books/bible/kings2/.sources/scripture/ (CUV: fhl 現代標點本，專有名詞依 ai-eden 定案；
NASB: biblegateway, 719 節與 biblehub 逐字比對相符). Chapter structure
(章題、分段) lives in .sources/chapters.json.

A chapter file holds either the placeholder line `@@SCRIPTURE@@` or a block
wrapped in <!-- KINGS2:SCRIPTURE:BEGIN --> / <!-- KINGS2:SCRIPTURE:END -->.
Run with --write to (re)generate; without it, reports what would change.
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent / "books/bible/kings2"
SRC = ROOT / ".sources"
BEGIN, END = "<!-- KINGS2:SCRIPTURE:BEGIN -->", "<!-- KINGS2:SCRIPTURE:END -->"


def verses(kind, ch):
    d = json.loads((SRC / "scripture" / f"{kind}-{ch:02d}.json").read_text(encoding="utf8"))
    return {int(k): v for k, v in d.items()}


def block(ch, meta):
    cuv, nasb = verses("cuv", ch), verses("nasb", ch)
    out = [BEGIN, "", "### 中文 — 和合本 (CUV)", ""]
    for a, b, zh, _ in meta["sec"]:
        rng = f"{ch}:{a}" if a == b else f"{ch}:{a}-{b}"
        out += [f"**{zh}（{rng}）**", "", "> " + "".join(f"^{v}^{cuv[v]}" for v in range(a, b + 1)), ""]
    out += ["### English — NASB", ""]
    for a, b, _, en in meta["sec"]:
        rng = f"{ch}:{a}" if a == b else f"{ch}:{a}-{b}"
        out += [f"**{en} ({rng})**", "", "> " + " ".join(f"^{v}^{nasb[v]}" for v in range(a, b + 1)), ""]
    out += [END]
    return "\n".join(out)


def main():
    write = "--write" in sys.argv
    chapters = json.loads((SRC / "chapters.json").read_text(encoding="utf8"))
    rc = 0
    for key, meta in chapters.items():
        f = ROOT / meta["file"]
        if not f.exists():
            continue
        text = f.read_text(encoding="utf8")
        blk = block(int(key), meta)
        if "@@SCRIPTURE@@" in text:
            new = text.replace("@@SCRIPTURE@@", blk)
        elif BEGIN in text:
            new = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), lambda m: blk, text, flags=re.S)
        else:
            print(f"NO-MARKER {f.name}")
            rc = 1
            continue
        if new != text:
            print(("WRITE " if write else "WOULD-WRITE ") + f.name)
            if write:
                f.write_text(new, encoding="utf8")
    return rc


if __name__ == "__main__":
    sys.exit(main())
