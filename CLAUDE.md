# CLAUDE.md - Project Instructions for Claude Code

## Project Overview

**Project Name**: 三書精讀出版系統 (Three Books Deep Reading & Publishing System)
**Primary Focus (MVP)**: 約翰福音研讀 (Gospel of John Study) ✅ COMPLETE
**Current Phase**: Phase 4 - Expansion (Luke, Acts, Johannine Epistles)
**Timeline**: 7-year plan (2025-2032)
**Tech Stack**: Next.js 16.1 + Tailwind 4 + Turbopack + pnpm + Claude AI
**Version**: 3.0.0

---

## Quick Reference

### Build Commands

```bash
pnpm install          # Install dependencies
pnpm dev              # Start dev server with Turbopack
pnpm build            # Production build
pnpm start            # Start production server
pnpm lint             # Run ESLint
pnpm typecheck        # Run TypeScript check
pnpm test             # Run tests with Vitest
pnpm test:run         # Run tests once
pnpm test:coverage    # Run tests with coverage
```

### Claude Skills (Slash Commands)

| Command | Agent | Function |
|---------|-------|----------|
| `/master-editor` | 總編輯 | Analyze and classify daily notes |
| `/annotate` | 注疏師 | Add historical commentary, bilingual |
| `/ai-parallels` | AI戰略家 | Map to 2025-2035 AI cases |
| `/proofread` | 校對神 | Bilingual proofreading |
| `/publish` | 出書總管 | Generate reports and manuscripts |

---

## Project Structure

```
pubhub/
├── CLAUDE.md                    # This file: Project instructions
├── package.json                 # pnpm + Next.js 16.1 + Tailwind 4
├── next.config.ts              # Turbopack configuration
├── pnpm-lock.yaml              # pnpm lockfile
├── .npmrc                      # pnpm settings
│
├── .claude/                    # Claude AI configuration
│   ├── settings.json           # Project settings
│   ├── CONTENT_RULES.md        # Content quality rules
│   ├── STYLE_GUIDE.md          # Code & doc style guide
│   ├── commands/               # AI Agent commands (skills)
│   │   ├── master-editor.md
│   │   ├── annotate.md
│   │   ├── ai-parallels.md
│   │   ├── proofread.md
│   │   └── publish.md
│   └── prompts/                # System prompts
│       └── system-context.md
│
├── docs/                       # Documentation
│   ├── BRD-gospel-of-john.md   # Business Requirements
│   ├── PRD-gospel-of-john.md   # Product Requirements
│   ├── study-notes/            # Study notes by chapter
│   └── sermons/                # Sermon outlines
│
├── daily-notes/                # Daily devotional notes
│   ├── drafts/
│   │   └── thursday-wong/      # Elder Wong's materials
│   └── published/
│
├── books/                      # Book manuscripts
│   ├── sunzi/                  # 孫子兵法
│   ├── zizhi-tongjian/         # 資治通鑑
│   └── bible/                  # 聖經
│       ├── gospel-of-john/     # ✅ 約翰福音 (21 chapters complete)
│       ├── gospel-of-luke/     # 路加福音
│       ├── acts/               # 使徒行傳
│       ├── johannine-epistles/ # 約翰書信
│       ├── james/              # 雅各書
│       └── ...
│
├── templates/                  # Markdown templates
├── scripts/                    # Automation scripts
└── app/                        # Next.js App Router (future)
```

---

## MVP Focus: Gospel of John

### Core Resources (三方整合)

1. **黃長老 (Elder Wong)** - 第一手教導
   - 週四查經班 Zoom 錄影
   - 查經筆記與大綱

2. **gty.org** - John MacArthur
   - 逐節解經講道
   - MacArthur Study Bible

3. **G. Campbell Morgan** - 解經王子
   - *The Gospel According to John* (1909)
   - 屬靈組織分析法

### Daily Rhythm

```
📖 早晨 (45-60分鐘)
├── 1. 禱告預備
├── 2. 經文朗讀 (RCUV + ESV)
├── 3. 黃長老教導
├── 4. MacArthur 講道/注釋
├── 5. Campbell Morgan 洞見
└── 6. 筆記記錄

🌙 晚間 (15分鐘)
├── 回顧經文
├── 反思應用
└── 禱告回應
```

### Gospel of John Structure

| Part | Chapters | Theme |
|------|----------|-------|
| 序言 | 1:1-18 | 道的本質 |
| 公開事工 | 1:19-12:50 | 神蹟與講論 |
| 私下教導 | 13-17 | 馬可樓上講論 |
| 受難復活 | 18-21 | 榮耀的高峰 |

**七個神蹟**: 水變酒、醫大臣子、醫瘸腿、五餅二魚、海面行走、醫瞎眼、拉撒路復活

**七個「我是」**: 生命的糧、世界的光、羊的門、好牧人、復活/生命、道路/真理/生命、真葡萄樹

---

## Coding Standards

### TypeScript

- Strict mode enabled
- Use `interface` over `type` for objects
- Prefer `const` over `let`
- Use descriptive variable names

### File Naming

- Components: `PascalCase.tsx`
- Utilities: `camelCase.ts`
- Constants: `SCREAMING_SNAKE_CASE`
- Markdown: `kebab-case.md`

### Content File Naming

| Type | Pattern | Example |
|------|---------|---------|
| Daily Note | `YYYY-MM-DD.md` | `2026-01-01.md` |
| Weekly Summary | `YYYY-WNN-weekly.md` | `2026-W01-weekly.md` |
| Monthly Report | `YYYY-MM-monthly.md` | `2026-01-monthly.md` |
| Study Note | `NN-chX-topic.md` | `01-ch1-prologue.md` |

### Imports

```typescript
// 1. React/Next imports
import { useState } from 'react'
import Link from 'next/link'

// 2. Third-party imports
import { clsx } from 'clsx'

// 3. Internal imports
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'
```

---

## Content Rules

### Bible References

- **Format**: `約 1:1` or `John 1:1`
- **Chinese Primary**: 和合本修訂版 (RCUV)
- **Chinese Reference**: 新譯本 (CNV), 呂振中譯本
- **English Primary**: ESV (English Standard Version)
- **English Reference**: NIV, NASB, NET Bible
- **Greek Reference**: NA28, UBS5

### Commentary Citations

- Must be verifiable
- Include author, work, page/section
- Format: `**[Author]**: "[Quote]" — [Source]`

### Writing Standards

| Type | Word Count | Key Sections |
|------|-----------|--------------|
| Daily Note | 300-500 | 經文、教導要點、洞見、應用 |
| Weekly Summary | 1000-2000 | 核心主題、金句、跨書關聯、下週計劃 |
| Monthly Report | 5000-7000 | 經文總結、神學要點、生命應用、展望 |

### Agent Behavior Rules

- **總編輯**: 客觀評估，1-5分制，不過度讚美
- **注疏師**: 必須核對原文，不可杜撰，標明出處
- **AI戰略家**: 只使用真實AI事件，不可虛構
- **校對神**: 高標準，保持作者語言風格，核對所有引文
- **出書總管**: 注重內容邏輯，質量優先於數量

### Forbidden

- Fabricated Scripture quotes (不杜撰經文)
- Unverifiable commentary (不編造注疏)
- Empty spiritual jargon (避免空洞套話)
- AI-generated filler content (避免AI腔調)
- Excessive emojis (避免過度使用emoji)

---

## Git Workflow

### Commit Format

```
<emoji> <type>: <description>

📝 docs: Update Gospel of John study notes
✨ feat: Add new daily note template
🐛 fix: Correct Scripture reference
🔧 config: Update Claude settings
📦 build: Upgrade Next.js to 15.1
```

### Branch Strategy

- `main` - Production ready
- `develop` - Development
- `feature/*` - New features
- `docs/*` - Documentation updates

---

## Environment Variables

```env
# .env.local (not committed)
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

---

## Key Files to Know

| File | Purpose |
|------|---------|
| `docs/BRD-gospel-of-john.md` | Business requirements, MVP definition |
| `docs/PRD-gospel-of-john.md` | Product requirements, daily rhythm |
| `.claude/settings.json` | AI behavior configuration |
| `.claude/CONTENT_RULES.md` | Content quality standards |
| `daily-notes/drafts/thursday-wong/` | Elder Wong's study materials |

---

## When Helping with This Project

1. **Always reference** the MVP focus (Gospel of John only)
2. **Use the three resources**: Elder Wong + gty.org + Campbell Morgan
3. **Follow content rules** in `.claude/CONTENT_RULES.md`
4. **Verify all Scripture** quotes against RCUV/ESV
5. **Never fabricate** commentary or historical facts
6. **Maintain bilingual** (繁體中文 + English) where appropriate

---

## Quality Checklist (Before Publish)

- [ ] 聖經引文是否準確？(RCUV/ESV)
- [ ] 中英對照是否完整？
- [ ] 注疏引用是否可查證？
- [ ] 邏輯是否連貫？
- [ ] 是否有屬靈洞見（而非常識）？
- [ ] 是否符合 MVP 焦點？
- [ ] 格式是否符合規範？

---

**Last Updated**: 2026-01-01
**Maintained By**: Jim Xiao
