#!/bin/bash
# hebrew-build.sh — the shared build pipeline for the two Biblehebrew books. Source it, then call:
#   hebrew_build <slug> <input-dir-name> <template-name> <combine-script> <generator-script>
# Steps: mine the series' 原文研讀 tables -> generate the data-driven parts -> combine the chapters ->
# widen pipe-table separators (a short separator row compiles to unwrappable `l` columns; see eat-bible gotchas) ->
# pandoc/xelatex with --verbose into a log -> latex_build_report (fails on missing glyphs / LaTeX errors).

hebrew_build() {
    local slug="$1" indir="$2" tpl="$3" combine="$4" gen="$5"
    local here root input out md pdf template log
    here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"          # scripts/
    root="$(dirname "$here")"
    input="$root/books/bible/$indir"; out="$root/output"
    md="$out/$slug-consolidated.md"; pdf="$out/$slug-consolidated.pdf"; template="$root/templates/pdf/$tpl.latex"
    [ -f "$template" ] || { echo "ERROR: Template not found: $template"; return 1; }
    mkdir -p "$out"
    python3 "$here/mine-hebrew-wordstudies.py" >/dev/null || { echo "❌ series mining failed"; return 1; }
    python3 "$here/$gen" >/dev/null || { echo "❌ data generation failed"; return 1; }
    python3 "$here/$combine" "$input" "$md" || { echo "❌ combine failed"; return 1; }
    python3 "$here/widen-table-separators.py" "$md" >/dev/null 2>&1 || true
    source "$here/lib/latex-check.sh"
    log="${pdf%.pdf}-build.log"
    pandoc "$md" -o "$pdf" --verbose --pdf-engine=xelatex --template="$template" \
        --from=markdown-superscript-subscript --top-level-division=chapter > "$log" 2>&1
    latex_build_report "$?" "$log" "$pdf"
}
