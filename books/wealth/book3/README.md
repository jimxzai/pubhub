# Book 3: Jim's Investment Memo / 阿甘的投资备忘录

> 25 Years of Silicon Valley Survival Wisdom · Simple & Practical
> 25年硅谷生存智慧 · 简单实用版

---

## 📖 Overview

This is the companion handbook to *Silicon Jim* (硅谷阿甘). If the main book is a movie, this is the **movie guide** — distilling 25 years of Jim's story into **simple rules** you can use right away.

**No theory, just action. No "why", just "how".**

---

## 📁 Structure

```
book3/
├── README.md           # This file
├── build.sh            # Build script for PDF generation
├── zh/                 # Chinese version (简体中文)
│   ├── 00-index.md     # Table of contents
│   ├── 00-wisdom.md    # Three Mentors prologue
│   ├── 01-31 *.md      # 31 chapters
│   └── appendix-*.md   # 4 appendices
├── en/                 # English version
│   ├── 00-index.md     # Table of contents
│   ├── 00-wisdom.md    # Three Mentors prologue
│   ├── 01-31 *.md      # 31 chapters
│   └── appendix-*.md   # 4 appendices
└── output/             # Generated PDFs (after build)
```

---

## 📚 Book Structure

### Prologue
- **Three Mentors**: Sun Tzu (孙子) + Benjamin Graham + Bible (圣经)

### Part 1: Fundamentals (基本功)
1. Never Go All-In on One Basket
2. Save Six Months First (Emergency Fund)
3. Don't Invest in What You Don't Understand

### Part 2: How to Buy (怎么买)
4. Be Greedy When Others Are Fearful
5. When in Doubt, Buy Index Funds
6. Dollar Cost Average, Don't Time

### Part 3: How to Sell (怎么卖)
7. Holding Is the Hardest Part
8. When to Walk Away
9. Don't Chase

### Part 4: Pitfall Guide (避坑指南)
10. The Sock Puppet Lesson (2000 Dot-com)
11. Enron-Style Innovation (2001)
12. Too Big to Fail Can Still Fail (2008 Lehman)
13. Memes Are Not Investments (2021 GME/Crypto)
14. Effective Altruism or Effective Embezzlement (2022 FTX)

### Part 5: Career Survival (职场生存)
15. Don't Mix Human Capital with Financial Capital
16. Always Have a Plan B
17. The Best Revenge Is Living Well

### Part 6: Children's Education (子女教育)
18. 529 Plans: Tax Weapon
19. Public or Private
20. Ivy League Isn't the Only Path
21. Financial Literacy Starts Young

### Part 7: Life Wisdom (人生智慧)
22. Compound Interest Needs Time
23. Real Wealth Is Time
24. Listen to Mama

### Part 8: Retirement Planning (退休规划)
25. Retirement Is Not the End, It's a Turning Point

### Part 9: Silicon Valley Life (硅谷生活)
26. Healthcare Is Hidden Wealth (HSA/ACA/Medicare)
27. Silicon Valley Chinese Churches
28. The Real Cost of Raising Kids
29. The Extracurricular Arms Race
30. Silicon Valley Asian Anxiety
31. Church and Community

### Appendices (附录)
- A: Investment Decision Checklist
- B: Jim's 10 Iron Rules
- C: Complete Mama Quotes
- D: Complete Sarah Quotes

---

## 🔨 Building PDFs

### Prerequisites
- Node.js 18+
- Pandoc (`brew install pandoc`)
- XeLaTeX (`brew install --cask mactex`)

### Build Commands

```bash
# Build both Chinese and English PDFs
./build.sh all

# Build Chinese version only
./build.sh zh

# Build English version only
./build.sh en
```

### Or using the main build script:

```bash
# Chinese
node scripts/build-pdf.js --format advisory-zh --input books/wealth/book3/zh

# English
node scripts/build-pdf.js --format advisory-en --input books/wealth/book3/en
```

---

## ✏️ Writing Style

### Chapter Format

Each chapter follows this structure:

```markdown
# Chapter N: Title

> **Mama said: "Opening quote from a mentor"**

---

## Story
[A real-life story or scenario]

## Rules
[Practical rules to follow]

## How to Do It
[Step-by-step instructions]

## Checklist
- [ ] Action item 1
- [ ] Action item 2

---

## Three Mentors Say

| Mentor | Wisdom |
|--------|--------|
| **Sun Tzu** | [Quote or principle] |
| **Graham** | [Quote or principle] |
| **Bible** | [Quote with reference] |

---

**Previous Chapter**: [Link]
**Next Chapter**: [Link]
```

### Tone
- Conversational, not academic
- Story-driven with practical takeaways
- "Mama said" quotes add warmth and wisdom
- Three Mentors provide cross-cultural depth

---

## 📝 Version History

- **v0.1** (2025-12-30): Initial complete draft with 31 chapters + 4 appendices

---

## 👤 Author

**Jim Xiao**

A Silicon Valley engineer who learned investing the hard way — through 25 years of mistakes, market crashes, and Mama's wisdom.
