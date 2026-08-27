#!/bin/bash
# Revelation PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位 (overview/position/spine) + systematic reception
#   + 35 pericope files in seven volumes + bridge + afterword
# Follows the Gospel of John consolidated assembly (build-gospel-consolidated.sh).
# Sources from books/bible/revelation/
# Uses templates/pdf/revelation.latex (Crown of Victory / 得勝之冠 theme)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/revelation"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/revelation-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/revelation-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/revelation.latex"

echo "=========================================="
echo "📖 Revelation PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
  echo "ERROR: Template not found: $TEMPLATE"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "得勝之冠"
subtitle: "啟示錄研讀 Revelation Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年8月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **CCIC 週四查經班** — 第一手屬靈領受

  • **John MacArthur** — 逐節解經 (gty.org)

  • **G.K. Beale / Robert Mounce / Grant Osborne** — 當代福音派注釋

  **聽見的是獅子，看見的卻是羔羊**

  七印、七號、七碗是審判的進程 | 七個得勝應許是給教會的冠冕

  「得勝的，我要賜他在我寶座上與我同坐。」（啟 3:21）

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
    [ -f "$f" ] || { echo "  ⚠️ MISSING: $(basename "$1")"; return 0; }
    echo "  Adding: $(basename "$f")"
    # ^12^ and ^12:34^ both become superscripts; a bare-digit-only pattern
    # silently leaves chapter:verse markers as literal carets in the PDF.
    tail -n +8 "$f" | sed 's/\^\([0-9][0-9:]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Volume divider: a part-title page carrying the volume's theme and,
# optionally, its coordinates ($3 $4 $5: 救恩計劃 / 舊約的根 / 得勝的應許).
add_volume() {
    printf '# %s\n\n> %s\n' "$1" "$2" >> "$COMBINED_MD"
    if [ -n "$3" ]; then
        printf '\n| | |\n|---|---|\n| **救恩計劃** | %s |\n| **舊約的根** | %s |\n| **得勝的應許** | %s |\n' \
            "$3" "$4" "$5" >> "$COMBINED_MD"
    fi
    printf '\n\\newpage\n\n' >> "$COMBINED_MD"
    echo "  --- $1"
}

# Append every file matching a chapter-number prefix, in glob order.
add_chapters() {
    local p f
    for p in "$@"; do
        for f in "$INPUT_DIR/$p"*.md; do
            [ -f "$f" ] && add_file "$f"
        done
    done
}

# 前言 — preface (grace at CCIC, vision, purpose)
add_file "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位 — orientation: map, coordinates, spine, method
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這幾章：地圖、座標、骨幹、方法。"

add_file "$INPUT_DIR/00-overview.md"
add_file "$INPUT_DIR/00a-crown-position.md"
add_file "$INPUT_DIR/00b-lamb-spine.md"

# 老弟兄 systematic reception — demote headings one level so the whole
# study reads as a single top-level chapter.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception)\n\n' >> "$COMBINED_MD"
    # drop the file's own H1 title line, demote all headings by one level
    # (single substitution per line: prepends one # to the leading run, no cascade)
    tail -n +2 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 七卷 — seven volumes, the book's own number
# ============================================================
add_volume "卷一 · 榮耀的人子 (The Glorified Son of Man) · 1章" \
    "拔摩海島上，主日，號筒般的大聲音。第一幅異象不是災難，是基督。" \
    "**顯現**——「我曾死過，現在又活了」（1:18）" \
    "但以理書 7 章的人子、10 章的異象" \
    "「不要懼怕」（1:17）——冠冕之路從敬拜起步"
add_chapters 01

add_volume "卷二 · 七教會——地上的燈臺 (The Seven Churches) · 2-3章" \
    "七封信，一位在燈臺中間行走的主。每一封都以「得勝的」作結。" \
    "**察驗**——主知道教會的行為（2:2 等七次「我知道」）" \
    "以西結書的守望者、何西阿書的失落之愛" \
    "生命樹、白衣、寶座——七個應許，全在 21-22 章兌現"
add_chapters 02 03

add_volume "卷三 · 寶座與羔羊 (The Throne and the Lamb) · 4-5章" \
    "地上風浪之前，先看天上的寶座。聽見的是獅子，看見的卻是羔羊。" \
    "**掌權**——寶座立定，書卷交在羔羊手中" \
    "以賽亞書 6 章、以西結書 1 章的寶座異象；創世記 49:9 猶大的獅子" \
    "「在我寶座上與我同坐」（3:21）的根據，在第 4-5 章"
add_chapters 04 05

add_volume "卷四 · 七印七號——審判的展開 (Seals and Trumpets) · 6-11章" \
    "羔羊揭印，天使吹號。審判層層加深，恩典的印記卻先蓋在額上。" \
    "**審判與保守**——災難之前，先印了十四萬四千人（7:3）" \
    "出埃及記的十災、約珥書的號角" \
    "「世上的國成了我主和主基督的國」（11:15）"
add_chapters 06 07

add_volume "卷五 · 宇宙的爭戰 (The Cosmic War) · 12-14章" \
    "幔子拉開：婦人與龍、海獸與地獸、錫安山上的羔羊。爭戰的真相在此。" \
    "**爭戰**——「弟兄勝過牠，是因羔羊的血」（12:11）" \
    "創世記 3:15 女人的後裔要傷蛇的頭" \
    "跟隨羔羊的十四萬四千人，額上有父的名（14:1）"
add_chapters 08

add_volume "卷六 · 七碗與巴比倫的傾倒 (Bowls and Babylon) · 15-18章" \
    "神的大怒在七碗中倒盡；大淫婦巴比倫，一時之間傾倒了。" \
    "**傾倒**——「成了！」（16:17）審判的成了，呼應十架救贖的成了" \
    "出埃及記的災、以賽亞書耶利米書的巴比倫神諭" \
    "「我的民哪，你們要從那城出來」（18:4）"
add_chapters 09 10

add_volume "卷七 · 羔羊得勝——再來、國度、新創造 (The Lamb's Victory) · 19-22章" \
    "羔羊的婚筵擺設，白馬騎士出征，白色大寶座立定，新耶路撒冷降下。" \
    "**成全**——「都成了！我是阿拉法，我是俄梅戛」（21:6）" \
    "創世記 1-3 章：伊甸失去的，在此全數歸回，且有加增" \
    "「得勝的，必承受這些為業」（21:7）"
add_chapters 11 12 13 14

# ============================================================
# 卷末 · 回到起初 — the arc back to Genesis, and the last prayer
# ============================================================
add_volume "卷末 · 回到起初 (Back to the Beginning)" \
    "聖經的最後一卷書，把第一卷書失去的都找了回來。
>
> 證明這事的說：是了，我必快來！阿們！主耶穌阿，我願你來！（啟 22:20）"
add_file "$INPUT_DIR/99-back-to-the-beginning.md"

# 跋 — afterword (the ministry, the 66-volume prayer).
# Last content file: no trailing \newpage (the template backmatter opens
# its own page; a trailing break here yields a header-only blank page
# whenever the afterword happens to fill its final page exactly).
if [ -f "$INPUT_DIR/999-afterword.md" ]; then
    echo "  Adding: 999-afterword.md"
    tail -n +8 "$INPUT_DIR/999-afterword.md" >> "$COMBINED_MD"
    ((chapter_count++))
fi

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count files)"
echo ""
echo "🔨 Generating PDF with revelation.latex template..."

pandoc "$COMBINED_MD" \
  -o "$OUTPUT_PDF" \
  --pdf-engine=xelatex \
  --template="$TEMPLATE" \
  --from=markdown-superscript-subscript \
  --toc \
  --toc-depth=1 \
  --top-level-division=chapter \
  -V tocdepth=0

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ PDF generated: $OUTPUT_PDF ($(du -h "$OUTPUT_PDF" | cut -f1))"
else
    echo "❌ PDF generation failed"
    exit 1
fi
