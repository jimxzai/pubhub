# PubHub 快速参考卡

## 每日命令

```bash
npm run new-note      # 创建今日笔记
```

## 5个 Claude Skills

| 命令 | 协作者 | 用途 |
|------|--------|------|
| `/master-editor` | 总编辑 | 分析评估 (14/20分+) |
| `/annotate` | 注疏师 | 历史注疏+中英对照 |
| `/ai-parallels` | AI战略家 | AI时代案例映射 |
| `/proofread` | 校对神 | 校对润色 |
| `/publish` | 出书总管 | 周报/月报/书稿 |

## 每日工作流 (60-90分钟)

```
1. npm run new-note           # 创建笔记
2. 阅读原文 + 写初稿          # 30+30分钟
3. /annotate                  # 可选: 获取注疏
4. /ai-parallels              # 可选: AI映射
5. /master-editor             # 分析评估
6. /proofread                 # 最终润色
7. git add && commit && push  # 发布
```

## 周度/月度

```bash
/publish --type weekly   # 周六: 生成周报
/publish --type monthly  # 月末: 生成月报
```

## 质量标准

**每日 (300-500字)**:
- [ ] 原文引用准确
- [ ] 有独特洞见
- [ ] AI案例真实
- [ ] 逻辑连贯

**目标分数**: 14/20分以上

## 禁止

- ❌ "非常棒"、"太厉害了"
- ❌ "让我们一起"、"深入探讨"
- ❌ "赋能"、"颠覆"
- ❌ 杜撰注疏/AI事件

## 三书版本

| 书 | 中文 | 英文 |
|----|------|------|
| 孙子 | 十一家注本 | Griffith |
| 通鉴 | 胡三省本 | 伯克利 |
| 圣经 | 和合本修订 | ESV |

## Git 提交格式

```bash
📝 Daily note: YYYY-MM-DD [书名]
📊 Weekly summary: YYYY-WNN
📖 Monthly report: YYYY-MM
```

---

**详细指南**: `WORKFLOW_GUIDE.md`
**配置说明**: `.claude/README.md`
