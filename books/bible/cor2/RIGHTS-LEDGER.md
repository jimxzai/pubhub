# 權利與來源登錄表

本表是出版作業用的追蹤表，不是法律意見。狀態為 `PENDING` 的項目，在取得書面許可、確認公有領域或完成合規引用審核前，不得視為可正式發行。

## 核心文本與來源

| 資產 | 使用方式 | 狀態 | 發行前證據 |
|---|---|---|---|
| 和合本（1919） | 24課完整或大段經文 | PENDING | 目標地區、版本來源與使用權確認 |
| NASB 1995 | 24課英文對照與概覽引文 | PENDING | Lockman許可或改用已授權版本 |
| ai-eden Bible | 經文核對連結 | PENDING | 確認網站內容來源、穩定網址與可引用範圍 |
| Google Drive課程資料 | 原始課堂材料 | PENDING | 教會或權利持有人書面授權 |
| John Chrysostom／NPNF | 歷代注疏引文與中文撮述 | PENDING | 原版、翻譯者與引文位置記錄 |
| John Calvin／CCEL | 歷代注疏引文與中文撮述 | PENDING | 版本、頁碼或段落位置記錄 |
| G. Campbell Morgan | 引文、撮述與1946年作品引用 | PENDING | 版權期限、版本與掃描來源確認 |
| John MacArthur／GTY | 講道引文與教義撮述 | PENDING | 引用比例、網站條款與書面許可審核 |

## 24課配詩

| 課次 | 詩歌 | 狀態 | 需要記錄 |
|---:|---|---|---|
| 01 | Be Still, My Soul | PENDING | 原作、英譯、中文翻譯與版本 |
| 02 | O for a Heart to Praise My God | PENDING | 作者、歌詞版本與翻譯 |
| 03 | There's a Wideness in God's Mercy | PENDING | 作者、歌詞版本與翻譯 |
| 04 | Jesus, the Very Thought of Thee | PENDING | 作者、歌詞版本與翻譯 |
| 05 | O Word of God Incarnate | PENDING | 作者、歌詞版本與翻譯 |
| 06 | Immortal, Invisible, God Only Wise | PENDING | 作者、歌詞版本與翻譯 |
| 07 | Christ, Whose Glory Fills the Skies | PENDING | 作者、歌詞版本與翻譯 |
| 08 | Have Thine Own Way, Lord | PENDING | 作者、歌詞版本與翻譯 |
| 09 | Abide with Me | PENDING | 作者、歌詞版本與翻譯 |
| 10 | Jerusalem the Golden | PENDING | 作者、歌詞版本與翻譯 |
| 11 | And Can It Be That I Should Gain | PENDING | 作者、歌詞版本與翻譯 |
| 12 | Take My Life, and Let It Be | PENDING | 作者、歌詞版本與翻譯 |
| 13 | O Love That Wilt Not Let Me Go | PENDING | 作者、歌詞版本與翻譯 |
| 14 | Just as I Am, Without One Plea | PENDING | 作者、歌詞版本與翻譯 |
| 15 | When I Survey the Wondrous Cross | PENDING | 作者、歌詞版本與翻譯 |
| 16 | A Charge to Keep I Have | PENDING | 作者、歌詞版本與翻譯 |
| 17 | We Give Thee but Thine Own | PENDING | 作者、歌詞版本與翻譯 |
| 18 | Now Thank We All Our God | PENDING | 作者、歌詞版本與翻譯 |
| 19 | A Mighty Fortress Is Our God | PENDING | 作者、歌詞版本與翻譯 |
| 20 | Not What My Hands Have Done | PENDING | 作者、歌詞版本與翻譯 |
| 21 | The Church's One Foundation | PENDING | 作者、歌詞版本與翻譯 |
| 22 | In the Cross of Christ I Glory | PENDING | 作者、歌詞版本與翻譯 |
| 23 | How Firm a Foundation | PENDING | 作者、歌詞版本與翻譯 |
| 24 | Blest Be the Tie That Binds | PENDING | 作者、歌詞版本與翻譯 |

## Release rule

機器可驗證的記錄位於 [release-approvals.json](release-approvals.json)：`source-1` 至 `source-8` 按上表八項核心來源順序對應，`hymn-01` 至 `hymn-24` 對應課次。正式發行檢查要求完整的32筆記錄，每筆須有審核人、日期、證據文件及 SHA-256；缺表、刪行、重複、未知狀態或缺少證據均不通過。`REMOVED` 項目仍須保留移除證據。

正式版只能把 `PENDING` 改成 `CLEARED`、`PUBLIC-DOMAIN` 或 `REMOVED`，並附上審核日期、負責人與證據位置。沒有證據的「公有領域」標記不得保留。
