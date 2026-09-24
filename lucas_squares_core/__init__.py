"""Implementation package for the Lucas-square generator."""

from .constants import (
    DEFAULT_MARGIN,
    DEFAULT_MAX_ITERATIONS,
    DEFAULT_PAGE_HEIGHT,
    DEFAULT_PAGE_WIDTH,
    DEFAULT_SVG_UNITS_PER_INCH,
    TARGET_RATIO,
)
from .geometry import (
    Square,
    bounds,
    filler_rectangles,
    normalize,
    orient_for_page,
    page_placement,
    page_ratio,
)
from .layouts import (
    choose_squares,
    fit_layout,
    layout_score,
    lucas_numbers,
    shelf_layout,
    turning_layout,
)
from .renderers import render_pdf, render_png, render_svg, write_output

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
