#!/bin/bash
# 讀懂聖經的希臘文 — Reading the Greek New Testament: a first guide for new Bible students
# = preface + 10 chapters + appendices (top-100 words, form codes, sources) + afterword
# Data (counts, John 1:1-5 parse) is generated from MorphGNT SBLGNT by gen-biblegreek-data.py.
# Template: templates/pdf/biblegreek.latex

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/Biblegreek"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/biblegreek-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/biblegreek-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/biblegreek.latex"

[ -f "$TEMPLATE" ] || { echo "ERROR: Template not found: $TEMPLATE"; exit 1; }
mkdir -p "$OUTPUT_DIR"
python3 "$SCRIPT_DIR/gen-biblegreek-grammar.py" || { echo "❌ grammar generation failed"; exit 1; }
python3 "$SCRIPT_DIR/gen-biblegreek-part2.py" || { echo "❌ part 2 generation failed"; exit 1; }
python3 "$SCRIPT_DIR/gen-biblegreek-data.py" || { echo "❌ data generation failed"; exit 1; }

# Combine: strip each file's 7-line YAML header, splice the generated parse table
# into chapter 07, drop backticks around Greek, and wrap every Greek run in \greekfont.
python3 - "$INPUT_DIR" "$COMBINED_MD" <<'PY'
import glob, os, re, sys
d, out = sys.argv[1], sys.argv[2]
header = """---
title: "讀懂聖經的希臘文"
subtitle: "Reading the Greek New Testament — A First Guide"
author: "PubHub 三書精讀系統"
date: "2026年11月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria——榮耀唯獨歸神

  **資料來源：** 希臘文與形態標注取自 MorphGNT SBLGNT；所有次數與逐字表由程式計算產生，見附錄〈資料來源與核對說明〉。

  中文經文引自《聖經》和合本（公有領域）；英文對照取自 NASB 1995。
  Scripture quotations taken from the New American Standard Bible® (NASB),
  Copyright © 1960, 1962, 1963, 1968, 1971, 1972, 1973, 1975, 1977, 1995 by
  The Lockman Foundation. Used by permission. All rights reserved. lockman.org
---

"""
GREEK = r"[\u0370-\u03FF\u1F00-\u1FFF]"
run = re.compile(rf"(?:{GREEK}[{GREEK[1:-1]}\u2019\u0027\u02BC]*)(?:[ ]+{GREEK}[{GREEK[1:-1]}\u2019\u0027\u02BC]*)*")
def wrap(text):
    # unwrap `greek` code spans
    text = re.sub(r"`([^`\n]*" + GREEK + r"[^`\n]*)`", r"\1", text)
    text = run.sub(lambda m: "`{\\greekfont " + m.group(0) + "}\\allowbreak{}`{=latex}", text)
    # Greek runs are unbreakable boxes: a bare CJK comma between two of them leaves no line-break
    # opportunity (a 305pt overfull in chapter 8). Give each separator a breakable space.
    # Lists of verse numbers ("5:5、8:24、8:45…") have no break point between Latin digits and the CJK separator
    text = re.sub(r"([、；，])(?=[0-9A-Za-z])", lambda m: m.group(1) + "`\\allowbreak{}`{=latex}", text)
    # Hebrew runs (a few word-study notes cite Hebrew): own font, else they print as blank boxes
    return re.sub("[\u0590-\u05FF](?:[\u0590-\u05FF\u05BE ]*[\u0590-\u05FF])?", lambda m: "`{\\hebrewfont " + m.group(0) + "}`{=latex}", text)
def order(path):
    n = os.path.basename(path)
    if n.startswith("p2-"): return (1, n)      # Part 2 sits after chapters 1-11 and before the appendices
    if re.match(r"9\d", n) and not n.startswith("999"): return (2, n)
    if n.startswith("999"): return (3, n)
    return (0, n)
files = sorted(glob.glob(os.path.join(d, "[0-9]*.md")) + glob.glob(os.path.join(d, "p2-*.md")), key=order)
parts = [header]
for f in files:
    body = "".join(open(f, encoding="utf-8").readlines()[7:])
    if os.path.basename(f).startswith("07-"):
        gen = open(os.path.join(d, "generated/john1-1-5-parse.md"), encoding="utf-8").read()
        body = body.replace("<!--PARSE-->", gen)
    body = re.sub(r"<!--GEN:([a-z0-9-]+)-->", lambda m: open(os.path.join(d, "generated", m.group(1) + ".md"), encoding="utf-8").read(), body)
    parts.append(wrap(body))
    parts.append("\n\n\\newpage\n\n")
open(out, "w", encoding="utf-8").write("".join(parts))
print("combined", len(files), "files")
PY
[ $? -eq 0 ] || exit 1

source "$SCRIPT_DIR/lib/latex-check.sh"
LATEX_LOG="${OUTPUT_PDF%.pdf}-build.log"
pandoc "$COMBINED_MD" -o "$OUTPUT_PDF" --verbose --pdf-engine=xelatex --template="$TEMPLATE" \
  --from=markdown-superscript-subscript --top-level-division=chapter > "$LATEX_LOG" 2>&1
latex_build_report "$?" "$LATEX_LOG" "$OUTPUT_PDF" || exit 1
