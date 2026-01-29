#!/usr/bin/env node

/**
 * 孫子兵法・三書對照 — 書稿合併腳本
 *
 * 用法:
 *   node scripts/build-sunzi-book.js
 *
 * 輸出:
 *   books/sunzi/output/孫子兵法-三書對照.md
 */

const fs = require('fs');
const path = require('path');

// 配置
const CONFIG = {
  name: '孫子兵法・三書對照',
  subtitle: 'AI時代的古典智慧',
  sourceDir: 'books/sunzi',
  outputDir: 'books/sunzi/output',
  outputFile: '孫子兵法-三書對照.md',

  // 文件順序
  order: [
    '00-introduction.md',      // 導讀
    '01-shi-ji.md',            // 始計篇
    '02-zuo-zhan.md',          // 作戰篇
    '03-mou-gong.md',          // 謀攻篇
    '04-jun-xing.md',          // 軍形篇
    '05-bing-shi.md',          // 兵勢篇
    '06-xu-shi.md',            // 虛實篇
    '07-jun-zheng.md',         // 軍爭篇
    '08-jiu-bian.md',          // 九變篇
    '09-xing-jun.md',          // 行軍篇
    '10-di-xing.md',           // 地形篇
    '11-jiu-di.md',            // 九地篇
    '12-huo-gong.md',          // 火攻篇
    '13-yong-jian.md',         // 用間篇
    '14-conclusion.md'         // 總結
  ]
};

// 書籍封面模板
const COVER_TEMPLATE = `---
title: "${CONFIG.name}"
subtitle: "${CONFIG.subtitle}"
author: "Thursday Wong Study Group"
date: "{{DATE}}"
lang: zh-TW
documentclass: book
fontsize: 12pt
linestretch: 1.5
geometry: margin=2.5cm
toc: true
toc-depth: 3
---

# ${CONFIG.name}

> **${CONFIG.subtitle}**

> **「兵者，國之大事，死生之地，存亡之道，不可不察也。」**
> — 孫子兵法・始計篇

---

**生成日期**: {{DATE}}

**項目**: 七年三書精讀出版系統

**框架**: 三書合讀 — 孫子兵法 × 資治通鑑 × 聖經

---

## 核心異象

> **「神既在古時藉著眾先知多次多方地曉諭列祖，就在這末世藉著他兒子曉諭我們。」**
> — 希伯來書 1:1-2

三書合讀的目的：
- **孫子兵法**：普遍恩典下的軍事智慧
- **資治通鑑**：歷史的興亡教訓
- **聖經**：特殊啟示的永恆真理

透過四維透視（人性、出路、神的計劃、爭戰），
看見人的智慧與神的智慧的對照，
最終指向：**愛永遠長存**。

---

\\newpage

`;

// 主函數
function build() {
  const baseDir = path.join(process.cwd(), CONFIG.sourceDir);
  const outputDir = path.join(process.cwd(), CONFIG.outputDir);
  const outputPath = path.join(outputDir, CONFIG.outputFile);

  // 確保輸出目錄存在
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // 獲取存在的文件
  const files = CONFIG.order
    .map(f => path.join(baseDir, f))
    .filter(f => fs.existsSync(f));

  if (files.length === 0) {
    console.error('❌ 找不到任何文件');
    console.log(`   目錄: ${baseDir}`);
    process.exit(1);
  }

  console.log(`📚 合併 ${CONFIG.name}...`);
  console.log(`   找到 ${files.length}/${CONFIG.order.length} 個文件`);
  console.log('');

  // 生成封面
  const date = new Date().toISOString().split('T')[0];
  let output = COVER_TEMPLATE.replace(/\{\{DATE\}\}/g, date);

  // 統計
  let totalChars = 0;

  // 合併所有文件
  files.forEach((file, index) => {
    const content = fs.readFileSync(file, 'utf-8');
    const fileName = path.basename(file);

    console.log(`   ✓ ${fileName}`);

    // 添加分頁符
    if (index > 0) {
      output += '\n\n\\newpage\n\n';
    }

    // 移除 YAML front matter
    const cleanContent = content.replace(/^---[\s\S]*?---\n*/m, '');

    // 移除標籤行
    const noTags = cleanContent.replace(/^`#[^`]+`\s*/gm, '');

    output += noTags + '\n\n';
    totalChars += cleanContent.length;
  });

  // 添加結語
  output += `
\\newpage

# 後記

> **「如今常存的有信、有望、有愛這三樣，其中最大的是愛。」**
> — 哥林多前書 13:13

孫子兵法教導我們「不可不察」的智慧，
資治通鑑讓我們「以史為鑑」，
唯有聖經指向永恆——

**愛永遠長存。**

---

*Thursday Wong Study Group*
*${date}*
`;

  // 寫入文件
  fs.writeFileSync(outputPath, output);

  console.log('');
  console.log(`✅ 已生成: ${CONFIG.outputDir}/${CONFIG.outputFile}`);
  console.log(`   字數估計: ~${Math.round(totalChars / 2)} 字`);
  console.log('');

  // 顯示未找到的文件
  const missingFiles = CONFIG.order.filter(f =>
    !fs.existsSync(path.join(baseDir, f))
  );
  if (missingFiles.length > 0) {
    console.log('⚠️  以下文件尚未創建:');
    missingFiles.forEach(f => console.log(`   - ${f}`));
    console.log('');
  }

  console.log(`
📖 下一步：生成 PDF

方法 1 - 使用 Pandoc (推薦，支持中文):
  ./scripts/generate-pdf.sh sunzi

方法 2 - 使用 md-to-pdf:
  npm install -g md-to-pdf
  md-to-pdf ${CONFIG.outputDir}/${CONFIG.outputFile}

方法 3 - 手動 Pandoc:
  pandoc "${outputPath}" \\
    -o "${outputDir}/孫子兵法-三書對照.pdf" \\
    --pdf-engine=xelatex \\
    -V mainfont="PingFang SC" \\
    -V CJKmainfont="PingFang SC" \\
    --toc --toc-depth=3
`);

  return outputPath;
}

// 執行
build();
