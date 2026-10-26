#!/bin/bash

# Song of Songs PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine/order) + 全書領受總綱 + 四卷 15 章 + 卷末 + 附錄 + 跋
# Uses templates/pdf/songofsolomen.latex (Rose/Vine/Wine theme, matching the Gospel
# of John / Joshua / Isaiah / Job series standard: cover art, frontispiece)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/songofsolomen"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/songofsolomen-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/songofsolomen-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/songofsolomen.latex"

echo "=========================================="
echo "Song of Songs Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "雅歌研讀"
subtitle: "Song of Songs Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年10月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **主要參考資料整合：**

  • **John Gill** — Exposition of the Entire Bible

  • **Keil & Delitzsch** — Biblical Commentary on the Old Testament（雅歌卷）

  • **The Pulpit Commentary**

  • **Matthew Henry** — Commentary on the Whole Bible

  • **Bernard of Clairvaux** — Sermons on the Canticle of Canticles（歌 1:1–3:1）

  • **J. Hudson Taylor** — Union and Communion (1894)

  • **C. H. Spurgeon** — Metropolitan Tabernacle Pulpit（雅歌講章）

  **愛有它的次序——先被呼喚，再被尋見；園子從裏面打開；失落之後歸屬更深；最後蓋上印記，仍然盼望**

  卷一：渴慕與尋見 (1-6章) | 卷二：園子的敞開 (7-8章)
  卷三：失落與重尋 (9-11章) | 卷四：渴想的反轉與印記 (12-15章)

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
add_front "$INPUT_DIR/00a-song-position.md"
add_front "$INPUT_DIR/00b-love-spine.md"
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
# 正文 · 四卷 · 15 段
# ============================================================
add_volume "卷一 · 渴慕與尋見 (Longing and Finding) · 歌 1:1-3:11" \
    "她先說出一個「願」字；他來了；夜間尋見；婚禮的行列。**啟示的次序（愛的次序）**：第 1 步 · 愛先被呼喚，也要等候——「吸引我，我們就快跑」（1:4），三處「不要叫醒」之前的兩次（2:7；3:5）。"
for f in 01-let-him-kiss-me.md 02-black-but-lovely.md 03-rose-of-sharon.md \
         04-the-voice-of-my-beloved.md 05-by-night-on-my-bed.md \
         06-solomons-litter.md; do
    add_chapter "$f"
done

add_volume "卷二 · 園子的敞開 (The Garden Opened) · 歌 4:1-5:1" \
    "關鎖的園，封閉的泉源；她說「願我的良人進入自己園裏」，他說「我進了我的園」。**啟示的次序（愛的次序）**：第 2 步 · 園子由她開口邀請，他才進去——先是關鎖的園（4:12），然後是她的邀請（4:16），然後是他的回答（5:1）。"
for f in 07-you-are-altogether-beautiful.md 08-the-garden-opened.md; do
    add_chapter "$f"
done

add_volume "卷三 · 失落與重尋 (Lost and Sought) · 歌 5:2-6:13" \
    "他敲門，她遲疑，他轉身走了；她尋找，不遇；眾女子問「你的良人比別人的良人有何強處」；她說出他是誰。**啟示的次序（愛的次序）**：第 3 步 · 遲疑付上代價，歸屬卻更深——「我屬我的良人，我的良人也屬我」（6:3），他仍稱她「獨一的」（6:9）。"
for f in 09-i-opened-but-he-was-gone.md 10-white-and-ruddy.md 11-fair-as-tirzah.md; do
    add_chapter "$f"
done

add_volume "卷四 · 渴想的反轉與印記 (Desire Reversed and the Seal) · 歌 7:1-8:14" \
    "王的心被髮綹繫住；「他也戀慕我」；愛如死之堅強；全書停在「求你快來」。**啟示的次序（愛的次序）**：第 4 步 · 印記與盼望——「我屬我的良人，他也戀慕我」（7:10）；「求你將我放在心上如印記」（8:6）；「我的良人哪，求你快來」（8:14）。"
for f in 12-how-beautiful-and-pleasant.md 13-his-desire-is-for-me.md \
         14-set-me-as-a-seal.md 15-make-haste-my-beloved.md; do
    add_chapter "$f"
done

# ============================================================
# 卷末 · 未完的呼喚
# ============================================================
add_volume "卷末 · 未完的呼喚 (The Open Ending)" \
    "全書從一個「願」字起頭，停在一個「快來」的呼喚——愛的次序還沒有走完；新約最後一頁也以「來」收尾，本書並讀，不當作對 8:14 的解答。"
add_front "$INPUT_DIR/99-the-open-ending.md"

# ============================================================
# 附錄 — every chapter's 體例說明 box points the reader at
# 《附錄：引用出處總表》; both appendices must be concatenated or those
# pointers dangle in the printed book (same defect Ruth and Joshua found).
# ============================================================
add_volume "附錄 (Appendices)" \
    "經文與主題索引、引用出處總表——各章「體例說明」所指的卷末附錄。附錄二的跨書經文索引，正是**啟示的次序**在全書的落點清單：它逐一列出雅歌以外的每一處經文，以及本書在哪一章接上那條線。"
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
echo "🔨 Generating PDF with songofsolomen.latex template..."

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
