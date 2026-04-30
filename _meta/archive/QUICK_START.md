# 快速开始指南

欢迎使用**三书精读出版系统**！

## 5分钟快速上手

### 第一步：初始化项目

```bash
cd three-books-publishing

# 初始化Git仓库
git init
git add .
git commit -m "🎉 开始7年三书精读之旅"

# （可选）创建GitHub仓库
gh repo create three-books-publishing --private
git push -u origin main
```

### 第二步：生成第一篇每日笔记

```bash
node scripts/daily-template.js
```

这会在 `daily-notes/drafts/` 下创建今天的笔记模板。

### 第三步：填写笔记

用你喜欢的编辑器打开生成的文件，填写：
- 今日阅读的书目和章节
- 原文摘要（中英对照）
- 你的理解和心得（300-500字）
- AI时代的对应
- 对7年大业的启发

### 第四步：发布笔记

```bash
# 移动到已发布目录
mv daily-notes/drafts/2025-11-28.md daily-notes/published/

# 提交到Git
git add .
git commit -m "📝 Daily note: 2025-11-28"
git push
```

## Claude Code "Agentic团队"使用方法

### Agent 1: 总编辑

分析和改进你的每日笔记：

```
/master-editor
```

然后在对话中提供你的笔记内容，AI会：
- 分类笔记（书名、章节、主题）
- 评估质量（1-5分）
- 提供改进建议
- 建议标签

### Agent 2: 注疏师

为经典章节添加深度注疏：

```
/annotate
```

提供章节名称（如"孙子兵法·始计篇"），AI会：
- 提供中英对照原文
- 摘录历代注疏精华
- 解析关键词
- 补充历史背景

### Agent 3: AI战略家

映射到AI时代战例：

```
/ai-parallels
```

提供你的笔记或经典段落，AI会：
- 提炼核心战略原则
- 找到2025-2035年AI战例
- 推演未来博弈
- 给出实践建议

### Agent 4: 校对神

润色和校对文本：

```
/proofread
```

提供需要校对的文本，AI会：
- 中英双语润色
- 逻辑检查
- 引文核对
- 格式规范

### Agent 5: 出书总管

生成周报、月报、书稿：

```
/publish
```

然后选择模式（weekly/monthly/book），AI会自动整合所有内容。

## 每日工作流示例

### 早上（60-90分钟）

```bash
# 1. 生成今日笔记模板
npm run new-note

# 2. 阅读原文（纸质书）+ NotebookLM音频
# （手动进行，30-40分钟）

# 3. 填写笔记
# 用 VS Code、Obsidian 或任何编辑器打开今日笔记
code daily-notes/drafts/$(date +%Y-%m-%d).md

# 4. 使用Claude Code优化笔记
# 在Claude Code中运行:
# /master-editor
# 复制粘贴你的笔记，获取改进建议

# 5. 发布笔记
mv daily-notes/drafts/$(date +%Y-%m-%d).md daily-notes/published/
git add . && git commit -m "📝 Daily note: $(date +%Y-%m-%d)" && git push
```

### 每周六（30分钟）

```bash
# 方式1: 本地运行脚本
npm run weekly-summary

# 方式2: 使用Claude Code Agent
# /publish --type weekly

# 审阅并完善
code weekly-summaries/*.md

# 发布
git add . && git commit -m "📊 Weekly summary" && git push
```

### 每月末（1小时）

```bash
# 方式1: 本地运行脚本
npm run monthly-report

# 方式2: 使用Claude Code Agent
# /publish --type monthly

# 深度完善月度专章（使用Claude Code各个Agent辅助）
code monthly-reports/*.md

# 发布
git add . && git commit -m "📖 Monthly report" && git push
```

## 进阶技巧

### 1. 配合Obsidian使用

将整个项目目录作为Obsidian的vault：
- 利用Obsidian的双向链接功能
- 使用标签和搜索快速定位
- 可视化笔记之间的关联

### 2. 本地搜索

```bash
# 搜索所有提到"知己知彼"的笔记
grep -r "知己知彼" daily-notes/published/

# 搜索所有孙子兵法相关笔记
grep -r "#孙子兵法" daily-notes/published/
```

### 3. 统计进度

```bash
# 查看已写笔记数
ls daily-notes/published/ | wc -l

# 查看总字数
wc -w daily-notes/published/*.md weekly-summaries/*.md
```

### 4. 备份

```bash
# 定期备份到外部存储
rsync -av three-books-publishing/ /path/to/backup/

# 或使用GitHub作为云备份（已经在用）
git push
```

## 自动化功能

### GitHub Actions

一旦推送到GitHub，以下任务会自动执行：

- **每周六08:00** - 自动生成周总结草稿并创建PR
- **每月1日08:00** - 自动生成月度报告草稿并创建PR

你只需要审阅PR，完善内容，然后合并即可。

## 常见问题

### Q: 我不想用GitHub，可以吗？

A: 完全可以！只使用本地脚本即可：
```bash
npm run new-note
npm run weekly-summary
npm run monthly-report
```

### Q: 可以修改模板吗？

A: 当然！模板都在 `templates/` 目录下，随意定制。

### Q: NotebookLM怎么用？

A: NotebookLM是Google的独立产品，需要手动使用：
1. 访问 notebooklm.google.com
2. 创建新项目，上传原文PDF或文本
3. 点击"Generate Audio Overview"
4. 听AI对谈，记录洞见

### Q: Claude Code的命令不工作？

A: 确保 `.claude/commands/` 目录存在且命令文件格式正确。
在Claude Code中输入 `/` 应该能看到所有可用命令。

### Q: 我可以邀请别人一起参与吗？

A: 可以！把GitHub仓库设为协作模式，邀请合作者即可。

---

## 下一步

现在你已经准备好开始7年的智慧之旅了！

**立即行动**:
```bash
npm run new-note
```

然后打开生成的文件，写下你的第一篇心得。

**7年后的今天**（2032-11-28），你将拥有：
- 2500+ 篇每日心得
- 350+ 篇周总结
- 84 篇月度专章
- 3-4 本可出版的传世之作

**开始日期**: 2025-11-28
**预计完成**: 2032-11-28
**第1天，加油！** 💪
