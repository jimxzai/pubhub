#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// 获取本月的所有周总结
function getThisMonthWeeklies(baseDir = path.join(__dirname, '..'), dateOverride = null) {
  const today = dateOverride ? new Date(dateOverride) : new Date();
  const year = today.getFullYear();
  const month = today.getMonth() + 1;
  const monthStr = String(month).padStart(2, '0');

  const weekliesDir = path.join(baseDir, 'weekly-summaries/published');
  const weeklies = [];

  if (!fs.existsSync(weekliesDir)) {
    console.log('⚠️  没有找到已发布的周总结。');
    return weeklies;
  }

  const files = fs.readdirSync(weekliesDir);
  files.forEach(file => {
    if (file.startsWith(`${year}-${monthStr}`) && file.endsWith('.md')) {
      const filePath = path.join(weekliesDir, file);
      weeklies.push({
        name: file,
        path: filePath,
        content: fs.readFileSync(filePath, 'utf-8')
      });
    }
  });

  return weeklies;
}

// 计算项目总天数
function getTotalDays(startDate = '2025-11-28', endDate = null) {
  const start = new Date(startDate);
  const end = endDate ? new Date(endDate) : new Date();
  const diffTime = Math.abs(end - start);
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return diffDays;
}

// 计算总字数
function calculateTotalWords(weeklies) {
  return weeklies.reduce((sum, w) => {
    const text = w.content.replace(/[#*>\-`]/g, '');
    return sum + text.length;
  }, 0);
}

// 计算进度百分比
function calculateProgress(totalDays, targetDays = 2557) {
  return ((totalDays / targetDays) * 100).toFixed(2);
}

// 生成月度报告
function generateMonthlyReport(baseDir = path.join(__dirname, '..'), dateOverride = null) {
  const weeklies = getThisMonthWeeklies(baseDir, dateOverride);
  const today = dateOverride ? new Date(dateOverride) : new Date();

  if (weeklies.length === 0) {
    console.log('❌ 本月没有已发布的周总结，无法生成月度报告。');
    return null;
  }

  const year = today.getFullYear();
  const month = today.getMonth() + 1;
  const monthStr = String(month).padStart(2, '0');

  // 读取模板
  const templatePath = path.join(baseDir, 'templates/monthly-report.md');
  const template = fs.readFileSync(templatePath, 'utf-8');

  // 生成周总结列表
  const weekliesList = weeklies.map(w => `- [${w.name}](../weekly-summaries/published/${w.name})`).join('\n');

  // 计算总字数
  const totalWords = calculateTotalWords(weeklies);

  // 计算进度
  const totalDays = getTotalDays();
  const progress = calculateProgress(totalDays);

  // 替换变量
  const content = template
    .replace(/{{YEAR}}/g, year)
    .replace(/{{MONTH}}/g, month)
    .replace(/{{SUBTITLE}}/g, '在此添加本月副标题')
    .replace(/{{DAYS}}/g, weeklies.length * 7) // 粗略估算
    .replace(/{{WORD_COUNT}}/g, totalWords)
    .replace(/{{WEEKLY_COUNT}}/g, weeklies.length)
    .replace(/{{WEEKLY_SUMMARIES_LIST}}/g, weekliesList)
    .replace(/{{TIMESTAMP}}/g, new Date().toISOString())
    .replace(/{{TOTAL_DAYS}}/g, totalDays)
    .replace(/{{PROGRESS}}/g, progress);

  // 保存草稿
  const outputDir = path.join(baseDir, 'monthly-reports/drafts');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const outputPath = path.join(outputDir, `${year}-${monthStr}.md`);
  fs.writeFileSync(outputPath, content, 'utf-8');

  console.log(`✅ 已生成本月报告草稿:`);
  console.log(`   ${outputPath}`);
  console.log(``);
  console.log(`📊 本月统计:`);
  console.log(`   - 周总结: ${weeklies.length}篇`);
  console.log(`   - 总字数: 约${totalWords}字`);
  console.log(`   - 项目进度: ${totalDays}/2557天 (${progress}%)`);
  console.log(``);
  console.log(`📝 接下来请:`);
  console.log(`   1. 打开草稿文件，填写各个部分`);
  console.log(`   2. 使用 Claude Code 帮助整理和深度分析`);
  console.log(`   3. 完成后移动到 monthly-reports/published/`);

  return { outputPath, weeklies, totalWords, totalDays, progress };
}

// 仅在直接执行时运行
if (require.main === module) {
  const result = generateMonthlyReport();
  if (!result) {
    process.exit(1);
  }
}

// 导出供测试使用
module.exports = {
  getThisMonthWeeklies,
  getTotalDays,
  calculateTotalWords,
  calculateProgress,
  generateMonthlyReport
};
