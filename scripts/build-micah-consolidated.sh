#!/bin/bash

# Micah PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine/order) + 全書領受總綱 + 三卷 9 篇 + 卷末 + 附錄 + 跋
# Uses templates/pdf/micah.latex (derived from revelation.latex: the same full-bleed front/back covers as
# Revelation and the Gospel of John; slate-green/gold theme)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/Micah"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/micah-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/micah-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/micah.latex"

echo "=========================================="
echo "Micah Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "有何神像你"
subtitle: "彌迦書研讀 Micah Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年10月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **主要參考資料整合：**

  • **Matthew Henry** — Commentary on the Whole Bible

  • **John Calvin** — Commentaries on the Twelve Minor Prophets, vol. 3（Jonah, Micah, Nahum；John Owen 英譯，CCEL）

  • **G. Campbell Morgan** — Living Messages of the Books of the Bible（〈The Message of Micah〉）

  • **John MacArthur** — gty.org 講章（各條標明出處；gty.org 沒有彌迦書逐節講道）

  • **早期教父** — 引文取自 NPNF／ANF 公有領域譯本（newadvent.org）

  **三輪「聽」：神親自下來、官長與山、爭辯與等候——七章經文，九篇研讀**

  卷一：聽——神親自下來 (1-2篇) | 卷二：官長與山 (3-6篇) | 卷三：爭辯與等候 (7-9篇)

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
# line. Marking these unnumbered lets the 9 study units number 1-9,
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
add_front "$INPUT_DIR/00a-micah-position.md"
add_front "$INPUT_DIR/00b-hear-spine.md"
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
# 正文 · 三卷 · 9 篇
# ============================================================
add_volume "卷一 · 聽——神親自下來 (He Comes Down) · 1-2篇（彌1-2）" \
    "第一次呼召：「萬民哪，你們都要聽！」神不是差人去，是自己出了居所、降臨步行地的高處；祂先作見證，才宣判。判決之後，馬上是一句「我必要聚集你們」。**啟示的次序**：第 1 步 · 神先下來，先作見證——「主耶和華從他的聖殿要見證你們的不是」（1:2）；「耶和華出了他的居所，降臨步行地的高處」（1:3）。"
for f in 01-the-lord-comes-down.md 02-woe-and-the-gathered-flock.md; do
    add_chapter "$f"
done

add_volume "卷二 · 官長與山 (Leaders and the Mountain) · 3-6篇（彌3-5）" \
    "第二次呼召：「雅各的首領，以色列家的官長啊，你們要聽！」首領、祭司、先知三職一同受審；錫安被耕種像一塊田，緊接著殿的山堅立超乎諸山；審判者的臉被杖擊，君王卻從最小的伯利恆出來。**啟示的次序**：第 2 步 · 審判從領袖與神的家起（3:11-12）；第 3 步 · 判決與應許並排，中間沒有過渡（3:12→4:1）；第 4 步 · 君王從最小的地方來（5:2）。"
for f in 03-heads-of-jacob.md 04-mountain-of-the-lord.md \
         05-travail-threshing-and-the-struck-judge.md 06-bethlehem-ephrathah.md; do
    add_chapter "$f"
done

add_volume "卷三 · 爭辯與等候 (The Case and the Waiting) · 7-9篇（彌6-7）" \
    "第三次呼召：「以色列人哪，當聽耶和華的話！」神先說「我向你做了甚麼」，才說「祂向你所要的是甚麼」；先知在沒有義人的世上說「至於我，我要仰望耶和華」；全書最後一個問句不是審判，是「有何神像你？」（7:18），而全書最後一節回到對列祖的誓言（7:20）。**啟示的次序**：第 5 步 · 先陳恩典、後提要求（6:3-8）；控告的神成為辯護的神（6:2→7:9）；「我的神必應允我」（7:7）。"
for f in 07-the-lord-has-a-case.md 08-i-will-wait-for-the-god-of-my-salvation.md 09-who-is-a-god-like-you.md; do
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
echo "🔨 Generating PDF with micah.latex template..."

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
