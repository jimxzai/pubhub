#!/bin/bash

# Acts of the Apostles PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine) + 全書領受總綱 + 五卷 28 章 + 卷末 + 跋
# Uses templates/pdf/acts.latex (Flame/Ember theme, matching the Gospel of John /
# Gospel Harmony Liturgical series standard: cover art, frontispiece, map, appendices)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/acts"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/acts-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/acts-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/acts.latex"

echo "=========================================="
echo "🔥 Acts of the Apostles PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "使徒行傳研讀"
subtitle: "Acts of the Apostles Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年8月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **週四查經班** — 第一手屬靈教導

  • **John MacArthur** — 逐節解經 (gty.org)

  • **G. Campbell Morgan** — 《使徒行傳》(1924)

  **能力 = 聖靈藉見證彰顯**

  耶路撒冷 (1-7章) | 猶太·撒瑪利亞 (8-12章) | 直到地極·第一次差遣 (13-15章)
  進入歐洲 (16-20章) | 捆鎖中的見證·直到羅馬 (21-28章)

  **經文版權聲明 (Scripture Copyright Notices)**

  本版為教會內部贈閱版（非賣品）；公開發行時另行申請 ISBN。

  中文經文引自《聖經》和合本（1919），屬公有領域。

  Scripture quotations taken from the New American Standard Bible® (NASB),
  Copyright © 1960, 1971, 1977, 1995 by The Lockman Foundation. Used by
  permission. All rights reserved. lockman.org
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

# Volume divider: a part-title page carrying the volume's theme and its
# position in the 1:8 progression / the Spirit's work / the "道的增長" summary verse.
add_volume() {
    printf '# %s\n\n> %s\n' "$1" "$2" >> "$COMBINED_MD"
    if [ -n "$3" ]; then
        printf '\n| | |\n|---|---|\n| **1:8 座標** | %s |\n| **聖靈的動作** | %s |\n| **道的增長** | %s |\n' \
            "$3" "$4" "$5" >> "$COMBINED_MD"
    fi
    printf '\n\\newpage\n\n' >> "$COMBINED_MD"
    echo "  --- $1"
}

# Append the file matching an exact chapter filename (no combined-file globbing —
# every chapter is now its own file).
add_chapter() {
    add_file "$INPUT_DIR/$1"
}

# 前言 — preface
add_file "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位 — orientation: overview, position, spine
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這幾章：總覽、位置、骨幹、方法。"

add_file "$INPUT_DIR/00-overview.md"
add_file "$INPUT_DIR/00a-acts-position.md"
add_file "$INPUT_DIR/00b-witness-spine.md"

# Systematic reception — demote headings one level so it reads as one chapter.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception)\n\n' >> "$COMBINED_MD"
    tail -n +2 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 五卷 · 28 章
# ============================================================
add_volume "卷一 · 耶路撒冷——你們就必得著能力 (Jerusalem) · 1-7章" \
    "等候、澆灌、放膽——福音從一座城的一間樓房開始。" \
    "耶路撒冷" "澆灌降臨（2:4）" "6:7 神的道興旺起來"
for f in 01-ascension.md 02-pentecost.md 03-beautiful-gate.md 04-no-other-name.md \
         05-ananias.md 06-the-seven.md 07-stephen.md; do
    add_chapter "$f"
done

add_volume "卷二 · 猶太全地和撒瑪利亞——門被推開 (Judea and Samaria) · 8-12章" \
    "逼迫叫門徒四散，四散卻叫福音蔓延——門一道一道被聖靈推開。" \
    "猶太·撒瑪利亞" "分散中引路（8:29, 39；10:19-20, 44）" "9:31；12:24"
for f in 08-philip.md 09-damascus-road.md 10-cornelius.md 11-antioch.md 12-herod-peter.md; do
    add_chapter "$f"
done

add_volume "卷三 · 直到地極·第一次差遣 (To the Ends of the Earth: First Sending) · 13-15章" \
    "聖靈親自從教會中分派差遣——福音第一次有計劃地走出耶路撒冷。" \
    "地極——小亞細亞" "分派差遣（13:2）" "16:5 信心越發堅固"
for f in 13-sent-by-the-spirit.md 14-through-tribulations.md 15-jerusalem-council.md; do
    add_chapter "$f"
done

add_volume "卷四 · 直到地極·進入歐洲 (To the Ends of the Earth: Into Europe) · 16-20章" \
    "馬其頓的呼聲，把福音第一次帶過了海——從此走向整個地中海世界。" \
    "馬其頓·亞該亞·亞細亞" "禁止與呼召（16:6-10）" "19:20 主的道大大興旺"
for f in 16-macedonian-call.md 17-unknown-god.md 18-corinth.md 19-ephesus.md 20-miletus-farewell.md; do
    add_chapter "$f"
done

add_volume "卷五 · 捆鎖中的見證·直到羅馬 (Bound Witness: To Rome) · 21-28章" \
    "鎖鏈沒有捆住福音——保羅在囚禁、審訊、風暴中，把見證一路帶到了羅馬。" \
    "羅馬" "在捆鎖中作證（20:23；23:11）" "28:31 並沒有人禁止"
for f in 21-bound-for-jerusalem.md 22-stairs-testimony.md 23-lord-stood-by.md \
         24-before-felix.md 25-appeal-to-caesar.md 26-heavenly-vision.md \
         27-storm-witness.md 28-unhindered.md; do
    add_chapter "$f"
done

# ============================================================
# 卷末 · 未完的行傳
# ============================================================
add_volume "卷末 · 未完的行傳 (The Unfinished Acts)" \
    "使徒行傳自己不收尾——它結在一個副詞上：「並沒有人禁止」，指著教會歷史與讀者的生命。
>
> 保羅在自己所租的房子裏，住了足足兩年。凡來見他的人，他全都接待，放膽傳講神國的道，將主耶穌基督的事教導人，並沒有人禁止。（徒 28:30-31）"
add_file "$INPUT_DIR/99-unfinished-acts.md"

# 跋 — afterword. Last content file: no trailing \newpage.
echo "  Adding: 999-afterword.md"
tail -n +8 "$INPUT_DIR/999-afterword.md" >> "$COMBINED_MD"
((chapter_count++))

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters)"
echo ""
echo "🔨 Generating PDF with acts.latex template..."

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
