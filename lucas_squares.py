"""Compatibility facade and executable for the Lucas-square generator."""

from lucas_squares_core import (
    DEFAULT_MARGIN,
    DEFAULT_MAX_ITERATIONS,
    DEFAULT_PAGE_HEIGHT,
    DEFAULT_PAGE_WIDTH,
    DEFAULT_SVG_UNITS_PER_INCH,
    TARGET_RATIO,
    Square,
    bounds,
    choose_squares,
    filler_rectangles,
    fit_layout,
    layout_score,
    lucas_numbers,
    normalize,
    orient_for_page,
    page_placement,
    page_ratio,
    render_pdf,
    render_png,
    render_svg,
    shelf_layout,
    turning_layout,
    write_output,
)
from lucas_squares_core.cli import main

__all__ = [
    "DEFAULT_MARGIN",
    "DEFAULT_MAX_ITERATIONS",
    "DEFAULT_PAGE_HEIGHT",
    "DEFAULT_PAGE_WIDTH",
    "DEFAULT_SVG_UNITS_PER_INCH",
    "TARGET_RATIO",
    "Square",
    "bounds",
    "choose_squares",
    "filler_rectangles",
    "fit_layout",
    "layout_score",
    "lucas_numbers",
    "main",
    "normalize",
    "orient_for_page",
    "page_placement",
    "page_ratio",
    "render_pdf",
    "render_png",
    "render_svg",
    "shelf_layout",
    "turning_layout",
    "write_output",
]


if __name__ == "__main__":
    main()
