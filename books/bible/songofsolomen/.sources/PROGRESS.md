# 雅歌研讀 — 進度（2026-10-26，每完成一步更新）
目錄：books/bible/songofsolomen/ ；規格 .sources/BOOK-SPEC.md（§9 有工具與守則）
工具：paste_scripture.py / fix_hebrew.py / check_chapter.py / show_unit.py / grab.py / check_dupes.py
並行寫作代理無法啟動（forked worker 不可再 fork）→ 全部由主線逐章親寫。

## 狀態
- [x] 來源：scripture、hebrew、speakers、commentary(biblehub 11家)、longform(Henry/Taylor/Bernard 1-5/Spurgeon 11/Morgan大綱)、xref(56章) 
- [x] BOOK-SPEC.md、PLAN.md
- [x] 第01章（範例章，check_chapter 全綠）
- [ ] 02 03 04 05 06 07 08 09 10 11 12 13 14 15
- [ ] 卷首：000-preface 00-overview 00a-song-position 00b-love-spine 00c-revelation-order
- [ ] 全書領受總綱 elder-wong-systematic-study.md；99-the-open-ending.md；999-afterword.md
- [ ] 附錄：scripts/gen-songofsolomen-indices.py / ledger → 98, 99-appendix-references
- [ ] templates/pdf/songofsolomen.latex（改自 ezra.latex）；scripts/build-songofsolomen-consolidated.sh
- [ ] lint-templates / lint-chapter-markup / lint-scripture-text / check-book-spine / driver.sh songofsolomen / 看頁
- [ ] 獨立校對輪（不信任既有核對，重新取證）；docs/scores/songofsolomen-2026-10-26.md；baselines.tsv
## 待告知使用者
- gospel-of-john 附錄 john-thursday-wong/book/appendix-03-commentary-excerpts.md 把約15章的話歸給伯爾拿《雅歌講道集》，疑誤（伯爾拿雅歌講道只到雅 3:1）；本任務未動。
