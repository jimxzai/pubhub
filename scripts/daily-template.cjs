#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// 获取今日日期
const today = new Date();
const dateStr = today.toISOString().split('T')[0]; // YYYY-MM-DD
const timeStr = today.toTimeString().split(' ')[0]; // HH:MM:SS

// 读取模板
const templatePath = path.join(__dirname, '../templates/daily-note.md');
const template = fs.readFileSync(templatePath, 'utf-8');

// 替换变量
const content = template
  .replace(/{{DATE}}/g, dateStr)
  .replace(/{{TIME}}/g, timeStr)
  .replace(/{{BOOK}}/g, '')
  .replace(/{{CHAPTER}}/g, '')
  .replace(/{{TOPIC}}/g, '');

// 创建文件
const outputDir = path.join(__dirname, '../daily-notes/drafts');
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

const outputPath = path.join(outputDir, `${dateStr}.md`);

if (fs.existsSync(outputPath)) {
  console.log(`⚠️  今日笔记已存在: ${outputPath}`);
  console.log(`如需重新生成，请先删除该文件。`);
  process.exit(1);
}

fs.writeFileSync(outputPath, content, 'utf-8');

console.log(`✅ 已生成今日笔记模板:`);
console.log(`   ${outputPath}`);
console.log(``);
console.log(`📝 接下来请:`);
console.log(`   1. 用你喜欢的编辑器打开该文件`);
console.log(`   2. 填写今日心得（300-500字）`);
console.log(`   3. 使用 Claude Skills 优化笔记 (可选)`);
console.log(``);
console.log(`🤖 Claude Skills (在 Claude Code 中运行):`);
console.log(`   /annotate        → 获取历史注疏和中英对照`);
console.log(`   /ai-parallels    → 映射到AI时代案例`);
console.log(`   /master-editor   → 分析评估笔记质量`);
console.log(`   /proofread       → 校对润色最终版本`);
console.log(``);
console.log(`📤 发布:`);
console.log(`   mv ${outputPath} daily-notes/published/`);
console.log(`   git add . && git commit -m "📝 Daily note: ${dateStr}"`);
console.log(``);
console.log(`💡 提示: 详见 WORKFLOW_GUIDE.md`);
