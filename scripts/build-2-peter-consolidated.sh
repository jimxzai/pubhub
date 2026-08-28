#!/bin/bash

# 2 Peter PDF Builder - CONSOLIDATED 2026 EDITION
# = preface + orientation (overview / position / knowledge spine / systematic
#   reception) + 3 chapters + 卷末 (day of eternity) + afterword
# Sources from books/bible/2-peter/ (老弟兄 methodology + MacArthur + Morgan,
# CUV scripture). 2 Peter is a short 3-chapter epistle — no multi-volume division,
# modeled primarily on scripts/build-titus-consolidated.sh, with the fuller
# front/back-matter framework (preface, position essay, knowledge spine,
# systematic reception, bridge/afterword chapters) assembled the way
# scripts/build-gospel-of-luke-consolidated.sh does it via add_front().
# Uses templates/pdf/2-peter.latex (Deep Purple Knowledge/Warning theme)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/2-peter"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/2-peter-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/2-peter-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/2-peter.latex"

echo "=========================================="
echo "📖 2 Peter PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "彼得後書研讀"
subtitle: "2 Peter Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年8月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **老弟兄查經方法論之應用**（本書無對應之老弟兄彼得後書逐節查經筆記原始記錄，詳見各章誠實說明）

  • **John MacArthur** — 逐節解經 (gty.org)

  • **G. Campbell Morgan** — *The Living Messages of the Books of the Bible*

  **成長 = 恩典 + 知識**

  「你們卻要在我們主救主耶穌基督的恩典和知識上有長進。」（彼後 3:18）

  **經文版權聲明 (Scripture Copyright Notices)**

  2026 年 8 月 · 初版。本版為教會內部贈閱版（非賣品）；公開發行時另行申請 ISBN。

  中文經文引自《聖經》和合本（1919），屬公有領域。

  Scripture quotations marked (ESV) are from the ESV® Bible
  (The Holy Bible, English Standard Version®), © 2001 by Crossway,
  a publishing ministry of Good News Publishers. Used by permission.
  All rights reserved.

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
    # [0-9][0-9:-]* handles both bare verse numbers (^12^) and ranges/verse
    # refs with hyphens or colons (^24-25^, ^1:19^) — a bare-digit-only
    # pattern silently leaves those carets as literal text and breaks xelatex.
    # Trailing {} after \textsuperscript{} is load-bearing, not cosmetic: a
    # verse-superscript digit landing directly against a following \textbf{
    # with no separator confuses ucharclasses' Han-transition hooks and
    # silently strips bold from the whole \textbf{} span (root-caused via
    # xelatex repro — the digit-to-Han script-class boundary coincides with
    # the \textbf group's opening brace). The empty group breaks that
    # coincidence with no visible spacing effect.
    tail -n +8 "$f" | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}{}/g' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Like add_file, but marks the file's first H1 unnumbered so front/back-matter
# chapters (preface, overview, position essay, knowledge spine, bridge,
# afterword) don't consume chapter numbers — the 3 content chapters then
# number 1..3, matching 2 Peter itself.
add_front() {
    local f="$1"
    [ -f "$f" ] || { echo "❌ Missing file: $1 — aborting build"; exit 1; }
    echo "  Adding (unnumbered): $(basename "$f")"
    tail -n +8 "$f" | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}{}/g' \
      | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}"; done=1 } } {print}' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Volume divider: a part-title page, matching build-gospel-consolidated.sh's
# add_volume (same two-arg form; John's 3-row table form is specific to its
# 00a-revelation-order.md and has no 2 Peter equivalent).
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
# 卷首 · 定位 — orientation: overview, position, knowledge spine
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這幾章：概覽、正典位置、知識的骨幹。"

add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-2peter-position.md"
add_front "$INPUT_DIR/00b-knowledge-spine.md"

# 全書領受總綱——老弟兄查經法 (Systematic Reception)
# The study file has no YAML frontmatter and its own first line is already
# an H1, so it is not run through add_file/add_front: demote its headings
# one level and give it a wrapper H1 of its own instead.
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

# ============================================================
# 正文 · 三卷
# ============================================================
add_volume "卷一 · 真知識的根基 (The Foundation of True Knowledge) · 1:1-21" \
    "美德的階梯、登山變像的見證、先知預言的確據——認識，是一切的起點。"
add_chapter 01

add_volume "卷二 · 假教師的警告 (The Warning Against False Teachers) · 2:1-22" \
    "審判是確定的，但神知道怎樣搭救敬虔的人。"
add_chapter 02

add_volume "卷三 · 主的日子 (The Day of the Lord) · 3:1-18" \
    "一日千年，主必再來——在恩典和知識上有長進，直到永恆的日子。"
add_chapter 03

# ============================================================
# 卷末 · 永恆的日子 (The Day of Eternity)
# ============================================================
add_volume "卷末 · 永恆的日子 (Toward the Day of Eternity)" \
    "從創世記到啟示錄，一封將盡的遺言把讀者的眼目再一次帶回基督。"
add_front "$INPUT_DIR/99-day-of-eternity.md"

# ============================================================
# 附錄 · 索引與參考資料
# ============================================================
add_volume "附錄 (Appendices)" \
    "經文與主題索引、參考資料——供查閱、跨章對照，並如實交代每一處引句的查證方式。"
add_front "$INPUT_DIR/98-appendix-indices.md"
add_front "$INPUT_DIR/99-appendix-references.md"

# 跋 — afterword. Last content file: no trailing \newpage (the template's
# closing matter opens its own page; a trailing break here yields a
# header-only blank page whenever the afterword happens to fill its final
# page exactly).
[ -f "$INPUT_DIR/999-afterword.md" ] || { echo "❌ Missing file: $INPUT_DIR/999-afterword.md — aborting build"; exit 1; }
echo "  Adding (unnumbered): 999-afterword.md"
tail -n +8 "$INPUT_DIR/999-afterword.md" \
  | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}"; done=1 } } {print}' >> "$COMBINED_MD"
((chapter_count++))

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters/sections)"
echo ""

# Convert markdown **bold** to \textbf{} inside any custom span macro the
# template defines for speaker tags. 2-peter.latex currently defines no such
# macro (no \paul{} or \jesus{} usage — the epistle quotes no words of Jesus
# directly and has no narrator/speaker markup), so there is nothing to
# convert here. If a future revision of templates/pdf/2-peter.latex adds a
# custom span macro (check \newcommand{\<name>}[1]{...} near the color
# definitions), port the conversion block from build-titus-consolidated.sh
# using that macro's name.

# Wrap Greek Unicode runs in {\greekfont ...} explicitly, instead of relying
# on ucharclasses' automatic per-character script detection. IMPORTANT —
# do not "simplify" this back to ucharclasses: ucharclasses' automatic
# hooking silently strips \textbf bold from Scripture quotes the moment
# ANY other package that hooks font/box machinery is also loaded (hyperref,
# eso-pic, pgfornament each independently trigger it — root-caused via a
# minimal xelatex reproduction; hyperref cannot be dropped, so ucharclasses
# had to go instead). This manual wrap is immune to that conflict because
# it's a single explicit group, not a per-character automatic hook — and it
# safely nests inside an existing \textbf{...} when a bold span contains
# Greek, since \greekfont now has a registered BoldFont so the surrounding
# bold series is honored rather than silently dropped.
#
# ROOT CAUSE of the previous cascading-corruption bug (finally isolated):
# it was never about headings/blockquotes/bold-spans/table-cell width
# measurement — it was pandoc itself. Pandoc's markdown reader escapes a
# literal "{" / "}" typed in prose to "\{" / "\}" in the LaTeX output
# UNLESS it's inside a recognized raw-TeX construct. So a plain
# "{\greekfont TEXT}" written straight into the markdown source came out
# as "\{\greekfont TEXT\}" — an UNSCOPED \greekfont with no real group to
# close it, which then applied to every character until some unrelated
# brace elsewhere in the document happened to close it, corrupting
# everything in between (confirmed via `echo '{\greekfont x}' | pandoc
# -f markdown -t latex`, which reproduces the escaped output exactly).
# The fix is pandoc's raw_attribute extension (on by default in this
# project's `markdown-superscript-subscript` format): wrapping the whole
# group in a backtick code span tagged `{=latex}` passes it through
# byte-for-byte, braces included. Verified safe in prose, headings,
# blockquotes, **bold** spans, and both empty and mixed-content table
# cells — no context-based exclusions are needed any more.
echo "Wrapping Greek Unicode runs in {\\greekfont ...}..."
COMBINED_MD_PATH="$COMBINED_MD" python3 <<'PYEOF'
import os, re

path = os.environ['COMBINED_MD_PATH']
with open(path, encoding='utf-8') as f:
    text = f.read()

# Greek and Coptic (U+0370-03FF) + Greek Extended / polytonic (U+1F00-1FFF):
# a run of Greek letters, optionally followed by more single-space-separated
# Greek runs, so a multi-word phrase ("εἰς ἡμέραν αἰῶνος") wraps as ONE group
# instead of three, without swallowing the space before/after the phrase.
greek_run = re.compile(r'[Ͱ-Ͽἀ-῿]+(?: [Ͱ-Ͽἀ-῿]+)*')

def wrap(m):
    return '`{\\greekfont ' + m.group(0) + '}`{=latex}'

wrapped_count = [0]
def wrap_and_count(m):
    wrapped_count[0] += 1
    return wrap(m)

new_text = greek_run.sub(wrap_and_count, text)
with open(path, 'w', encoding='utf-8') as f:
    f.write(new_text)
print(f"  Wrapped {wrapped_count[0]} Greek run(s)")
PYEOF

echo "🔨 Generating PDF with 2-peter.latex template..."

pandoc "$COMBINED_MD" \
  -o "$OUTPUT_PDF" \
  --pdf-engine=xelatex \
  --template="$TEMPLATE" \
  --from=markdown-superscript-subscript \
  --toc \
  --toc-depth=1 \
  --top-level-division=chapter
  # Note: template hardcodes \setcounter{tocdepth}{0} directly (~line 520),
  # so a `-V tocdepth=0` pandoc flag here would be a no-op — omitted.

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ PDF generated: $OUTPUT_PDF ($(du -h "$OUTPUT_PDF" | cut -f1))"
else
    echo "❌ PDF generation failed"
    exit 1
fi
