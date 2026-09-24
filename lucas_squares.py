"""Generate printable Lucas-square arrangements as SVG, PNG, or PDF."""

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
    scaled_square,
    shelf_layout,
    turning_layout,
    write_output,
)
from lucas_squares_core import __all__ as _CORE_EXPORTS
from lucas_squares_core.cli import main

__all__ = [*_CORE_EXPORTS, "main"]


if __name__ == "__main__":
    main()
