#!/bin/bash

# Philippians PDF Builder - CONSOLIDATED 2026 EDITION
# = preface + orientation (overview / position / four-P spine) + 4 chapters
#   + 卷末 (closing) + afterword. Sources from books/bible/philipian/
# (老弟兄 methodology + MacArthur + G. Campbell Morgan, CUV+NASB scripture).
# Philippians is a short 4-chapter epistle — no multi-volume division,
# modeled on scripts/build-2-peter-consolidated.sh (same front/back-matter
# shape: preface, position essay, word-spine, systematic reception,
# closing reflection, afterword, assembled via add_front()/add_volume()).
# Uses templates/pdf/philipian.latex (Wine/Gold theme — kenosis to exaltation)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/philipian"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/philipian-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/philipian-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/philipian.latex"

echo "=========================================="
echo "📖 Philippians PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "腓立比書研讀"
subtitle: "Philippians Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年9月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **老弟兄查經方法論之應用**（本書無對應之老弟兄腓立比書逐節查經筆記原始記錄，詳見各章誠實說明）

  • **John MacArthur** — 逐節解經 (gty.org)

  • **G. Campbell Morgan** — *Living Messages of the Books of the Bible*（1912，"The Message of Philippians" 一章；另參 *The Analyzed Bible* 綱要）

  **存這樣的心思，直到主的日子**

  「你們當以基督耶穌的心為心。」（腓 2:5）

  **經文版權聲明 (Scripture Copyright Notices)**

  2026 年 9 月 · 初版。本版為教會內部贈閱版（非賣品）；公開發行時另行申請 ISBN。

  中文經文引自《聖經》和合本（1919），屬公有領域。

  Scripture quotations are from the New American Standard Bible®,
  Copyright © 1960, 1971, 1977, 1995, 2020 by The Lockman Foundation.
  All rights reserved.
---

HEADER

chapter_count=0

# Append one source file: strip its 7-line YAML front matter, convert ^n^ verse
# markers (including ranges like ^24-25^) to \textsuperscript, then start a
# new page.
add_file() {
    local f="$1"
    [ -f "$f" ] || { echo "❌ Missing file: $1 — aborting build"; exit 1; }
    echo "  Adding: $(basename "$f")"
    tail -n +8 "$f" | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}{}/g' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Like add_file, but marks the file's first H1 unnumbered so front/back-matter
# chapters (preface, overview, position essay, word spine, bridge, afterword)
# don't consume chapter numbers — the 4 content chapters then number 1..4,
# matching Philippians itself.
add_front() {
    local f="$1"
    [ -f "$f" ] || { echo "❌ Missing file: $1 — aborting build"; exit 1; }
    echo "  Adding (unnumbered): $(basename "$f")"
    tail -n +8 "$f" | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}{}/g' \
      | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}"; done=1 } } {print}' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Volume divider: a part-title page.
add_volume() {
    printf '# %s {.unnumbered}\n\n> %s\n' "$1" "$2" >> "$COMBINED_MD"
    printf '\n\\newpage\n\n' >> "$COMBINED_MD"
    echo "  --- $1"
}

# Append the first file matching a chapter-number prefix (e.g. 01-, 02-).
add_chapter() {
    local f
    for f in "$INPUT_DIR/$1-"*.md; do
        [ -f "$f" ] && { add_file "$f"; return 0; }
    done
    echo "❌ Missing chapter file for prefix '$1-' in $INPUT_DIR — aborting build"
    exit 1
}

# 前言 — preface
add_front "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位 — orientation: overview, position, four-P spine
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這幾章：概覽、正典位置、全書的骨幹——一個心思，四步展開。"

add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-philipian-position.md"
add_front "$INPUT_DIR/00b-four-p-spine.md"

# ============================================================
# 正文 · 四章
# ============================================================
add_volume "卷一 · 原則 (Principle) · 1:1-30" \
    "啟示的次序·第一步：活著就是基督，死了就有益處——這是一切的原則，也是全書的起點。"
add_chapter 01

add_volume "卷二 · 目的 (Purpose) · 2:1-30" \
    "啟示的次序·第二步：你們當以基督耶穌的心為心——降卑到十字架，升高到萬名之上，這是神給教會的目的與樣式。"
add_chapter 02

add_volume "卷三 · 竭力向前 (Pressing Forward) · 3:1-21" \
    "啟示的次序·第三步：忘記背後，努力面前，向著標竿直跑——認識基督為至寶，勝過一切。"
add_chapter 03

add_volume "卷四 · 追求 (Pursue) · 4:1-23" \
    "啟示的次序·第四步：凡是真實的、可敬的……這些事你們都要思念；我靠著那加給我力量的，凡事都能做。"
add_chapter 04

# ============================================================
# 卷末 · 存這樣的心思 (Have This Mind)
# ============================================================
add_volume "卷末 · 回望與站立 (Looking Back, and Standing Firm)" \
    "四章讀完了，先把全書的領受收攏成一張圖，再讓保羅最後的囑咐把眼目帶回基督。"

# 全書領受總綱——老弟兄查經法 (Systematic Reception).
# Placed here, not in 卷首, for the same reason as 2 Peter: it is a
# synthesis OF the four chapters, so reading it before them would ask the
# reader to digest conclusions about chapters not yet read.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——老弟兄查經法 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
    tail -n +2 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
else
    echo "❌ Missing file: $STUDY_FILE — aborting build"
    exit 1
fi

add_front "$INPUT_DIR/99-standing-firm.md"

# ============================================================
# 附錄 · 索引與參考資料
# ============================================================
add_volume "附錄 (Appendices)" \
    "經文與主題索引、參考資料——供查閱、跨章對照，並如實交代每一處引句的查證方式。"
add_front "$INPUT_DIR/98-appendix-indices.md"
add_front "$INPUT_DIR/99-appendix-references.md"

# 跋 — afterword. Last content file: no trailing \newpage (the template's
# closing matter opens its own page).
[ -f "$INPUT_DIR/999-afterword.md" ] || { echo "❌ Missing file: $INPUT_DIR/999-afterword.md — aborting build"; exit 1; }
echo "  Adding (unnumbered): 999-afterword.md"
tail -n +8 "$INPUT_DIR/999-afterword.md" \
  | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}"; done=1 } } {print}' >> "$COMBINED_MD"
((chapter_count++))

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters/sections)"
echo ""

# Wrap Greek Unicode runs in {\greekfont ...} explicitly, instead of relying
# on ucharclasses' automatic per-character script detection (same rationale
# as build-2-peter-consolidated.sh — see comments there for the fully
# root-caused explanation of why ucharclasses corrupts bold spans at scale,
# and why the raw_attribute {=latex} code-span wrap is required to survive
# pandoc's brace-escaping of literal "{"/"}" in markdown prose).
echo "Wrapping Greek Unicode runs in {\\greekfont ...}..."
COMBINED_MD_PATH="$COMBINED_MD" python3 <<'PYEOF'
import os, re

path = os.environ['COMBINED_MD_PATH']
with open(path, encoding='utf-8') as f:
    text = f.read()

# Some source chapters already hand-wrap a Greek run using the correct
# raw_attribute code-span form (`` `{\greekfont ΧΧΧ}`{=latex} ``) — a second,
# blanket regex pass over the WHOLE combined file would then match the Greek
# characters again, nested inside the existing wrap, producing
# `{\greekfont `{\greekfont ΧΧΧ}`{=latex}}`{=latex}` (mismatched braces,
# "Too many }'s" from xelatex). Protect any already-wrapped span first with a
# placeholder, run the blanket wrap on what's left, then restore.
already_wrapped = re.compile(r'`\{\\greekfont [^`]*?\}`\{=latex\}')
protected = []
def protect(m):
    protected.append(m.group(0))
    return f'\x00PROTECTED{len(protected) - 1}\x00'
text = already_wrapped.sub(protect, text)

greek_run = re.compile(r'[Ͱ-Ͽἀ-῿]+(?: [Ͱ-Ͽἀ-῿]+)*')

def wrap(m):
    return '`{\\greekfont ' + m.group(0) + '}`{=latex}'

wrapped_count = [0]
def wrap_and_count(m):
    wrapped_count[0] += 1
    return wrap(m)

new_text = greek_run.sub(wrap_and_count, text)

for i, span in enumerate(protected):
    new_text = new_text.replace(f'\x00PROTECTED{i}\x00', span)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_text)
print(f"  Wrapped {wrapped_count[0]} new Greek run(s); left {len(protected)} already-wrapped span(s) untouched")
PYEOF

echo "🔨 Generating PDF with philipian.latex template..."

source "$SCRIPT_DIR/lib/latex-check.sh"
LATEX_LOG="${OUTPUT_PDF%.pdf}-build.log"

pandoc "$COMBINED_MD" \
  -o "$OUTPUT_PDF" \
  --verbose \
  --pdf-engine=xelatex \
  --template="$TEMPLATE" \
  --from=markdown-superscript-subscript \
  --toc \
  --toc-depth=2 \
  --top-level-division=chapter > "$LATEX_LOG" 2>&1
PANDOC_EXIT=$?

latex_build_report "$PANDOC_EXIT" "$LATEX_LOG" "$OUTPUT_PDF" || exit 1
