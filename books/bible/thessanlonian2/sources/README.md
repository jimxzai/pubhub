# 帖撒羅尼迦後書 — 來源文本 (sources)

本目錄保存本書核對所用的原始文本，讓任何人都能重跑檢查，不必信任書稿自己的「已核對」。

## 已收入

| 路徑 | 內容 | 來源 |
|---|---|---|
| `scripture/cuv.tsv` | 帖後47節和合本（FHL unv，依本書用字體例正規化） | `bible.fhl.net/json/qb.php?version=unv` |
| `scripture/cuvmpt.tsv` | 現代標點和合本，第二來源 | `cnbible.com/cuvmpt/2_thessalonians/N.htm` |
| `scripture/nasb1995.tsv` | NASB 1995 | `biblehub.com/nasb/2_thessalonians/N.htm`；以 `nasb1995-biblegateway-N.html` 比對 |
| `scripture/sblgnt-2th-morphgnt.txt` | 帖後希臘文（SBLGNT＋MorphGNT 標註） | github.com/morphgnt/sblgnt |
| `commentary/calvin-2thess.txt` | 加爾文帖後註釋（Pringle 英譯） | CCEL calcom42 切出 |
| `commentary/chrysostom-2thess.txt` | 屈梭多模帖後講道集 | CCEL NPNF1-13 切出 |
| `commentary/augustine-civdei-20-19.txt` | 奧古斯丁《上帝之城》20.19 | CCEL NPNF1-02 切出 |
| `commentary/henry-2thess.txt` | 《聖經全註》帖後（實為 Daniel Mayo 續寫） | CCEL mhc6 切出 |
| `commentary/morgan-message-of-2thess.txt` | 摩根〈The Message of II. Thessalonians〉 | archive.org `livingmessagesof0000gcam` OCR 切出 |
| `commentary/gty/53-N.txt`、`gty-cache/` | 麥克阿瑟帖後講道 53-1 至 53-17 逐字稿 | gty.org |
| `hymns/*.txt` | 七首配詩的公有領域印本文字 | Wikisource（*The Army and Navy Hymnal*, 1920 等） |

## 未收入（體積大，需要時重新下載）

整卷原檔只用來切出上表各檔，不進版本庫：CCEL `calcom42.txt`、`npnf113.txt`、`npnf102.txt`、`mhc6.txt`，archive.org 摩根全卷 OCR，gty.org 講道 HTML 原頁，以及全新約 SBLGNT（`sources/scripture/gen_greek_appendix.py --sblgnt <dir>` 與 `nt_lemma_count.py` 需要它）：

```bash
for f in 61-Mt 62-Mk 63-Lk 64-Jn 65-Ac 66-Ro 67-1Co 68-2Co 69-Ga 70-Eph 71-Php 72-Col \
         73-1Th 74-2Th 75-1Ti 76-2Ti 77-Tit 78-Phm 79-Heb 80-Jas 81-1Pe 82-2Pe 83-1Jn \
         84-2Jn 85-3Jn 86-Jud 87-Re; do
  curl -s https://raw.githubusercontent.com/morphgnt/sblgnt/master/$f-morphgnt.txt \
       -o sources/scripture/sblgnt-nt/$f.txt
done
```

## 重跑檢查

見 `docs/scores/2-thessalonians-2026-10-01.md` 各輪所列的指令。
