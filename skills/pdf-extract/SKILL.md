---
name: pdf-extract
description: Extracts text from a local PDF file, optionally limited to the first N pages. Use when the user asks what a PDF says, or wants its text, content or a page of it.
license: MIT
compatibility: Requires Python with the pypdf package installed.
---

# PDF text extraction

1. Run `scripts/extract.py` with the PDF path and, optionally, the maximum number of pages (default 3).
2. Use only the text it prints to answer. Text may be incomplete for scanned PDFs.
3. If the script reports an error or no text, tell the user; do not guess the contents.
