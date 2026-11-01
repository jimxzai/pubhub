#!/bin/bash

# Zechariah PDF Builder - CONSOLIDATED 2026 EDITION
# = preface + orientation (overview / position / order of revelation)
#   + 19 units of Zechariah under four part dividers (one per step of the spine)
#   + 卷末 (systematic reception) + appendices + afterword
# Sources from books/bible/zechariah/ (老弟兄 methodology + Calvin + Henry + Morgan
# + MacArthur + Pusey + the Fathers, CUV + NASB 1995 scripture).
# Modeled on the other books' consolidated build scripts in scripts/ (unnumbered front/back matter so
# the 19 units number 1..19; part dividers carry the spine:
# 「啟示的次序·第N步」 + 貫穿的線 table).
# Uses templates/pdf/zechariah.latex (midnight indigo / lampstand gold, full-bleed front and back covers).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/zechariah"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/zechariah-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/zechariah-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/zechariah.latex"

echo "=========================================="
echo "📖 Zechariah PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "撒迦利亞書研讀"
subtitle: "The Book of Zechariah Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年10月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **資源整合：**

  • **老弟兄查經方法論之應用**（倉庫中沒有老弟兄以撒迦利亞書為題的查經記錄，詳見附錄〈引用出處總表〉的誠實聲明）

  • **John Calvin** — *Commentaries on the Twelve Minor Prophets*, vol. 5（Zechariah and Malachi），tr. John Owen（公有領域）

  • **Matthew Henry** — *Commentary on the Whole Bible*, vol. 4（公有領域）

  • **G. Campbell Morgan** — *Living Messages of the Books of the Bible*（1912）與 *An Exposition of the Whole Bible*（1959）

  • **John MacArthur** — gty.org 撒迦利亞書逐章講道（sermon 2153-2171）；講道逐字稿僅作簡短引用並註明出處，版權屬原講者與 Grace to You

  • **E. B. Pusey** — *The Minor Prophets*, vol. 8（Zechariah，公有領域）；教父：**Justin Martyr**、**John Chrysostom**、**Cyril of Jerusalem**、**Augustine**（公有領域）

  **「你們要轉向我，我就轉向你們。」（亞1:3）**

  **經文版權聲明 (Scripture Copyright Notices)**

  2026 年 10 月 · 2026 整編版。本版為教會內部贈閱版（非賣品）；公開發行時另行申請 ISBN。

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

# A numbered chapter (the 19 units of Zechariah).
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
add_front "$INPUT_DIR/00a-zechariah-position.md"
add_front "$INPUT_DIR/00c-revelation-order.md"

# ============================================================
# 正文 · 四步（十九個單元）
# ============================================================
add_volume "第一步 · 撒迦利亞書 1–6 章 (Step One)" \
    "啟示的次序·第一步：神先回來——話在先，安慰在先，潔淨在先，靈在先；八個夜間異象之後，冠冕放在約書亞頭上，卻說有一人名叫苗（צֶמַח）。" \
    "**我已回來**——1:16 與 8:3 同一個完成式；「你們就知道萬軍之耶和華差遣了我」四次" \
    "4:6「不是倚靠勢力，不是倚靠才能，乃是倚靠我的靈」" \
    "我今天的工，是在神已經回來的前提下做，還是為了請祂回來而做？"
for n in 01 02 03 04 05 06 07 08 09; do add_chapter $n; done

add_volume "第二步 · 撒迦利亞書 7–8 章 (Step Two)" \
    "啟示的次序·第二步：百姓問禁食，神反問「豈是絲毫向我禁食麼」；然後「萬軍之耶和華如此說」連說，第8章獨佔十八次——我現在回到錫安，住在耶路撒冷中。" \
    "**萬軍之耶和華如此說**——全書五十三次，第8章十八次" \
    "7:5「豈是絲毫向我禁食麼？」；8:3「我現在回到錫安，要住在耶路撒冷中」" \
    "我做的宗教行為，是向誰做的？"
for n in 10 11; do add_chapter $n; done

add_volume "第三步 · 撒迦利亞書 9–11 章 (Step Three)" \
    "啟示的次序·第三步：第一個擔子——謙卑的王騎驢而來（9:9），無人牧養的群羊（10:2），被估價三十塊錢的牧人（11:12-13）。" \
    "**王**（9:9）與**牧人**（10:2；11:4-17；13:7）" \
    "9:9「你的王來到你這裏」；11:12-13" \
    "我把祂放在甚麼價位上？"
for n in 12 13 14 15; do add_chapter $n; done

add_volume "第四步 · 撒迦利亞書 12–14 章 (Step Four)" \
    "啟示的次序·第四步，也是全書的終點：第二個擔子——神先澆灌恩惠的靈，他們才仰望所扎的；牧人被擊，群羊被煉；耶和華的腳站在橄欖山上，作全地的王；連馬的鈴鐺和鍋都歸耶和華為聖。" \
    "**在那日**——全書二十二次，本步十七次" \
    "12:10；14:9；14:20-21" \
    "那日來到以前，我今天歸給主為聖的是甚麼？"
for n in 16 17 18 19; do add_chapter $n; done

# ============================================================
# 卷末 · 全書領受總綱
# ============================================================
add_volume "卷末 · 回望 (Looking Back)" \
    "四步讀完，把全書的領受收攏成一張圖——從「你們要轉向我」（1:3）走到「歸耶和華為聖」（14:20-21），再看一次那位回到錫安、住在祂百姓當中的主。"

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

echo "🔨 Generating PDF with zechariah.latex template..."

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
