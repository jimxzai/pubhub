#!/bin/bash

# Exodus PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine) + 全書領受總綱 + 七卷 40 章 + 卷末 + 跋
# Uses templates/pdf/exodus.latex (Blood/Sea/Glory theme, matching the Gospel
# of John / Acts of the Apostles / Isaiah / Job series standard: cover art,
# frontispiece)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/exodus"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/exodus-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/exodus-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/exodus.latex"

echo "=========================================="
echo "🔥 Exodus Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "出埃及記研讀"
subtitle: "Exodus Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年9月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **老弟兄查經法** — 整本聖經的脈絡領受

  • **John MacArthur** — 相關專題講章 (gty.org)

  • **G. Campbell Morgan** — 《Exposition on the Whole Bible》／《Living Messages of the Books of the Bible》(1912)

  **從為奴到同住：十災與逾越的羔羊、西奈之約、會幕的建造與耶和華的榮光**

  卷一：為奴之地與蒙召的僕人 (1-6章) | 卷二：十災與逾越的羔羊 (7-13章) | 卷三：過紅海與曠野路 (14-18章)
  卷四：西奈之約與律法 (19-24章) | 卷五：會幕的藍圖 (25-31章) | 卷六：金牛犢與立約的更新 (32-34章) | 卷七：建造與榮耀充滿 (35-40章)

  **經文版權聲明 (Scripture Copyright Notices)**

  本版為教會內部贈閱版（非賣品）；公開發行時另行申請 ISBN。

  中文經文引自《聖經》和合本（1919），屬公有領域。

  Scripture quotations marked (NASB) are from the NEW AMERICAN STANDARD
  BIBLE®, Copyright © 1960, 1962, 1963, 1968, 1971, 1972, 1973, 1975, 1977,
  1995 by The Lockman Foundation. Used by permission. www.Lockman.org.
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
    tail -n +8 "$f" | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Volume divider: a part-title page carrying the volume's theme.
# Front/back matter and volume dividers: same as add_file but marks the H1
# {.unnumbered}. Without this LaTeX numbers EVERY chapter sequentially, so the
# preface, orientation chapters and the seven volume divider pages consume
# numbers 1-9 and the book's own 第一章 comes out as LaTeX chapter 10 — the
# contents page then reads "10  第一章 · ...", two conflicting numbers on one
# line. Marking these unnumbered lets the 40 study units number 1-40,
# matching 第一章-第四十章. Same approach as build-job-consolidated.sh.
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
    # xelatex then dies on "Undefined control sequence \n". Same fix as
    # build-job-consolidated.sh.
    printf '# %s {.unnumbered}\n\n> %b\n' "$1" "$2" >> "$COMBINED_MD"
    # Optional 3rd arg: a full markdown table (header + rows) listing the
    # volume's chapters, so the divider page carries real structural content
    # instead of a title + one sentence floating over an otherwise blank page.
    if [ -n "$3" ]; then
        printf '\n%s\n' "$3" >> "$COMBINED_MD"
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
    "讀正文之前先讀這幾章：總覽、位置、骨幹。" \
    "| 章 | 內容 |
|---|---|
| 概覽 | 書卷簡介、核心經文、七卷四十章結構表 |
| 位置 | 出埃及記在摩西五經中的位置；新約如何反覆回到這卷書 |
| 骨幹 | 全書的神學脊柱：從「我要作你們的神」到「榮光充滿了帳幕」 |
| 領受總綱 | 依老弟兄查經方法，逐卷撮述全書的查經領受 |"

add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-exodus-position.md"
add_front "$INPUT_DIR/00b-presence-spine.md"

# Systematic reception — demote headings one level so it reads as one chapter.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
    tail -n +2 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 七卷 · 40 章
# ============================================================
add_volume "卷一 · 為奴之地與蒙召的僕人 (Bondage and the Called Deliverer) · 1-6章" \
    "以色列在埃及為奴受苦，神卻紀念祂與亞伯拉罕、以撒、雅各所立的約，親自呼召一個曾經逃亡的牧羊人回去領百姓出來。\n>\n> **啟示的次序·第一步（起點）**：救贖尚未開始，神已經定意「我要以你們為我的百姓，我也要作你們的神」（6:7）——同住的心意，比第一件神蹟還早。" \
    "| 章 | 標題 | 經文 |
|---|---|---|
| 1 | 為奴之地的興起 | 1:1-22 |
| 2 | 蒙拯救的嬰孩 | 2:1-25 |
| 3 | 焚而不燬的荊棘 | 3:1-22 |
| 4 | 神所賜的憑據 | 4:1-31 |
| 5 | 稻草與磚 | 5:1-23 |
| 6 | 神紀念祂的約 | 6:1-30 |"
for f in 01-rise-of-affliction.md 02-child-drawn-out.md 03-burning-bush.md \
         04-signs-and-excuses.md 05-straw-and-bricks.md 06-god-remembers-his-covenant.md; do
    add_chapter "$f"
done

add_volume "卷二 · 十災與逾越的羔羊 (Ten Plagues and the Passover Lamb) · 7-13章" \
    "耶和華一連九次審判埃及的假神，最終以逾越節的羔羊分別自己的百姓——救贖從一開始就是流血的救贖。\n>\n> **啟示的次序·第二步（脫離）**：第一步的應許開始兌現——不是靠百姓的功德，是靠塗在門框上的血（12:13）。神先救人脫離轄制，才能領人進入同住。" \
    "| 章 | 標題 | 經文 |
|---|---|---|
| 7 | 杖變蛇與血災 | 7:1-25 |
| 8 | 蛙災、蝨災、蠅災 | 8:1-32 |
| 9 | 畜疫、瘡災、雹災 | 9:1-35 |
| 10 | 蝗災與黑暗之災 | 10:1-29 |
| 11 | 長子之災的宣告 | 11:1-10 |
| 12 | 逾越節的羔羊 | 12:1-51 |
| 13 | 分別為聖與雲柱火柱 | 13:1-22 |"
for f in 07-staff-and-blood.md 08-frogs-gnats-flies.md 09-livestock-boils-hail.md \
         10-locusts-and-darkness.md 11-death-of-firstborn-announced.md 12-passover-lamb.md \
         13-consecration-and-pillar.md; do
    add_chapter "$f"
done

add_volume "卷三 · 過紅海與曠野路 (The Red Sea and the Wilderness Road) · 14-18章" \
    "紅海在百姓面前分開，摩西高唱得勝的歌；然而得勝之後立刻是曠野的乾渴與飢餓——神在路上供應糧食、水與智慧。\n>\n> **啟示的次序·脫離之後**：出了埃及不等於學會倚靠。神用糧、水、爭戰逐一操練百姓：祂不只救人一次，是天天供應，直到西奈山下。" \
    "| 章 | 標題 | 經文 |
|---|---|---|
| 14 | 紅海分開 | 14:1-31 |
| 15 | 摩西的凱旋之歌 | 15:1-27 |
| 16 | 天上降下的糧 | 16:1-36 |
| 17 | 磐石出水與亞瑪力之戰 | 17:1-16 |
| 18 | 葉忒羅的建議 | 18:1-27 |"
for f in 14-sea-divided.md 15-song-of-moses.md 16-bread-from-heaven.md \
         17-water-and-war.md 18-jethros-counsel.md; do
    add_chapter "$f"
done

add_volume "卷四 · 西奈之約與律法 (The Covenant at Sinai) · 19-24章" \
    "耶和華在西奈山上向全會眾顯現，賜下十誡與立約的律例——百姓在雷轟閃電中回答：凡耶和華所吩咐的，我們都必遵行。\n>\n> **啟示的次序·第四步（發展）**：脫離轄制的百姓，如今領受身分——「祭司的國度，聖潔的國民」（19:6）。律法緊接著恩典的宣告而來，不是換取恩典的條件。" \
    "| 章 | 標題 | 經文 |
|---|---|---|
| 19 | 耶和華降臨西奈山 | 19:1-25 |
| 20 | 十誡 | 20:1-26 |
| 21 | 律例：僕婢與人身傷害 | 21:1-36 |
| 22 | 律例：財產賠償與社會公義 | 22:1-31 |
| 23 | 律例：公正審判、節期與應許 | 23:1-33 |
| 24 | 立約的血與摩西上山 | 24:1-18 |"
for f in 19-lord-descends-on-sinai.md 20-ten-commandments.md 21-laws-on-servants-and-injury.md \
         22-laws-on-property-and-justice.md 23-laws-on-courts-and-feasts.md 24-blood-of-the-covenant.md; do
    add_chapter "$f"
done

add_volume "卷五 · 會幕的藍圖 (The Tabernacle Blueprint) · 25-31章" \
    "神吩咐摩西按著山上指示的樣式建造會幕——每一件器具、每一寸幔子，都是要在百姓中間預備一個可安居之處。\n>\n> **啟示的次序·第五步（高峰）**：全書骨幹在此揭曉底牌——「使我可以住在他們中間」（25:8）。前四步的一切，原來都是要走到這一句話。" \
    "| 章 | 標題 | 經文 |
|---|---|---|
| 25 | 約櫃、桌子、燈臺 | 25:1-40 |
| 26 | 帳幕的幔子與木板 | 26:1-37 |
| 27 | 燔祭壇與院子 | 27:1-21 |
| 28 | 祭司的聖衣 | 28:1-43 |
| 29 | 祭司的承接聖職 | 29:1-46 |
| 30 | 香壇、洗濯盆與膏油 | 30:1-38 |
| 31 | 比撒列、亞何利亞伯與安息日 | 31:1-18 |"
for f in 25-ark-table-lampstand.md 26-curtains-and-frames.md 27-altar-and-court.md \
         28-priestly-garments.md 29-ordination-of-priests.md 30-incense-basin-anointing-oil.md \
         31-bezalel-oholiab-and-sabbath.md; do
    add_chapter "$f"
done

add_volume "卷六 · 金牛犢與立約的更新 (The Golden Calf and the Renewed Covenant) · 32-34章" \
    "摩西還在山上，百姓已在山下鑄造金牛犢——約幾乎在頒布的當下就被踐踏；摩西為百姓代求，神卻願意更新祂的約。\n>\n> **啟示的次序·第六步（轉折）**：高峰之後立刻是墜落——但即使百姓親手打破了約，神的同在仍是摩西懇求、神也應允恢復的核心（33:14-15）。同住的心意沒有因背約而收回。" \
    "| 章 | 標題 | 經文 |
|---|---|---|
| 32 | 金牛犢 | 32:1-35 |
| 33 | 摩西懇求神的同在 | 33:1-23 |
| 34 | 立約的更新與摩西的榮光 | 34:1-35 |"
for f in 32-golden-calf.md 33-moses-pleads-for-gods-presence.md 34-covenant-renewed.md; do
    add_chapter "$f"
done

add_volume "卷七 · 建造與榮耀充滿 (Construction and the Filling Glory) · 35-40章" \
    "百姓甘心樂意地奉獻，巧匠按著吩咐的樣式建成會幕——全書在此抵達目的地：耶和華的榮光親自降下，充滿了帳幕。\n>\n> **啟示的次序·第七步（終點）**：從6:7的應許，到40:34的榮光——七步路走完，神拯救人的心意終於不再是言語，成了看得見、住得下的實際。" \
    "| 章 | 標題 | 經文 |
|---|---|---|
| 35 | 甘心樂意的奉獻 | 35:1-35 |
| 36 | 巧匠的工作與帳幕的建造 | 36:1-38 |
| 37 | 約櫃、桌子、燈臺、香壇的製作 | 37:1-29 |
| 38 | 燔祭壇、洗濯盆與院子的建造 | 38:1-31 |
| 39 | 祭司聖衣的完成與總數點核 | 39:1-43 |
| 40 | 會幕立起、榮光充滿 | 40:1-38 |"
for f in 35-willing-offering.md 36-skilled-work-begins.md 37-furniture-of-the-tent.md \
         38-altar-basin-and-court-built.md 39-priestly-garments-completed.md 40-glory-fills-the-tabernacle.md; do
    add_chapter "$f"
done

# ============================================================
# 卷末 · 從為奴到同住
# ============================================================
add_volume "卷末 · 從為奴到同住 (From Bondage to Dwelling)" \
    "全書從為奴之地的哀哭起頭，走過紅海、西奈與金牛犢的背約，最終停在雲彩與榮光——這條路沒有一步是繞過救贖走的。" \
    "| 段落 | 內容 |
|---|---|
| 神的帳幕在人間 | 出埃及記40章的雲彩，如何在約翰福音1:14、啟示錄21:3裏找到全書終點的完全實現 |
| 附錄一 | 經文與主題索引 |
| 附錄二 | 引用出處總表 |
| 跋 | 全書的收束與禱告 |"
add_front "$INPUT_DIR/99-god-with-us.md"

add_front "$INPUT_DIR/98-appendix-indices.md"
add_front "$INPUT_DIR/99-appendix-references.md"

# 跋 — afterword. Last content file: no trailing \newpage.
echo "  Adding (unnumbered): 999-afterword.md"
tail -n +8 "$INPUT_DIR/999-afterword.md" \
  | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}" ; done=1 } } {print}' >> "$COMBINED_MD"
((chapter_count++))

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters)"
echo ""
echo "🔨 Generating PDF with exodus.latex template..."

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
