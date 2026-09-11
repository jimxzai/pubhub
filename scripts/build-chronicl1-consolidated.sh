#!/bin/bash

# 1 Chronicles PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine/revelation-order) + 七部分 29 章 + 跋 + 附錄
# Uses templates/pdf/chronicl1.latex (Name/Ark/Temple theme, matching the
# Job / Gospel of John / Acts of the Apostles series standard: cover art,
# frontispiece)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/chronicl1"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/chronicl1-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/chronicl1-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/chronicl1.latex"

echo "=========================================="
echo "🏛️  1 Chronicles Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "歷代志上研讀"
subtitle: "1 Chronicles Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年9月"
publisher: "三書精讀出版系統"
copyright: |
  **歷代志上研讀** (A Study of the First Book of Chronicles)

  三書精讀出版系統 · 從家譜到聖殿系列

  初版　2026 年 9 月

  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  本版為教會內部贈閱版（非賣品），未公開發行；公開發行時另行申請 ISBN。
  歡迎為個人研讀與教會查經複印使用，請保留完整版權頁。

  **經文版權聲明 (Scripture Copyright Notices)**

  中文經文引自《聖經》和合本（1919），屬公有領域。

  Scripture quotations marked (NASB) are from the NEW AMERICAN STANDARD
  BIBLE®, Copyright © 1960, 1962, 1963, 1968, 1971, 1972, 1973, 1975, 1977,
  1995 by The Lockman Foundation. Used by permission. www.Lockman.org.
  All rights reserved.

  **注疏引用 (Commentary Sources)**

  本書引用之歷代注疏均屬公有領域或依授權引用。逐條出處、版本與核校方式，
  見卷末《附錄：參考資料》。
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

# Front/back matter and volume dividers: same as add_file but marks the H1
# {.unnumbered}. Without this LaTeX numbers EVERY chapter sequentially, so the
# preface, orientation chapters and the volume divider pages would consume
# numbers 1-N and the book's own 第一章 would come out as a mismatched LaTeX
# chapter number. Marking these unnumbered lets the 29 chapters number 1-29.
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
    # %b (not %s) for the description: several volume descriptions carry a
    # literal \n>\n> to open a second blockquote paragraph (the 啟示的次序
    # marker). printf only expands escapes inside the FORMAT string, so with
    # %s those arrive in the markdown as the two characters \ and n and
    # xelatex then dies on "Undefined control sequence \n".
    printf '# %s {.unnumbered}\n\n> %b\n' "$1" "$2" >> "$COMBINED_MD"
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

# The two index tables in 98-appendix-indices.md carry a note saying they are
# generated from the chapter files at build time. Regenerate first so that
# claim is true of the PDF being produced (Job shipped a false version of
# this claim before its generators were wired in here).
echo "🔄 Regenerating indices from chapter sources..."
python3 "$SCRIPT_DIR/gen-chronicl1-scripture-index.py" --write || exit 1
python3 "$SCRIPT_DIR/gen-chronicl1-theme-index.py" --write || exit 1
echo ""

# 前言 — preface
add_front "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位 — orientation: overview, position, spine, revelation order
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這四章：全書地圖、歷代志上在正典的位置、全書的骨幹，以及最要緊的一章——神在這卷書裏按甚麼次序顯明自己。"

add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-position.md"
add_front "$INPUT_DIR/00b-spine.md"
add_front "$INPUT_DIR/00c-revelation-order.md"

# ============================================================
# 正文 · 七部分 · 29 章
# ============================================================
add_volume "一 · 家譜與根源 (Genealogies and Roots) · 1-9章" \
    "神先一一記念每一個名字——包括還沒有走上應許之路的旁支——這在大衛、所羅門任何一件事發生之前就已如此。\n>\n> **啟示的次序·第一步**：神記念，先於神揀選；祂沒有弄丟任何一個名字（1:1—9:44）。"
for f in 01-from-adam-to-esau-and-ishmael.md 02-tribe-of-judah.md 03-royal-house-of-david.md \
         04-prayer-of-jabez.md 05-transjordan-tribes.md 06-tribe-of-levi.md \
         07-northern-tribes.md 08-house-of-saul.md 09-those-who-returned.md; do
    add_chapter "$f"
done

add_volume "二 · 掃羅的結局 (The End of Saul) · 10章" \
    "掃羅求問交鬼的婦人、不求問耶和華，神的國就這樣轉離他、交給大衛。\n>\n> **啟示的次序·第二步**：這是一個警戒，不是一句判詞——不求問神的國度，無論外表多麼強盛，終必傾覆。"
add_chapter "10-end-of-saul.md"

add_volume "三 · 大衛的興起 (David's Rise) · 11-12章" \
    "神從羊圈中揀選一個牧羊人；眾人的心也被神感動、成為「一心」歸向這位神所揀選的王。\n>\n> **啟示的次序·第三步**：合一是神所賜的禮物，不是人手促成的成就。"
for f in 11-david-anointed-and-mighty-men.md 12-all-israel-rallies-to-david.md; do
    add_chapter "$f"
done

add_volume "四 · 約櫃入城 (The Ark Comes Home) · 13-16章" \
    "神的同在絕不能按人的方法擅自搬運；利未人按神所定的規矩抬約櫃，約櫃終於安然進城。\n>\n> **啟示的次序·第四步**：親近神的路，只能按神所定的方式走。"
for f in 13-arks-first-journey-failure.md 14-philistines-defeated.md \
         15-arks-second-journey-success.md 16-davids-song-of-praise.md; do
    add_chapter "$f"
done

add_volume "五 · 大衛之約 (The Davidic Covenant) · 17章" \
    "神親口起誓，要建立的不是一座建築，而是祂自己永遠的家與國，直到那一位真正配得「我要作他的父，他要作我的子」（來1:5）的大衛之子出現。\n>\n> **啟示的次序·第五步，全書最深的一步**：一切成就以先，先有應許。"
add_chapter "17-davidic-covenant.md"

add_volume "六 · 軍事擴張 (Military Expansion) · 18-20章" \
    "神所賜的每一場勝利，不是為叫大衛的名被高舉，而是要清出一片可以安然敬拜的地土。\n>\n> **啟示的次序·第六步**：建殿以先，先有應許之下的得勝。"
for f in 18-victories-philistia-moab-aram-edom.md 19-war-with-ammon-and-aram.md \
         20-fall-of-rabbah-and-giants.md; do
    add_chapter "$f"
done

add_volume "七 · 聖殿籌備 (Preparing the Temple) · 21-29章" \
    "神藉審判定下聖殿的地點，大衛——那流人血的手——不能建殿，卻傾盡一生為殿預備一切，最終交棒給「和平之子」所羅門。\n>\n> **啟示的次序·第七步，也是全書的終點**：開創應許的人，往往看不到應許實現的那一天；但神的計劃不會因此落空。"
for f in 21-census-and-threshing-floor.md 22-preparing-temple-materials.md \
         23-duties-of-the-levites.md 24-priestly-divisions.md 25-divisions-of-singers.md \
         26-gatekeepers-and-treasuries.md 27-military-and-civil-administration.md \
         28-davids-charge-to-solomon.md 29-davids-final-offering-and-prayer.md; do
    add_chapter "$f"
done

# 跋 — afterword.
echo "  Adding (unnumbered): 999-afterword.md"
tail -n +8 "$INPUT_DIR/999-afterword.md" \
  | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}" ; done=1 } } {print}' >> "$COMBINED_MD"
printf '\n\\newpage\n\n' >> "$COMBINED_MD"
((chapter_count++))

# ============================================================
# 附錄 — bibliography and indices
# ============================================================
# Order is bibliography then indices: the index goes last in a printed book.
add_volume "附錄 (Appendices)" \
    "參考資料、經文索引與主題索引——各章正文所指的「卷末附錄」即此。"
add_front "$INPUT_DIR/99-appendix-references.md"
add_front "$INPUT_DIR/98-appendix-indices.md"

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters)"
echo ""
echo "🔨 Generating PDF with chronicl1.latex template..."

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
