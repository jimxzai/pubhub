#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// 获取本月的所有周总结
function getThisMonthWeeklies() {
  const today = new Date();
  const year = today.getFullYear();
  const month = today.getMonth() + 1;
  const monthStr = String(month).padStart(2, '0');

  const weekliesDir = path.join(__dirname, '../weekly-summaries/published');
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
function getTotalDays() {
  const startDate = new Date('2025-11-28');
  const today = new Date();
  const diffTime = Math.abs(today - startDate);
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return diffDays;
}

// 生成月度报告
function generateMonthlyReport() {
  const weeklies = getThisMonthWeeklies();

  if (weeklies.length === 0) {
    console.log('❌ 本月没有已发布的周总结，无法生成月度报告。');
    process.exit(1);
  }

  const today = new Date();
  const year = today.getFullYear();
  const month = today.getMonth() + 1;
  const monthStr = String(month).padStart(2, '0');

  // 读取模板
  const templatePath = path.join(__dirname, '../templates/monthly-report.md');
  const template = fs.readFileSync(templatePath, 'utf-8');

  // 生成周总结列表
  const weekliesList = weeklies.map(w => `- [${w.name}](../weekly-summaries/published/${w.name})`).join('\n');

  // 计算总字数
  const totalWords = weeklies.reduce((sum, w) => {
    const text = w.content.replace(/[#*>\-`]/g, '');
    return sum + text.length;
  }, 0);

  // 计算进度
  const totalDays = getTotalDays();
  const progress = ((totalDays / 2557) * 100).toFixed(2);

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
  const outputDir = path.join(__dirname, '../monthly-reports/drafts');
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
}

// 执行
generateMonthlyReport();
