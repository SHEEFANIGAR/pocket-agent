import sys

if len(sys.argv) < 2:
    print("ERROR: Usage: extract.py FILE.pdf [MAX_PAGES]")
    sys.exit(1)
try:
    from pypdf import PdfReader
except ImportError:
    print("ERROR: pypdf is not installed (pip install pypdf)")
    sys.exit(1)
try:
    reader = PdfReader(sys.argv[1])
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    out = []
    for i, page in enumerate(reader.pages[:limit], 1):
        out.append(f"--- page {i} ---\n{(page.extract_text() or '').strip()}")
    text = "\n".join(out)
    print(text[:3500] if text.strip() else "no extractable text")
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
