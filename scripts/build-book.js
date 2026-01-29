#!/usr/bin/env node

/**
 * 書稿合併腳本
 *
 * 用法:
 *   node scripts/build-book.js hebrews     # 合併希伯來書
 *   node scripts/build-book.js sunzi       # 合併孫子兵法
 *   node scripts/build-book.js john        # 合併約翰五部曲
 *   node scripts/build-book.js all         # 合併所有
 */

const fs = require('fs');
const path = require('path');

// 書籍配置
const BOOKS = {
  hebrews: {
    name: '希伯來書研讀',
    subtitle: '漸進啟示的高峰',
    sourceDir: 'docs/study-notes-hebrews',
    outputFile: 'books/hebrews-study-guide.md',
    order: [
      '00-overview.md',
      '01-introduction.md',
      '02-superior-to-angels.md',
      '03-superior-to-moses.md',
      '04-great-high-priest.md',
      '05-better-covenant.md',
      '06-draw-near.md',
      '07-faith-hall.md',
      '08-endurance.md',
      '09-practical.md'
    ]
  },
  sunzi: {
    name: '孫子兵法・三書對照',
    subtitle: 'AI時代的古典智慧',
    sourceDir: 'docs/study-notes-sunzi',
    outputFile: 'books/sunzi-three-books.md',
    order: [
      '01-shi-ji-beginning.md',
      '02-zuo-zhan-warfare.md',
      '03-mou-gong-strategy.md',
      '04-xing-formation.md',
      '05-shi-momentum.md',
      '06-xu-shi-weakness.md',
      '07-jun-zheng-maneuver.md',
      '08-jiu-bian-adaptation.md',
      '09-xing-jun-march.md',
      '10-di-xing-terrain.md',
      '11-jiu-di-situations.md',
      '12-huo-gong-fire.md',
      '13-yong-jian-spies.md'
    ]
  },
  john: {
    name: '約翰五部曲',
    subtitle: '從太初有道到愛永遠長存',
    sourceDir: 'docs',
    outputFile: 'books/john-pentalogy.md',
    customOrder: true
  }
};

// 書籍封面模板
const COVER_TEMPLATE = `---
title: "{{TITLE}}"
subtitle: "{{SUBTITLE}}"
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

# {{TITLE}}

> **{{SUBTITLE}}**

---

**生成日期**: {{DATE}}

**項目**: 七年三書精讀出版系統

---

\\newpage

`;

// 讀取並合併文件
function mergeFiles(bookKey) {
  const book = BOOKS[bookKey];
  if (!book) {
    console.error(`未知的書籍: ${bookKey}`);
    console.log('可用選項: ' + Object.keys(BOOKS).join(', '));
    process.exit(1);
  }

  const baseDir = path.join(process.cwd(), book.sourceDir);

  // 檢查目錄是否存在
  if (!fs.existsSync(baseDir)) {
    console.error(`目錄不存在: ${baseDir}`);
    process.exit(1);
  }

  // 獲取文件列表
  let files;
  if (book.customOrder) {
    // 約翰五部曲需要特殊處理
    files = getJohnFiles();
  } else {
    // 按照預定順序獲取存在的文件
    files = book.order
      .map(f => path.join(baseDir, f))
      .filter(f => fs.existsSync(f));
  }

  if (files.length === 0) {
    console.error('找不到任何文件');
    process.exit(1);
  }

  console.log(`📚 合併 ${book.name}...`);
  console.log(`   找到 ${files.length} 個文件`);

  // 生成封面
  const date = new Date().toISOString().split('T')[0];
  let output = COVER_TEMPLATE
    .replace(/\{\{TITLE\}\}/g, book.name)
    .replace(/\{\{SUBTITLE\}\}/g, book.subtitle)
    .replace(/\{\{DATE\}\}/g, date);

  // 合併所有文件
  files.forEach((file, index) => {
    const content = fs.readFileSync(file, 'utf-8');
    const fileName = path.basename(file);

    console.log(`   ✓ ${fileName}`);

    // 添加分頁符（除了第一個文件）
    if (index > 0) {
      output += '\n\n\\newpage\n\n';
    }

    // 移除 YAML front matter（如果有）
    const cleanContent = content.replace(/^---[\s\S]*?---\n*/m, '');

    output += cleanContent + '\n\n';
  });

  // 確保輸出目錄存在
  const outputPath = path.join(process.cwd(), book.outputFile);
  const outputDir = path.dirname(outputPath);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // 寫入合併後的文件
  fs.writeFileSync(outputPath, output);
  console.log(`\n✅ 已生成: ${book.outputFile}`);
  console.log(`   字數估計: ~${Math.round(output.length / 2)} 字`);

  return outputPath;
}

// 獲取約翰五部曲的文件
function getJohnFiles() {
  const baseDir = process.cwd();
  const files = [];

  // 約翰福音
  const johnDir = path.join(baseDir, 'docs/study-notes');
  if (fs.existsSync(johnDir)) {
    fs.readdirSync(johnDir)
      .filter(f => f.endsWith('.md'))
      .sort()
      .forEach(f => files.push(path.join(johnDir, f)));
  }

  // 約翰一書
  const john1Dir = path.join(baseDir, 'docs/study-notes-1john');
  if (fs.existsSync(john1Dir)) {
    fs.readdirSync(john1Dir)
      .filter(f => f.endsWith('.md'))
      .sort()
      .forEach(f => files.push(path.join(john1Dir, f)));
  }

  // 約翰二書
  const john2Dir = path.join(baseDir, 'docs/study-notes-2john');
  if (fs.existsSync(john2Dir)) {
    fs.readdirSync(john2Dir)
      .filter(f => f.endsWith('.md'))
      .sort()
      .forEach(f => files.push(path.join(john2Dir, f)));
  }

  // 約翰三書
  const john3Dir = path.join(baseDir, 'docs/study-notes-3john');
  if (fs.existsSync(john3Dir)) {
    fs.readdirSync(john3Dir)
      .filter(f => f.endsWith('.md'))
      .sort()
      .forEach(f => files.push(path.join(john3Dir, f)));
  }

  // 啟示錄
  const revDir = path.join(baseDir, 'docs/study-notes-revelation');
  if (fs.existsSync(revDir)) {
    fs.readdirSync(revDir)
      .filter(f => f.endsWith('.md'))
      .sort()
      .forEach(f => files.push(path.join(revDir, f)));
  }

  return files;
}

// 主程序
const args = process.argv.slice(2);
const bookKey = args[0] || 'hebrews';

if (bookKey === 'all') {
  Object.keys(BOOKS).forEach(key => {
    try {
      mergeFiles(key);
    } catch (e) {
      console.error(`合併 ${key} 時出錯: ${e.message}`);
    }
    console.log('');
  });
} else {
  mergeFiles(bookKey);
}

console.log(`
📖 下一步：生成 PDF

方法 1 - 使用 md-to-pdf (推薦):
  npm install -g md-to-pdf
  md-to-pdf books/hebrews-study-guide.md

方法 2 - 使用 Pandoc + LaTeX:
  brew install pandoc
  brew install --cask mactex
  pandoc books/hebrews-study-guide.md -o books/hebrews-study-guide.pdf

方法 3 - 使用 VS Code 擴展:
  安裝 "Markdown PDF" 擴展
  打開合併後的 .md 文件
  右鍵 > Markdown PDF: Export (pdf)
`);
