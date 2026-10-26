#!/bin/bash

# Ecclesiastes PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine/order) + 全書領受總綱 + 四卷 12 章 + 卷末 + 附錄 + 跋
# Uses templates/pdf/ecclesiastes.latex (Dusk/Ochre/Rose theme, derived from nehemiah.latex)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/ecclesiastes"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/ecclesiastes-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/ecclesiastes-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/ecclesiastes.latex"

echo "=========================================="
echo "Ecclesiastes Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "傳道書研讀"
subtitle: "Ecclesiastes Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年10月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **主要參考資料整合：**

  • **Matthew Henry** — Commentary on the Whole Bible

  • **Charles Bridges** — An Exposition of the Book of Ecclesiastes (1860)

  • **G. Campbell Morgan** — Living Messages of the Books of the Bible

  • **John MacArthur** — 《研讀本聖經》傳道書導論；gty.org 講章與部落格（零星引用，非逐節講道；各條標明出處）

  • **Gregory Thaumaturgus** — A Metaphrase of the Book of Ecclesiastes（ANF vol. 6，公有領域；傳為其作）

  • **巴比倫塔木德 Shabbat 30b** — William Davidson Edition 英譯（Sefaria.org，CC-BY-NC）

  • **希伯來文** — Miqra according to the Masorah（MAM，以亞勒坡抄本為本；取自 Sefaria.org，CC-BY-SA）

  **試、時、問、歸——十二章經文，十二篇研讀**

  卷一：試 (1-2章) | 卷二：時 (3-6章)

  卷三：問 (7-10章) | 卷四：歸 (11-12章)

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
    [ -f "$f" ] || return 0
    echo "  Adding: $(basename "$f")"
    tail -n +8 "$f" | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Front/back matter and volume dividers: same as add_file but marks the H1
# {.unnumbered}. Without this LaTeX numbers EVERY chapter sequentially, so the
# preface, orientation chapters and the four volume divider pages consume
# numbers ahead of the book's own 第一章, and the contents page reads two
# conflicting numbers on one line. Marking these unnumbered lets the 12 study
# units number 1-12, matching the chapter files. Same approach as
# build-nehemiah-consolidated.sh / build-job-consolidated.sh.
add_front() {
    local f="$1"
    [ -f "$f" ] || return 0
    echo "  Adding (unnumbered): $(basename "$f")"
    tail -n +8 "$f" | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}/g' \
      | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}" ; done=1 } } {print}' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Volume divider: a part-title page carrying the volume's theme.
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
# 卷首 · 定位 — orientation: overview, position, spine, order
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這幾章：總覽、位置、骨幹、啟示的次序，以及全書領受總綱。"

add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-ecclesiastes-position.md"
add_front "$INPUT_DIR/00b-vanity-spine.md"
add_front "$INPUT_DIR/00c-revelation-order.md"

# Systematic reception — demote headings one level so it reads as one chapter.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
    tail -n +10 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 四卷 · 12 章
# ============================================================
add_volume "卷一 · 試 (Tried) · 1-2章" \
    "一位王把智慧、享樂與工程一樣一樣試過，每一樣都問同一句：有甚麼益處？神第一次出場是一份沉重的差事（1:13），第二次是一隻手（2:24）。**啟示的次序**：第 1 步 · 神給了一份差事，也給了一隻手——人在日光之下試遍一切，找不到益處（1:13；2:24-26）。"
for f in 01-vanity-of-vanities.md 02-the-kings-experiment.md; do
    add_chapter "$f"
done

add_volume "卷二 · 時 (Times) · 3-6章" \
    "凡事都有定時；冤屈、孤單、敬拜、財富，一章一章攤開在日光之下。**啟示的次序**：第 2 步 · 神定了時候，又把永遠放在人心裏，卻不讓人看全（3:1, 11）——四章的見聞，都在這條界線之內。"
for f in 03-a-time-for-everything.md 04-two-are-better-than-one.md \
         05-guard-your-steps.md 06-the-appetite-never-filled.md; do
    add_chapter "$f"
done

add_volume "卷三 · 問 (Questions) · 7-10章" \
    "智慧碰到它的邊：往遭喪的家去；義人遭難、惡人享壽；臨到眾人的事都是一樣；一隻死蒼蠅就能敗壞香膏。**啟示的次序**：第 3 步 · 神使好日子與壞日子並列（7:14）——人查不出來（8:17），然而敬畏神的，終久必得福樂（8:12）。"
for f in 07-the-house-of-mourning.md 08-who-knows-the-interpretation.md \
         09-one-event-for-all.md 10-dead-flies.md; do
    add_chapter "$f"
done

add_volume "卷四 · 歸 (Return) · 11-12章" \
    "不知道神的作為，仍要撒種；少年人快樂，卻要知道神必審問；日頭光明變為黑暗之先，當記念造你的主。**啟示的次序**：第 4 步 · 神必審問（11:9；12:14），也賜下一個牧者（12:11）；人所當盡的本分是敬畏（12:13）。"
for f in 11-cast-your-bread.md 12-remember-your-creator.md; do
    add_chapter "$f"
done

# ============================================================
# 卷末 · 全書的結束
# ============================================================
add_front "$INPUT_DIR/99-remember-your-creator.md"

# ============================================================
# 附錄 — every chapter's 體例說明 box points the reader at
# 《附錄：引用出處總表》; both appendices must be concatenated or those
# pointers dangle in the printed book (same defect Ruth and Joshua found).
# ============================================================
add_volume "附錄 (Appendices)" \
    "經文與主題索引、引用出處總表——各章「體例說明」所指的卷末附錄。"
add_front "$INPUT_DIR/98-appendix-indices.md"
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
echo "🔨 Generating PDF with ecclesiastes.latex template..."

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
