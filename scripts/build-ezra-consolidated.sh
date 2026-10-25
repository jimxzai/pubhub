#!/bin/bash

# Ezra PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine/order) + 全書領受總綱 + 四卷 14 章 + 卷末 + 附錄 + 跋
# Uses templates/pdf/ezra.latex (Stone/Amber/Clay theme, matching the Gospel of
# John / Joshua / Isaiah / Job series standard: cover art, frontispiece)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/ezra"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/ezra-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/ezra-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/ezra.latex"

echo "=========================================="
echo "Ezra Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "以斯拉記研讀"
subtitle: "Ezra Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年10月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **主要參考資料整合：**

  • **Matthew Henry** — Commentary on the Whole Bible

  • **Keil & Delitzsch** — Biblical Commentary on the Old Testament

  • **The Pulpit Commentary**

  • **G. Campbell Morgan** — The Analyzed Bible, vol. 1 (1907)，僅用全書概觀

  **歸回、重建聖殿、神施恩的手在先——十章經文，十四篇研讀**

  卷一：激動與歸回 (1-3章) | 卷二：攔阻與完工 (4-7章)
  卷三：神的手與定志的心 (8-11章) | 卷四：污穢與認罪 (12-14章)

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
# preface, orientation chapters and the four volume divider pages consume
# numbers 1-9 and the book's own 第一章 comes out as LaTeX chapter 10 — the
# contents page then reads "10  第一章 · ...", two conflicting numbers on one
# line. Marking these unnumbered lets the 14 study units number 1-20,
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
add_front "$INPUT_DIR/00a-ezra-position.md"
add_front "$INPUT_DIR/00b-hand-spine.md"
add_front "$INPUT_DIR/00c-revelation-order.md"

# Systematic reception — demote headings one level so it reads as one chapter.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
    tail -n +2 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 四卷 · 14 段
# ============================================================
add_volume "卷一 · 激動與歸回 (Stirred Up and Returned) · 1-3章" \
    "神先激動古列的心、再激動百姓的心；名冊一個一個數過；到了耶路撒冷，壇先於殿。**啟示的次序**：第 1 步 · 神先動——神先激動王的心（1:1）、再激動百姓的心（1:5），人才起來；壇在根基之先（3:2-6），先事奉神，才建神的殿。"
for f in 01-cyrus-decree-and-the-vessels.md 02-the-list-of-the-returned.md \
         03-altar-before-foundation.md; do
    add_chapter "$f"
done

add_volume "卷二 · 攔阻與完工 (Opposed and Finished) · 4-7章" \
    "攔阻先以合作的假面、後以公文的控告而來；先知的話使停了的工重新動起來；答案早在王室檔案中；完工與歡喜都是神所賜。**啟示的次序**：第 2 步 · 神的話使停了的工重新動起來——使工程復工的不是人的決心，是先知的話（5:1-2）；完工與歡喜都是神所賜（6:14, 6:22）。"
for f in 04-adversaries-and-the-stopped-work.md \
         05-prophets-and-the-governors-letter.md \
         06-the-scroll-at-ecbatana.md 07-dedication-and-passover.md; do
    add_chapter "$f"
done

add_volume "卷三 · 神的手與定志的心 (The Hand and the Heart) · 8-11章" \
    "沉默約六十年後神再動手；以斯拉定志考究遵行教訓；王的詔書；亞哈瓦河邊的禁食；銀子一件一件稱過。**啟示的次序**：第 3 步 · 神的手在前，人的定志在後——「神的手」六次；以斯拉寧可禁食也不求兵護（8:21-23）。"
for f in 08-ezra-the-scribe.md 09-the-kings-decree-for-ezra.md \
         10-fast-at-the-ahava-canal.md 11-treasure-and-the-road.md; do
    add_chapter "$f"
done

add_volume "卷四 · 污穢與認罪 (Defilement and Confession) · 12-14章" \
    "平安抵達之後，才揭露內部的罪；以斯拉伏在神殿前認罪；然而以色列人還有指望；書以一份罪人的名冊作結。**啟示的次序**：第 4 步 · 平安抵達之後，才揭露內部的罪——認罪先於行動，指望先於改革；書以一份名冊作結，沒有凱旋，開向尼希米、瑪拉基，終必指向另一位。"
for f in 12-ezras-confession.md 13-shecaniah-and-the-covenant.md \
         14-the-register-of-the-guilty.md; do
    add_chapter "$f"
done

# ============================================================
# 卷末 · 未完的歸回
# ============================================================
add_volume "卷末 · 未完的歸回 (The Unfinished Return)" \
    "全書從神激動人心起頭，走過重建與認罪，最終停在一份罪人的名冊——歸回不是句點，也還不是終點。"
add_front "$INPUT_DIR/99-the-unfinished-return.md"

# ============================================================
# 附錄 — every chapter's 體例說明 box points the reader at
# 《附錄：引用出處總表》; both appendices must be concatenated or those
# pointers dangle in the printed book (same defect Ruth and Joshua found).
# ============================================================
add_volume "附錄 (Appendices)" \
    "經文與主題索引、引用出處總表——各章「體例說明」所指的卷末附錄。附錄二的跨書經文索引，正是**啟示的次序**在全書的落點清單：它逐一列出以斯拉記以外的每一處經文，以及本書在哪一章接上那條線。"
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
echo "🔨 Generating PDF with ezra.latex template..."

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
