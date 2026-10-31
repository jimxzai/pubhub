# Nahum — source texts

Fetched 2026-10-31 with `curl` (browser UA). Scripture and commentary files
were not typed from memory. Counts of Hebrew words come from
`count_hebrew.py` run on `hebrew/wlc-nah.xml`.

## Scripture

| File | Source | Notes |
|---|---|---|
| `scripture/cuv-nahum.txt` | ai-eden.com `https://www.ai-eden.com/api/bible/nahum/{1,2,3}?t=CUV` (`textZh`), 裡→裏 | Primary 和合本 text used in the book; tab-separated `chapter:verse<TAB>text` |
| `scripture/cuv-nahum-{1,2,3}-aieden.json` | same, raw JSON | |
| `scripture/cuv-nahum-fhl.txt` | bible.fhl.net `json/qb.php` (unv, `chineses=鴻`) | Second witness; differs from ai-eden in 12 of 47 verses (punctuation, variant characters, 他/她, small notes — see `99-appendix-references.md`) |
| `scripture/nasb1995-nahum.txt` | biblehub.com `https://biblehub.com/nasb/nahum/{1,2,3}.htm` (header "NASB 1995") | Italics = supplied words; section headings removed. **No second witness was compared.** |
| `scripture/xref/*.json` | bible.fhl.net unv | Every other 和合本 verse quoted in the prose, cached by `xref.py` |
| `hebrew/wlc-nah.xml` | github.com/openscriptures/morphhb `wlc/Nah.xml` | WLC with OSHB lemma tags; **Hebrew verse numbering** (Heb 2:1 = English 1:15) |
| `hebrew/wlc-nah-plain.txt` | derived from the above | cantillation marks stripped, **English verse numbering**, one verse per line |

Other WLC books consulted for comparisons (not stored; fetched from the same repo): `Exod.xml`, `Num.xml`, `Isa.xml`, `Jonah.xml`, `Jer.xml`.

Helper scripts: `scripture_block.py` (emits the 經文 blocks from the two files above), `splice.py` (fills `@@HYMN@@`/`@@SCRIPTURE@@` placeholders), `xref.py` (fetches/caches cross-reference verses), `count_hebrew.py` (reproduces every Hebrew count printed in the book).

## Commentary

| File | Source | Notes |
|---|---|---|
| `commentary/calvin-nahum.txt`, `calvin-nahum-clean.txt` | CCEL `calcom28` (Calvin, *Commentaries on Jonah, Micah, and Nahum*, tr. John Owen), the Nahum section | Includes Owen's editorial footnotes (Ed.) — those are not Calvin. The raw ThML download was not kept; URL `https://www.ccel.org/ccel/calvin/calcom28.xml` |
| `commentary/henry-nahum.txt` | CCEL `mhc4` (Matthew Henry, Isaiah–Malachi), pages `Nah.i`–`Nah.iv` | Henry wrote the whole OT; no page numbers |
| `commentary/morgan-living-messages-nahum-ocr1.txt` | archive.org `livingmessagesof0000gcam_p4q1` djvu text, "The Message of Nahum" (about pp. 257–272) | Raw OCR; running heads kept |
| `commentary/morgan-living-messages-nahum-ocr2.txt` | archive.org `livingmessagesof0000unse` djvu text | Second scan; used to settle OCR doubts |

## MacArthur

None. gty.org `sitemap.xml` (downloaded 2026-10-31) has no `/sermons/34-N` URL
(34 = Nahum) and no page naming Nahum.

## Hymns

Wikisource (MediaWiki `action=parse`): *Olney Hymns* (1840 ed.) for Cowper;
*A Selection of Hymns … Ulverston* (1863) Hymn 48; *The Army and Navy Hymnal*
(1920) for Luther/Hedge, Watts ×2. `hymns/hymn-blocks.md` holds the pasted blocks; the
three small corrections made are listed in `99-appendix-references.md` §六.
