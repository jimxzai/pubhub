---
name: eat-bible
description: Build, verify, and edit this repo's consolidated study-book PDFs (pandoc + xelatex + templates/pdf/*.latex). Use when asked to build, compile, render, or screenshot a book PDF; to debug a build (missing glyphs, LaTeX errors, fonts, cover); to restructure or tighten a book's chapter markdown for print; or to source/verify Scripture text (CUV, NASB) for a chapter.
---

Paths are relative to the repo root (`pubhub/`), except `references/*.md`,
which sit beside this file.

| Reference | Read it when |
|---|---|
| `references/gotchas.md` | A build fails, a page looks wrong, or you are about to edit a `templates/pdf/*.latex`. Every silent failure this repo has hit, plus a symptom → cause → fix table. |
| `references/chapter-template.md` | You are restructuring or tightening a book's chapters for print: the 11-section house template, what stays verbatim, the dedupe rules, the per-chapter checks, and the fan-out that worked. |
| `references/scripture-sources.md` | You are writing or converting Scripture text: ai-eden.com URL patterns and quirks, the RCUV caveat, NASB-1995 sourcing on biblehub, CUV by the chapter, disclosure when a fallback source is used. |

## The order that works

Each step catches a class the next one cannot. Skipping a step means
shipping the defects only that step can see — every one of these was
learned by shipping it.

```bash
scripts/lint-templates.sh <slug>                       # 1. template bugs   ~1 s, no build
python3 scripts/lint-chapter-markup.py books/bible/<dir>  # 2. markdown bugs   ~1 s, no build
python3 scripts/lint-scripture-text.py books/bible/<dir>  # 3. CUV character slips
python3 scripts/verify-citations.py books/bible/<dir> --source <work.txt>  # 4. book quotes are verbatim
python3 scripts/verify-sermon-quotes.py books/bible/<dir>                  # 4a. sermon quotes are verbatim
python3 scripts/check-citation-ledger.py books/bible/<dir>                 # 4b. ledger matches the book
python3 scripts/normalize-commentary-notice.py books/bible/<dir>           # 4c. per-chapter notice matches too
.claude/skills/eat-bible/driver.sh <slug>              # 5. build + log + fonts + baseline
pdftoppm -f <n> -l <n> -r 110 -png output/<slug>-consolidated.pdf /tmp/pg   # 6. LOOK
.claude/skills/eat-bible/driver.sh <slug> --record-baseline   # 7. only after 6, only for an intended change
```

Fix lint findings first; they are causes, the build only shows symptoms.
Batch "algorithmic" fixes have a poor record here (four attempts at
re-proportioning table columns barely moved the overfull count and twice
made it worse). Read the pt figure xelatex reports and size from it. After
any batch change rebuild everything and diff against `baselines.tsv`; if a
number got worse, `git checkout` and rethink rather than layering a guess.

## What this is

There is no server or GUI. The "app" is `scripts/build-<slug>-consolidated.sh`
(older one-off books: `scripts/build-<slug>.sh`), which concatenates a
book's markdown (preface, orientation chapters, part dividers, chapters,
appendices) and pipes it through `pandoc --pdf-engine=xelatex` with
`templates/pdf/<slug>.latex`, producing `output/<slug>-consolidated.pdf`.
`pandoc` exiting 0 proves nothing: xelatex emits a PDF after recoverable
errors, absent glyphs render as blank boxes, a cover background can stop
short of the page edge, and markdown inside a raw-LaTeX macro prints as
literal asterisks. Run the driver with no arguments to list the slugs it
can build.

## Lints — free, run them every time

**`scripts/lint-templates.sh [slug …]`** reads `templates/pdf/*.latex`,
reports `file:LINE` per finding, exits 1 on any. Rules, all silent at
compile time: `real-bold-face` (a real `BoldFont` flattens CJK bold),
`cjk-blind-monofont` (`\setmonofont{Menlo}` → blank CJK),
`minipage-overflows-textblock`, `table-wider-than-textblock`,
`table-cell-wider-than-column` (Greek/Latin words cannot break, CJK can),
`ucharclasses-dead-transition`, `ucharclasses-two-way-clobber`.
This script exists because the same bug, documented in prose with "check the
other templates", was still in 56 of 57 templates months later; repo-wide
findings went 139 → 1 once each rule was a script.

**`scripts/lint-chapter-markup.py [path …]`** reads chapter markdown.
`markdown-inside-raw-macro` (error): `**x**` inside `\jesus{…}` — pandoc
passes the argument through untouched, so the PDF prints asterisks in
red-letter text; use `\textbf{}`/`\textit{}`. `duplicate-h2` (review): the
same `## ` title twice in one file. `dangling-section-ref` (review): a
「見『X』一節」 pointing at a heading the file no longer has.
`ascii-comma-in-cjk` (style). Luke shipped 18 raw-macro spans and five
dangling boxes through a clean driver run; the repo still carries ~170.

**`scripts/verify-citations.py <book-dir> --source <text> [--heading 摩根] [--accept <file>]`**
checks every `> "quoted"` commentary line against a local plain-text copy of the
work being quoted. `OK` = verbatim. **`DRIFT` = the dangerous one**: a long
prefix matches and then diverges — a real quote silently reworded. Luke shipped
four of those in one chapter ("heart-break in them" printed as "heartbreak in
these words", "irrevocable" as "inevitable") while its appendix simultaneously
claimed the book contained no verbatim quotes at all. `MISS` = unverified;
locate it or convert the point to unquoted summary. The matcher ignores case,
curly quotes, dashes and punctuation (all OCR-unstable) and is strict about
words. `--accept` takes a reviewed allowlist (see
`books/bible/gospel-of-luke/.citation-accept`) for deviations that are provably
the *source's* defect — never for a mismatch you haven't run down. It also
flags quotes that inline the translation as `> "English"（中文）` instead of the
house two-line form.

Getting a source text: many public-domain commentaries are online as one long
page — `curl` the HTML and strip tags locally rather than using WebFetch, which
truncates long pages and will make you think a genuine quote is missing.
Morgan's *The Gospel According to Luke* is at
`biblenotes.online/resources/commentaries/cmorgan_luke.htm` (63 expositions,
~1M chars); the archive.org copy is access-restricted and unusable for this.

**`scripts/verify-sermon-quotes.py <book-dir> [--heading 麥克阿瑟]`** does the same
for sermon quotes, which have no single local text: each chapter cites several
sermons, so a quote can only be checked against the ONE transcript it claims. It
maps each quote to the `sermon CODE` on the source line that follows it (「同上講章」
inherits the previous code), curls that gty.org transcript, caches it, and
string-matches. Luke's appendix asserted all MacArthur quotes were verified
word-for-word; running this found 6 of 18 in one batch had drifted — a fragment
recast as a standalone sentence, a clause cut at a comma and given a period, and
one chapter where all three quotes had key phrases absent from the transcript.
Two gotchas the script now handles, both of which produced false MISSes: split an
ellipsis-joined quote on the raw text BEFORE normalising (normalisation strips the
punctuation the split depends on), and try every code on a line that cites two.

**`scripts/check-citation-ledger.py <book-dir>`** compares the book's citation
ledger (`99-appendix-references.md`) against what the chapters actually contain,
per commentator. `UNDECLARED` = a chapter quotes verbatim but the ledger doesn't
say so (the Luke failure: the ledger declared all 24 Morgan sections
summary-only while 8 chapters carried 29 quotes — the dangerous direction, the
book quoting further than it admits to having verified). `OVERCLAIMED` = ledger
credits a chapter with quotes it doesn't have. `NO-ORIGINAL` = a citation gives
only a Chinese translation, so a reader cannot check it against the source.
Nothing else can catch a ledger that disagrees with its own book: the quotes are
valid markdown, the build is clean, and the appendix reads as coherent prose.

**`scripts/normalize-commentary-notice.py <book-dir> [--dry-run]`** rewrites each
chapter's 體例說明 notice from what the chapter actually contains. Luke had that
notice in seven different wordings, fourteen of them declaring 「帶引號引文均為編者
自英文原著的中譯」 — true when the chapters held Chinese only, false once English
originals were added, i.e. the honesty notice told readers the opposite of what
the page showed. Derive the notice, don't hand-maintain it.

**`scripts/lint-scripture-text.py [path …]`** flags 和合本 variant-character
slips inside scripture blocks (鑒/鑑, 熔/鎔, 汙/污, 裡/裏, 做/作). Rules are
word-scoped because CUV itself is mixed; the 做/作 class is flagged for
review, never auto-fixed. A findings-free run is a floor, not proof — only
a two-source diff (see `references/scripture-sources.md`) settles a verse.

**A template with no build script** is checked with a probe document
(CJK, full-width punctuation, Greek, Hebrew, italic Latin, a table):

```bash
pandoc probe.md -o /tmp/t.pdf --pdf-engine=xelatex \
  --template=templates/pdf/<name>.latex --verbose 2>&1 | grep -c "Missing character"
```

Never change a template you cannot compile even once.

## Driver

```bash
.claude/skills/eat-bible/driver.sh <slug> [page-to-screenshot]
.claude/skills/eat-bible/driver.sh <slug> --record-baseline
```

Runs the build, then in order: exit code → `Missing character` warnings
→ LaTeX errors → `Overfull \hbox` count → `pdffonts` (every font embedded
and subset) → `pdftoppm` one page to `/tmp/<slug>-p<N>*.png` → compare
with `baselines.tsv`. **It gates on regression, not on zero**: several
books carried defects from birth, so "fail if nonzero" would fail always
and be ignored. Read current numbers from `baselines.tsv`, not from prose.
Record a new baseline only after you have looked at the pages, and only
for a change you meant to make.

**The log greps only work because the build script feeds them.** pandoc
swallows the xelatex log unless given `--verbose`; every build script
routes that to `output/<slug>-build.log` and calls `latex_build_report`
from `scripts/lib/latex-check.sh`. If the driver warns that a script
printed no xelatex summary, fix that first — otherwise every check passes
vacuously (`grep -c "This is XeTeX" output/<slug>-build.log` = 0 means an
empty haystack).

## Look at the artifact

Lint and driver both read *sources*; a class of defect exists only in the
PDF and raises nothing. Isaiah passed every automated check with a 33-page
TOC, headings numbered `33.7.2`, no PDF metadata, and blank versos bearing
page numbers. Luke passed with asterisks in red-letter text. Once per book:

```bash
pdfinfo  output/<slug>-consolidated.pdf                 # Title/Author/Subject? page count?
pdftotext -f 7 -l 12 output/<slug>-consolidated.pdf -   # TOC length and depth
pdffonts output/<slug>-consolidated.pdf                 # every row emb/sub/uni = yes
pdftoppm -f <n> -l <n> -r 110 -png output/<slug>-consolidated.pdf /tmp/pg   # then Read the PNG
```

Pages worth rendering: the copyright page, one Scripture block (italics,
red letter, superscripts), one commentary page with quotes, one table-heavy
word study, the cover. Locate a page with
`for i in $(seq 1 N); do pdftotext -f $i -l $i f.pdf - | grep -q "phrase" && echo $i; done`.

## Human path

```bash
bash scripts/build-<slug>-consolidated.sh && open output/<slug>-consolidated.pdf
```

Same build, none of the verification.

## Prerequisites (macOS, verified)

```bash
pandoc --version    # 3.10, /opt/homebrew/bin/pandoc
xelatex --version   # TeX Live 2026, /Library/TeX/texbin/xelatex
kpsewhich lettrine.sty pgfornament.sty   # drop caps / ornaments
brew list poppler >/dev/null && echo ok  # pdftoppm pdftotext pdfinfo pdffonts
```

**Fonts are a hard macOS dependency.** Templates name Apple system fonts
by family: CJK `Songti SC`, `Songti SC Bold`, `Kaiti SC`/`STKaitiSC`,
`PingFang SC` (the CJK-safe monospace — never `Menlo`); display Latin
`Baskerville`, `Didot`, `Big Caslon`, `Hoefler Text` (+ Ornaments), all in
`/System/Library/Fonts/Supplemental/`; Greek/Hebrew fallback `Times New
Roman`, `Arial Hebrew`, switched per character by `ucharclasses`. The
interpunct in copyright pages must be U+00B7 `·` — U+30FB `・` is missing
from Songti SC.
