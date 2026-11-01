#!/bin/bash

# Malachi PDF Builder - CONSOLIDATED 2026 EDITION
# = preface + orientation (overview / position / order of revelation)
#   + 6 steps of Malachi (one part divider per step of the spine; eight chapters)
#   + 卷末 (the way to the Gospels) + systematic reception + appendices + afterword
# Sources from books/bible/malachi/ (老弟兄 methodology + Calvin + Henry + Morgan +
# MacArthur's remarks on Malachi verses in sermons elsewhere; CUV + NASB 1995 scripture;
# gty.org has no Malachi verse-by-verse series).
# Modeled on scripts/build-obadiah-consolidated.sh (unnumbered front/back matter so
# the eight chapters number 1..8; part dividers carry the spine:
# 「啟示的次序·第N步」 + 貫穿的線 table).
# Uses templates/pdf/malachi.latex (dawn claret / gold, full-bleed front and back covers).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/malachi"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/malachi-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/malachi-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/malachi.latex"

echo "=========================================="
echo "📖 Malachi PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "瑪拉基書研讀"
subtitle: "The Book of Malachi Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年10月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **資源整合：**

  • **老弟兄查經方法論之應用**（倉庫中沒有老弟兄以瑪拉基書為題的查經記錄，詳見附錄〈引用出處總表〉的誠實聲明）

  • **John Calvin** — *Commentaries on the Twelve Minor Prophets*, vol. 5（Zechariah, Malachi），tr. John Owen（公有領域）

  • **Matthew Henry** — *An Exposition of the Old and New Testament*（公有領域）

  • **G. Campbell Morgan** — *Living Messages of the Books of the Bible*（公有領域）

  • **John MacArthur** — gty.org 沒有瑪拉基書的逐節系列；本書只引他在別篇講道裏解釋瑪拉基書經節的句子（出處見各章與附錄）

  **你在何事上愛我們呢？**

  「耶和華說：我曾愛你們。你們卻說：你在何事上愛我們呢？」（瑪1:2）

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

# A numbered chapter (the eight chapters of Malachi).
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
add_front "$INPUT_DIR/00a-malachi-position.md"
add_front "$INPUT_DIR/00c-revelation-order.md"

# ============================================================
# 正文 · 六步
# ============================================================
add_volume "第一步 · 瑪拉基書 1:1-5 (Step One)" \
    "啟示的次序·第一步：神先開口——「我曾愛你們」是全書第一句神的話；人的第一個問題「你在何事上愛我們呢？」緊跟在後。" \
    "**愛**——神的第一句話，人的第一個質問" \
    "2節「耶和華說：我曾愛你們。你們卻說：你在何事上愛我們呢？」" \
    "我向神要的證據，是甚麼？"
add_chapter 01

add_volume "第二步 · 瑪拉基書 1:6–2:9 (Step Two)" \
    "啟示的次序·第二步：名——神向祭司說話：你們輕看我的名；問題二、三；利未之約本是生命與平安。" \
    "**名**——十次，八次在這一步" \
    "1:6「我若是父親，尊敬我的在哪裏呢？」" \
    "我獻給神的，是我最好的，還是我不要的？"
add_chapter 02
add_chapter 03

add_volume "第三步 · 瑪拉基書 2:10-16 (Step Three)" \
    "啟示的次序·第三步：約——詭詐五次，全在這一步；對弟兄、對妻子；耶和華在中間作見證。" \
    "**詭詐**（בגד）五次，全在 2:10-16" \
    "2:14「因耶和華在你和你幼年所娶的妻中間作見證」" \
    "我與人所立的約，神是見證人。我記得嗎？"
add_chapter 04

add_volume "第四步 · 瑪拉基書 2:17–3:5 (Step Four)" \
    "啟示的次序·第四步：使者——「公義的神在哪裏呢？」神的回答是差遣：我的使者，和忽然進入殿的主。" \
    "**差遣**——神作主詞的 שלח 四次，這是第三次" \
    "3:1「你們所尋求的主必忽然進入他的殿」" \
    "我天天問「神在哪裏」，若祂真的來了，我站得住嗎？"
add_chapter 05

add_volume "第五步 · 瑪拉基書 3:6-12 (Step Five)" \
    "啟示的次序·第五步：轉向——我不改變，所以你們沒有滅亡；現在你們要轉向我，我就轉向你們。" \
    "**轉向**（שׁוּב）七次，三次在 3:7" \
    "3:6「因我─耶和華是不改變的，所以你們雅各之子沒有滅亡」" \
    "我的轉向，是從哪一件事開始？"
add_chapter 06

add_volume "第六步 · 瑪拉基書 3:13–4:6 (Step Six)" \
    "啟示的次序·第六步，也是全書的終點：日子——紀念冊、公義的日頭、以利亞；全書最後一個詞是「咒詛」，後面跟著「免得」。" \
    "**日子**八次，**日頭**兩次（1:11；4:2）" \
    "4:2「但向你們敬畏我名的人必有公義的日頭出現」" \
    "那日來到，我要的是怎樣的光？"
add_chapter 07
add_chapter 08

# ============================================================
# 卷末 · 通往福音書與啟示錄
# ============================================================
add_volume "卷末 · 通往福音書與啟示錄 (The Way On)" \
    "舊約最後一卷與新約第一卷之間，沒有再留下任何一卷書。瑪拉基書最後的兩個「差遣」，是福音書開頭的第一批句子。"
add_front "$INPUT_DIR/90-to-the-gospels.md"

# ============================================================
# 卷末 · 全書領受總綱
# ============================================================
add_volume "卷末 · 回望 (Looking Back)" \
    "六步讀完，把全書的領受收攏成一張圖——再一次站在「我曾愛你們」和「免得我來咒詛遍地」中間，看見那位被差來的主。"

# The study file is a synthesis OF the six steps, so it sits after them.
# No YAML: first line is its H1.
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

echo "🔨 Generating PDF with malachi.latex template..."

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
