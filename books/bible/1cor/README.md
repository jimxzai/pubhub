# 哥林多前書研讀

This repository contains the canonical consolidated edition of the PubHub study volume on 1 Corinthians.

## Production status

The manuscript is the single canonical consolidated review proof, not a final public release. Rights clearance, theological review, proofreading, and final metadata are still required before distribution.

The consolidated builder restores the reference edition's systematic study, five volume divisions, all sixteen chapters, closing material, and appendices A-F. `outline.md` remains editorial source material.

`rights-log.md` is an internal clearance register and is not part of the reader edition.

## Build and QA

Requirements: Pandoc, XeLaTeX, Python 3 with pypdf, STSong, Arial Unicode MS, and Times New Roman. The restored template contains the original vector artwork and appendices. PDF output is compiled directly to preserve navigation.

```sh
make verify
make html
make pdf
make epub
```

`make verify` checks the controlled file list, front matter, chapter numbering, raw TeX leakage, unresolved editorial markers, and Markdown fences. Rendering must still be followed by visual page inspection.

Run `make all` to build every format and audit the artifacts. Local `output/` files are staging files; the assigned publication location is `/Users/jimxiao/Documents/GitHub/pubhub/output/1cor-consolidated.pdf`. HTML embeds resources and EPUB includes its cover. PDF compilation retains auxiliary files until the contents page stabilizes.

After visual approval, `python3 scripts/publish_consolidated.py` installs the audited PDF, HTML, and EPUB at the assigned project output location. It backs up replaced files and moves obsolete combined Markdown/build logs to a printed recovery folder under `/private/tmp`. It also routes the project-level consolidated build entry point through this builder. Writing the parent project requires permission in a restricted workspace. This installs a review proof, not a rights-cleared public release.

## Editorial policy

- The Chinese Bible text is labeled as the 1919 Chinese Union Version and requires territory-specific rights confirmation.
- English Bible material is labeled as selected NASB 1995 readings unless a complete parallel text is intentionally licensed.
- Unverified commentary is editorial paraphrase, not a verbatim quotation.
- The biblical author's name and the book's author/editor are separate metadata fields.
- The restored LaTeX template supplies the vector cover, diagrams, maps, front matter, and appendices. Digital appendices are converted from this same source.
