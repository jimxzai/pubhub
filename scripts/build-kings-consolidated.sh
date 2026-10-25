#!/bin/bash

# 1 Kings PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine) + 全書領受總綱 + 八卷 24 單元 + 卷末 + 跋
# Uses templates/pdf/kings.latex (Cedar/Lamp/Whisper theme, matching the 1 Kings /
# Gospel of John / Isaiah / Job series standard: cover art, frontispiece)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/kings"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/kings-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/kings-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/kings.latex"

echo "=========================================="
echo "📖  1 Kings Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

# 98-appendix-indices.md's two generated tables carry a note saying they are
# built from the chapter files at build time. That note was false until these
# generators were wired in here (same gap as build-job-consolidated.sh once had).
echo "🔄 Regenerating indices from chapter sources..."
python3 "$SCRIPT_DIR/gen-kings-scripture-index.py" --write-units || exit 1
python3 "$SCRIPT_DIR/gen-kings-scripture-index.py" --write || exit 1
python3 "$SCRIPT_DIR/gen-kings-theme-index.py" --write || exit 1
echo ""

cat > "$COMBINED_MD" << 'HEADER'
---
title: "列王紀上研讀"
subtitle: "1 Kings Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年10月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **核心資源整合：**

  • **老弟兄查經法** — 方法性應用（本卷無以列王紀上為題的第一手教導）

  • **Matthew Henry** — *Commentary on the Whole Bible*, Vol. II（CCEL 全文）

  • **教父與公有領域注疏** — Augustine、Jerome、Chrysostom、Ambrose、Calvin、Farrar、Meyer 等（見卷末《附錄：引用出處總表》逐章說明）

  • **G. Campbell Morgan** — 《Exposition on the Whole Bible》王上各章概述；《The Analyzed Bible》卷一（1907）結構總覽

  • **John MacArthur** — gty.org 講章與網誌中順帶談到王上人物與事件的段落（逐章註明專論或順帶；逐字核對 gty.org 逐字稿）

  **經文版權聲明 (Scripture Copyright Notices)**

  本版為教會內部贈閱版（非賣品）；公開發行時另行申請 ISBN。

  中文經文引自《聖經》和合本（1919），屬公有領域。

  Scripture quotations marked (NASB) are from the NEW AMERICAN STANDARD
  BIBLE®, Copyright © 1960, 1962, 1963, 1968, 1971, 1972, 1973, 1975, 1977,
  1995 by The Lockman Foundation. Used by permission. www.Lockman.org.
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
# preface, orientation chapters and the nine volume divider pages consume
# numbers ahead of the book's own 第一章 — the contents page would then read
# two conflicting numbers on one line. Marking these unnumbered lets the 21
# study units number 1-21, matching 第一章-第二十一章. Same approach as
# build-job-consolidated.sh / build-isaiah-consolidated.sh.
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
    # %b (not %s) for the description: several volume descriptions carry a
    # literal \n>\n> to open a second blockquote paragraph (the 啟示的次序
    # marker). printf only expands escapes inside the FORMAT string, so with
    # %s those arrive in the markdown as the two characters \ and n and
    # xelatex then dies on "Undefined control sequence \n". Same convention
    # as build-job-consolidated.sh.
    printf '# %s {.unnumbered}\n\n> %b\n' "$1" "$2" >> "$COMBINED_MD"
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
add_front "$INPUT_DIR/00a-kings-position.md"
add_front "$INPUT_DIR/00b-lamp-spine.md"

# Systematic reception — demote headings one level so it reads as one chapter.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
    tail -n +2 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 八卷 · 24 個研讀單元
# ============================================================
add_volume "卷一 · 王位的交接 (The Succession) · 王上 1-2 章" \
    "亞多尼雅自立為王，所羅門在起誓之上登基；大衛臨終的遺命，與一連串清除政敵的行動。\n>\n> **啟示的次序·第一步**：神先把話交出去，王位後交——登基靠的是大衛指著永生的耶和華所起的誓（1:29-30）與那句「照著摩西律法上所寫的行」（2:3），不是派系，也不是武力。"
for f in 01-adonijah-and-solomon.md 02-davids-charge.md; do
    add_chapter "$f"
done

add_volume "卷二 · 智慧與國度 (Wisdom and the Kingdom) · 王上 3-4 章" \
    "基遍的夢與兩個婦人；一位智慧之王所治理的、多如海沙的國民。\n>\n> **啟示的次序·第二步（神對所羅門說話的第一次）**：先賜、再多賜、最後才說「若」——「你若效法你父親大衛……我必使你長壽」（3:14）；條件放在恩典的後面，不是前面。"
for f in 03-solomon-asks-for-wisdom.md 04-wise-kings-kingdom.md; do
    add_chapter "$f"
done

add_volume "卷三 · 殿 (The House) · 王上 5-8 章" \
    "備料與徭役、七年建殿、王宮與銅海、約櫃入殿、雲充滿，以及那篇有七項祈求的獻殿禱告。\n>\n> **啟示的次序·第三步（神對所羅門說話的第二次，建殿之中）**：殿還在蓋，祂已經說：「論到你所建的這殿，你若遵行我的律例……我必住在以色列人中間」（6:12-13）——殿不是保證，同在才是；獻殿時所羅門自己也問：「神果真住在地上嗎？……何況我所建的這殿呢？」（8:27）"
for f in 05-hiram-and-the-levy.md 06-building-the-temple.md \
         07-palace-and-furnishings.md 08-glory-fills-the-house.md \
         09-dedication-prayer.md; do
    add_chapter "$f"
done

add_volume "卷四 · 榮華與墮落 (Splendor and Decline) · 王上 9-11 章" \
    "二度顯現的警告、示巴女王的來訪、七百妃三百嬪與興起的敵人。\n>\n> **啟示的次序·第四步（第三次與第四次說話）**：第二次顯現是警告（9:2-9），第三次是判決（11:11-13）——條件句從「若」變成「既」；然而判決裏同一口氣留下一盞燈：「使我僕人大衛……長有燈光」（11:36）。"
for f in 10-second-appearance.md 11-queen-of-sheba.md \
         12-solomons-heart-turns.md; do
    add_chapter "$f"
done

add_volume "卷五 · 分裂 (The Division) · 王上 12-14 章" \
    "示劍之會、重軛與蠍子鞭；金牛犢取代聖殿；猶大來的神人與伯特利的老先知；亞希雅與示撒。\n>\n> **啟示的次序·第五步**：判決藉人的愚昧成就——「這事乃出於耶和華」（12:15）；從此神不再向任何君王顯現，祂的話改由先知的口傳來，王的詔令與神的話開始分家。"
for f in 13-shechem-and-the-yoke.md 14-golden-calves.md \
         15-man-of-god-and-old-prophet.md 16-ahijah-and-shishak.md; do
    add_chapter "$f"
done

add_volume "卷六 · 王朝更迭 (Dynasties Rise and Fall) · 王上 15-16 章" \
    "亞比央、亞撒與北國諸王：拿答、巴沙、以拉、心利、暗利，以及亞哈與耶洗別的登場。\n>\n> **啟示的次序·第六步**：話像時鐘，一個王朝一個王朝地兌現——15:29、16:12、16:34；北國的王朝靠刀劍更換，南國的王朝靠一盞燈留存（15:4）。"
for f in 17-abijam-asa-and-baasha.md 18-omri-ahab-and-jezebel.md; do
    add_chapter "$f"
done

add_volume "卷七 · 以利亞 (Elijah) · 王上 17-19 章" \
    "乾旱、撒勒法的寡婦、迦密山上的火、何烈山上微小的聲音。\n>\n> **啟示的次序·第七步**：神先把先知藏起來，再供養、再使死人復活、再降火；最後在何烈山，同一位神卻不在風、地震、火中，而在「微小的聲音」裏（19:11-12）。"
for f in 19-elijah-and-the-widow.md 20-mount-carmel.md \
         21-horeb-still-small-voice.md; do
    add_chapter "$f"
done

add_volume "卷八 · 亞哈的末日 (The End of Ahab) · 王上 20-22 章" \
    "亞蘭戰爭、拿伯的葡萄園、米該雅與一支隨便射出的箭。\n>\n> **啟示的次序·第八步**：憐憫與審判並行——勝利先賜給亞哈（20:13，28），然後責備（20:42；21:19），悔改被看見而審判延遲（21:29），最後那支「隨便」射出的箭，正應驗了「耶和華所說的話」（22:34，38）。"
for f in 22-ben-hadad-and-the-prophets.md 23-naboths-vineyard.md \
         24-micaiah-and-ahabs-death.md; do
    add_chapter "$f"
done

# ============================================================
# 卷末 · 燈與真光
# ============================================================
add_volume "卷末 · 燈與真光 (The Lamp, and the True Light)" \
    "列王紀上從「大衛的燈」開始盼望，到「羔羊為城的燈」得著回答。"
add_front "$INPUT_DIR/99-the-lamp.md"

# 附錄：引用出處總表——每一章都承諾「見卷末《附錄：引用出處總表》」。
add_front "$INPUT_DIR/99-appendix-references.md"

# 附錄：經文與主題索引——跨書經文索引由 scripts/gen-kings-scripture-index.py
# 於原始檔案自動生成，見該檔案與 98-appendix-indices.md 內的說明。
add_front "$INPUT_DIR/98-appendix-indices.md"

# 跋 — afterword. Last content file: no trailing \newpage.
echo "  Adding (unnumbered): 999-afterword.md"
tail -n +8 "$INPUT_DIR/999-afterword.md" \
  | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}" ; done=1 } } {print}' >> "$COMBINED_MD"
((chapter_count++))

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters)"
echo ""
echo "🔨 Generating PDF with kings.latex template..."

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
