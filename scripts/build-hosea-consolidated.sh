#!/bin/bash

# Hosea PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine/order) + 全書領受總綱 + 四卷 15 章 + 卷末 + 附錄 + 跋
# Uses templates/pdf/hosea.latex (Wine/Dew/Olive theme, derived from hosea.latex)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/hosea"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/hosea-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/hosea-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/hosea.latex"

echo "=========================================="
echo "Hosea Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "何西阿書研讀"
subtitle: "Hosea Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年10月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **主要參考資料整合：**

  • **Matthew Henry** — Commentary on the Whole Bible

  • **John Calvin** — Commentaries on the Twelve Minor Prophets（Hosea；John Owen 英譯，CCEL）

  • **G. Campbell Morgan** — Living Messages of the Books of the Bible

  • **John MacArthur** — gty.org 講章（各條標明出處）

  • **早期教父** — 引文取自 NPNF／ANF 公有領域譯本（newadvent.org）

  **婚姻即信息、訴訟與退隱、醫治與顯露、心腸翻轉與白白的愛——十四章經文，十五篇研讀**

  卷一：婚姻即信息 (1-4篇) | 卷二：訴訟與退隱 (5-7篇) | 卷三：醫治與顯露 (8-11篇) | 卷四：心腸翻轉與白白的愛 (12-15篇)

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

# Volume divider: a part-title page carrying the volume's theme.
# Front/back matter and volume dividers: same as add_file but marks the H1
# {.unnumbered}. Without this LaTeX numbers EVERY chapter sequentially, so the
# preface, orientation chapters and the four volume divider pages consume
# numbers 1-9 and the book's own 第一章 comes out as LaTeX chapter 10 — the
# contents page then reads "10  第一章 · ...", two conflicting numbers on one
# line. Marking these unnumbered lets the 15 study units number 1-15,
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
    "讀正文之前先讀這幾章：總覽、位置、骨幹、啟示的次序，以及全書領受總綱。"

add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-hosea-position.md"
add_front "$INPUT_DIR/00b-who-turns-first.md"
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
# 正文 · 四卷 · 15 章
# ============================================================
add_volume "卷一 · 婚姻即信息 (The Marriage Is the Message) · 1-4篇（何1-3）" \
    "先知的家成為信息：神先命令、先起名、先付買價。**啟示的次序**：第 1 步 · 神先動手，贖價先付——「你去娶淫婦為妻」（1:2）；「我便用銀子十五舍客勒，大麥一賀梅珥半，買她歸我」（3:2）；買回在前，「後來以色列人必歸回」（3:5）在後。"
for f in 01-gomer-and-three-names.md 02-lawsuit-against-mother.md \
         03-allure-and-betroth.md 04-buy-her-back.md; do
    add_chapter "$f"
done

add_volume "卷二 · 訴訟與退隱 (The Lawsuit and the Withdrawal) · 5-7篇（何4-6）" \
    "神與這地的居民爭辯；神退回原處，等人來尋；人說「來吧，我們歸向耶和華」，神說那良善如早晨的雲霧。**啟示的次序**：第 2 步 · 先爭辯、後審判；先退隱、等人來尋——「耶和華與這地的居民爭辯」（4:1）；「我要回到原處，等他們自覺有罪，尋求我面」（5:15）。"
for f in 05-no-knowledge-of-god.md 06-return-to-my-place.md 07-come-let-us-return.md; do
    add_chapter "$f"
done

add_volume "卷三 · 醫治與顯露 (Healing and Exposure) · 8-11篇（何7-10）" \
    "沒有翻過的餅、愚蠢的鴿子、種風收暴風、不再歡喜的日子，直到「現今正是尋求耶和華的時候」。**啟示的次序**：第 3 步 · 神一伸手要醫，病就顯露——「我想醫治以色列的時候，以法蓮的罪孽和撒馬利亞的罪惡就顯露出來」（7:1）。"
for f in 08-cake-not-turned.md 09-sow-the-wind.md \
         10-days-of-recompense.md 11-break-up-fallow-ground.md; do
    add_chapter "$f"
done

add_volume "卷四 · 心腸翻轉與白白的愛 (The Heart Turns Over, and Love Freely Given) · 12-15篇（何11-14）" \
    "「我怎能捨棄你」；雅各的得勝是哭泣；贖脫陰間的話與撒馬利亞的結局並排；最後是「我必醫治他們背道的病，甘心愛他們」，以及一句留給讀者的話。**啟示的次序**：第 4 步 · 神的心腸先翻轉——「我回心轉意，我的憐愛大大發動」（11:8）；第 5 步 · 神自己醫治、白白愛——「因為我的怒氣向他們轉消」（14:4）；「誰是智慧人？可以明白這些事」（14:9）。"
for f in 12-how-can-i-give-you-up.md 13-jacob-and-the-prophet.md \
         14-ransom-from-sheol.md 15-return-o-israel.md; do
    add_chapter "$f"
done

# ============================================================
# 卷末 · 通往啟示錄
# ============================================================
add_front "$INPUT_DIR/99-to-revelation.md"

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
echo "  Adding (unnumbered): 999-afterword.md"
tail -n +8 "$INPUT_DIR/999-afterword.md" \
  | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}" ; done=1 } } {print}' >> "$COMBINED_MD"
((chapter_count++))

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters)"
echo ""
echo "🔨 Generating PDF with hosea.latex template..."

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
