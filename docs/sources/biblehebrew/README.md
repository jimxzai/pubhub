# Biblehebrew — source corpus

Used by `books/bible/Biblehebrew/` (《讀懂聖經的希伯來文》) and `books/bible/Biblehebrew-compendium/` (《舊約希伯來文彙編》).
Nothing here was typed from memory.

| File | What | Fetched |
|------|------|---------|
| `oshb/*.xml` | OSHB (Open Scriptures Hebrew Bible): the Westminster Leningrad Codex with lemma and morphology tags, 39 books (OSIS XML). `https://raw.githubusercontent.com/openscriptures/morphhb/master/wlc/<Book>.xml` | 2026-11-01, `curl` |
| `HebrewStrong.xml` | Strong's Hebrew Dictionary in the Open Scriptures edition: pointed Hebrew form, part of speech, definition. `https://raw.githubusercontent.com/openscriptures/HebrewLexicon/master/HebrewStrong.xml` | 2026-11-01, `curl` |
| `scripture-excerpts.json` | The few CUV/NASB 1995 verses the guide quotes. CUV from ai-eden's `data/cuv.json`; NASB 1995 from biblehub.com chapter pages (`https://biblehub.com/nasb/<book>/<chapter>.htm`), cross-checked against the live ai-eden.com pages on 2026-11-01 | 2026-11-01 |
| `hymns.json` | Public-domain English hymn texts and their provenance (Wikisource transcriptions) | 2026-11-01 |
| `SHA256SUMS` | Checksums of `oshb/*.xml` and `HebrewStrong.xml` as fetched, to detect upstream drift: `shasum -a 256 -c SHA256SUMS` | |

`series-wordstudies.json` (not tracked) is derived from the OT books' 原文研讀 tables by `scripts/mine-hebrew-wordstudies.py`.

## Licence and attribution

- **OSHB:** based on the Westminster Leningrad Codex, which is in the public domain; the Open Scriptures lemma and morphology data are licensed CC BY 4.0
  (see `https://github.com/openscriptures/morphhb/blob/master/LICENSE.md`). Required attribution:
  *"Original work of the Open Scriptures Hebrew Bible available at https://github.com/openscriptures/morphhb"* — printed on both books' copyright pages.
- **HebrewStrong.xml:** Strong's dictionary is an old public-domain work; the Open Scriptures edition's own licence terms are not stated in that repository's readme,
  and were not independently confirmed here. Check `https://github.com/openscriptures/HebrewLexicon` before redistributing the file outside this repository.
- **NASB 1995:** quoted under the Lockman Foundation notice printed on the copyright pages; only a handful of verses.
