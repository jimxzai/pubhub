---
name: eat-bible
description: Build and verify one of this repo's consolidated study-book PDFs (pandoc + xelatex + custom LaTeX templates under templates/pdf/). Use when asked to build, compile, run, render, or screenshot a book PDF, or to debug a PDF build failure (missing glyphs, LaTeX errors, font embedding, cover layout).
---

Paths below are relative to the repo root (`pubhub/`), not to this skill
directory — except `references/*.md`, which are beside this file.

**Reference files, loaded on demand:**

| File | Read it when |
|---|---|
| `references/gotchas.md` | A build fails, a page looks wrong, or you are about to edit a `templates/pdf/*.latex`. Every silent failure this repo has hit, plus the troubleshooting table. |
| `references/scripture-sources.md` | You are *writing* chapter markdown and need to verify a verse. ai-eden.com URL patterns, the RCUV caveat, rate limits, fallback disclosure. |

**The order that works.** Each step catches a class the next one cannot:

1. `scripts/lint-templates.sh` — static, ~1s, no build. Fix findings first;
   they are causes, the build only shows symptoms.
2. `.claude/skills/eat-bible/driver.sh <slug>` — builds, then checks the
   xelatex log, font embedding, and the baseline. Fails on *regression*.
3. Read the rendered PNG, and inspect the PDF as a published object
   (`pdfinfo`, TOC depth, `pdffonts`). Neither of the first two steps can
   see a page that merely *looks* wrong.
4. `driver.sh <slug> --record-baseline` — only after you have looked, and
   only for a change you intend.

Batch fixes have a poor record here: four attempts at re-proportioning
table columns barely moved the overfull count and twice made it worse.
What works is reading the pt figure xelatex reports and sizing from it.
After any batch change, rebuild everything and diff against the baselines;
if a number got worse, `git checkout` and rethink rather than layering
another guess on top.

## What this is

This repo has no server/GUI/REPL to launch — the "app" is a build
pipeline: `scripts/build-<book>-consolidated.sh` concatenates a book's
markdown source files (overview, systematic-study essay, chapters,
appendices) and pipes the result through `pandoc --pdf-engine=xelatex`
using a book-specific template in `templates/pdf/<book>.latex`. The
output is `output/<book>-consolidated.pdf`.

"Driving" it means: run the build, then actually check the PDF that
came out — `pandoc` exiting 0 does **not** mean the PDF is correct.
xelatex can emit a PDF after recoverable errors, glyphs can silently
render as blank boxes, and a full-bleed cover background can silently
fail to reach the page edge. The driver below checks all of that.

## Lint first — it's free

Before building anything, run the static check. It takes about a second,
needs no build, and catches six template bugs that are completely
silent at compile time (exit 0, no warnings, no errors):

```bash
scripts/lint-templates.sh              # every templates/pdf/*.latex
scripts/lint-templates.sh isaiah acts  # just these
```

It reports `template.latex:LINE` for each finding, grouped by kind, and
exits 1 if anything is found:

- `real-bold-face` — `BoldFont=<Family> Bold` silently flattens CJK bold
- `cjk-blind-monofont` — `\setmonofont{Menlo}` renders CJK as blank boxes
- `minipage-overflows-textblock` — a fixed-inch box printing into the margin
- `table-wider-than-textblock` — `p{}` widths exceeding the column budget
- `table-cell-wider-than-column` — the table total fits but one cell does
  not; a Greek or Latin word cannot break, CJK can
- `ucharclasses-dead-transition` — `\setTransitionsFor{Greek}` and friends
  are silent no-ops; the block names come from the installed
  `ucharclasses.sty`, not a hardcoded list
- `ucharclasses-two-way-clobber` — `\setTransitionsFor` sets both
  directions, so a later out-code overwrites an earlier in-code

**This script exists because prose didn't work.** `references/gotchas.md`
documented the BoldFont bug and told the reader to "check every
other `templates/pdf/*.latex` file for this exact pattern". Months
later 56 of 57 templates still had it, including 14 of the 17 buildable
books. An instruction to go grep is a task nobody performs; a script
runs every time. Repo-wide the count went 139 → 1 once each rule existed.

**For a template with no build script, use a probe document.** Feed a
markdown file containing CJK, full-width punctuation, Greek, Hebrew,
italic Latin and a table through the template and count missing glyphs:

```bash
pandoc probe.md -o /tmp/t.pdf --pdf-engine=xelatex \
  --template=templates/pdf/<name>.latex --verbose 2>&1 |
  grep -c "Missing character"
```

That is how the 21 non-buildable templates were migrated and verified —
0 made worse, and one (`gospel-harmony-liturgical`) went 20 → 0. Never
change a template you cannot compile even once.

## Run (agent path) — use this first

```bash
.claude/skills/eat-bible/driver.sh <book-slug> [page-to-screenshot]
.claude/skills/eat-bible/driver.sh <book-slug> --record-baseline
```

`<book-slug>` is the part between `build-` and `-consolidated.sh` in
`scripts/`. Run with no args to list available slugs. Verified this
session:

```
.claude/skills/eat-bible/driver.sh titus
.claude/skills/eat-bible/driver.sh pastoral-epistles 1
```

The driver runs the build, then checks in order: exit code → grep the
build log for `Missing character` warnings (a font asked to render a
glyph it doesn't have) → grep for LaTeX errors → report `Overfull
\hbox` warnings (non-fatal; content printing outside its column or past
the text block) → `pdffonts` to confirm every font is embedded/subset,
not just referenced → `pdftoppm` to render one page to
`/tmp/<slug>-p<N>*.png` for you to actually look at. It exits nonzero
and prints the relevant log lines on any failure.

**The last step gates on regression, not on zero.** `baselines.tsv`
(checked in beside the driver) records `pages / missing-glyphs /
overfull-boxes` per book. The driver fails if this build is *worse*
than the recorded numbers. Absolute counts can't be the gate here —
several books carried defects since they were created, so
"fail if nonzero" would mean the driver always fails and everyone stops
reading it. Read the current numbers from `baselines.tsv` rather than
from this file — as of 2026-08-28, 14 of 17 books sit at 0 overfull and
the remainder are `romans` 12, `gospel-of-matthew` 8,
`pastoral-epistles` 4. Every book is at 0 missing glyphs.

Those last 24 are all the same shape: a Latin or Greek word wedged
between full-width punctuation (`5:20，perisseuō（充盈`), which offers no
break opportunity. Fixing them means rewriting the cell, not widening
the column.

Those last three are the pre-existing backlog the lint predicts; the
rest are small. After deliberately fixing (or knowingly accepting) a
change, re-run with `--record-baseline` to move the reference. Never
use that flag to silence a regression you haven't looked at.

**Those log greps only work because the build script feeds them.**
`pandoc --pdf-engine=xelatex` swallows the entire xelatex log unless it
is passed `--verbose`; a build script that omits it produces a log with
zero warnings of any kind and the driver passes vacuously. Every
`scripts/build-*-consolidated.sh` now routes its verbose output to
`output/<slug>-build.log` and calls `latex_build_report` from
`scripts/lib/latex-check.sh`, which prints the counts and re-echoes the
offending lines for the driver to find. If the driver warns that a
build script printed no xelatex log summary, fix that before trusting
anything else it says. `references/gotchas.md` has the full account of
how this was found.

**Read the rendered PNG.** A clean exit from the driver only proves no
glyph is *entirely absent* from its font — it doesn't prove the page
*looks right*. Overflowing text boxes, a cover background that stops
short of the physical edge, or a diagram with colliding labels all
render "successfully" with zero warnings. Every cover/diagram page
touched this session was confirmed by rendering it and reading the
PNG, not by trusting a clean exit code.

**Then inspect the PDF as a published object, not as build output.**
The driver and the lint both read the *source*; a whole class of defect
is only visible in the artifact, and none of it raises a warning. Isaiah
passed every automated check while carrying a **33-page table of
contents** (8% of the book, itemised down to `30.8.2 詩篇 121:1-2`),
headings numbered `33.7.2` like a technical manual, a contents line
reading `8  第一章` with two contradicting numbers, no Title/Author
metadata whatsoever, and blank versos each bearing a lone page number.
Four commands, worth running once per book before calling it finished:

```bash
pdfinfo output/<slug>-consolidated.pdf          # Title/Author/Subject present? Tagged? page size?
pdftotext -f 7 -l 12 output/<slug>-consolidated.pdf -   # how long is the TOC, and at what depth?
pdffonts output/<slug>-consolidated.pdf         # every row emb/sub/uni = yes (columns are not positional)
pdftoppm -f <n> -l <n> -r 110 -png output/<slug>-consolidated.pdf /tmp/pg   # then actually look
```

`references/gotchas.md` has the fix for each of those, plus why tagged
PDF is out of reach on XeLaTeX.

Currently buildable (17 books, all using the `-consolidated.sh` /
`templates/pdf/<slug>.latex` pattern this driver assumes):
`1-peter`, `1-timothy`, `2-peter`, `2-timothy`, `acts`, `gospel`
(→ Gospel of John), `gospel-of-luke`, `gospel-of-mark`,
`gospel-of-matthew`, `hebrews`, `isaiah`, `pastoral-epistles`, `psalm`,
`psalm-liturgical`, `revelation`, `romans`, `titus`. Any other book in
`scripts/` using an older one-off build script won't follow this naming
convention — the driver won't find it by slug; check `scripts/`
directly. Run the driver with no args to get the current list.

## Run (human path)

```bash
bash scripts/build-<book>-consolidated.sh
open output/<book>-consolidated.pdf
```

Same thing, minus the automated verification. Useful for a quick eyeball
check but skips the missing-glyph/font-embedding checks the driver does.

## Prerequisites

Verified present on this machine (macOS):

```bash
pandoc --version    # pandoc 3.10 — /opt/homebrew/bin/pandoc
xelatex --version   # XeTeX 3.141592653-2.6-0.999998 (TeX Live 2026) — /Library/TeX/texbin/xelatex
kpsewhich lettrine.sty pgfornament.sty   # both resolve — needed for drop caps / ornamental flourishes
brew list poppler >/dev/null 2>&1 && echo ok   # gives pdftoppm/pdftotext/pdfinfo/pdffonts for verification
```

**Fonts are a hard macOS dependency, not a portability nicety.** The
templates require these exact Apple system fonts to be present
(`fontspec`'s `\setmainfont`/`\newfontfamily` will fail to find them
on Linux/Windows without installing substitutes):

- CJK: `Songti SC`, `Songti SC Bold`, `Kaiti SC` / `STKaitiSC`,
  `PingFang SC` (used for CJK-safe monospace — **do not** use `Menlo`
  for `\setmonofont` — see `references/gotchas.md`)
- Classical Latin display (added when a template gets the "classical
  redesign" treatment): `Baskerville`, `Didot`, `Big Caslon`,
  `Hoefler Text` + `Hoefler Text Ornaments` — all in
  `/System/Library/Fonts/Supplemental/` on macOS
- Greek/Hebrew fallback: `Times New Roman`, `Arial Hebrew`, switched
  automatically per-character via the `ucharclasses` package
