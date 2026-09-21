# Build, cover, and delivery verification

## Safe implementation

Read builder assignments and ordered inputs first. Preserve unrelated edits.
Build experiments in a uniquely named temporary directory using an existing
output override when supported; Matthew currently supports `MATTHEW_OUTPUT_DIR`.
Do not assume the shared driver follows this override: its PDF lookup may still
target `output/`. For scratch builds invoke the builder and inspect the resolved
scratch artifact directly. Preserve one pre-change proof for comparisons.

Build scripts should fail on missing required inputs and propagate errors.
When editing Bash with `set -e`, avoid `((count++))` returning failure on zero;
check optional positional arguments safely. Test the changed behavior, not just
the presence of strict-mode flags. Do not apply repository-wide refactors as a
side effect of fixing one book.

## Covers at a professional standard

If a reference such as Genesis is named, locate and render its actual front
and back covers beside the assigned book. Compare title hierarchy, bilingual
balance, typography, spacing, visual motif, contrast, and back-cover readability.
Match production quality, not necessarily the reference's palette or imagery.
Preserve title, edition/year, author/publisher identity unless asked to change.

Prefer the existing vector/LaTeX design system when appropriate; raster art is
optional, not a requirement for a professional result. Inspect local macro
definitions before porting a call from another template. For full-bleed cover
backgrounds, use page dimensions and one-page starred shipout hooks so body
geometry/backgrounds remain unchanged. First and true last pages must be the
covers, without running heads, folios, unintended white margins, or stray pages.

For cover-only changes, compare page count and all interior text before/after.
For claims that the interior is visually unchanged, additionally compare
interior page renders; identical text is insufficient. Review covers at thumbnail
size and readable resolution. Check bilingual line endings and back-cover copy.
A digital full-bleed cover is not automatically a printer-ready wrap/spine cover:
obtain trim, bleed, binding, paper, and printer specifications when that is asked.

### John and Luke reference lessons (observed 2026-09-21)

The user specifically likes both books. Reference artifacts are
`output/gospel-of-john-consolidated.pdf` (then 327 pages) and
`output/gospel-of-luke-consolidated.pdf` (then 299 pages). Recheck current page
counts; back covers are the actual last pages, not permanently 327/299.

- **John:** a compact light emblem, strong Chinese thematic title, gold italic
  English counterpart, and restrained secondary study title create a clear
  reading order. Its back cover explains the reader benefit and explicitly
  discloses CUV 1919 / NASB 1995 selections rather than claiming a complete
  verse-aligned bilingual Gospel. Borrow this transparency, not John's title,
  edition number, unique claims, or navy color as a mandatory series rule.
- **Luke:** an economical doorway/path motif, generous space around the title,
  paired Chinese/English theme, and a short reader-centered back-cover hook.
  Three concise benefit rows are easier to scan than a dense feature inventory.
  Avoid copying incidental English hyphenation or duplicated publisher wording.
- **Matthew:** preserve its royal purple, crown motif, assigned title and 2026
  edition. Potential refinements are stronger Chinese/English theme pairing,
  a single publisher lockup, explicit translation/selection disclosure, and
  more breathing room between back-cover prose and the benefits block. Inspect
  current renders before deciding whether these remain necessary.

The user's requested benchmarks are **9.6/10 overall and 9.7/10 covers**.
They are goals, not preassigned results. A cover subscore is a useful separately
reported diagnostic; do not insert it into the ten-row rubric as an additional
weighted row or import a reference book's score as evidence for Matthew.

## Layered PDF verification

1. Run the relevant source and template lints. Resolve warnings by cause, not
   blind substitutions. Record unresolved review items separately from errors.
2. Inspect the real verbose TeX log: an engine banner and `Output written on`
   must be present. Search fatal errors, missing glyphs, and horizontal/vertical
   overfull boxes. Repeated passes inflate warning counts; don't equate eight
   warnings with eight distinct locations. Check the log belongs to this build.
3. Run `scripts/audit_pdf.py` in this skill against the exact PDF. It hashes the
   file and checks all-page rendering, text outside the page, links, and optional
   expected chapter bookmarks/log/interior text. A blank extracted page may be
   an illustration or intentional verso. Review it; don't delete automatically.
4. Inspect `pdfinfo` and `pdffonts`: title, author/XMP, language, dimensions,
   and actual font embedding. Parse the named columns: `CID TrueType` has a
   space; `sub=no` does not mean unembedded and `uni=no` is a separate concern.
   Check Greek/Hebrew and italic/bold faces visually, not just presence in a list.
5. Render with Poppler and **view** front, back, contents, dividers, representative
   early/middle/late chapters, dense tables, callouts, multilingual text, and every
   changed/risk page. Full-book publication review needs broader coverage than
   two pages. Record inspected page numbers and renderer warnings.

The automated bounds check sees text boxes outside the physical page, not all
text-block/column overflow, overlaps, already-clipped text, bad contrast, or
proofreading defects. Decoder checks at low resolution do not replace print-size
inspection. An untagged PDF remains an accessibility limitation; tagged output
alone does not certify PDF/UA. Do not silently migrate XeLaTeX to LuaLaTeX during
a cover pass; that is a separate re-typesetting and accessibility project.

## Known traps worth checking when relevant

- Clean logs can miss a callout positioned above a page edge. Matthew needed
  an explicit page break before an overflowing front-matter section.
- Missing ExtGState resources may appear only when rendering. In a Matthew
  shipout design, an opaque blended color avoided the transparency defect.
- Keep TikZ font specifications simple; paragraph assignments in `font=` can
  cause “Missing number”. Explicit line breaks can be safer for cover copy.
- Pandoc template `$...$` syntax collides with TikZ math delimiters; escape
  appropriately in templates. JavaScript replacement strings interpret `$$`:
  use a replacement callback when preserving template text literally.
- Font-switch groups in Markdown need Pandoc raw-LaTeX spans, otherwise braces
  may be escaped and font changes leak. Test generated LaTeX before broad edits.
- `ucharclasses` block/group APIs differ, and two-way transitions can overwrite
  one another. Do not migrate transitions without a used-block census and renders.
- CJK text in Latin-only/monospace fonts, upright “italic” fallback fonts, or
  mixed-script weight changes can survive builds. Inspect actual rendered text.
  Don't hardcode macOS hashed asset-font paths or misdiagnose sandbox access as
  a missing font; inspect availability and request permissions when needed.
- Budget table widths with padding/rules included; Hebrew runs may not wrap.
  Inspect Pandoc's generated column types before adjusting Markdown separators.
- `scale=` in TikZ doesn't scale text without `transform shape`. Scope changes
  to the affected diagram instead of changing all body typography.
- TOC depth depends on the LaTeX counter, not merely Pandoc's command-line flag.
  Front/back matter must not unintentionally consume study chapter numbers.
- In a two-stage `.tex` build, verify em-dashes survive smart substitutions;
  check index injection skips fenced-code contents and doesn't print raw macros.

The original `.claude/skills/eat-bible/references/gotchas.md` contains historical
reproductions for these mechanisms. Consult the relevant section only when
needed; its historical environment claims are not guarantees about today's tools.

## Scoped cleanup

Keep the user's assigned basename and edition. Inventory candidate alternate
outputs, confirm what the builder and docs reference, and check tracked/untracked
status. Similar names alone do not prove a file is disposable. Preserve canonical
PDF/combined Markdown, required logs, source, templates, score evidence, and
reusable validation scripts. Do not conflate old manuscript directories with
generated duplicate PDFs.

For clearly authorized redundant generated versions, prefer a recoverable
archive outside the canonical output listing. Record exact source/destination
paths; move only resolved candidates, never broad globs or entire output/source
directories. If ownership or active use is unclear, ask before removal. Keep
one temporary pre-change proof until checks finish, then report what was archived
or removed and how it can be recovered. Do not delete Claude's original skill as
part of importing it into Codex.
