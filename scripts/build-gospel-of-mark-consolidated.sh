#!/bin/bash

# Gospel of Mark PDF Builder - CONSOLIDATED 2026 EDITION
# = preface + 4-chapter orientation + 20 chapters in 4 parts + epilogue chapter + afterword
# Mirrors scripts/build-gospel-consolidated.sh (Gospel of John).
# Uses the dedicated template: templates/pdf/gospel-of-mark.latex

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/gospel-of-mark"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/gospel-of-mark-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/gospel-of-mark-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/gospel-of-mark.latex"

echo "=========================================="
echo "📖 Gospel of Mark PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "馬可福音研讀"
subtitle: "Gospel of Mark Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年8月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **老弟兄查經法** — 週四查經班領受的讀經進路

  • **John MacArthur** — 逐節解經 (gty.org)

  • **G. Campbell Morgan** — 解經王子 (*The Gospel According to Mark*, 1927)

  **僕人基督——外院的祭壇與洗濯盆**

  「因為人子來，並不是要受人的服事，乃是要服事人，並且要捨命作多人的贖價。」——馬可福音 10:45

  服事（洗濯盆）在前十章 | 捨命（祭壇）在後六章

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
    # ^12^ and ^12:34^ both become superscripts; a bare-digit-only pattern
    # silently leaves chapter:verse markers as literal carets in the PDF.
    tail -n +8 "$f" | sed 's/\^\([0-9][0-9:]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Part divider: a part-title page carrying the part's theme and,
# optionally, its place in the outer-court picture / the book's spine /
# the harvest at the throne ($3 $4 $5; see 00a and 00c orientation chapters).
add_volume() {
    printf '# %s\n\n> %s\n' "$1" "$2" >> "$COMBINED_MD"
    if [ -n "$3" ]; then
        printf '\n| | |\n|---|---|\n| **外院的位置** | %s |\n| **全書骨幹** | %s |\n| **寶座的收成** | %s |\n' \
            "$3" "$4" "$5" >> "$COMBINED_MD"
    fi
    printf '\n\\newpage\n\n' >> "$COMBINED_MD"
    echo "  --- $1"
}

# Append the first file matching a chapter-number prefix (e.g. 01b-, 07-).
add_chapter() {
    local f
    for f in "$INPUT_DIR/$1-"*.md; do
        [ -f "$f" ] && { add_file "$f"; return 0; }
    done
}

# 前言 — preface (second station of the 66-volume prayer)
add_file "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位 — orientation: map, coordinates, spine, method
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這四章：地圖、座標、骨幹、方法。"

add_file "$INPUT_DIR/00-overview.md"
add_file "$INPUT_DIR/00a-servant-position.md"
add_file "$INPUT_DIR/00c-servant-spine.md"
add_file "$INPUT_DIR/00b-systematic-reception.md"

# ============================================================
# 正文 · 四部
# ============================================================
add_volume "序言 · 預備道路——僕人登場 (Prologue) · 1:1-13" \
    "十三節，三幕戲：被預告、被印證、被試驗。僕人不需要家譜——第一章第九節，祂已經站在約但河裡了。" \
    "**進院門**——曠野的人聲替主開路" \
    "1:1「神的兒子」——作者向讀者交底" \
    "啟 22:16「我是大衛的根，又是他的後裔」"
for i in 01a 01b 01c; do add_chapter "$i"; done

add_volume "第一部 · 加利利事工——僕人的服事 (Galilean Ministry) · 1:14-8:26" \
    "服事的展開，衝突的升高，身分的追問——「這到底是誰？」八章的服事，就為逼出一個答案。" \
    "**洗濯盆**——醫病、趕鬼、餵飽、趕路" \
    "εὐθύς「立刻」——僕人的步伐" \
    "來 7:25「他是長遠活著，替他們祈求」"
for i in 01d 02 03 04 05 06 07 08a; do add_chapter "$i"; done

add_volume "第二部 · 走向耶路撒冷——僕人的道路 (The Way to Jerusalem) · 8:27-10:52" \
    "書脊在這裡：彼得答對了名字，答錯了意思。三次預言，三次跌倒，三堂僕人的課——結在 10:45。" \
    "**從盆到壇的那段路**——兩個瞎子作前後的括號" \
    "8:29「你們說我是誰」→ 10:45「捨命作多人的贖價」" \
    "啟 5:9「用自己的血……買了人來」"
for i in 08b 09 10; do add_chapter "$i"; done

add_volume "第三部 · 受難與復活——僕人的犧牲與高升 (Passion & Resurrection) · 11:1-16:20" \
    "三年寫十章，八天寫六章——急的是服事，慢的是捨命。幔子裂開，百夫長說出全書等了十五章的那句話。" \
    "**祭壇**——祭牲上壇，幔子從上到下裂為兩半" \
    "15:39「這人真是神的兒子」——彌賽亞隱秘的謎底" \
    "啟 5:6「羔羊站立，像是被殺過的」"
for i in 11 12 13 14 15 16; do add_chapter "$i"; done

# ============================================================
# 卷末 · 望向那一頭 — the arc into Acts, 1 Peter, Revelation
# ============================================================
add_volume "卷末 · 望向那一頭 (Toward the Other End)" \
    "馬可福音自己不收尾——第一句話說「起頭」，最後一句話說「同工」。
>
> 門徒出去，到處宣傳福音。主和他們同工，用神蹟隨著，證實所傳的道。阿們！（可 16:20）"
add_file "$INPUT_DIR/99-to-the-throne.md"

# 跋 — afterword (the ministry, the 66-volume prayer).
# Last content file: no trailing \newpage (the template backmatter opens
# its own page; a trailing break here yields a header-only blank page
# whenever the afterword happens to fill its final page exactly).
echo "  Adding: 999-afterword.md"
tail -n +8 "$INPUT_DIR/999-afterword.md" >> "$COMBINED_MD"
((chapter_count++))

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters)"
echo ""
echo "🔨 Generating PDF with dedicated template (gospel-of-mark.latex)..."

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
