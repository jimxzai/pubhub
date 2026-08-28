#!/bin/bash

# 1 Peter PDF Builder - CONSOLIDATED 2026 EDITION (rebuilt in the Gospel-of-John format)
# = preface + orientation (overview / position / spine / systematic reception)
#   + 5 chapters in three volumes with divider pages + 卷末 + appendices + afterword
# Sources from books/bible/1-peter/ (老弟兄 methodology + MacArthur + Morgan, CUV scripture)
# Uses templates/pdf/1-peter.latex (Slate Stone / Refiner's Ember theme)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/1-peter"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/1-peter-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/1-peter-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/1-peter.latex"

echo "=========================================="
echo "📖 1 Peter PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "彼得前書研讀"
subtitle: "1 Peter Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年8月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **老弟兄查經方法論** — 週四查經班一貫的查經框架之應用

  • **John MacArthur** — 逐節解經 (gty.org)

  • **G. Campbell Morgan** — 解經王子

  **信心經過試驗，比精金更顯寶貴**

  「他曾照自己的大憐憫，藉耶穌基督從死裡復活，重生了我們，使我們有活潑的盼望。」（彼前 1:3）

  **經文版權聲明 (Scripture Copyright Notices)**

  本版為教會內部贈閱版（非賣品）；公開發行時另行申請 ISBN。

  中文經文引自《聖經》和合本（1919），屬公有領域；
  逐章核對來源見附錄二〈參考資料〉之逐章說明。

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
    printf '# %s\n\n> %s\n' "$1" "$2" >> "$COMBINED_MD"
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

# 前言 — preface (grace at CCIC, vision, honesty note, purpose)
add_file "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位 — orientation: map, coordinates, spine, method
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這三章：地圖、座標、骨幹。"

add_file "$INPUT_DIR/00-overview.md"
add_file "$INPUT_DIR/00a-1-peter-position.md"
add_file "$INPUT_DIR/00c-living-hope-spine.md"

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
# 正文 · 三卷
# ============================================================
add_volume "卷一 · 蒙揀選的身份 (A Chosen People) · 1-2 章" \
    "從重生得著活潑的盼望，到蒙召作君尊的祭司、聖潔的國度——身份先於行為。" \
    "**身份**——你們是被揀選的族類" \
    "2:9「惟有你們是被揀選的族類，是有君尊的祭司，是聖潔的國度」" \
    "我是誰，在基督裡？"
for i in 01 02; do add_chapter "$i"; done

add_volume "卷二 · 客旅在世的品行 (Sojourners in the World) · 3-4 章" \
    "順服掌權者、順服的妻子、體貼的丈夫、彼此相愛，直到為義受苦——苦難不是計劃外的意外。" \
    "**受苦**——有分於基督的苦難" \
    "4:13「你們倒要歡喜；因為你們是與基督一同受苦」" \
    "苦難臨到，我怎樣站立？"
for i in 03 04; do add_chapter "$i"; done

add_volume "卷三 · 牧養與儆醒 (Shepherding and Vigilance) · 5 章" \
    "長老牧養群羊，眾人謙卑順服，抵擋那吼叫的獅子——直到那賜諸般恩典的神親自成全。" \
    "**得榮**——賜諸般恩典的神必要親自成全你們" \
    "5:10「那賜諸般恩典的神……必要親自成全你們，堅固你們，賜力量給你們」" \
    "教會怎樣一同儆醒，直到主來？"
add_chapter "05"

# ============================================================
# 卷末 · 望向那一頭 — the road on to 2 Peter and to Revelation
# ============================================================
add_volume "卷末 · 望向那一頭 (Toward the Other End)" \
    "彼得前書結在儆醒等候裡——牠指著還沒寫的彼得後書，也指著新天新地。
>
> 你們暫受苦難之後，那賜諸般恩典的神……必要親自成全你們。（彼前 5:10）"
add_file "$INPUT_DIR/99-to-2-peter.md"

# ============================================================
# 附錄 — indices & references
# ============================================================
add_volume "附錄 (Appendices)" \
    "經文與主題索引；希臘文詞彙表；讀經計劃；資料來源與版本之逐章誠實說明。"
add_file "$INPUT_DIR/98-appendix-indices.md"
add_file "$INPUT_DIR/97-appendix-glossary.md"
add_file "$INPUT_DIR/96-appendix-reading-plan.md"
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
echo "🔨 Generating PDF with 1-peter.latex template..."

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
