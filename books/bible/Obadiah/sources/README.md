# Obadiah — source texts

Fetched 2026-10-30 with `curl` (browser UA). Scripture and commentary files
were not typed from memory. Counts of Hebrew words come from
`count_hebrew.py` run on `hebrew/wlc-obad.xml`.

## Scripture

| File | Source | Notes |
|---|---|---|
| `scripture/cuv-obadiah.txt` | ai-eden.com `https://www.ai-eden.com/api/bible/obadiah/1?t=CUV` (`textZh`), 裡→裏 | Primary 和合本 text used in the book |
| `scripture/cuv-obadiah-aieden.json` | same, raw JSON | |
| `scripture/cuv-obadiah-fhl.txt` | bible.fhl.net unv (`chineses=俄&chap=1&sec=1-21`) | Second witness; differs from ai-eden only at v.1 (吧/罷), v.18 (焰/燄), v.19 (馬/瑪) |
| `scripture/nasb1995-obadiah.txt` | biblehub.com `https://biblehub.com/nasb/obadiah/1.htm` (header "NASB 1995") | Italics = supplied words; section headings removed |
| (not stored) | biblegateway.com NASB1995 `Obadiah+1` | Second witness, identical after stripping footnote markers |
| `scripture/xref/*.json` | bible.fhl.net unv | Every other 和合本 verse quoted in the prose, cached |
| `hebrew/wlc-obad.xml` | github.com/openscriptures/morphhb `wlc/Obad.xml` | WLC with OSHB lemma/morph tags |

## Commentary

| File | Source | Notes |
|---|---|---|
| `commentary/calvin-obadiah.txt` | CCEL `calcom27` (Calvin, *Commentaries on the Twelve Minor Prophets*, vol. 2, tr. John Owen), lines 15776–17250 | Includes Owen's editorial footnotes (Ed.) — those are not Calvin |
| `commentary/henry-obadiah.txt` | CCEL `mhc4` (Matthew Henry, Isaiah–Malachi), the Obadiah section | Henry wrote the whole OT; no page numbers |
| `commentary/morgan-living-messages-obadiah-ocr1.txt` | archive.org `livingmessagesof0000gcam_p4q1` djvu text, "The Message of Obadiah" pp. 213–225 | Raw OCR; running heads kept |
| `commentary/morgan-living-messages-obadiah-ocr2.txt` | archive.org `livingmessagesof0000unse` djvu text | Second scan; used to settle OCR doubts |

## MacArthur

None. gty.org `sitemap.xml` (downloaded 2026-10-30) has no `/sermons/31-N` URL
(31 = Obadiah) and no sermon slug naming Obadiah.

## Hymns

Wikisource, parsed with the MediaWiki `action=parse` API: *The Army and Navy
Hymnal* (1920) for Watts ×2, Toplady, Alexander; *A Selection of Hymns … Ulverston*
(1863) Hymn 21 for Newton.
