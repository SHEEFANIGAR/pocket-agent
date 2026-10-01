import sys

TABLES = {
    "length": {"mm": 0.001, "cm": 0.01, "m": 1, "km": 1000, "in": 0.0254, "ft": 0.3048, "yd": 0.9144, "mi": 1609.344},
    "mass": {"g": 0.001, "kg": 1, "oz": 0.028349523125, "lb": 0.45359237},
    "volume": {"ml": 0.001, "l": 1, "cup": 0.2365882365, "gal": 3.785411784},
}
TEMPS = {"c", "f", "k"}


def to_c(v, u):
    return v if u == "c" else (v - 32) * 5 / 9 if u == "f" else v - 273.15


def from_c(v, u):
    return v if u == "c" else v * 9 / 5 + 32 if u == "f" else v + 273.15


def convert(value, src, dst):
    if src in TEMPS and dst in TEMPS:
        return from_c(to_c(value, src), dst)
    for t in TABLES.values():
        if src in t and dst in t:
            return value * t[src] / t[dst]
    raise ValueError(f"cannot convert '{src}' to '{dst}'")


if __name__ == "__main__":
    try:
        v, s, d = float(sys.argv[1]), sys.argv[2].lower(), sys.argv[3].lower()
        print(f"{v:g} {s} = {convert(v, s, d):.4f} {d}")
    except (IndexError, ValueError) as e:
        print(f"ERROR: {e}. Usage: convert.py VALUE FROM TO")
        sys.exit(1)
