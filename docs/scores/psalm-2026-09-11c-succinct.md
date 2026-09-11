---
title: 詩篇研讀 · 出版品質評分（第三輪：以啟示的次序為準的精簡）
subtitle: "Psalms Deep Study — Editorial Quality Score, Round 3 (Succinct Pass Guided by the Revelation-Order Design)"
date: 2026-09-11
scope: books/bible/psalm
build: output/psalm-consolidated.pdf (108 pages, 原110) · output/psalm-liturgical-consolidated.pdf (335 頁, 原339)
---

# 詩篇研讀 · 出版品質評分（第三輪：以啟示的次序為準的精簡）

**這一輪的來由**：作者要求「optimize it to be clearer and succinct, based on the spiritual revelation design」，範圍選定全書。本輪不是逐段砍字數，而是先量後砍——找出真正「同一個點講了兩次」的地方，以〈啟示的次序〉這一章立起的骨幹為判準：凡服務這條骨幹的內容留下並理順，凡與它重複的內容合併或刪除。

---

## 找到的問題與判斷

**先量後砍的結果**：對06-10共147篇「逐篇領受」做了長度分佈檢查（每篇993-1755字元，中位數約1100），**沒有發現異常臃腫的篇目**——這一部分本已相當精煉，體例（精義一句話→背景→黃長老帶讀→連結→呼求→住與行→你看見耶穌了嗎）本身就是緊湊的骨架，各節重複引用同一錨點經文是刻意的設計（從不同角度回看同一句話），不是贅述，本輪未予處理。

真正的冗餘出在**第一、二輪自己加進去的內容**——這是〈spine-and-score.md〉早已警告過的模式（辛工加的收尾段容易和既有收尾段重複）：

1. **00-overview.md 有兩張幾乎相同的五卷對照表**（一次在「一本書、五卷、多層結構」，一次在「如何使用本研讀指南」）——後者刪去範圍／對應摩西五經欄位，改為「依上表」帶過。
2. **00-overview.md 完全沒有指向新增的〈啟示的次序〉章**——鑰匙表第4把與「聖靈的編排次序」段落都未提及；已補上雙重指向，並把該段落原本重複展開五卷弧線的一整段，縮成一句話加指標。
3. **01-book-one-1-41.md 的「每日應用」第一點，與本人上一輪新加的「你看見耶穌了嗎」收尾大段重複**（同樣列舉有福的人、受膏的王、受苦的牧人、被出賣的至交）——刪去第一點，保留兩則真正的應用提問。
4. **11-voices-morgan-macarthur.md 的「你看見耶穌了嗎」與前一段「三個聲音的合唱」重複**同一句「每一卷都往頌讚裏走，每一篇都往基督身上走」——收尾段落刪去重複句，只留下新內容（詩23/51/107的具體對應）。
5. **13-prayer-testimony.md 的「你看見耶穌了嗎」與「收束：如何禱告？」重複**十架兩句禱詞、以及一字不差的收尾句「剩下的不是詞，是祂」——兩段合併為一段，砍去約80%。
6. **14-christ-through-psalms.md 的「收束」與「你看見耶穌了嗎」幾乎是同一段話寫了兩次**（同樣引詩40「看哪，我來了」、同樣的「白讀了」收筆）——直接合併成一段。

12-backgrounds.md、15-hebrew-poetics.md、16-liturgical-use.md 的既有收尾段與新加的「你看見耶穌了嗎」逐一核對後，**內容確實不同**（各自舉出不同的具體例證），予以保留，未強行合併。

---

## 驗證

| 項目 | 結果 |
|---|---|
| `lint-chapter-markup.py books/bible/psalm` | 0 errors |
| `lint-scripture-text.py books/bible/psalm` | clean |
| `check-book-spine.py books/bible/psalm` | 四項全 ok，座標 16/16，回到基督 16/16——精簡未動到骨幹標記（`spine-and-score.md` 特別警告過這是精簡輪最容易誤傷的一項，本輪逐一核對確認未受影響） |
| `driver.sh psalm` | 108 頁（110→108），0 missing glyph，0 overfull |
| `driver.sh psalm-liturgical` | 335 頁（339→335），0 missing glyph，0 overfull |
| 目視：page 17（compact，七焦點表＋如何使用本研讀指南） | 正確引用上表、未重複列印，渲染正常 |
| 淨變動 | 5 個檔案，10 insertions / 34 deletions |

---

## 仍未完成（誠實列出）

1. **06-10 共147篇逐篇領受本輪只做了長度分佈檢查，沒有逐篇通讀找措辭層級的可精簡處。** 分佈檢查排除了「結構性臃腫」，但不排除個別段落有可再收緊一兩句的空間——量體不足以支持這一層精簡，需要逐篇讀。
2. **00-overview.md、01-05 的正文本身（非收尾段）本輪未做逐段精簡**——本輪聚焦於「新舊收尾段重複」與「00a的結構性缺口」兩類問題，未對每一段的遣詞造句做進一步壓縮。
3. **12-backgrounds、15-hebrew-poetics、16-liturgical-use 收尾段有主題上的重疊詞**（如15章的「慢下來」重複三次），判斷為修辭手法而非贅述、予以保留，但這是編輯判斷，並非機器可驗證的結論，仍可能有不同意見。

---

相關記憶：[[feedback_succinct_pass_method]]、[[project_eat_bible_spine_score]]
