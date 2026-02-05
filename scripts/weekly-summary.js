#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// 获取本周的开始日期（周一）
function getWeekMonday(date = new Date()) {
  const today = new Date(date);
  const dayOfWeek = today.getDay();
  const monday = new Date(today);
  monday.setDate(today.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1));
  return monday;
}

// 获取本周的所有每日笔记
function getThisWeekNotes(baseDir = path.join(__dirname, '..'), dateOverride = null) {
  const monday = getWeekMonday(dateOverride);
  const notesDir = path.join(baseDir, 'daily-notes/published');
  const notes = [];

  if (!fs.existsSync(notesDir)) {
    console.log('⚠️  没有找到已发布的每日笔记。');
    console.log('请先将草稿移动到 daily-notes/published/ 目录。');
    return notes;
  }

  for (let i = 0; i < 7; i++) {
    const date = new Date(monday);
    date.setDate(monday.getDate() + i);
    const dateStr = date.toISOString().split('T')[0];
    const notePath = path.join(notesDir, `${dateStr}.md`);

    if (fs.existsSync(notePath)) {
      notes.push({
        date: dateStr,
        path: notePath,
        content: fs.readFileSync(notePath, 'utf-8')
      });
    }
  }

  return notes;
}

// 统计书籍阅读次数
function countBookReading(notes) {
  const counts = { sunzi: 0, zizhi: 0, bible: 0 };

  notes.forEach(note => {
    if (note.content.includes('#孙子兵法') || note.content.includes('#sunzi')) {
      counts.sunzi++;
    }
    if (note.content.includes('#资治通鉴') || note.content.includes('#zizhi')) {
      counts.zizhi++;
    }
    if (note.content.includes('#圣经') || note.content.includes('#bible')) {
      counts.bible++;
    }
  });

  return counts;
}

// 计算总字数
function calculateWordCount(notes) {
  return notes.reduce((sum, note) => {
    // 简单估算：去除Markdown标记后的字符数
    const text = note.content.replace(/[#*>\-`]/g, '');
    return sum + text.length;
  }, 0);
}

// 生成周范围字符串
function getWeekRange(date = new Date()) {
  const today = new Date(date);
  const weekNum = Math.ceil((today.getDate()) / 7);
  return `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-W${weekNum}`;
}

// 生成周总结
function generateWeeklySummary(baseDir = path.join(__dirname, '..'), dateOverride = null) {
  const notes = getThisWeekNotes(baseDir, dateOverride);
  const today = dateOverride ? new Date(dateOverride) : new Date();

  if (notes.length === 0) {
    console.log('❌ 本周没有已发布的笔记，无法生成周总结。');
    return null;
  }

  const counts = countBookReading(notes);
  const weekRange = getWeekRange(today);

  // 读取模板
  const templatePath = path.join(baseDir, 'templates/weekly-summary.md');
  const template = fs.readFileSync(templatePath, 'utf-8');

  // 生成笔记列表
  const notesList = notes.map(note => `- [${note.date}](../daily-notes/published/${path.basename(note.path)})`).join('\n');

  // 计算总字数
  const totalWords = calculateWordCount(notes);

  // 替换变量
  const content = template
    .replace(/{{WEEK_RANGE}}/g, weekRange)
    .replace(/{{DAYS}}/g, notes.length)
    .replace(/{{SUNZI_COUNT}}/g, counts.sunzi)
    .replace(/{{ZIZHI_COUNT}}/g, counts.zizhi)
    .replace(/{{BIBLE_COUNT}}/g, counts.bible)
    .replace(/{{DAILY_NOTES_LIST}}/g, notesList)
    .replace(/{{WORD_COUNT}}/g, totalWords)
    .replace(/{{TIMESTAMP}}/g, new Date().toISOString());

  // 保存草稿
  const outputDir = path.join(baseDir, 'weekly-summaries/drafts');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const outputPath = path.join(outputDir, `${weekRange}.md`);
  fs.writeFileSync(outputPath, content, 'utf-8');

  console.log(`✅ 已生成本周总结草稿:`);
  console.log(`   ${outputPath}`);
  console.log(``);
  console.log(`📊 本周统计:`);
  console.log(`   - 笔记数: ${notes.length}天`);
  console.log(`   - 孙子兵法: ${counts.sunzi}次`);
  console.log(`   - 资治通鉴: ${counts.zizhi}次`);
  console.log(`   - 圣经: ${counts.bible}次`);
  console.log(`   - 总字数: 约${totalWords}字`);
  console.log(``);
  console.log(`📝 接下来请:`);
  console.log(`   1. 打开草稿文件，完善核心主题和金句`);
  console.log(`   2. 可以使用 Claude Code 帮助润色和扩充`);
  console.log(`   3. 完成后移动到 weekly-summaries/published/`);

  return { outputPath, notes, counts, totalWords, weekRange };
}

// 仅在直接执行时运行
if (require.main === module) {
  const result = generateWeeklySummary();
  if (!result) {
    process.exit(1);
  }
}

// 导出供测试使用
module.exports = {
  getWeekMonday,
  getThisWeekNotes,
  countBookReading,
  calculateWordCount,
  getWeekRange,
  generateWeeklySummary
};
