#!/bin/bash

# Jude PDF Builder - CONSOLIDATED 2026 EDITION
# = preface + orientation (overview / position / order of revelation)
#   + 5 sections of Jude (one part divider per step of the spine)
#   + 卷末 (systematic reception) + appendices + afterword
# Sources from books/bible/jude/ (老弟兄 methodology + Clement of Alexandria +
# Calvin + Morgan + MacArthur, CUV + NASB 1995 scripture).
# Modeled on scripts/build-2-peter-consolidated.sh (unnumbered front/back
# matter so the five sections number 1..5) and scripts/build-james-consolidated.sh
# (part dividers carrying the spine: 「啟示的次序·第N步」 + 貫穿的線 table).
# Uses templates/pdf/jude.latex (deep purple / gold).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/jude"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/jude-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/jude-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/jude.latex"

echo "=========================================="
echo "📖 Jude PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "猶大書研讀"
subtitle: "Epistle of Jude Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年10月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **資源整合：**

  • **老弟兄查經方法論之應用**（倉庫中沒有老弟兄以猶大書為題的查經記錄，詳見附錄〈引用出處總表〉的誠實聲明）

  • **亞歷山大的革利免** — *Comments on the Epistle of Jude*（《尼西亞前教父》第二卷，公有領域）

  • **John Calvin** — *Commentaries on the Catholic Epistles*（公有領域）

  • **G. Campbell Morgan** — 解經著作（公有領域）

  • **John MacArthur** — 逐節講道 (gty.org)

  **蒙保守的人，為真道竭力地爭辯**

  「保守自己常在神的愛中，仰望我們主耶穌基督的憐憫，直到永生。」（猶21）

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

# A numbered chapter (the five sections of Jude).
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
add_front "$INPUT_DIR/00a-jude-position.md"
add_front "$INPUT_DIR/00c-revelation-order.md"

# ============================================================
# 正文 · 五步
# ============================================================
add_volume "第一步 · 猶大書 1-4 節 (Step One)" \
    "啟示的次序·第一步：神先開口說你是誰——被召、蒙愛、蒙保守；然後才把爭辯交在你手裏。真道已經「一次交付」，神的話說完了。" \
    "**保守在先，爭辯在後**——警告之前，先有身分" \
    "3節「要為從前一次交付聖徒的真道竭力地爭辯」" \
    "我是站在神的保守裏爭辯，還是想靠爭辯來站穩？"
add_chapter 01

add_volume "第二步 · 猶大書 5-7 節 (Step Two)" \
    "啟示的次序·第二步：神的審判不是將來才有的假設，是已經寫進歷史的事實——救了又滅的百姓、被拘留的天使、作為鑑戒的城。" \
    "**提醒**——你們雖然都知道，我卻仍要提醒你們" \
    "5節「從前主救了他的百姓出埃及地，後來就把那些不信的滅絕了」" \
    "我把神從前的審判當作故事，還是當作鏡子？"
add_chapter 02

add_volume "第三步 · 猶大書 8-16 節 (Step Three)" \
    "啟示的次序·第三步：神早已預言了「這些人」，也預言了祂自己的來臨——審判有一個日子，有一位審判者。" \
    "**這些人**——經上的樣本，今日的應驗" \
    "14節「看哪，主帶著他的千萬聖者降臨」" \
    "我身上有沒有「這些人」的影子——輕慢、怨言、為利？"
add_chapter 03

add_volume "第四步 · 猶大書 17-23 節 (Step Four)" \
    "啟示的次序·第四步：在主來以前的等候裏，神藉使徒的話、藉聖靈、藉祂的愛與憐憫說話——被保守的人保守自己，也去憐憫人。" \
    "**你們卻要**——父、聖靈、主耶穌基督，三一的神環繞等候的人" \
    "21節「保守自己常在神的愛中，仰望我們主耶穌基督的憐憫，直到永生」" \
    "我在等候主來的日子裏，是在建造自己，還是只在批評別人？"
add_chapter 04

add_volume "第五步 · 猶大書 24-25 節 (Step Five)" \
    "啟示的次序·第五步，也是全信的終點：最後一句話交給神的能力——從萬古以前，到現今，直到永永遠遠。猶大原想寫的「同得的救恩」，寫在這裏。" \
    "**那能**——全信最後的主詞是神" \
    "24節「那能保守你們不失腳、叫你們無瑕無疵、歡歡喜喜站在他榮耀之前的」" \
    "我最後靠的，是自己的持守，還是那能保守我的？"
add_chapter 05

# ============================================================
# 卷末 · 全書領受總綱
# ============================================================
add_volume "卷末 · 回望 (Looking Back)" \
    "五步讀完，把全信的領受收攏成一張圖——再一次站在兩個「保守」中間，看見那位保守者。"

# The study file is a synthesis OF the five sections, so it sits after them
# (as in 2 Peter), not in the front matter. No YAML: first line is its H1.
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

echo "🔨 Generating PDF with jude.latex template..."

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
