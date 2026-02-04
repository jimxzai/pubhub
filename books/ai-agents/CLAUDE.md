# AI Agents Book - Claude Code Project Configuration

## Book: The AI-Powered One-Person Company

**Author:** Jim Xiao
**Template:** O'Reilly Style (dev-book-template)
**Pages:** ~275
**Status:** Complete

---

## STANDARD WORKFLOW

### Directory Structure

```
/Users/jimxiao/Documents/GitHub/pubhub/books/ai-agents/
├── latex-template/
│   ├── Book/
│   │   ├── book.tex           # Main LaTeX file
│   │   ├── preamble.tex       # Styles, packages, keyinsight, codebox
│   │   └── chapters/          # ch01.tex - ch18.tex
│   ├── output/                # Build output directory
│   ├── images/                # Cover and images
│   ├── Makefile               # Build commands (uses pdflatex)
│   └── COMPILE.md             # Compilation instructions
├── ai-agents-oreilly-style.pdf   # FINAL OUTPUT
└── CLAUDE.md                  # This file
```

---

## PDF COMPILATION (CRITICAL)

### Compiler: tectonic

**tectonic** is installed at `/opt/homebrew/bin/tectonic`. Use this for LaTeX compilation.

### Compile Command

```bash
cd /Users/jimxiao/Documents/GitHub/pubhub/books/ai-agents/latex-template/Book
tectonic book.tex
```

### Copy to Final Location

```bash
cp /Users/jimxiao/Documents/GitHub/pubhub/books/ai-agents/latex-template/Book/book.pdf \
   /Users/jimxiao/Documents/GitHub/pubhub/books/ai-agents/ai-agents-oreilly-style.pdf
```

### Final Output Location

```
/Users/jimxiao/Documents/GitHub/pubhub/books/ai-agents/ai-agents-oreilly-style.pdf
```

---

## PDF Verification (Python fitz)

```python
import fitz
doc = fitz.open('/Users/jimxiao/Documents/GitHub/pubhub/books/ai-agents/ai-agents-oreilly-style.pdf')
print(f"Pages: {len(doc)}")
```

---

## Book Structure

| Part | Chapters | Title |
|------|----------|-------|
| 1 | 1-3 | The Paradigm Shift |
| 2 | 4-9 | Your AI Agent Team (Emma, Sam, Maya, Casey, Finn, Oscar) |
| 3 | 10-11 | The AI-Native Business |
| 4 | 12-14 | Technical Infrastructure |
| 5 | 15-16 | Advanced Playbooks |
| 6 | 17 | Case Studies (Illustrative Scenarios) |
| 7 | 18 | Your Transformation (90-Day Action Plan) |

---

## Key Fixes Applied

### White Text Bug (FIXED)
- **Root cause:** codebox (tcolorbox + lstlisting) corrupted text color state
- **Solution in preamble.tex:**
  - Added `coltext=black` and `after={\color{black}}` to codebox
  - Added `before={\color{black}}` to itemize/enumerate settings

### keyinsight Environment (ADDED)
- Added `\newtcolorbox{keyinsight}` in preamble.tex for McKinsey-style callouts

---

## Chapter Formatting (McKinsey-Style)

Chapters 17-18 use executive framework:
- Executive Summary at start
- `\begin{keyinsight}...\end{keyinsight}` callouts
- Strategic comparison tables
- "Illustrative Scenario" labeling (not "Case Study")
- `\section*{Sources \& References}` at end

---

**Last Updated:** 2026-02-01
