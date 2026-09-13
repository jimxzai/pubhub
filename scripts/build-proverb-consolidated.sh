#!/bin/bash

# Proverbs PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/structure/spine) + 全書領受總綱 + 五卷 31 章 + 卷末 + 跋
# Uses templates/pdf/proverb.latex (Amber/Voice/Noon theme, matching the
# Gospel of John / Job / Acts of the Apostles series standard: cover art,
# frontispiece)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/proverb"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/proverb-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/proverb-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/proverb.latex"

echo "=========================================="
echo "🌅 Proverbs Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "箴言研讀"
subtitle: "Proverbs Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年9月"
publisher: "三書精讀出版系統"
copyright: |
  **箴言研讀** (A Study of the Book of Proverbs)

  三書精讀出版系統 · 晨光系列

  初版　2026 年 9 月

  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  本版為教會內部贈閱版（非賣品），未公開發行；公開發行時另行申請 ISBN。
  歡迎為個人研讀與教會查經複印使用，請保留完整版權頁。

  **經文版權聲明 (Scripture Copyright Notices)**

  中文經文引自《聖經》和合本（1919），屬公有領域。

  Scripture quotations marked (NASB) are from the NEW AMERICAN STANDARD
  BIBLE®, Copyright © 1960, 1962, 1963, 1968, 1971, 1972, 1973, 1975, 1977,
  1995 by The Lockman Foundation. Used by permission. www.Lockman.org.
  All rights reserved.

  **注疏引用 (Commentary Sources)**

  本書引用之歷代注疏均屬公有領域。逐條出處、版本與核校方式，
  見卷末《附錄：參考資料》。
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
# preface, orientation chapters and the five volume divider pages consume
# numbers 1-N and the book's own 第一章 comes out as a LaTeX chapter greater
# than 1 — the contents page then reads two conflicting numbers on one line.
# Marking these unnumbered lets the 31 study units number 1-31, matching
# 第一章-第三十一章. Same approach as build-job-consolidated.sh.
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
    # %b (not %s) for the description: several volume descriptions carry a
    # literal \n>\n> to open a second blockquote paragraph (the 啟示的次序
    # marker). printf only expands escapes inside the FORMAT string, so with
    # %s those arrive in the markdown as the two characters \ and n and
    # xelatex then dies on "Undefined control sequence \n".
    printf '# %s {.unnumbered}\n\n> %b\n' "$1" "$2" >> "$COMBINED_MD"
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

# The two index tables in 98-appendix-indices.md carry a note saying they are
# generated from the chapter files at build time. Regenerate first so that
# claim is true of the PDF being produced (see Job's build script for the
# incident this guards against: an index note asserting freshness it did not
# have).
echo "🔄 Regenerating indices from chapter sources..."
python3 "$SCRIPT_DIR/gen-proverb-scripture-index.py" --write || exit 1
python3 "$SCRIPT_DIR/gen-proverb-theme-index.py" --write || exit 1
echo ""

# 前言 — preface
add_front "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位 — orientation: overview, structure, spine
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這四章：全書地圖、智慧位格化是誰、全書的五卷結構，以及最要緊的一章——神在這卷書裏按甚麼次序，把敬畏祂這件事從抽象的呼喚，走成具體的日常生活。"

add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-wisdom-personified.md"
add_front "$INPUT_DIR/00b-book-structure.md"
add_front "$INPUT_DIR/00c-revelation-order.md"

# Systematic reception — demote headings one level so it reads as one chapter.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
    tail -n +2 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 五卷 · 31 章
# ============================================================
add_volume "卷一 · 智慧的呼喚 (Wisdom's Call) · 1-9章" \
    "父對子的九篇長勸勉，智慧親自位格化為一位在街市上呼喊的女子——她自稱在創造之先就已與神同在。根基先於規條：還沒有一句具體的生活教訓之前，全書先立下一句判詞。\n>\n> **啟示的次序·第一步**：「敬畏耶和華是知識的開端」（1:7）先於一切——這是關係，不是規條。神先給根基，後給規條。"
for f in 01-wisdom-begins-with-fear.md 02-the-two-paths.md 03-trust-and-honor.md \
         04-the-path-of-light.md 05-warning-against-adultery.md 06-sluggard-and-seducer.md \
         07-the-simple-youth.md 08-wisdom-at-creation.md 09-two-houses-two-feasts.md; do
    add_chapter "$f"
done

add_volume "卷二 · 所羅門的箴言（一） (Proverbs of Solomon I) · 10-22:16章" \
    "三百七十五對句，幾乎不再重複「因為耶和華說」——義人與惡人、智慧與愚昧的對比鋪滿生活的每一角落：言語、財富、懶惰、君王、朋友、教養兒女。\n>\n> **啟示的次序·沉默的中段**：神不再逐句重複祂的名字，卻讓敬畏祂的心滲透了尋常生活的每一寸——這正是次序本身要說的話：信仰不是聖殿裏的宗教活動，是餐桌、帳本、口舌上的忠信。"
for f in 10-first-collection-opens.md 11-integrity-and-generosity.md 12-righteous-tongue-diligence.md \
         13-wise-son-and-wealth.md 14-wisdom-builds-house.md 15-soft-answer.md \
         16-lord-establishes-steps.md 17-friend-loves-at-all-times.md 18-tower-of-the-name.md \
         19-poverty-and-discipline.md 20-weights-and-wine.md 21-kings-heart-in-lords-hand.md \
         22-good-name-and-training.md; do
    add_chapter "$f"
done

add_volume "卷三 · 智慧人的言語 (Words of the Wise) · 22:17-24章" \
    "語氣一轉，改用「我兒」式的具體訓誨——先是三十句智慧人的言語，後附智慧人的補充言語，篇幅雖短，卻把卷二鋪開的原則收攏成幾組扎實的忠告。\n>\n> **啟示的次序·沉默的中段**：不要嫉妒惡人的一時得勢（23:17、24:19-20）——次序仍在教導同一件事：眼睛看的是「現在」，敬畏耶和華看的是「終局」。"
for f in 23-words-of-the-wise-begin.md 24-further-words-of-wise.md; do
    add_chapter "$f"
done

add_volume "卷四 · 希西家人所輯所羅門箴言 (Hezekiah's Collection) · 25-29章" \
    "「這也是所羅門的箴言，是猶大王希西家的人所謄錄的」（25:1）——第二批所羅門箴言，多用比擬手法（「如同……」），集中談君王、審判與治家。\n>\n> **啟示的次序·沉默的中段**：連這卷書本身的傳遞過程都示範著次序——智慧不是一次性頒佈就完了，是要被謄錄、被傳給下一代（25:1），一如以色列歷代的敬虔要傳給兒女（申6:6-7）。"
for f in 25-hezekiahs-collection-opens.md 26-fool-sluggard-and-strife.md 27-iron-sharpens-iron.md \
         28-righteous-bold-as-lion.md 29-vision-and-correction.md; do
    add_chapter "$f"
done

add_volume "卷五 · 亞古珥、利慕伊勒與才德婦人 (Agur, Lemuel, and the Excellent Wife) · 30-31章" \
    "全書收在兩個人物身上：謙卑承認自己無知的亞古珥，以及利慕伊勒王母教導兒子分辨的智慧——終篇是一首離合詩，把三十章抽象的智慧位格化，具體活成一位敬畏耶和華的婦女一天的作息。\n>\n> **啟示的次序·終點**：抽象的智慧（1、8、9章那位在街市呼喊的女子）終於落成具體的婦人（31章）——她紡線、理家、賙濟窮人、開口就是智慧。1:7「敬畏耶和華是知識的開端」與31:30「惟敬畏耶和華的婦女必得稱讚」首尾扣合，三十一章走了一整圈，只為回答一個問題：敬畏耶和華，落在生活裏，是甚麼樣子？"
for f in 30-agurs-oracle.md 31-the-excellent-wife.md; do
    add_chapter "$f"
done

# ============================================================
# 卷末 · 越照越明，直到日午
# ============================================================
add_volume "卷末 · 越照越明，直到日午 (Brighter unto the Perfect Day)" \
    "全書從一句判詞起頭，走過街市上智慧的呼喚，鋪滿了尋常生活的每一角落，最終停在一位婦人一天的作息——這條路沒有一步是繞過日常走的。"
add_front "$INPUT_DIR/99-fear-of-the-lord.md"

# 跋 — afterword.
echo "  Adding (unnumbered): 999-afterword.md"
tail -n +8 "$INPUT_DIR/999-afterword.md" \
  | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}" ; done=1 } } {print}' >> "$COMBINED_MD"
printf '\n\\newpage\n\n' >> "$COMBINED_MD"
((chapter_count++))

# ============================================================
# 附錄 — bibliography and indices
# ============================================================
# Order is bibliography then indices: the index goes last in a printed book.
# See build-job-consolidated.sh for the incident (a book shipping 363 pages
# with no bibliography while every chapter cross-referenced one) this order
# and the --write regeneration above both guard against.
add_volume "附錄 (Appendices)" \
    "參考資料、逐章引句一覽、經文索引與主題索引——各章正文所指的「卷末附錄」即此。"
add_front "$INPUT_DIR/99-appendix-references.md"
add_front "$INPUT_DIR/98-appendix-indices.md"

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters)"
echo ""
echo "🔨 Generating PDF with proverb.latex template..."

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
