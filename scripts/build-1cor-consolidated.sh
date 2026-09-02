#!/bin/bash

# 1 Corinthians PDF Builder — CONSOLIDATED 2026 EDITION
# Rebuilt to the Gospel of John standard (the series reference):
#   preface → 卷首·定位 → 全書領受總綱 → 五卷 16 單元 → 卷末 → 跋
# Uses templates/pdf/1cor.latex.
#
# Replaces the older scripts/build-1cor.sh, which concatenated the overview
# plus 16 loose chapters with no volume structure, no front/back matter, and
# no build verification.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/1cor"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/1cor-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/1cor-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/1cor.latex"

echo "=========================================="
echo "📜 1 Corinthians Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "哥林多前書研讀"
subtitle: "1 Corinthians Deep Study — 十字架的道理，是神的大能"
author: "PubHub 三書精讀系統"
date: "2026年8月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **週四查經班** — 第一手屬靈教導

  • **John MacArthur** — 逐節解經 (gty.org)

  • **G. Campbell Morgan** — 屬靈組織分析法

  **全書骨幹 = 十字架的道理 + 復活的盼望**

  紛爭與十字架的智慧 (1-4) | 紀律與身體的聖潔 (5-7) | 自由、良心與榜樣 (8-10)
  聚會的次序與恩賜 (11-14) | 復活的盼望與收尾 (15-16)

  **經文版權聲明 (Scripture Copyright Notices)**

  本版為教會內部贈閱版（非賣品）；公開發行時另行申請 ISBN。

  中文經文引自《聖經》和合本（1919），屬公有領域。

  Scripture quotations taken from the New American Standard Bible® (NASB),
  Copyright © 1960, 1971, 1977, 1995 by The Lockman Foundation. Used by
  permission. All rights reserved. lockman.org

  All rights reserved.
---

HEADER

chapter_count=0

# Append one source file. Sources are mixed: the front/back-matter files carry
# a YAML header of varying length, the 16 chapter files carry one too — so
# detect and strip it rather than assuming a fixed line count. Then convert
# ^n^ verse markers to \textsuperscript.
add_file() {
    local f="$1"
    [ -f "$f" ] || return 0
    echo "  Adding: $(basename "$f")"
    local start=1
    if [ "$(head -n 1 "$f")" = "---" ]; then
        start=$(( $(awk 'NR>1 && /^---$/{print NR; exit}' "$f") + 1 ))
    fi
    tail -n +$start "$f" | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Front/back matter: same as add_file, but marks the file's first `# ` heading
# {.unnumbered}. Without this the preface, orientation chapters and appendices
# consume chapter numbers, so 第一章 prints as "Chapter 8" and its sections as
# 8.1, 8.2 — visible only in the rendered PDF.
add_front() {
    local f="$1"
    [ -f "$f" ] || return 0
    echo "  Adding (unnumbered): $(basename "$f")"
    local start=1
    if [ "$(head -n 1 "$f")" = "---" ]; then
        start=$(( $(awk 'NR>1 && /^---$/{print NR; exit}' "$f") + 1 ))
    fi
    tail -n +$start "$f" | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}/g' \
      | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}"; done=1 } } {print}' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Volume divider: a part-title page carrying the volume's theme.
add_volume() {
    printf '# %s {.unnumbered}\n\n> %s\n' "$1" "$2" >> "$COMBINED_MD"
    printf '\n\\newpage\n\n' >> "$COMBINED_MD"
    echo "  --- $1"
}

# 前言
add_front "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀哥林多前書之前先站遠一點：這封信為何而寫，它在保羅書信中站在哪裡，全書的骨幹是哪一條線。"

add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-1cor-position.md"
add_front "$INPUT_DIR/00b-cross-spine.md"

# 全書領受總綱
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
    tail -n +8 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 五卷 · 16 單元
# ============================================================
add_volume "卷一 · 紛爭與十字架的智慧 (Division and the Wisdom of the Cross) · 1-4 章" \
    "教會分成四派，保羅沒有去調解四派，他問了一句：「基督是分開的嗎？」——他不處理糾紛，他處理糾紛底下的東西。"
for i in 01 02 03 04; do add_file "$INPUT_DIR/ch$i.md"; done

add_volume "卷二 · 教會的紀律與身體的聖潔 (Discipline and Holiness) · 5-7 章" \
    "三件難堪的事——容讓淫亂、彼此告狀、婚姻的難處——結論都繫在同一句話上：「你們是重價買來的。」"
for i in 05 06 07; do add_file "$INPUT_DIR/ch$i.md"; done

add_volume "卷三 · 自由、良心與榜樣 (Freedom, Conscience and Example) · 8-10 章" \
    "保羅同意他們的知識是對的，然後用三章告訴他們：對，不等於該。"
for i in 08 09 10; do add_file "$INPUT_DIR/ch$i.md"; done

add_volume "卷四 · 聚會的次序與恩賜 (Order and Gifts in Worship) · 11-14 章" \
    "四章講聚會，一把尺量到底：造就。而第十三章夾在中間，是這把尺的來源。"
for i in 11 12 13 14; do add_file "$INPUT_DIR/ch$i.md"; done

add_volume "卷五 · 復活的盼望與收尾 (Resurrection and Closing) · 15-16 章" \
    "復活放在最後，不是因為它最不重要，是因為它托住前面的一切——而結論是一個非常實際的命令。"
for i in 15 16; do add_file "$INPUT_DIR/ch$i.md"; done

# ============================================================
# 卷末
# ============================================================
add_volume "卷末 · 直等到他來 (Until He Comes)" \
    "十六章，十來類問題，一把尺。而全書最後一句呼喊，是最早期教會的原話：「主必要來！」"
add_front "$INPUT_DIR/99-until-he-comes.md"

# 附錄 — 引用出處與查證狀態
add_front "$INPUT_DIR/99-appendix-references.md"

# 跋 — last content file: no trailing \newpage, which would otherwise leave a
# header-only blank page whenever the afterword fills its final page exactly.
if [ -f "$INPUT_DIR/999-afterword.md" ]; then
    echo "  Adding: 999-afterword.md"
    tail -n +8 "$INPUT_DIR/999-afterword.md" \
      | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}"; done=1 } } {print}' >> "$COMBINED_MD"
    ((chapter_count++))
fi

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count units)"
echo ""
echo "🔨 Generating PDF with 1cor.latex template..."

# --verbose is load-bearing, not chatter: without it pandoc swallows the whole
# xelatex log and every grep-the-log check (here and in driver.sh) passes
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
