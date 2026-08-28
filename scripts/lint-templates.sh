#!/bin/bash
# lint-templates.sh — static check for the four template-level bugs documented
# in .claude/skills/eat-bible/SKILL.md. No build required; runs in about a
# second across every templates/pdf/*.latex.
#
# WHY THIS EXISTS
# ---------------
# SKILL.md documented the BoldFont glyph-fallback bug and told the reader to
# "check every other templates/pdf/*.latex file for this exact BoldFont=
# pattern". Months later 56 of 57 templates still carried it, including 14 of
# the 17 buildable books. An instruction to go grep is a task nobody performs.
# Every bug this script checks for is silent at build time: exit code 0, no
# glyph warning, no LaTeX error.
#
# Usage:
#   scripts/lint-templates.sh              # all templates
#   scripts/lint-templates.sh isaiah acts  # only these (by template basename)
#
# Exits 1 if any finding is reported, 0 if clean.

set -uo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

TEMPLATES_ARG="$*" python3 <<'PYEOF'
import glob, os, re, subprocess, sys

TARGETS = os.environ.get("TEMPLATES_ARG", "").split()

PT_PER = {"pt": 1.0, "in": 72.27, "cm": 28.4528, "mm": 2.84528, "bp": 1.00375}


def to_pt(value, unit):
    return float(value) * PT_PER[unit]


def strip_comments(text):
    """Blank out full-line LaTeX comments, keeping the line count intact so
    reported line numbers still match the file. SKILL.md's own explanatory
    comments quote the buggy patterns verbatim, so linting them would produce
    false positives."""
    return "\n".join("" if l.lstrip().startswith("%") else l
                     for l in text.split("\n"))


def text_width_pt(src):
    """Recover \\textwidth from the template's \\geometry{...} block."""
    m = re.search(r"\\geometry\{(.*?)\}", src, re.S)
    if not m:
        return None
    body = m.group(1)
    keys = dict(
        (k, to_pt(v, u))
        for k, v, u in re.findall(r"(\w+)\s*=\s*([\d.]+)(pt|in|cm|mm|bp)", body)
    )
    paper = keys.get("paperwidth")
    if paper is None:
        return None
    if "inner" in keys and "outer" in keys:
        return paper - keys["inner"] - keys["outer"]
    if "left" in keys and "right" in keys:
        return paper - keys["left"] - keys["right"]
    if "margin" in keys:
        return paper - 2 * keys["margin"]
    return None



def load_ucharclasses():
    """Read the real block and class-group names out of the installed
    ucharclasses.sty rather than hardcoding a list that will drift."""
    try:
        path = subprocess.run(["kpsewhich", "ucharclasses.sty"],
                              capture_output=True, text=True).stdout.strip()
        if not path:
            return None, set()
        txt = open(path, encoding="utf-8", errors="replace").read()
        blocks = set(re.findall(r"\\do\{([A-Za-z]+)\}\{\"", txt))
        groups = set(re.findall(r"\\doclass\{([A-Za-z]+)\}", txt))
        return (blocks or None), groups
    except Exception:
        return None, set()


UC_BLOCKS, UC_GROUPS = load_ucharclasses()

findings = []


def report(path, src, pos, kind, detail, fix):
    line = src.count("\n", 0, pos) + 1
    findings.append((f"{os.path.basename(path)}:{line}", kind, detail, fix))


for path in sorted(glob.glob("templates/pdf/*.latex")):
    name = os.path.basename(path).replace(".latex", "")
    if TARGETS and name not in TARGETS:
        continue

    raw = open(path, encoding="utf-8").read()
    src = strip_comments(raw)
    tw = text_width_pt(src)

    # 1. BoldFont pointing at a separate real bold face. For a CJK family this
    #    silently flattens \textbf{} wherever the bold span contains full-width
    #    punctuation (：。), because the bold face lacks those glyphs. Zero
    #    warnings, exit code 0.
    for m in re.finditer(r"BoldFont\s*=\s*([^,\]\n]*\bBold)\b", src):
        report(path, src, m.start(), "real-bold-face", f"BoldFont={m.group(1).strip()}",
               "point BoldFont at the same regular family with "
               "BoldFeatures={FakeBold=N}")

    # 2. Menlo (or any Latin-only face) as \setmonofont: every CJK character in
    #    a code block renders as a blank box.
    for m in re.finditer(r"\\setmonofont\{(Menlo|Courier[^}]*|Monaco)\}", src):
        report(path, src, m.start(), "cjk-blind-monofont", f"\\setmonofont{{{m.group(1)}}}",
               "use Songti SC or PingFang SC — Menlo has zero CJK glyphs")

    # 3. A fixed-dimension minipage that, once wrapped in \fcolorbox's rule and
    #    padding, is wider than the text block — it prints into the margin.
    #    Narrow centred boxes are deliberate, so only flag ones that actually
    #    overflow.
    if tw:
        box_overhead = 2 * 3.0 + 2 * 0.4  # \fboxsep + \fboxrule, LaTeX defaults
        for m in re.finditer(r"\\begin\{minipage\}\{([\d.]+)(pt|in|cm|mm|bp)\}", src):
            w = to_pt(m.group(1), m.group(2))
            if w + box_overhead > tw:
                report(path, src, m.start(),
                       "minipage-overflows-textblock",
                       f"minipage {{{m.group(1)}{m.group(2)}}} = {w:.1f}pt, "
                       f"+{box_overhead:.1f}pt box > textwidth {tw:.1f}pt",
                       r"use \dimexpr\textwidth-2\fboxsep-2\fboxrule\relax")

    # 5. ucharclasses misuse. Two distinct silent failures:
    #    (a) \setTransitionsFor{X} where X is a class GROUP or not a block at
    #        all -> compiles fine, does absolutely nothing.
    #    (b) \setTransitionsFor sets BOTH directions for every pair, so with
    #        two or more of them a later out-code overwrites an earlier
    #        in-code. \setTransitionTo sets only the entering direction.
    if UC_BLOCKS is not None:
        setfor = list(re.finditer(r"\\setTransitionsFor\{([A-Za-z]+)\}", src))
        for m in setfor:
            name = m.group(1)
            if name not in UC_BLOCKS:
                hint = ("is a class GROUP — the 2-arg form is "
                        f"\\setTransitionsFor{name}{{in}}{{out}}"
                        if name in UC_GROUPS else "is not a ucharclasses block")
                report(path, src, m.start(), "ucharclasses-dead-transition",
                       f"\\setTransitionsFor{{{name}}} — {hint}",
                       "use the real block name, or the 2-arg group form; as "
                       "written this line does nothing")
        if len(setfor) > 1:
            report(path, src, setfor[0].start(),
                   "ucharclasses-two-way-clobber",
                   f"{len(setfor)} \\setTransitionsFor calls — each sets BOTH "
                   "directions, so a later out-code overwrites an earlier "
                   "in-code",
                   r"migrate to \setTransitionTo (entering direction only), but "
                   "ONLY together with a census of every block the book uses — "
                   "it removes the leaving-code, so any block without an "
                   "explicit destination inherits the previous font")

    # 4. Fixed-width table column specs that exceed the text block. LaTeX puts
    #    \tabcolsep on both sides of every column; @{} strips only the outer
    #    two, leaving 2*\tabcolsep between each adjacent pair.
    if tw:
        for m in re.finditer(
            r"\\begin\{(longtable|tabular)\}(?:\[[^\]]*\])?\{@\{\}((?:p\{[\d.]+(?:pt|in|cm|mm|bp)\})+)@\{\}\}",
            src,
        ):
            cols = re.findall(r"p\{([\d.]+)(pt|in|cm|mm|bp)\}", m.group(2))
            total = sum(to_pt(v, u) for v, u in cols)
            gaps = 2 * 6.0 * (len(cols) - 1)  # \tabcolsep default 6pt
            if total + gaps > tw:
                report(path, src, m.start(),
                       "table-wider-than-textblock",
                       f"{len(cols)} cols = {total:.1f}pt + {gaps:.1f}pt gaps "
                       f"> textwidth {tw:.1f}pt (over by "
                       f"{total + gaps - tw:.1f}pt)",
                       "shrink the p{} widths: sum(p{}) + "
                       "2*tabcolsep*(ncol-1) must fit textwidth")

if not findings:
    print("clean: no template-level defects found")
    sys.exit(0)

by_kind = {}
for f in findings:
    by_kind.setdefault(f[1], []).append(f)

for kind in sorted(by_kind, key=lambda k: -len(by_kind[k])):
    rows = by_kind[kind]
    files = set(r[0].rsplit(":", 1)[0] for r in rows)
    print(f"\n{kind}  ({len(rows)} in {len(files)} template(s))")
    print(f"  fix: {rows[0][3]}")
    for loc, _, detail, _ in rows:
        print(f"    {loc:<40} {detail}")

print(f"\n{len(findings)} finding(s). See .claude/skills/eat-bible/SKILL.md "
      f"Gotchas for why each one is silent at build time.")
sys.exit(1)
PYEOF
