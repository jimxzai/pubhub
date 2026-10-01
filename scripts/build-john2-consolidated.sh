#!/bin/bash

# 2 John (約翰二書) PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine) + 全書領受總綱 + 五卷 9 章 + 卷末 + 跋
# Uses templates/pdf/john2.latex (InkNavy/ThresholdSlate/LoveCrimson theme;
# base copied from ruth.latex — cover art, frontispiece, five-volume diagram)
#
# Book-level spine (00b-revelation-order.md): 住 → 行 → 辨 → 守 → 見
#   卷一 住 1-3節 (ch 01-02) | 卷二 行 4-6節 (ch 03-04) | 卷三 辨 7-9節 (ch 05-07)
#   卷四 守 10-11節 (ch 08)  | 卷五 見 12-13節 (ch 09)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/john2"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/john2-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/john2-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/john2.latex"

echo "=========================================="
echo "📜 2 John Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "約翰二書研讀"
subtitle: "2 John Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年10月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **歷代注疏資源整合**（詳見書中〈附錄：參考資料〉）

  **住、行、辨、守、見：真理住進來、被活出來、被試驗、劃出家門的界線，終於面對面**

  卷一 · 住 (1-3節) | 卷二 · 行 (4-6節) | 卷三 · 辨 (7-9節)
  卷四 · 守 (10-11節) | 卷五 · 見 (12-13節)

  **經文版權聲明 (Scripture Copyright Notices)**

  本版為教會內部贈閱版（非賣品）；公開發行時另行申請 ISBN。

  中文經文引自《聖經》和合本（1919），屬公有領域。

  Scripture quotations marked (NASB) are from the NEW AMERICAN STANDARD
  BIBLE®, Copyright © 1960, 1962, 1963, 1968, 1971, 1972, 1973, 1975, 1977,
  1995 by The Lockman Foundation. Used by permission. www.Lockman.org.
  All rights reserved.
---

HEADER

chapter_count=0

# Append one source file: strip its 7-line YAML front matter, convert ^n^ verse
# markers to \textsuperscript, then start a new page.
add_file() {
    local f="$1"
    [ -f "$f" ] || { echo "❌ Missing: $f — aborting build"; exit 1; }
    echo "  Adding: $(basename "$f")"
    tail -n +8 "$f" | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Front/back matter: same as add_file but marks the H1 {.unnumbered}, so the
# preface, orientation chapters and dividers do not consume chapter numbers
# ahead of the book's own 第1章 (same approach as build-ruth-consolidated.sh).
add_front() {
    local f="$1"
    [ -f "$f" ] || { echo "❌ Missing: $f — aborting build"; exit 1; }
    echo "  Adding (unnumbered): $(basename "$f")"
    tail -n +8 "$f" | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}/g' \
      | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}" ; done=1 } } {print}' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Volume divider: a part-title page carrying the volume's step on the spine.
# Descriptions are single paragraphs (no literal \n), so %s is safe here; use
# %b if a multi-paragraph description is ever needed (see acts/judges/job).
add_volume() {
    printf '# %s {.unnumbered}\n\n> %s\n' "$1" "$2" >> "$COMBINED_MD"
    printf '\n\\newpage\n\n' >> "$COMBINED_MD"
    echo "  --- $1"
}

# 前言 — preface
add_front "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位 — orientation: overview, position, spine
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這幾章：總覽、位置、骨幹。"

add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-2john-position.md"
add_front "$INPUT_DIR/00b-revelation-order.md"

# Systematic reception — demote headings one level so it reads as one chapter.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
    tail -n +9 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 五卷 · 9 章
# ============================================================
add_volume "卷一 · 住：真理住進來 (Abide) · 約翰二書 1-3節" \
    "啟示的次序·第一步——神先給，後吩咐：作長老的在真理中愛這一家人，因為真理存在我們裏面，也必永遠同在；恩惠、憐憫、平安不是祝願，而是「必常與我們同在」的應許。"
add_file "$INPUT_DIR/01-the-elder-and-the-elect-lady.md"
add_file "$INPUT_DIR/02-grace-mercy-peace.md"

add_volume "卷二 · 行：在真理與愛中行 (Walk) · 約翰二書 4-6節" \
    "啟示的次序·第二步——住進來的真理被活出來：長老看見兒女中有遵行真理的，就甚歡喜；他不頒新命令，只提醒那從起初的命令——照他的命令行，這就是愛。"
add_file "$INPUT_DIR/03-walking-in-truth.md"
add_file "$INPUT_DIR/04-the-commandment-from-the-beginning.md"

add_volume "卷三 · 辨：成了肉身的基督 (Discern) · 約翰二書 7-9節" \
    "啟示的次序·第三步——真理被試驗：試金石不是一套體系，而是成了肉身來的耶穌基督；迷惑人的越過基督的教訓，就沒有神，常守這教訓的，就有父又有子。全信五步都繞著這一步轉。"
add_file "$INPUT_DIR/05-come-in-the-flesh.md"
add_file "$INPUT_DIR/06-lose-not-the-work.md"
add_file "$INPUT_DIR/07-abide-in-the-teaching.md"

add_volume "卷四 · 守：家門的界線 (Guard) · 約翰二書 10-11節" \
    "啟示的次序·第四步——真理劃出門檻：門是到這一步才關上的；一個被真理和愛充滿的家，不把傳另一位基督的人接進來，也不向他說「願你喜樂」。"
add_file "$INPUT_DIR/08-the-door-of-the-house.md"

add_volume "卷五 · 見：面對面 (See) · 約翰二書 12-13節" \
    "啟示的次序·第五步——真理的終點是同在：長老不願用紙墨，盼望當面談論，使喜樂滿足；全信不停在關上的門，而停在打開的面。"
add_file "$INPUT_DIR/09-face-to-face.md"

# ============================================================
# 卷末
# ============================================================
add_volume "卷末 · 回看五步 (Looking Back)" \
    "十三節從真理住進來起頭，走過行、辨、守，停在一次面對面的探望。"
add_front "$INPUT_DIR/99-epilogue.md"

# 附錄：參考資料 — every chapter's 體例說明 box points here; it must be in the
# printed book, not just a repo file read by check-citation-ledger.py.
add_front "$INPUT_DIR/99-appendix-references.md"

# 跋 — afterword. Last content file: no trailing \newpage.
echo "  Adding (unnumbered): 999-afterword.md"
tail -n +8 "$INPUT_DIR/999-afterword.md" \
  | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}" ; done=1 } } {print}' >> "$COMBINED_MD"
((chapter_count++))

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters)"
echo ""
echo "🔨 Generating PDF with john2.latex template..."

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
