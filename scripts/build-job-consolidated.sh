#!/bin/bash

# Job PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine) + 全書領受總綱 + 七卷 31 章 + 卷末 + 跋
# Uses templates/pdf/job.latex (Ash/Storm/Dawn theme, matching the Gospel of
# John / Acts of the Apostles / Isaiah series standard: cover art, frontispiece)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/job"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/job-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/job-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/job.latex"

echo "=========================================="
echo "🌫️  Job Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "約伯記研讀"
subtitle: "Job Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年9月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **貴格利一世** — 《約伯記倫理講疏》(Morals on the Book of Job)

  • **馬太·亨利** — 《聖經全書註釋》約伯記卷 (Commentary on the Whole Bible)

  • **G. Campbell Morgan** — 《The Analyzed Bible: The Book of Job》

  **從灰塵到黎明：公義人的試煉、三輪對話的激辯、耶和華從旋風中的回答**

  序幕與哀歌 (1-3章) | 第一輪對話：受苦的無辜 (4-14章) | 第二輪對話：惡人的結局 (15-21章)
  第三輪對話與智慧頌 (22-28章) | 約伯的終極申辯 (29-31章) | 以利戶的講論 (32-37章) | 耶和華的回答與結局 (38-42章)

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
# line. Marking these unnumbered lets the 31 study units number 1-31,
# matching 第一章-第三十一章. Same approach as build-isaiah-consolidated.sh.
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
    # xelatex then dies on "Undefined control sequence \n".
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
    "讀正文之前先讀這四章：全書地圖、約伯記在正典的位置、約伯這個人的軌跡，以及最要緊的一章——神在這卷書裏按甚麼次序顯明自己。"

add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-job-position.md"
add_front "$INPUT_DIR/00b-suffering-spine.md"
add_front "$INPUT_DIR/00c-revelation-order.md"

# Systematic reception — demote headings one level so it reads as one chapter.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
    tail -n +2 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 七卷 · 31 段
# ============================================================
# 卷一收 01-04 四章（伯 1-3）：序幕的散文（1-2章）與約伯的哀歌（3章）同屬「對話
# 尚未開始」的階段，這也是卷首各檔（00-overview 的全書結構表與七週讀經計劃、
# elder-wong-systematic-study 的分卷標題）一致採用的分法。第三輪校對發現本腳本
# 原將 04-jobs-lament.md（伯3）歸入卷二、並把兩卷標成 1-2章／3-14章，與卷首各檔
# 的 1-3章／4-14章互相矛盾——讀者會先讀到一張寫著「卷一 1-3章」的表，再翻到一頁
# 寫著「卷一 1-2章」的分卷扉頁。已改以卷首各檔的分法為準。
add_volume "卷一 · 序幕與哀歌 (Prologue and Lament) · 1-3章" \
    "苦難不是從人的罪開始，是從天上的一場對話開始——約伯自己始終不知情；等他開口，先出來的不是答案，是哀歌。\n>\n> **啟示的次序·第一步**：神先在天上為約伯說話（1:8、2:3），而約伯永遠聽不見。你的處境不等於神對你的評價。"
for f in 01-blameless-and-upright.md 02-wager-in-heaven.md 03-second-test.md \
         04-jobs-lament.md; do
    add_chapter "$f"
done

add_volume "卷二 · 第一輪對話：受苦的無辜 (First Cycle) · 4-14章" \
    "三個朋友輪流回應——第一輪的邏輯還算克制，卻已埋下日後尖銳的種子。\n>\n> **啟示的次序·第二步（沉默的開始）**：從這裏起，神三十五章不發一言。約伯在 9:33 伸手要第一樣他那個時代給不出的東西——一位能按手在神與人兩造之間的聽訟者。"
for f in 05-eliphaz-first-speech.md 06-friends-like-a-brook.md \
         07-bildad-tradition.md 08-job-contends-with-god.md 09-zophar-accusation.md \
         10-wisdom-is-with-me.md; do
    add_chapter "$f"
done

add_volume "卷三 · 第二輪對話：惡人的結局 (Second Cycle) · 15-21章" \
    "朋友們的話越說越重，全部收窄成同一個公式：惡人必遭報應——約伯的處境卻怎麼看都不合這個公式。\n>\n> **啟示的次序·沉默之中**：神仍然不說話。約伯卻在最黑的一刻伸手要第二樣——一位至近的救贖主（19:25）。"
for f in 11-eliphaz-fate-of-wicked.md 12-miserable-comforters.md 13-bildad-lamp-of-wicked.md \
         14-my-redeemer-lives.md 15-zophar-brief-joy.md 16-why-do-wicked-prosper.md; do
    add_chapter "$f"
done

add_volume "卷四 · 第三輪對話與智慧頌 (Third Cycle & Hymn to Wisdom) · 22-28章" \
    "第三輪對話漸漸散開、辯論難以為繼，卻在此處插入一首獨立的智慧頌——人能找到金銀，卻找不到智慧本身。\n>\n> **啟示的次序·沉默之中**：28 章先給出答案「敬畏主就是智慧」，但那還只是道理；要等到 42 章，約伯才真正遇見。道理在前，遇見在後，次序不能顛倒。"
for f in 17-eliphaz-final-accusation.md 18-longing-for-gods-presence.md \
         19-bildad-and-jobs-reply.md 20-hymn-to-wisdom.md; do
    add_chapter "$f"
done

add_volume "卷五 · 約伯的終極申辯 (Job's Final Defense) · 29-31章" \
    "約伯回顧從前蒙福的日子，對照如今被輕視的地步，最終立下一連串的誓言，宣告自己的清白。\n>\n> **啟示的次序·沉默的盡頭**：約伯伸手要第三樣——一位肯聽、肯回答的（31:35）。話說到這裏，他把能說的都說盡了。"
for f in 21-job-former-glory.md 22-job-present-disgrace.md 23-oath-of-innocence.md; do
    add_chapter "$f"
done

add_volume "卷六 · 以利戶的講論 (Elihu's Speeches) · 32-37章" \
    "一位年輕人打破沉默——他不站在三友的公式裡，卻先為神的公義辯護，再指向即將來臨的旋風。\n>\n> **啟示的次序·沉默的最後一段**：以利戶話沒說完，神就開口了（38:1）。人的話說盡之處，正是神開口之時。"
for f in 24-elihu-enters.md 25-elihu-gods-justice.md 26-elihu-gods-greatness.md; do
    add_chapter "$f"
done

add_volume "卷七 · 耶和華的回答與結局 (The LORD's Answer and Restoration) · 38-42章" \
    "耶和華終於開口，卻不回答「為什麼」，只是一連串的問題——約伯在問題中看見了祂，苦難也在看見裡得著了出路。\n>\n> **啟示的次序·第三與第四步**：神開口卻只發問——祂換掉了約伯的問題，比回答它更好；末了才是平反（42:7），而且是在約伯不再要求平反之後。先得著神，然後才得著名譽。"
for f in 27-lord-first-speech-creation.md 28-job-first-response.md \
         29-behemoth-and-leviathan.md 30-job-repents.md 31-restoration.md; do
    add_chapter "$f"
done

# ============================================================
# 卷末 · 從塵土到黎明
# ============================================================
add_volume "卷末 · 從塵土到黎明 (From Dust to Dawn)" \
    "全書從灰塵中的哀哭起頭，走過旋風中的沉默，最終停在黎明的恢復——這條路沒有一步是繞過苦難走的。"
add_front "$INPUT_DIR/99-restoration-and-hope.md"

# 跋 — afterword. Last content file: no trailing \newpage.
echo "  Adding (unnumbered): 999-afterword.md"
tail -n +8 "$INPUT_DIR/999-afterword.md" \
  | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}" ; done=1 } } {print}' >> "$COMBINED_MD"
((chapter_count++))

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters)"
echo ""
echo "🔨 Generating PDF with job.latex template..."

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
