#!/bin/bash

# 3 John PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine) + 全書領受總綱 + 五卷 9 章 + 卷末 + 跋
# Uses templates/pdf/john3.latex (TruthTeal/ShutSlate/LampGold theme, matching
# the Ruth / Job / Isaiah series standard: cover art, frontispiece).
# Modelled on scripts/build-john3-consolidated.sh.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/john3"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/john3-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/john3-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/john3.latex"

echo "=========================================="
echo "📜 3 John Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "約翰三書研讀"
subtitle: "3 John Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年10月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **注疏資源**：馬太·亨利、韋斯科特、普盧默、摩根、麥克阿瑟（逐字核校，詳見書中〈附錄：引用出處總表〉）

  **一扇門，一個名字：真理在先、為那名出外、關上的門、真理作見證、面對面**

  卷一 · 在真理中 (1-4節) | 卷二 · 為那名出外 (5-8節) | 卷三 · 關上的門 (9-10節)
  卷四 · 真理作見證 (11-12節) | 卷五 · 面對面 (13-15節)

  **經文版權聲明 (Scripture Copyright Notices)**

  本版為教會內部贈閱版（非賣品）；公開發行時另行申請 ISBN。

  中文經文引自《聖經》和合本（1919），屬公有領域。

  Scripture quotations marked (NASB) are from the NEW AMERICAN STANDARD
  BIBLE®, Copyright © 1960, 1962, 1963, 1968, 1971, 1972, 1973, 1975, 1977,
  1995 by The Lockman Foundation. Used by permission. www.Lockman.org.
  All rights reserved.

  希臘文據 SBL Greek New Testament (SBLGNT)，MorphGNT 詞法標記（CC BY-SA）。
---

HEADER

chapter_count=0

# Append one source file: strip its 7-line YAML front matter, convert ^n^ verse
# markers to \textsuperscript, then start a new page.
add_file() {
    local f="$1"
    [ -f "$f" ] || return 0
    echo "  Adding: $(basename "$f")"
    tail -n +8 "$f" | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Volume divider: a part-title page carrying the volume's theme.
# Front/back matter and volume dividers: same as add_file but marks the H1
# {.unnumbered}. Without this LaTeX numbers EVERY chapter sequentially, so the
# preface, orientation chapters and the volume divider pages consume numbers
# ahead of the book's own 第一章, and the contents page reads two conflicting
# numbers on one line. Marking these unnumbered lets the 9 study units number
# 1-9. Same approach as build-job-consolidated.sh / build-isaiah-consolidated.sh.
add_front() {
    local f="$1"
    [ -f "$f" ] || return 0
    echo "  Adding (unnumbered): $(basename "$f")"
    tail -n +8 "$f" | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}/g' \
      | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}" ; done=1 } } {print}' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

add_volume() {
    printf '# %s {.unnumbered}\n\n> %s\n' "$1" "$2" >> "$COMBINED_MD"
    if [ -n "$3" ]; then
        printf '\n| %s | %s |\n|---|---|\n' "$3" "$4" >> "$COMBINED_MD"
    fi
    printf '\n\\newpage\n\n' >> "$COMBINED_MD"
    echo "  --- $1"
}

# Append the file matching an exact chapter filename (no combined-file globbing —
# every chapter is its own file).
add_chapter() {
    add_file "$INPUT_DIR/$1"
}

# 前言 — preface
add_front "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位 — orientation: overview, position, spine
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這幾章：總覽、位置、骨幹。"

add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-john3-position.md"
add_front "$INPUT_DIR/00b-truth-spine.md"

# Systematic reception — demote headings one level so it reads as one chapter.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
    tail -n +2 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

add_range() {
    for f in "$@"; do
        for match in "$INPUT_DIR"/$f; do
            [ -f "$match" ] && add_chapter "$(basename "$match")"
        done
    done
}

# ============================================================
# 正文 · 五卷 · 9 章
# ============================================================
add_volume "卷一 · 在真理中 (In the Truth) · 約翰三書 1-4節" \
    "啟示的次序·第一步——真理在先：長老在真理中愛該猶，最大的喜樂是聽見兒女們按真理而行。先有真理，後有愛；愛是在真理裏面的愛。"
add_range "01-*.md" "02-*.md"

add_volume "卷二 · 為那名出外 (For the Sake of the Name) · 約翰三書 5-8節" \
    "啟示的次序·第二步——真理被差出去：弟兄們為那名出外，對外邦人一無所取；開門接待的家，就與真理一同做工。"
add_range "03-*.md" "04-*.md"

add_volume "卷三 · 關上的門 (The Shut Door) · 約翰三書 9-10節" \
    "啟示的次序·第三步——真理被拒絕：好為首的丟特腓不接待使徒，也不接待弟兄，還把接待的人趕出教會——約翰福音 1:11 在教會裏重演。"
add_range "05-*.md" "06-*.md"

add_volume "卷四 · 真理作見證 (Witnessed by the Truth) · 約翰三書 11-12節" \
    "啟示的次序·第四步——真理親自作見證：不要效法惡，只要效法善；低米丟有眾人、有真理、有使徒為他作見證，最後的判斷屬於真理本身。"
add_range "07-*.md" "08-*.md"

add_volume "卷五 · 面對面 (Face to Face) · 約翰三書 13-15節" \
    "啟示的次序·第五步——終點是面對面：紙墨讓位給同在，名單讓位給名字；那位按著名叫自己羊的牧人，是這封信最後的落點。"
add_range "09-*.md"

# ============================================================
# 卷末 · 一扇門，一個名字
# ============================================================
add_volume "卷末 · 一扇門，一個名字 (One Door, One Name)" \
    "全書從「在真理中所愛的」起頭，走過為那名出外、關上的門與真理的見證，停在「按著姓名」——每一扇門外站的，都是為那名而來的人。"
add_front "$INPUT_DIR/99-epilogue.md"

# 附錄：參考資料 — every chapter's 體例說明 box points here ("見卷末《附錄：
# 引用出處總表》"); it must actually be in the printed book, not just exist
# as a repo file used by check-citation-ledger.py.
add_front "$INPUT_DIR/99-appendix-references.md"

# 跋 — afterword. Last content file: no trailing \newpage.
if [ -f "$INPUT_DIR/999-afterword.md" ]; then
    echo "  Adding (unnumbered): 999-afterword.md"
    tail -n +8 "$INPUT_DIR/999-afterword.md" \
      | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}" ; done=1 } } {print}' >> "$COMBINED_MD"
    ((chapter_count++))
fi

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters)"
echo ""
echo "🔨 Generating PDF with john3.latex template..."

# --verbose is load-bearing, not chatter: without it pandoc swallows the whole
# xelatex log and every grep-the-log check below (and in driver.sh) passes
# vacuously. See scripts/lib/latex-check.sh for the full explanation.
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
  --top-level-division=chapter \
  -V tocdepth=0 > "$LATEX_LOG" 2>&1
PANDOC_EXIT=$?

latex_build_report "$PANDOC_EXIT" "$LATEX_LOG" "$OUTPUT_PDF" || exit 1
