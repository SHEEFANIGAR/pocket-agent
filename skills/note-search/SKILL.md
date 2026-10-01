---
name: note-search
description: Searches local plain-text and Markdown notes for a keyword and returns matching lines with file names. Use when the user asks to find, look up, or search their notes or text files for something.
license: MIT
---

# Note search

1. Run `scripts/search.py` with two arguments: the notes directory (default `notes`) and one keyword or phrase.
2. Report the matching lines and which file each came from.
3. If nothing matches, say no notes matched. Do not invent notes.
