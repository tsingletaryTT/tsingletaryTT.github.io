#!/usr/bin/env python3
"""Generate a `card`-kind project figure: an SVG "terminal card".

For repos that ship no images at all. The card's text must be lifted **verbatim**
from the repo's own README or real command output — a card is a screenshot
substitute, not an illustration, so nothing here may invent numbers.

Two rules learned the hard way (see CLAUDE.md):

* Leading must be ~1.23x the font size. Tighter than that and any box-drawing
  vertical (│ ├ └) renders as a dashed line instead of a solid one.
* Cards are displayed at natural width (`.project-media--card img { width: auto }`),
  so keep the card near the 632px content column. Upscaling monospace blurs it.

Usage:
    python3 script/make_card.py <spec.json> <out.svg>

The spec is {"title", "aria", "lines": [[{"t": text, "c": color-key}, ...], ...]},
one list per line; an empty list is a blank line.
"""
import json
import sys
from xml.sax.saxutils import escape

FONT = "ui-monospace,Menlo,Consolas,'DejaVu Sans Mono',monospace"
SIZE = 13.0
LEADING = 16.0          # 1.23x SIZE — see the box-drawing note above
CHAR_W = SIZE * 0.6022  # advance width of this monospace stack at SIZE
PAD_X = 24.0
HEADER_H = 36.0         # title bar: dot + label + rule
TOP = 23.0              # first baseline below the header

# Palette lifted from assets/css/style.css so cards match the page they sit on.
COLORS = {
    "bg": "#111318",
    "border": "#232730",
    "muted": "#607D8B",   # --text-muted: prompts, labels, commentary
    "body": "#aaa",        # ordinary output
    "teal": "#4FD1C5",     # --teal: the values that carry the point
    "warn": "#F6BC42",
    "alert": "#FA512E",
}


def build(spec):
    lines = spec["lines"]
    width = PAD_X * 2 + CHAR_W * max(
        (sum(len(run["t"]) for run in line) for line in lines), default=0
    )
    height = HEADER_H + TOP + LEADING * (len(lines) - 1) + 22

    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" '
        'height="%d" role="img" aria-label="%s">'
        % (round(width), round(height), round(width), round(height), escape(spec["aria"])),
        '<rect x="0.5" y="0.5" width="%d" height="%d" rx="6" fill="%s" stroke="%s"/>'
        % (round(width) - 1, round(height) - 1, COLORS["bg"], COLORS["border"]),
        '<circle cx="28" cy="24" r="4" fill="%s"/>' % COLORS["teal"],
        '<text x="42" y="28" font-family="%s" font-size="11.5" fill="%s">%s</text>'
        % (FONT, COLORS["muted"], escape(spec["title"])),
        '<line x1="0" y1="%g" x2="%d" y2="%g" stroke="%s"/>'
        % (HEADER_H, round(width), HEADER_H, COLORS["border"]),
    ]

    for i, line in enumerate(lines):
        if not line:
            continue
        y = HEADER_H + TOP + LEADING * i
        # Each run is placed at its own absolute x, computed from the column it
        # starts in, so runs never depend on the renderer's kerning of the run
        # before them — that is what keeps columns aligned across colour changes.
        col, spans = 0, []
        for run in line:
            spans.append(
                '<tspan x="%.2f" fill="%s">%s</tspan>'
                % (PAD_X + col * CHAR_W, COLORS[run.get("c", "body")], escape(run["t"]))
            )
            col += len(run["t"])
        out.append(
            '<text y="%g" font-family="%s" font-size="%g" xml:space="preserve">%s</text>'
            % (y, FONT, SIZE, "".join(spans))
        )

    out.append("</svg>")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    spec_path, out_path = sys.argv[1], sys.argv[2]
    with open(spec_path) as fh:
        spec = json.load(fh)
    with open(out_path, "w") as fh:
        fh.write(build(spec))
    print("wrote %s" % out_path)
