# Correction Log

## Changes Made to Markdown Files

1. **Newline Preservation**: The initial issue where all paragraphs were merged onto a single line has been corrected. The markdown files now preserve their original structural newlines and readability.

2. **Deduplication of Cascading Lines**: Fixed a widespread formatting anomaly where paragraphs were duplicated in a cascading pattern (A, A, B, B, C, C, etc.) caused by the initial data extraction. 
   - A Python script (`process_final.py`) was used to scan all `.md` files line by line, comparing each line against the previously seen non-empty line.
   - Any exactly matching or highly similar adjacent lines were merged, preserving the one with the richest formatting (e.g. keeping code blocks and links over plain text).

3. **Backlink Conversion**: All external links targeting `learncpp.com` (e.g., `[O.2 -- Bitwise operators](https://www.learncpp.com/cpp-tutorial/bitwise-operators/)`) were converted to Obsidian-compatible internal links (e.g., `[[O.2 -- Bitwise operators]]`).

4. **Heading & Spacing Cleanup**:
   - Ensured a single space follows Markdown header hashes (e.g., `#Header` -> `# Header`) for better rendering.
   - Collapsed blocks of 3 or more empty lines into double empty lines to maintain a uniform, clean document flow.

All changes were carefully scripted to ensure no arbitrary content deletion occurred. The integrity of all code blocks and learning material was preserved.
