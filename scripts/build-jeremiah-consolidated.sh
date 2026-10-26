#!/bin/bash

# Jeremiah PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine/order) + 全書領受總綱 + 六卷 27 章 + 卷末 + 附錄 + 跋
# Uses templates/pdf/jeremiah.latex (Plum/Almond/Ash theme, companion to nehemiah.latex)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/jeremeiah"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/jeremiah-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/jeremiah-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/jeremiah.latex"

echo "=========================================="
echo "Jeremiah Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "耶利米書研讀"
subtitle: "Jeremiah Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年10月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **主要參考資料整合：**

  • **Matthew Henry** — Commentary on the Whole Bible

  • **John Calvin** — Commentaries on the Book of the Prophet Jeremiah and the Lamentations（John Owen 英譯，CCEL）

  • **G. Campbell Morgan** — Living Messages of the Books of the Bible

  • **John MacArthur** — gty.org 講章（各條標明出處）

  • **早期教父** — 引文取自 NPNF／ANF 公有領域譯本（newadvent.org）

  **呼召與控訴、殿與不聽、君王與假先知、安慰之書、話語與焚燒、列國與終局——五十二章經文，二十七篇研讀**

  卷一：呼召與控訴 (1-4篇) | 卷二：殿與不聽 (5-11篇) | 卷三：君王與假先知 (12-16篇)

  卷四：安慰之書 (17-19篇) | 卷五：話語與焚燒 (20-24篇) | 卷六：列國與終局 (25-27篇)

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
add_front "$INPUT_DIR/00a-jeremiah-position.md"
add_front "$INPUT_DIR/00b-watching-spine.md"
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
# 正文 · 六卷 · 27 章
# ============================================================
add_volume "卷一 · 呼召與控訴 (Call and Indictment) · 1-4篇（耶1-6）" \
    "話先到，人後到：先知未出母胎已被曉得、被分別；神先控訴、先呼喚，才宣告審判。**啟示的次序**：第 1 步 · 話先於人——「我留意保守我的話，使得成就」（1:12）；第 2 步 · 先呼喚、後審判——「背道的以色列啊，回來吧」（3:12）；「你們這背道的兒女啊，回來吧」（3:22）。"
for f in 01-before-i-formed-you.md 02-broken-cisterns.md \
         03-return-faithless-israel.md 04-peace-peace.md; do
    add_chapter "$f"
done

add_volume "卷二 · 殿與不聽 (The Temple and the Unheeding Ear) · 5-11篇（耶7-20）" \
    "殿門口的講道、哀哭的先知、麻褲帶與酒罈、乾旱與被關上的代求、詭詐的心、窯匠與瓦瓶，直到「火在我骨中」。**啟示的次序**：第 3 步 · 代求被關上，眼淚沒有關——神說「你不要為這百姓祈禱」（7:16），自己卻先哀哭（9:1；8:21）。"
for f in 05-den-of-robbers.md 06-weeping-prophet-living-god.md \
         07-covenant-belt-jar.md 08-drought-and-closed-intercession.md \
         09-deceitful-heart.md 10-potter-and-flask.md 11-fire-in-my-bones.md; do
    add_chapter "$f"
done

add_volume "卷三 · 君王與假先知 (Kings and False Prophets) · 12-16篇（耶21-29）" \
    "君王一個一個倒下；假先知喊「平安」；兩筐無花果與七十年；哈拿尼雅折斷木軛，耶利米寫信給被擄的人。**啟示的次序**：第 4 步 · 審判藉巴比倫，盼望種在審判裏——「我僕人巴比倫王尼布甲尼撒」（25:9）；「我向你們所懷的意念是賜平安的意念」（29:11）。"
for f in 12-kings-before-the-fall.md 13-righteous-branch.md \
         14-two-baskets-seventy-years.md 15-trial-and-yoke.md \
         16-hananiah-and-the-letter.md; do
    add_chapter "$f"
done

add_volume "卷四 · 安慰之書 (The Book of Consolation) · 17-19篇（耶30-33）" \
    "傳統稱為「安慰之書」的四章：拉結不肯受安慰，以法蓮悔改，新約寫在心上，耶利米在圍城中買了一塊田。**啟示的次序**：第 4 步（續）· 盼望種在審判裏——新約（31:31-34）在書中排在城破（39 章）之前；亞拿突的田（32:6-15）是在圍城中買的（32:2）。"
for f in 17-book-of-consolation.md 18-new-covenant.md 19-field-at-anathoth.md; do
    add_chapter "$f"
done

add_volume "卷五 · 話語與焚燒 (The Word and the Fire) · 20-24篇（耶34-45）" \
    "背約釋奴的人、不肯喝酒的利甲族、被小刀割破又被火燒掉的書卷、淤泥坑與牢院、城破、基大利，以及被帶往埃及的先知。**啟示的次序**：第 5 步 · 話語勝過刀與火——書卷被燒，神使它再寫，「另外又添了許多相彷的話」（36:32）。"
for f in 20-broken-covenant-rechabites.md 21-scroll-and-penknife.md \
         22-cistern-and-courtyard.md 23-fall-of-the-city.md \
         24-egypt-and-baruch.md; do
    add_chapter "$f"
done

add_volume "卷六 · 列國與終局 (The Nations and the End) · 25-27篇（耶46-52）" \
    "向列國的宣告、巴比倫的傾覆、一卷石頭拴著沉進幼發拉底河的書，以及全書最後一幕：約雅斤脫去囚服，終身在王面前吃飯。**啟示的次序**：第 5 步（續）· 審判者亦受審——審判先臨到神的百姓，也臨到執行審判的巴比倫（51:63-64）；燈沒有熄滅（52:31-34）。"
for f in 25-oracles-against-nations.md 26-fall-of-babylon.md 27-jehoiachins-table.md; do
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
echo "🔨 Generating PDF with jeremiah.latex template..."

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
