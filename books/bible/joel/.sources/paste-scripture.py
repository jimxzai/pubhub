#!/usr/bin/env python3
"""paste-scripture.py <chapter.md>   — replace the chapter's `## 經文 (Scripture)` body with the generated unit
(.sources/units/<same-stem>.scripture.md). NEVER type Scripture by hand: the first Daniel chapter's hand-typed
block differed from the sources in a dozen places (宗室/王室, 一分/一份 ...)."""
import re, sys
from pathlib import Path
p = Path(sys.argv[1]).resolve()
unit = (Path(__file__).parent / "units" / f"{p.stem}.scripture.md").read_text().strip()
t = p.read_text()
new, n = re.subn(r"(## 經文 \(Scripture\)\n\n).*?(\n\n---\n+## 背景)", lambda m: m.group(1) + unit + m.group(2), t, flags=re.S)
if n != 1: sys.exit("could not find '## 經文 (Scripture)' … '---' '## 背景' in " + str(p))
p.write_text(new); print("pasted", p.name)
