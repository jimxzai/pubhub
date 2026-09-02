#!/bin/bash

# Hebrews PDF Builder — CONSOLIDATED 2026 EDITION
# Rebuilt to the Gospel of John standard (the series reference):
#   前言 → 卷首·定位 → 全書領受總綱 → 五卷 13 章 → 卷末 → 跋 → 附錄
# Sources from books/bible/hebrews/, uses templates/pdf/hebrews.latex
# (Royal Purple/Gold priestly theme; the back cover carries the blurb).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/hebrews"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
REFS_FILE="$INPUT_DIR/99-appendix-references.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/hebrews-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/hebrews-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/hebrews.latex"

echo "=========================================="
echo "📖 Hebrews PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "希伯來書研讀"
subtitle: "Hebrews Deep Study — 更美的中保，一次獻上就坐下了"
author: "PubHub 三書精讀系統"
date: "2026年8月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **週四查經班** — 整本聖經脈絡的深度領受

  • **John MacArthur** — 逐節解經講道 (gty.org)

  • **G. Campbell Morgan** — 屬靈組織分析 (*God's Last Word to Man*)

  **全書骨幹 = 更美 (κρείττων) + 五段警告 + 一次 (ἐφάπαξ)**

  更美的啟示 (1-4) | 更美的大祭司 (5-7) | 更美之約與更美的祭 (8-10)
  信心與奔跑 (11-12) | 營外的生活 (13)

  **經文版權聲明 (Scripture Copyright Notices)**

  本版為教會內部贈閱版（非賣品）；公開發行時另行申請 ISBN。

  中文經文引自《聖經》和合本（1919），屬公有領域，十三章全文逐節收錄，
  並經 [ai-eden.com/bible](https://www.ai-eden.com/bible) 核對。

  英文經文引自 New American Standard Bible (NASB, 1995)，十三章全文逐節
  收錄，與中文逐段對照；舊約引文依 NASB 體例排作小型大寫字。詳見卷首〈凡例〉。

  **全卷引用之書面授權正在向 The Lockman Foundation 申請中，公開發行前完成。**

  Scripture quotations taken from the New American Standard Bible® (NASB),
  Copyright © 1960, 1971, 1977, 1995 by The Lockman Foundation.
  All rights reserved. www.Lockman.org

  Written permission for the full-book quotation in this volume has been
  applied for and is pending; this edition is for internal church
  distribution and is not for sale.

  All rights reserved.
---

HEADER

chapter_count=0

# Append one source file. All sources carry a 7-line YAML header; strip it only
# when it is actually there, then convert ^n^ verse markers to \textsuperscript.
add_file() {
    local f="$1"
    if [ ! -f "$f" ]; then
        echo "❌ Missing source file: $f — aborting build"
        exit 1
    fi
    echo "  Adding: $(basename "$f")"
    local start=1
    if [ "$(head -n 1 "$f")" = "---" ]; then
        start=$(( $(awk 'NR>1 && /^---$/{print NR; exit}' "$f") + 1 ))
    fi
    tail -n +$start "$f" | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Same as add_file, but marks the file's first H1 {.unnumbered}. Without this
# LaTeX numbers EVERY chapter sequentially, so the preface, three orientation
# chapters, the systematic-study essay and the seven divider pages consume
# numbers 1-12 and the book's own 第一章 comes out as LaTeX chapter 13 — the
# contents page then reads "13  基督超越天使", two conflicting numbers on one
# line. Marking these unnumbered lets the 13 chapters number 1-13.
add_front() {
    local f="$1"
    if [ ! -f "$f" ]; then
        echo "❌ Missing source file: $f — aborting build"
        exit 1
    fi
    echo "  Adding (unnumbered): $(basename "$f")"
    local start=1
    if [ "$(head -n 1 "$f")" = "---" ]; then
        start=$(( $(awk 'NR>1 && /^---$/{print NR; exit}' "$f") + 1 ))
    fi
    tail -n +$start "$f" | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}/g' \
      | awk 'BEGIN{d=0} /^# /{ if(!d){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}"; d=1 } } {print}' \
      >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Volume divider: a part-title page carrying the volume's theme.
add_volume() {
    printf '# %s {.unnumbered}\n\n> %s\n' "$1" "$2" >> "$COMBINED_MD"
    printf '\n\\newpage\n\n' >> "$COMBINED_MD"
    echo "  --- $1"
}

add_chapter() {
    local found=""
    for f in "$INPUT_DIR/$1-"*.md; do
        [ -f "$f" ] || continue
        add_file "$f"; found=1; break
    done
    if [ -z "$found" ]; then
        echo "❌ Missing chapter file for prefix '$1-' in $INPUT_DIR — aborting build"
        exit 1
    fi
}

# 前言
add_front "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀希伯來書之前先站遠一點：這封「勸勉的話」為誰而寫，它在正典中站在哪裏，全書的骨幹是哪一條線。"

add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-hebrews-position.md"
add_front "$INPUT_DIR/00b-better-spine.md"

# 全書領受總綱
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
    tail -n +8 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 五卷 · 13 章
# ============================================================
add_volume "卷一 · 更美的啟示 (A Better Word) · 1:1-4:13" \
    "神說話的方式已經改變——從「多次多方藉著眾先知」，到「藉著他兒子」。這一卷處理的是：你聽的是誰？"
for i in 01 02 03 04; do add_chapter "$i"; done

add_volume "卷二 · 更美的大祭司 (A Better Priest) · 4:14-7:28" \
    "亞倫的祭司體系不是敗在腐敗上，是敗在葬禮上。這一卷處理的是：你的中保會不會有一天辦葬禮？"
for i in 05 06 07; do add_chapter "$i"; done

add_volume "卷三 · 更美之約與更美的祭 (A Better Covenant, A Better Sacrifice) · 8:1-10:39" \
    "舊約的至聖所裏沒有椅子，祭司永遠站著。這一卷處理的是：那位大祭司為甚麼坐下了？"
for i in 08 09 10; do add_chapter "$i"; done

add_volume "卷四 · 信心與奔跑 (Faith and the Race) · 11:1-12:29" \
    "信心堂的名單不是成功者名冊——後半是「因著信……沒有得著」。這一卷處理的是：沒有得著所應許的，還算信心嗎？"
for i in 11 12; do add_chapter "$i"; done

add_volume "卷五 · 營外的生活 (Outside the Camp) · 13:1-25" \
    "十二章的道理，最後只換來一個方位詞。這一卷處理的是：這一切，把你的腳帶到哪裏？"
add_chapter 13

# ============================================================
# 卷末
# ============================================================
add_volume "卷末 · 全書的落點 (Where It All Lands)" \
    "敬畏、倚靠、良心、眼睛、腳——這卷書是一路往下走的：從你抬頭看的地方，走到你站著的地方。"
add_front "$INPUT_DIR/99-outside-the-camp.md"

# 跋
add_front "$INPUT_DIR/999-afterword.md"

# 附錄一～五：參考資料、經文索引、希臘文詞彙表、徵引書目、人名索引
# The index and glossary are generated from the chapter sources by
# scripts/gen-hebrews-apparatus.py — regenerate them after editing any chapter.
add_volume "附錄 (Appendices)" \
    "參考資料與核實狀態、經文索引、希臘文詞彙表、徵引書目、人名索引——供查考與備課之用。"
add_front "$REFS_FILE"
add_front "$INPUT_DIR/99a-scripture-index.md"
add_front "$INPUT_DIR/99b-greek-glossary.md"
add_front "$INPUT_DIR/99c-bibliography.md"
add_front "$INPUT_DIR/99d-name-index.md"

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count units)"
echo ""
echo "🔨 Generating PDF with hebrews.latex template..."

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
