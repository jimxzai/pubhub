#!/bin/bash

# Genesis PDF Builder - CONSOLIDATED 2026 EDITION
# = 前言 + 卷首定位(overview/revelation-order) + 五卷 17 章 + 卷末 + 跋 + 九篇附錄
# Uses templates/pdf/genesis.latex, matching the Gospel of John / Job /
# Romans / Acts consolidated-build standard: part dividers carry the
# book's spine (啟示的次序) forward at every volume opening.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/genesis"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/genesis-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/genesis-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/genesis.latex"

echo "=========================================="
echo "📖 Genesis Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "創世記研讀"
subtitle: "Genesis Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年9月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **黃長老查經法** — 整本聖經脈絡的深度領受，以約翰福音1:1-18與希伯來書為理解創世記的鑰匙

  • **John MacArthur** — 逐節解經講道 (gty.org)

  • **G. Campbell Morgan** — 解經王子 (*The Analyzed Bible*)

  **經文版權聲明 (Scripture Copyright Notices)**

  中文經文引自《聖經》和合本修訂版。

  Scripture quotations taken from the New American Standard Bible® (NASB),
  Copyright © 1960, 1971, 1977, 1995 by The Lockman Foundation. Used by
  permission. All rights reserved. lockman.org

  **起初的道——創造萬有的主，也是後來道成肉身的主**

  「太初有道，道與神同在，道就是神……萬物是藉著他造的。」——約翰福音 1:1,3

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

# Front/back matter: same as add_file but marks the H1 {.unnumbered} so it
# does not consume a LaTeX chapter number ahead of the 17 study chapters.
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
    # %b (not %s) for the description: it carries a literal \n>\n> to open a
    # second blockquote paragraph (the 啟示的次序 marker). printf only expands
    # escapes inside the FORMAT string, so with %s those arrive in the
    # markdown as the two characters \ and n and xelatex then dies on
    # "Undefined control sequence \n".
    printf '# %s {.unnumbered}\n\n> %b\n' "$1" "$2" >> "$COMBINED_MD"
    printf '\n\\newpage\n\n' >> "$COMBINED_MD"
    echo "  --- $1"
}

add_chapter() {
    add_file "$INPUT_DIR/$1"
}

# 前言 — preface
add_front "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位 — orientation: overview and the order of revelation
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這兩章：全書地圖與十段家譜的骨架，以及最要緊的一章——神在創世記裏按甚麼次序顯明自己與祂的計劃。"

add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-revelation-order.md"

# ============================================================
# 正文 · 五卷 · 17 章
# ============================================================
add_volume "卷一 · 太初歷史 (Primeval History) · 1-11章" \
    "創造、墮落、洪水、巴別——敘事的漏斗在此最寬：神與全人類同在，尚未收窄到一個家、一個支派。\n>\n> **啟示的次序·第一步**：應許被嵌入審判正中央（3:15）——神定罪的同時，已經應許救法。恩典的記號隨後向全人類敞開，沒有揀選的門檻（9:12-17 彩虹之約）。"
for f in 01-creation.md 02-fall.md 03-cain-abel.md 04-noah.md 05-babel.md; do
    add_chapter "$f"
done

add_volume "卷二 · 亞伯拉罕 (Abraham) · 12-25:18章" \
    "漏斗第一次收窄：從全人類收到一個人、一個家——亞伯蘭蒙召，應許臨到他和他的後裔。\n>\n> **啟示的次序·第二步**：應許的記號從普世（彩虹）收窄為一家（割禮，17章），並第一次有了「代替者」的形狀——摩利亞山上的公羊，「耶和華以勒」（22:8,14）。"
for f in 06-abraham-call.md 07-covenant.md 08-sodom.md 09-isaac-sacrifice.md; do
    add_chapter "$f"
done

add_volume "卷三 · 以撒與雅各 (Isaac and Jacob) · 25:19-36章" \
    "漏斗再收窄：以撒而非以實瑪利，雅各而非以掃——應許不是按長幼常規、不是按人的功勞轉移的。\n>\n> **啟示的次序·第三步**：應許臨到逃亡、一無所有的雅各；他與神較力，蒙賜新名以色列（32章）——揀選先於配得。"
for f in 10-jacob-esau.md 11-bethel.md 12-wrestling.md; do
    add_chapter "$f"
done

add_volume "卷四 · 約瑟 (Joseph) · 37-50章" \
    "應許透過一個被弟兄所賣、被主人所棄的人存活下來——「你們的意思是要害我，但神的意思原是好的」（50:20）。\n>\n> **啟示的次序·收窄的終點**：鏡頭最終停在猶大身上（49:8-10）——圭必不離猶大，直到啟示錄5:5才交在那位猶大支派的獅子手裏。"
for f in 13-joseph-dreams.md 14-joseph-egypt.md 15-reconciliation.md 16-blessings.md; do
    add_chapter "$f"
done

# ============================================================
# 卷末 · 應許存留 — bridging chapter into Exodus and Joshua
# ============================================================
add_volume "卷末 · 應許存留 (The Promise Kept in Waiting)" \
    "全書以一具棺材、一句「神必定看顧你們」收筆——不是失敗，是次序：神沒有把整個計劃一次交代完。"
add_chapter "17-covenant-fulfillment.md"

# From here on, every remaining chapter is unnumbered ({.unnumbered},
# \@schapter) back matter. \@schapter never resets the `section` counter the
# way a real \chapter does, so without this its subsections would keep
# counting up from wherever chapter 17 left off and print as "17.62" etc —
# a reader-facing bug (looks like the afterword and every appendix are
# subsections of chapter 17). secnumdepth=-1 turns off section numbering
# entirely for this unnumbered back matter; nothing after this point is a
# numbered chapter, so there is no need to restore it.
printf '\\setcounter{secnumdepth}{-1}\n\n' >> "$COMBINED_MD"

# 跋 — afterword
add_front "$INPUT_DIR/999-afterword.md"

# ============================================================
# 附錄 — nine appendices: index, themes, references, typology, etc.
# ============================================================
add_volume "附錄 (Appendices)" \
    "經文索引、主題索引、參考資料、創世記在五經中的位置、基督預表總表、原文詞彙表、讀經計劃、十段家譜深析、約與名字總表。"
for i in 99a 99b 99c 99d 99e 99f 99g 99h 99i; do
    for f in "$INPUT_DIR/$i-"*.md; do
        [ -f "$f" ] && add_front "$f"
    done
done

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count files)"
echo ""
echo "🔨 Generating PDF with genesis.latex template..."

# --verbose is load-bearing, not chatter: without it pandoc swallows the whole
# xelatex log and every grep-the-log check (and in driver.sh) passes vacuously.
# See scripts/lib/latex-check.sh for the full explanation.
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

echo ""
echo "✅ PDF generated: $OUTPUT_PDF"
