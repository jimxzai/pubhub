#!/bin/bash

# Romans PDF Builder - CONSOLIDATED 2026 EDITION (rebuilt in the Gospel-of-John format)
# = preface + orientation (overview / position / spine / systematic reception)
#   + 16 chapters in five volumes with divider pages + 卷末 + appendices + afterword
# Sources from books/bible/roman/ (老弟兄 methodology + MacArthur + Morgan, CUV scripture)
# Uses templates/pdf/romans.latex (Navy/Gold Imperial Rome theme)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/roman"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/romans-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/romans-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/romans.latex"

echo "=========================================="
echo "📖 Romans PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "羅馬書研讀"
subtitle: "Romans Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年8月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **老弟兄查經方法論** — 週四查經班一貫的查經框架之應用

  • **John MacArthur** — 逐節解經 (gty.org)

  • **G. Campbell Morgan** — 解經王子

  **福音書是圖畫，羅馬書是圖畫下面的說明文字**

  「神的義正在這福音上顯明出來；這義是本於信，以致於信。」（羅 1:17）

  **經文版權聲明 (Scripture Copyright Notices)**

  本版為教會內部贈閱版（非賣品）；公開發行時另行申請 ISBN。

  中文經文引自《聖經》和合本（1919），屬公有領域；
  逐章核對來源見附錄二〈參考資料〉之逐章說明。

  Scripture quotations taken from the New American Standard Bible®
  (NASB), Copyright © 1960, 1971, 1977, 1995 by The Lockman Foundation.
  Used by permission. All rights reserved. lockman.org
---

HEADER

chapter_count=0

# Append one source file: strip its 7-line YAML front matter, convert ^n^ verse
# markers to \textsuperscript, then start a new page.
add_file() {
    local f="$1"
    [ -f "$f" ] || { echo "❌ Missing file: $1 — aborting build"; exit 1; }
    echo "  Adding: $(basename "$f")"
    # ^12^ and ^12:34^ both become superscripts; a bare-digit-only pattern
    # silently leaves chapter:verse markers as literal carets in the PDF.
    tail -n +8 "$f" | sed 's/\^\([0-9][0-9:]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Volume divider: a part-title page carrying the volume's theme and,
# optionally, its place in the salvation order ($3 $4 $5).
add_volume() {
    printf '# %s\n\n> %s\n' "$1" "$2" >> "$COMBINED_MD"
    if [ -n "$3" ]; then
        # The separator row must be at least pandoc's --columns threshold (72),
        # or pandoc emits bare `l` columns that cannot wrap and the 鑰節 cell
        # overflows the text block. See scripts/widen-table-separators.py.
        printf '\n| | |\n|----------------------|-----------------------------------------------------------------|\n| **救恩的環節** | %s |\n| **鑰節** | %s |\n| **貫穿的問題** | %s |\n' \
            "$3" "$4" "$5" >> "$COMBINED_MD"
    fi
    printf '\n\\newpage\n\n' >> "$COMBINED_MD"
    echo "  --- $1"
}

# Append the first file matching a chapter-number prefix (e.g. 01-, 07-).
add_chapter() {
    local f
    for f in "$INPUT_DIR/$1-"*.md; do
        [ -f "$f" ] && { add_file "$f"; return 0; }
    done
    echo "❌ Missing chapter file for prefix '$1-' in $INPUT_DIR — aborting build"
    exit 1
}

# 前言 — preface (grace at CCIC, vision, honesty note, purpose)
add_file "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位 — orientation: map, coordinates, spine, method
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這四章：地圖、座標、骨幹、方法。"

add_file "$INPUT_DIR/00-overview.md"
add_file "$INPUT_DIR/00a-romans-position.md"
add_file "$INPUT_DIR/00c-gospel-spine.md"

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
# 正文 · 五卷
# ============================================================
add_volume "卷一 · 福音與定罪 (The Gospel and the Condemnation) · 1-3 章" \
    "先讓每一張嘴都閉口——1:18 到 3:20 是聖經最長的一份起訴書；它存在的唯一理由，是叫 3:21 的「但如今」成為天亮。" \
    "**定罪**——沒有義人，連一個也沒有（3:10）" \
    "3:23「因為世人都犯了罪，虧缺了神的榮耀」" \
    "人為甚麼需要救？"
for i in 01 02 03; do add_chapter "$i"; done

add_volume "卷二 · 因信稱義 (Justification by Faith) · 4-5 章" \
    "兩個見證人（亞伯拉罕與大衛），兩個元首（亞當與基督）。稱義不是感覺，是判決；不是過程，是地位。" \
    "**稱義**——解決罪的刑罰，一次完成" \
    "5:1「我們既因信稱義，就藉著我們的主耶穌基督得與神相和」" \
    "神怎樣救人？"
for i in 04 05; do add_chapter "$i"; done

add_volume "卷三 · 與基督聯合 (Union with Christ) · 6-8 章" \
    "從「豈可仍在罪中」到「不能隔絕的愛」——6 章講地位，7 章講誠實，8 章講確據。" \
    "**成聖**——解決罪的權勢，天天進行" \
    "8:1「如今，那些在基督耶穌裏的就不定罪了」" \
    "得救的人怎樣活？"
for i in 06 07 08; do add_chapter "$i"; done

add_volume "卷四 · 神的主權與以色列 (God's Sovereignty and Israel) · 9-11 章" \
    "若神在以色列身上失信，8 章的確據就站不住腳。這三章不是離題，是應許的保證書——末了以「深哉」的敬拜收尾。" \
    "**揀選**——神的話沒有落空（9:6）" \
    "11:29「因為神的恩賜和選召是沒有後悔的」" \
    "神的應許可靠嗎？"
for i in 09 10 11; do add_chapter "$i"; done

add_volume "卷五 · 活祭 (The Living Sacrifice) · 12-16 章" \
    "前十一章幾乎沒有一句命令句；12:1 的「所以」之後，命令排山倒海——恩典在先，順服在後。" \
    "**生活**——因信稱義的人如何而活" \
    "12:1「將身體獻上，當作活祭，是聖潔的，是神所喜悅的」" \
    "恩典要求甚麼回應？"
for i in 12 13 14 15 16; do add_chapter "$i"; done

# ============================================================
# 卷末 · 望向那一頭 — the road on to Spain and to Revelation
# ============================================================
add_volume "卷末 · 望向那一頭 (Toward the Other End)" \
    "羅馬書自己不收尾——它結在一張還沒走完的行程表上，指著士班雅，也指著新天新地。
>
> 我不以福音為恥；這福音本是神的大能，要救一切相信的。（羅 1:16）"
add_file "$INPUT_DIR/99-to-spain.md"

# ============================================================
# 附錄 — indices & references
# ============================================================
add_volume "附錄 (Appendices)" \
    "經文與主題索引；資料來源與版本之逐章誠實說明。"
python3 "$SCRIPT_DIR/gen-romans-scripture-index.py" --write
add_file "$INPUT_DIR/98-appendix-indices.md"
add_file "$INPUT_DIR/99-appendix-references.md"

# 跋 — afterword (the ministry, the 66-volume prayer).
# Last content file: no trailing \newpage (the template backmatter opens
# its own page; a trailing break here yields a header-only blank page
# whenever the afterword happens to fill its final page exactly).
echo "  Adding: 999-afterword.md"
tail -n +8 "$INPUT_DIR/999-afterword.md" >> "$COMBINED_MD"
((chapter_count++))

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count sections)"
echo ""
echo "🔨 Generating PDF with romans.latex template..."

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
