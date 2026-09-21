# 約翰福音研讀 (Gospel of John Deep Study)

**狀態**：⚠️ 編輯與出版驗證中（最近建置：327 頁；排版閘門已清，權利與編輯核驗待清）
**版本**：4.0 — 十一節房規版／NASB 1995
**最近更新**：2026-09-20

---

## 這卷書是甚麼

逐章研讀約翰福音二十一章，整合三大資源：

- **老弟兄（CCIC 週四查經班）** — 第一手查經教導（未出版之班內筆記）
- **John MacArthur** — 逐節解經講道（gty.org，講章編號 43-2 至 43-116）
- **G. Campbell Morgan** — *The Gospel According to John*（1909）

**核心框架**：榮耀 = 恩典 + 真理。七個神蹟（works）彰顯恩典，七個「我是」（words）彰顯真理——兆頭是圖畫，「我是」是圖畫下面的說明文字。

**內容範圍聲明**：本版是「研讀指南＋經文選摘」，不是完整的中英雙語《約翰福音》排印本。各章的 CUV／NASB 經文區塊按研讀需要選取；除非明確標示完整段落，兩種語言不保證逐節平行。若要作完整雙語聖經研讀本，必須先完成逐節配對與版本權利確認。

---

## 建置

數位閱讀校樣：先完成 PDF 建置，再執行 `python3 build_digital.py`。
產物位於 `digital/`，包含 EPUB 3 及自足的 HTML；保留正文、九個附錄與附文字說明的地圖。
仍需閱讀器及螢幕閱讀器實測，不能據此宣稱通過無障礙認證。

`bash build_release.sh` 驗證並產生編輯校樣；`--publish` 另要求所有出版簽核都有證據。
每次建置均重新產生經文索引及 `output/gospel-of-john-passage-inventory.md` 節號清單。
書名、版本及兩種譯本均有精確檢查；沒有 YAML 的全書領受總綱除外。

```bash
# 從倉庫根目錄
bash books/bible/gospel-of-john/build_release.sh  # 驗證 manifest + 建置 + 警告閘門
.claude/skills/eat-bible/driver.sh gospel        # 建置 + 驗證（log／字型／baseline）
```

改稿之前先跑三支 lint（都只要一秒，且能抓到建置時完全靜默的缺陷）：

```bash
scripts/lint-templates.sh gospel-of-john
python3 scripts/lint-chapter-markup.py books/bible/gospel-of-john
python3 scripts/lint-scripture-text.py books/bible/gospel-of-john
```

出版源碼驗證（在本目錄執行）：

```bash
python3 validate_publication.py
```

驗證器會檢查出版 manifest、必要檔案、十一節體例、CUV／NASB 選摘標記
差異，以及 README 的版本漂移。差異在目前「選摘版」定位下列為 REVIEW，
不是假裝成完整雙語排印本的通行證。

模板：`templates/pdf/gospel-of-john.latex`（含九個附錄與封面）。

---

## 檔案結構

書稿由 `scripts/build-gospel-consolidated.sh` 依下列次序串接：

| 次序 | 檔案 | 內容 |
|------|------|------|
| 前言 | `000-preface.md` | 成書緣起 |
| 卷首 | `00-overview.md` | 概覽——地圖、七兆頭、七「我是」、章節目錄、如何使用本書 |
| 卷首 | `00a-revelation-order.md` | 啟示的次序與組織——座標 |
| 卷首 | `00b-i-am-deity.md` | 「我是」——全書的骨幹 |
| 卷首 | `elder-wong-systematic-study.md` | 全書領受總綱（按結構逐部深讀） |
| 卷一 | `01-prologue.md` | 序言：道成肉身（1:1-18） |
| 卷二 | `01b`–`12`（13 章，含 `01b`、`04b` 分章） | 兆頭之書（1:19-12:50） |
| 卷三 | `13`–`17` | 樓上私語（13-17） |
| 卷四 | `18`–`20` | 受難復活（18-20） |
| 卷五 | `21-epilogue.md` | 跋：爐火邊的恢復與差遣（21） |
| 卷末 | `99-to-revelation.md` | 從「太初有道」到「我必快來」 |
| 跋 | `999-afterword.md` | 事工、六十六卷的願望、結尾頁 |

未納入建置的參考檔：`RED-LETTER-GUIDE.md`、`JESUS-TO-DISCIPLES.md`。

---

## 每章的十一節體例

23 章一律照同一條路走（機器驗證：標題與順序完全一致）：

```
# 章題 (English)
約翰福音 N:x-y
**經文核對**：ai-eden.com 連結（CUV／NASB 選摘核對）

## 基督焦點      鑰詞／「我是」座標框 + 一段導引
## 配詩          一首公有領域聖詩 + 作者年份
## 經文          ### 中文 — 和合本 (CUV)  /  ### English — NASB
## 背景
## 原文研讀      希臘文／音譯／意義／註解
## 領受要點      三至五個要點，散文體
## 歷代注疏      體例說明框 → 教父時期／改革宗時期／摩根／麥克阿瑟
## 詩篇與聖詩
## 老弟兄查經    精義一句話 → 全經連線／提問式對話／活在今天／今天的祭壇 → 你看見耶穌了嗎
## 生命應用      ### 默想問題（≤3）／### 禱告回應
## 與其他經文的關聯   主題｜本章經文｜相關經文
```

---

## 體例規則（改稿必讀）

- **經文**：中文以《聖經》和合本（CUV, 1919）為準，英文用 **NASB 1995**。本版為選摘；每一段已納入的引文仍不得改動——包括 `^n^` 節號、`\jesus{}` 紅字段、粗體。
- **`\jesus{}` 內只能用 `\textbf{}`／`\textit{}`**：markdown 的 `**`／`*` 在 raw LaTeX 巨集裏不會轉換，會印出星號。
- **引號內的經文必須逐字等同和合本**。要強調或改寫，就把字放到引號外。
- **不杜撰**：經文、注疏、史料一律可查證；轉引他人之說須標明未覆核原著。
- **稱呼**：一律「老弟兄」，不用「黃長老」。
- **用字**：繁體；`裏` 不用 `裡`，`甚麼` 不用 `什麼`。
- **模板未開 `Ligatures=TeX`**：不要寫 `--`（用 `–`）或 ` `` `／`''`（用 `“`／`”`）。
- **聖詩須為公有領域**，並註明作者與年份。

---

## 版本說明

出版 manifest：`publication-manifest.json`。權利與引用清單：`RIGHTS-AND-CITATION-LEDGER.md`。需要單一串接檔，請跑建置腳本產生 `output/gospel-of-john-consolidated.md`；目前該產物仍須通過權利、引文與排版警告清理，才可稱為正式出版檔。

出版報告與評分：`docs/build-reports/gospel-of-john/FINAL-PUBLICATION-REPORT.md`。
