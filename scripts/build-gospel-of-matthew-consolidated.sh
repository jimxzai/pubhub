#!/bin/bash

# Gospel of Matthew PDF Builder - CONSOLIDATED 2026 EDITION (August revision)
# Structure mirrors build-gospel-consolidated.sh (Gospel of John, Aug 2026):
#   preface + 卷首·定位 (overview, two orientation essays, systematic reception)
#   + five volumes with divider pages + 卷末 + references appendix + afterword
# Sources from books/bible/matthew/book/ (the current, actively maintained project)
# Uses templates/pdf/gospel-of-matthew.latex (Royal Purple King theme)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/matthew/book"
PROLOGUE_FILE="$INPUT_DIR/prologue-canonical-context.md"
ORDER_FILE="$INPUT_DIR/00a-kingdom-order.md"
KEY_FILE="$INPUT_DIR/00b-emmanuel-spine.md"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
INDEX_FILE="$INPUT_DIR/99b-appendix-indexes.md"
GLOSSARY_FILE="$INPUT_DIR/99c-appendix-glossary.md"
EXTRAS_FILE="$INPUT_DIR/99d-appendix-extras.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/gospel-of-matthew-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/gospel-of-matthew-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/gospel-of-matthew.latex"

echo "=========================================="
echo "📖 Gospel of Matthew PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "馬太福音研讀"
subtitle: "天國之王 — Gospel of Matthew Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年8月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **CCIC 週四查經班** — 第一手屬靈領受

  • **John MacArthur** — 逐節解經 (gty.org)

  • **G. Campbell Morgan** — 解經王子，*The Gospel According to Matthew* (1929)

  **經文版權聲明 (Scripture Copyright Notices)**

  本版為教會內部贈閱版（非賣品）；公開發行時另行申請 ISBN。

  中文經文引自《聖經》和合本（1919），屬公有領域。

  Scripture quotations taken from the New American Standard Bible® (NASB),
  Copyright © 1960, 1971, 1977, 1995 by The Lockman Foundation.
  Used by permission. All rights reserved. lockman.org

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
# optionally, its place in the salvation plan / the fulfillment marker /
# the Revelation harvest ($3 $4 $5; see 00a-kingdom-order.md 總表).
add_volume() {
    printf '# %s {-}\n\n> %s\n' "$1" "$2" >> "$COMBINED_MD"
    if [ -n "$3" ]; then
        printf '\n| | |\n|---|---|\n| **救恩計劃** | %s |\n| **應驗的記號** | %s |\n| **啟示錄的收成** | %s |\n' \
            "$3" "$4" "$5" >> "$COMBINED_MD"
    fi
    printf '\n\\newpage\n\n' >> "$COMBINED_MD"
    echo "  --- $1"
}

# Append the first file matching a chapter-number prefix (e.g. 01-, 13-).
add_chapter() {
    local f
    for f in "$INPUT_DIR/$1-"*.md; do
        [ -f "$f" ] && { add_file "$f"; return 0; }
    done
    echo "❌ Missing chapter file for prefix '$1-' in $INPUT_DIR — aborting build"
    exit 1
}

# 前言 — preface (the Thursday table, the vision, the anonymity)
add_file "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位 — orientation: map, coordinates, spine, method
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這四章：地圖、座標、骨幹、方法。"

add_file "$INPUT_DIR/00-overview.md"
add_file "$PROLOGUE_FILE"
add_file "$ORDER_FILE"
add_file "$KEY_FILE"

# Elder reception — demote headings one level so the whole
# study reads as a single top-level chapter.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception) {-}\n\n' >> "$COMBINED_MD"
    # drop the file's own H1 title line, demote all headings by one level
    # (single substitution per line: prepends one # to the leading run, no cascade)
    tail -n +2 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 五卷
# ============================================================
add_volume "卷一 · 君王的身分 (The King's Identity) · 1-4" \
    "家譜、降生、受洗、受試探——四章立定一件事：這一位是誰。" \
    "**賜下**——以馬內利，神與我們同在" \
    "1:22-23 童女懷孕生子（賽 7:14）" \
    "5:5 猶大支派的獅子，大衛的根"
for i in 01 02 03 04; do add_chapter "$i"; done

add_volume "卷二 · 君王的宣告 (The King's Manifesto) · 5-7" \
    "登山寶訓——天國的憲章。不是進天國的門檻，是天國子民的畫像。" \
    "**陳明**——天國的義擺在人面前" \
    "5:17「我來不是要廢掉，乃是要成全」" \
    "22:14 那些洗淨自己衣服的有福了（八福的收成）"
for i in 05 06 07; do add_chapter "$i"; done

add_volume "卷三 · 君王的權能與奧祕 (Power and Mystery) · 8-13" \
    "十個神蹟印證所宣告的；天國的奧祕藏在比喻裡——聽的人被分開了。" \
    "**印證**——權能印證所宣告的" \
    "8:17 代替我們的軟弱（賽 53:4）；13:35 開口用比喻（詩 78:2）" \
    "10:7 神的奧祕就成全了"
for i in 08 09 10 11 12 13; do add_chapter "$i"; done

add_volume "卷四 · 君王的教導 (Training the Twelve) · 14-20" \
    "從餵飽五千人到磐石上的教會，從登山變像到十字架的路——門徒被重新造。" \
    "**預告內化**——磐石上的教會，十字架的路" \
    "17:5「這是我的愛子……你們要聽他」（申 18:15）" \
    "21:14 根基上有羔羊十二使徒的名字"
for i in 14 15 16 17 18 19 20; do add_chapter "$i"; done

add_volume "卷五 · 君王的受難與復活 (Passion and Resurrection) · 21-28" \
    "和散那到十字架，只有五天；墳墓到大使命，只有三天。" \
    "**成全與傳遞**——十字架成全，大使命傳遞" \
    "21:4-5 看哪，你的王來到（亞 9:9）" \
    "1:7 駕雲降臨，萬族哀哭（太 24:30 的收成）；11:15 世上的國成了我主和主基督的國"
for i in 21 22 23 24 25 26 27 28; do add_chapter "$i"; done

# ============================================================
# 卷末 · 望向那一頭 — the arc into Revelation
# ============================================================
add_volume "卷末 · 望向那一頭 (Toward the Other End)" \
    "馬太福音自己不收尾——它結在「直到世界的末了」，指著另一卷書。
>
> 天上地下所有的權柄都賜給我了。所以，你們要去，使萬民作我的門徒。（太 28:18-19）"
add_file "$INPUT_DIR/99-to-revelation.md"

# References appendix (7-line front matter stripped like every other file)
add_file "$INPUT_DIR/99-appendix-references.md"

# Reference-book back matter: Scripture/subject indexes, Greek glossary,
# and the extra appendices (four-gospels comparison, red-letter format
# note, reading plan) — parallel to the John book's appendix suite.
add_file "$INDEX_FILE"
add_file "$GLOSSARY_FILE"
add_file "$EXTRAS_FILE"

# 跋 — afterword (the ministry, the 66-volume prayer).
# Last content file: no trailing \newpage (the template backmatter opens
# its own page; a trailing break here yields a header-only blank page
# whenever the afterword happens to fill its final page exactly).
echo "  Adding: 999-afterword.md"
tail -n +8 "$INPUT_DIR/999-afterword.md" >> "$COMBINED_MD"
((chapter_count++))

# ============================================================
# Integrity gate: this project's source directory lives under a
# cloud-synced path (iCloud Drive), which has repeatedly been observed
# this session returning stale/incomplete reads under load — a chapter
# file can pass `[ -f "$f" ]` and even echo "Adding: ..." while its
# `tail | sed` content read silently comes back empty, producing a
# PDF that's missing an entire chapter with a *successful* exit code.
# Refuse to hand pandoc a corrupt combined file — count real chapter
# headings and abort loudly (instead of silently shipping a book
# short one chapter) if the count isn't exactly 28.
# ============================================================
found_chapters=$(grep -c '^# 第[^：]*章：' "$COMBINED_MD")
if [ "$found_chapters" -ne 28 ]; then
    echo ""
    echo "❌ Integrity check failed: found $found_chapters chapter headings in"
    echo "   $COMBINED_MD, expected 28. A source file was likely read"
    echo "   incompletely (cloud-sync filesystem lag) during this build —"
    echo "   re-run the build. Missing chapter(s):"
    for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28; do
        f=$(ls "$INPUT_DIR/$i-"*.md 2>/dev/null | head -1)
        [ -n "$f" ] && grep -qF "$(sed -n '9p' "$f")" "$COMBINED_MD" || echo "   - chapter $i ($(basename "${f:-unknown}"))"
    done
    exit 1
fi
echo "✅ Integrity check passed: all 28 chapters present in combined markdown."

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count files)"
echo ""
echo "🔨 Generating PDF with gospel-of-matthew.latex template..."

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
