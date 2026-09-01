#!/usr/bin/env python3
"""Static check for markdown-source markup defects that build clean but print wrong.

WHY THIS EXISTS
---------------
2026-08-31, Gospel of Luke: the PDF passed lint-templates, the driver, and the
baseline (0 missing glyphs, 0 overfull) while printing literal asterisks in
red-letter text — 18 spans across 7 chapters had been written as
`\\jesus{...**必須**...}`. `\\jesus{}` is a raw LaTeX inline, so pandoc passes
its argument through untouched and markdown emphasis inside it never becomes
`\\textbf`. Nothing in the pipeline warns: xelatex happily typesets "*".
The same book also carried the same H2 title twice per chapter (`## 配詩` ×2)
and, after a restructure, five callout boxes pointing readers to a section
that no longer existed. All three are source-level facts a one-second scan
can see; none are visible to the template lint (which reads .latex files) or
to the build log.

CHECKS
------
  markdown-inside-raw-macro   `**x**` / `*x*` inside \\jesus{...}  → use \\textbf{} / \\textit{}
  duplicate-h2                the same `## ` title appears twice in one file
  dangling-section-ref        「見…「X」一節/二節/小節」 where no heading in the
                              file contains X  (review — may be a cross-chapter ref)
  ascii-comma-in-cjk          half-width `,` directly between two CJK characters (style)

Usage:  python3 scripts/lint-chapter-markup.py [path ...]     # default books/bible
        exit 1 if any error-severity finding
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT = ROOT / "books" / "bible"

# \jesus{ ... } with at most one level of nested \textbf{}/\textit{} braces
JESUS = re.compile(r"\\jesus\{((?:[^{}]|\\text(?:bf|it|superscript)\{[^{}]*\})*)\}")
MD_EMPH = re.compile(r"\*\*[^*]+\*\*|(?<![*\w])\*[^*\s][^*]*\*(?![*\w])")
H2 = re.compile(r"^##\s+(.+?)\s*$")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$")
SECT_REF = re.compile(r"見[^「」\n]{0,12}「([^「」]{2,24})」(?:與「([^「」]{2,24})」)?[一二三兩]?(?:小)?節")
CJK = "\u4e00-\u9fff\u3400-\u4dbf"
ASCII_COMMA = re.compile(rf"[{CJK}],[{CJK}]")

SEVERITY = {
    "markdown-inside-raw-macro": "error",
    "duplicate-h2": "review",
    "dangling-section-ref": "review",
    "ascii-comma-in-cjk": "style",
}


def check(path):
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    lines = text.splitlines()
    out = []  # (lineno, kind, context)

    for m in JESUS.finditer(text):
        inner = m.group(1)
        e = MD_EMPH.search(inner)
        if e:
            lineno = text.count("\n", 0, m.start()) + 1
            out.append((lineno, "markdown-inside-raw-macro", e.group(0)[:40]))

    seen = {}
    for i, ln in enumerate(lines, 1):
        h = H2.match(ln)
        if h:
            key = re.sub(r"\s*\(.*\)\s*$", "", h.group(1))  # strip "(English)" tail
            if key in seen:
                out.append((i, "duplicate-h2", f"{key} (first at line {seen[key]})"))
            else:
                seen[key] = i

    headings = " | ".join(m.group(1) for ln in lines if (m := HEADING.match(ln)))
    for i, ln in enumerate(lines, 1):
        for m in SECT_REF.finditer(ln):
            for name in (m.group(1), m.group(2)):
                if name and name not in headings:
                    out.append((i, "dangling-section-ref", f"「{name}」"))

    for i, ln in enumerate(lines, 1):
        if ln.lstrip().startswith("|") or ln.lstrip().startswith(">"):
            # tables and scripture/quote blocks are where this lands; prose too
            pass
        m = ASCII_COMMA.search(ln)
        if m:
            out.append((i, "ascii-comma-in-cjk", ln[max(0, m.start() - 6): m.end() + 6].strip()))
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    targets = [Path(a) for a in args] or [DEFAULT]
    files = []
    for t in targets:
        files.extend(sorted(t.rglob("*.md")) if t.is_dir() else [t])

    by_kind = {}
    for f in files:
        for lineno, kind, ctx in check(f):
            by_kind.setdefault(kind, []).append((f, lineno, ctx))

    errors = 0
    for kind in SEVERITY:
        hits = by_kind.get(kind, [])
        if not hits:
            continue
        sev = SEVERITY[kind]
        errors += len(hits) if sev == "error" else 0
        print(f"== {kind} [{sev}] — {len(hits)} ==")
        for f, lineno, ctx in hits[:200]:
            try:
                rel = f.relative_to(ROOT)
            except ValueError:
                rel = f
            print(f"  {rel}:{lineno}  {ctx}")
        if len(hits) > 200:
            print(f"  … {len(hits) - 200} more")
    if not by_kind:
        print(f"clean: {len(files)} files, no markup defects found")
    else:
        print(f"scanned {len(files)} files; errors={errors}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
