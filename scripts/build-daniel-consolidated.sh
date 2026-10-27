#!/bin/bash

# Daniel PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine/order) + 全書領受總綱 + 五卷 16 章 + 卷末 + 附錄 + 跋
# Uses templates/pdf/daniel.latex (Stone/Amber/Clay theme, matching the Gospel of
# John / Ezra / Job series standard: cover art, frontispiece)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/daniel"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/daniel-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/daniel-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/daniel.latex"

echo "=========================================="
echo "Daniel Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "但以理書研讀"
subtitle: "Daniel Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年10月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **主要參考資料整合：**

  • **John Calvin** — Commentaries on the Book of the Prophet Daniel（CCEL，公有領域英譯）

  • **Matthew Henry** — Commentary on the Whole Bible

  • **John MacArthur** — 但以理書講道系列（gty.org，27-01 至 27-31）

  • **G. Campbell Morgan** — Living Messages of the Books of the Bible（舊約卷），僅用全書概觀

  • **Hippolytus**、**Flavius Josephus**（公有領域）

  • **Sefaria** — *Miqra according to the Masorah*（希伯來文與亞蘭文經文）

  **至高者在人的國中掌權、國度是賜的不是奪的——十二章經文，十六篇研讀**

  卷一：在巴比倫立志 (1章) | 卷二：列國之王與天上的神 (2-7章)
  卷三：四獸與人子 (8-10章) | 卷四：禱告與七十個七 (11-12章)
  卷五：看不見的爭戰與結局 (13-16章)

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
# preface, orientation chapters and the five volume divider pages consume
# numbers and the book's own 第一章 comes out as a later LaTeX chapter number — the
# contents page then reads "10  第一章 · ...", two conflicting numbers on one
# line. Marking these unnumbered lets the 16 study units number 1-16,
# matching the chapter files. Same approach as build-job-consolidated.sh.
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
# 卷首 · 定位 — orientation: overview, position, spine, order
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這幾章：總覽、位置、骨幹、啟示的次序。"

add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-daniel-position.md"
add_front "$INPUT_DIR/00b-given-spine.md"
add_front "$INPUT_DIR/00c-revelation-order.md"

# Systematic reception — demote headings one level so it reads as one chapter.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
    # drop the 7-line YAML header AND the file's own H1 (replaced by the heading above), then demote the rest
    awk 'BEGIN{y=0;h=0} NR==1&&/^---/{y=1;next} y&&/^---/{y=0;next} y{next} !h&&/^# /{h=1;next} {print}' "$STUDY_FILE" \
      | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 五卷 · 16 段
# ============================================================
add_volume "卷一 · 在巴比倫立志 (Resolved in Babylon) · 1章" \
    "被擄不是巴比倫贏了，是「主將猶大王約雅敬……交付他手」；但以理在宮中立志，蒙恩惠與聰明知識也是神所賜。**啟示的次序**：第 1 步 · 神先交付，人才立志——被擄本身是主的交付（1:2），在但以理立志（1:8）之前。"
add_chapter 01-the-lord-gave.md

add_volume "卷二 · 列國之王與天上的神 (Kings and the God of Heaven) · 2-7章" \
    "忘了的夢、巨像與石頭、金像與火窯、至高者掌權、牆上的字、獅子坑——五個故事（分成六篇研讀），三位王，一位天上的神。**啟示的次序**：第 2 步 · 天上的神賜國、廢國——「他改變時候、日期，廢王，立王」（2:21）；至高者在人的國中掌權，要將國賜與誰就賜與誰（4:17, 25, 32）。"
for f in 02-the-forgotten-dream.md 03-the-image-and-the-stone.md 04-even-if-not.md \
         05-the-most-high-rules.md 06-the-writing-on-the-wall.md 07-the-lions-den.md; do
    add_chapter "$f"
done

add_volume "卷三 · 四獸與人子 (Beasts and the Son of Man) · 8-10章" \
    "四獸從海中上來；亙古常在者坐定；像人子的駕著天雲而來；公綿羊與公山羊。**啟示的次序**：第 3 步 · 列國的權柄是借來的，人子才是承受者——獸得了人心、得了權柄（7:4, 6），其餘的獸權柄又被奪去（7:12）；國賜給人子（7:14）、賜給至高者的聖民（7:18, 22, 27）。"
for f in 08-four-beasts-and-the-son-of-man.md 09-the-kingdom-given-to-the-saints.md \
         10-the-ram-and-the-goat.md; do
    add_chapter "$f"
done

add_volume "卷四 · 禱告與七十個七 (Prayer and the Seventy Sevens) · 11-12章" \
    "從書上得知耶利米的話，便禁食披麻、認罪代求；加百列飛來，說答覆在懇求之初就發出。**啟示的次序**：第 4 步 · 先讀書，後禱告；答覆在懇求之初已發出（9:23）；歷史的時間表交給禱告的人。"
for f in 11-daniels-prayer.md 12-seventy-sevens.md; do
    add_chapter "$f"
done

add_volume "卷五 · 看不見的爭戰與結局 (The Unseen Conflict and the End) · 13-16章" \
    "天上的爭戰、南北二王的歷史、自高的王、復醒與等候。**啟示的次序**：第 5 步 · 結局寫在真確書上，人只要去等候——名錄在冊上的必得拯救（12:1），「你必起來，享受你的福分」（12:13）。"
for f in 13-the-unseen-conflict.md 14-kings-of-the-south-and-north.md \
         15-the-king-who-exalts-himself.md 16-rise-to-your-lot.md; do
    add_chapter "$f"
done

# ============================================================
# 卷末 · 國度直到啟示錄
# ============================================================
add_volume "卷末 · 國度是賜的 (The Kingdom Given)" \
    "從但以理書到啟示錄：那一位「像人子的」，以及賜給聖民的國。"
add_front "$INPUT_DIR/99-to-revelation.md"

# ============================================================
# 附錄 — every chapter's 體例說明 box points the reader at
# 《附錄：引用出處總表》; both appendices must be concatenated or those
# pointers dangle in the printed book (same defect Ruth and Joshua found).
# ============================================================
add_volume "附錄 (Appendices)" \
    "經文與主題索引、引用出處總表——各章「體例說明」所指的卷末附錄。附錄二的跨書經文索引，正是**啟示的次序**在全書的落點清單：它逐一列出行文與注疏引文裏提到的、但以理書以外的經文，以及本書在哪一章接上那條線。"
add_front "$INPUT_DIR/98-appendix-indices.md"
add_front "$INPUT_DIR/99-appendix-references.md"

# 跋 — afterword. Last content file: no trailing \newpage.
echo "  Adding (unnumbered): 999-afterword.md"
tail -n +8 "$INPUT_DIR/999-afterword.md" \
  | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}" ; done=1 } } {print}' >> "$COMBINED_MD"
((chapter_count++))

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters)"
echo ""
echo "🔨 Generating PDF with daniel.latex template..."

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
