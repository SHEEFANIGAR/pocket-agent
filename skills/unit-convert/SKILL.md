---
name: unit-convert
description: Converts a number between units of length, mass, volume or temperature. Use when the user asks to convert, e.g. km to miles, kg to pounds, litres to gallons, Celsius to Fahrenheit.
license: MIT
---

# Unit conversion

1. Run `scripts/convert.py` with three arguments: the value, the source unit, the target unit (for example `12 km mi`).
2. Report the script's output as the answer.
3. If it prints an error (unknown or incompatible units), say so. Never compute the conversion yourself.

Supported units: mm cm m km in ft yd mi | g kg oz lb | ml l cup gal | c f k
