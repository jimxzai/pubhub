#!/usr/bin/env node
// pnpm stats — what has actually been written. Counts files, never estimates.
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const md = (dir) => {
  const full = path.join(root, dir);
  return fs.existsSync(full) ? fs.readdirSync(full).filter((f) => f.endsWith('.md') && !f.startsWith('.') && !f.startsWith('_')) : [];
};
const latest = (files) => (files.length ? files.sort().at(-1).replace(/\.md$/, '') : '—');

const rows = [
  ['每日筆記 · 草稿', 'daily-notes/drafts'],
  ['每日筆記 · 已發布', 'daily-notes/published'],
  ['週報', 'weekly-summaries'],
  ['月報', 'monthly-reports'],
].map(([label, dir]) => {
  const files = md(dir);
  return { label, count: files.length, latest: latest(files) };
});

const booksDir = path.join(root, 'books/bible');
const books = fs.existsSync(booksDir)
  ? fs.readdirSync(booksDir, { withFileTypes: true }).filter((d) => d.isDirectory())
  : [];

console.log('筆記');
for (const r of rows) console.log(`  ${r.label.padEnd(12, '　')} ${String(r.count).padStart(4)}   最新: ${r.latest}`);
console.log(`\n聖經書卷目錄: ${books.length}`);
console.log('各書的頁數、溢出、骨幹與評分請看 docs/library-status.md（python3 scripts/gen-library-status.py）');
