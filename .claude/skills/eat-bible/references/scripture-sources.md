# eat-bible — Scripture sourcing

Loaded on demand from `SKILL.md`. This is about **writing** a book's markdown
chapters, not about building the PDF — it lives with this skill because it is
the same content pipeline, but note that anyone writing chapters is unlikely
to invoke a skill described as a PDF builder. If that keeps costing us, this
section wants to become its own skill.

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

**Get the book slug right before concluding the site is down.** The slug is
the full English book name, not the common abbreviation: `isaiah`, **not**
`isa`. A wrong slug 404s, which reads exactly like "ai-eden is unreachable"
and sends agents to the fallback chain for no reason. In the Isaiah build
this cost **15 of 26 chapters** an unnecessary fallback, and the wrong
conclusion ("ai-eden is JS-rendered and can't be fetched") then propagated
into a dozen citation lines that had to be redone. Try the full name, and
retry once, before falling back.

**Ask for a diff, not for the text.** The reliable verification method is to
**paste the manuscript's verses into the prompt and ask for differences
only**, verse by verse:

> Compare this manuscript CUV text against the page's CUV and report ONLY
> character-level differences per verse; say "match" if identical.

Asking WebFetch to *reproduce* a passage fails two ways: requesting ESV text
can trip a copyright refusal, and when the fetcher does answer it silently
normalises verse-final punctuation and truncates long verses — which then
reads as a discrepancy that isn't one, and invites "corrections" that damage
correct text.

**ai-eden's own CUV has occasional artifacts.** Confirmed in Isaiah 60 and
63: wrong characters and a dropped clause, where the book was already right.
Cross-check against `cnbible.com` before "correcting" a manuscript to match
it; prefer the reading attested by both the second source and the book's own
internal usage.

**和合本 is not internally consistent, so never blanket-convert a character.**
The 做/作 pair is the trap: CUV genuinely uses 作 at Isa 1:1, 1:23, 2:6, 3:4,
22:21, 60:19-20, 63:8 and genuinely uses 做 at 2:8 and 5:4. Two agents in one
session reached opposite blanket conclusions — one "corrected" 做→作
everywhere, another declared the book's base text was CUVMP and left them all
— and both were wrong in different directions. Verify per verse.

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

## NASB (English) — sourcing that is actually verbatim

Several volumes (Philemon, Revelation, 2 Peter, Luke) use **NASB 1995**
for the English column. Sourcing rules learned 2026-08-31:

- **biblehub chapter pages, no underscore, are 1995:**
  `https://biblehub.com/nasb/luke/15.htm`. With a trailing underscore
  (`/nasb_/`) you get **NASB 2020**; the per-verse pages
  `biblehub.com/luke/15-20.htm` show both, labelled. Confirm the edition
  by content, not URL (彼後 3:10 "burned up" = 1995, "discovered" = 2020;
  提前 2:5 "God and men" = 1995, "and mankind" = 2020).
- **Ask WebFetch for a verse list, not the chapter** ("return verses 4, 5,
  6, 20–24 verbatim, one per line, and state the edition") — it declines a
  whole copyrighted chapter but complies with a list, and 24 chapters of
  Luke came back in one parallel round. Re-fetch any verse the extractor
  truncated or doubled the quote marks on; do not fill from memory.
- **Supplied words are italic in NASB** (biblehub renders them `_word_`).
  Keep them: `*word*` in markdown, `\textit{word}` inside a `\jesus{}` span.
- **Each NASB verse in continuing speech re-opens a quotation mark**
  (`^21^"Blessed…`). When joining verses into one blockquote paragraph,
  keep only the opening and closing marks — that is layout, not text.
- OT quotations are ALL CAPS in NASB; leave them so.
- **Copyright page wording** (build script `copyright:` block):
  `Scripture quotations taken from the New American Standard Bible® (NASB),
  Copyright © 1960, 1971, 1977, 1995 by The Lockman Foundation. Used by
  permission. All rights reserved. lockman.org`. Also change the template's
  `$else$` fallback copyright block, the overview key verse, the appendix
  版本 line, and every `經文核對` link (`t=CUV,NASB`) — `grep -rn ESV` on
  the book directory, the build script and the template until it is empty.

## CUV by the chapter — a cheaper second source

`bible.fhl.net/new/read.php?VERSION1=unv&TABFLAG=1&chineses=<書>&chap=<n>`
(書 URL-encoded, e.g. 詩=%E8%A9%A9, 彼後=%E5%BD%BC%E5%BE%8C) returns clean
和合本 for a whole chapter — far cheaper than cnbible per-verse pages, and
a useful second source to diff against. Then run
`python3 scripts/lint-scripture-text.py <dir>` for the variant-character
classes (鑒/鑑, 熔/鎔, 汙/污, 裡/裏, 做/作 — rules are word-scoped because
CUV itself is mixed; the script refuses to auto-fix the 做/作 class).
