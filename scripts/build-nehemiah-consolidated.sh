#!/bin/bash

# Nehemiah PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine/order) + 全書領受總綱 + 四卷 13 章 + 卷末 + 附錄 + 跋
# Uses templates/pdf/nehemiah.latex (Slate/Amber/Clay theme, companion to ezra.latex)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/nehemiah"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/nehemiah-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/nehemiah-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/nehemiah.latex"

echo "=========================================="
echo "Nehemiah Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "尼希米記研讀"
subtitle: "Nehemiah Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年10月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **主要參考資料整合：**

  • **Matthew Henry** — Commentary on the Whole Bible

  • **Walter F. Adeney** — Ezra, Nehemiah, and Esther (The Expositor's Bible, 1893)

  • **Keil & Delitzsch** — Biblical Commentary on the Old Testament

  • **G. Campbell Morgan** — Living Messages of the Books of the Bible

  • **John MacArthur** — gty.org 講章與部落格各一（零星引用，非逐節講道；各條標明出處）

  • **耶柔米、蘇比丟·西弗勒、耶路撒冷的區利羅** — 早期教父，引文取自 NPNF 公有領域譯本

  **憂與禱、牆與敵、書與樂、城與誓——十三章經文，十三篇研讀**

  卷一：憂與禱 (1-2章) | 卷二：牆與敵 (3-6章)

  卷三：書與樂 (7-10章) | 卷四：城與誓 (11-13章)

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
    "讀正文之前先讀這幾章：總覽、位置、骨幹、啟示的次序，以及全書領受總綱。"

add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-nehemiah-position.md"
add_front "$INPUT_DIR/00b-remember-spine.md"
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
# 正文 · 四卷 · 13 章
# ============================================================
add_volume "卷一 · 憂與禱 (Grief and Prayer) · 1-2章" \
    "城牆還沒有動一塊石頭，先有一個人坐下來哭；他的禱告是一篇用聖經拼成的禱告；神的回應不是神蹟，是一隻施恩的手。**啟示的次序**：第 1 步 · 神先使人憂傷（1:4）；第 2 步 · 神施恩的手，不用神蹟（2:8, 2:18）。"
for f in 01-a-burden-and-a-prayer.md 02-the-good-hand-of-my-god.md; do
    add_chapter "$f"
done

add_volume "卷二 · 牆與敵 (The Wall and the Enemy) · 3-6章" \
    "各人修各人的一段，從羊門到羊門；嘲笑、威脅、內部的剝削、四次邀請與一封公開信，都擋不住；五十二天，連仇敵也承認這工作出乎神。**啟示的次序**：第 3 步 · 神使眾人同工、為我們爭戰——牆是為話語而造的（6:15-16）。"
for f in 03-every-man-before-his-own-house.md 04-sword-and-trowel.md \
         05-the-cry-of-the-poor.md 06-i-am-doing-a-great-work.md; do
    add_chapter "$f"
done

add_volume "卷三 · 書與樂 (The Book and the Joy) · 7-10章" \
    "牆成了，百姓卻少；名冊先於讀經；水門前一本書被讀、被解明，百姓先哭後樂，繼而認罪、立約。**啟示的次序**：第 4 步 · 神的書在水門前被讀——牆為書而造，書使人哭、使人樂、使人認罪（8:1-9:3）。"
for f in 07-who-came-up-first.md 08-the-book-at-the-water-gate.md \
         09-the-long-confession.md 10-the-sealed-covenant.md; do
    add_chapter "$f"
done

add_volume "卷四 · 城與誓 (The City and the Oath) · 11-13章" \
    "十人取一住進城；兩班稱謝的人在城上遊行；然後尼希米回來，發現誓約一條一條被打破。**啟示的次序**：第 5 步 · 牆圍住了城，圍不住心——書以「我的神啊，求你記念我」作結，指向一個寫在心裏的新約（耶 31:31-34；來 8:13）。"
for f in 11-one-in-ten.md 12-two-choirs-on-the-wall.md 13-remember-me.md; do
    add_chapter "$f"
done

# ============================================================
# 卷末 · 還沒寫完的約
# ============================================================
add_front "$INPUT_DIR/99-remember-me.md"

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
echo "🔨 Generating PDF with nehemiah.latex template..."

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
