---
name: eat-bible
description: Build and verify one of this repo's consolidated study-book PDFs (pandoc + xelatex + custom LaTeX templates under templates/pdf/). Use when asked to build, compile, run, render, or screenshot a book PDF, or to debug a PDF build failure (missing glyphs, LaTeX errors, font embedding, cover layout).
---

Paths below are relative to the repo root (`pubhub/`), not to this skill directory.

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

## Run (agent path) — use this first

```bash
.claude/skills/eat-bible/driver.sh <book-slug> [page-to-screenshot]
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
glyph it doesn't have) → grep for LaTeX errors → `pdffonts` to confirm
every font is embedded/subset, not just referenced → `pdftoppm` to
render one page to `/tmp/<slug>-p<N>*.png` for you to actually look at.
It exits nonzero and prints the relevant log lines on any failure.

**Read the rendered PNG.** A clean exit from the driver only proves no
glyph is *entirely absent* from its font — it doesn't prove the page
*looks right*. Overflowing text boxes, a cover background that stops
short of the physical edge, or a diagram with colliding labels all
render "successfully" with zero warnings. Every cover/diagram page
touched this session was confirmed by rendering it and reading the
PNG, not by trusting a clean exit code.

Currently buildable (8 books, all using the `-consolidated.sh` /
`templates/pdf/<slug>.latex` pattern this driver assumes):
`1-timothy`, `2-timothy`, `titus`, `pastoral-epistles`, `acts`, `gospel`
(→ Gospel of John), `gospel-of-matthew`, `hebrews`. Other books in
`scripts/` use older one-off build scripts that don't follow this
naming convention — the driver won't find them by slug; check
`scripts/` directly.

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
  for `\setmonofont`, see Gotchas)
- Classical Latin display (added when a template gets the "classical
  redesign" treatment): `Baskerville`, `Didot`, `Big Caslon`,
  `Hoefler Text` + `Hoefler Text Ornaments` — all in
  `/System/Library/Fonts/Supplemental/` on macOS
- Greek/Hebrew fallback: `Times New Roman`, `Arial Hebrew`, switched
  automatically per-character via the `ucharclasses` package

## Scripture sourcing (before the build — during content writing)

The project's own site, **ai-eden.com**, is the standard Bible source for
all scripture verification when *writing* a book's markdown chapters
(this is distinct from the PDF-build concern above, but belongs in this
skill because it's the same content pipeline). Never quote Scripture
from training-data memory — fetch and verify against a real source, per
this project's anti-fabrication rules (`CLAUDE.md`, `.claude/CONTENT_RULES.md`).

**URL pattern:**

```
https://www.ai-eden.com/bible/<book-slug>/<chapter>?t=<VERSION1>,<VERSION2>&cols=2
# e.g. https://www.ai-eden.com/bible/romans/1?t=RCUV,ESV&cols=2
```

Version codes confirmed genuinely available: `CUV` (和合本), `ESV`,
`NASB` (per the site owner's own reference notes). **`RCUV` (和合本修訂版)
is NOT confirmed as a distinct dataset on this site** — see caution
below.

**Known quirks, verified this session:**

- The page is JS-rendered (Next.js/Turbopack). `WebFetch` sometimes
  extracts the rendered text fine (confirmed working for `ESV`) but
  can come back empty for a specific translation on a given try
  (confirmed: one fetch returned the `ESV` column complete but
  reported the requested `RCUV` column "header present, content
  absent") — content appears to hydrate asynchronously per-version.
  **Retry the WebFetch once or twice** before concluding a
  translation isn't retrievable; don't give up on the first empty
  result.
- **`t=RCUV` is suspect — it may silently serve CUV instead of a real
  RCUV dataset.** One fetch requesting `?t=RCUV` alone returned visible
  verse text, but the extracting model identified it as "CUV (Chinese
  Union Version), not RCUV (修訂版)" — i.e. the site may not
  distinguish RCUV from CUV at all, or may fall back silently when an
  unsupported code is passed. Do not assume text returned under an
  `RCUV` request is actually the 2010 Revised Version; if RCUV
  specifically is required, verify independently (e.g. against
  `cnbible.com`'s RCUV pages) rather than trusting the `t=RCUV` label
  at face value.
- There is a real JSON API behind the page — confirmed via the
  `x-matched-path: /api/bible/[book]/[chapter]` response header — at
  `https://www.ai-eden.com/api/bible/<book-slug>/<chapter>?t=<VERSION>`.
  This is the correct machine-readable path when it's available, but
  it is **aggressively rate-limited**: repeated `curl` requests this
  session returned `HTTP 429 {"success":false,"error":{"code":"RATE_LIMITED"}}`
  even when spaced tens of seconds apart. **Do not hammer it** — space
  requests out, and don't fan out more than 2-3 concurrent
  fetches/agents against ai-eden.com at once (this is very likely why,
  in a 16-chapter parallel Romans build this session, most chapter
  agents fetching concurrently fell back to `cnbible.com` /
  `biblehub.com` / `biblegateway.com` for RCUV instead of getting it
  from ai-eden.com).
- Its CSP header (`connect-src`) references `https://bolls.life`, a
  public Bible-text API — the site's backend likely proxies Bolls'
  data for at least some translations. Useful context if debugging
  further, not something to fetch directly instead of ai-eden.com.

**Fallback chain:** ai-eden.com (primary) → `cnbible.com` →
`biblegateway.com` / `biblehub.com`. If a fallback source is used for a
verse or chapter because ai-eden.com couldn't be verified after retrying,
**disclose this honestly in the content** rather than silently
presenting it as the primary version — see the disclosure pattern
already established in
`books/bible/pauline-epistles/1-timothy/99-appendix-references.md`
and `books/bible/pauline-epistles/romans/99-appendix-references.md`
(a short "版本說明" note naming the actual source used, right after
the Scripture section, plus a per-chapter breakdown in the book's
own references appendix).

## Gotchas

These are specific failures hit and fixed across this session's builds
(1 Timothy, 2 Timothy, Titus, the combined "盡職" volume), not generic
LaTeX advice:

- **`BoldFont=<Family> Bold` pointing at a real bold font file silently
  weakens (and can fully flatten) `\textbf{}` for CJK text that contains
  full-width punctuation (：。) — with zero warnings, zero errors, exit
  code 0.** Root cause, confirmed on the 1 Peter template: "Songti SC
  Bold" has missing/mismatched glyphs for full-width colon and period.
  When xelatex hits one of those inside a `\textbf` run, it silently
  degrades that run's weight rather than erroring or substituting just
  the one glyph — and since nearly every bolded Chinese phrase in this
  project contains such punctuation, the practical effect on a real
  chapter page is bold text that's measurably weaker throughout (see
  measurement method below), sometimes reading as fully non-bold to the
  eye, sometimes just "not as heavy as it should be." **This will not
  show up in `driver.sh`'s missing-glyph/error checks — those only
  catch glyphs absent from a font entirely, not glyphs present but
  triggering a silent weight fallback.** The only way to catch it is to
  actually look at (or measure) rendered bold text.
  **Fix**: point `BoldFont` at the *same* regular font file, thickened
  synthetically, instead of a separate real bold face — guarantees
  identical glyph coverage so the fallback can't trigger:
  ```latex
  \setmainfont{Songti SC}[BoldFont=Songti SC, BoldFeatures={FakeBold=2.2}, ItalicFont=Kaiti SC]
  ```
  Apply the same pattern to **every** `\newfontfamily` ucharclasses can
  switch into mid-run (`\cjkfallbackfont`, `\greekfont`, `\hebrewfont`,
  `\basklatin`/whatever the Latin-run font is called) — the bug recurs
  identically the instant a bold span crosses into any of them, since
  none of them had a working bold face either. Confirmed this affects
  at least `templates/pdf/1-peter.latex` and (pre-fix, since it was
  copied from) `templates/pdf/romans.latex` — **check every other
  `templates/pdf/*.latex` file for this exact `BoldFont=` pattern before
  assuming a book's bold text is fine.**
  **How to verify, reliably** (eyeballing a production page is not
  reliable — see below): compile a *minimal* reproduction, not the full
  book — the effect is dramatic and unambiguous in isolation but gets
  visually diluted (while remaining just as real) once buried in a full
  page of mixed content:
  ```latex
  \documentclass[11pt]{article}
  \usepackage{fontspec}
  \setmainfont{Songti SC}[BoldFont=Songti SC Bold, ItalicFont=Kaiti SC]  % the template's current setting
  \begin{document}
  \textbf{一句話精義：受苦不是意外，是操練場。}
  \end{document}
  ```
  Render at `pdftoppm -r 200` and look — with the buggy `BoldFont=<real
  face>` this renders visibly flat/non-bold; with `BoldFont=<same file>,
  BoldFeatures={FakeBold=2.2}` it's unambiguously heavier. **Do not
  trust a same-page-by-eye comparison on real book content** — a
  same-page pixel-density measurement (crop the same x/y region across
  a broken vs. fixed render, count pixels below a darkness threshold)
  showed the real effect is a consistent 13–32% ink-density increase on
  lines containing bold text once fixed, with an exact 0% difference on
  bold-free control lines in the same page — real and measurable, but
  visually subtle enough at normal reading distance that a rushed
  eyeball check can miss it. Trust the minimal isolated repro to decide
  whether a template has this bug at all; don't rely on "does this real
  page look bold enough to me" as the test.

- **CJK text under `\setmonofont{Menlo}`** → every CJK character in a
  code/ASCII-art block renders as a blank box and emits a "Missing
  character" warning. Menlo has zero CJK glyphs. Fix: `\setmonofont`
  to `Songti SC` or `PingFang SC` instead.
- **A custom Latin-only font command (`\baskervillefont`, etc.) wrapped
  around mixed CJK+English text** → same failure, same fix (narrow the
  font-switch scope to the English-only substring). This recurred
  independently in at least four separate template files this
  session — it's the single most common bug in this codebase's LaTeX.
- **Pandoc's own template engine parses `$...$` before xelatex ever
  sees it** — a TikZ coordinate like `$(0,0)$` inside a `\newcommand`
  used in a pandoc `.latex` template gets eaten as a pandoc variable
  delimiter, not passed through. Fix: escape to `$$(0,0)$$` in the
  template source.
- **`\foreach` with a braced, multi-line value** (e.g. looping over
  `{...\\...}` entries) breaks pgf's list parser —
  `Undefined control sequence` inside `pgffor@atendforeach`. Fix:
  unroll into explicit separate `\node` calls instead of looping.
- **TikZ's `scale=` option shrinks geometry but not font size** — reuse
  a diagram at a smaller scale and its text overflows the (now
  smaller) boxes. Fix: add `transform shape` alongside `scale=`.
- **`\hrule` in horizontal mode** → `LaTeX Error: There's no line here
  to end.` Use `\rule{width}{height}` instead of `\hrule` inside
  centered/inline contexts.
- **Full-bleed page backgrounds**: use `eso-pic`'s
  `\AddToShipoutPictureBG*{...}` / `\AddToShipoutPictureFG*{...}` (the
  **starred** form applies to exactly the next page, not every page)
  painting a rectangle sized `\paperwidth`×`\paperheight` — not
  `\textwidth`/`\textheight`, which stops at the margin, not the
  physical edge. This does not require touching `geometry` for any
  other page.
- **Porting a macro call between templates without checking its local
  signature** — e.g. one file's `\fleuron[width]{}` vs. another's
  `\fleuron[color]{}`. Copying a call site verbatim compiles into
  silently wrong PGF math or an outright error. Check the target
  file's own macro definition before reusing a call from a reference
  file; when in doubt, add a differently-named variant rather than
  redefining an existing macro's meaning everywhere it's already used.
- **Missing a font-command alias when porting code** — reference code
  calling `\baskervillefont` into a file that only defines
  `\basklatin` → `Undefined control sequence`. One-line fix:
  `\newcommand{\baskervillefont}{\basklatin}` rather than renaming
  every call site.
- **No `\clearpage` + `\pagestyle{empty}` before `\backmatter`** → a
  stray header/pagestyle from the preceding appendix leaks onto what
  should be a blank full-bleed cover page.
- **`\vspace*{\fill}...\vspace*{\fill}` for vertical centering, relied
  on to also produce page breaks** → pushes short trailing content onto
  an orphan near-blank page, or (once tightened) splits a bilingual
  line mid-sentence across two pages. Use an explicit `\clearpage`
  between distinct page-content blocks; don't overload fill-based
  centering to do page-breaking too.
- **Verify page order with `pdftotext -f N -l N`, not by eyeballing a
  screenshot render.** When adding a half-title/dedication/colophon
  page, it's easy to get the front-cover-must-be-page-1 /
  back-cover-must-be-the-true-last-page ordering backwards, and a
  quickly-skimmed screenshot can be misread. `pdftotext -f N -l N
  output/<book>.pdf -` on the specific page number you expect is
  unambiguous.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `**bold**` Chinese text renders flat/weak in the PDF, but the build log shows zero warnings and zero errors | `BoldFont=` points at a real bold font file missing glyphs for full-width punctuation (：。) inside the bold span — silent weight fallback, not a missing-glyph error | Point `BoldFont` at the same regular font file with `BoldFeatures={FakeBold=<n>}` instead of a separate real bold face; apply to every `\newfontfamily` ucharclasses can switch into, not just `\setmainfont`. See Gotchas above for the isolated repro to confirm before/after. |
| `Missing character: There is no X in font Y!` in the build log | A font is missing a glyph it's being asked to render — almost always CJK text scoped under a Latin-only font, or a monospace font (Menlo) with no CJK glyphs | See Gotchas above; narrow the font scope or switch `\setmonofont` |
| `! LaTeX Error: There's no line here to end.` | `\hrule` used outside vertical mode | Replace with `\rule{width}{height}` |
| `! Undefined control sequence` naming a `pgffor@...` internal | `\foreach` looping over a braced multi-line value | Unroll the loop into explicit statements |
| `! Undefined control sequence` naming a font command you just added | Ported code calls a macro (`\baskervillefont`) this file never defined | Add a one-line `\newcommand` alias, or fix the call site |
| PDF builds clean but a cover/background doesn't reach the physical page edge | Background painted to `\textwidth`/`\textheight` instead of `\paperwidth`/`\paperheight` | Repaint using the paper dimensions, via `eso-pic`'s starred shipout hooks |
| `pdffonts` shows a font row without `yes yes yes` in the emb/sub/uni columns | A font referenced but not embedded — will render wrong on a machine without it installed | Usually a fontspec fallback path skipped `xelatex`'s embedding; check the font name resolves correctly for `\newfontfamily` |
