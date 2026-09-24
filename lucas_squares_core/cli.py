"""Command-line interface for the Lucas-square generator."""

from __future__ import annotations

import argparse
from pathlib import Path

from .constants import (DEFAULT_MARGIN, DEFAULT_MAX_ITERATIONS, DEFAULT_PAGE_HEIGHT,
                        DEFAULT_PAGE_WIDTH, DEFAULT_SVG_UNITS_PER_INCH)
from .geometry import bounds, page_ratio
from .layouts import choose_squares
from .renderers import render_svg, write_output


def main() -> None:
    parser = argparse.ArgumentParser(description="Draw printable Lucas squares on a page.")
    parser.add_argument("--iterations", type=int, default=8,
                        help="number of squares, or maximum count in auto mode (default: 8)")
    parser.add_argument("--count-mode", choices=("exact", "auto"), default="exact",
                        help="draw exactly N squares or choose the best ratio up to N")
    parser.add_argument("--layout", choices=("turning", "fit"), default="turning",
                        help="outward-turning arrangement or row-packed page fit")
    parser.add_argument("--alignment", choices=("seamless", "edges"), default="seamless",
                        help="fill gaps for a solid rectangular footprint (default), "
                             "or draw only Lucas square edges")
    parser.add_argument("--width", type=float, default=DEFAULT_PAGE_WIDTH,
                        help="printed page width in inches (default: 12)")
    parser.add_argument("--height", type=float, default=DEFAULT_PAGE_HEIGHT,
                        help="printed page height in inches (default: 9)")
    parser.add_argument("--margin", type=float, default=DEFAULT_MARGIN,
                        help="white page margin in the same unit as width and height (default: 0.45)")
    parser.add_argument("--svg-units-per-inch", type=float,
                        default=DEFAULT_SVG_UNITS_PER_INCH,
                        help="SVG viewBox units assigned to each printed inch (default: 100)")
    parser.add_argument("--max-iterations", "--override-max-iterations", dest="max_iterations",
                        type=int, default=DEFAULT_MAX_ITERATIONS,
                        help="raise or lower the iteration safety limit (default: 70)")
    parser.add_argument("--labels", action="store_true",
                        help="print Lucas numbers inside squares when legible")
    parser.add_argument("--format", choices=("svg", "png", "pdf"), default="svg",
                        help="output file format (default: svg)")
    parser.add_argument("--dpi", type=int, default=300,
                        help="PNG output resolution in dots per inch (default: 300)")
    parser.add_argument("--output", type=Path,
                        help="output file to create (default: lucas_squares.FORMAT)")
    args = parser.parse_args()
    try:
        ratio = page_ratio(args.width, args.height, args.margin)
        squares = choose_squares(args.iterations, args.layout, args.count_mode, ratio,
                                 args.max_iterations)
        svg = render_svg(squares, args.labels, args.alignment, args.width, args.height,
                         args.margin, args.svg_units_per_inch)
    except ValueError as error:
        parser.error(str(error))
    output = args.output or Path(f"lucas_squares.{args.format}")
    try:
        write_output(svg, squares, output, args.format, args.labels, args.alignment,
                     args.width, args.height, args.margin, args.dpi)
    except ValueError as error:
        parser.error(str(error))
    if squares:
        width, height = bounds(squares)
        print(f"Wrote {output} ({args.format}; {len(squares)} squares; footprint "
              f"{width}:{height} = {width / height:.5f}; page {args.width:g}:{args.height:g} "
              f"= {args.width / args.height:.5f})")
    else:
        print(f"Wrote {output} ({args.format}; 0 squares; blank page)")