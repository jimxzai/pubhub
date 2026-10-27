# Pubhub System Skill

This is a customized, standalone AI coding agent skill specifically designed for the **Three Books Deep Reading & Publishing System** (三書精讀出版系統). 

It consolidates all the context, content rules, formatting guidelines, and multi-agent workflows (Master Editor, Annotator, AI Strategist, Proofreader, Publisher) from your `.claude/` directory into a single, standardized `SKILL.md` file.

## Why Extract This?

By adhering to the [agentskills.io](https://github.com/alirezarezvani/claude-skills) standard, you can now seamlessly load your "Pubhub" workflow into various AI agents including:
- **Antigravity**
- **Cursor**
- **Windsurf**
- **OpenAI Codex**
- **Claude Code**

## How to Use

If your AI agent supports the standard skill format (like Antigravity), simply instruct it to read this skill:
> "Please load and act according to the pubhub-system skill located in `pubhub-skill/SKILL.md`."

Once loaded, you can call upon the sub-agents natively:
- "Please act as the **Master Editor** and analyze my daily note draft."
- "Act as the **AI Strategist** and map Chapter 13 to the 2025 AI chip war."

## Directory Structure

```
pubhub-skill/
├── README.md       # This file
└── SKILL.md        # The unified, standardized skill definition
```
