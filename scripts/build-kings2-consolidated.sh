#!/bin/bash

# 2 Kings PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine) + 全書領受總綱 + 六卷 25 章 + 卷末 + 跋
# Uses templates/pdf/kings2.latex (Mantle/Lamp/Exile theme, matching the Gospel
# of John / Acts of the Apostles / Isaiah / Job / 2 Kings series standard: cover art,
# frontispiece)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/kings2"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/kings2-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/kings2-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/kings2.latex"

echo "=========================================="
echo "🕯  2 Kings Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

# 98-appendix-indices.md's two generated tables carry a note saying they are
# built from the chapter files at build time. That note was false until these
# generators were wired in here (same gap as build-job-consolidated.sh once had).
echo "🔄 Regenerating indices from chapter sources..."
python3 "$SCRIPT_DIR/gen-kings2-scripture-index.py" --write || exit 1
python3 "$SCRIPT_DIR/gen-kings2-theme-index.py" --write || exit 1
echo ""

cat > "$COMBINED_MD" << 'HEADER'
---
title: "列王紀下研讀"
subtitle: "2 Kings Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年10月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **核心資源整合：**

  • **老弟兄查經法** — 方法性撮述（本卷無第一手教導筆記，詳見前言）

  • **G. Campbell Morgan** — 《Exposition on the Whole Bible》列王紀下逐章概述

  • **Matthew Henry ／ Albert Barnes ／ Cambridge Bible for Schools and Colleges** 等公有領域注疏
    （見卷末《附錄：引用出處總表》逐章說明）

  • **John MacArthur** — gty.org 講道（限於現存講章涵蓋之處）

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

# Volume divider: a part-title page carrying the volume's theme.
# Front/back matter and volume dividers: same as add_file but marks the H1
# {.unnumbered}. Without this LaTeX numbers EVERY chapter sequentially, so the
# preface, orientation chapters and the six volume divider pages consume
# numbers ahead of the book's own 第一章 — the contents page would then read
# two conflicting numbers on one line. Marking these unnumbered lets the 21
# study units number 1-21, matching 第一章-第二十一章. Same approach as
# build-job-consolidated.sh / build-isaiah-consolidated.sh.
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
    # xelatex then dies on "Undefined control sequence \n". Same convention
    # as build-job-consolidated.sh.
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

# 前言 — preface
add_front "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位 — orientation: overview, position, spine
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這幾章：總覽、位置、骨幹。"

add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-kings2-position.md"
add_front "$INPUT_DIR/00b-word-spine.md"

# Systematic reception — demote headings one level so it reads as one chapter.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
    tail -n +2 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 六卷 · 25 章
# ============================================================
add_volume "卷一 · 接棒：話語的傳承 (The Handing On) · 1-2章" \
    "一個王因問錯了神而病死，一位先知被旋風接去，另一位撿起他掉下的外衣——全書的第一幕，是話語從一個人手上交到另一個人手上。\n>\n> **啟示的次序·第一步（話先出口）**：全書第一個「照耶和華……所說的話」（1:17）就在這裏；以利亞的火證明神在以色列中，卻不是那位要降下來救人的。"
for f in 01-ahaziah-and-the-fire.md 02-whirlwind-and-mantle.md; do
    add_chapter "$f"
done

add_volume "卷二 · 以利沙：話語在人間行走 (Elisha) · 3-8章" \
    "水從沒有風雨的谷中湧出，油倒到沒有器皿，餅吃了還剩下，敵人的眼睛被昏迷又被打開——話語一出口，事就跟著發生。\n>\n> **啟示的次序·第一步（話先出口）**：這六章裏，「照……的話」出現了五節（4:44；5:14；6:18；7:16；8:2）；王的命令走不出城門，神人的話卻一路應驗。"
for f in 03-three-kings-and-moab.md 04-oil-upper-room-and-pot.md 05-naaman.md \
         06-axe-head-and-chariots-of-fire.md 07-four-lepers.md 08-hazael-and-the-lamp.md; do
    add_chapter "$f"
done

add_volume "卷三 · 衰亡：北國的結局 (The Decline) · 9-17章" \
    "耶戶的革命、亞他利雅的篡位、約阿施修殿、以利沙之死、王如更替，最後是撒瑪利亞淪亡——九章走完北國，猶大在旁邊搖搖欲墜。\n>\n> **啟示的次序·第二步（憐憫延遲審判）**：耶戶得「四代」的應許，約哈斯一懇求神就賜拯救者，「尚未趕逐」（13:23）——然後作者停下來，用「這是因為」交代北國為何亡（17:7）。"
for f in 09-jehu-anointed.md 10-jehus-zeal.md 11-athaliah-and-joash.md \
         12-joash-repairs-the-temple.md 13-elishas-last-arrows.md \
         14-amaziah-and-jeroboam-ii.md 15-kings-come-and-go.md \
         16-ahaz-and-the-altar.md 17-fall-of-samaria.md; do
    add_chapter "$f"
done

add_volume "卷四 · 希西家：信靠與驕傲 (Hezekiah) · 18-20章" \
    "亞述的大軍壓境，拉伯沙基在城牆下喊話；希西家把書信展開在耶和華面前；一夜之間，圍城解除——然後王病了，又讓巴比倫的使者看了他的寶庫。\n>\n> **啟示的次序·第三步（話被遺失又被尋見）**：希西家「專靠耶和華，總不離開」（18:6），是全書北國諸王沒有得到的稱讚；但他最後一次對話的結論，是以賽亞對巴比倫的預告（20:17）。"
for f in 18-hezekiah-and-rabshakeh.md 19-prayer-and-the-angel.md \
         20-hezekiahs-illness-and-babylon.md; do
    add_chapter "$f"
done

add_volume "卷五 · 瑪拿西與約西亞：遺失又尋見的話 (Manasseh and Josiah) · 21-23章" \
    "猶大史上最長的在位，也是最壞的一個；然後是最後一次復興——律法書在耶和華殿裏被人尋見。\n>\n> **啟示的次序·第三步（話被遺失又被尋見）**：話一直在殿裏，只是被遺失了；約西亞聽見，撕裂衣服（22:11）；他是全書最「盡心、盡性、盡力」的王（23:25），卻擋不住瑪拿西種下的後果（23:26-27）。"
for f in 21-manasseh-and-amon.md 22-the-book-found.md 23-josiahs-reformation.md; do
    add_chapter "$f"
done

add_volume "卷六 · 終局：燈與桌子 (The Lamp and the Table) · 24-25章" \
    "巴比倫三次圍城，殿被焚，王被擄，百姓離鄉；全書最後四節，卻是一張桌子。\n>\n> **啟示的次序·第四步（審判之後，燈仍亮著）**：審判寫完了，作者沒有寫悔改，也沒有寫歸回，他寫約雅斤「終身常在巴比倫王面前吃飯」（25:29）——8:19 那句「永遠賜燈光」，還沒有被吹熄。"
for f in 24-jehoiakim-and-jehoiachin.md 25-fall-of-jerusalem.md; do
    add_chapter "$f"
done

# ============================================================
# 卷末 · 沒有王，直到真王
# ============================================================
add_volume "卷末 · 燈仍亮著 (The Lamp Is Still Burning)" \
    "列王紀下以一張桌子收尾，沒有說這盞燈要怎樣重新亮起——這個空白，要等到新約的第一句才有人填上。"
add_front "$INPUT_DIR/99-the-lamp-still-burns.md"

# 附錄：引用出處總表——每一章都承諾「見卷末《附錄：引用出處總表》」，
# 這份檔案卻從未被加進建置腳本；書目先於索引，是出版慣例（見約伯記第七輪）。
add_front "$INPUT_DIR/99-appendix-references.md"

# 附錄：經文與主題索引——跨書經文索引由 scripts/gen-kings2-scripture-index.py
# 於原始檔案自動生成，見該檔案與 98-appendix-indices.md 內的說明。
add_front "$INPUT_DIR/98-appendix-indices.md"

# 跋 — afterword. Last content file: no trailing \newpage.
echo "  Adding (unnumbered): 999-afterword.md"
tail -n +8 "$INPUT_DIR/999-afterword.md" \
  | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}" ; done=1 } } {print}' >> "$COMBINED_MD"
((chapter_count++))

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters)"
echo ""
echo "🔨 Generating PDF with kings2.latex template..."

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
