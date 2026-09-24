"""PNG renderer for Lucas-square arrangements."""

from __future__ import annotations

from pathlib import Path

from ..constants import DEFAULT_SVG_UNITS_PER_INCH
from ..geometry import Square, bounds, filler_rectangles, page_placement


def render_png(
    squares: list[Square],
    output: Path,
    labels: bool,
    alignment: str,
    page_width: float,
    page_height: float,
    margin: float,
    dpi: int,
) -> None:
    """Render the arrangement to a PNG at the requested physical resolution."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as error:
        raise ValueError(
            "PNG output requires Pillow; install requirements.txt"
        ) from error
    if dpi <= 0:
        raise ValueError("PNG DPI must be a positive integer")
    pixel_width, pixel_height = round(page_width * dpi), round(page_height * dpi)
    image = Image.new("RGB", (pixel_width, pixel_height), "white")
    if not squares:
        image.save(output, dpi=(dpi, dpi))
        return
    placement = page_placement(squares, pixel_width, pixel_height, margin * dpi)
    assert placement is not None
    scale, left, top = placement
    draw = ImageDraw.Draw(image)
    if alignment == "seamless":
        for x, y, width, height in filler_rectangles(squares):
            draw.rectangle(
                (
                    left + x * scale,
                    top + y * scale,
                    left + (x + width) * scale,
                    top + (y + height) * scale,
                ),
                fill="#e8e8e8",
            )
    stroke_width = max(1, round(1.5 * dpi / DEFAULT_SVG_UNITS_PER_INCH))
    for square in squares:
        x, y, side = (
            left + square.x * scale,
            top + square.y * scale,
            square.size * scale,
        )
        draw.rectangle((x, y, x + side, y + side), outline="black", width=stroke_width)
        if labels and side >= 15:
            font_size = max(
                1,
                round(
                    min(side * 0.45, side * 1.35 / len(str(square.size)), dpi * 0.32)
                ),
            )
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except OSError:
                font = ImageFont.load_default()
            draw.text(
                (x + side / 2, y + side / 2),
                str(square.size),
                fill="black",
                font=font,
                anchor="mm",
            )
    if alignment == "seamless":
        width, height = bounds(squares)
        draw.rectangle(
            (left, top, left + width * scale, top + height * scale),
            outline="black",
            width=stroke_width,
        )
    image.save(output, dpi=(dpi, dpi))
