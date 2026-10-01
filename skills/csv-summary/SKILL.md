---
name: csv-summary
description: Summarizes a local CSV file (row count, columns, numeric stats). Use when the user asks about the contents or statistics of a CSV file.
license: MIT
---

# CSV summary

1. Call `scripts/summarize.py` with the CSV path as the only argument.
2. Report the row count, column names, and numeric min/mean/max from its output.
3. If the script prints an error, report it. Do not guess values.
