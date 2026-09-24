"""Output renderers and format dispatch."""

from __future__ import annotations

from pathlib import Path

from ..geometry import Square
from .pdf import render_pdf
from .png import render_png
from .svg import render_svg


def write_output(svg: str, squares: list[Square], output: Path, output_format: str,
                 labels: bool, alignment: str, page_width: float, page_height: float,
                 margin: float, dpi: int) -> None:
    """Write the selected vector or raster output format."""
    if output_format == "svg":
        output.write_text(svg, encoding="utf-8")
    elif output_format == "png":
        render_png(squares, output, labels, alignment, page_width, page_height, margin, dpi)
    elif output_format == "pdf":
        render_pdf(squares, output, labels, alignment, page_width, page_height, margin)
    else:
        raise ValueError("format must be 'svg', 'png', or 'pdf'")


__all__ = ["render_pdf", "render_png", "render_svg", "write_output"]