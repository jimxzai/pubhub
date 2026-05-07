#!/usr/bin/env node

/**
 * ═══════════════════════════════════════════════════════════════════════════════
 *  啟示錄導讀 - 書稿構建腳本
 *  Build script for Revelation Study Notes
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 * 用法:
 *   node scripts/build-revelation-book.js
 *
 * 輸出:
 *   docs/study-notes-revelation/output/revelation-complete.md
 */

const fs = require('fs');
const path = require('path');

// 路徑設置
const PROJECT_ROOT = path.join(__dirname, '..');
const REVELATION_DIR = path.join(PROJECT_ROOT, 'docs/study-notes-revelation');
const OUTPUT_DIR = path.join(REVELATION_DIR, 'output');

// 文件順序
const FILE_ORDER = [
  '00-overview.md',
  '01-introduction.md',
  '02-seven-churches.md',
  '03-heavenly-worship.md',
  '04-seals-trumpets.md',
  '05-cosmic-conflict.md',
  '06-bowls-babylon.md',
  '07-new-creation.md'
];

// 書名與元數據
const BOOK_TITLE = '啟示錄導讀：愛永遠長存';
const BOOK_SUBTITLE = 'Revelation Study Notes: Love Endures Forever';
const BOOK_AUTHOR = 'Thursday Wong';
const BOOK_DATE = new Date().toISOString().split('T')[0];

// 顏色輸出
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  blue: '\x1b[34m',
  yellow: '\x1b[33m',
  red: '\x1b[31m'
};

function log(color, message) {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

// 確保輸出目錄存在
function ensureOutputDir() {
  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    log('green', `✓ 創建輸出目錄: ${OUTPUT_DIR}`);
  }
}

// 讀取並處理文件
function readAndProcessFile(filename) {
  const filepath = path.join(REVELATION_DIR, filename);

  if (!fs.existsSync(filepath)) {
    log('yellow', `⚠ 文件不存在: ${filename}`);
    return '';
  }

  let content = fs.readFileSync(filepath, 'utf8');

  // 移除文件開頭的 H1 標題（將在合併時統一處理）
  // 保留其他內容
  content = content.replace(/^# [^\n]+\n/, '');

  return content;
}

// 生成封面頁
function generateFrontMatter() {
  return `---
title: "${BOOK_TITLE}"
subtitle: "${BOOK_SUBTITLE}"
author: "${BOOK_AUTHOR}"
date: "${BOOK_DATE}"
lang: zh-TW
toc: true
toc-depth: 3
numbersections: true
documentclass: book
classoption:
  - openany
  - 11pt
geometry:
  - margin=2.5cm
  - a4paper
mainfont: "PingFang SC"
CJKmainfont: "PingFang SC"
monofont: "Menlo"
linkcolor: blue
urlcolor: blue
toccolor: black
header-includes:
  - \\usepackage{fancyhdr}
  - \\pagestyle{fancy}
  - \\fancyhead[L]{啟示錄導讀}
  - \\fancyhead[R]{愛永遠長存}
---

\\newpage

# 啟示錄導讀

## 愛永遠長存

**Revelation Study Notes: Love Endures Forever**

---

> **「看哪，神的帳幕在人間。他要與人同住，他們要作他的子民；神要親自與他們同在，作他們的神。」**
> — 啟示錄 21:3

> **「如今常存的有信、有望、有愛這三樣，其中最大的是愛。」**
> — 哥林多前書 13:13

---

**作者**: ${BOOK_AUTHOR}

**完成日期**: ${BOOK_DATE}

**版本**: 1.0

---

**約翰著作五部曲**

| 書卷 | 主題 | 時間指向 |
|------|------|----------|
| 約翰福音 | 道成肉身 | 過去：信的根基 |
| 約翰一書 | 神就是愛 | 現在：愛的生活 |
| 約翰二書 | 保護真理 | 現在：愛的邊界 |
| 約翰三書 | 傳播真理 | 現在：愛的行動 |
| **啟示錄** | **道榮耀再來** | **將來：望的實現** |

---

\\newpage

`;
}

// 生成章節標題
function generateChapterTitle(filename) {
  const titles = {
    '00-overview.md': '# 概覽：啟示錄研讀導引',
    '01-introduction.md': '# 第一章：正典脈絡與神學框架',
    '02-seven-churches.md': '# 第二章：七教會書信 (1-3章)',
    '03-heavenly-worship.md': '# 第三章：天上的敬拜 (4-5章)',
    '04-seals-trumpets.md': '# 第四章：七印與七號 (6-11章)',
    '05-cosmic-conflict.md': '# 第五章：宇宙爭戰 (12-14章)',
    '06-bowls-babylon.md': '# 第六章：七碗與巴比倫 (15-19章)',
    '07-new-creation.md': '# 第七章：新天新地 (20-22章)'
  };

  return titles[filename] || `# ${filename}`;
}

// 構建完整書稿
function buildCompleteBook() {
  log('blue', '═══════════════════════════════════════════════════════════');
  log('blue', '   構建啟示錄導讀完整書稿');
  log('blue', '═══════════════════════════════════════════════════════════');
  console.log('');

  ensureOutputDir();

  let content = generateFrontMatter();
  let totalWords = 0;

  for (const filename of FILE_ORDER) {
    log('blue', `處理: ${filename}`);

    const chapterTitle = generateChapterTitle(filename);
    const fileContent = readAndProcessFile(filename);

    if (fileContent) {
      content += `${chapterTitle}\n\n`;
      content += fileContent;
      content += '\n\n\\newpage\n\n';

      // 計算字數
      const wordCount = fileContent.length;
      totalWords += wordCount;
      log('green', `  ✓ ${wordCount.toLocaleString()} 字`);
    }
  }

  // 添加結語
  content += `
# 結語：愛永遠長存

> **「主耶穌啊，我願你來！」** — 啟示錄 22:20

從約翰福音到啟示錄，約翰的見證始終如一：

- **約翰福音**：神愛世人，甚至將祂的獨生子賜給他們
- **約翰一書**：神就是愛，住在愛裡面的，就是住在神裡面
- **約翰二三書**：在真理和愛中行走
- **啟示錄**：神的帳幕在人間，祂要與人同住

**信會成為眼見，望會成為實現，唯有愛，永遠長存。**

---

**愛是主題。愛是精神。愛是靈魂。愛永遠長存。**

---

*Soli Deo Gloria — 唯獨榮耀歸於神*

`;

  // 寫入文件
  const outputPath = path.join(OUTPUT_DIR, 'revelation-complete.md');
  fs.writeFileSync(outputPath, content, 'utf8');

  console.log('');
  log('green', '═══════════════════════════════════════════════════════════');
  log('green', '   ✅ 構建完成！');
  log('green', '═══════════════════════════════════════════════════════════');
  console.log('');
  log('green', `輸出文件: ${outputPath}`);
  log('green', `總字數: ~${totalWords.toLocaleString()} 字`);
  log('green', `章節數: ${FILE_ORDER.length}`);
  console.log('');
  log('yellow', '下一步：運行 PDF 生成');
  log('yellow', '  npm run pdf:revelation');
  log('yellow', '  或');
  log('yellow', '  bash scripts/generate-pdf.sh revelation');
  console.log('');
}

// 主函數
function main() {
  buildCompleteBook();
}

main();
