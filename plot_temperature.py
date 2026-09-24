"""Plot temperature_data.csv as an SVG line chart (no third-party dependencies)."""
import csv

W, H = 720, 420
LEFT, RIGHT, TOP, BOTTOM = 64, 40, 64, 56
Y_MIN, Y_MAX, Y_STEP = -5, 40, 5

SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID = "#e4e3df"
BASELINE = "#a3a29c"
SERIES = "#2a78d6"

with open("temperature_data.csv") as f:
    rows = [(int(r["index"]), float(r["temperature_c"])) for r in csv.DictReader(f)]

n = len(rows)
plot_w, plot_h = W - LEFT - RIGHT, H - TOP - BOTTOM


def x(i):
    return LEFT + (i - 1) / (n - 1) * plot_w


def y(t):
    return TOP + (Y_MAX - t) / (Y_MAX - Y_MIN) * plot_h


out = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
    f'viewBox="0 0 {W} {H}" font-family="system-ui, -apple-system, Segoe UI, sans-serif">',
    f'<rect width="{W}" height="{H}" fill="{SURFACE}"/>',
    f'<text x="{LEFT}" y="28" font-size="16" font-weight="600" fill="{TEXT_PRIMARY}">'
    f"Temperature measurements (°C)</text>",
    f'<text x="{LEFT}" y="46" font-size="12" fill="{TEXT_SECONDARY}">'
    f"{n} random readings between {Y_MIN} °C and {Y_MAX} °C</text>",
]

# Horizontal gridlines and y-axis labels; 0 °C gets a stronger line.
for t in range(Y_MIN, Y_MAX + 1, Y_STEP):
    stroke = BASELINE if t == 0 else GRID
    out.append(f'<line x1="{LEFT}" x2="{W - RIGHT}" y1="{y(t):.1f}" y2="{y(t):.1f}" '
               f'stroke="{stroke}" stroke-width="1"/>')
    out.append(f'<text x="{LEFT - 8}" y="{y(t) + 4:.1f}" font-size="11" text-anchor="end" '
               f'fill="{TEXT_SECONDARY}">{t}</text>')

# X-axis labels.
for i, _ in rows:
    out.append(f'<text x="{x(i):.1f}" y="{H - BOTTOM + 18}" font-size="11" text-anchor="middle" '
               f'fill="{TEXT_SECONDARY}">{i}</text>')
out.append(f'<text x="{LEFT + plot_w / 2}" y="{H - 12}" font-size="12" text-anchor="middle" '
           f'fill="{TEXT_SECONDARY}">Measurement #</text>')

# Line and point markers, each with a hover tooltip.
points = " ".join(f"{x(i):.1f},{y(t):.1f}" for i, t in rows)
out.append(f'<polyline points="{points}" fill="none" stroke="{SERIES}" stroke-width="2" '
           f'stroke-linejoin="round"/>')
for i, t in rows:
    out.append(f'<circle cx="{x(i):.1f}" cy="{y(t):.1f}" r="4.5" fill="{SERIES}" '
               f'stroke="{SURFACE}" stroke-width="2"><title>#{i}: {t:.1f} °C</title></circle>')

# Direct labels on the highest and lowest readings only.
for i, t in (max(rows, key=lambda r: r[1]), min(rows, key=lambda r: r[1])):
    dy = -12 if t == max(r[1] for r in rows) else 20
    out.append(f'<text x="{x(i):.1f}" y="{y(t) + dy:.1f}" font-size="11" font-weight="600" '
               f'text-anchor="middle" fill="{TEXT_PRIMARY}">{t:.1f} °C</text>')

out.append("</svg>")

with open("temperature_plot.svg", "w") as f:
    f.write("\n".join(out) + "\n")
print("Wrote temperature_plot.svg")
