"""SVG renderer for Lucas-square arrangements."""

from __future__ import annotations

import math

from ..constants import (DEFAULT_MARGIN, DEFAULT_PAGE_HEIGHT, DEFAULT_PAGE_WIDTH,
                         DEFAULT_SVG_UNITS_PER_INCH)
from ..geometry import Square, bounds, filler_rectangles, page_placement, page_ratio


def render_svg(squares: list[Square], labels: bool = False, alignment: str = "seamless",
               page_width: float = DEFAULT_PAGE_WIDTH,
               page_height: float = DEFAULT_PAGE_HEIGHT,
               margin: float = DEFAULT_MARGIN,
               svg_units_per_inch: float = DEFAULT_SVG_UNITS_PER_INCH) -> str:
    """Render exact shared square edges; optionally fill unused footprint."""
    if alignment not in ("seamless", "edges"):
        raise ValueError("alignment must be 'seamless' or 'edges'")
    page_ratio(page_width, page_height, margin)
    if not math.isfinite(svg_units_per_inch) or svg_units_per_inch <= 0:
        raise ValueError("SVG units per inch must be a positive finite number")
    page_width_units = page_width * svg_units_per_inch
    page_height_units = page_height * svg_units_per_inch
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{page_width:g}in" '
        f'height="{page_height:g}in" viewBox="0 0 {page_width_units:g} {page_height_units:g}">',
        f'<rect width="{page_width_units:g}" height="{page_height_units:g}" fill="white"/>',
    ]
    if not squares:
        lines.append("</svg>")
        return "\n".join(lines) + "\n"
    placement = page_placement(squares, page_width_units, page_height_units,
                               margin * svg_units_per_inch)
    assert placement is not None
    scale, left, top = placement
    width, height = bounds(squares)
    lines.append(f'<g transform="translate({left:.15g} {top:.15g}) scale({scale:.15g})">')
    if alignment == "seamless":
        lines.append('<g id="fillers" fill="#e8e8e8">')
        for x, y, filler_width, filler_height in filler_rectangles(squares):
            lines.append(f'<rect x="{x}" y="{y}" width="{filler_width}" height="{filler_height}"/>')
        lines.append("</g>")
    lines.append(f'<g id="lucas" fill="none" stroke="black" stroke-width="{1.5 / scale:.12g}">')
    for square in squares:
        lines.append(f'<rect x="{square.x}" y="{square.y}" '
                     f'width="{square.size}" height="{square.size}"/>')
    lines.append("</g>")
    if alignment == "seamless":
        lines.append(f'<rect width="{width}" height="{height}" fill="none" '
                     f'stroke="black" stroke-width="{1.5 / scale:.12g}"/>')
    lines.append("</g>")
    for square in squares:
        side = square.size * scale
        if labels and side >= 15:
            x, y = left + square.x * scale, top + square.y * scale
            font_size = min(side * 0.45, side * 1.35 / len(str(square.size)), 32)
            lines.append(f'<text x="{x + side / 2:.4f}" y="{y + side / 2:.4f}" '
                         f'text-anchor="middle" dominant-baseline="central" '
                         f'font-family="sans-serif" font-size="{font_size:.4f}" '
                         f'fill="black">{square.size}</text>')
    lines.append("</svg>")
    return "\n".join(lines) + "\n"