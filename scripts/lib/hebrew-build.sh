#!/bin/bash
# hebrew-build.sh — the build pipeline for 《讀懂聖經的希伯來文》 (Part 1 guide + Part 2 per-book Hebrew). Source it, then:
#   hebrew_build
# Steps: mine the OT books' 原文研讀 tables -> generate Part 1's data (gen-biblehebrew-data.py) -> generate Part 2's data
# (gen-hebrew-compendium.py) -> recount the quoted 〈數一數〉 tables against OSHB -> combine the chapters ->
# widen pipe-table separators (a short separator row compiles to unwrappable `l` columns; see eat-bible gotchas) ->
# pandoc/xelatex with --verbose into a log -> latex_build_report (fails on missing glyphs / LaTeX errors).

hebrew_build() {
    local here root input out md pdf template log
    here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"          # scripts/
    root="$(dirname "$here")"
    input="$root/books/bible/Biblehebrew"; out="$root/output"
    md="$out/biblehebrew-consolidated.md"; pdf="$out/biblehebrew-consolidated.pdf"; template="$root/templates/pdf/biblehebrew.latex"
    [ -f "$template" ] || { echo "ERROR: Template not found: $template"; return 1; }
    mkdir -p "$out"
    python3 "$here/mine-hebrew-wordstudies.py" >/dev/null || { echo "❌ series mining failed"; return 1; }
    python3 "$here/gen-biblehebrew-data.py" >/dev/null || { echo "❌ Part 1 data generation failed"; return 1; }
    python3 "$here/gen-hebrew-compendium.py" >/dev/null || { echo "❌ Part 2 data generation failed"; return 1; }
    python3 "$here/verify-count-sections.py" >/dev/null || { echo "❌ section-count verification failed"; return 1; }
    python3 "$here/combine-biblehebrew.py" "$input" "$md" || { echo "❌ combine failed"; return 1; }
    python3 "$here/widen-table-separators.py" "$md" >/dev/null 2>&1 || true
    source "$here/lib/latex-check.sh"
    log="${pdf%.pdf}-build.log"
    pandoc "$md" -o "$pdf" --verbose --pdf-engine=xelatex --template="$template" \
        --from=markdown-superscript-subscript --top-level-division=chapter > "$log" 2>&1
    latex_build_report "$?" "$log" "$pdf" || return 1
    # Hebrew phrases must read right to left WORD by word (TeXXeT); a plain Hebrew run prints the words reversed
    python3 "$here/verify-rtl-order.py" || { echo "❌ Hebrew word order check failed"; return 1; }
}
