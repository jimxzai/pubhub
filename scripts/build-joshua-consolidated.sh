#!/bin/bash

# Joshua PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine) + 全書領受總綱 + 五卷 20 章 + 卷末 + 跋
# Uses templates/pdf/joshua.latex (Jordan/Conquest/Rest theme, matching the
# Gospel of John / Acts of the Apostles / Isaiah / Job series standard: cover
# art, frontispiece)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/joshua"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/joshua-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/joshua-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/joshua.latex"

echo "=========================================="
echo "🌊 Joshua Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "約書亞記研讀"
subtitle: "Joshua Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年9月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **主要參考資料整合：**

  • **老弟兄查經法** — 提問式、全經連線、活在今天

  • **John Calvin** — Commentary on the Book of Joshua (1564)

  • **Matthew Henry** — Commentary on the Whole Bible, Joshua

  • **F.B. Meyer** — Joshua and the Land of Promise (1893)

  • **C.H. Spurgeon** — Metropolitan Tabernacle Pulpit Sermons

  **過約旦河、爭戰得地、均分為業——一句都沒有落空的信實見證**

  卷一：預備與信心，跨越約旦河 (1-5章) | 卷二：中央突破，耶利哥與艾城 (6-8章)
  卷三：南征北討，全地底定 (9-12章) | 卷四：地業均分，家家有份 (13-21章) | 卷五：立約立志，至死不渝 (22-24章)

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
# numbers 1-9 and the book's own 第一章 comes out as LaTeX chapter 10 — the
# contents page then reads "10  第一章 · ...", two conflicting numbers on one
# line. Marking these unnumbered lets the 20 study units number 1-20,
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
# 卷首 · 定位 — orientation: overview, position, spine
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這幾章：總覽、位置、骨幹、啟示的次序。"

add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-joshua-position.md"
add_front "$INPUT_DIR/00b-conquest-spine.md"
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
# 正文 · 五卷 · 20 段
# ============================================================
add_volume "卷一 · 預備與信心：跨越約旦河 (Preparation) · 1-5章" \
    "摩西已死，約書亞受命；探子窺探，喇合搭救；全會眾在約旦河乾地上過河，於吉甲立石為記。"
for f in 01-commission-and-courage.md 02-rahab-and-the-scarlet-cord.md \
         03-crossing-the-jordan.md 04-gilgal-and-commander-of-the-lords-army.md; do
    add_chapter "$f"
done

add_volume "卷二 · 中央突破：耶利哥與艾城 (Central Campaign) · 6-8章" \
    "耶利哥的城牆因信心與順服傾倒；亞干的貪心使艾城初戰慘敗；除罪之後，艾城攻克，以巴路山築壇立約。"
for f in 05-fall-of-jericho.md 06-achans-sin.md 07-ai-conquered.md; do
    add_chapter "$f"
done

add_volume "卷三 · 南征北討，全地底定 (Southern and Northern Campaigns) · 9-12章" \
    "基遍人用詭計求和；南方五王聯軍潰敗、日頭停住；北方諸王聯軍瓦解；三十一個被擊敗的王一一列冊。"
for f in 08-gibeonite-deception.md 09-southern-campaign-sun-stands-still.md \
         10-northern-campaign-and-kings-list.md; do
    add_chapter "$f"
done

add_volume "卷四 · 地業均分，家家有份 (Division of the Inheritance) · 13-21章" \
    "河東二支派半先得地業；迦勒憑信心求取希伯崙；猶大、以法蓮、瑪拿西、餘下七支派逐一抽籤分地；又設逃城，立利未人的城邑。"
for f in 11-inheritance-east-of-jordan.md 12-caleb-claims-hebron.md \
         13-judahs-inheritance.md 14-ephraim-and-manasseh.md \
         15-seven-tribes-and-joshuas-portion.md 16-cities-of-refuge.md \
         17-levitical-cities.md; do
    add_chapter "$f"
done

add_volume "卷五 · 立約立志，至死不渝 (Covenant and Legacy) · 22-24章" \
    "河東支派築壇為證，幾乎引發內戰卻及時化解；約書亞臨別勸勉全會眾；示劍立約，「至於我和我家，我們必定事奉耶和華」。"
for f in 18-altar-of-witness.md 19-joshuas-farewell-address.md \
         20-covenant-renewal-and-joshuas-death.md; do
    add_chapter "$f"
done

# ============================================================
# 卷末 · 至於我和我家
# ============================================================
add_volume "卷末 · 至於我和我家 (As for Me and My House)" \
    "全書從約旦河的乾地起頭，走過爭戰的煙塵，最終停在示劍的立約——神的信實一句都沒有落空，剩下的是人當如何回應。"
add_front "$INPUT_DIR/99-covenant-and-legacy.md"

# 跋 — afterword. Last content file: no trailing \newpage.
echo "  Adding (unnumbered): 999-afterword.md"
tail -n +8 "$INPUT_DIR/999-afterword.md" \
  | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}" ; done=1 } } {print}' >> "$COMBINED_MD"
((chapter_count++))

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters)"
echo ""
echo "🔨 Generating PDF with joshua.latex template..."

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
