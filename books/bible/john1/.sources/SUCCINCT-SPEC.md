# 約翰一書 精簡輪規格（同一個點全章只講一次）

Repo: /Users/jimxiao/Documents/GitHub/pubhub   Book: books/bible/john1
Pre-edit copies (for your own diffing): /private/tmp/claude-501/-Users-jimxiao-Documents-GitHub-pubhub-books-bible-john1/23dc1de0-f3c9-4514-a375-536c61104b67/scratchpad/pre-succinct/<file>

**The exemplar diff is the most precise statement of this spec:** books/bible/john1/.sources/succinct-exemplar-ch03.diff (chapter 3, done by the coordinator, movable prose 4228 → 3617 CJK = 86%). Read it first.

## Goal
Movable prose (everything except the ## 經文 section) to roughly **80–88%** of its current CJK count. 寧可不足，不可傷及內容: stopping at 88% with a reason is fine; going below 78% means real content went.

## Method (do in this order)
1. Read the whole chapter. Write down every point that is made more than once, and count how many times (save this list in your report).
2. Give each point ONE home section; elsewhere cut it or leave a pointer. Section duties:
   - 基督焦點: the theological center, once. Keep the 座標 line intact (wording may tighten, but keep 「啟示的次序·第N步——**…**」 and the link to previous/next step).
   - 背景: context needed before reading; not exegetical conclusions.
   - 原文研讀: what the Greek gives that the Chinese misses.
   - 領受要點: 3–5 points that differ from each other (merge overlaps, renumber).
   - 歷代注疏 Chinese lead-ins: positioning only (which verse, what question) — do NOT pre-paraphrase the quote.
   - 老弟兄查經: questions, not answers inside the questions; 全經連線 3–5 bullets; 今天的祭壇 keeps the three lines with trailing ` \`.
   - 生命應用 默想問題: ≤3, angles not already asked elsewhere in the chapter.
3. For understanding: split long sentences; conclusion first; delete phrases like 「值得注意的是」「這正是為甚麼」「換言之」; keep at most one bold sentence per subsection. A sentence that could be moved unchanged into another chapter should be cut or made specific.
4. Unsourced factual claims you notice (dates, biography, "only in NT", counts not verified in .sources/sblgnt-1jn-morph.txt) → cut or flag.

## Never touch (verify before finishing)
- 7-line YAML; `## 經文` section byte-identical; every `> "..."` quote line and every `> — ` attribution line identical (delete a whole quote+attribution only if it duplicates another quote — and then tell me; the ledger must be updated).
- Hymn lyrics, author/year lines; all 11 `## ` headings; the `**你看見耶穌了嗎**？` closing paragraph (may tighten, must remain and return to Christ).
- These deliberate tensions must survive, stated as open (do not resolve them): 1:8 vs 3:6/3:9; 2:2「普天下人的罪」scope; 2:27 vs teachers; 3:20 comfort vs warning; 5:6 water and blood (three readings, MacArthur rejects 19:34 and ordinances; Calvin links 19:34); 5:16「至於死的罪」; Comma Johanneum history (Westcott); Augustine 7.8 context.
- Any Chinese Scripture inside 「」 must stay a verbatim CUV substring (house style 裏).

## Self-check commands (paste results in report)
cd /Users/jimxiao/Documents/GitHub/pubhub
python3 - <<'PY'
import re,sys
f=sys.argv[1] if len(sys.argv)>1 else ''
PY
# write your own small python check: movable-CJK before/after; set(quote lines) equal; 經文 section equal; count of '^## ' == 11; '座標' and '你看見耶穌了嗎' present
python3 scripts/lint-chapter-markup.py books/bible/john1/<file>
python3 scripts/check-book-spine.py books/bible/john1
python3 scripts/verify-prose-citations.py books/bible/john1 --self 約一   # no NEW MISS in your file (known false positives: 00c:73, 03 μένω row, 06 παρρησία row)

## Report
File, movable CJK before→after (ratio), the repetition list with counts, what you cut/merged by section, anything flagged, self-check outputs.
Shell commands here sometimes hang (iCloud): use the Read/Edit/Write tools for files, never retry a hung command. Edit only your own chapter file.
