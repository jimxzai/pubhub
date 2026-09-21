---
title: 約翰福音研讀 · 出版品質評分
subtitle: "Gospel of John Deep Study — Edition 4.0"
date: 2026-09-21
scope: books/bible/gospel-of-john
build: output/gospel-of-john-consolidated.pdf (327 pages)
---

# 約翰福音研讀 · 出版品質評分

**評分立場**：專業出版社總編輯式評估；分數反映目前 editorial proof，不等同於權利清關或正式出版批准。

## 總分：**9.6 / 10**

與上一輪 9.6 分持平，但封面與整體產品包裝由「可接受」提升至系列出版水準。分數沒有因技術建置乾淨而虛增，因為版權、獨立神學審閱、無障礙 PDF 與紙樣仍未完成。

| 項目 | 分數 | 專業出版判斷 |
|---|---:|---|
| 聖經引文準確度 | 9.6 | CUV 1919 / NASB 1995 身份與選摘模型明確；仍需逐節人工終校。 |
| 體例一致性 | 9.5 | 章節、附錄、卷首卷末與版本標示一致。 |
| 排版與建置 | 10.0 | 327 頁；0 missing glyph；0 overfull；字型與連結檢查通過。 |
| 結構與邏輯連貫 | 9.5 | 啟示次序、四卷結構、章末回到基督的主線完整。 |
| 屬靈洞見 | 9.5 | 約翰福音的道、生命、七個「我是」與見證線索有清楚編輯主軸。 |
| 注疏可查證性 | 9.6 | 已核對的 MacArthur / Morgan 引文有定位；少數歷史與書目資料仍待終核。 |
| 中英雙語完整度 | 9.6 | 指定為 CUV 1919 + NASB 1995 選摘研讀指南，沒有冒充完整平行雙語經文。 |
| 引文格式規範 | 9.5 | 引文框、來源說明與編者觀察區分清楚；仍需權利與來源終審。 |
| 讀者可用性 | 9.5 | 自動經文索引、書籤、372 個連結與地圖文字替代資訊均保留。 |
| 封面與產品包裝 | 9.7 | 前後封面已達 Genesis 系列標準：午夜藍、金線、象徵徽記、雙語層級與選摘聲明一致。 |

## 本輪清理與提升

- 更新封面與 back-cover 排版，修正英文引號、斷字與角飾定位。
- 保留 assigned identity：**生命之道 / The Word of Life**、**約翰福音研讀 / Gospel of John Deep Study**、**Edition 4.0**。
- 清理日期與技術證據標記，統一為 2026-09-21；沒有引入其他版本名稱。
- 重新建立並目視檢查 PDF 第 1 頁與第 327 頁；兩頁均為 7 × 10 英寸，無裁切、重疊或不可讀文字。

## 尚未計入「完成」的出版缺口

- CUV / NASB 權利與正式版權聲明仍需權利人確認。
- MacArthur、CCIC 未出版教學材料、詩歌與其他來源仍需許可或替代方案。
- 需要獨立神學／編輯終審、紙樣校對，以及 EPUB / tagged-PDF 螢幕閱讀器測試。

## 驗證證據

- `bash build_release.sh`：validated 30 declared files；errors=0；PDF 327 pages。
- `verify_pdf.py`：bookmarks present；372 links；final TeX pass clean。
- `python3 -m unittest test_publication.py`：6 tests passed。
- 本文件是評分記錄，不是出版許可；正式出版仍須 `editorial-signoffs.json` 的人工作業批准。
