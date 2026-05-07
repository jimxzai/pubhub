#!/usr/bin/env node

/**
 * PubHub Book Builder
 * Compiles annual notes into a cohesive book manuscript
 *
 * Usage:
 *   node scripts/build-book.js --book sunzi --year 2025
 *   node scripts/build-book.js --book bible --year 2025 --format pdf
 */

import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const CONFIG = {
  booksDir: path.join(__dirname, '..', 'books'),
  dailyNotesDir: path.join(__dirname, '..', 'daily-notes', 'published'),
  weeklyDir: path.join(__dirname, '..', 'weekly-summaries', 'published'),
  monthlyDir: path.join(__dirname, '..', 'monthly-reports', 'published'),
  outputDir: path.join(__dirname, '..', 'output'),
  projectStart: new Date('2025-11-28'),
  projectEnd: new Date('2032-11-28'),
  books: {
    sunzi: {
      name: '孙子兵法',
      englishName: 'The Art of War',
      tag: '#孙子兵法',
      chapters: 13
    },
    'zizhi-tongjian': {
      name: '资治通鉴',
      englishName: 'Comprehensive Mirror in Aid of Governance',
      tag: '#资治通鉴',
      volumes: 294
    },
    bible: {
      name: '圣经',
      englishName: 'The Holy Bible',
      tag: '#圣经',
      chapters: 1189
    }
  }
};

// Parse command line arguments
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    book: null,
    year: new Date().getFullYear(),
    format: 'markdown', // markdown, pdf, epub
    output: null,
    verbose: false,
    help: false
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--book':
      case '-b':
        options.book = args[++i];
        break;
      case '--year':
      case '-y':
        options.year = parseInt(args[++i]);
        break;
      case '--format':
      case '-f':
        options.format = args[++i];
        break;
      case '--output':
      case '-o':
        options.output = args[++i];
        break;
      case '--verbose':
      case '-v':
        options.verbose = true;
        break;
      case '--help':
      case '-h':
        options.help = true;
        break;
    }
  }

  return options;
}

// Show help
function showHelp() {
  console.log(`
PubHub Book Builder - Compile Annual Notes into Book Manuscripts

Usage:
  node scripts/build-book.js [options]

Options:
  -b, --book <name>      Book to compile: sunzi, zizhi-tongjian, bible
  -y, --year <year>      Year to compile (default: current year)
  -f, --format <type>    Output format: markdown, pdf, epub (default: markdown)
  -o, --output <path>    Output file path
  -v, --verbose          Show detailed output
  -h, --help             Show this help message

Examples:
  # Build Art of War manuscript for 2025
  node scripts/build-book.js --book sunzi --year 2025

  # Build Bible manuscript as PDF
  node scripts/build-book.js --book bible --year 2025 --format pdf

  # Build all books for a year
  node scripts/build-book.js --year 2025
`);
}

// Collect notes for a specific book and year
function collectNotes(bookKey, year) {
  const bookConfig = CONFIG.books[bookKey];
  const tag = bookConfig.tag;
  const notes = [];

  // Scan daily notes
  if (fs.existsSync(CONFIG.dailyNotesDir)) {
    const files = fs.readdirSync(CONFIG.dailyNotesDir)
      .filter(f => f.startsWith(`${year}-`) && f.endsWith('.md'))
      .sort();

    for (const file of files) {
      const filePath = path.join(CONFIG.dailyNotesDir, file);
      const content = fs.readFileSync(filePath, 'utf8');

      if (content.includes(tag)) {
        notes.push({
          type: 'daily',
          date: file.replace('.md', ''),
          file: filePath,
          content: content
        });
      }
    }
  }

  return notes;
}

// Collect monthly reports for a year
function collectMonthlyReports(year) {
  const reports = [];

  if (fs.existsSync(CONFIG.monthlyDir)) {
    const files = fs.readdirSync(CONFIG.monthlyDir)
      .filter(f => f.startsWith(`${year}-`) && f.endsWith('.md'))
      .sort();

    for (const file of files) {
      const filePath = path.join(CONFIG.monthlyDir, file);
      const content = fs.readFileSync(filePath, 'utf8');
      reports.push({
        month: file.replace('.md', ''),
        file: filePath,
        content: content
      });
    }
  }

  return reports;
}

// Extract sections from a note
function extractSections(content) {
  const sections = {};
  const lines = content.split('\n');
  let currentSection = null;
  let sectionContent = [];

  for (const line of lines) {
    const headerMatch = line.match(/^##\s+(.+)$/);
    if (headerMatch) {
      if (currentSection) {
        sections[currentSection] = sectionContent.join('\n').trim();
      }
      currentSection = headerMatch[1];
      sectionContent = [];
    } else if (currentSection) {
      sectionContent.push(line);
    }
  }

  if (currentSection) {
    sections[currentSection] = sectionContent.join('\n').trim();
  }

  return sections;
}

// Calculate project statistics
function calculateStats(notes, year) {
  const totalDays = Math.floor((new Date() - CONFIG.projectStart) / (1000 * 60 * 60 * 24));
  const totalProjectDays = Math.floor((CONFIG.projectEnd - CONFIG.projectStart) / (1000 * 60 * 60 * 24));
  const progress = ((totalDays / totalProjectDays) * 100).toFixed(2);

  let totalWords = 0;
  for (const note of notes) {
    totalWords += note.content.length; // Rough character count
  }

  return {
    notesCount: notes.length,
    totalWords: totalWords,
    projectProgress: progress,
    daysElapsed: totalDays,
    daysRemaining: totalProjectDays - totalDays
  };
}

// Generate book frontmatter
function generateFrontmatter(bookKey, year, stats) {
  const bookConfig = CONFIG.books[bookKey];
  const today = new Date().toISOString().split('T')[0];

  return `---
title: "${bookConfig.name} · AI时代注疏"
english-title: "${bookConfig.englishName}: AI-Era Annotations"
subtitle: "${year}年精读笔记集"
author: "PubHub Project"
date: "${today}"
year: ${year}
book: "${bookKey}"
notes-count: ${stats.notesCount}
total-words: ${stats.totalWords}
project-progress: "${stats.projectProgress}%"
days-elapsed: ${stats.daysElapsed}
days-remaining: ${stats.daysRemaining}
abstract: |
  本书收录${year}年对《${bookConfig.name}》的精读笔记，
  结合2025-2035年AI时代的战略案例进行古今对照分析。
  这是一个为期七年的深度阅读与注疏项目的年度成果。
---

`;
}

// Generate table of contents
function generateTOC(notes, monthlyReports) {
  let toc = '# 目录 / Table of Contents\n\n';

  // Group notes by month
  const notesByMonth = {};
  for (const note of notes) {
    const month = note.date.substring(0, 7);
    if (!notesByMonth[month]) {
      notesByMonth[month] = [];
    }
    notesByMonth[month].push(note);
  }

  // Add monthly chapters
  const months = Object.keys(notesByMonth).sort();
  for (let i = 0; i < months.length; i++) {
    const month = months[i];
    const monthNotes = notesByMonth[month];
    const monthName = new Date(month + '-01').toLocaleDateString('zh-CN', { year: 'numeric', month: 'long' });

    toc += `## 第${i + 1}章 ${monthName}\n\n`;

    for (const note of monthNotes) {
      toc += `- ${note.date}: [笔记](#${note.date})\n`;
    }
    toc += '\n';
  }

  return toc;
}

// Compile book manuscript
function compileBook(bookKey, year, options) {
  const bookConfig = CONFIG.books[bookKey];
  console.log(`\n📚 Compiling: ${bookConfig.name} (${year})`);

  // Collect materials
  const notes = collectNotes(bookKey, year);
  const monthlyReports = collectMonthlyReports(year);
  const stats = calculateStats(notes, year);

  console.log(`   Found ${notes.length} daily notes`);
  console.log(`   Found ${monthlyReports.length} monthly reports`);

  if (notes.length === 0) {
    console.log('   ⚠️  No notes found for this book and year');
    return null;
  }

  // Generate manuscript
  let manuscript = '';

  // Add frontmatter
  manuscript += generateFrontmatter(bookKey, year, stats);

  // Add introduction
  manuscript += `# 导言 / Introduction

本书是七年三书精读项目的${year}年度成果集。

**项目进度**: ${stats.projectProgress}% (第${stats.daysElapsed}天 / 共2557天)

**本年统计**:
- 精读笔记: ${stats.notesCount}篇
- 总字数: 约${Math.floor(stats.totalWords / 1000)}千字

---

`;

  // Add table of contents
  manuscript += generateTOC(notes, monthlyReports);
  manuscript += '\n---\n\n';

  // Add notes organized by month
  const notesByMonth = {};
  for (const note of notes) {
    const month = note.date.substring(0, 7);
    if (!notesByMonth[month]) {
      notesByMonth[month] = [];
    }
    notesByMonth[month].push(note);
  }

  const months = Object.keys(notesByMonth).sort();
  for (let i = 0; i < months.length; i++) {
    const month = months[i];
    const monthNotes = notesByMonth[month];
    const monthName = new Date(month + '-01').toLocaleDateString('zh-CN', { year: 'numeric', month: 'long' });

    manuscript += `# 第${i + 1}章 ${monthName}\n\n`;

    // Add monthly report if exists
    const monthReport = monthlyReports.find(r => r.month === month);
    if (monthReport) {
      manuscript += `## 月度综述\n\n`;
      // Extract summary from monthly report
      const sections = extractSections(monthReport.content);
      if (sections['核心主题'] || sections['Core Themes']) {
        manuscript += sections['核心主题'] || sections['Core Themes'];
        manuscript += '\n\n';
      }
    }

    // Add daily notes
    for (const note of monthNotes) {
      manuscript += `## ${note.date} {#${note.date}}\n\n`;

      // Clean up content (remove duplicate frontmatter)
      let content = note.content;
      content = content.replace(/^---[\s\S]*?---\n*/m, '');
      content = content.replace(/^#\s+.*\n/m, ''); // Remove first H1

      manuscript += content;
      manuscript += '\n\n---\n\n';
    }
  }

  // Add appendix
  manuscript += `# 附录 / Appendix

## 项目说明

本项目始于2025年11月28日，计划于2032年11月28日完成。
目标是完成对三部经典著作的深度阅读与AI时代注疏：

1. **孙子兵法** - 战略智慧
2. **资治通鉴** - 历史洞察
3. **圣经** - 灵性与伦理

每日精读300-500字的原文，结合2025-2035年AI时代的真实案例进行古今对照分析。

## 版权声明

© ${new Date().getFullYear()} PubHub Project. All rights reserved.
`;

  // Determine output path
  const outputFilename = `${bookKey}-${year}`;
  const markdownPath = options.output ||
    path.join(CONFIG.booksDir, bookKey, 'published', `${outputFilename}.md`);

  // Ensure directory exists
  const dir = path.dirname(markdownPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  // Write markdown
  fs.writeFileSync(markdownPath, manuscript);
  console.log(`   ✓ Markdown: ${markdownPath}`);

  // Convert to PDF if requested
  if (options.format === 'pdf') {
    const pdfPath = markdownPath.replace('.md', '.pdf');
    try {
      execSync(`node "${path.join(__dirname, 'build-pdf.js')}" --format book --input "${markdownPath}" --output "${pdfPath}"`, {
        stdio: options.verbose ? 'inherit' : 'pipe'
      });
      console.log(`   ✓ PDF: ${pdfPath}`);
    } catch (error) {
      console.error(`   ✗ PDF generation failed: ${error.message}`);
    }
  }

  return markdownPath;
}

// Main
function main() {
  const options = parseArgs();

  if (options.help) {
    showHelp();
    process.exit(0);
  }

  console.log('\n📖 PubHub Book Builder');
  console.log(`   Year: ${options.year}`);
  console.log(`   Format: ${options.format}`);

  if (options.book) {
    // Build specific book
    if (!CONFIG.books[options.book]) {
      console.error(`Error: Unknown book '${options.book}'`);
      console.error(`Available: ${Object.keys(CONFIG.books).join(', ')}`);
      process.exit(1);
    }
    compileBook(options.book, options.year, options);
  } else {
    // Build all books
    for (const bookKey of Object.keys(CONFIG.books)) {
      compileBook(bookKey, options.year, options);
    }
  }

  console.log('\n✅ Book compilation complete!\n');
}

main();
