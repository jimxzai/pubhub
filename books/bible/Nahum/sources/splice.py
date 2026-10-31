#!/usr/bin/env python3
"""Fill @@HYMN@@ and @@SCRIPTURE@@ placeholders in a chapter file from verified sources.
usage: splice.py FILE CH FROM-TO "GROUPS" HYMN-INDEX(1-5)"""
import sys, re, subprocess
from pathlib import Path
f, ch, rng, groups, hn = sys.argv[1:6]
here = Path(__file__).resolve().parent
blocks = (here / "hymns" / "hymn-blocks.md").read_text(encoding="utf-8")
parts = re.split(r"^## ch\.\d+ .*$", blocks, flags=re.M)[1:]
hymn = parts[int(hn) - 1].strip()
hymn = re.split(r"\n\(Stanza 2 line 8", hymn)[0].strip()
scr = subprocess.run([sys.executable, str(here / "scripture_block.py"), ch, rng, groups], capture_output=True, text=True, check=True).stdout.strip()
s = Path(f).read_text(encoding="utf-8")
s = re.sub(r"@@HYMN\d@@", lambda m: "## 配詩 (Opening Hymn)\n\n" + hymn, s)
s = s.replace("@@SCRIPTURE@@", scr)
Path(f).write_text(s, encoding="utf-8")
