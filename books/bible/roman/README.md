# 羅馬書研讀

## Start here

Recorded assessments: editorial/production **9.6/10**, cover **9.7/10**, commercial readiness **7.8/10 — HOLD**. These are separate prior judgments, not new scores from cleanup. See [publisher status](PUBLISHER-FIX-REPORT.md) for current counts and evidence limitations.

| Location | Role |
|---|---|
| [Publisher status](PUBLISHER-FIX-REPORT.md) | Current status and remaining work |
| [Editorial audit](EDITORIAL-AUDIT.md), [cover audit](COVER-AUDIT.md) | Review controls and cover assessment |
| [Release checklist](RELEASE-CHECKLIST.md) | Outstanding publication gates |
| [Rights ledger](RIGHTS-AND-CITATION-LEDGER.md), [rights policy](RIGHTS.md) | Clearance tracking versus usage policy; neither grants permission |
| `book.json`, `publication-manifest.json` | Build/source-order configuration versus publication control summary |
| `sources/archive/` | Original PDF and secondary recovery/reference material |
| `sources/reference/`, `sources/audits/` | Retained research, reproducible evidence and review history |
| `scripts/`, `templates/` | Reusable build and validation tools |

Keep root manuscript paths intact: they are build inputs. `ROMANS-EDITORIAL-REVIEW.md` is an earlier manuscript review, not the current PDF score. The only canonical shared Romans deliverable is `output/romans-consolidated.pdf`.

The true PDF starting point is the user's restored **348-page `romans-consolidated 3.pdf`**, archived byte-for-byte as `sources/archive/romans-original-baseline.pdf`. Its navy/gold cover, 7 × 10-inch format, full systematic study, five volume dividers, diagrams, sixteen chapters and back matter are authoritative.

The newer 221-page manuscript-generated edition is a secondary editorial reference, archived as `sources/archive/romans-editorial-reference.pdf`. Do not substitute its shorter structure or letter-size layout for the original PDF.

## Build the assigned PDF

Run `make pdf`. `make all` also builds only the assigned PDF. The repository's older build entry point delegates here. Python 3 and PyMuPDF are required; no PDF reflow is performed.

The only release output is `/Users/jimxiao/Documents/GitHub/pubhub/output/romans-consolidated.pdf`.

The builder validates the source SHA-256, applies measured editorial/cover corrections and chapter-number repairs, and verifies page preservation. Currently 196 pages are wholly unchanged and 144 further pages are compared outside approved rectangles; eight earlier corrected/cover pages retain their prior treatment. It retains 348 pages and all original printed page numbers. A failed comparison prevents replacement of the output. The report is `sources/audits/baseline-merge.json`.

Run `make pdf-audit` for reproducible Scripture and quotation comparisons of the actual PDF. Reference files are preserved in `sources/reference`; unresolved differences are not automatic errors or passes. See `sources/audits/substantive-review.md` for the latest comparable score, methodology and limits. Numbering labels require Times New Roman; `ROMANS_LABEL_FONT` can supply its full TTF path on other systems. `ROMANS_CANONICAL_PDF` supports a temporary proof path without changing the assigned release name.

## Source archives and other tooling

Keep both archived PDFs. Cleaning the shared output directory must never delete the original archive. The extracted text is a secondary recovery aid, not the layout authority.

Markdown files, `make check`, `make citations`, and `make test` remain editorial tools. Their counts describe the editable manuscript, not fresh quotation verification of the baseline PDF. Optional EPUB/HTML builds use the manuscript and are not equivalent releases of the authoritative PDF.

Rights, quotation evidence, theological review and accessibility approval remain separate editorial requirements. See `PUBLISHER-FIX-REPORT.md` and `SOURCE-RECONCILIATION.md` for scope and limits.
