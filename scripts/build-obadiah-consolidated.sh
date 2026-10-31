#!/bin/bash

# Obadiah PDF Builder - CONSOLIDATED 2026 EDITION
# = preface + orientation (overview / position / order of revelation)
#   + 5 sections of Obadiah (one part divider per step of the spine)
#   + 卷末 (systematic reception) + appendices + afterword
# Sources from books/bible/Obadiah/ (老弟兄 methodology + Calvin + Henry +
# Morgan, CUV + NASB 1995 scripture; no MacArthur — gty.org has no Obadiah series).
# Modeled on scripts/build-jude-consolidated.sh (unnumbered front/back matter so
# the five sections number 1..5; part dividers carry the spine:
# 「啟示的次序·第N步」 + 貫穿的線 table).
# Uses templates/pdf/obadiah.latex (Petra rust / gold, full-bleed front and back covers).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/Obadiah"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/obadiah-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/obadiah-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/obadiah.latex"

echo "=========================================="
echo "📖 Obadiah PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "俄巴底亞書研讀"
subtitle: "The Book of Obadiah Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年10月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **資源整合：**

  • **老弟兄查經方法論之應用**（倉庫中沒有老弟兄以俄巴底亞書為題的查經記錄，詳見附錄〈引用出處總表〉的誠實聲明）

  • **John Calvin** — *Commentaries on the Twelve Minor Prophets*, vol. 2（Joel, Amos, Obadiah），tr. John Owen（公有領域）

  • **Matthew Henry** — *An Exposition of the Old and New Testament*（公有領域）

  • **G. Campbell Morgan** — *Living Messages of the Books of the Bible*（公有領域）

  • 本書沒有 John MacArthur 的引文：gty.org 沒有以俄巴底亞書為題的講道系列

  **弟兄遭難的日子，你站在哪裏？**

  「耶和華降罰的日子臨近萬國。你怎樣行，他也必照樣向你行。」（俄15）

  **經文版權聲明 (Scripture Copyright Notices)**

  2026 年 10 月 · 初版。本版為教會內部贈閱版（非賣品）；公開發行時另行申請 ISBN。

  中文經文引自《聖經》和合本，屬公有領域；逐節核對來源見附錄〈引用出處總表〉。

  Scripture quotations taken from the New American Standard Bible® (NASB),
  Copyright © 1960, 1971, 1977, 1995 by The Lockman Foundation. Used by
  permission. All rights reserved. lockman.org
---

HEADER

chapter_count=0

# Strip the 7-line YAML front matter, convert ^n^ / ^24-25^ verse markers to
# \textsuperscript{}{} (the trailing {} keeps a digit from abutting a following
# \textbf{ — see build-2-peter-consolidated.sh for the root cause).
emit() {
    tail -n +8 "$1" | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}{}/g'
}

# A numbered chapter (the five sections of Obadiah).
add_file() {
    local f="$1"
    [ -f "$f" ] || { echo "❌ Missing file: $1 — aborting build"; exit 1; }
    echo "  Adding: $(basename "$f")"
    emit "$f" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Front/back matter: first H1 marked unnumbered so it does not consume a
# chapter number.
add_front() {
    local f="$1"
    [ -f "$f" ] || { echo "❌ Missing file: $1 — aborting build"; exit 1; }
    echo "  Adding (unnumbered): $(basename "$f")"
    emit "$f" \
      | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); if($0 !~ /\{\.unnumbered\}$/) $0=$0" {.unnumbered}"; done=1 } } {print}' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Part divider. $2 is the one-line description (carries 「啟示的次序·第N步」);
# optional $3-$5 add the 貫穿的線 / 鑰節 / 貫穿的問題 table.
# printf '%s' (not %b) on purpose: descriptions are plain text, and %b would
# turn a literal backslash sequence into a control character.
add_volume() {
    printf '# %s {.unnumbered}\n\n> %s\n' "$1" "$2" >> "$COMBINED_MD"
    if [ -n "$3" ]; then
        printf '\n| | |\n|---|---|\n| **貫穿的線** | %s |\n| **鑰節** | %s |\n| **貫穿的問題** | %s |\n' \
            "$3" "$4" "$5" >> "$COMBINED_MD"
    fi
    printf '\n\\newpage\n\n' >> "$COMBINED_MD"
    echo "  --- $1"
}

add_chapter() {
    local f
    for f in "$INPUT_DIR/$1-"*.md; do
        [ -f "$f" ] && { add_file "$f"; return 0; }
    done
    echo "❌ Missing chapter file for prefix '$1-' in $INPUT_DIR — aborting build"
    exit 1
}

# 前言
add_front "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這三章：地圖、座標、骨幹——啟示的次序與神的計劃。"
add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-obadiah-position.md"
add_front "$INPUT_DIR/00c-revelation-order.md"

# ============================================================
# 正文 · 五步
# ============================================================
add_volume "第一步 · 俄巴底亞書 1-4 節 (Step One)" \
    "啟示的次序·第一步：神先開口——戰事還在傳言，使者已差往列國；以東問「誰能」，神用同一個動詞回答「我必」。" \
    "**拉下**——以東的問題，神的回答" \
    "4節「我必從那裏拉下你來」" \
    "我心裏有沒有一句「誰能……」？"
add_chapter 01

add_volume "第二步 · 俄巴底亞書 5-9 節 (Step Two)" \
    "啟示的次序·第二步：神一件一件取走以東所倚靠的——財寶、盟友、智慧、勇士；拆的不是他的過錯，是他的長處。" \
    "**何竟**——五樣倚靠，沒有一樣留到最後" \
    "8節「到那日，我豈不從以東除滅智慧人」" \
    "我最倚靠的那一樣，是在用它，還是在靠它？"
add_chapter 02

add_volume "第三步 · 俄巴底亞書 10-14 節 (Step Three)" \
    "啟示的次序·第三步：然後才說罪名——全書詳列的罪名，核心是在弟兄的日子站在一旁；同一個日子，十次點名。" \
    "**日子**十次，**不當**八次——從站在一旁到站在岔路口" \
    "11節「你竟站在一旁，像與他們同夥」" \
    "我的弟兄現在正在過哪一個「日子」？我站在哪裏？"
add_chapter 03

add_volume "第四步 · 俄巴底亞書 15-16 節 (Step Four)" \
    "啟示的次序·第四步：日子擴大——耶和華降罰的日子臨近萬國；你怎樣行，他也必照樣向你行；杯從神手裏出去。" \
    "**照樣**——公義的對稱；**杯**——喝三次" \
    "15節「你怎樣行，他也必照樣向你行」" \
    "我用甚麼量器量人？我願意被同樣的量器量嗎？"
add_chapter 04

add_volume "第五步 · 俄巴底亞書 17-21 節 (Step Five)" \
    "啟示的次序·第五步，也是全書的終點：最後一句屬於國度——逃脫、成聖、承受；拯救者上到錫安山；全書最後一個字是「國度」。" \
    "**國度**——全書最後一個字" \
    "21節「必有拯救者上到錫安山，審判以掃山；國度就歸耶和華了」" \
    "我今天在建造的，是誰的國度？"
add_chapter 05

# ============================================================
# 卷末 · 全書領受總綱
# ============================================================
add_volume "卷末 · 回望 (Looking Back)" \
    "五步讀完，把全書的領受收攏成一張圖——再一次站在兩個「那日」中間，看見那位在我們的日子裏沒有站在一旁的主。"

# The study file is a synthesis OF the five sections, so it sits after them
# (as in Jude), not in the front matter. No YAML: first line is its H1.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——老弟兄查經法 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
    tail -n +2 "$STUDY_FILE" | sed 's/^#/##/' | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}{}/g' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
else
    echo "❌ Missing file: $STUDY_FILE — aborting build"
    exit 1
fi

# ============================================================
# 附錄
# ============================================================
add_volume "附錄 (Appendices)" \
    "經文與主題索引、讀經計劃、引用出處總表——供查閱、跨章對照，並如實交代每一處引句的查證方式。"
add_front "$INPUT_DIR/98-appendix-indices.md"
add_front "$INPUT_DIR/96-appendix-reading-plan.md"
add_front "$INPUT_DIR/99-appendix-references.md"

# 跋 — last content file: no trailing \newpage (the colophon opens its own page).
[ -f "$INPUT_DIR/999-afterword.md" ] || { echo "❌ Missing file: $INPUT_DIR/999-afterword.md — aborting build"; exit 1; }
echo "  Adding (unnumbered): 999-afterword.md"
emit "$INPUT_DIR/999-afterword.md" \
  | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); if($0 !~ /\{\.unnumbered\}$/) $0=$0" {.unnumbered}"; done=1 } } {print}' >> "$COMBINED_MD"
((chapter_count++))

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count sections)"
echo ""

# Wrap Greek runs in an explicit {\greekfont …} group passed through pandoc as
# raw LaTeX (see build-2-peter-consolidated.sh for why ucharclasses alone is
# not trusted with bold spans, and why the group must be a `…`{=latex} span —
# a bare {…} is escaped by pandoc into an unscoped font switch). Chapter
# markdown therefore carries plain Greek, never a hand-written wrap.
echo "Wrapping Greek Unicode runs in {\\greekfont ...}..."
COMBINED_MD_PATH="$COMBINED_MD" python3 <<'PYEOF'
import os, re
path = os.environ['COMBINED_MD_PATH']
text = open(path, encoding='utf-8').read()
# Skip anything already inside a backtick span.
parts = re.split(r'(`[^`]*`(?:\{=latex\})?)', text)
greek_run = re.compile(r'[Ͱ-Ͽἀ-῿]+(?: [Ͱ-Ͽἀ-῿]+)*')
n = 0
for i in range(0, len(parts), 2):
    def wrap(m):
        global n
        n += 1
        return '`{\\greekfont ' + m.group(0) + '}`{=latex}'
    parts[i] = greek_run.sub(wrap, parts[i])
open(path, 'w', encoding='utf-8').write(''.join(parts))
print(f"  Wrapped {n} Greek run(s)")
PYEOF

echo "🔨 Generating PDF with obadiah.latex template..."

# --verbose is load-bearing: without it pandoc swallows the xelatex log and
# every grep-the-log check (here and in driver.sh) passes vacuously.
source "$SCRIPT_DIR/lib/latex-check.sh"
LATEX_LOG="${OUTPUT_PDF%.pdf}-build.log"

pandoc "$COMBINED_MD" \
  -o "$OUTPUT_PDF" \
  --verbose \
  --pdf-engine=xelatex \
  --template="$TEMPLATE" \
  --from=markdown-superscript-subscript \
  --toc \
  --toc-depth=1 \
  --top-level-division=chapter > "$LATEX_LOG" 2>&1
PANDOC_EXIT=$?

latex_build_report "$PANDOC_EXIT" "$LATEX_LOG" "$OUTPUT_PDF" || exit 1
