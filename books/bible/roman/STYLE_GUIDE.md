# Editorial and production style guide

## Language

- Use Traditional Chinese throughout the Chinese prose.
- Use `這裏`, `裏`, `祂`, and other project-approved forms consistently; do not normalize character variants mechanically without editorial review.
- Use one term consistently for each theological concept. Record intentional exceptions in the glossary before release.
- Keep English section labels in parentheses only where they help the bilingual reader.

## Scripture

- Chinese Scripture: 和合本 (CUV), unless a passage is explicitly marked as a textual or translation comparison.
- English Scripture: New American Standard Bible (NASB 1995), not NASB 2020.
- Verse numbers use semantic HTML `<sup>n</sup>` so they survive HTML, EPUB, and PDF conversion.
- Every Scripture block must retain its version note and source record.

## Sources

- Quoted text must be distinguished from paraphrase and editorial synthesis.
- A quotation requires author, work, edition or sermon identifier, location, URL or archive reference, access date, and rights status.
- “撮述”, “一般性歸納”, and “方法論之應用” are not interchangeable with verbatim quotation.

## Markdown

- Use semantic Markdown only in manuscript files.
- Do not add raw LaTeX commands to content files.
- Use headings in the canonical section order defined in `book.json`.
- Use tables for compact comparisons, not for long prose.
- Keep paragraphs short enough for both print and reflowable digital editions.
