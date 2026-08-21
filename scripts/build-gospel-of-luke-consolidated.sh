#!/bin/bash

# Gospel of Luke PDF Builder - CONSOLIDATED 2026 EDITION
# = preface + 3-chapter orientation + 24 chapters in 5 parts + epilogue chapter + afterword
# Mirrors scripts/build-gospel-of-mark-consolidated.sh (Gospel of Mark).
# Uses the dedicated template: templates/pdf/gospel-of-luke.latex

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/gospel-of-luke"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/gospel-of-luke-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/gospel-of-luke-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/gospel-of-luke.latex"

echo "=========================================="
echo "📖 Gospel of Luke PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "路加福音研讀"
subtitle: "Gospel of Luke Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年8月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **老弟兄查經法** — 週四查經班領受的讀經進路

  • **John MacArthur** — 逐節解經 (gty.org)

  • **G. Campbell Morgan** — 解經王子 (*The Gospel According to Luke*, 1931)

  **完全人子——聖所的香壇、餅桌與燈臺**

  「人子來，為要尋找、拯救失喪的人。」——路加福音 19:10

  「定意向耶路撒冷去」（9:51）在前，「失而又得」（15:24, 32）在中，尋見在後

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
# markers to \textsuperscript, then start a new page.
add_file() {
    local f="$1"
    [ -f "$f" ] || return 0
    echo "  Adding: $(basename "$f")"
    # ^12^ and ^12:34^ both become superscripts; a bare-digit-only pattern
    # silently leaves chapter:verse markers as literal carets in the PDF.
    tail -n +8 "$f" | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Like add_file, but marks the file's first H1 unnumbered so front/back-matter
# chapters (preface, orientation, epilogue, afterword) don't consume chapter
# numbers — the 24 content chapters then number 1..24, matching Luke itself.
add_front() {
    local f="$1"
    [ -f "$f" ] || return 0
    echo "  Adding (unnumbered): $(basename "$f")"
    tail -n +8 "$f" | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}/g' \
      | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}"; done=1 } } {print}' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Part divider: a part-title page carrying the part's theme and,
# optionally, its place in the Holy Place picture / the book's spine /
# the harvest of the nations ($3 $4 $5; see 00a and 00c orientation chapters).
add_volume() {
    printf '# %s {.unnumbered}\n\n> %s\n' "$1" "$2" >> "$COMBINED_MD"
    if [ -n "$3" ]; then
        printf '\n| | |\n|---|---|\n| **聖所的位置** | %s |\n| **全書骨幹** | %s |\n| **萬邦的收成** | %s |\n' \
            "$3" "$4" "$5" >> "$COMBINED_MD"
    fi
    printf '\n\\newpage\n\n' >> "$COMBINED_MD"
    echo "  --- $1"
}

# Append the file matching an exact chapter-number filename prefix (e.g. 01-, 19-).
add_chapter() {
    local f
    for f in "$INPUT_DIR/$1-"*.md; do
        [ -f "$f" ] && { add_file "$f"; return 0; }
    done
}

# 前言 — preface (third station of the 66-volume prayer)
add_front "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位 — orientation: map, coordinates, method, spine
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這四章：地圖、座標、方法、骨幹。"

add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-son-of-man-position.md"
add_front "$INPUT_DIR/00b-systematic-reception.md"
add_front "$INPUT_DIR/00c-set-face-spine.md"

# ============================================================
# 正文 · 五部
# ============================================================
add_volume "第一部 · 預備——人子登場 (Preparation) · 1:5-4:13" \
    "四章，四首頌歌：先鋒的出生、道成肉身的降卑、家譜的追溯、曠野的得勝——完全人子真實地誕生、真實地長大、真實地受試探。" \
    "**香壇**——靜默四百年後，神在香煙裏重新開口" \
    "十二歲的少年：「我應當以我父的事為念」（2:49）" \
    "啟 5:9「你曾被殺，用自己的血……買了人來」"
for i in 01 02 03 04; do add_chapter "$i"; done

add_volume "第二部 · 加利利事工——人子的服事與身分顯明 (Galilean Ministry) · 4:14-9:50" \
    "拿撒勒會堂的宣告是憲章，此後六章一步步活出「傳福音給貧窮的人」——服事越展開，身分的追問也越逼近，直到9:20彼得的認信。" \
    "**燈臺初點**——「照亮外邦人的光」開始照進加利利" \
    "8:9「這到底是誰」→ 9:20「神所立的基督」" \
    "啟 7:9「從各國、各族、各民、各方來的」"
for i in 05 06 07 08 09; do add_chapter "$i"; done

add_volume "第三部 · 往耶路撒冷之旅——人子的道路 (The Way to Jerusalem) · 9:51-19:48" \
    "9:51「定意向耶路撒冷去」，一趟走了近十章的旅程；十五章的「失而又得」是這段路的心跳，19:10收束全部的目的句。" \
    "**香壇與餅桌交織**——恆切的禱告，一路的筵席" \
    "9:51「定意」→ 15:24「失而又得」→ 19:10「尋找、拯救失喪的人」" \
    "啟 19:9「被請赴羔羊之婚筵的有福了」"
for i in 10 11 12 13 14 15 16 17 18 19; do add_chapter "$i"; done

add_volume "第四部 · 耶路撒冷事工——人子與聖殿的對峙 (Jerusalem Ministry) · 20:1-21:38" \
    "榮進之後，路加獨記耶穌「看見城，就為它哀哭」——完全人子的眼淚，落在一座即將棄絕祂的城市上。" \
    "**燈臺照城**——光照到了拒絕光的地方" \
    "19:41「哀哭」——恩言與棄絕發生在同一座城" \
    "啟 21:23-24「羔羊就是城的燈；列國要在城的光裏行走」"
for i in 20 21; do add_chapter "$i"; done

add_volume "第五部 · 受難與復活——人子的十架與復活 (Passion & Resurrection) · 22:1-24:53" \
    "汗如血滴的禱告，十架上三句話——赦免、應許、交託，以馬忤斯路上的擘餅收束全書「路上」的意象。" \
    "**餅桌收束**——「他們的眼睛明亮了，這才認出他來」" \
    "23:43「今日你要同我在樂園裏了」——19:10的極致示範" \
    "啟 5:6「羔羊站立，像是被殺過的」"
for i in 22 23 24; do add_chapter "$i"; done

# ============================================================
# 卷末 · 望向那一頭 — the arc into Acts, Romans, Revelation
# ============================================================
add_volume "卷末 · 望向那一頭 (Toward the Nations)" \
    "路加福音自己不收尾——第一卷寫「開頭」，第二卷寫「繼續」。
>
> 他們就常在殿裏，稱頌神。（路 24:53）"
add_front "$INPUT_DIR/99-toward-the-nations.md"

# 附錄 — sources & verification ledger
add_front "$INPUT_DIR/99-appendix-references.md"

# 跋 — afterword (the ministry, the 66-volume prayer).
# Last content file: no trailing \newpage (the template backmatter opens
# its own page; a trailing break here yields a header-only blank page
# whenever the afterword happens to fill its final page exactly).
echo "  Adding: 999-afterword.md"
tail -n +8 "$INPUT_DIR/999-afterword.md" \
  | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}"; done=1 } } {print}' >> "$COMBINED_MD"
((chapter_count++))

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters)"
echo ""
echo "🔨 Generating PDF with dedicated template (gospel-of-luke.latex)..."

pandoc "$COMBINED_MD" \
  -o "$OUTPUT_PDF" \
  --pdf-engine=xelatex \
  --template="$TEMPLATE" \
  --from=markdown-superscript-subscript \
  --toc \
  --toc-depth=1 \
  --top-level-division=chapter \
  -V tocdepth=0

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ PDF generated: $OUTPUT_PDF ($(du -h "$OUTPUT_PDF" | cut -f1))"
else
    echo "❌ PDF generation failed"
    exit 1
fi
