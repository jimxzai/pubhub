#!/bin/bash

# James PDF Builder - CONSOLIDATED 2026 EDITION (built in the Gospel-of-John / 1-Peter format)
# = preface + orientation (overview / position / revelation-order / systematic reception)
#   + 5 chapters in three volumes with divider pages + 卷末 + appendices + afterword
# Sources from books/bible/james/ (老弟兄 methodology + Calvin + MacArthur, CUV scripture)
# Uses templates/pdf/james.latex (Forest Green / Scripture Gold theme)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/james"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/james-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/james-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/james.latex"

echo "=========================================="
echo "📖 James PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "雅各書研讀"
subtitle: "Epistle of James Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年9月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **四大核心資源整合：**

  • **老弟兄查經方法論** — 週四查經班一貫的查經框架之應用

  • **John Calvin** — 大公書信註釋（公有領域）

  • **G. Campbell Morgan** — 《聖經各卷的生命信息》（公有領域）

  • **John MacArthur** — 逐節解經 (gty.org)

  **你們要行道，不要單單聽道，自己欺哄自己**

  「他按自己的旨意，用真道生了我們，叫我們在他所造的萬物中好像初熟的果子。」（雅1:18）

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
    "讀正文之前先讀這三章：地圖、座標、骨幹——啟示的次序與神的計劃。"

add_file "$INPUT_DIR/00-overview.md"
add_file "$INPUT_DIR/00a-james-position.md"
add_file "$INPUT_DIR/00c-revelation-order.md"

# 老弟兄 systematic reception — demote headings one level so the whole
# study reads as a single top-level chapter.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception)\n\n' >> "$COMBINED_MD"
    # drop the file's 7-line YAML frontmatter (lines 1-7 + blank line 8, same
    # as add_file()'s `tail -n +8`) AND its own H1 title line (line 9), then
    # demote all remaining headings by one level (single substitution per
    # line: prepends one # to the leading run, no cascade)
    tail -n +10 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 三卷 — 啟示的次序：從「聽道」到「行道」，五步展開
# ============================================================
add_volume "卷一 · 活出所信的道 (Living the Word You Received)" \
    "1-2章 · 啟示的次序·第一、二步：試煉熬煉出真信心，真信心必有真行為——從「聽道」到「行道」。" \
    "**聽道到行道**——你們要行道，不要單單聽道" \
    "1:22「你們要行道，不要單單聽道，自己欺哄自己」" \
    "我所信的，活出來了嗎？"
for i in 01 02; do add_chapter "$i"; done

add_volume "卷二 · 智慧與衝突 (Wisdom and Conflict)" \
    "3-4章 · 啟示的次序·第三、四步：真智慧馴服舌頭，真謙卑順服神——是誰在心中掌權。" \
    "**順服**——你們要順服神，抵擋魔鬼" \
    "4:7「你們要順服神，抵擋魔鬼，魔鬼就必離開你們逃跑了」" \
    "是誰在我心中掌權——屬地的智慧，還是從上頭來的智慧？"
for i in 03 04; do add_chapter "$i"; done

add_volume "卷三 · 忍耐等候與代求 (Patience and the Praying Community)" \
    "5章 · 啟示的次序·第五步，也是全書的終點：真忍耐盼望主來，彼此代求，把失迷的人找回來。" \
    "**忍耐**——你們也當忍耐，堅固你們的心" \
    "5:8「你們也當忍耐，堅固你們的心，因為主來的日子近了」" \
    "我在等候主來的日子裏，怎樣忍耐、怎樣代求？"
add_chapter "05"

add_volume "卷四 · 專題深論 (Topical Deep Dives)" \
    "回頭把啟示的次序·五步共同的底色描深——六篇跨書卷對照：箴言、以利亞與禱告、彼得前書、利未記19章、阿摩司書、詩篇第一篇。" \
    "**回頭深挖**——同一條啟示的次序，換一個角度再看一次" \
    "3:17「從上頭來的智慧，先是清潔，後是和平」" \
    "我讀雅各書時，是否也把它放回整本聖經的智慧傳統與先知傳統裏讀？"
for i in 06 07 08 09 10 11 12; do add_chapter "$i"; done

# ============================================================
# 卷末 · 你信的，活出來了嗎 — the book's own closing return
# ============================================================
add_volume "卷末 · 你信的，活出來了嗎 (Toward a Living Faith)" \
    "雅各書結在最貼地的牧養提醒裏——不是莊重的祝福語，是一句彼此挽回的呼籲。
>
> 叫一個罪人從迷路上轉回，便是救一個靈魂不死，並且遮蓋許多的罪。（雅5:20）"

# ============================================================
# 附錄 — indices & references
# ============================================================
add_volume "附錄 (Appendices)" \
    "經文與主題索引；讀經計劃；資料來源與版本之逐章誠實說明。"
[ -f "$INPUT_DIR/98-appendix-indices.md" ] && add_file "$INPUT_DIR/98-appendix-indices.md"
[ -f "$INPUT_DIR/97-appendix-greek-vocabulary.md" ] && add_file "$INPUT_DIR/97-appendix-greek-vocabulary.md"
[ -f "$INPUT_DIR/96-appendix-reading-plan.md" ] && add_file "$INPUT_DIR/96-appendix-reading-plan.md"
[ -f "$INPUT_DIR/99-appendix-references.md" ] && add_file "$INPUT_DIR/99-appendix-references.md"

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
echo "🔨 Generating PDF with james.latex template..."

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
