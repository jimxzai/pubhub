#!/bin/bash

# Isaiah PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine) + 全書領受總綱 + 六卷 26 章 + 卷末 + 跋
# Uses templates/pdf/isaiah.latex (Throne/Coal theme, matching the Gospel of John /
# Acts of the Apostles series standard: cover art, frontispiece, appendices)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/isaiah"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/isaiah-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/isaiah-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/isaiah.latex"

echo "=========================================="
echo "🔥 Isaiah Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "以賽亞書研讀"
subtitle: "Isaiah Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年8月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **週四查經班** — 第一手屬靈教導

  • **John MacArthur** — 逐節解經 (gty.org)

  • **G. Campbell Morgan** — 《The Analyzed Bible: Isaiah》

  **以色列的聖者 = 審判的聖潔 + 拯救的聖潔**

  猶大的控告與呼召 (1-6章) | 以馬內利與亞述的陰影 (7-12章) | 對列國的審判與啟示錄 (13-27章)
  禍哉與拯救·通往希西家 (28-39章) | 安慰與僕人之歌 (40-55章) | 公義的呼召與新天新地 (56-66章)

  **經文版權聲明 (Scripture Copyright Notices)**

  本版為教會內部贈閱版（非賣品）；公開發行時另行申請 ISBN。

  中文經文引自《聖經》和合本（1919），屬公有領域。

  Scripture quotations marked (ESV) are from the ESV® Bible
  (The Holy Bible, English Standard Version®), © 2001 by Crossway,
  a publishing ministry of Good News Publishers. Used by permission.
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
# preface, orientation chapters and the six volume divider pages consume
# numbers 1-7 and the book's own 第一章 comes out as LaTeX chapter 8 — the
# contents page then reads "8  第一章 · 悖逆的兒女", two conflicting numbers on
# one line. Marking these unnumbered lets the 26 study units number 1-26,
# matching 第一章-第二十六章. Same approach as build-gospel-of-luke-consolidated.sh.
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
    "讀正文之前先讀這幾章：總覽、位置、骨幹——聖哉的異象如何焊住全書。"

add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-isaiah-position.md"
add_front "$INPUT_DIR/00b-holy-one-spine.md"

# Systematic reception — demote headings one level so it reads as one chapter.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
    tail -n +2 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 六卷 · 26 段
# ============================================================
add_volume "卷一 · 猶大的控告與呼召 (Indictment and Calling) · 1-6章" \
    "審判的起點不是冷酷的審判台，是被辜負的愛——先看見聖潔，才看見自己的污穢。"
for f in 01-rebellious-children.md 02-day-of-the-lord.md 03-song-of-the-vineyard.md \
         04-isaiahs-call.md; do
    add_chapter "$f"
done

add_volume "卷二 · 以馬內利與亞述的陰影 (Immanuel and the Shadow of Assyria) · 7-12章" \
    "人的不信，攔不住神信實的應許——危機裏，神親自賜下以馬內利的記號。"
for f in 05-sign-of-immanuel.md 06-child-and-the-rod.md 07-root-of-jesse.md; do
    add_chapter "$f"
done

add_volume "卷三 · 對列國的審判與啟示錄 (Judgment on the Nations and the Apocalypse) · 13-27章" \
    "以色列的聖者不是一位地方神——祂的公義審判及於萬邦，祂的拯救也向萬邦敞開。"
for f in 08-fall-of-babylon.md 09-oracles-against-nations.md 10-watchman-and-tyre.md \
         11-isaiahs-apocalypse.md; do
    add_chapter "$f"
done

add_volume "卷四 · 禍哉與拯救·通往希西家 (Woes and Deliverance — Toward Hezekiah) · 28-39章" \
    "唯獨『平靜安穩』才是得救的力量——希西家的故事，是這句話從理論變成歷史現實的示範。"
for f in 12-ephraim-and-ariel.md 13-woe-to-egypt.md 14-righteous-king-refuge.md \
         15-day-of-vengeance-ransomed-return.md 16-siege-of-assyria.md \
         17-hezekiahs-illness.md; do
    add_chapter "$f"
done

add_volume "卷五 · 安慰與僕人之歌 (Comfort and the Servant Songs) · 40-55章" \
    "『你們要安慰、安慰我的百姓』——全書在這裏轉了調，藉著僕人的受苦，藉著白白賜下的恩典，神親自成就拯救。"
for f in 18-comfort-my-people.md 19-besides-me-no-god.md 20-cyrus-leave-babylon.md \
         21-zion-tongue-of-learned.md 22-suffering-servant.md 23-waters-without-price.md; do
    add_chapter "$f"
done

add_volume "卷六 · 公義的呼召與新天新地 (The Call to Righteousness and the New Heavens and New Earth) · 56-66章" \
    "拯救的高峰過去，先知回到公義的呼召；全書的終局，是神親自造新天新地，眼淚全被擦去。"
for f in 24-arm-of-the-lord-shortened.md 25-arise-shine.md 26-from-edom.md; do
    add_chapter "$f"
done

# ============================================================
# 卷末 · 沒有寫完的榮耀
# ============================================================
add_volume "卷末 · 沒有寫完的榮耀 (The Unfinished Glory)" \
    "以賽亞書自己不肯用一個乾淨的句號收尾——先知從『我滅亡了』（6:5）寫到『我造新天新地』（65:17），這條路今天還沒有走完，因為新天新地還沒有臨到，我們仍活在應許與成就之間。
>
> 耶和華說：我所要造的新天新地，怎樣在我面前長存；你們的後裔和你們的名字也必照樣長存。（賽 66:22）"
add_front "$INPUT_DIR/99-new-heavens-new-earth.md"

# 跋 — afterword. Last content file: no trailing \newpage.
echo "  Adding (unnumbered): 999-afterword.md"
tail -n +8 "$INPUT_DIR/999-afterword.md" \
  | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}" ; done=1 } } {print}' >> "$COMBINED_MD"
((chapter_count++))

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters)"
echo ""
echo "🔨 Generating PDF with isaiah.latex template..."

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
