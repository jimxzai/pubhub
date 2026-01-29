#!/usr/bin/env node

/**
 * 圣经与资治通鉴时空宇宙观 - 书稿构建脚本
 *
 * 功能：
 * 1. 合并所有markdown文件为单一书稿
 * 2. 生成目录
 * 3. 输出为可用于PDF转换的格式
 *
 * 用法：
 *   node scripts/build-bible-tongjian-book.js [options]
 *
 * 选项：
 *   --volume <n>    只构建第n卷 (1-8)
 *   --all           构建全部8卷合集
 *   --academic      构建学术资源
 *   --training      构建培训材料
 *   --output <path> 指定输出路径
 */

const fs = require('fs');
const path = require('path');

// 项目根目录
const PROJECT_ROOT = path.join(__dirname, '..', 'books', 'bible-tongjian-parallel');
const OUTPUT_DIR = path.join(PROJECT_ROOT, 'output');

// 书籍结构定义
const BOOK_STRUCTURE = {
  frontMatter: [
    'README.md',
    '00-progressive-revelation.md',
    '00-four-themes.md',
    '00-readers-guide.md',
  ],
  volumes: [
    { num: 1, title: '第一卷：透视人性（上）', file: '01-human-nature-part1.md' },
    { num: 2, title: '第二卷：透视人性（下）', file: '02-human-nature-part2.md' },
    { num: 3, title: '第三卷：寻找出路（上）', file: '03-seeking-way-part1.md' },
    { num: 4, title: '第四卷：寻找出路（下）', file: '04-seeking-way-part2.md' },
    { num: 5, title: '第五卷：认识神的计划（上）', file: '05-gods-plan-part1.md' },
    { num: 6, title: '第六卷：认识神的计划（下）', file: '06-gods-plan-part2.md' },
    { num: 7, title: '第七卷：明白属灵争战（上）', file: '07-spiritual-warfare-part1.md' },
    { num: 8, title: '第八卷：明白属灵争战（下）', file: '08-spiritual-warfare-part2.md' },
  ],
  appendices: [
    { title: '属灵争战专论', file: '09-spiritual-warfare.md' },
    { title: 'AI时代镜鉴', file: '10-ai-era-mirror.md' },
    { title: '人物传记', file: '11-biographies.md' },
    { title: '地理志', file: '12-geography.md' },
    { title: '考古篇', file: '13-archaeology.md' },
    { title: '节期与礼仪', file: '14-festivals.md' },
    { title: '家庭与伦理', file: '15-family-ethics.md' },
  ],
  indices: [
    { title: '时间线对照', file: 'appendix-timeline.md' },
    { title: '人物索引', file: 'appendix-character-index.md' },
    { title: '主题索引', file: 'appendix-theme-index.md' },
    { title: '原文引用', file: 'appendix-original-texts.md' },
    { title: '地图与图表', file: 'appendix-maps-charts.md' },
  ]
};

// 学术资源结构
const ACADEMIC_STRUCTURE = {
  title: '学术资源集',
  files: [
    'academic/seminary-courses.md',
    'academic/research-papers.md',
  ]
};

// 培训材料结构
const TRAINING_STRUCTURE = {
  title: '培训材料集',
  files: [
    'training/leader-training-manual.md',
    'training/facilitator-guide.md',
    'community/community-building-guide.md',
    'community/content-update-mechanism.md',
  ]
};

// 辅助函数
function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
    console.log(`📁 创建目录: ${dir}`);
  }
}

function readFile(filePath) {
  const fullPath = path.join(PROJECT_ROOT, filePath);
  if (fs.existsSync(fullPath)) {
    return fs.readFileSync(fullPath, 'utf-8');
  }
  console.warn(`⚠️  文件不存在: ${filePath}`);
  return `\n\n> [待完成] ${filePath}\n\n`;
}

function addPageBreak() {
  return '\n\n\\newpage\n\n';
}

function generateTOC(structure) {
  let toc = '# 目录\n\n';

  toc += '## 前言部分\n';
  toc += '- 序言\n';
  toc += '- 渐进启示导论\n';
  toc += '- 四大主题\n';
  toc += '- 读者指南\n\n';

  toc += '## 正文\n';
  structure.volumes.forEach(v => {
    toc += `- ${v.title}\n`;
  });
  toc += '\n';

  toc += '## 附录\n';
  structure.appendices.forEach(a => {
    toc += `- ${a.title}\n`;
  });
  toc += '\n';

  toc += '## 索引\n';
  structure.indices.forEach(i => {
    toc += `- ${i.title}\n`;
  });

  return toc;
}

function buildFullBook() {
  console.log('📚 构建完整书稿...\n');

  let content = '';

  // 书名页
  content += '---\n';
  content += 'title: "圣经与资治通鉴时空宇宙观"\n';
  content += 'subtitle: "历史长河中的福音对话"\n';
  content += 'author: ""\n';
  content += 'date: "' + new Date().toISOString().split('T')[0] + '"\n';
  content += 'lang: zh-CN\n';
  content += 'documentclass: book\n';
  content += 'papersize: a4\n';
  content += 'fontsize: 11pt\n';
  content += 'geometry: margin=2.5cm\n';
  content += 'toc: true\n';
  content += 'toc-depth: 3\n';
  content += 'numbersections: true\n';
  content += '---\n\n';

  // 前言部分
  console.log('  📖 添加前言部分...');
  BOOK_STRUCTURE.frontMatter.forEach(file => {
    content += readFile(file);
    content += addPageBreak();
  });

  // 正文卷册
  console.log('  📖 添加正文卷册...');
  BOOK_STRUCTURE.volumes.forEach(vol => {
    console.log(`     - ${vol.title}`);
    content += `# ${vol.title}\n\n`;
    content += readFile(vol.file);
    content += addPageBreak();
  });

  // 附录
  console.log('  📖 添加附录...');
  content += '# 附录\n\n';
  BOOK_STRUCTURE.appendices.forEach(app => {
    console.log(`     - ${app.title}`);
    content += `## ${app.title}\n\n`;
    content += readFile(app.file);
    content += addPageBreak();
  });

  // 索引
  console.log('  📖 添加索引...');
  content += '# 索引\n\n';
  BOOK_STRUCTURE.indices.forEach(idx => {
    console.log(`     - ${idx.title}`);
    content += `## ${idx.title}\n\n`;
    content += readFile(idx.file);
    content += addPageBreak();
  });

  // 版权页
  content += '# 版权信息\n\n';
  content += '**Soli Deo Gloria — 唯独荣耀归于神**\n\n';
  content += `构建日期: ${new Date().toLocaleDateString('zh-CN')}\n\n`;

  return content;
}

function buildSingleVolume(volumeNum) {
  const vol = BOOK_STRUCTURE.volumes.find(v => v.num === volumeNum);
  if (!vol) {
    console.error(`❌ 卷册 ${volumeNum} 不存在`);
    process.exit(1);
  }

  console.log(`📚 构建 ${vol.title}...\n`);

  let content = '';

  // YAML 头
  content += '---\n';
  content += `title: "${vol.title}"\n`;
  content += 'subtitle: "圣经与资治通鉴时空宇宙观"\n';
  content += 'lang: zh-CN\n';
  content += 'documentclass: article\n';
  content += 'papersize: a4\n';
  content += 'fontsize: 11pt\n';
  content += 'geometry: margin=2.5cm\n';
  content += 'toc: true\n';
  content += '---\n\n';

  content += readFile(vol.file);

  return content;
}

function buildAcademic() {
  console.log('📚 构建学术资源集...\n');

  let content = '';

  content += '---\n';
  content += 'title: "圣经与资治通鉴 - 学术资源"\n';
  content += 'subtitle: "神学院课程与研究论文大纲"\n';
  content += 'lang: zh-CN\n';
  content += 'documentclass: article\n';
  content += 'papersize: a4\n';
  content += 'fontsize: 11pt\n';
  content += 'geometry: margin=2.5cm\n';
  content += 'toc: true\n';
  content += '---\n\n';

  ACADEMIC_STRUCTURE.files.forEach(file => {
    console.log(`  📖 添加: ${file}`);
    content += readFile(file);
    content += addPageBreak();
  });

  return content;
}

function buildTraining() {
  console.log('📚 构建培训材料集...\n');

  let content = '';

  content += '---\n';
  content += 'title: "圣经与资治通鉴 - 培训材料"\n';
  content += 'subtitle: "领袖培训与社群建立指南"\n';
  content += 'lang: zh-CN\n';
  content += 'documentclass: article\n';
  content += 'papersize: a4\n';
  content += 'fontsize: 11pt\n';
  content += 'geometry: margin=2.5cm\n';
  content += 'toc: true\n';
  content += '---\n\n';

  TRAINING_STRUCTURE.files.forEach(file => {
    console.log(`  📖 添加: ${file}`);
    content += readFile(file);
    content += addPageBreak();
  });

  return content;
}

function writeOutput(content, filename) {
  ensureDir(OUTPUT_DIR);
  const outputPath = path.join(OUTPUT_DIR, filename);
  fs.writeFileSync(outputPath, content, 'utf-8');
  console.log(`\n✅ 已生成: ${outputPath}`);
  return outputPath;
}

// 主函数
function main() {
  const args = process.argv.slice(2);

  console.log('═══════════════════════════════════════════════════════════');
  console.log('   圣经与资治通鉴时空宇宙观 - 书稿构建工具');
  console.log('═══════════════════════════════════════════════════════════\n');

  let content = '';
  let filename = '';

  if (args.includes('--all') || args.length === 0) {
    content = buildFullBook();
    filename = 'bible-tongjian-complete.md';
  } else if (args.includes('--volume')) {
    const volIndex = args.indexOf('--volume');
    const volNum = parseInt(args[volIndex + 1]);
    content = buildSingleVolume(volNum);
    filename = `bible-tongjian-vol${volNum}.md`;
  } else if (args.includes('--academic')) {
    content = buildAcademic();
    filename = 'bible-tongjian-academic.md';
  } else if (args.includes('--training')) {
    content = buildTraining();
    filename = 'bible-tongjian-training.md';
  } else {
    console.log('用法:');
    console.log('  node scripts/build-bible-tongjian-book.js          # 构建完整书稿');
    console.log('  node scripts/build-bible-tongjian-book.js --all    # 同上');
    console.log('  node scripts/build-bible-tongjian-book.js --volume 1  # 只构建第1卷');
    console.log('  node scripts/build-bible-tongjian-book.js --academic  # 构建学术资源');
    console.log('  node scripts/build-bible-tongjian-book.js --training  # 构建培训材料');
    process.exit(0);
  }

  const outputPath = writeOutput(content, filename);

  console.log('\n───────────────────────────────────────────────────────────');
  console.log('📝 下一步: 转换为PDF');
  console.log('───────────────────────────────────────────────────────────\n');
  console.log('1. 安装 pandoc (如果还没安装):');
  console.log('   brew install pandoc');
  console.log('   brew install --cask mactex-no-gui  # 或 basictex\n');
  console.log('2. 转换为PDF:');
  console.log(`   pandoc "${outputPath}" -o "${outputPath.replace('.md', '.pdf')}" \\`);
  console.log('     --pdf-engine=xelatex \\');
  console.log('     -V mainfont="PingFang SC" \\');
  console.log('     -V CJKmainfont="PingFang SC" \\');
  console.log('     --toc --toc-depth=3\n');
  console.log('或使用简化命令:');
  console.log('   npm run pdf\n');
}

main();
