# Mark consolidated edition: build and release checks

Keep the assigned title and output stem. Both historical entry points now run the same staged PDF/EPUB build:

```sh
bash build-publication.sh
python3 -m unittest discover -s publishing -v
```

Requirements: Python with pypdf, Pandoc, XeLaTeX, installed template fonts,
Poppler (`pdftotext`, `pdftoppm`, `pdffonts`), Java and official EPUBCheck.
Set `EPUBCHECK_JAR` to the installed validator JAR. The current workstation
fallback is `/tmp/mark-epubcheck-tools/epubcheck-5.3.0/epubcheck.jar`; that temporary
installation may disappear after cleanup. Missing EPUBCheck blocks promotion.
No dependency is silently downloaded by the builder.

The single template source remains `templates/pdf/gospel-of-mark.latex` at the
repository root. Appendix index numbers in it are bootstrap data; the build
regenerates them from PDF text and requires stable pagination. Never invoke
Pandoc directly to produce a distributable companion: it drops custom TeX
macros and template-only content. Use the paired build to keep print-page
references aligned. The low-level `publishing/epub.py` is for development only.

Each build verifies the 29 source front-matter boundaries, stages both formats,
rejects fatal TeX/glyph/overflow/reference errors, checks PDF language and
outlines, checks EPUB content and internal links, and requires zero EPUBCheck
errors/warnings. Previous outputs are copied to a recovery directory outside
`output` before replacement; ordinary promotion failures restore them. A sudden
machine shutdown during multi-file promotion is not an atomic transaction;
restore the reported backup directory if interrupted. PDF/EPUB hashes are in
the QA JSON. Builds are serialized by `publishing/.build.lock`.

After inspecting rendered pages and running Ace, `record_review.py` can attach
that review to the QA JSON. It requires an explicit reviewed PDF SHA-256, physical
page numbers, and a passing Ace report; it does not perform visual inspection.
Every rebuild resets review status and moves any prior Ace report to the backup
directory so a report for an older artifact is not mistaken for current evidence.

Automated checks do **not** certify independent textual accuracy, permissions,
PDF/UA, EPUB Accessibility or WCAG. The PDF is untagged. The EPUB retains the
historical `-accessible.epub` filename without a conformance claim. Pure English
paragraphs are language-marked; mixed-language inline phrases need manual review.
The EPUB includes the same front cover; print maps and the designed back cover
are not reproduced as EPUB illustrations.

Before releasing: inspect rendered final pages; run DAISY Ace on the exact EPUB;
review any findings; test keyboard and screen-reader reading order and table
navigation; independently proofread Scripture and quotations; close permissions
in `PUBLICATION_RELEASE_REGISTER.md`. Retain the validator reports and signed
review evidence alongside the matching hashes. Never treat non-sale status as
permission clearance.
