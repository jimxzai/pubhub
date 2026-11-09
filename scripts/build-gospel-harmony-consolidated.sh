#!/bin/bash

# Gospel Harmony PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview / 神的總計劃 / 耶穌的世界 / 序言) + 九卷 37 站 + 附錄 + 跋
# Uses templates/pdf/gospel-harmony.latex (Royal/Shepherd/Glory theme, red-letter
# words of Jesus). Modelled on scripts/build-job-consolidated.sh.
#
# Chapter files are unchanged: 01..37-*.md are the 37 stations. Front/back
# matter files that do not exist yet are skipped silently (add_front returns
# early), so the build works while the book is still being written.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/gospel-harmony"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/gospel-harmony-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/gospel-harmony-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/gospel-harmony.latex"

echo "=========================================="
echo "✝️  Gospel Harmony PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "耶穌基督完整生平"
subtitle: "The Complete Life of Jesus Christ — A Gospel Harmony"
author: "PubHub 三書精讀系統"
date: "2026年11月"
publisher: "三書精讀出版系統"
copyright: |
  **耶穌基督完整生平** (The Complete Life of Jesus Christ — A Gospel Harmony)

  三書精讀出版系統 · 四福音合參

  初版　2026 年 11 月

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

# Front/back matter: same as add_file but marks the H1 {.unnumbered}. Without
# this LaTeX numbers EVERY chapter sequentially, so the preface, orientation
# chapters and volume dividers would consume numbers and the book's own 站 1
# would come out as LaTeX chapter N+1 — two conflicting numbers on one TOC line.
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
    # %b (not %s) for the description: volume descriptions carry a literal
    # \n>\n> to open a second blockquote paragraph (the 啟示的次序 marker).
    # printf only expands escapes inside the FORMAT string, so with %s those
    # arrive in the markdown as the two characters \ and n and xelatex dies on
    # "Undefined control sequence \n".
    printf '# %s {.unnumbered}\n\n> %b\n' "$1" "$2" >> "$COMBINED_MD"
    if [ -n "$3" ]; then
        printf '\n| %s | %s |\n|---|---|\n' "$3" "$4" >> "$COMBINED_MD"
    fi
    printf '\n\\newpage\n\n' >> "$COMBINED_MD"
    echo "  --- $1"
}

# Append the file matching an exact chapter filename.
add_chapter() {
    add_file "$INPUT_DIR/$1"
}

# The index appendix is generated from the chapters' 參照行 at build time; its
# own note says so, so regenerate first to make that claim true of this PDF.
echo "🔄 Regenerating indices from chapter sources..."
python3 "$SCRIPT_DIR/gen-gospel-harmony-scripture-index.py" --write || exit 1
python3 "$SCRIPT_DIR/gen-gospel-harmony-word-index.py" --write || exit 1
echo ""

# 前言 — preface
add_front "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位 — orientation: overview, God's plan, Jesus' world, prologue
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這幾章：全書地圖、神的總計劃（六十六卷的七步，四福音站在第六步）、耶穌的世界（四百年靜默之後），以及約翰福音的序言——太初有道。"

add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-gods-plan.md"
add_front "$INPUT_DIR/00b-world-of-jesus.md"
add_front "$INPUT_DIR/00-prologue-logos.md"

# ============================================================
# 正文 · 九卷 · 37 站
# The order statements below are the ones in 00a-gods-plan.md §五 (the
# authoritative table); keep the two in step.
# ============================================================
add_volume "卷一 · 道成肉身 (The Incarnation) · 站 1–3" \
    "本卷收站 1–3。\n>\n> **啟示的次序·第六步**：神先說話，天使先對卑微的人說，王先睡在馬槽——道成肉身是從最小處開始的。"
for f in 01-angelic-announcements.md 02-bethlehem-night.md 03-childhood-years.md; do
    add_chapter "$f"
done

add_volume "卷二 · 預備與呼召 (Preparation and Calling) · 站 4–5" \
    "本卷收站 4–5。\n>\n> **啟示的次序·第六步**：先有預備的聲音，後有受膏的人；先受試探，後呼召人。王的事工從曠野開始，不從宮殿開始。"
for f in 04-wilderness-preparation.md 05-first-disciples.md; do
    add_chapter "$f"
done

add_volume "卷三 · 初期事工：彰顯與更新 (Early Ministry) · 站 6–10" \
    "本卷收站 6–10。\n>\n> **啟示的次序·第六步**：先有記號，後有潔淨，再有重生——祂先彰顯榮耀，才更新人與殿。"
for f in 06-cana-wedding.md 07-temple-cleansing.md 08-nicodemus.md \
         09-samaritan-woman.md 10-healing-miracles.md; do
    add_chapter "$f"
done

add_volume "卷四 · 國度的憲章與記號 (Charter and Signs) · 站 11–14" \
    "本卷收站 11–14。\n>\n> **啟示的次序·第六步**：王先說話，才行神蹟，最後解釋自己就是那糧。"
for f in 11-sermon-on-mount.md 12-feeding-five-thousand.md \
         13-walking-on-water.md 14-bread-of-life.md; do
    add_chapter "$f"
done

add_volume "卷五 · 光與牧者：衝突加深 (Light and Shepherd) · 站 15–19" \
    "本卷收站 15–19。\n>\n> **啟示的次序·第六步**：光先來，衝突隨光而來；最大的記號，也成了定意殺祂的導火線。"
for f in 15-feast-tabernacles.md 16-man-born-blind.md 17-good-shepherd.md \
         18-lazarus.md 19-parables-kingdom.md; do
    add_chapter "$f"
done

add_volume "卷六 · 定意上耶路撒冷 (Set Toward Jerusalem) · 站 20–24" \
    "本卷收站 20–24。\n>\n> **啟示的次序·第六步**：祂不是被帶往耶路撒冷，是自己定意去。"
for f in 20-transfiguration.md 21-rich-young-ruler.md 22-triumphal-entry.md \
         23-temple-cleansing.md 24-olivet-discourse.md; do
    add_chapter "$f"
done

add_volume "卷七 · 樓上與園中 (The Upper Room and the Garden) · 站 25–29" \
    "本卷收站 25–29。\n>\n> **啟示的次序·第六步**：被捉拿之前，先把門徒交託給父。"
for f in 25-last-supper.md 26-upper-room-discourse.md 27-high-priestly-prayer.md \
         28-gethsemane.md 29-trial.md; do
    add_chapter "$f"
done

add_volume "卷八 · 十架與復活 (The Cross and the Resurrection) · 站 30–34" \
    "本卷收站 30–34。\n>\n> **啟示的次序·第六步**：十架不是計劃的失敗，是計劃的中心。"
for f in 30-crucifixion.md 31-burial.md 32-resurrection.md \
         33-appearances.md 34-ascension.md; do
    add_chapter "$f"
done

add_volume "卷九 · 教會與再來 (The Church and the Return) · 站 35–37" \
    "本卷收站 35–37。\n>\n> **啟示的次序·第七步**：祂先差遣，後同在，最後親自回來與人同住。"
for f in 35-pentecost.md 36-revelation-letters.md 37-revelation-return.md; do
    add_chapter "$f"
done

# ============================================================
# 跋 — afterword (skipped silently until written)
# ============================================================
add_front "$INPUT_DIR/999-afterword.md"

# ============================================================
# 附錄 — bibliography and indices. The index goes last in a printed book.
# 98-appendix-indices.md is generated above, so it always exists; the
# references appendix is owner-written and may not exist yet.
# ============================================================
add_volume "附錄 (Appendices)" \
    "參考資料、站次一覽與經文索引——各章正文所指的「卷末附錄」即此。"
add_front "$INPUT_DIR/99-appendix-references.md"
add_front "$INPUT_DIR/98-appendix-indices.md"
add_front "$INPUT_DIR/98b-appendix-word-index.md"

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters)"
echo ""
echo "🔨 Generating PDF with gospel-harmony.latex template..."

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
