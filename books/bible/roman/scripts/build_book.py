#!/usr/bin/env python3
"""Build PDF, EPUB, and HTML outputs from the manifest-defined source order."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBHUB_ROOT = ROOT.parents[2]
BUILD = ROOT / "build"
DIST = ROOT / "dist"
CANONICAL_PDF = PUBHUB_ROOT / "output" / "romans-consolidated.pdf"


def load_manifest() -> dict:
    return json.loads((ROOT / "book.json").read_bytes().decode("utf-8"))


def body(path: Path) -> str:
    text = path.read_bytes().decode("utf-8")
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end >= 0:
            return text[end + len("\n---\n"):].strip()
    return text.strip()


def mark_unnumbered(text: str) -> str:
    """Add {.unnumbered} to the first top-level heading, merging into an
    existing attribute block ({#id} -> {#id .unnumbered}) instead of
    appending a second one, which pandoc would not parse as an attribute."""
    def repl(m: "re.Match[str]") -> str:
        title, attrs = m[1], m[2]
        if attrs is None:
            return f'{title} {{.unnumbered}}'
        inner = attrs.strip()[1:-1].strip()
        if '.unnumbered' in inner:
            return m[0]
        return f'{title} {{{inner} .unnumbered}}'
    return re.sub(r'^(# .+?)(\s*\{[^}]*\})?$', repl, text, count=1, flags=re.M)


def make_combined(manifest: dict, target: str) -> Path:
    BUILD.mkdir(exist_ok=True)
    separator = "\n\n"
    if target == "pdf":
        separator = "\n\n\\newpage\n\n"
    elif target in {"html", "epub"}:
        separator = "\n\n<div class=\"chapter-break\"></div>\n\n"
    pieces = [body(ROOT / name) for name in manifest["source_order"]]
    for index, name in enumerate(manifest['source_order']):
        chapter = re.match(r'^(0[1-9]|1[0-6])-', name)
        if chapter:
            number = int(chapter.group(1))
            pieces[index] = re.sub(r'^# (.+)$', rf'# 羅馬書第 {number} 章 · \1 {{#romans-{number}}}', pieces[index], count=1, flags=re.M)
            if target == 'pdf':
                pieces[index] = re.sub(r'^(# .+)$', lambda m: m[0] + '\n\n\\markboth{羅馬書第 ' + str(number) + ' 章 · Romans ' + str(number) + '}{}', pieces[index], count=1, flags=re.M)
        else:
            # Front/back matter must not consume \chapter numbers, or the
            # book's own chapter 1 prints as some later number (see eat-bible
            # gotchas.md, "Front matter and part-divider pages consume
            # chapter numbers").
            pieces[index] = mark_unnumbered(pieces[index])
        if name == '98-appendix-indices.md':
            # Link chapter destinations, preserving the curated index wording.
            pieces[index] = re.sub(r'第(1[0-6]|[1-9])章', lambda m: f'[第{m[1]}章](#romans-{m[1]})', pieces[index])
            pieces[index] = re.sub(r'\| (0[1-9]|1[0-6]) \|', lambda m: f'| [第{int(m[1])}章](#romans-{int(m[1])}) |', pieces[index])
    if target == "pdf":
        # Two part-divider pages exist in the original baseline PDF with no
        # corresponding source file (they predate the current 26-file manifest
        # -- see SOURCE-RECONCILIATION.md). Reproduced verbatim from the
        # baseline (sources/archive/romans-original-baseline.pdf pages 308
        # and 314) so a from-source rebuild doesn't silently drop them.
        dividers = {
            '99-to-spain.md': '# 卷末 · 望向那一頭 (Toward the Other End) {.unnumbered}\n\n'
                '> 羅馬書自己不收尾——它結在一張還沒走完的行程表上，指著士班雅，也指著新天新地。\n>\n'
                '> 我不以福音為恥；這福音本是神的大能，要救一切相信的。（羅1:16）\n',
            '98-appendix-indices.md': '# 附錄 (Appendices) {.unnumbered}\n\n'
                '> 經文與主題索引；資料來源與版本之逐章誠實說明。\n',
        }
        for name, divider in dividers.items():
            i = manifest['source_order'].index(name)
            pieces[i] = divider + '\n\\newpage\n\n' + pieces[i]
        # Keep the manuscript source renderer-neutral while giving XeLaTeX a
        # real superscript command. Raw HTML <sup> is ignored by Pandoc's PDF
        # writer, which would otherwise flatten verse numbers into the prose.
        pieces = [
            re.sub(r"<sup>(\d+)</sup>", r"\\textsuperscript{\1}", piece)
            for piece in pieces
        ]
        # No manual Greek-font wrapping here: templates/pdf/romans.latex
        # already auto-switches fonts for the GreekAndCoptic/GreekExtended
        # Unicode blocks via ucharclasses (\ucGreekRun). A prior version of
        # this function wrapped Greek runs in a bare `{\greekfallback ...}`
        # group targeting the old templates/roman-header.tex's font (a
        # command that doesn't exist in the real template) — and a bare
        # `{...}` typed into markdown prose gets its braces silently escaped
        # by pandoc's reader regardless (see eat-bible gotchas.md), so this
        # was doubly broken as soon as the real template was ever exercised.
        # The afterword is intentionally a single closing unit. Give its
        # opening page a small amount of extra vertical room so a short
        # closing blessing cannot become an orphan on a new final page.
        if "999-afterword.md" in manifest["source_order"]:
            afterword_index = manifest["source_order"].index("999-afterword.md")
            pieces[afterword_index] = "\\small\\enlargethispage{7\\baselineskip}\n" + pieces[afterword_index]
    output = BUILD / f"roman-{target}.md"
    output.write_text(separator.join(pieces) + "\n", encoding="utf-8")
    return output


def run(command: list[str]) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def build(target: str, manifest: dict) -> None:
    if target == 'pdf':
        from merge_baseline_pdf import main as merge_baseline
        merge_baseline()
        return
    pandoc = shutil.which("pandoc")
    if not pandoc:
        raise SystemExit("pandoc is required; install it before building")
    DIST.mkdir(exist_ok=True)
    source = make_combined(manifest, target)
    common = [
        pandoc,
        str(source),
        "--from=markdown+raw_html",
        "--metadata-file=book.json",
        "--standalone",
        "--toc",
        "--toc-depth=2",
        "-V",
        "documentclass=book",
        "-V",
        "classoption=oneside",
        "-V",
        "classoption=openany",
        "-V",
        "toc-title=目錄 Contents",
        "-V",
        "mainfont=Times New Roman",
        "-V",
        "CJKmainfont=STSong",
    ]
    if target == "pdf":
        xelatex = shutil.which("xelatex")
        if not xelatex:
            raise SystemExit("xelatex is required for the PDF build")
        CANONICAL_PDF.parent.mkdir(exist_ok=True)
        command = common + [
            "--pdf-engine=xelatex",
            "--include-in-header=templates/roman-header.tex",
            f"--output={CANONICAL_PDF}",
        ]
    elif target == "epub":
        command = common + [
            "--to=epub3",
            "--css=templates/roman.css",
            "--output=dist/romans-consolidated.epub",
        ]
    else:
        command = common + [
            "--standalone",
            "--to=html5",
            "--css=templates/roman.css",
            "--output=dist/romans-consolidated.html",
        ]
    run(command)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", choices=["pdf", "epub", "html", "all"])
    args = parser.parse_args()
    manifest = load_manifest()
    targets = ["pdf", "epub", "html"] if args.target == "all" else [args.target]
    for target in targets:
        build(target, manifest)
    print("Build complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
