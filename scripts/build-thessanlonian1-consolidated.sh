#!/bin/bash

# First Thessalonians PDF Builder - CONSOLIDATED 2026 EDITION (Gospel-of-John / James format)
# = preface + orientation (overview / position / revelation-order / systematic reception)
#   + 11 chapters in five volumes with divider pages + 卷末 + appendices + afterword
# Sources from books/bible/thessanlonian1/ (老弟兄 methodology + Chrysostom + Calvin
# + Morgan + MacArthur, CUV + NASB 1995 scripture)
# Uses templates/pdf/thessanlonian1.latex (night-to-dawn indigo / gold theme)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/thessanlonian1"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/thessanlonian1-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/thessanlonian1-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/thessanlonian1.latex"

echo "=========================================="
echo "📖 1 Thessalonians PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

# The cross-book Scripture index is generated from the chapters, never kept
# by hand (scripts/gen-thessanlonian1-scripture-index.py).
python3 "$SCRIPT_DIR/gen-thessanlonian1-scripture-index.py" --write || exit 1

cat > "$COMBINED_MD" << 'HEADER'
---
title: "帖撒羅尼迦前書研讀"
subtitle: "1 Thessalonians Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年10月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **資源整合：**

  • **老弟兄查經方法論** — 週四查經班一貫的查經框架之應用（原始筆記無本卷逐節記錄，見前言）

  • **屈梭多模 John Chrysostom** — *Homilies on First Thessalonians*（NPNF¹ 13，公有領域）

  • **John Calvin** — *Commentary on 1 Thessalonians*（CCEL，公有領域）

  • **G. Campbell Morgan** — *An Exposition of the Whole Bible*；*Living Messages of the Books of the Bible*

  • **John MacArthur** — 帖撒羅尼迦前書系列講道 52-1~52-36 (gty.org)

  **那召你們的本是信實的，他必成就這事**

  「你們是怎樣離棄偶像，歸向神，要服事那又真又活的神，等候他兒子從天降臨。」（帖前1:9-10）

  **經文版權聲明 (Scripture Copyright Notices)**

  本版為教會內部贈閱版（非賣品）；公開發行時另行申請 ISBN。

  中文經文引自《聖經》和合本，屬公有領域；逐章核對來源見附錄〈引用出處總表〉。

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
# optionally, its place in the salvation/discipleship order ($3 $4 $5).
add_volume() {
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
# 卷首 · 定位 — orientation: map, coordinates, spine, method
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這幾章：地圖、座標、骨幹——啟示的次序與神的計劃。"

add_file "$INPUT_DIR/00-overview.md"
add_file "$INPUT_DIR/00a-1thess-position.md"
add_file "$INPUT_DIR/00c-revelation-order.md"

# 老弟兄 systematic reception — demote headings one level so the whole
# study reads as a single top-level chapter.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
    # drop the 7-line YAML + blank line 8 AND the file's own H1 (line 9),
    # then demote every remaining heading by one level
    tail -n +10 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 五卷 — 啟示的次序：神的五個動詞
# ============================================================
add_volume "卷一 · 福音臨到 (The Gospel Came)" \
    "1:1-2:12 · 啟示的次序·第一步：神揀選——福音不獨在乎言語，也在乎權能和聖靈；人才離棄偶像，歸向神。" \
    "**神揀選**——被神所愛的弟兄啊，我知道你們是蒙揀選的" \
    "1:4-5「我知道你們是蒙揀選的；因為我們的福音傳到你們那裏，不獨在乎言語，也在乎權能和聖靈」" \
    "我的信心，是建立在神揀選我的作為上，還是建立在我對神的感覺上？"
for i in 01 02 03; do add_chapter "$i"; done

add_volume "卷二 · 道在患難中運行 (The Word at Work in Affliction)" \
    "2:13-3:13 · 啟示的次序·第二步：神的道運行在信的人心中，神在患難裏堅固人心——直到主耶穌同他眾聖徒來的時候。" \
    "**神堅固**——這道實在是神的，並且運行在你們信主的人心中" \
    "3:13「好使你們當我們主耶穌同他眾聖徒來的時候，在我們父神面前，心裏堅固，成為聖潔，無可責備」" \
    "患難臨到的時候，我靠甚麼站立得穩？"
for i in 04 05; do add_chapter "$i"; done

add_volume "卷三 · 蒙召成聖 (Called to Holiness)" \
    "4:1-12 · 啟示的次序·第三步：神的旨意就是要你們成為聖潔——神召我們成聖，又賜聖靈給我們。" \
    "**神的旨意**——神召我們，本不是要我們沾染污穢，乃是要我們成為聖潔" \
    "4:3「神的旨意就是要你們成為聖潔」" \
    "我的身體、我的弟兄、我的工作，是否都在神的旨意之下？"
for i in 06 07; do add_chapter "$i"; done

add_volume "卷四 · 盼望的忍耐 (The Steadfastness of Hope)" \
    "4:13-5:11 · 啟示的次序·第四步：神必將睡了的人與耶穌一同帶來，神預定我們藉主耶穌基督得救——補上教會所缺的盼望。" \
    "**神必帶來**——主必親自從天降臨……這樣，我們就要和主永遠同在" \
    "5:9「因為神不是預定我們受刑，乃是預定我們藉著我們主耶穌基督得救」" \
    "面對死亡與末日，我是像那些沒有指望的人，還是光明之子？"
for i in 08 09; do add_chapter "$i"; done

add_volume "卷五 · 那召你們的 (Faithful Is He Who Calls)" \
    "5:12-28 · 啟示的次序·第五步，也是全書的終點：賜平安的神親自使你們全然成聖；那召你們的本是信實的，他必成就這事。" \
    "**神親自成就**——願賜平安的神親自使你們全然成聖" \
    "5:24「那召你們的本是信實的，他必成就這事」" \
    "我把自己的成聖，交在誰的手裏？"
for i in 10 11; do add_chapter "$i"; done

# ============================================================
# 卷末 · 等候他兒子 — the book's own closing return
# ============================================================
add_volume "卷末 · 等候他兒子 (Waiting for His Son)" \
    "帖撒羅尼迦前書結在一句祝福裏——不是要求，是恩典。
>
> 願我主耶穌基督的恩常與你們同在！（帖前5:28）"

# ============================================================
# 附錄 — indices & references
# ============================================================
add_volume "附錄 (Appendices)" \
    "經文索引與原文詞彙；資料來源與版本之逐章誠實說明。"
add_file "$INPUT_DIR/97-appendix-greek-vocabulary.md"
add_file "$INPUT_DIR/98-appendix-indices.md"
add_file "$INPUT_DIR/99-appendix-references.md"

# 跋 — afterword. Last content file: no trailing \newpage (the template's
# backmatter opens its own page).
echo "  Adding: 999-afterword.md"
tail -n +8 "$INPUT_DIR/999-afterword.md" >> "$COMBINED_MD"
((chapter_count++))

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count sections)"
echo ""
echo "🔨 Generating PDF with thessanlonian1.latex template..."

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
