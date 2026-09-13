#!/bin/bash

# Leviticus PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine) + 全書領受總綱 + 六卷 27 章 + 跋
# Uses templates/pdf/leviticus.latex (Scarlet/Blue/Gold theme, matching the
# Gospel of John / Acts of the Apostles / Isaiah / Job series standard:
# cover art, frontispiece)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/leviticus"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/leviticus-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/leviticus-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/leviticus.latex"

echo "=========================================="
echo "🩸 Leviticus Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "利未記研讀"
subtitle: "Leviticus Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年9月"
publisher: "三書精讀出版系統"
copyright: |
  **利未記研讀**　Leviticus Deep Study

  三書精讀出版系統　初版 · 2026年9月

  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **全書結構：啟示的六個次序**

  卷一　獻祭的條例（1-7章）——你可以這樣來

  卷二　祭司的設立（8-10章）——誰替你來

  卷三　潔淨的條例（11-15章）——甚麼攔阻你來

  卷四　贖罪日（16章）——一天解決全部

  卷五　聖潔典章（17-26章）——蒙贖之後怎麼活

  卷六　許願與估值（27章）——一切都歸祂

  **歷代注疏來源**（本卷無老弟兄第一手教導筆記可用，詳見前言與卷末附錄）

  Andrew Bonar, *A Commentary on Leviticus* (1846)

  Matthew Henry, *Commentary on the Whole Bible*, Leviticus

  John MacArthur, gty.org（機會性引用，僅限確有相關講道之七章）

  **經文版本與版權 (Scripture Versions and Copyright)**

  中文經文引自《聖經》和合本（1919），屬公有領域。

  Scripture quotations marked (NASB) are from the NEW AMERICAN STANDARD
  BIBLE®, Copyright © 1960, 1962, 1963, 1968, 1971, 1972, 1973, 1975, 1977,
  1995 by The Lockman Foundation. Used by permission. www.Lockman.org.
  All rights reserved.

  本版為教會內部贈閱版（非賣品）；公開發行時另行申請 ISBN。

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
    tail -n +8 "$f" | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Volume divider: a part-title page carrying the volume's theme.
# Front/back matter and volume dividers: same as add_file but marks the H1
# {.unnumbered}. Without this LaTeX numbers EVERY chapter sequentially, so the
# preface, orientation chapters and the volume divider pages consume numbers
# 1-N and the book's own 第一章 comes out as LaTeX chapter N+1 — the contents
# page then reads two conflicting numbers on one line. Marking these
# unnumbered lets the 27 study units number 1-27, matching 第一章-第二十七章.
# Same approach as build-job-consolidated.sh / build-isaiah-consolidated.sh.
add_front() {
    local f="$1"
    [ -f "$f" ] || return 0
    echo "  Adding (unnumbered): $(basename "$f")"
    tail -n +8 "$f" | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}/g' \
      | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}" ; done=1 } } {print}' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

add_volume() {
    printf '# %s {.unnumbered}\n\n> %s\n' "$1" "$2" >> "$COMBINED_MD"
    if [ -n "$3" ]; then
        printf '\n| %s | %s |\n|---|---|\n' "$3" "$4" >> "$COMBINED_MD"
    fi
    printf '\n\\newpage\n\n' >> "$COMBINED_MD"
    echo "  --- $1"
}

# Append the file matching an exact chapter filename (no combined-file globbing —
# every chapter is its own file).
add_chapter() {
    add_file "$INPUT_DIR/$1"
}

# 前言 — preface
add_front "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位 — orientation: overview, position, spine
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這幾章：總覽、位置、骨幹。"

add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-leviticus-position.md"
add_front "$INPUT_DIR/00b-holiness-spine.md"

# Systematic reception — demote headings one level so it reads as one chapter.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
    tail -n +2 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 六卷 · 27 章
# ============================================================
add_volume "卷一 · 獻祭的條例 (Laws of Offering) · 1-7章" \
    "**啟示的次序·第一步：神先給路。**榮光既已充滿會幕、連摩西都進不去（出40:35），神開口的第一句不是要求，是「你可以這樣來」——五種祭，五種來到祂面前的方式。"
for f in 01-burnt-offering.md 02-grain-offering.md 03-peace-offering.md \
         04-sin-offering.md 05-guilt-and-restitution.md \
         06-priestly-portion-burnt-grain-sin.md 07-priestly-portion-guilt-peace-waving.md; do
    add_chapter "$f"
done

add_volume "卷二 · 祭司的設立 (Institution of the Priesthood) · 8-10章" \
    "**啟示的次序·第二步：神設立中保。**有了路，才需要領路的人。而按立才剛完成，拿答亞比戶就因擅獻凡火被焚——領路的人自己也不可靠。"
for f in 08-ordination-of-aaron.md 09-glory-appears.md 10-strange-fire.md; do
    add_chapter "$f"
done

add_volume "卷三 · 潔淨的條例 (Laws of Purity) · 11-15章" \
    "**啟示的次序·第三步：神揭開問題的深度。**不潔不只在祭壇上——在餐桌、產房、皮膚、身體裏。走完這五章，人才知道自己無處可躲。"
for f in 11-clean-and-unclean-food.md 12-purification-after-childbirth.md \
         13-diagnosing-the-plague.md 14-cleansing-the-leper.md 15-bodily-discharges.md; do
    add_chapter "$f"
done

add_volume "卷四 · 贖罪日 (The Day of Atonement) · 16章" \
    "**啟示的次序·第四步：一天解決全部。**前十五章把問題挖到見底，這一章才有份量。全書的樞紐，也是希伯來書9-10章論證的根基。"
add_chapter "16-day-of-atonement.md"

add_volume "卷五 · 聖潔典章 (The Holiness Code) · 17-26章" \
    "**啟示的次序·第五步：蒙贖之後怎麼活。**贖罪已成，才談得上「你們要聖潔」——聖潔是贖罪的果子，不是贖罪的價錢。從祭壇一路推到鄰舍、日曆與田地。"
for f in 17-sanctity-of-blood.md 18-sexual-holiness.md 19-be-holy-as-i-am-holy.md \
         20-penalties-for-holiness.md 21-holiness-of-priests.md 22-holiness-of-offerings.md \
         23-feasts-of-the-lord.md 24-lamp-bread-blasphemy.md 25-sabbath-year-and-jubilee.md \
         26-blessings-and-curses.md; do
    add_chapter "$f"
done

add_volume "卷六 · 許願與估值 (Vows and Valuations) · 27章" \
    "**啟示的次序·第六步（末了）：一切都歸祂，也都有價。**全書收在估價與贖回——把主權釘回神身上：凡分別為聖的，都當按價贖回。"
add_chapter "27-vows-and-valuations.md"

# ============================================================
# 卷末 · 附錄 — the reference apparatus.
# A study volume that quotes 193 passages from named sources has to let the
# reader look them up: the Scripture index (which doubles as a map of the
# revelation order) and the sources ledger with its honest record of how each
# citation was verified. These existed as repo files but were not printed,
# so the printed book gave a reader no way to check any citation.
# ============================================================
add_volume "卷末 · 附錄 (Appendices)" \
    "經文索引兼作啟示次序的地圖；引用出處總表記錄每一條引文的來源與核校方式。"

add_front "$INPUT_DIR/98-appendix-indices.md"
add_front "$INPUT_DIR/99-appendix-references.md"

# ============================================================
# 跋 — afterword. Last content file: no trailing \newpage.
# ============================================================
if [ -f "$INPUT_DIR/999-afterword.md" ]; then
    echo "  Adding (unnumbered): 999-afterword.md"
    tail -n +8 "$INPUT_DIR/999-afterword.md" \
      | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}" ; done=1 } } {print}' >> "$COMBINED_MD"
    ((chapter_count++))
fi

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters)"
echo ""
# Mark every Scripture reference for the page-referenced index. Must run
# on the COMBINED markdown, after all chapters are concatenated and before
# pandoc sees it. See scripts/lib/scripture-index.py for the grammar.
python3 "$SCRIPT_DIR/lib/scripture-index.py" "$COMBINED_MD"

echo "🔨 Generating PDF with leviticus.latex template..."

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
