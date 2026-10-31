# Haggai — source texts

Fetched 2026-10-31 with `curl` (browser UA). Scripture and commentary files
were not typed from memory. Counts of Hebrew words come from
`count_hebrew.py` run on `hebrew/wlc-hag.xml`.

## Scripture

| File | Source | Notes |
|---|---|---|
| `scripture/cuv-haggai.txt` | ai-eden.com `https://www.ai-eden.com/api/bible/haggai/{1,2}?t=CUV` (`textZh`), 裡→裏 | Primary 和合本 text used in the book (`cuv-haggai-{1,2}.json` = raw) |
| `scripture/cuv-haggai-fhl.txt` | bible.fhl.net unv (`chineses=該&chap=N&sec=1-15/1-23`) | Second witness; differs from ai-eden at 1:4, 2:3, 2:12, 2:13, 2:19 (麼 / 嗎, plus FHL's added quotation marks) and 2:4 (作工 / 做工) |
| (not stored) | cnbible.com `haggai/2-4.htm` | Third witness for 2:4: its CUV (繁體中文和合本) reads 作工, its 現代標點和合本 reads 做工; ai-eden's 作工 is kept |
| `scripture/nasb1995-haggai.txt` | biblehub.com `https://biblehub.com/nasb/haggai/{1,2}.htm` (raw: `nasb-raw-{1,2}.html`) | NASB 1995; italics = supplied words; section headings removed |
| (not stored) | biblegateway.com NASB1995 `Haggai+1`, `Haggai+2` | Second witness: identical to biblehub after removing footnote letters (compared chapter by chapter on letters only) |
| `scripture/xref/*.json` | bible.fhl.net unv | Every other 和合本 verse quoted in the prose, cached by `cuv.py`-style lookups |
| `hebrew/wlc-hag.xml` | github.com/openscriptures/morphhb `wlc/Hag.xml` | WLC with OSHB lemma/morph tags; `hebrew/haggai-vowelled.txt` = verse text without cantillation |

## Commentary

| File | Source | Notes |
|---|---|---|
| `commentary/calvin-haggai.txt` | CCEL `calcom29` (Calvin, *Commentaries on the Twelve Minor Prophets*, vol. 4, tr. John Owen), `…/cache/calcom29.txt` lines 11958–15270 | Includes Calvin's Preface to Haggai and Owen's editorial footnotes (Ed.) — those are not Calvin |
| `commentary/henry-haggai.txt` | CCEL `mhc4` (Matthew Henry, Isaiah–Malachi), `…/cache/mhc4.txt` lines 120291–121312 | No page numbers |
| `commentary/morgan-living-messages-haggai-ocr.txt` | archive.org `livingmessagesof0000gcam_p4q1` djvu text, "The Message of Haggai" pp. 303–315 | Raw OCR; running heads kept. Page numbers were checked against the scanned PDF's text layer (pdf pp. 590–603 = printed pp. 302–315) |

## MacArthur

None. gty.org `sitemap.xml` (downloaded 2026-10-31) has no `/sermons/37-N` URL
(37 = Haggai) and no sermon slug naming Haggai.

## Hymns

Not re-fetched for this book. The stanzas are copied from chapters of this
repository that already carry them: *Take My Life* (Havergal, 1874) from
`thessanlonian1/03`; *How Firm a Foundation* stanza 3 ("Fear not, I am with
thee") from `james/01`; *Glorious Things of Thee Are Spoken* (Newton, 1779)
from `kings2/11`; *Rock of Ages* (Toplady) from `lamentation/08`;
*O God, Our Help in Ages Past* (Watts, 1719) stanza 1 from the kings2 hymn
bank and the "Time, like an ever-rolling stream" stanza from `ecclesiastes/03`.
