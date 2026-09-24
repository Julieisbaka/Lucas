"""PDF renderer for Lucas-square arrangements."""

from __future__ import annotations

from pathlib import Path

from ..constants import DEFAULT_SVG_UNITS_PER_INCH
from ..geometry import (
    Square,
    bounds,
    filler_rectangles,
    page_placement,
    scaled_square,
)


# Lazy import keeps SVG-only use independent of ReportLab.
# pylint: disable=too-many-arguments,too-many-locals,import-outside-toplevel
def render_pdf(
    squares: list[Square],
    output: Path,
    labels: bool,
    alignment: str,
    page_width: float,
    page_height: float,
    margin: float,
) -> None:
    """Render the arrangement as a vector PDF at the requested page size."""
    try:
        from reportlab.lib.colors import Color, black
        from reportlab.pdfgen.canvas import Canvas
    except ImportError as error:
        raise ValueError(
            "PDF output requires reportlab; install requirements.txt"
        ) from error
    points_per_inch = 72
    page_width_points, page_height_points = (
        page_width * points_per_inch,
        page_height * points_per_inch,
    )
    canvas = Canvas(str(output), pagesize=(page_width_points, page_height_points))
    if squares:
        placement = page_placement(
            squares, page_width_points, page_height_points, margin * points_per_inch
        )
        assert placement is not None
        scale, left, top = placement
        if alignment == "seamless":
            canvas.setFillColor(Color(0.91, 0.91, 0.91))
            for x, y, width, height in filler_rectangles(squares):
                canvas.rect(
                    left + x * scale,
                    page_height_points - top - (y + height) * scale,
                    width * scale,
                    height * scale,
                    stroke=0,
                    fill=1,
                )
        canvas.setStrokeColor(black)
        canvas.setFillColor(black)
        canvas.setLineWidth(1.5 * points_per_inch / DEFAULT_SVG_UNITS_PER_INCH)
        for square in squares:
            x, y, side = scaled_square(square, scale, left, top)
            canvas.rect(x, page_height_points - y - side, side, side, stroke=1, fill=0)
            if labels and side >= 15:
                font_size = min(
                    side * 0.45,
                    side * 1.35 / len(str(square.size)),
                    points_per_inch * 0.32,
                )
                canvas.setFont("Helvetica", font_size)
                # ReportLab writes a PDF text operator here, not a raster glyph.
                canvas.drawCentredString(
                    x + side / 2,
                    page_height_points - y - side / 2 - font_size * 0.35,
                    str(square.size),
                )
        if alignment == "seamless":
            width, height = bounds(squares)
            canvas.rect(
                left,
                page_height_points - top - height * scale,
                width * scale,
                height * scale,
                stroke=1,
                fill=0,
            )
    canvas.save()
