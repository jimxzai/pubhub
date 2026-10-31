#!/bin/bash

# Zephaniah PDF Builder - CONSOLIDATED 2026 EDITION
# = preface + orientation (overview / position / order of revelation)
#   + 8 chapters of Zephaniah (one part divider per step of the spine)
#   + 卷末 (systematic reception) + appendices + afterword
# Sources from books/bible/Zapphaniah/ (老弟兄 methodology + Calvin + Henry +
# Morgan, CUV + NASB 1995 scripture; no MacArthur — gty.org has no Zephaniah series).
# Modeled on scripts/build-jude-consolidated.sh (unnumbered front/back matter so
# the five sections number 1..5; part dividers carry the spine:
# 「啟示的次序·第N步」 + 貫穿的線 table).
# Uses templates/pdf/zephaniah.latex (Petra rust / gold, full-bleed front and back covers).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/Zapphaniah"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/zephaniah-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/zephaniah-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/zephaniah.latex"

echo "=========================================="
echo "📖 Zephaniah PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "西番雅書研讀"
subtitle: "The Book of Zephaniah Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年10月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **資源整合：**

  • **老弟兄查經方法論之應用**（倉庫中沒有老弟兄以西番雅書為題的查經記錄，詳見附錄〈引用出處總表〉的誠實聲明）

  • **John Calvin** — *Commentaries on the Twelve Minor Prophets*, vol. 4（Habakkuk, Zephaniah, Haggai），tr. John Owen（公有領域）

  • **Matthew Henry** — *An Exposition of the Old and New Testament*（公有領域）

  • **G. Campbell Morgan** — *Living Messages of the Books of the Bible*（公有領域）

  • 本書沒有 John MacArthur 的引文：gty.org 沒有以西番雅書為題的講道系列

  **日子近了，祂也在你中間。**

  「他在你中間必因你歡欣喜樂，默然愛你，且因你喜樂而歡呼。」（番3:17）

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

# A numbered chapter (the eight chapters of Zephaniah).
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
add_front "$INPUT_DIR/00a-zephaniah-position.md"
add_front "$INPUT_DIR/00c-revelation-order.md"

# ============================================================
# 正文 · 八章，五步
# ============================================================
add_volume "卷一 · 日子近了 (Volume One: The Day Is Near)" \
    "啟示的次序·第一、二步：西番雅書第1章——神先開口，從萬有說起，縮到祂自己的家；然後日子近了，祂親自巡查。"

add_volume "第一章 · 西番雅書 1:1-6 (Step One)" \
    "啟示的次序·第一步：神先開口，從萬有說起，再縮到祂自己的家——全地、猶大、一個一個不尋求的人。" \
    "**除滅**——範圍一路縮小" \
    "4節「我必伸手攻擊猶大和耶路撒冷的一切居民」" \
    "我聽見「萬類」的時候，想到的是誰？"
add_chapter 01

add_volume "第二章 · 西番雅書 1:7-13 (Step Two)" \
    "啟示的次序·第二步：日子近了，神親自巡查——要人靜默，預備祭物，用燈搜查那些心裏說「耶和華必不降福，也不降禍」的人。" \
    "**近**、**燈**——親自來，不是遠遠下令" \
    "12節「我必用燈巡查耶路撒冷」" \
    "我有沒有哪一處，是自以為神看不到的？"
add_chapter 02

add_volume "第三章 · 西番雅書 1:14-18 (Step Two)" \
    "啟示的次序·第二步（續）：「近」兩次（1:14；全書共三次），六個「……的日子」；金銀不能救；1:18 的火，將在 3:8 再出現。" \
    "**六個「日子」**；**近**×3" \
    "14節「耶和華的大日臨近，臨近而且甚快」" \
    "我倚靠的，是不是能在那日救我的？"
add_chapter 03

add_volume "卷二 · 尋求與四方 (Volume Two: Seek, and the Four Directions)" \
    "啟示的次序·第三步：西番雅書第2章——在日子之前，先開一道門；然後審判推向西、東、南、北。"

add_volume "第四章 · 西番雅書 2:1-3 (Step Three)" \
    "啟示的次序·第三步：在日子之前先開一道門——聚集、尋求，並一個「或者」；1:6 的「不尋求」得到三個「尋求」的回答。" \
    "**尋求**×3；**或者**" \
    "3節「你們都當尋求耶和華！當尋求公義謙卑」" \
    "我今天向神動身了嗎？"
add_chapter 04

add_volume "第五章 · 西番雅書 2:4-15 (Step Three)" \
    "啟示的次序·第三步（續）：審判推向四方——西邊非利士、東邊摩押亞捫、南邊古實、北邊亞述；最後一座城說「惟有我，除我以外再沒有別的」。" \
    "**四方**——西、東、南、北" \
    "15節「惟有我，除我以外再沒有別的」" \
    "我心裏有沒有一句「惟有我」？"
add_chapter 05

add_volume "卷三 · 城與其中的神 (Volume Three: The City and the God in Her Midst)" \
    "啟示的次序·第四、五步：西番雅書第3章——回到那座城；她不親近，祂在中間；等候之後，是歌唱。"

add_volume "第六章 · 西番雅書 3:1-7 (Step Four)" \
    "啟示的次序·第四步：回到那座城——她不聽、不領受、不倚靠、不親近；耶和華卻在她中間，每早晨顯明公義。" \
    "**親近**×1；**在她中間**" \
    "5節 耶和華在那城中間是公義的" \
    "我「不親近」的，是哪一件事？"
add_chapter 06

add_volume "第七章 · 西番雅書 3:8-13 (Step Five)" \
    "啟示的次序·第五步：等候——同一句火再出現（3:8＝1:18），之後是清潔的言語，與留在你中間的困苦貧寒的民。" \
    "**等候**；**清潔的言語**；**留下**" \
    "8節「你們要等候我」" \
    "我願意等候嗎？"
add_chapter 07

add_volume "第八章 · 西番雅書 3:14-20 (Step Five)" \
    "啟示的次序·第五步，也是全書的終點：祂在你中間，歡欣、默然愛、歡呼，並且招聚；全書最後一個詞是「耶和華」。" \
    "**在你中間**——全書最後的安慰" \
    "17節「他在你中間必因你歡欣喜樂，默然愛你」" \
    "我相信祂為我歡呼嗎？"
add_chapter 08

# ============================================================
# 卷末 · 全書領受總綱
# ============================================================
add_volume "卷末 · 回望 (Looking Back)" \
    "八章讀完，把全書的領受收攏成一張圖——日子近了，祂在你中間。"

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

echo "🔨 Generating PDF with zephaniah.latex template..."

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
