#!/usr/bin/env python3
"""Combine books/bible/Biblehebrew/*.md into one pandoc-ready file.

Usage: combine-biblehebrew.py <input-dir> <output.md>

Steps per source file: strip the 7-line YAML header, fill {{key}} placeholders from generated/stats.json
(fails on any unknown key), splice generated tables for <!--SONG:..-->, <!--PARSE-->, <!--VERBS-->,
<!--VERBFORMS-->, <!--PREFIX-->, <!--SERIES-->, <!--HYMNS-->, <!--GRAM:..-->, <!--VERSES:book.ch:a-b-->,
<!--HEB:ref-->; normalise 裡->裏; wrap every Hebrew run in \\hebrewfont and Greek runs in \\greekfont.
"""
import glob, importlib.util, json, os, re, sys

d, out = sys.argv[1], sys.argv[2]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts/lib"))
import hebrew_book as hb
GEN = os.path.join(d, "generated")
stats = json.load(open(os.path.join(GEN, "stats.json"), encoding="utf-8"))
exc = json.load(open(os.path.join(ROOT, "docs/sources/biblehebrew/scripture-excerpts.json"), encoding="utf-8"))
spec = importlib.util.spec_from_file_location("g", os.path.join(ROOT, "scripts/gen-biblehebrew-data.py"))
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
_verses = None


def read(name):
    return open(os.path.join(GEN, name), encoding="utf-8").read().rstrip("\n")


def verses(m):
    book, ch, a, b = m.group(1), m.group(2), int(m.group(3)), int(m.group(4))
    rows = ["| 節 | 和合本 | NASB 1995 |", "|--------|------------------------------|------------------------------------------|"]
    for v in range(a, b + 1):
        e = exc[f"{book}.{ch}.{v}"]
        zh = re.sub(r"^（[^）]*）", "", e["cuv"])
        rows.append(f"| {ch}:{v} | {zh} | {e['nasb1995']} |")
    return "\n".join(rows)


def heb(m):
    global _verses
    if _verses is None:
        _verses = {}
        for r, l, mo, t in g.tokens():
            _verses.setdefault(r, []).append(g.strip_cantillation(t))
    words = _verses[m.group(1)]
    return "\n".join("| " + " ".join(words[i:i + 5]) for i in range(0, len(words), 5))


def fill(text):
    text = hb.fill_stats(text, stats)
    text = re.sub(r"<!--SONG:(\w+)-->", lambda m: read(f"song-{m.group(1)}.md"), text)
    text = re.sub(r"<!--GRAM:(\w+)-->", lambda m: read(f"gram-{m.group(1)}.md"), text)
    text = text.replace("<!--PARSE-->", read("genesis1-parse.md"))
    vs = read("verb-stats.md").split("\n\n")
    text = text.replace("<!--VERBS-->", vs[0]).replace("<!--VERBFORMS-->", vs[1])
    text = text.replace("<!--PREFIX-->", read("prefix-stats.md")).replace("<!--SERIES-->", read("series-vocab.md"))
    text = text.replace("<!--HYMNS-->", read("hymns.md"))
    text = re.sub(r"<!--VERSES:(\w+)\.(\d+):(\d+)-(\d+)-->", verses, text)
    text = re.sub(r"<!--HEB:([A-Za-z0-9.]+)-->", heb, text)
    if "<!--" in text and re.search(r"<!--(SONG|GRAM|VERSES|HEB|PARSE|VERBS|PREFIX|SERIES|HYMNS)", text):
        sys.exit("unresolved placeholder: " + re.search(r"<!--[^>]*-->", text).group(0))
    return text.replace("裡", "裏")


wrap = lambda text: hb.wrap_scripts(text, greek=True)


header = '''---
title: "讀懂聖經的希伯來文"
subtitle: "Reading the Hebrew Old Testament — A First Guide"
author: "PubHub 三書精讀系統"
date: "2026年11月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria——榮耀唯獨歸神

  **資料來源：** 希伯來文與形態標注取自 OSHB（Open Scriptures Hebrew Bible，列寧格勒抄本）；所有次數、逐字表與文法表由程式計算產生，見附錄〈資料來源與核對說明〉。

  Original work of the Open Scriptures Hebrew Bible available at https://github.com/openscriptures/morphhb (CC BY 4.0; based on the Westminster Leningrad Codex, public domain).

  中文經文引自《聖經》和合本（公有領域）；英文對照取自 NASB 1995。
  Scripture quotations taken from the New American Standard Bible® (NASB),
  Copyright © 1960, 1962, 1963, 1968, 1971, 1972, 1973, 1975, 1977, 1995 by
  The Lockman Foundation. Used by permission. All rights reserved. lockman.org
---

'''
files = sorted(glob.glob(os.path.join(d, "[0-9]*.md")))
parts = [header]
for f in files:
    body = hb.strip_header(f, open(f, encoding="utf-8").read())
    parts.append(wrap(fill(body)))
    parts.append("\n\n\\newpage\n\n")
open(out, "w", encoding="utf-8").write("".join(parts))
print("combined", len(files), "files")
