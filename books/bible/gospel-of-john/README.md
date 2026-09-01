# 約翰福音研讀 (Gospel of John Deep Study)

**狀態**：✅ 出版就緒（321 頁，0 glyph／0 overfull，三支 lint 全清）
**版本**：4.0 — 十一節房規版／NASB 1995
**最近更新**：2026-08-31

---

## 這卷書是甚麼

逐章研讀約翰福音二十一章，整合三大資源：

- **老弟兄（CCIC 週四查經班）** — 第一手查經教導（未出版之班內筆記）
- **John MacArthur** — 逐節解經講道（gty.org，講章編號 43-2 至 43-116）
- **G. Campbell Morgan** — *The Gospel According to John*（1909）

**核心框架**：榮耀 = 恩典 + 真理。七個神蹟（works）彰顯恩典，七個「我是」（words）彰顯真理——兆頭是圖畫，「我是」是圖畫下面的說明文字。

---

## 建置

```bash
# 從倉庫根目錄
bash scripts/build-gospel-consolidated.sh        # → output/gospel-of-john-consolidated.pdf
.claude/skills/eat-bible/driver.sh gospel        # 建置 + 驗證（log／字型／baseline）
```

改稿之前先跑三支 lint（都只要一秒，且能抓到建置時完全靜默的缺陷）：

```bash
scripts/lint-templates.sh gospel-of-john
python3 scripts/lint-chapter-markup.py books/bible/gospel-of-john
python3 scripts/lint-scripture-text.py books/bible/gospel-of-john
```

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
**經文核對**：ai-eden.com 連結（CUV,NASB 對照）

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

- **經文**：中文以《聖經》和合本（CUV, 1919）為準，英文用 **NASB 1995**。`## 經文` 一節的內容不得改動——包括 `^n^` 節號、`\jesus{}` 紅字段、粗體。
- **`\jesus{}` 內只能用 `\textbf{}`／`\textit{}`**：markdown 的 `**`／`*` 在 raw LaTeX 巨集裏不會轉換，會印出星號。
- **引號內的經文必須逐字等同和合本**。要強調或改寫，就把字放到引號外。
- **不杜撰**：經文、注疏、史料一律可查證；轉引他人之說須標明未覆核原著。
- **稱呼**：一律「老弟兄」，不用「黃長老」。
- **用字**：繁體；`裏` 不用 `裡`，`甚麼` 不用 `什麼`。
- **模板未開 `Ligatures=TeX`**：不要寫 `--`（用 `–`）或 ` `` `／`''`（用 `“`／`”`）。
- **聖詩須為公有領域**，並註明作者與年份。

---

## 版本說明

`complete-book.md`（2026-01 的全書串接檔）已於 2026-08-31 移除：它是舊版產物，不在建置流程內，且內容與現行 4.0 版（十一節體例、NASB、老弟兄稱呼）不符，留著只會誤導。需要單一檔案的全書，請跑建置腳本產生 `output/gospel-of-john-consolidated.md`。舊檔仍可從 git 歷史取回。

出版報告與評分：`docs/build-reports/gospel-of-john/FINAL-PUBLICATION-REPORT.md`。
