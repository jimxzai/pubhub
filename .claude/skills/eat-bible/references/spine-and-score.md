# eat-bible — Spine and score: what the machine cannot check

Loaded on demand from `SKILL.md`. Read this **before starting work on a book**,
and again before declaring one finished. The rest of this skill answers
*"is it correct, and does it build?"*. This file answers the two questions
that decide whether the book is worth building:

1. **Does it have a spine?** — does the book say something, in an order a
   reader can follow, and can the reader see that order from any page?
2. **Where is it on the ladder?** — score it, let the score name the next
   piece of work, re-score. Don't polish at random.

---

## Why this file exists

The Job volume, 2026-09-05: every lint clean, every citation checked, the
ledger check green, a full driver run passing, 359 pages, scored **9.6/10**
on the nine-item house rubric.

It was still missing God's side of the book. Nowhere did it say in what order
God reveals Himself in Job, or why that order. A reader could finish the whole
volume without ever being told where it was going. **The rubric did not have a
row for that, so nine rounds of scoring never asked.**

The same hole was already sitting in books treated as finished. Run
`scripts/check-book-spine.py <dir> --brief` across the shelf and look: Isaiah
closed 0 of 26 chapters by returning to Christ; Romans located the reader in
its argument in 0 of 16; even gospel-of-john, which is 21/21 on both
per-chapter checks, carried the spine on 0 of its 5 part dividers.

**On the first survey, of 33 books none passed all four checks.** Within a
day that was 4 of 33 (job, joshua, judges, ruth) — the gap is cheap to close
once you can see it. This is not a backlog to feel bad about; it is the
single highest-value thing available to do to this shelf, and it is now one
command to find.

So the rubric gets a tenth row, and the spine gets a script.

---

## Part 1 — The spine

### What a spine is

Not the table of contents. Not the chapter list. The spine is the answer to
**"what is God doing across this book, in what order, and why that order?"**

Two different lines, and a book needs both:

| Line | Question it answers | Job's example |
|---|---|---|
| **人的軌跡** | What happens to the person? | 1:21 → 13:15 → 19:25 → 42:5 |
| **神的次序** | In what order does God reveal Himself? | 天上先判決（約伯終身不知）→ 三十五章沉默 → 開口卻只發問 → 平反排在最後 |

Most books in this repo had the first and were missing the second. The second
is the one that makes a book preach rather than inform, because the *order* is
itself the message: God's silence is not absence but waiting; He replaces Job's
question rather than answering it; vindication comes last, so what Job receives
first is God rather than his reputation.

### The four places a spine has to be visible

A spine written once in the front matter is not a spine — the reader has
forgotten it by part five. `scripts/check-book-spine.py` checks all four:

| Where | What it looks like | Model |
|---|---|---|
| **One orientation chapter** | States the order of revelation and God's plan | `job/00c-revelation-order.md`, `gospel-of-john/00a-revelation-order.md` |
| **Every part divider** | One line: 「啟示的次序·第 N 步」…, in the `add_volume` description | `scripts/build-job-consolidated.sh` |
| **Every chapter opening** | A 座標 line in 基督焦點 locating this chapter on the spine | any `job/NN-*.md` |
| **Every chapter close** | Returning to Christ — `ask-elder-wong` calls this 「永不缺席的句號」 | `job/30-job-repents.md` |

```bash
python3 scripts/check-book-spine.py books/bible/<dir>     # one book, with fixes suggested
python3 scripts/check-book-spine.py --all --brief         # the whole repo, one line each
```

### Finding a book's spine

Load `ask-elder-wong`'s `references/distillation.md` — that is the method.
The short form:

- **Find the author's own purpose statement** and reason backwards from it.
- **Count the repeated word.** Actually count it, don't estimate.
- **The section divisions are the revelation** — what changes between parts,
  and who is acting in each?
- **Where does the book land?** The last movement, not the first, is usually
  the point.
- For God's order specifically, ask: **when does God speak, when is He silent,
  and what does He do first, second, last?** Then ask why that order and not
  another. That question has produced the strongest material in this repo.

### Two rules that keep a spine honest

- **A spine is discovered, not imposed.** If the order you describe is not
  actually in the text, you have written a sermon outline and attached a book
  to it. Job's four movements are in the text; the claim that Job is a type of
  Christ is not, which is why this repo refuses it.
- **Never flatten a genuine tension to make the spine tidy.** Job 19:26's two
  readings, Job 42:6's translation dispute, Elihu's contested reputation — the
  spine has to be able to hold these open. When the Job volume was cut by 21%,
  the instruction to every agent included the list of tensions that must
  survive; they all did, and one got *clearer* for the trimming.

---

## Part 2 — The score

### The rubric

Ten rows, 0-10 each. Rows 1-9 are the house rubric used since Philemon;
row 10 is new (see above). Write the sheet to
`docs/scores/<slug>-<YYYY-MM-DD>.md`.

| # | 項目 | What a 10 looks like |
|---|---|---|
| 1 | 聖經引文準確度 | Every verse two-source verified; 做/作 and variant chars settled per verse |
| 2 | 體例一致性 | Every chapter on the 11-section template; naming and titles uniform |
| 3 | 排版與建置 | driver clean, 0 missing glyph, 0 overfull, fonts embedded, baseline recorded |
| 4 | 結構與邏輯連貫 | No chapter contradicts another; front matter agrees with the build script |
| 5 | 屬靈洞見（非常識） | Every 領受要點 is specific to its chapter; no sentence that could move to any other chapter |
| 6 | 注疏可查證性 | Every quoted sentence verbatim from a locatable source; ledger agrees with the book |
| 7 | 中英雙語完整度 | CUV + NASB 1995 parallel and equal; no verse present in one column and missing in the other |
| 8 | 引文格式規範 | Every citation gives version, volume, page/section — checkable by a reader |
| 9 | 讀者可用性 | Indices generated not hand-kept; a reader can find anything |
| **10** | **屬靈骨幹（啟示的次序）** | **`check-book-spine.py` clean: spine chapter, every divider, every chapter's coordinate and close** |

Score honestly. A 10 does not mean perfect; it means nothing left that this
project's standards can name. Say what is unfinished in a 「仍未完成」 section
and mark which items need the author's decision rather than another round.

### The maturity ladder

Each rung finds a class the rung below cannot see. This is the observed
sequence from the Job volume (8.0 → 9.0 → 9.4 → 9.6 → 9.7), and the classes
repeat across books.

| Rung | Round | What only this rung finds |
|---|---|---|
| 1 | **Build** | Structure exists, it compiles, citations are sourced but unverified |
| 2 | **Skill audit** | Ledger disagrees with the book; a skill's mandatory element missing wholesale (29 of 31 chapters lacked the required closing line) |
| 3 | **Proofread** | Fabricated Scripture in front matter; the copyright page contradicting the book's own honesty statement; editing artifacts printed as text; counts that don't survive counting |
| 4 | **Succinct** | The same point made 4-13 times per chapter; four tables of the same structure |
| 5 | **Spine** | God's order never stated; the book informs but does not lead anywhere |

**Do them in order.** Trimming before proofreading polishes errors; adding a
spine before trimming buries it. And do not stop at rung 3 because everything
is green — rungs 4 and 5 are invisible to every checker in this repo except
`check-book-spine.py`.

**Rung 4 does not only fail to find rung 5's defects — it creates them.**
Job's succinct pass deleted the 座標 line from 16 of 31 chapters. The
instruction was "make each point once per chapter", and a coordinate line
looks exactly like a repeat: it restates the book's structure, which the
front matter already gave. Two further scoring rounds passed over the loss
without noticing. Trimming is not lossless — it removes what is redundant
*within a chapter* and necessary *across the book*. **Re-run
`check-book-spine.py` after every succinct pass**, not only after a spine
pass.

The same round found four spellings of the coordinate label in use
(`全書座標`, `座標`, `全卷座標`, `全書骨幹座標`). All four satisfy the checker,
which matches on 座標 alone. Loose matching keeps a check honest across books
that word things differently, and the price is that consistency of wording
stays a human job.

### What no script will ever catch

Budget a human read for these. Each was found by reading, after all checkers
were green:

- A quoted verse whose final clause is not in the CUV at all
- A verse whose meaning is inverted (「未曾與眼睛立約」 where the text says he *did*)
- The build script's copyright page naming sources the preface says the book
  does not have — two files, each internally consistent, contradicting each other
- 「約伯記41章」 (it has 42), 「七個兒女」 (ten), 「三個朋友」 written as ten
- An English word left mid-sentence in Chinese prose; a 「需verify」 note printed
  as a heading
- A commentator's quote sitting under a different commentator's name
- One chapter's Scripture wrapped in italics, so it alone renders differently

The pattern: **every one of these is valid markdown that builds cleanly.**
The checkers verify correctness of form. Only reading verifies truth of content.
