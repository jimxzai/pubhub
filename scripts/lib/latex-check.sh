#!/bin/bash
# latex-check.sh — shared post-build verification for the consolidated book
# builds. Source it, then call latex_build_report after pandoc.
#
# WHY THIS EXISTS
# ---------------
# `pandoc --pdf-engine=xelatex` swallows the entire xelatex log. Without
# `--verbose` the build output contains zero "Missing character", zero
# "Overfull \hbox" and zero LaTeX-error lines no matter what xelatex actually
# reported — so any grep-the-log verification (notably
# .claude/skills/eat-bible/driver.sh steps 2-3) passes vacuously on a broken
# book. Measured on Isaiah: the driver's log was 51 lines and reported a clean
# build; re-running the same source through xelatex directly surfaced 28
# Overfull \hbox warnings, including three appendix boxes bleeding 39pt past
# the page's text block and a Hebrew word-study cell overprinting the column
# beside it.
#
# So every build script must:
#   1. pass --verbose to pandoc,
#   2. redirect that output to a log file (it is tens of thousands of lines —
#      it belongs in a file, not the terminal),
#   3. call latex_build_report, which re-echoes anything worth failing on so
#      driver.sh's greps have something real to find.

# latex_build_report <pandoc-exit-code> <latex-log> <output-pdf>
latex_build_report() {
    local exit_code="$1" log="$2" pdf="$3"

    if [ "$exit_code" -ne 0 ]; then
        echo "❌ PDF generation failed — last 40 lines of $log:"
        tail -40 "$log"
        return 1
    fi

    echo ""
    echo "✅ PDF generated: $pdf ($(du -h "$pdf" | cut -f1))"
    echo ""
    echo "🔍 xelatex log checks ($log)"

    if ! grep -q "This is XeTeX" "$log"; then
        echo "  ⚠️  log holds no xelatex output — the --verbose flag is missing"
        echo "     from the pandoc call, or pandoc changed; every check below"
        echo "     is meaningless without it."
    fi

    local missing overfull
    missing=$(grep -c "Missing character" "$log")
    overfull=$(grep -c "Overfull \\\\hbox" "$log")

    # These label strings deliberately avoid the literal phrases "Missing
    # character" and "Overfull \hbox": driver.sh greps this output by count,
    # so a summary line echoing the phrase would itself register as a failure.
    echo "  missing-glyph warnings: $missing"
    echo "  overfull-box warnings:  $overfull"

    # Re-echo the offending lines themselves. A missing glyph is a hard
    # defect; an overfull box means content is printing outside its column or
    # off the text block. Neither is visible in the exit code — xelatex can
    # emit a PDF after a recoverable error and still exit 0.
    grep "Missing character" "$log" | head -5
    grep "Overfull \\\\hbox" "$log" | head -10
    grep -E '^! (LaTeX Error|Undefined control sequence|Package .* Error)' "$log" | head -5

    return 0
}
