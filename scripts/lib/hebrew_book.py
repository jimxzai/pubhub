"""Shared helpers for the Biblehebrew combine scripts (combine-biblehebrew.py, combine-hebrew-compendium.py).

Kept in one place so a fix (such as the \\leavevmode note below) cannot be applied to only one of the two books.
"""
import re
import sys

HEB_C = "[֑-״͏יִ-ﭏ]"
GRK_C = "[Ͱ-Ͽἀ-῿]"
_heb_run = re.compile(rf"{HEB_C}+(?:[ ]+{HEB_C}+)*")
_grk_run = re.compile(rf"{GRK_C}[{GRK_C[1:-1]}’'ʼ]*(?:[ ]+{GRK_C}[{GRK_C[1:-1]}’'ʼ]*)*")
_code_span = re.compile(r"`([^`\n]+)`")
_has_script = re.compile(f"{HEB_C}|{GRK_C}")


def strip_header(path, text):
    """Remove the leading YAML front matter block, whatever its length; refuse a file without one."""
    m = re.match(r"---\n.*?\n---\n", text, re.S)
    if not m:
        sys.exit(f"{path}: no YAML header (expected a leading --- ... --- block)")
    return text[m.end():]


def fill_stats(text, stats):
    """Replace {{key}} with stats[key] (ints >= 1000 get thousands separators); unknown keys are fatal."""
    def num(m):
        k = m.group(1)
        if k not in stats:
            sys.exit(f"unknown placeholder {{{{{k}}}}}")
        v = stats[k]
        return f"{v:,}" if isinstance(v, int) and v >= 1000 else str(v)
    out = re.sub(r"\{\{([A-Za-z0-9_]+)\}\}", num, text)
    if "{{" in out:                      # a malformed placeholder (space, hyphen...) would otherwise print literally
        sys.exit("malformed placeholder left in text: " + re.search(r".{0,20}\{\{.{0,30}", out).group(0))
    return out


def wrap_scripts(text, greek=True):
    """Wrap every Hebrew run (and, optionally, Greek run) in an explicit font group.

    * Code spans are paired left to right by a single scan, then unwrapped only if THEIR OWN content holds Hebrew or
      Greek. (A regex that looks for 'a backtick, script text, a backtick' can pair the closing backtick of one span
      with the opening backtick of the next.)
    * The leading \\leavevmode matters. A table cell that STARTS with \\allowbreak begins with a penalty in vertical
      mode, which moves the cell's reference baseline and prints the Hebrew a full line below its row.
    * No \\beginR..\\endR: XeTeX already reorders a single Hebrew font run, so it would reverse it twice.
    """
    text = _code_span.sub(lambda m: m.group(1) if _has_script.search(m.group(1)) else m.group(0), text)
    text = _heb_run.sub(lambda m: "`\\leavevmode\\allowbreak{\\hebrewfont " + m.group(0) + "}\\allowbreak`{=latex}", text)
    if greek:
        text = _grk_run.sub(lambda m: "`{\\greekfont " + m.group(0) + "}`{=latex}", text)
    return text
