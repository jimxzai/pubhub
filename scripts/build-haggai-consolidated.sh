#!/bin/bash

# Haggai PDF Builder - CONSOLIDATED 2026 EDITION
# = preface + orientation (overview / position / order of revelation)
#   + 5 sections of Haggai (one part divider per step of the spine)
#   + 卷末 (systematic reception) + appendices + afterword
# Sources from books/bible/Haggai/ (老弟兄 methodology + Calvin + Henry +
# Morgan, CUV + NASB 1995 scripture; no MacArthur — gty.org has no Haggai series).
# Modeled on scripts/build-jude-consolidated.sh (unnumbered front/back matter so
# the five sections number 1..5; part dividers carry the spine:
# 「啟示的次序·第N步」 + 貫穿的線 table).
# Uses templates/pdf/haggai.latex (temple-stone slate / gold, full-bleed front and back covers).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/Haggai"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/haggai-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/haggai-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/haggai.latex"

echo "=========================================="
echo "📖 Haggai PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "哈該書研讀"
subtitle: "The Book of Haggai Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年10月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **資源整合：**

  • **老弟兄查經方法論之應用**（倉庫中沒有老弟兄以哈該書為題的查經記錄，詳見附錄〈引用出處總表〉的誠實聲明）

  • **John Calvin** — *Commentaries on the Twelve Minor Prophets*, vol. 4（Habakkuk, Zephaniah, Haggai），tr. John Owen（公有領域）

  • **Matthew Henry** — *An Exposition of the Old and New Testament*（公有領域）

  • **G. Campbell Morgan** — *Living Messages of the Books of the Bible*（公有領域）

  • 本書沒有 John MacArthur 的引文：gty.org 沒有以哈該書為題的講道系列

  **你把心放在哪裏？**

  「從今日起，我必賜福與你們。」（該2:19）

  **經文版權聲明 (Scripture Copyright Notices)**

  2026 年 10 月 · 初版。本版為教會內部贈閱版（非賣品）；公開發行時另行申請 ISBN。

  中文經文引自《聖經》和合本，屬公有領域；逐節核對來源見附錄〈引用出處總表〉。

  Scripture quotations taken from the New American Standard Bible® (NASB),
  Copyright © 1960, 1971, 1977, 1995 by The Lockman Foundation. Used by
  permission. All rights reserved. lockman.org
---

HEADER

chapter_count=0

# Strip the 7-line YAML front matter, convert ^n^ / ^24-25^ verse markers to
# \textsuperscript{}{} (the trailing {} keeps a digit from abutting a following
# \textbf{ — see build-2-peter-consolidated.sh for the root cause).
emit() {
    tail -n +8 "$1" | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}{}/g'
}

# A numbered chapter (the five sections of Haggai).
add_file() {
    local f="$1"
    [ -f "$f" ] || { echo "❌ Missing file: $1 — aborting build"; exit 1; }
    echo "  Adding: $(basename "$f")"
    emit "$f" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Front/back matter: first H1 marked unnumbered so it does not consume a
# chapter number.
add_front() {
    local f="$1"
    [ -f "$f" ] || { echo "❌ Missing file: $1 — aborting build"; exit 1; }
    echo "  Adding (unnumbered): $(basename "$f")"
    emit "$f" \
      | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); if($0 !~ /\{\.unnumbered\}$/) $0=$0" {.unnumbered}"; done=1 } } {print}' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Part divider. $2 is the one-line description (carries 「啟示的次序·第N步」);
# optional $3-$5 add the 貫穿的線 / 鑰節 / 貫穿的問題 table.
# printf '%s' (not %b) on purpose: descriptions are plain text, and %b would
# turn a literal backslash sequence into a control character.
add_volume() {
    printf '# %s {.unnumbered}\n\n> %s\n' "$1" "$2" >> "$COMBINED_MD"
    if [ -n "$3" ]; then
        printf '\n| | |\n|---|---|\n| **貫穿的線** | %s |\n| **鑰節** | %s |\n| **貫穿的問題** | %s |\n' \
            "$3" "$4" "$5" >> "$COMBINED_MD"
    fi
    printf '\n\\newpage\n\n' >> "$COMBINED_MD"
    echo "  --- $1"
}

add_chapter() {
    local f
    for f in "$INPUT_DIR/$1-"*.md; do
        [ -f "$f" ] && { add_file "$f"; return 0; }
    done
    echo "❌ Missing chapter file for prefix '$1-' in $INPUT_DIR — aborting build"
    exit 1
}

# 前言
add_front "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這三章：地圖、座標、骨幹——啟示的次序與神的計劃。"
add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-haggai-position.md"
add_front "$INPUT_DIR/00c-revelation-order.md"

# ============================================================
# 正文 · 五步
# ============================================================
add_volume "第一步 · 哈該書 1:1-11 (Step One)" \
    "啟示的次序·第一步：神先翻開帳本，才說「上山取木料」——百姓說「時候未到」，神不爭論時間表，先讀他們的收成，兩次說「省察」，然後才說「上山取木料」。" \
    "**省察**——把心放在你的道路上（五次）" \
    "5節「你們要省察自己的行為」" \
    "我撒的種多、收的卻少的，是哪一塊？"
add_chapter 01

add_volume "第二步 · 哈該書 1:12-15 (Step Two)" \
    "啟示的次序·第二步：先同在，後作工——百姓聽從之後，先知傳了兩個字的信息「我與你們同在」，耶和華激動三處的靈，他們才動工。" \
    "**同在**——兩個字，神動手" \
    "13節「我與你們同在」" \
    "我在等「感覺對了」的那件事，是在等時候，還是在等同在？"
add_chapter 02

add_volume "第三步 · 哈該書 2:1-9 (Step Three)" \
    "啟示的次序·第三步：用同在回答比較——眼睛說「如無有」，神三次說「當剛強」，指著出埃及的約說「我的靈住在你們中間」，並說「我就使這殿滿了榮耀」。" \
    "**榮耀**——被充滿的，不是造出來的" \
    "4節「因為我與你們同在」" \
    "我手上那件在我眼中如無有的事，我是在比較，還是在做工？"
add_chapter 03

add_volume "第四步 · 哈該書 2:10-19 (Step Four)" \
    "啟示的次序·第四步：祝福在收成之前——聖不傳染，污傳染；樹上還沒有果子，神說「從今日起，我必賜福與你們」。" \
    "**從今日**——主詞是神" \
    "19節「從今日起，我必賜福與你們」" \
    "我偷偷在用工作和獻上去換的那份祝福，是哪一份？"
add_chapter 04

add_volume "第五步 · 哈該書 2:20-23 (Step Five)" \
    "啟示的次序·第五步，也是全書的終點：最後一句是揀選——全書第一個「放」是人把心放在路上，最後一個「放」是神把人放成印；信息裏沒有一個命令是給所羅巴伯的。" \
    "**印**——放上去的，不是自己決定的" \
    "23節「我必以你為印，因我揀選了你」" \
    "我以為神揀選我是因為我的甚麼？"
add_chapter 05

# ============================================================
# 卷末 · 全書領受總綱
# ============================================================
add_volume "卷末 · 回望 (Looking Back)" \
    "五步讀完，把全書的領受收攏成一張圖——再一次回到那句話：「我與你們同在」，看見那位自己成為殿、又把我們放在手上的主。"

# The study file is a synthesis OF the five sections, so it sits after them
# (as in Jude), not in the front matter. No YAML: first line is its H1.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——老弟兄查經法 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
    tail -n +2 "$STUDY_FILE" | sed 's/^#/##/' | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}{}/g' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
else
    echo "❌ Missing file: $STUDY_FILE — aborting build"
    exit 1
fi

# ============================================================
# 附錄
# ============================================================
add_volume "附錄 (Appendices)" \
    "經文與主題索引、讀經計劃、引用出處總表——供查閱、跨章對照，並如實交代每一處引句的查證方式。"
add_front "$INPUT_DIR/98-appendix-indices.md"
add_front "$INPUT_DIR/96-appendix-reading-plan.md"
add_front "$INPUT_DIR/99-appendix-references.md"

# 跋 — last content file: no trailing \newpage (the colophon opens its own page).
[ -f "$INPUT_DIR/999-afterword.md" ] || { echo "❌ Missing file: $INPUT_DIR/999-afterword.md — aborting build"; exit 1; }
echo "  Adding (unnumbered): 999-afterword.md"
emit "$INPUT_DIR/999-afterword.md" \
  | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); if($0 !~ /\{\.unnumbered\}$/) $0=$0" {.unnumbered}"; done=1 } } {print}' >> "$COMBINED_MD"
((chapter_count++))

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count sections)"
echo ""

# Wrap Greek runs in an explicit {\greekfont …} group passed through pandoc as
# raw LaTeX (see build-2-peter-consolidated.sh for why ucharclasses alone is
# not trusted with bold spans, and why the group must be a `…`{=latex} span —
# a bare {…} is escaped by pandoc into an unscoped font switch). Chapter
# markdown therefore carries plain Greek, never a hand-written wrap.
echo "Wrapping Greek Unicode runs in {\\greekfont ...}..."
COMBINED_MD_PATH="$COMBINED_MD" python3 <<'PYEOF'
import os, re
path = os.environ['COMBINED_MD_PATH']
text = open(path, encoding='utf-8').read()
# Skip anything already inside a backtick span.
parts = re.split(r'(`[^`]*`(?:\{=latex\})?)', text)
greek_run = re.compile(r'[Ͱ-Ͽἀ-῿]+(?: [Ͱ-Ͽἀ-῿]+)*')
n = 0
for i in range(0, len(parts), 2):
    def wrap(m):
        global n
        n += 1
        return '`{\\greekfont ' + m.group(0) + '}`{=latex}'
    parts[i] = greek_run.sub(wrap, parts[i])
open(path, 'w', encoding='utf-8').write(''.join(parts))
print(f"  Wrapped {n} Greek run(s)")
PYEOF

echo "🔨 Generating PDF with haggai.latex template..."

# --verbose is load-bearing: without it pandoc swallows the xelatex log and
# every grep-the-log check (here and in driver.sh) passes vacuously.
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
  --top-level-division=chapter > "$LATEX_LOG" 2>&1
PANDOC_EXIT=$?

latex_build_report "$PANDOC_EXIT" "$LATEX_LOG" "$OUTPUT_PDF" || exit 1
