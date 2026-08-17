#!/bin/bash

# Gospel of John PDF Builder - CONSOLIDATED 2026 EDITION
# = 21 chapters + Elder Wong systematic reception (structure-based deep study)
# Uses the system default template: templates/pdf/gospel-of-john.latex

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/gospel-of-john"
ORDER_FILE="$INPUT_DIR/00a-revelation-order.md"
KEY_FILE="$INPUT_DIR/00b-i-am-deity.md"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/gospel-of-john-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/gospel-of-john-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/gospel-of-john.latex"

echo "=========================================="
echo "📖 Gospel of John PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "約翰福音研讀"
subtitle: "Gospel of John Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年8月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **CCIC 週四查經班** — 第一手屬靈領受

  • **John MacArthur** — 逐節解經 (gty.org)

  • **G. Campbell Morgan** — 解經王子 (1909)

  **榮耀 = 恩典 + 真理**

  七個神蹟 (works) 彰顯恩典 | 「我是」(words) 彰顯真理

  兆頭是圖畫，「我是」是圖畫下面的說明文字

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

# Volume divider: a part-title page carrying the volume's theme and,
# optionally, its place in the salvation plan / the Spirit's position /
# the Revelation harvest ($3 $4 $5; see 00a-revelation-order.md 總表).
add_volume() {
    printf '# %s\n\n> %s\n' "$1" "$2" >> "$COMBINED_MD"
    if [ -n "$3" ]; then
        printf '\n| | |\n|---|---|\n| **救恩計劃** | %s |\n| **聖靈在哪裡** | %s |\n| **啟示錄的收成** | %s |\n' \
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

# 前言 — preface (grace at CCIC, vision, purpose)
add_file "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位 — orientation: map, coordinates, spine, method
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這四章：地圖、座標、骨幹、方法。"

add_file "$INPUT_DIR/00-overview.md"
add_file "$ORDER_FILE"
add_file "$KEY_FILE"

# Elder Wong systematic reception — demote headings one level so the whole
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
# 正文 · 五卷
# ============================================================
add_volume "卷一 · 序言——道 (Prologue: The Word) · 1:1-18" \
    "十八節，抵一部系統神學。永恆切入時間。" \
    "**賜下**——神把獨生子給出去" \
    "1:32「彷彿鴿子從天降下，住在他的身上」" \
    "19:13「祂的名稱為神之道」"
add_chapter 01

add_volume "卷二 · 兆頭之書——信與不信的交戰 (The Book of Signs) · 1:19-12:50" \
    "三年半的事工，十二章。兆頭是圖畫，「我是」是圖畫下面的說明文字。" \
    "**陳明**——信與不信分開（1:12）" \
    "7:39「那時還沒有賜下聖靈來，因為耶穌尚未得著榮耀」" \
    "5:6 羔羊站立，像是被殺過的"
for i in 01b 02 03 04 04b 05 06 07 08 09 10 11 12; do add_chapter "$i"; done

add_volume "卷三 · 榮耀之書·樓上私語——愛 (The Upper Room) · 13-17" \
    "一個晚上，五章。祂既然愛世間屬自己的人，就愛他們到底。" \
    "**預告內化**——住在我裡面" \
    "14:17「常與你們同在，也要在你們裡面」" \
    "21:3 神的帳幕在人間"
for i in 13 14 15 16 17; do add_chapter "$i"; done

add_volume "卷四 · 榮耀之書·受難復活——榮耀的高峰 (Passion & Resurrection) · 18-20" \
    "三天，三章。榮耀的高峰不在寶座，在十字架——「成了」。" \
    "**成全**——τετέλεσται，成全了且永遠成全著" \
    "20:22「就向他們吹一口氣，說：你們受聖靈！」" \
    "1:18「我曾死過，現在又活了」"
for i in 18 19 20; do add_chapter "$i"; done

add_volume "卷五 · 跋——爐火邊的恢復與差遣 (Epilogue) · 21" \
    "一頓早餐，一章。三次問，對著三次否認。" \
    "**傳遞**——你餵養我的羊" \
    "20:21「父怎樣差遣了我，我也照樣差遣你們」——五旬節在書外（徒 2）" \
    "22:17「聖靈和新婦都說：來！」"
add_chapter 21

# ============================================================
# 卷末 · 望向那一頭 — the arc into Revelation
# ============================================================
add_volume "卷末 · 望向那一頭 (Toward the Other End)" \
    "約翰福音自己不收尾——它結在「等到我來的時候」，指著另一卷書。"
add_file "$INPUT_DIR/99-to-revelation.md"

# 跋 — afterword (the ministry, the 66-volume prayer)
add_file "$INPUT_DIR/999-afterword.md"

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters)"
echo ""
echo "🔨 Generating PDF with default template (gospel-of-john.latex)..."

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
