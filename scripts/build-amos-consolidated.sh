#!/bin/bash

# Amos PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine/order) + 全書領受總綱 + 五卷 12 章 + 卷末 + 附錄 + 跋
# Uses templates/pdf/amos.latex (Slate/Summer-fruit/Sycamore theme, derived from amos.latex)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/Amos"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/amos-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/amos-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/amos.latex"

echo "=========================================="
echo "Amos Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "阿摩司書研讀"
subtitle: "Amos Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年10月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **主要參考資料整合：**

  • **Matthew Henry** — Commentary on the Whole Bible

  • **John Calvin** — Commentaries on the Twelve Minor Prophets, vol. 2（Joel, Amos, Obadiah；John Owen 英譯，CCEL）

  • **G. Campbell Morgan** — Living Messages of the Books of the Bible

  • **John MacArthur** — gty.org 講章（各條標明出處）

  • **早期教父** — 引文取自 NPNF／ANF 公有領域譯本（newadvent.org）

  **吼聲與列國、揀選與管教、尋求與安逸、準繩與籃子、篩子與帳幕——九章經文，十二篇研讀**

  卷一：吼聲與列國 (1-2篇) | 卷二：揀選與管教 (3-4篇) | 卷三：尋求與安逸 (5-7篇)

  卷四：準繩與籃子 (8-10篇) | 卷五：篩子與帳幕 (11-12篇)

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
# line. Marking these unnumbered lets the 27 study units number 1-27,
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
add_front "$INPUT_DIR/00a-amos-position.md"
add_front "$INPUT_DIR/00b-hearing-spine.md"
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
# 正文 · 五卷 · 12 章
# ============================================================
add_volume "卷一 · 吼聲與列國 (The Roar and the Nations) · 1-2篇（摩1-2）" \
    "聲音先到，人後到：提哥亞的牧人只是聽見的人；審判從最遠的鄰國講起，一圈一圈收窄，最後落在聽的人自己身上。**啟示的次序**：第 1 步 · 吼聲先於先知——「耶和華必從錫安吼叫」（1:2）；第 2 步 · 審判由外而內，最後落在聽的人身上——八個「三番四次」，末一個是以色列（2:6）。"
for f in 01-the-lord-roars.md 02-three-and-four.md; do
    add_chapter "$f"
done

add_volume "卷二 · 揀選與管教 (Election and Discipline) · 3-4篇（摩3-4）" \
    "「在地上萬族中，我只認識你們；因此，我必追討你們的一切罪孽」（3:2）；神用饑荒、乾旱、霉爛、蝗蟲、瘟疫、傾覆五次管教，五次都是「你們仍不歸向我」。**啟示的次序**：第 3 步 · 認識即責任；管教五次，仍不歸向——「你當預備迎見你的神」（4:12）。"
for f in 03-you-only-have-i-known.md 04-prepare-to-meet-your-god.md; do
    add_chapter "$f"
done

add_volume "卷三 · 尋求與安逸 (Seeking and Ease) · 5-7篇（摩5-6）" \
    "哀歌、「求我就存活」、神厭惡的節期、公平如大水滾滾，以及躺在象牙牀上的人。**啟示的次序**：第 4 步 · 尋求我，就存活——門在哀歌與禍哉中仍開著：「你們要尋求我，就必存活」（5:4；亦見 5:6, 14）。"
for f in 05-seek-me-and-live.md 06-justice-like-waters.md 07-at-ease-in-zion.md; do
    add_chapter "$f"
done

add_volume "卷四 · 準繩與籃子 (The Plumb Line and the Basket) · 8-10篇（摩7-8）" \
    "蝗蟲、火、準繩；亞瑪謝與牧人；一筐夏天的果子與聽耶和華話的饑荒。**啟示的次序**：第 5 步 · 代求兩次蒙允，準繩垂下；話語的饑荒——阿摩司兩次代求，耶和華兩次「後悔」（7:3, 6）；第三、四個異象起，「我必不再寬恕他們」（7:8；8:2）；最後是「聽耶和華話的飢荒」（8:11）。"
for f in 08-locusts-fire-plumb-line.md 09-amos-and-amaziah.md 10-summer-fruit-famine-of-the-word.md; do
    add_chapter "$f"
done

add_volume "卷五 · 篩子與帳幕 (The Sieve and the Booth) · 11-12篇（摩9）" \
    "主站在祭壇旁，無處可逃；篩穀，連一粒也不落在地上；到那日，倒塌的帳幕要重新建立。**啟示的次序**：第 6 步 · 篩子裏不掉一粒；倒塌的帳幕要重建——「連一粒也不落在地上」（9:9）；「我要將他們栽於本地，他們不再……拔出來」（9:15）。"
for f in 11-the-lord-by-the-altar.md 12-davids-fallen-booth.md; do
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
echo "🔨 Generating PDF with amos.latex template..."

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
