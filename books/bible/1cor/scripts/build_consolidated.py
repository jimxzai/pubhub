#!/usr/bin/env python3
"""Build all formats with the reference edition's structure and appendices."""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
NAME = "1cor-consolidated"

def run(args, **kwargs):
    return subprocess.run(args, cwd=ROOT, check=True, **kwargs)

def source(name):
    return re.sub(r"\A---\n.*?\n---\n", "", (ROOT / name).read_text(),
                  count=1, flags=re.S).strip()

def assemble():
    chunks = []
    def add(name, numbered=False):
        text = source(name).replace("\\newpage", "")
        if not numbered:
            text = re.sub(r"^(# .+)$", r"\1 {.unnumbered}", text, count=1, flags=re.M)
        chunks.append(text)
    def part(title):
        chunks.append("# " + title + " {.unnumbered}")
    add("000-preface.md")
    part("卷首 · 定位 (Orientation)")
    for name in ["00-overview.md", "00a-1cor-position.md", "00b-cross-spine.md"]:
        add(name)
    text = source("elder-wong-systematic-study.md")
    text = re.sub(r"\\textcolor\{ScriptureGold\}\{\\textbf\{([^{}]*)\}\}", r"**\1**", text)
    text = text.replace(r"\begin{center}\textcolor{ScriptureGold}{\textbf{\large 主必要來！}}\end{center}", "**主必要來！**")
    text = re.sub(r"^(#+) ", r"#\1 ", text, flags=re.M)
    chunks.append("# 全書領受總綱——查經領受 (Systematic Reception) {.unnumbered}\n\n" + text)
    parts = [
        (1, 4, "卷一 · 紛爭與十字架的智慧 · 1-4 章"),
        (5, 7, "卷二 · 教會的紀律與身體的聖潔 · 5-7 章"),
        (8, 10, "卷三 · 自由、良心與榜樣 · 8-10 章"),
        (11, 14, "卷四 · 聚會的次序與恩賜 · 11-14 章"),
        (15, 16, "卷五 · 復活的盼望與收尾 · 15-16 章"),
    ]
    for start, end, title in parts:
        part(title)
        for n in range(start, end + 1):
            add(f"ch{n:02d}.md", True)
    part("卷末 · 直等到他來 (Until He Comes)")
    for name in ["99-until-he-comes.md", "99-appendix-references.md", "999-afterword.md"]:
        add(name)
    copyright_text = re.sub(r"^# .+\n", "", source("000-copyright.md"), count=1).strip()
    meta = {
        "title": "哥林多前書研讀",
        "subtitle": "1 Corinthians Deep Study — 十字架的道理，是神的大能",
        "author": "PubHub 三書精讀編輯部", "date": "2026年9月20日",
        "lang": "zh-Hant", "copyright": copyright_text, "toc-title": "目錄 Contents",
    }
    BUILD.mkdir(exist_ok=True)
    (BUILD / "metadata.json").write_text(json.dumps(meta, ensure_ascii=False))
    (BUILD / (NAME + ".md")).write_text("\n\n".join(chunks) + "\n")
    template = (ROOT / "templates/1cor.latex").read_text()
    appendix = template[template.index(r"\chapter*{Appendix A:"):template.index("%% END COVER PAGE")]
    appendix = re.sub(r"\\addcontentsline\{toc\}\{chapter\}\{[^\n]*\}", "", appendix)
    result = run(["pandoc", "-f", "latex", "-t", "markdown"], input=appendix, text=True, capture_output=True)
    (BUILD / "appendices.md").write_text(result.stdout)
    digital = "# 版權與使用說明 {.unnumbered}\n\n" + copyright_text + "\n\n" + "\n\n".join(chunks) + "\n\n" + result.stdout
    (BUILD / (NAME + "-digital.md")).write_text(digital)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("format", choices=["pdf", "html", "epub"])
    args = parser.parse_args()
    assemble()
    output = ROOT / "output" / args.format / (NAME + "." + args.format)
    output.parent.mkdir(parents=True, exist_ok=True)
    common = ["pandoc", "--standalone", "--toc", "--toc-depth=1",
              "--metadata-file=build/metadata.json"]
    if args.format == "pdf":
        tex = BUILD / (NAME + ".tex")
        run(common + [str(BUILD / (NAME + ".md")), "--template=templates/1cor.latex",
                      "--top-level-division=chapter", "-t", "latex", "-o", str(tex)])
        for attempt in range(5):
            toc = tex.with_suffix(".toc")
            before = toc.read_bytes() if toc.exists() else b""
            result = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error",
                                     "-output-directory=build", str(tex)], cwd=ROOT,
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            (BUILD / "xelatex-console.log").write_bytes(result.stdout)
            if result.returncode:
                raise SystemExit(result.stdout.decode(errors="replace")[-5000:])
            if attempt >= 1 and toc.exists() and toc.read_bytes() == before:
                break
        else:
            raise SystemExit("Table of contents did not converge after five passes")
        log = tex.with_suffix(".log").read_text(errors="replace")
        if "Missing character:" in log:
            raise SystemExit("Missing glyphs; inspect build/1cor-consolidated.log")
        if "Overfull" in log:
            raise SystemExit("Layout overflow; inspect build/1cor-consolidated.log")
        shutil.copy2(tex.with_suffix(".pdf"), output)
    else:
        cmd = common + [str(BUILD / (NAME + "-digital.md"))]
        if args.format == "html":
            cmd += ["--embed-resources", "--css=templates/book.css"]
        else:
            cmd += ["--epub-cover-image=assets/1cor-consolidated-cover.png", "--css=templates/book.css"]
        run(cmd + ["-o", str(output)])
    print(output)

if __name__ == "__main__":
    main()
