# 約翰一書 校對神輪 — proofreader brief

Repo: /Users/jimxiao/Documents/GitHub/pubhub   Book: books/bible/john1   Built PDF: output/john1-consolidated.pdf

## The one rule
不要相信本書任何一句「已核對」「逐字相符」「105/105」「19/19」的聲明——這些聲明本身可能是假的。就當作你是第一個看到這份書稿的人，向一手來源重新取證。
**REPORT ONLY. Do not edit any file.** The coordinator decides what to change. Do not invent problems to look useful; "no defect found" is a valid result for a category.

## Primary sources (local copies in books/bible/john1/.sources/ — but spot-check a few against the live web too)
- CUV: bible.fhl.net JSON `https://bible.fhl.net/json/qb.php?chineses=<URL-encoded 書卷 e.g. 約一 / 約 / 創>&chap=N&sec=N&version=unv&gb=0` (use curl --max-time 30). House style converts 裡→裏 and drops the space before 神; 「─」 dashes as fhl prints them.
- NASB 1995: biblehub.com/nasb/1_john/N.htm (no underscore = 1995)
- Augustine NPNF¹ 7: newadvent.org/fathers/1702NN.htm ; Calvin: .sources/calvin-1john.txt (CCEL calcom45) ; Morgan: .sources/morgan-letters-of-john.txt (pp. 175-195, page = running header) ; MacArthur: .sources/gty/62-N.txt (also live https://www.gty.org/library/sermons-library/62-N) ; Westcott: .sources/westcott-epistles-st-john-1892.txt ; Irenaeus/Polycarp/Eusebius: .sources/irenaeus-*.txt, nadv-*.txt ; SBLGNT: .sources/sblgnt-1john.txt / sblgnt-1jn-morph.txt
- 老弟兄 quote whitelist: .claude/skills/ask-elder-wong/references/voice.md

## Defect classes to hunt (each has slipped past every script in this repo before)
1. Chinese Scripture inside 「」 in PROSE (not the ## 經文 block) that is reworded, truncated wrongly, has a wrong verse address, or inverts meaning. Check EVERY 「」 that claims to be Scripture.
2. ## 經文 blocks: re-diff CUV and NASB against the live/primary text (do not reuse anyone's earlier diff).
3. Counts and numbers that don't survive counting (「出現N次」「三次」「六次」「全書N次」, verse counts, dates, page numbers). Count yourself.
4. Commentary: a quote under the wrong commentator; a lead-in summary that misstates what the quoted author actually argues (read the surrounding paragraph in the source); a locator (Homily N.§, page, verse, sermon code/title) that is wrong.
5. Historical/textual claims (Cerinthus, Polycarp, Papias, Comma Johanneum, manuscript facts, Greek grammar claims, "only in NT" claims) — verify or flag as unsupported.
6. Internal contradictions: one chapter vs another, chapter vs front matter (00-overview, 00a, 00c, elder-wong-systematic-study), and the build script's YAML / volume dividers (scripts/build-john1-consolidated.sh) and template front pages (templates/pdf/john1.latex lines ~500-840: cover, frontispiece, title, closing page) — these are part of the book though not in books/.
7. Editing artifacts printed as text (English left mid-sentence, notes-to-self, broken markup), and anything only visible in the PDF (use pdftotext / pdftoppm on output/john1-consolidated.pdf to spot-check pages for your files).
8. 老弟兄: any 「」 sentence attributed to 老弟兄/黃長老 not in the whitelist or a cited repo file.
9. Chinese prose quality: AI filler, empty jargon, awkward or ungrammatical Chinese, 什麼/裡 instead of 甚麼/裏.

## Report format
For each finding: file:line — class # — what the book says — what the source says (with URL/path) — suggested fix — severity (critical = false Scripture/false quote/false fact; major = wrong locator/contradiction/miscount; minor = style).
End with a per-class tally, including classes where you found nothing.
