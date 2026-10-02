#!/bin/bash

# 1 John PDF Builder - CONSOLIDATED 2026 EDITION (built in the Gospel-of-John / James format)
# = preface + orientation (overview / position / revelation-order / systematic reception)
#   + 6 chapters in three volumes with divider pages + 卷末 + appendices + afterword
# Sources from books/bible/john1/ (老弟兄 methodology + Augustine + Calvin + Morgan +
# MacArthur, CUV scripture, NASB 1995)
# Uses templates/pdf/john1.latex (Johannine-letters palette shared with john2.latex)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/john1"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/john1-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/john1-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/john1.latex"

echo "=========================================="
echo "📖 1 John PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

# Regenerate the scripture/topic indices from the chapters themselves, so the
# index can never drift from the book (a hand-kept index always does).
if [ -f "$SCRIPT_DIR/gen-john1-indices.py" ]; then
    python3 "$SCRIPT_DIR/gen-john1-indices.py" || { echo "❌ index generation failed"; exit 1; }
fi

cat > "$COMBINED_MD" << 'HEADER'
---
title: "約翰一書研讀"
subtitle: "First Epistle of John Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年10月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria——榮耀唯獨歸神

  **注疏資源：**

  • **老弟兄查經方法論** — 週四查經班一貫的查經框架之應用

  • **奧古斯丁 (Augustine)** — 《約翰一書講道十篇》（NPNF¹ 第7冊英譯，公有領域）

  • **約翰·加爾文 (John Calvin)** — 大公書信註釋（公有領域）

  • **G. Campbell Morgan** — 《聖經各卷的生命信息》（1912，公有領域）

  • **John MacArthur** — 約翰一書逐節講道 (gty.org)

  • **B. F. Westcott** — *The Epistles of St John*（1892，公有領域；經文鑑別）

  凡加引號的注疏引文，均已與上列原著或逐字講道稿機器核校；各條出處見附錄〈引用出處總表〉。

  **我們愛，因為神先愛我們**

  「我將這些話寫給你們信奉神兒子之名的人，要叫你們知道自己有永生。」（約壹5:13）

  **經文版權聲明 (Scripture Copyright Notices)**

  本版為教會內部贈閱版（非賣品）；公開發行時另行申請 ISBN。

  中文經文引自《聖經》和合本，屬公有領域；底本與逐節覆核來源見附錄〈引用出處總表〉。

  Scripture quotations taken from the New American Standard Bible® (NASB),
  Copyright © 1960, 1962, 1963, 1968, 1971, 1972, 1973, 1975, 1977, 1995 by
  The Lockman Foundation. Used by permission. All rights reserved. lockman.org
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
# optionally, its place in the order of revelation ($3 $4 $5).
# printf %b, not %s, for the description: a literal "\n" inside it must
# become a line break (job/judges/acts each shipped the %s version once).
add_volume() {
    printf '# %s\n\n> %b\n' "$1" "$2" >> "$COMBINED_MD"
    if [ -n "$3" ]; then
        printf '\n| | |\n|----------------|------------------------------------------------------------------------|\n| **貫穿的線** | %s |\n| **鑰節** | %s |\n| **貫穿的問題** | %s |\n' \
            "$3" "$4" "$5" >> "$COMBINED_MD"
    fi
    printf '\n\\newpage\n\n' >> "$COMBINED_MD"
    echo "  --- $1"
}

# Append the first file matching a chapter-number prefix (e.g. 01-, 04-).
add_chapter() {
    local f
    for f in "$INPUT_DIR/$1-"*.md; do
        [ -f "$f" ] && { add_file "$f"; return 0; }
    done
    echo "❌ Missing chapter file for prefix '$1-' in $INPUT_DIR — aborting build"
    exit 1
}

# 前言 — preface
add_file "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位 — orientation: map, coordinates, spine, method
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這四章：地圖、座標、骨幹（啟示的次序與神的計劃），以及全書領受總綱。"

add_file "$INPUT_DIR/00-overview.md"
add_file "$INPUT_DIR/00a-1john-position.md"
add_file "$INPUT_DIR/00c-revelation-order.md"

# 老弟兄 systematic reception — demote headings one level so the whole
# study reads as a single top-level chapter.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱 (Systematic Reception)\n\n' >> "$COMBINED_MD"
    # drop the 7-line YAML + blank line 8 AND the file's own H1 (line 9),
    # then demote all remaining headings by one level
    tail -n +10 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 三卷 — 啟示的次序：神先，人後，六步展開
# ============================================================
add_volume "卷一 · 光中相交 (Fellowship in the Light)" \
    "1:1-2:11 · 啟示的次序·第一、二步：神先顯現——那原與父同在的生命被聽見、看見、摸過；神先是光——光顯出罪，也預備了血與中保。人的回應：相交、認罪、行在光中。" \
    "**相交**——我們乃是與父並他兒子耶穌基督相交的" \
    "1:5「神就是光，在他毫無黑暗」" \
    "我是在光中與神相交，還是只說自己與神相交？"
for i in 01 02; do add_chapter "$i"; done

add_volume "卷二 · 住在主裏面 (Abiding as Children)" \
    "2:12-3:24 · 啟示的次序·第三、四步：神先把道與恩膏放在人裏面，神先賜人兒女的名分。人的回應：住在主裏面、不愛世界、潔淨自己、捨己相愛。" \
    "**住**——你們要住在主裏面" \
    "3:1「你看父賜給我們是何等的慈愛，使我們得稱為神的兒女」" \
    "我是暫時拜訪主，還是住在主裏面？"
for i in 03 04; do add_chapter "$i"; done

add_volume "卷三 · 愛與確據 (Love and Assurance)" \
    "4:1-5:21 · 啟示的次序·第五、六步，也是全書的終點：神先愛我們，差祂兒子作挽回祭；神先為祂兒子作見證，叫信的人知道自己有永生。人的回應：試驗諸靈、彼此相愛、信、遠避偶像。" \
    "**知道**——要叫你們知道自己有永生" \
    "4:19「我們愛，因為神先愛我們」" \
    "我的確據建在自己的感覺上，還是建在神為祂兒子作的見證上？"
for i in 05 06; do add_chapter "$i"; done

# ============================================================
# 卷末 · 這是真神，也是永生 — the book's own closing return
# ============================================================
add_volume "卷末 · 小子們哪，你們要自守 (Little Children, Guard Yourselves)" \
    "約翰一書以「永遠的生命」開卷（1:2），也以「永生」收卷——那位真實的，就是神的兒子耶穌基督。\n>\n> 我們也在那位真實的裏面，就是在他兒子耶穌基督裏面。這是真神，也是永生。小子們哪，你們要自守，遠避偶像！（約壹5:20-21）"

# ============================================================
# 附錄 — indices & references
# ============================================================
add_volume "附錄 (Appendices)" \
    "經文與主題索引；希臘文字彙；讀經計劃；資料來源與引文核校之逐條說明。"
[ -f "$INPUT_DIR/98-appendix-indices.md" ] && add_file "$INPUT_DIR/98-appendix-indices.md"
[ -f "$INPUT_DIR/97-appendix-greek-vocabulary.md" ] && add_file "$INPUT_DIR/97-appendix-greek-vocabulary.md"
[ -f "$INPUT_DIR/96-appendix-reading-plan.md" ] && add_file "$INPUT_DIR/96-appendix-reading-plan.md"
[ -f "$INPUT_DIR/99-appendix-references.md" ] && add_file "$INPUT_DIR/99-appendix-references.md"

# 跋 — afterword. Last content file: no trailing \newpage (the template
# backmatter opens its own page).
echo "  Adding: 999-afterword.md"
tail -n +8 "$INPUT_DIR/999-afterword.md" >> "$COMBINED_MD"
((chapter_count++))

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count sections)"
echo ""
echo "🔨 Generating PDF with john1.latex template..."

# --verbose is load-bearing: without it pandoc swallows the xelatex log and
# every grep-the-log check (here and in driver.sh) passes vacuously.
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
