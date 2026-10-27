# 雅歌研讀 — 單元表與來源任務（2026-10-26）

目錄 `books/bible/songofsolomen/`；slug `songofsolomen`；建置 `scripts/build-songofsolomen-consolidated.sh`；模板 `templates/pdf/songofsolomen.latex`；PDF `output/songofsolomen-consolidated.pdf`。
經文來源：ai-eden 書卷代碼 `song-of-solomon`（JSON 已在 `.sources/ai-eden/ch1..8.json`，欄 verse/text=NASB/textZh=和合本）。
節號 = 英文／和合本節號（希伯來文版 6:13 = 英 6:13 的後半移為 7:1；英 7:1-13 = 希伯來 7:2-14；英 1:1 = 希 1:1；希 4:1—5:1 一致；其餘見 Sefaria 節號對照，**mapping 由處理者核對**）。

## 單元表（「章」= 本書研讀單元；H1 序號 1–15 連續，H1 標題不夾經文章號）

| # | 檔名 | 暫定 H1 | 範圍 | 卷 |
|---|---|---|---|---|
| 01 | 01-let-him-kiss-me.md | 願他用口與我親嘴 (Let Him Kiss Me) | 歌 1:1-4 | 一 |
| 02 | 02-black-but-lovely.md | 我雖然黑，卻是秀美 (Dark, Yet Lovely) | 歌 1:5-8 | 一 |
| 03 | 03-rose-of-sharon.md | 沙崙的玫瑰，谷中的百合 (The Rose of Sharon) | 歌 1:9-2:7 | 一 |
| 04 | 04-the-voice-of-my-beloved.md | 聽啊，是我良人的聲音 (The Voice of My Beloved) | 歌 2:8-17 | 一 |
| 05 | 05-by-night-on-my-bed.md | 我夜間在床上尋找 (By Night on My Bed) | 歌 3:1-5 | 一 |
| 06 | 06-solomons-litter.md | 所羅門王的轎 (The Litter of Solomon) | 歌 3:6-11 | 一 |
| 07 | 07-you-are-altogether-beautiful.md | 我的佳偶，你全然美麗 (All Fair, My Love) | 歌 4:1-15 | 二 |
| 08 | 08-the-garden-opened.md | 願我的良人進入自己的園裏 (The Garden Opened) | 歌 4:16-5:1 | 二 |
| 09 | 09-i-opened-but-he-was-gone.md | 我開門，他卻轉身走了 (I Opened, But He Was Gone) | 歌 5:2-8 | 三 |
| 10 | 10-white-and-ruddy.md | 我的良人白而且紅 (My Beloved Is White and Ruddy) | 歌 5:9-6:3 | 三 |
| 11 | 11-fair-as-tirzah.md | 美麗如得撒，威武如展開旗幟的軍隊 (Fair as Tirzah) | 歌 6:4-13 | 三 |
| 12 | 12-how-beautiful-and-pleasant.md | 王的心被髮綹纏住 (How Beautiful, How Pleasant) | 歌 7:1-9 | 四 |
| 13 | 13-his-desire-is-for-me.md | 他也戀慕我 (His Desire Is for Me) | 歌 7:10-8:4 | 四 |
| 14 | 14-set-me-as-a-seal.md | 求你將我放在心上如印記 (Set Me as a Seal) | 歌 8:5-7 | 四 |
| 15 | 15-make-haste-my-beloved.md | 我的良人哪，願你快來 (Make Haste, My Beloved) | 歌 8:8-14 | 四 |

四卷：一 渴慕與尋見（1–6，歌 1:1–3:11）／二 園子的敞開（7–8，歌 4:1–5:1）／三 失落與重尋（9–11，歌 5:2–6:13）／四 渴想的反轉與印記（12–15，歌 7:1–8:14）。

## 來源任務

- **S1（biblehub 每節注疏）**：`https://biblehub.com/commentaries/songs/<章>-<節>.htm`（已驗：`songs/1-2.htm` 回 200）。逐節抓 117 節，限速（每請求間隔 ≥ 2 秒，出現 429／空殼就退避），各注疏者分檔：`commentary/<src>-NN.txt`（NN = 本書單元序號 01..15，即把該單元範圍內的節合併），檔內每段以 `===== [Song of Solomon C:V] =====` 起頭，檔頂一行出處。要抓的注疏者：Pulpit Commentary、Keil & Delitzsch、JFB、Gill、Clarke、Ellicott、Cambridge Bible、Barnes（若有）、Benson、Coke、Poole、Matthew Henry（biblehub 版，僅作備援）等 biblehub 頁面實有者；每位寫入 `commentary/_INDEX.txt`（有哪些、各有幾節、約幾字）。
- **S2（長篇）**：(a) 馬太·亨利 vol. III 全文 `https://ccel.org/ccel/h/henry/mhc3/cache/mhc3.txt`（已驗 200），抽出 Song of Solomon 段，依單元切成 `commentary/henry-NN.txt`；(b) 戴德生《Union and Communion》（Gutenberg #26172；archive id `unionandcommunio26172gut`）全文 → `commentary/taylor-union-and-communion.txt`，並建「戴德生所講經節 → 段落」索引；(c) 伯爾拿《雅歌講道集》公有領域英譯（Eales 1895 或同期；先找可 curl 的全文，archive.org/ccel），**只做可定位的逐篇檔**；(d) 摩根 *The Analyzed Bible* 中雅歌段落（先找出哪一冊，用 `scripts/normalize-ocr-source.py` 清洗）；(e) 司布真論雅歌經節的講道（spurgeongems.org／ccel 的 Metropolitan Tabernacle Pulpit，列出可用清單與網址，抓 3–6 篇最相關的全文）。(f) 確認 **麥克阿瑟無雅歌逐節講道**（gty.org 站點地圖已查：無；`.sources/gty-sitemap.xml`），另找 gty.org 是否有「Song of Solomon」書卷導論頁，有則只記網址，不入引文庫。
- **S3（經文與原文）**：以 `.sources/ai-eden/ch*.json` 為主，抓 fhl（`unv`）與 cnbible 作和合本第二／第三來源三向比對，寫 `CUV-DIFF-REPORT.txt`；NASB 與 ai-eden 對校（biblehub 1995 章頁）；Sefaria 取希伯來文（Miqra according to the Masorah，去讀經符號保留母音）→ `hebrew/song-he.tsv`（`章:節<TAB>經文`，**用英文節號標示並註明對應的希伯來節號**）；`scripture-NN.tsv`（NN=單元 01..15？不——沿用 Ezra：NN=雅歌章 1..8；欄：節、ai-eden 和合本、fhl 和合本、ai-eden NASB）；`units/<檔名>.scripture.md`（15 個，格式同 `books/bible/ezra/.sources/units/01-*.scripture.md`）。**ai-eden 的 `（新娘）（新郎）（耶路撒冷的眾女子）` 等括號是和合本的講者標題、附在上一節末尾，不是經文：從節文中移出，另建 `speakers.tsv`（單元、節、講者、依據）；`（或譯：…）`邊注保留為節末括號。**
