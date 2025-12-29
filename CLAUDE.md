# CLAUDE.md - Project Instructions for Claude Code

## Project Overview

**Project Name**: 三書精讀出版系統 (Three Books Deep Reading & Publishing System)
**Primary Focus (MVP)**: 約翰福音研讀 (Gospel of John Study)
**Timeline**: 7-year plan (2025-2032)
**Tech Stack**: Next.js 16.1 + Turbopack + pnpm + Claude AI

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
├── package.json                 # pnpm + Next.js 15.1
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
- **English Primary**: ESV
- **Greek Reference**: NA28, UBS5

### Commentary Citations

- Must be verifiable
- Include author, work, page/section
- Format: `**[Author]**: "[Quote]" — [Source]`

### Forbidden

- Fabricated Scripture quotes
- Unverifiable commentary
- Empty spiritual jargon
- AI-generated filler content

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

**Last Updated**: 2025-12-28
**Maintained By**: Jim Xiao
