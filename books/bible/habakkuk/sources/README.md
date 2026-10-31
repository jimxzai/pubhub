# Habakkuk — source texts

Fetched 2026-10-31 with `curl` (browser UA). Scripture and commentary files
were not typed from memory. Counts of Hebrew words come from
`count_hebrew.py` run on `hebrew/wlc-hab.xml`.

## Scripture

| File | Source | Notes |
|---|---|---|
| `scripture/aieden-hab-N.json` | ai-eden.com `https://www.ai-eden.com/api/bible/habakkuk/N?t=CUV,NASB` | `textZh` = 和合本（本書底本，裡→裏）；`text` = NASB（與 biblehub 比對用） |
| `scripture/cuv-hab-N.txt` | derived from the JSON above | one verse per line |
| `scripture/fhl-hab-N.json` | bible.fhl.net `qb.php?chineses=哈&chap=N&version=unv` | Second witness. Differs from ai-eden in 13 verses: 1:4 punctuation（，／；）, 1:12/3:3/3:18 `神` spacing, 1:12/2:7/2:13/2:19/3:8 麼↔嗎, 2:11 棟梁↔棟樑, 2:17 利巴嫩↔黎巴嫩, 2:18 他↔它, 3:11 標點, 3:12 憤恨↔忿恨. Policy: ai-eden is the base text. |
| `scripture/bh-nasb-N.html` | biblehub.com `https://biblehub.com/nasb/habakkuk/N.htm` | NASB 1995; italics = supplied words |
| `scripture/nasb1995-hab-N.txt` | `parse_nasb.py` on the HTML | one verse per line, `*italic*` kept; identical to ai-eden NASB ignoring punctuation and italics (0 diffs) |
| `scripture/units/NN.md` | `gen_scripture_blocks.py` | the 經文 block pasted into each chapter (中文／English) |
| `hebrew/wlc-hab.xml` | github.com/openscriptures/morphhb `wlc/Hab.xml` | WLC with OSHB lemma/morph tags; 56 verses, 672 `<w>` tokens |
| `hebrew.tsv`, `heb.py` | derived from the XML | `heb.py 2:4` prints a verse without cantillation |
| `lexicon/LexicalIndex.xml`, `HebrewStrong.xml`, `bdb-short.tsv` | github.com/openscriptures/HebrewLexicon | BDB short glosses by Strong number for every lemma in Habakkuk. Short glosses only; no full BDB entries, no HALOT |
| `cuv.py` | bible.fhl.net unv JSON, cached in `cuvcache.json` | `cuv.py '羅 1:17'` — used for every cross-reference quoted in the prose |

## Commentary

| File | Source | Notes |
|---|---|---|
| `commentary/calvin-habakkuk.txt` | CCEL `calcom29` (`https://ccel.org/ccel/calvin/calcom29/cache/calcom29.txt`), Calvin, *Commentaries on the Twelve Minor Prophets*, vol. 4 (Habakkuk, Zephaniah, Haggai), tr. John Owen; the Habakkuk portion (preface through Lecture 117) | Contains Owen's editorial footnotes (`[n]` … `--Ed.`) — those are not Calvin. `calvin-index.txt` lists verse headings with line numbers. |
| `commentary/henry-hab-{i,ii,iii,iv}.html`, `henry-habakkuk.txt` | CCEL `mhc4.Hab.i` … `iv` (`https://www.ccel.org/ccel/henry/mhc4.Hab.i.html`) | Henry wrote the whole OT commentary; i = introduction, ii/iii/iv = chapters 1/2/3 |
| `commentary/morgan-living-messages-habakkuk-ocr1.txt` | archive.org `livingmessagesof0000gcam_p4q1` djvu text, "The Message of Habakkuk," pp. 273-286 | Raw OCR; running heads kept. Morgan's chapter in this scan ends at p. 286 |
| `commentary/morgan-living-messages-habakkuk-ocr2.txt` | archive.org `livingmessagesof0000unse` djvu text | Second scan; settles OCR doubts |
| `commentary/augustine-cityofgod-18-32-33.txt` | New Advent, Augustine, *The City of God*, Book 18 ch. 32-33, tr. Marcus Dods | Augustine reads the Latin (Septuagint-family) text of Hab 3, not the Hebrew |

## MacArthur

None. gty.org `sitemap.xml` (downloaded 2026-10-31) has no `/sermons/35-N` URL
(35 = Habakkuk) and no sermon slug naming Habakkuk.

## Hymns

Wikisource, *The Army and Navy Hymnal* (1920), via the MediaWiki raw page
interface (page numbers per hymn from the hymn's index page). See the
appendix 〈引用出處總表〉 for the chapter-by-chapter list.
