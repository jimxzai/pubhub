#!/usr/bin/env python3
"""Check that every multi-word Hebrew run in the built book is printed in READING order.

Why: XeTeX reverses the letters inside each space-separated Hebrew word but not the order of the words, so a phrase
typeset as a plain Hebrew font run prints with its words left to right (the Shema as "ישראל שמע"). The fix is TeXXeT's
\\beginR…\\endR. This check is how we know it worked: for correct right-to-left output, `pdftotext` returns the
Hebrew in reading order; for the wrong output it returns the words reversed.

For every `{\\hebrewfont … }` run of two or more words in output/biblehebrew-consolidated.md, take its consonants,
and require them to occur, in that order, in the PDF's text (spaces, vowels, cantillation, maqqef and the letter alef ignored: see skeleton()).
Also checks the cover. Exit 1 if any run fails.      Usage: verify-rtl-order.py [-v]
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "output/biblehebrew-consolidated.md")
PDF = os.path.join(ROOT, "output/biblehebrew-consolidated.pdf")


def skeleton(s):
    """Consonants only, and WITHOUT alef (א): pdftotext often drops or relocates the alef glyph of a word, which would
    fail a correct page. Every other letter still has to appear in reading order, so a reversed phrase still fails."""
    return re.sub(r"[^\u05D1-\u05EA]", "", s)


def main():
    text = subprocess.run(["pdftotext", PDF, "-"], capture_output=True, text=True).stdout
    flat = skeleton(text)
    md = open(MD, encoding="utf-8").read()
    runs = re.findall(r"`\\leavevmode\\allowbreak\{\\hebrewfont (.*?)\}\\allowbreak`\{=latex\}", md)
    multi = [re.sub(r"\\(?:beginR|endR) ?", "", r).strip() for r in runs]
    multi = [r for r in multi if " " in r]
    bad = [r for r in multi if skeleton(r) not in flat]
    # the cover is typeset in the template, not in the markdown
    cover = skeleton(subprocess.run(["pdftotext", "-f", "1", "-l", "1", PDF, "-"], capture_output=True, text=True).stdout)
    shema = skeleton("שְׁמַע יִשְׂרָאֵל יְהוָה אֱלֹהֵינוּ יְהוָה אֶחָד")
    cover_ok = shema in cover
    print(f"{len(multi)} multi-word Hebrew runs; {len(multi) - len(bad)} in reading order, {len(bad)} not; "
          f"cover Shema in reading order: {cover_ok}")
    if "-v" in sys.argv or bad:
        for r in bad[:15]: print("  NOT IN READING ORDER:", re.sub(r"[֑-ׇ]", "", r))
    sys.exit(0 if (not bad and cover_ok) else 1)


if __name__ == "__main__":
    main()
