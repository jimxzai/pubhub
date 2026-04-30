# .claude/

Claude Code 配置目录。

## 文件结构

```
.claude/
├── README.md              # 本文件
├── settings.json          # 项目共享配置（团队约定，签入 git）
├── settings.local.json    # 本地权限配置（个人允许列表）
└── commands/              # Slash commands / Skills
    ├── today.md           # /today - 今日写作助手
    ├── master-editor.md   # /master-editor - 总编辑（四维透视评估）
    ├── annotate.md        # /annotate - 注疏师（救赎历史定位）
    ├── ai-parallels.md    # /ai-parallels - AI 战略家（信望爱框架）
    ├── proofread.md       # /proofread - 校对神（神学准确性）
    ├── publish.md         # /publish - 出书总管（周/月/书稿）
    ├── weekly.md          # /weekly - 周报生成
    └── monthly.md         # /monthly - 月报生成
```

## 工作原则

- **核心精神**: 透视人性、出路、神的计划、争战、永恆（详见 [`../CLAUDE.md`](../CLAUDE.md)）
- **写作标准**: 每日 300-500 字、周报 1000-2000 字、月报 5000+ 字
- **质量底线**: 引文准确、案例真实、逻辑连贯、有非常识洞见
- **禁止**: 空洞溢美、AI 腔调、商业术语、杜撰注疏、编造 AI 事件

## 配置约定

- `settings.json` 是签入 git 的团队配置；`settings.local.json` 是 `.gitignore` 之外的个人权限。修改前者影响所有协作者，修改后者只影响本机。
- Slash commands 用前置 frontmatter (`description`, `allowed-tools`) 声明元数据，正文是 prompt。
- 修改 skill 后无需重启；下次调用即生效。

## 相关文档

- [`../CLAUDE.md`](../CLAUDE.md) — 项目说明（核心异象、工作流、三书版本、质量标准）
- [`../_meta/WORKFLOW_GUIDE.md`](../_meta/WORKFLOW_GUIDE.md) — 完整工作流
- [`../_meta/SEVEN_YEAR_ROADMAP.md`](../_meta/SEVEN_YEAR_ROADMAP.md) — 7 年路线图
- [`../_meta/THEOLOGICAL_FRAMEWORK.md`](../_meta/THEOLOGICAL_FRAMEWORK.md) — 神学框架
