"""Shared font loading for the Romans PDF patch scripts.

`insert_htmlbox()` ignores a CSS `font-family` that names a system font by
its display name — it silently falls back to its own bundled Droid Sans
Fallback (CJK) / Charis SIL (Latin) instead of erroring or warning. Verified
on this book: exactly the 15 pages patched via `put()`/`replace()`
(merge_baseline_pdf.py) and both cover pages (cover_design.py) render in
those fallback fonts instead of the project's Songti SC / Times New Roman
standard. Fix: register the real font as an `@font-face` backed by an
in-memory `fitz.Archive`, never by name alone. Fonts are read live from the
local macOS install each run (see eat-bible SKILL.md, "Fonts are a hard
macOS dependency") and never written to disk or committed.
"""
import io
from pathlib import Path


def _extract_from_collection(path, family, style):
    from fontTools.ttLib import TTCollection
    if not Path(path).is_file():
        raise SystemExit(f'{path} not found; this patch requires macOS with {family} installed')
    tc = TTCollection(path)
    for face in tc.fonts:
        if face['name'].getDebugName(1) == family and face['name'].getDebugName(2) == style:
            buf = io.BytesIO()
            face.save(buf)
            return buf.getvalue()
    raise SystemExit(f'{family} {style} face not found in {path}')


def _extract_single(path, family):
    from fontTools.ttLib import TTFont
    if not Path(path).is_file():
        raise SystemExit(f'{path} not found; this patch requires macOS with {family} installed')
    tt = TTFont(path)
    buf = io.BytesIO()
    tt.save(buf)
    return buf.getvalue()


def load_songti_regular():
    return _extract_from_collection('/System/Library/Fonts/Supplemental/Songti.ttc', 'Songti SC', 'Regular')


def load_times_italic():
    return _extract_single('/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf', 'Times New Roman Italic')
