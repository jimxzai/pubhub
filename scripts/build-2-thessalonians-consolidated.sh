#!/bin/bash

# 2 Thessalonians PDF Builder - CONSOLIDATED 2026 EDITION (James / Gospel-of-John format)
# = preface + orientation (overview / position / revelation-order / systematic reception)
#   + 7 chapters in four volumes (the four steps of the spine) + 卷末 + appendices + afterword
# Sources from books/bible/thessanlonian2/ (老弟兄 methodology + Chrysostom, Calvin,
# Morgan, MacArthur; CUV + NASB 1995 scripture)
# Uses templates/pdf/2-thessalonians.latex (Dusk Plum / Scripture Gold theme)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/thessanlonian2"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/2-thessalonians-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/2-thessalonians-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/2-thessalonians.latex"

echo "=========================================="
echo "📖 2 Thessalonians PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

# Regenerate the indices from the chapters before every build, so the
# appendix can never drift from the text it indexes.
python3 "$SCRIPT_DIR/gen-2-thessalonians-scripture-index.py" --write || exit 1
python3 "$INPUT_DIR/sources/gen_ledger.py" || exit 1

cat > "$COMBINED_MD" << 'HEADER'
---
title: "帖撒羅尼迦後書研讀"
subtitle: "Second Thessalonians Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年10月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **資源整合：**

  • **老弟兄查經方法論** — 查經框架與提問帶領之應用（本卷無老弟兄論帖撒羅尼迦後書的第一手講章，書中不引述其語錄，見〈前言〉）

  • **屈梭多模 John Chrysostom** — 《帖撒羅尼迦後書講道集》（NPNF¹ 13，公有領域）

  • **John Calvin** — 帖撒羅尼迦後書註釋（John Pringle 英譯，公有領域）

  • **G. Campbell Morgan** — 《聖經各卷的生命信息》（1912，公有領域）

  • **John MacArthur** — 帖撒羅尼迦後書逐段講道，1992 (gty.org)

  **你們要站立得穩**

  「所以，弟兄們，你們要站立得穩，凡所領受的教訓，不拘是我們口傳的，是信上寫的，都要堅守。」（帖後2:15）

  **經文版權聲明 (Scripture Copyright Notices)**

  本版為教會內部贈閱版（非賣品）；公開發行時另行申請 ISBN。

  中文經文引自《聖經》和合本，屬公有領域；
  逐章核對來源見附錄〈參考資料〉之逐章說明。

  Scripture quotations taken from the New American Standard Bible® (NASB),
  Copyright © 1960, 1971, 1977, 1995 by The Lockman Foundation. Used by
  permission. All rights reserved. lockman.org

  All rights reserved.
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
add_volume() {
    # {.unnumbered}: dividers are not chapters, so the seven study chapters
    # print as 1-7, matching the 第N章 the book's own text and indices use
    printf '# %s {.unnumbered}\n\n> %s\n' "$1" "$2" >> "$COMBINED_MD"
    if [ -n "$3" ]; then
        printf '\n| | |\n|---|---|\n| **貫穿的線** | %s |\n| **鑰節** | %s |\n| **貫穿的問題** | %s |\n' \
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
# 卷首 · 定位 — orientation: map, coordinates, spine, reception
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這三章：地圖、座標、骨幹——啟示的次序與神的計劃。"

add_file "$INPUT_DIR/00-overview.md"
add_file "$INPUT_DIR/00a-2thess-position.md"
add_file "$INPUT_DIR/00c-revelation-order.md"

# 老弟兄 systematic reception — demote headings one level so the whole
# study reads as a single top-level chapter.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
    # drop the 7-line YAML frontmatter + blank line 8 AND the file's own H1
    # (line 9), then demote remaining headings one level
    tail -n +10 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 四卷 — 啟示的次序：那日必到 → 那日未到 → 從起初到榮光 → 按次序而活
# ============================================================
add_volume "卷一 · 那日必到 (The Day Will Surely Come)" \
    "1章 · 啟示的次序·第一步：神已在患難中動工，祂公義的審判必要來到——主耶穌必從天上顯現。" \
    "**那日必到**——神是公義的，主耶穌必從天上顯現" \
    "1:7「主耶穌同他有能力的天使從天上在火焰中顯現」" \
    "我在患難中，看得見神正在動工、也必要審判嗎？"
for i in 01 02; do add_chapter "$i"; done

add_volume "卷二 · 那日未到 (Not Before Its Appointed Order)" \
    "2:1-12 · 啟示的次序·第二步：神定了先後——必先有離道反教，不法的人要到了的時候才顯露，主一口氣就滅絕他。" \
    "**那日未到**——那日子以前必有先後" \
    "2:3「那日子以前，必有離道反教的事」" \
    "有人說「現在到了」的時候，我是動心，還是站在神的次序上？"
for i in 03 04; do add_chapter "$i"; done

add_volume "卷三 · 從起初到榮光 (From the Beginning to Glory)" \
    "2:13-17 · 啟示的次序·第三步，也是全書的地基：末世的時間表安放在神永恆的次序裏——從起初揀選，到得著主耶穌基督的榮光。" \
    "**從起初到榮光**——揀選、成聖、呼召、得榮" \
    "2:13「他從起初揀選了你們」" \
    "我是站在那不法者的短線上，還是站在神從起初到榮光的長線上？"
add_chapter "05"

add_volume "卷四 · 按次序而活 (Living in Step with God's Order)" \
    "3章 · 啟示的次序·第四步：知道神次序的人，今天就按次序而活——禱告、倚靠信實的主、安靜做工、行善不喪志。" \
    "**按次序而活**——時候的次序帶出生活的次序" \
    "3:12「要安靜做工，吃自己的飯」" \
    "我的日子，是在神的行列裏，還是脫了隊？"
for i in 06 07; do add_chapter "$i"; done

# ============================================================
# 卷末 · 賜平安的主 — the book's own closing return
# ============================================================
add_volume "卷末 · 賜平安的主 (The Lord of Peace)" \
    "帖撒羅尼迦後書不結在末世的圖表上，結在一句祝福裏：神的次序，終點是平安。
>
> 願賜平安的主隨時隨事親自給你們平安！願主常與你們眾人同在！（帖後3:16）"

# ============================================================
# 附錄 — indices & references
# ============================================================
add_volume "附錄 (Appendices)" \
    "經文與主題索引；希臘文字彙；讀經計劃；資料來源與版本之逐章誠實說明。"
[ -f "$INPUT_DIR/98-appendix-indices.md" ] && add_file "$INPUT_DIR/98-appendix-indices.md"
[ -f "$INPUT_DIR/97-appendix-greek-vocabulary.md" ] && add_file "$INPUT_DIR/97-appendix-greek-vocabulary.md"
[ -f "$INPUT_DIR/96-appendix-reading-plan.md" ] && add_file "$INPUT_DIR/96-appendix-reading-plan.md"
[ -f "$INPUT_DIR/99-appendix-references.md" ] && add_file "$INPUT_DIR/99-appendix-references.md"

# 跋 — afterword. Last content file: no trailing \newpage (the template
# backmatter opens its own page; a trailing break here yields a header-only
# blank page whenever the afterword happens to fill its final page exactly).
echo "  Adding: 999-afterword.md"
tail -n +8 "$INPUT_DIR/999-afterword.md" >> "$COMBINED_MD"
((chapter_count++))

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count sections)"
echo ""
echo "🔨 Generating PDF with 2-thessalonians.latex template..."

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
