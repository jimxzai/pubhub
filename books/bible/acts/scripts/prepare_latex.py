#!/usr/bin/env python3
"""Prepare the generated Markdown stream for the LaTeX renderer."""

from __future__ import annotations

import re
import sys
from pathlib import Path


source = Path(sys.argv[1])
target = Path(sys.argv[2])
text = source.read_text(encoding="utf-8")
text = re.sub(
    r"\^(\d+(?:-\d+)?)\^",
    lambda match: rf"\textsuperscript{{{match.group(1)}}}",
    text,
)
target.write_text(text, encoding="utf-8")
