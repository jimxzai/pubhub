#!/bin/bash

# Deuteronomy PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine) + 全書領受總綱 + 五卷 26 章 + 卷末 + 跋
# Uses templates/pdf/duetonomy.latex (Stone/Covenant/Jordan theme, matching the
# Gospel of John / Acts of the Apostles / Isaiah / Job series standard: cover
# art, frontispiece)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/duetonomy"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/duetonomy-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/duetonomy-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/duetonomy.latex"

echo "=========================================="
echo "🪨  Deuteronomy Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "申命記研讀"
subtitle: "Deuteronomy Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年9月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **老弟兄查經法** — 方法論應用（本書無第一手教導筆記，詳見卷首說明）

  • **Matthew Henry** — 《Commentary on the Whole Bible》申命記部分

  • **John Calvin** — 《Commentary on the Last Four Books of Moses Arranged
    in the Form of a Harmony》

  • **G. Campbell Morgan** — 《Full Exposition of the Bible》（12 章）；
    另有麥克阿瑟新約講道中論及申命記經文者、屈梭多模與麥克拉倫各一處，
    逐條出處與核校結果見卷末《附錄：引用出處總表》

  **曠野路程的終點，應許之地的起點：立約更新、律法的第二次頒佈、摩西最後的話**

  曠野路程的回顧 (1-4章) | 總綱誡命 (5-11章) | 律例典章 (12-26章)
  立約更新：祝福與咒詛 (27-30章) | 摩西的末了 (31-34章)

  **經文版權聲明 (Scripture Copyright Notices)**

  本版為教會內部贈閱版（非賣品）；公開發行時另行申請 ISBN。

  中文經文引自《聖經》和合本（1919），屬公有領域。

  Scripture quotations taken from the New American Standard Bible® (NASB),
  Copyright © 1960, 1971, 1977, 1995 by The Lockman Foundation. Used by
  permission. All rights reserved. lockman.org

  All rights reserved.
---

HEADER

# ------------------------------------------------------------------
# Regenerate the Scripture index BEFORE assembling, so the appendix can
# never describe an older state of the chapters than the one being built.
# This was a real defect: the appendix was generated at 22:24 and two of
# the chapters it indexes were edited at 23:38, so the shipped table was
# missing 王下18 (cited in ch26) and still carried a 羅馬書2 row for a
# citation ch16 no longer had. A script you have to remember to run is a
# script that will be forgotten; wiring it into the build removes the
# remembering.
# ------------------------------------------------------------------
if [ -f "$SCRIPT_DIR/gen-duetonomy-scripture-index.py" ]; then
    echo "🔄 Regenerating Scripture index from current chapter text..."
    python3 "$SCRIPT_DIR/gen-duetonomy-scripture-index.py" --write || {
        echo "❌ Scripture index regeneration failed"; exit 1; }
fi

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
# numbers 1-9 and the book's own 第一章 comes out as LaTeX chapter 10 — the
# contents page then reads "10  第一章 · ...", two conflicting numbers on one
# line. Marking these unnumbered lets the 26 study units number 1-26,
# matching 第一章-第二十六章. Same approach as build-job-consolidated.sh and
# build-isaiah-consolidated.sh.
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
add_front "$INPUT_DIR/00a-duetonomy-position.md"
add_front "$INPUT_DIR/00b-covenant-spine.md"
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
# 正文 · 五卷 · 26 段
# ============================================================
add_volume "卷一 · 曠野路程的回顧 (Historical Prologue) · 1-4章" \
    "啟示的次序·第一步：先數算恩典，才提出要求。條約第一、二要素：序言與歷史回顧。摩西回顧四十年曠野路，不是為了懷舊——立約文書的規矩是：先數算宗主做過甚麼，才提出要求。**恩典的敘述擺在要求之前**，這個次序本身就是信息。"
for f in 01-wilderness-review.md 02-call-to-obedience.md; do
    add_chapter "$f"
done

add_volume "卷二 · 總綱誡命 (The Great Commandments) · 5-11章" \
    "啟示的次序·第二步：先立原則，後給細則。條約第三要素：總綱要求。十誡重申，繼而是示瑪與盡心盡性盡力愛神的呼召。十誡自己也守著同一個次序——先宣告「我是耶和華你的神，曾將你從埃及地為奴之家領出來」（5:6），才說「除了我以外，你不可有別的神」（5:7）。**原則在細節之前**：這一卷立定根基，下一卷才展開條例。"
for f in 03-ten-words-again.md 04-shema-and-love.md 05-set-apart-nations.md \
         06-remember-the-wilderness.md 07-golden-calf-remembered.md \
         08-blessing-and-curse-choice.md; do
    add_chapter "$f"
done

add_volume "卷三 · 律例典章 (The Specific Stipulations) · 12-26章" \
    "啟示的次序·第三步：把愛神落實成日常的具體長相。條約第四要素：具體規範。敬拜、審判、聖潔、家庭、戰爭、市場的條例——十五章，全書篇幅最長的一卷。這些不是另一套要求，是同一個「盡心愛神」在生活各角落的具體長相。**離開示瑪讀律例，律例就成了瑣碎的規條**；記住示瑪讀律例，才看得出神要的是甚麼樣的一個群體。"
for f in 09-one-place-of-worship.md 10-false-prophets-and-idolatry.md \
         11-clean-unclean-and-tithes.md 12-sabbatical-release.md \
         13-three-feasts-and-justice.md 14-priests-levites-and-the-prophet.md \
         15-cities-of-refuge-and-war.md 16-family-and-community-laws.md \
         17-holiness-in-community.md 18-firstfruits-and-declaration.md; do
    add_chapter "$f"
done

add_volume "卷四 · 立約更新：祝福與咒詛 (Covenant Renewal: Blessing and Curse) · 27-30章" \
    "啟示的次序·第四步：說盡了，才要人選。條約第五要素：祝福與咒詛。示劍宣讀祝福與咒詛，摩押平原重新立約。**抉擇擺在教導之後，不擺在開頭當威嚇**——摩西把該說的都說盡了，才說「我今日將生與福，死與禍，陳明在你面前……所以你要揀選生命」（30:15, 19）。神從不要求人在不明白的情況下作決定。"
for f in 19-shechem-covenant.md 20-blessings-and-curses.md 21-moab-covenant.md \
         22-choose-life.md; do
    add_chapter "$f"
done

add_volume "卷五 · 摩西的末了 (The End of Moses) · 31-34章" \
    "啟示的次序·第五步：話語留下，中保退場，應許朝前開著。條約第六要素：繼承安排。約書亞受託、摩西之歌、十二支派的祝福，最終死在尼波山，望見卻不得進入。在古代立約文書裏，指定接班人與存放約書不是附錄，**是這份約如何活過中保之死的安排**——而全書合上時，18:15 所應許「像我的一位先知」仍未出現（34:10），妥拉刻意停在這個懸念上。"
for f in 23-joshua-commissioned.md 24-song-of-moses.md 25-blessing-of-the-tribes.md \
         26-death-of-moses.md; do
    add_chapter "$f"
done

# ============================================================
# 卷末 · 從曠野到迦南
# ============================================================
add_volume "卷末 · 從曠野到迦南 (From Wilderness to Canaan)" \
    "全書從曠野的回顧起頭，走過總綱、典章與立約的更新，最終停在約旦河邊——這條路沒有一步是繞過選擇走的。"
add_front "$INPUT_DIR/99-covenant-and-conquest.md"

# ============================================================
# 附錄 — indices and the citation ledger. These are part of the book:
# the per-chapter 體例說明 boxes point readers at 《附錄：引用出處總表》,
# so omitting them leaves 25 dangling cross-references in the printed text.
# ============================================================
add_volume "附錄 (Appendices)" \
    "全書索引、新約引用對照，以及每一條引文的出處與核校結果。附錄二把新約引用申命記之處編成十四組對照（共二十四則新約經文），附錄三是自動生成的全書經文索引，附錄的引用出處總表則逐位注疏者、逐章交代核校狀態。"
add_front "$INPUT_DIR/98-appendix-indices.md"
add_front "$INPUT_DIR/99-appendix-references.md"

# 跋 — afterword. Last content file: no trailing \newpage.
echo "  Adding (unnumbered): 999-afterword.md"
tail -n +8 "$INPUT_DIR/999-afterword.md" \
  | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}" ; done=1 } } {print}' >> "$COMBINED_MD"
((chapter_count++))

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters)"
echo ""
echo "🔨 Generating PDF with duetonomy.latex template..."

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
