#!/bin/bash

# Esther PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine) + 全書領受總綱 + 四卷 13 段 + 卷末 + 跋
# Uses templates/pdf/esther.latex (ImperialPurple/NightIndigo/HiddenCrimson theme,
# matching the Ruth / Job / Isaiah series standard: cover art, frontispiece)
# INPUT_DIR may be overridden from the environment (used for probe builds).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="${INPUT_DIR:-$PROJECT_ROOT/books/bible/esther}"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/esther-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/esther-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/esther.latex"

echo "=========================================="
echo "🕯️ Esther Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "以斯帖記研讀"
subtitle: "Esther Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年10月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **歷代注疏資源整合**（詳見書中〈附錄：參考資料〉）

  **神的名字不在，神的手無處不在：隱、危、轉、定**

  卷一 · 隱：神的手在暗處預備 (第1–2章) | 卷二 · 危：危機公開，神仍不出聲 (第3–4章)
  卷三 · 轉：一串「恰巧」 (第5–7章) | 卷四 · 定：寫進律法、日曆與記憶 (第8–10章)

  **經文版權聲明 (Scripture Copyright Notices)**

  本版為教會內部贈閱版（非賣品）；公開發行時另行申請 ISBN。

  中文經文引自《聖經》和合本（1919），屬公有領域。

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
# ahead of the book's own 第一章, and the contents page reads two conflicting
# numbers on one line. Marking these unnumbered lets the 13 study units number
# 1-13. Same approach as build-ruth/job/isaiah-consolidated.sh.
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
add_front "$INPUT_DIR/00a-esther-position.md"
add_front "$INPUT_DIR/00b-hidden-providence-spine.md"

# Systematic reception — demote headings one level so it reads as one chapter.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
    tail -n +2 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 四卷 · 13 段
# ============================================================
add_volume "卷一 · 隱：神的手在暗處預備 (Hidden) · 以斯帖記 1–2章" \
    "啟示的次序·第一步——先預備，後患難：王后的位子空了，孤女被帶進王宮，一樁無人記功的救駕寫進史冊，全在危機出現之前，神一句話也沒有說。"
for f in 01-*.md 02-*.md 03-*.md; do
    for match in "$INPUT_DIR"/$f; do
        [ -f "$match" ] && add_chapter "$(basename "$match")"
    done
done

add_volume "卷二 · 危：危機公開，神仍不出聲 (Endangered) · 以斯帖記 3–4章" \
    "啟示的次序·第二步——亞甲人哈曼抽籤定日，詔書發遍一百二十七省；神沒有發言，卻讓末底改把「焉知」放到以斯帖面前。"
for f in 04-*.md 05-*.md 06-*.md; do
    for match in "$INPUT_DIR"/$f; do
        [ -f "$match" ] && add_chapter "$(basename "$match")"
    done
done

add_volume "卷三 · 轉：一串「恰巧」(Turned) · 以斯帖記 5–7章" \
    "啟示的次序·第三步——整個翻轉靠一串恰巧：金杖、兩次筵席、不眠之夜、哈曼自己的木架。"
for f in 07-*.md 08-*.md 09-*.md 10-*.md; do
    for match in "$INPUT_DIR"/$f; do
        [ -f "$match" ] && add_chapter "$(basename "$match")"
    done
done

add_volume "卷四 · 定：寫進律法、日曆與記憶 (Settled) · 以斯帖記 8–10章" \
    "啟示的次序·第四步——翻轉被寫進律法、日曆與記憶：王的反詔、反轉之日、普珥節、末底改的尊榮。"
for f in 11-*.md 12-*.md 13-*.md; do
    for match in "$INPUT_DIR"/$f; do
        [ -f "$match" ] && add_chapter "$(basename "$match")"
    done
done

# ============================================================
# 卷末 · 隱而不缺席
# ============================================================
add_volume "卷末 · 隱而不缺席 (The Hidden Yet Present)" \
    "全書從王后的空缺起頭，經過詔書、不眠之夜與木架，停在普珥日的日曆上——神的名字始終不在書裏，神的手始終不在書外。"
add_front "$INPUT_DIR/99-epilogue.md"

# 附錄：參考資料 — every chapter's 體例說明 box points here ("見卷末《附錄：
# 引用出處總表》"); it must actually be in the printed book, not just exist
# as a repo file used by check-citation-ledger.py.
add_front "$INPUT_DIR/98-appendix-indices.md"
add_front "$INPUT_DIR/99-appendix-references.md"

# 跋 — afterword. Last content file: no trailing \newpage.
if [ -f "$INPUT_DIR/999-afterword.md" ]; then
    echo "  Adding (unnumbered): 999-afterword.md"
    tail -n +8 "$INPUT_DIR/999-afterword.md" \
      | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}" ; done=1 } } {print}' >> "$COMBINED_MD"
    ((chapter_count++))
fi

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters)"
echo ""
echo "🔨 Generating PDF with esther.latex template..."

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
