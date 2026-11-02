#!/usr/bin/env python3
"""Combine books/bible/Biblehebrew-compendium/*.md into one pandoc-ready file.
Usage: combine-hebrew-compendium.py <input-dir> <output.md>
Strips each file's 7-line header, fills {{key}} from generated/stats.json (fails on unknown keys), splices
<!--ABBR-->, <!--OVERVIEW-->, <!--BOOKS-->, <!--INDEX-->, normalises 裡->裏, wraps Hebrew runs in \\hebrewfont.
"""
import glob, importlib.util, os, re, sys, json

d, out = sys.argv[1], sys.argv[2]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN = os.path.join(d, "generated")
stats = json.load(open(os.path.join(GEN, "stats.json"), encoding="utf-8"))
spec = importlib.util.spec_from_file_location("c", os.path.join(ROOT, "scripts/gen-hebrew-compendium.py"))
c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)


def read(n): return open(os.path.join(GEN, n), encoding="utf-8").read().rstrip("\n")


def abbr():
    rows = ["| 簡稱 | 書卷 | 簡稱 | 書卷 | 簡稱 | 書卷 |", "|------|----------------|------|----------------|------|----------------|"]
    items = [(b[2], b[1]) for b in c.BOOKS]
    for i in range(0, len(items), 3):
        chunk = items[i:i + 3] + [("", "")] * (3 - len(items[i:i + 3]))
        rows.append("| " + " | ".join(f"{a} | {z}" for a, z in chunk) + " |")
    return "\n".join(rows)


def fill(t):
    def num(m):
        k = m.group(1)
        if k not in stats: sys.exit(f"unknown placeholder {{{{{k}}}}}")
        v = stats[k]; return f"{v:,}" if isinstance(v, int) and v >= 1000 else str(v)
    t = re.sub(r"\{\{([A-Za-z0-9_]+)\}\}", num, t)
    t = t.replace("<!--ABBR-->", abbr()).replace("<!--OVERVIEW-->", read("overview.md"))
    t = t.replace("<!--BOOKS-->", read("books.md")).replace("<!--INDEX-->", read("index.md"))
    if re.search(r"<!--(ABBR|OVERVIEW|BOOKS|INDEX)", t): sys.exit("unresolved placeholder")
    return t.replace("裡", "裏")


HEB = "[֑-״͏יִ-ﭏ]"
run = re.compile(rf"{HEB}+(?:[ ]+{HEB}+)*")


def wrap(t):
    t = re.sub(r"`([^`\n]*" + HEB + r"[^`\n]*)`", r"\1", t)   # unwrap `code` spans around Hebrew
    return run.sub(lambda m: "`\\leavevmode\\allowbreak{\\hebrewfont " + m.group(0) + "}\\allowbreak`{=latex}", t)


header = '''---
title: "舊約希伯來文彙編"
subtitle: "A Hebrew Companion to the Old Testament Series"
author: "PubHub 三書精讀系統"
date: "2026年11月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria——榮耀唯獨歸神

  **資料來源：** 希伯來文與詞目取自 OSHB（Open Scriptures Hebrew Bible，列寧格勒抄本）與其強氏詞典；本系列〈原文研讀〉的內容取自舊約各卷章節檔案；所有次數、索引與一覽由程式計算產生，見附錄〈資料來源與核對說明〉。

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
    body = "".join(open(f, encoding="utf-8").readlines()[7:])
    parts.append(wrap(fill(body))); parts.append("\n\n\\newpage\n\n")
open(out, "w", encoding="utf-8").write("".join(parts))
print("combined", len(files), "files")
