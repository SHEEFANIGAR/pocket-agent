import sys
from pathlib import Path

if len(sys.argv) < 3:
    print("ERROR: Usage: search.py NOTES_DIR QUERY")
    sys.exit(1)
root, q = Path(sys.argv[1]), " ".join(sys.argv[2:]).lower()
if not root.is_dir():
    print(f"ERROR: directory not found: {root}")
    sys.exit(1)
hits = []
for f in sorted(root.rglob("*")):
    if f.suffix.lower() in {".txt", ".md"} and f.is_file():
        for i, line in enumerate(f.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            if q in line.lower():
                hits.append(f"{f.relative_to(root)}:{i}: {line.strip()}")
print("\n".join(hits[:10]) if hits else "no matches")
