import csv, sys, statistics as st

rows = list(csv.DictReader(open(sys.argv[1], newline="", encoding="utf-8")))
print(f"rows: {len(rows)}\ncolumns: {list(rows[0]) if rows else []}")
for c in (rows[0] if rows else {}):
    try:
        v = [float(r[c]) for r in rows]
        print(f"{c}: min={min(v)} mean={st.mean(v):.3f} max={max(v)}")
    except ValueError:
        pass
