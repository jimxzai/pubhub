# eat-bible — Gotchas and Troubleshooting

Loaded on demand from `SKILL.md`. Read this when a build fails, when a page
looks wrong, or before changing a `templates/pdf/*.latex` file.

Every entry here is a failure actually hit and fixed in this repo (1 Timothy,
2 Timothy, Titus, the combined 「盡職」 volume, 2 Peter, Isaiah) — not generic
LaTeX advice. The silent ones produce **exit code 0, no warning, and a PDF**;
they are only findable by looking at the rendered page, reading the xelatex
log, or running `scripts/lint-templates.sh`.

Four of them are now checked automatically — run the lint before reading
further, it may answer your question in a second:

```bash
scripts/lint-templates.sh [template-name ...]
```

## Gotchas

- **`ucharclasses` has two APIs, and passing the wrong name to either one
  compiles cleanly and does nothing at all.**
  ```latex
  \setTransitionsFor{<Block>}{in}{out}   % 3 args — a real Unicode BLOCK
  \setTransitionsFor<Group>{in}{out}     % 2 args — a class GROUP
  ```
  `Greek`, `Latin`, `CJK`, `Chinese`, `Punctuation`, `Other` are class
  **groups**. `GreekAndCoptic`, `GreekExtended`, `Hebrew`,
  `CJKSymbolsAndPunctuation`, `HalfwidthAndFullwidthForms`,
  `CJKUnifiedIdeographs` are **blocks**. `Han` is neither. Feeding a group
  name — or a name that doesn't exist — to the 3-arg form is a silent no-op:
  no error, no warning, and the font simply never switches.

  Found on `revelation.latex`, where three of five transitions were dead:
  `{Greek}` (block is `GreekAndCoptic`), `{Han}` (no such thing), and
  `{Latin}` (group form is `\setTransitionsForLatin`). `isaiah.latex` has the
  same dead `{Greek}` line. **Check every template for this** — the symptom is
  invisible, because the text still renders, just in the main font.

  Downstream consequence worth knowing: with the Latin transition dead,
  `\emph{}` on a Latin word resolves to `\setmainfont`'s `ItalicFont`. In
  these templates that is `Kaiti SC`, a Chinese brush face whose Latin glyphs
  are **upright** — so every italicised book title renders as roman, with no
  warning. Confirmed by repro with ucharclasses not even loaded.

- **A `\newfontfamily` switch used as a ucharclasses transition resets series
  and shape**, dropping `\textbf` and `\emph` at every script boundary. Carry
  them across:
  ```latex
  \makeatletter
  \newcommand{\uckeep}[1]{%
    \edef\uc@sh{\f@shape}\edef\uc@se{\f@series}%
    #1\fontshape{\uc@sh}\fontseries{\uc@se}\selectfont}
  \makeatother
  \setTransitionsFor{Hebrew}{\uckeep{\hebrewfont}}{\normalfont}
  ```

- **Enabling a Latin transition in a CJK book is a project, not a one-liner.**
  Once Latin switches families, every other class needs an explicit
  destination or it inherits Baskerville/Times and emits missing-glyph
  warnings. Four measured attempts on Revelation got 5 → 5 → 6 → 4 missing
  glyphs without reaching zero; the residue was the first character of each
  Hebrew and polytonic-Greek run. Facts established, so the next attempt
  starts further along:
  - ASCII punctuation is in `BasicLatin` → the **Latin** class, so enabling
    Latin does *not* fragment English words.
  - `。` is `CJKSymbolsAndPunctuation`, `）` is `HalfwidthAndFullwidthForms`;
    both are in the `Chinese` and `CJK` groups, neither is in the
    `CJKUnifiedIdeographs` block.
  - Later `\setTransitionsFor*` declarations win for any block two of them
    claim, and `\setTransitionsForOther` claims nearly everything — declare it
    early.
  - Leave-codes matter: `\normalfont` on exit can clobber the next class's
    enter code; empty leave-codes strand characters in the previous font.
  - **The blocker, characterised**: a ucharclasses transition does NOT fire
    when the preceding character is CJK/full-width punctuation. Isolated
    repro — `ἀποκάλυψις` immediately after each of these:

    | preceding char | transition fires? |
    |---|---|
    | `：` U+FF1A full-width colon | **no** |
    | `、` U+3001 ideographic comma | **no** |
    | space | yes |
    | a CJK ideograph | yes |
    | `:` ASCII colon | yes |
    | paragraph start | yes |

    This is not specific to enabling Latin — it applies to the
    `GreekExtended` / `Hebrew` transitions the templates already ship. It is
    invisible in Revelation and Isaiah today only because Songti SC happens to
    have basic Greek glyphs, so a failed switch renders the wrong face with no
    warning; you only get a "Missing character" when the fallback font lacks
    the glyph outright (polytonic `ἀ`, Hebrew). **So a clean driver run does
    not prove the Greek in a book is in `\greekfont`** — check a rendered page
    if it matters.

- **`pandoc --pdf-engine=xelatex` discards the entire xelatex log unless
  you pass `--verbose` — so every "grep the build log" check in this
  repo passed vacuously for as long as it existed.** Measured on
  Isaiah: `driver.sh`'s captured log was **51 lines**, contained no
  xelatex output at all, and duly reported `Missing character
  warnings: 0` / `LaTeX error lines: 0`. Piping the same combined
  markdown through `pandoc -t latex` and running `xelatex` by hand
  surfaced **28 `Overfull \hbox` warnings** on that identical "clean"
  build — including three appendix boxes printing 39.3pt past the text
  block and a Hebrew word-study cell overprinting the column beside
  it. Nothing about the exit code, the PDF, or the driver's green
  `PASS` distinguished that from a genuinely clean book.
  **Fix**: pass `--verbose`, send it to a file (it is tens of thousands
  of lines), and re-echo the offending lines so a log-grepping caller
  has something real to find. That is what
  `scripts/lib/latex-check.sh`'s `latex_build_report` does; all 17
  `scripts/build-*-consolidated.sh` now source it. Confirm a build
  script is honest with:
  ```bash
  grep -c "This is XeTeX" output/<slug>-build.log   # 0 → the log is empty theatre
  ```
  Careful with the summary wording: a status line that itself contains
  the literal string `Missing character` or `Overfull \hbox` will be
  counted by the driver's own `grep -c` and register as a failure. The
  helper prints `missing-glyph warnings:` / `overfull-box warnings:`
  for exactly this reason.

- **`Overfull \hbox` is the *only* signal that content is printing
  outside its column or off the text block.** Exit code 0, no glyph
  warnings, no LaTeX error, PDF renders. Three distinct causes
  confirmed on Isaiah, all invisible until the log was readable:
  - **A right-to-left Hebrew run has no line-break opportunities**, so
    a long one in a narrow table cell simply overprints the cell to its
    right. XeTeX does *not* break inside a reordered RTL run — not at
    the embedded spaces, not at the full-width parens or `／` inside
    it: `אָמַן（תַאֲמִינוּ／תֵאָמֵנוּ）` was measured as one 103.5pt box in a
    60.6pt column. Do not assume a cell will wrap because it contains
    separators. Either widen the column to fit the whole run, or move
    the extra forms into the prose/註解 column.
  - **`\begin{minipage}{<fixed>in}` inside `\fcolorbox`** — a 6.0in
    minipage plus `2\fboxsep + 2\fboxrule` is 440.4pt against a 401.1pt
    `\textwidth`, i.e. exactly the 39.3pt overflow observed. Use
    `\begin{minipage}{\dimexpr\textwidth-2\fboxsep-2\fboxrule\relax}`;
    never a hardcoded inch value that happens to look right.
  - **A pandoc pipe table whose separator row is all-equal short
    dashes** compiles to `\begin{longtable}[]{@{}lll@{}}` — natural-width
    columns that never wrap. Fine until one row's content grows. Give
    the separator row proportional dash counts so pandoc emits `p{}`
    columns instead.

  For a fixed-width `longtable` the budget is
  `sum(p{}) + 2·\tabcolsep·(ncol−1) ≤ \textwidth`, i.e. with the
  7in×10in / 0.8in+0.65in geometry these templates use:
  `\textwidth` = 5.55in = **401.1pt = 14.097cm**, and `\tabcolsep` = 6pt,
  so a 4-column table has 12.83cm and a 3-column table 13.25cm to
  divide between its `p{}` widths. Four of Isaiah's template tables
  were over that budget and had been shipping overfull since the book
  was created.

- **A Hebrew/Greek fallback font needs an explicit `Scale=`.** Times
  New Roman's Hebrew glyphs are drawn far smaller than its own Latin
  and much smaller than Songti SC's CJK, so pointed Hebrew set at the
  nominal size renders with the nikkud crushed into an unreadable
  smudge — beside CJK at the same point size it looks like a footnote.
  Zero warnings, clean driver run; it is a pure legibility defect that
  only a rendered PNG shows. Fix:
  ```latex
  \newfontfamily\hebrewfont{Times New Roman}[Script=Hebrew, Scale=1.35, ...]
  ```
  Decide the number with an isolated repro rather than by eye on a book
  page — set the same word at several scales and against the real
  alternatives (macOS also has **`Arial Hebrew Scholar`**, purpose-built
  for pointed/cantillated text, and `New Peninim MT`, `Raanana`).
  Raising the scale makes the RTL-overflow problem above worse, so
  re-measure the table columns in the same pass.

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

- **A bare `{\somefont TEXT}` font-switch group typed directly into
  markdown prose (not inside a raw-LaTeX construct) gets its braces
  silently escaped by pandoc's markdown reader** — `{` → `\{`, `}` →
  `\{` — producing an UNSCOPED font command in the LaTeX output
  (`\{\somefont TEXT\}`, i.e. two literal brace *characters* plus a
  font switch with no real group to close it). The font then applies
  to every character from that point until some unrelated brace
  elsewhere in the document happens to close a group, cascading into
  pages of text stuck in the wrong font/encoding — CJK characters
  rendered as if they were Latin, "Missing character" warnings by the
  thousand, and no LaTeX error (exit code 0) because nothing is
  actually malformed from TeX's point of view. **This was root-caused
  on the 2 Peter template only after two prior debugging passes wrongly
  attributed the same symptom to ucharclasses conflicts, `\par` inside
  repeated groups, and longtable cell-measurement corruption** — those
  were each independently real, separate bugs (see the BoldFont/Menlo
  entries above), but none of them was the cause of *this* specific
  cascading corruption. Confirm the mechanism directly before touching
  anything else:
  ```bash
  echo '{\greekfont test}' | pandoc -f markdown -t latex
  # → \{\greekfont test\}     (broken: escaped literal braces, unscoped command)
  ```
  **Fix**: never write a raw `{...}` font-switch group straight into
  markdown source (prose, headings, blockquotes, table cells, bold
  spans — all of them escape identically). Wrap it in pandoc's
  `raw_attribute` extension instead (on by default in this project's
  `markdown-superscript-subscript` format), which passes the span
  through byte-for-byte:
  ```
  `{\greekfont ἐπίγνωσις}`{=latex}
  ```
  ```bash
  echo '`{\greekfont test}`{=latex}' | pandoc -f markdown -t latex
  # → {\greekfont test}       (correct: real matched braces)
  ```
  Verified safe in every context this bug previously seemed context-
  dependent on — plain prose, `#` headings, `>` blockquotes, `**bold**`
  spans, and markdown table cells (both a cell containing only the
  wrapped term and a cell mixing it with other text). No exclusion
  logic by markdown context is needed once the span is used correctly;
  a build-script `re.sub` that wraps every matched run this way is
  safe to run unconditionally. If a template's build script has a
  Greek/Hebrew-wrapping step **disabled** with a comment blaming
  ucharclasses, `\par`, or longtable — that disabled state predates
  this fix and should be re-enabled using the `` `{...}`{=latex} ``
  form (check `scripts/build-2-peter-consolidated.sh` for the
  confirmed-working version).

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
| A template bug you already know about (flat CJK bold, blank CJK in a code block, a box in the margin, a table past the text block) | It was documented in prose and nobody re-checked the other 56 templates | `scripts/lint-templates.sh` — one second, no build, reports `template.latex:LINE`. Run it before touching a template and after. |
| `driver.sh` fails with `REGRESSION: overfull boxes went N → M` | Your edit pushed content outside a column or past the text block | Diff the new `Overfull \hbox` lines in `output/<book>-build.log` against what you changed. Only after you've looked, and the change is intended, re-run with `--record-baseline`. |
| `driver.sh` prints `no baseline for '<slug>'` | That book isn't tracked in `baselines.tsv` yet | Re-run with `--record-baseline` once you've confirmed the current state is one you want to hold the line at. |
| `driver.sh` prints `PASS` and a build log with zero warnings of any kind, but the PDF has visible defects | The build script isn't passing `--verbose` to pandoc, so the xelatex log was never captured and every log grep is checking an empty haystack | Route pandoc's `--verbose` output to `output/<slug>-build.log` and call `latex_build_report` from `scripts/lib/latex-check.sh`. Confirm with `grep -c "This is XeTeX" output/<slug>-build.log` — a 0 means the log is empty theatre. |
| Text overprints the column beside it, or a boxed callout bleeds into the margin — no warning, no error, exit 0 | `Overfull \hbox`: an unbreakable RTL Hebrew run wider than its cell, a `minipage{<fixed>in}` inside `\fcolorbox` wider than `\textwidth`, or a pandoc pipe table whose flat separator row compiled to non-wrapping `lll` columns | Read the overfull lines in the build log; they name the offending box. Widen the column (or move content out of it), swap the fixed minipage width for `\dimexpr\textwidth-2\fboxsep-2\fboxrule\relax`, and give pipe-table separator rows proportional dash counts. Column budget: `sum(p{}) + 2·\tabcolsep·(ncol−1) ≤ \textwidth`. |
| Hebrew/Greek renders legibly at a glance but the vowel points are an illegible smudge next to the CJK | The fallback font's non-Latin glyphs are drawn at a much smaller design size than the CJK main font; no warning, since the glyphs all exist | Add `Scale=` to the `\newfontfamily` (Isaiah uses `Scale=1.35` for Times New Roman Hebrew). Pick the value from an isolated repro; on macOS also compare `Arial Hebrew Scholar`. Re-measure table columns afterwards — scaling up can push a cell into overflow. |
| `**bold**` Chinese text renders flat/weak in the PDF, but the build log shows zero warnings and zero errors | `BoldFont=` points at a real bold font file missing glyphs for full-width punctuation (：。) inside the bold span — silent weight fallback, not a missing-glyph error | Point `BoldFont` at the same regular font file with `BoldFeatures={FakeBold=<n>}` instead of a separate real bold face; apply to every `\newfontfamily` ucharclasses can switch into, not just `\setmainfont`. See Gotchas above for the isolated repro to confirm before/after. |
| Pages of CJK text suddenly render in the wrong font (e.g. Times New Roman) with hundreds/thousands of "Missing character" warnings, starting right after a `{\somefont ...}` group somewhere earlier in the source, and exit code is still 0 | A bare `{...}` font-switch group was typed straight into markdown prose; pandoc escaped its braces to `\{`/`\}`, leaving `\somefont` unscoped and bleeding into everything after it | Wrap the group in a raw-LaTeX span so pandoc passes the braces through untouched: `` `{\somefont TEXT}`{=latex} `` instead of `{\somefont TEXT}`. See Gotchas above — confirm with the one-line `echo ... \| pandoc -f markdown -t latex` repro before assuming it's something else. |
| `Missing character: There is no X in font Y!` in the build log | A font is missing a glyph it's being asked to render — almost always CJK text scoped under a Latin-only font, or a monospace font (Menlo) with no CJK glyphs | See Gotchas above; narrow the font scope or switch `\setmonofont` |
| `! LaTeX Error: There's no line here to end.` | `\hrule` used outside vertical mode | Replace with `\rule{width}{height}` |
| `! Undefined control sequence` naming a `pgffor@...` internal | `\foreach` looping over a braced multi-line value | Unroll the loop into explicit statements |
| `! Undefined control sequence` naming a font command you just added | Ported code calls a macro (`\baskervillefont`) this file never defined | Add a one-line `\newcommand` alias, or fix the call site |
| PDF builds clean but a cover/background doesn't reach the physical page edge | Background painted to `\textwidth`/`\textheight` instead of `\paperwidth`/`\paperheight` | Repaint using the paper dimensions, via `eso-pic`'s starred shipout hooks |
| `pdffonts` shows a font row without `yes yes yes` in the emb/sub/uni columns | A font referenced but not embedded — will render wrong on a machine without it installed | Usually a fontspec fallback path skipped `xelatex`'s embedding; check the font name resolves correctly for `\newfontfamily` |
