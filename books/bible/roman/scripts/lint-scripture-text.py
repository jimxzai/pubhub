#!/usr/bin/env python3
"""Check internal Scripture-version labeling; this does not replace rights review."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    manifest = json.loads((ROOT / "book.json").read_bytes().decode("utf-8"))
    chapters = [p for p in manifest["source_order"] if re.match(r"^(?:0[1-9]|1[0-6])-", p)]
    errors: list[str] = []
    for name in chapters:
        text = (ROOT / name).read_bytes().decode("utf-8")
        if text.count("### 中文 — 和合本") != 1:
            errors.append(f"{name}: expected one Chinese CUV Scripture heading")
        if text.count("### English — NASB") != 1:
            errors.append(f"{name}: expected one NASB Scripture heading")
        scripture_note = text[text.find("## 經文"):text.find("## 背景")]
        if "NASB 1995" not in scripture_note:
            errors.append(f"{name}: Scripture section does not identify NASB 1995")
        if "和合本" not in scripture_note:
            errors.append(f"{name}: Scripture section does not identify CUV")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: Scripture labels are internally consistent across {len(chapters)} chapters")
    print("NOTE: this is a labeling check, not a textual or licensing certification")
    return 0


if __name__ == "__main__":
    sys.exit(main())
