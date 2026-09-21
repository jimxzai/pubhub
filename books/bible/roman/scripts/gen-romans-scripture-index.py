#!/usr/bin/env python3
"""Generate a candidate Scripture-reference report for editorial review.

The published index remains curated because a regex cannot reliably decide
whether every reference is an argument, a quotation, or merely background.
This report makes omissions visible without silently rewriting the book.
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "build" / "scripture-reference-candidates.tsv"

BOOKS = (
    "創世記|出埃及記|利未記|民數記|申命記|約書亞記|士師記|路得記|撒母耳記上|撒母耳記下|"
    "列王紀上|列王紀下|歷代志上|歷代志下|以斯拉記|尼希米記|以斯帖記|約伯記|詩篇|箴言|"
    "傳道書|雅歌|以賽亞書|耶利米書|耶利米哀歌|以西結書|但以理書|何西阿書|約珥書|阿摩司書|"
    "俄巴底亞書|約拿書|彌迦書|那鴻書|哈巴谷書|西番雅書|哈該書|撒迦利亞書|瑪拉基書|"
    "馬太福音|馬可福音|路加福音|約翰福音|使徒行傳|羅馬書|哥林多前書|哥林多後書|加拉太書|"
    "以弗所書|腓立比書|歌羅西書|帖撒羅尼迦前書|帖撒羅尼迦後書|提摩太前書|提摩太後書|"
    "提多書|腓利門書|希伯來書|雅各書|彼得前書|彼得後書|約翰一書|約翰二書|約翰三書|猶大書|啟示錄"
)
ALIASES = dict(zip(
    '創 出 利 民 申 書 士 得 撒上 撒下 王上 王下 代上 代下 拉 尼 斯 伯 詩 箴 傳 歌 賽 耶 哀 結 但 何 珥 摩 俄 拿 彌 鴻 哈 番 該 亞 瑪 太 可 路 約 徒 羅 林前 林後 加 弗 腓 西 帖前 帖後 提前 提後 多 門 來 雅 彼前 彼後 約一 約二 約三 猶 啟'.split(),
    BOOKS.split('|')))
ALIASES.update({'Romans': '羅馬書', 'Rom': '羅馬書', 'Genesis': '創世記', 'Gen': '創世記', 'Psalms': '詩篇', 'Ps': '詩篇', 'Galatians': '加拉太書', 'Gal': '加拉太書', 'Acts': '使徒行傳', 'John': '約翰福音'})
NAMES = '|'.join(re.escape(s) for s in sorted(BOOKS.split('|') + list(ALIASES), key=len, reverse=True))
REFERENCE = re.compile(rf"(?<![A-Za-z])({NAMES})\.?\s*([0-9]+)(?:[:：]([0-9]+)(?:[-–]([0-9]+))?)?")


def main() -> int:
    manifest = json.loads((ROOT / "book.json").read_bytes().decode("utf-8"))
    hits: dict[str, set[str]] = defaultdict(set)
    for name in manifest["source_order"]:
        if name in ('98-appendix-indices.md', '99-appendix-references.md', '998-colophon.md'):
            continue  # An index must not count itself as evidence of a citation.
        text = (ROOT / name).read_bytes().decode("utf-8")
        for match in REFERENCE.finditer(text):
            book, chapter, verse, end_verse = match.groups()
            book = ALIASES.get(book, book)
            reference = f"{book} {chapter}"
            if verse:
                reference += f":{verse}"
                if end_verse:
                    reference += f"-{end_verse}"
            hits[reference].add(name)

    OUTPUT.parent.mkdir(exist_ok=True)
    lines = ["reference\tsources"]
    for reference in sorted(hits):
        lines.append(f"{reference}\t{', '.join(sorted(hits[reference]))}")
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"OK: generated {len(hits)} Scripture-reference candidates at {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
