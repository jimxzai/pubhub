# Jude — verified source texts

All files fetched 2026-10-01 with `curl` (browser UA) and stripped locally with Python. Nothing typed from memory. WebFetch was not used for any text in this folder. (The `hymns/` folder and `morgan-living-messages.norm.txt` were written by a different process and are not covered here.)

## Scripture

| File | Source / edition | Size | Notes |
|---|---|---|---|
| `cuv-jude.txt` | 和合本 (FHL "和合本", `unv`): `https://bible.fhl.net/json/qb.php?chineses=猶&chap=1&sec=1-25&version=unv&gb=0` | 3,166 B | 25 verses, `N<TAB>text`. Primary text. Keeps FHL's U+3000 space before 神 and its marginal notes (或譯：…). |
| `cuv-jude-aieden.txt` | ai-eden.com `https://www.ai-eden.com/api/bible/jude/1?t=CUV` (`textZh`) | 3,137 B | Second witness. One request only. |
| `cuvmpt-jude-cnbible.txt` | cnbible.com `https://www.cnbible.com/jude/1.htm`, first column | 3,100 B | **This is CUVMPT (modern punctuation), not the 1919 CUV.** Third witness only. |
| `cuv-jude-diff.txt` | character diff, FHL vs ai-eden, with notes | 1,925 B | 13 of 25 verses match exactly. The rest differ in punctuation or variant characters, with **one wording difference: v.4, where ai-eden has 「變放縱」 and lacks 作. FHL has 「變作」 and cnbible 「變做」.** ai-eden v.9 also has a stray `{`. |
| `nasb1995-jude.txt` | biblehub `https://biblehub.com/nasb/jude/1.htm` (page header "NASB 1995") | 3,732 B | Italic supplied words kept as `*word*` (vv.14, 16, 25). v.5 matches the expected 1995 wording exactly. Cross-checked against the English `text` field of the ai-eden API: identical except for quote style (' vs “ ”) and [brackets] vs italics. |
| `greek-jude.txt` | SBLGNT `https://raw.githubusercontent.com/LogosBible/SBLGNT/master/data/sblgnt/text/Jude.txt` | 6,493 B | Keeps the ⸀ ⸂ ⸃ sigla. |
| `greek-jude-sblgnt-apparatus.txt` | SBLGNT apparatus `.../data/sblgntapp/text/Jude.txt` | 2,054 B | Readings of WH, Treg, NA28 and RP. |
| `greek-counts.txt` | Counted by script from MorphGNT `https://raw.githubusercontent.com/morphgnt/sblgnt/master/86-Jud-morphgnt.txt` (lemmatized SBLGNT) | 3,170 B | Lemma counts with forms for each verse, plus a surface-regex cross-check and an explanation of each mismatch. |

## MacArthur (gty.org)

`gty-index.tsv` and `gty/65-1.txt` … `gty/65-15.txt`. Each is also cached as `/tmp/sermon-cache/gty-65-N.txt`, the name `scripts/verify-sermon-quotes.py` `fetch()` reads (it needs files over 5,000 B and normalizes on read). The cache holds the transcript only: the SSR `div.expand--content.hide` block. The copies in `gty/` add a three-line header.

- Enumeration: `https://www.gty.org/sitemap.xml` is a single urlset of 6,036 URLs. It lists exactly 15 `/sermons/65-N/` URLs, and the series pages `65V1` and `65V2` list the same 15.
- Codes are **not** zero-padded. `65-01` and `65-16`…`65-20` return an empty "65-01" stub page.
- Other gty sermons on Jude: I checked 55 sitemap sermons whose slugs looked related (apostasy, keep, security, doxology, Enoch, Cain, false teachers…), reading the scripture tag on each page. None is on Jude. The list is in `gty/other-candidates-checked.tsv`. **This is not a full scan of all 3,337 sermon URLs.** The gty scripture-browse and search pages render client-side only and gave no listing.
- Note: gty.org's robots.txt is reportedly `Disallow: /` (per project memory). Requests were sequential with 1 s spacing.

## Commentaries and patristic texts

| File | Source / edition | Size | Notes |
|---|---|---|---|
| `calvin-jude.txt` | Calvin, *Commentaries on the Catholic Epistles*, tr. John Owen (CCEL calcom45): `https://ccel.org/ccel/c/calvin/calcom45/cache/calcom45.txt`, lines 17927–18951 | 58,761 B | Runs from the Argument to "END OF THE EPISTLE OF JUDE", plus Owen's footnotes [187]–[204]. The `ccel.org/ccel/calvin/calcom45.txt` URL in the brief returns an HTML landing page. **The CCEL txt has no print page numbers.** This volume has no "Calvin's version" appendix for Jude (it has them for 1 Peter, 1 John and James only). |
| `clement-jude.txt` | Clement of Alexandria, "Comments on the Epistle of Jude" (Adumbrationes), ANF 2:573–574: `https://ccel.org/ccel/schaff/anf02/anf02.vi.iv.ix.html` | 8,876 B | The page break to 574 is marked inline. Word-for-word identical to the CCEL anf02.txt version. Footnotes 3751–3784 included. The ANF section also includes the closing Mark 14:62 paragraph, kept as printed. |
| `henry-jude.txt` | Matthew Henry's Commentary vol. VI, CCEL `https://ccel.org/ccel/h/henry/mhc6/cache/mhc6.txt`, lines 98057–99043 | 66,493 B | **Henry did not write the Jude section. The volume itself says it was "Completed by John Billingsley"**, so cite it as Henry/Billingsley. No page numbers. |
| `spurgeon-jude.txt` | spurgeon.org: No. 634 "Christians Kept in the Time and Glorified in Eternity" (MTP 11, 1865) and "Saints Guarded from Stumbling" (MTP 39, delivered 19 Feb 1893) | 68,742 B | The number for the second sermon, **No. 2296**, is not on spurgeon.org. It comes from answersingenesis.org ("No. 2296-39:85"), a secondary source. spurgeon.org lists 5 Spurgeon sermons on Jude in all; only the two on vv.24–25 were fetched. |
| `morgan-living-messages.txt` | G. Campbell Morgan, *Living Messages of the Books of the Bible: Matthew to Revelation* (Revell, 1912), "The Message of Jude", chart [193] and pp. 194–208. archive.org `livingmessagesof0000gcam` `_djvu.txt` | 18,325 B | **Raw OCR.** The p.193 two-column chart is cut off at the right edge. Running heads are kept as page markers. |
| `morgan-living-messages-scan2.txt` | Same edition, a second scan: archive.org `livingmessagesof0000gcam_e1y3` | 17,884 B | Agrees with the first scan on 98.6% of words, and its chart column B is more complete. Use the two together to correct OCR; check the page image before quoting. The Google scans `livingmessagesb00morggoog` and `livingmessagesof01morgiala` turned out to be the OT volume (no Jude). |
| `morgan-exposition.txt` | Morgan, *An Exposition of the Whole Bible* (StudyLight gives 1959): `https://www.studylight.org/commentaries/eng/gcm/jude-1.html` | 2,851 B | The first request got a Cloudflare 403. It worked with a cookie jar plus a Referer from the gcm index page. **Source defect: "The subject of the h e attitude of believers" is garbled on StudyLight itself.** It is a one-page survey of the whole epistle. |
| `morgan-analyzed-bible.txt` | Morgan, *The Analyzed Bible* vol. 3, *Introduction: Matthew to Revelation* (Revell, 1907), "Jude: Christ the Perfect and Perfecting Lord". archive.org `analyzedbible03morg` (Princeton Theological Seminary scan) `_djvu.txt`, lines 13480–13745 | 6,320 B | Raw OCR. Running heads 322 and 324 survive. **The start page is not established.** |
| `eusebius-jude.txt` | Eusebius, *Church History* (tr. McGiffert), NPNF2 vol. 1, CCEL HTML: 2.23 (`npnf201.iii.vii.xxiv`, begins p.125; §24 runs across pp.127–128; §25, with the James/Jude "disputed" remark, is on p.128), 3.19 and 3.20 (pp.148–149), 3.25 (begins p.155; §3 on p.156) | 70,431 B | Whole chapters, with page breaks inline and McGiffert's footnotes (n.530 on Jude's authenticity, n.720 on Jude, n.791). |
| `jerome-jude.txt` | Jerome, *De viris illustribus* ch. 4, tr. E. C. Richardson, NPNF2 3:362 (`npnf203.v.iii.vi`) | 823 B | The page comes from the neighbouring sections' page breaks: 362 in ch.2, 363 inside ch.5. |
| `muratorian.txt` | "Canon Muratorianus", ANF 5:603–604 (`anf05.v.iii.iii`, in the Caius fragments) | 8,118 B | The whole fragment. The Jude sentence is marked `>>>` and is on p.603. |
| `tertullian-enoch.txt` | Tertullian, *On the Apparel of Women* 1.3, tr. S. Thelwall, ANF 4:15–16 (`anf04.iii.iii.i.iii`) | 3,011 B | The ANF footnote cites Jude 14–15. |

## Known gaps

- There are no print page numbers for Calvin or Henry, because CCEL's txt has none.
- The start page of Morgan's *Analyzed Bible* Jude section is not established, and both Morgan OCR texts are uncorrected.
- The gty search for Jude sermons outside series 65 covered only candidates picked by slug.
- The Spurgeon No. 2296 comes from a secondary site.
- NA28 itself was not consulted. Its readings (Jude 5 Ἰησοῦς; v.15 πᾶσαν ψυχήν) come from the SBLGNT apparatus.

## hymns/ (added by the main session, 2026-10-01)

Fetched via the Wikisource API (`action=parse&prop=text`), HTML stripped locally; each file's first line gives its URL.

| File | Hymn | Printed edition transcribed |
|---|---|---|
| faith.txt | Faith of Our Fathers (Faber, 1849) | *A First Series of Hymns and Songs: Catholic Hymns* (1853), no. 37 |
| guideme.txt | Guide Me, O Thou Great Jehovah (W. Williams, tr. P. Williams) | *The Army and Navy Hymnal* (1920) |
| lohecomes.txt | Lo! He Comes with Clouds Descending (C. Wesley, 1758) | *A Selection of Hymns … Ulverston* (1863), Hymn 65 |
| rescue.txt | Rescue the Perishing (F. J. Crosby) | *The Army and Navy Hymnal* (1920); transcription has typos in stanza 2 ("chil", "belive") — stanza 2 not used |
| lovedivine.txt | Love Divine, All Loves Excelling (C. Wesley, 1747) | *The Army and Navy Hymnal* (1920) |

hymnary.org was not used: it serves modern altered texts by default ("Faith of the martyrs", "Guide me, O my great Redeemer") and a bot challenge on some pages.
