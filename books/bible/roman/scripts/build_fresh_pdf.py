#!/usr/bin/env python3
"""One-off full xelatex/pandoc rebuild of the whole book, used to source the
freshly-rendered chapters 12-end for splicing onto the frozen baseline's
pages 1-228 (see merge_baseline_pdf.py). Mirrors the working pandoc
invocation pattern used by scripts/build-judges-consolidated.sh (--template=,
not --include-in-header=, which is what templates/pdf/romans.latex actually
needs to produce the full cover/TOC/chapter-styling, not just a preamble
injected into pandoc's default template).
"""
from pathlib import Path
import shutil
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_book import make_combined, load_manifest  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT.parents[2] / "templates" / "pdf" / "romans.latex"
OUTPUT_PDF = ROOT / "build" / "romans-fresh.pdf"
LOG = ROOT / "build" / "romans-fresh-build.log"


# Printed-page continuity with the frozen pages 1-228: page 228 there prints
# "208" (the baseline's own front-matter uses 20 physical pages before Arabic
# numbering starts), so chapter 12's first page in the spliced document must
# print "209". Injected as a raw LaTeX block right before the chapter 12
# heading so xelatex's own page counter carries the right number through the
# rest of the book, instead of patching ~117 footer numbers by hand after.
PAGE_RESET = '\n\n```{=latex}\n\\setcounter{page}{209}\n```\n\n'


def main() -> int:
    manifest = load_manifest()
    source = make_combined(manifest, "pdf")
    text = source.read_text(encoding="utf-8")
    marker = "# 羅馬書第 12 章 · "
    assert text.count(marker) == 1, f"expected exactly one chapter-12 heading, found {text.count(marker)}"
    text = text.replace(marker, PAGE_RESET.strip("\n") + "\n\n" + marker, 1)
    source.write_text(text, encoding="utf-8")
    pandoc = shutil.which("pandoc")
    xelatex = shutil.which("xelatex")
    if not pandoc or not xelatex:
        raise SystemExit("pandoc and xelatex are required")
    OUTPUT_PDF.parent.mkdir(exist_ok=True)
    command = [
        pandoc, str(source),
        "-o", str(OUTPUT_PDF),
        "--verbose",
        "--pdf-engine=xelatex",
        f"--template={TEMPLATE}",
        "--from=markdown+raw_html+raw_attribute",
        "--metadata-file=book.json",
        "--toc",
        "--toc-depth=2",
        "--top-level-division=chapter",
        "-V", "tocdepth=1",
    ]
    print("+", " ".join(command))
    with open(LOG, "w") as log:
        result = subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
    print(f"exit code: {result.returncode}; log: {LOG}")
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
