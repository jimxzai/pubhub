#!/bin/bash

# Ruth PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine) + 全書領受總綱 + 四卷 13 段 + 卷末 + 跋
# Uses templates/pdf/ruth.latex (FieldAmber/DuskIndigo/DawnRose theme, matching
# the Gospel of John / Acts of the Apostles / Isaiah / Job series standard:
# cover art, frontispiece)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/ruth"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/ruth-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/ruth-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/ruth.latex"

echo "=========================================="
echo "🌾 Ruth Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "路得記研讀"
subtitle: "Ruth Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年9月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合**（詳見書中〈附錄：參考資料〉）

  **從空到滿：饑荒中的離散、拾穗禾場的恩待、禾場夜求贖、贖回與家譜**

  卷一 · 空：破碎與離散 (第1章) | 卷二 · 遇：拾穗與恩待 (第2章)
  卷三 · 求：禾場夜求贖 (第3章) | 卷四 · 滿：贖回與家譜 (第4章)

  **經文版權聲明 (Scripture Copyright Notices)**

  本版為教會內部贈閱版（非賣品）；公開發行時另行申請 ISBN。

  中文經文引自《聖經》和合本（1919），屬公有領域。

  Scripture quotations marked (NASB) are from the NEW AMERICAN STANDARD
  BIBLE®, Copyright © 1960, 1962, 1963, 1968, 1971, 1972, 1973, 1975, 1977,
  1995 by The Lockman Foundation. Used by permission. www.Lockman.org.
  All rights reserved.

  All rights reserved.
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
# numbers on one line. Marking these unnumbered lets the 13 study units number
# 1-13. Same approach as build-job-consolidated.sh / build-isaiah-consolidated.sh.
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
add_front "$INPUT_DIR/00a-ruth-position.md"
add_front "$INPUT_DIR/00b-redemption-spine.md"

# Systematic reception — demote headings one level so it reads as one chapter.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
    tail -n +2 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 四卷 · 13 段
# ============================================================
add_volume "卷一 · 空：破碎與離散 (Emptied) · 路得記 1章" \
    "全書骨幹·第一步——救贖者尚未出現，神的護理只藏在沉默的空裏：饑荒逼遷摩押，丈夫兒子相繼離世，拿俄米空手空心歸回伯利恆，路得卻立誓不離不棄。"
for f in 01-*.md 02-*.md 03-*.md; do
    for match in "$INPUT_DIR"/$f; do
        [ -f "$match" ] && add_chapter "$(basename "$match")"
    done
done

add_volume "卷二 · 遇：拾穗與恩待 (Encountered) · 路得記 2章" \
    "全書骨幹·第二步——至近的親屬（גֹּאֵל go'el）第一次被認出：路得下田拾穗，「恰巧」來到波阿斯的田，恩待悄悄開始。"
for f in 04-*.md 05-*.md 06-*.md; do
    for match in "$INPUT_DIR"/$f; do
        [ -f "$match" ] && add_chapter "$(basename "$match")"
    done
done

add_volume "卷三 · 求：禾場夜求贖 (Sought) · 路得記 3章" \
    "全書骨幹·第三步——認出救贖者之後，照著律法正式求贖：拿俄米定計，路得夜叩禾場，求波阿斯用衣襟遮蓋，等候天亮見分曉。"
for f in 07-*.md 08-*.md 09-*.md; do
    for match in "$INPUT_DIR"/$f; do
        [ -f "$match" ] && add_chapter "$(basename "$match")"
    done
done

add_volume "卷四 · 滿：贖回與家譜 (Filled) · 路得記 4章" \
    "全書骨幹·第四步——救贖依法完成，血脈直通基督：波阿斯城門前贖回產業與路得，孩子出生，家譜直通大衛，從空手到滿懷。"
for f in 10-*.md 11-*.md 12-*.md 13-*.md; do
    for match in "$INPUT_DIR"/$f; do
        [ -f "$match" ] && add_chapter "$(basename "$match")"
    done
done

# ============================================================
# 卷末 · 從空到滿
# ============================================================
add_volume "卷末 · 從空到滿 (From Empty to Full)" \
    "全書從饑荒中的空手起頭，走過拾穗禾場的恩待與禾場夜的求贖，最終停在滿懷的家譜——這條路沒有一步繞過忠誠與委身。"
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
echo "🔨 Generating PDF with ruth.latex template..."

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
