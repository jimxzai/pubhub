#!/bin/bash

# Galatians PDF Builder — CONSOLIDATED 2026 EDITION (Gospel-of-John format)
# = preface + orientation (overview / position / spine / systematic reception)
#   + 8 chapters in three volumes (申辯·教義·生活) with divider pages
#   + 卷末 + appendices + afterword
# Sources from books/bible/galatian/ (老弟兄 methodology + MacArthur + Morgan
#   + Luther + Calvin, CUV scripture)
# Uses templates/pdf/galatian.latex (Burgundy/Gold "broken chains" theme)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/galatian"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/galatian-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/galatian-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/galatian.latex"

echo "=========================================="
echo "📖 Galatians PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "加拉太書研讀"
subtitle: "因信得自由 — Galatians Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年9月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **主要參考資料整合：**

  • **老弟兄查經方法論** — 週四查經班一貫的查經框架之應用

  • **John MacArthur** — Galatians 逐節解經講道系列 (gty.org)

  • **G. Campbell Morgan** — *Living Messages of the Books of the Bible*

  • **Martin Luther** — *A Commentary on St. Paul's Epistle to the Galatians*

  • **John Calvin** — *Commentary on Galatians and Ephesians*

  **只有一個福音——人稱義不是因行律法，乃是因信耶穌基督**

  「基督釋放了我們，叫我們得以自由。所以要站立得穩，不要再被奴僕的軛挾制。」（加 5:1）

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
# optionally, its place in the revelation order ($3 $4 $5).
add_volume() {
    printf '# %s\n\n> %s\n' "$1" "$2" >> "$COMBINED_MD"
    if [ -n "$3" ]; then
        # The separator row must be at least pandoc's --columns threshold (72),
        # or pandoc emits bare `l` columns that cannot wrap and the 鑰節 cell
        # overflows the text block. See scripts/widen-table-separators.py.
        printf '\n| | |\n|----------------------|-----------------------------------------------------------------|\n| **啟示的次序·第 N 步** | %s |\n| **鑰節** | %s |\n| **貫穿的問題** | %s |\n' \
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

# 前言 — preface
add_file "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位 — orientation: map, coordinates, spine, method
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這三章：地圖、座標、骨幹。"

add_file "$INPUT_DIR/00-overview.md"
add_file "$INPUT_DIR/00a-galatians-position.md"
add_file "$INPUT_DIR/00c-gospel-spine.md"

# 老弟兄 systematic reception — demote headings one level so the whole
# study reads as a single top-level chapter.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception)\n\n' >> "$COMBINED_MD"
    tail -n +2 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 三卷
# ============================================================
add_volume "卷一 · 為福音申辯 (Defense of the Gospel) · 1-2 章" \
    "啟示的次序·第一步——保羅不是先講道理，是先站穩自己的使徒職分與所傳福音的來源：福音不是人的意思，是耶穌基督的啟示；這福音的內容，連彼得在安提阿都必須被當面指正。" \
    "**根基**——這福音不是我從人領受的，也不是人教導我的" \
    "1:11-12「我素來所傳的福音，不是照著人的意思。因為這不是我從人領受的，也不是人教導我的，乃是我藉著耶穌基督的啟示得來的」" \
    "這福音，憑甚麼可信？"
for i in 01 02; do add_chapter "$i"; done

add_volume "卷二 · 因信稱義的教義 (The Doctrine of Justification by Faith) · 3-4 章" \
    "啟示的次序·第二步——全書的論證核心：用亞伯拉罕、用律法與應許的時間先後、用一個寓意，證明因信稱義從創世記15章起就是神一貫的救法，律法只是暫時的師傅。" \
    "**應許先於律法**——律法是為過犯添上的，直等那蒙應許的子孫來到" \
    "3:29「你們既屬乎基督，就是亞伯拉罕的後裔，是照著應許承受產業的了」" \
    "神的救法，次序是甚麼？"
for i in 03 04 05 06; do add_chapter "$i"; done

add_volume "卷三 · 聖靈中的自由生活 (Life of Freedom in the Spirit) · 5-6 章" \
    "啟示的次序·第三步——教義若不落地，就只是知識：這兩章講因信稱義的人如何靠聖靈而行、結出聖靈的果子、彼此擔當、只誇基督的十字架。" \
    "**成果**——聖靈所結的果子" \
    "5:22-23「聖靈所結的果子，就是仁愛、喜樂、和平、忍耐、恩慈、良善、信實、溫柔、節制」" \
    "得了自由的人，怎樣活？"
for i in 07 08; do add_chapter "$i"; done

# ============================================================
# 卷末 — closing: the letter's own last word
# ============================================================
add_volume "卷末 · 我身上帶著耶穌的印記 (The Marks of Jesus)" \
    "加拉太書不以問安收尾，以一道傷疤收尾——保羅身上因這福音留下的印記，是全書最後的論證。
>
> 從今以後，人都不要攪擾我，因為我身上帶著耶穌的印記。（加 6:17）"
add_file "$INPUT_DIR/99-closing.md"

# ============================================================
# 附錄 — indices & references
# ============================================================
add_volume "附錄 (Appendices)" \
    "經文與主題索引；資料來源與版本之逐章誠實說明。"
if [ -f "$SCRIPT_DIR/gen-galatian-scripture-index.py" ]; then
    python3 "$SCRIPT_DIR/gen-galatian-scripture-index.py" --write
fi
add_file "$INPUT_DIR/98-appendix-indices.md"
add_file "$INPUT_DIR/99-appendix-references.md"

# 跋 — afterword. Last content file: no trailing \newpage (the template
# backmatter opens its own page; a trailing break here yields a
# header-only blank page whenever the afterword happens to fill its
# final page exactly).
echo "  Adding: 999-afterword.md"
tail -n +8 "$INPUT_DIR/999-afterword.md" >> "$COMBINED_MD"
((chapter_count++))

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count sections)"
echo ""

# Mark every Scripture reference for the page-referenced index. Must run
# on the COMBINED markdown, after all chapters are concatenated and before
# pandoc sees it. See scripts/lib/scripture-index.py for the grammar.
# "48 加拉太書" tells the library that a BARE "N:N" reference (no book name
# prefix — very common in this book's own prose, e.g. "(3:16)") means
# Galatians itself, not the library's original default of Leviticus.
python3 "$SCRIPT_DIR/lib/scripture-index.py" "$COMBINED_MD" 48 加拉太書

echo "🔨 Generating PDF with galatian.latex template..."

# --verbose is load-bearing, not chatter: without it pandoc swallows the whole
# xelatex log and every grep-the-log check below (and in driver.sh) passes
# vacuously. See scripts/lib/latex-check.sh for the full explanation.
source "$SCRIPT_DIR/lib/latex-check.sh"
LATEX_LOG="${OUTPUT_PDF%.pdf}-build.log"
COMBINED_TEX="${OUTPUT_PDF%.pdf}.tex"

# Two-stage build, because this book has a page-referenced Scripture index.
#
# pandoc --pdf-engine runs xelatex inside a temporary directory it deletes
# afterwards, so the .idx file never survives long enough for makeindex to
# process it and the index silently comes out empty — the PDF builds clean
# and simply has no index. So: pandoc emits .tex here, and we drive
# xelatex/makeindex ourselves in $OUTPUT_DIR where the aux files persist.
pandoc "$COMBINED_MD" \
  -o "$COMBINED_TEX" \
  --standalone \
  --template="$TEMPLATE" \
  --from=markdown-superscript-subscript \
  --to=latex-smart \
  --toc \
  --toc-depth=1 \
  --top-level-division=chapter \
  -V tocdepth=0 2> "$LATEX_LOG"
PANDOC_EXIT=$?
if [ "$PANDOC_EXIT" -ne 0 ]; then
    echo "❌ pandoc failed to produce LaTeX — see $LATEX_LOG"
    tail -20 "$LATEX_LOG"
    exit 1
fi

# xelatex ×2 → makeindex → xelatex ×2.
# The first two passes settle the TOC and write the .idx; makeindex turns
# that into the .ind; the last two place the index and settle page numbers
# that the index itself shifted.
( cd "$OUTPUT_DIR" && {
    xelatex -interaction=nonstopmode -halt-on-error "$(basename "$COMBINED_TEX")"
    xelatex -interaction=nonstopmode -halt-on-error "$(basename "$COMBINED_TEX")"
    # imakeidx names the files after the index ("scripture"), not the job.
    # TeX Live allows makeindex under restricted shell-escape, so imakeidx
    # usually runs it itself; this call is the fallback for when it cannot.
    [ -f scripture.idx ] && makeindex -q scripture.idx -o scripture.ind
    xelatex -interaction=nonstopmode -halt-on-error "$(basename "$COMBINED_TEX")"
    xelatex -interaction=nonstopmode -halt-on-error "$(basename "$COMBINED_TEX")"
  } ) >> "$LATEX_LOG" 2>&1
XELATEX_EXIT=$?

latex_build_report "$XELATEX_EXIT" "$LATEX_LOG" "$OUTPUT_PDF" || exit 1
