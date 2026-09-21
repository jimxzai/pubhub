# 哥林多後書研讀：十字架事奉
## 2 Corinthians — Be His Servant: Ministry of the Cross

> CONSOLIDATED 2026 EDITION｜唯一指定出版版本；交付格式：PDF、EPUB

> **「祂對我說：『我的恩典夠你用的，因為我的能力是在人的軟弱上顯得完全。』**
> **所以，我更喜歡誇自己的軟弱，好叫基督的能力覆庇我。」**
> — 哥林多後書 12:9

---

## 課程資訊

- **教會**: 基督會堂 (CCIC Sunnyvale) 主日學
- **時間**: 2026年3月 - 2026年8月 (24課)
- **教會網站**: [CCIC Sunnyvale](https://www.ccic-sunnyvale.org/)（原主日學課程頁 `/sunday-school` 已下架）
- **教材**: [Google Drive](https://drive.google.com/drive/folders/11O1LnvKwyiw3ILxY3lV1q1-N4wgpN-fr)
- **經文**: [ai-eden.com/bible/2-corinthians](https://ai-eden.com/bible/2-corinthians)

---

## 目錄

- [課程概覽](00-overview.md) — 書卷簡介、大綱、關鍵詞彙、24課進度表
- [版權與版本說明](000-copyright.md) — 工作稿狀態與正式發行前提
- [出版工作流程](RELEASE-CHECKLIST.md) — 版本、權利與發行前檢查
- [權利與來源登錄表](RIGHTS-LEDGER.md) — 聖經版本、詩歌與注疏來源
- [內部課堂筆記](cor2.md) — 僅供編輯參考，不進入正式發行檔

### Part 1: 在苦難中顯出僕人的真實和榮耀 (Ch 1-7)

| # | 日期 | 主題 | 經文 | 筆記 |
|----------------|----------------|----------------|----------------|----------------|
| 01 | 03/01 | 患難安慰 | 1:1-11 | [筆記](01-comfort.md) |
| 02 | 03/08 | 誠實事奉 | 1:12-24 | [筆記](02-sincerity.md) |
| 03 | 03/15 | 饒恕修復 | 2:1-11 | [筆記](03-forgiveness.md) |
| 04 | 03/22 | 馨香之氣 | 2:12-17 | [筆記](04-aroma-of-christ.md) |
| 05 | 03/29 | 新約執事 | 3:1-6 | [筆記](05-new-covenant-ministers.md) |
| 06 | 04/05 | 榮上加榮 | 3:7-18 | [筆記](06-glory-to-glory.md) |
| 07 | 04/12 | 光照人心 | 4:1-6 | [筆記](07-light-of-gospel.md) |
| 08 | 04/19 | 瓦器寶貝 | 4:7-12 | [筆記](08-jars-of-clay.md) |
| 09 | 04/26 | 永恆眼光 | 4:13-18 | [筆記](09-eternal-perspective.md) |
| 10 | 05/03 | 天家盼望 | 5:1-10 | [筆記](10-heavenly-dwelling.md) |
| 11 | 05/10 | 和好使命 | 5:11-21 | [筆記](11-ministry-reconciliation.md) |
| 12 | 05/17 | 分別為聖 | 6:1-7:1 | [筆記](12-set-apart.md) |

### Part 2: 真使徒的記號、愛中的權柄與十字架能力 (Ch 7-13)

| # | 日期 | 主題 | 經文 | 筆記 |
|----------------|----------------|----------------|----------------|----------------|
| 13 | 05/24 | 敞開心門 | 7:2-7 | [筆記](13-open-hearts.md) |
| 14 | 05/31 | 憂愁悔改 | 7:8-16 | [筆記](14-godly-sorrow.md) |
| 15 | 06/07 | 恩典奉獻 | 8:1-9 | [筆記](15-grace-of-giving.md) |
| 16 | 06/14 | 忠心管理 | 8:10-24 | [筆記](16-faithful-stewardship.md) |
| 17 | 06/21 | 甘心樂意 | 9:1-7 | [筆記](17-cheerful-giver.md) |
| 18 | 06/28 | 感恩榮神 | 9:8-15 | [筆記](18-thanksgiving-glory.md) |
| 19 | 07/05 | 屬靈爭戰 | 10:1-6 | [筆記](19-spiritual-warfare.md) |
| 20 | 07/12 | 真實權柄 | 10:7-18 | [筆記](20-true-authority.md) |
| 21 | 07/19 | 純正福音 | 11:1-15 | [筆記](21-pure-gospel.md) |
| 22 | 07/26 | 軟弱誇口 | 11:16-33 | [筆記](22-boasting-in-weakness.md) |
| 23 | 08/02 | 刺中恩典 | 12:1-10 | [筆記](23-thorn-and-grace.md) |
| 24 | 08/09 | 愛中權柄 | 12:11-13:14 | [筆記](24-authority-in-love.md) |

---

**開始日期**: 2026-03-01
**最後更新**: 2026-09-20

## 建置與驗證

需要 Python 3（含 pypdf）、Pandoc、TeX Live 2026 的 LuaLaTeX／luatexja、EPUBCheck（`brew install epubcheck`）與 macOS 繁體中文字體。執行：

```bash
make all
```

唯一輸出為倉庫根目錄的 `output/cor2-consolidated.pdf` 與 `output/cor2-consolidated.epub`。書名與版次由 `publication.yaml` 統一管理；七個卷首／分卷／卷末由 `volumes.json` 管理。

PDF 與 EPUB 使用同一份語義化正文及完整附錄。附錄 A 依24課明寫卷名的引用生成課次連結；附錄 B–E 共用 `appendices/`；附錄 C 另自動生成逐課注疏來源網址表。

`make all` 會執行13項回歸測試、EPUBCheck、逐片段 EPUB 內容比對、PDF 附錄完整性、PDF 語義結構、內部連結、缺字／溢出與目錄長度檢查。所有檢查通過後才更新正式文件；失敗時保留上次成功的版本。`output/cor2-consolidated-qa.json` 記錄檢查結果與文件 SHA-256。語義標記不等於已完成 PDF/UA 認證或螢幕閱讀器人工測試。

`make release-check` 另驗證 [release-approvals.json](release-approvals.json) 的32項權利記錄、9項編輯簽核、負責人、日期、證據檔案及當前 PDF／EPUB 雜湊。完成權利核查與人工簽核前應保持失敗。詳見 [RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md) 與 [EDITORIAL-SIGNOFF.md](EDITORIAL-SIGNOFF.md)。
