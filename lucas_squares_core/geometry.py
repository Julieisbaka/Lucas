"""Square geometry, page validation, and placement helpers."""

from __future__ import annotations

import math
from dataclasses import dataclass

from .constants import DEFAULT_MARGIN


@dataclass(frozen=True)
class Square:
    """A Lucas square in unscaled arrangement coordinates."""

    index: int
    size: int
    x: int
    y: int


def bounds(squares: list[Square]) -> tuple[int, int]:
    """Return the width and height of the arrangement's enclosing rectangle."""
    if not squares:
        return (0, 0)
    return (max(s.x + s.size for s in squares), max(s.y + s.size for s in squares))


def page_ratio(
    page_width: float, page_height: float, margin: float = DEFAULT_MARGIN
) -> float:
    """Validate shared page dimensions and margin, then return their ratio."""
    if not all(math.isfinite(value) for value in (page_width, page_height, margin)):
        raise ValueError("page dimensions and margin must be finite numbers")
    if margin < 0:
        raise ValueError("margin cannot be negative")
    if min(page_width, page_height) <= 2 * margin:
        raise ValueError(
            f"page dimensions must be greater than twice the margin ({2 * margin:g})"
        )
    return page_width / page_height


def normalize(squares: list[Square]) -> list[Square]:
    """Translate an arrangement so its upper-left bound is at the origin."""
    if not squares:
        return []
    min_x = min(s.x for s in squares)
    min_y = min(s.y for s in squares)
    return [Square(s.index, s.size, s.x - min_x, s.y - min_y) for s in squares]


def orient_for_page(squares: list[Square], target_ratio: float) -> list[Square]:
    """Keep the orientation whose enclosing ratio is closest to the page."""
    if not squares:
        return []
    width, height = bounds(squares)
    if abs(width / height - target_ratio) <= abs(height / width - target_ratio):
        return squares
    return [Square(s.index, s.size, height - s.y - s.size, s.x) for s in squares]


def _unoccupied_runs(
    squares: list[Square], horizontal_edges: list[int], y: int, next_y: int
) -> set[tuple[int, int]]:
    """Return horizontal unoccupied intervals in one row of the edge grid."""
    runs: set[tuple[int, int]] = set()
    start: int | None = None
    for x, next_x in zip(horizontal_edges, horizontal_edges[1:]):
        occupied = any(
            square.x <= x
            and next_x <= square.x + square.size
            and square.y <= y
            and next_y <= square.y + square.size
            for square in squares
        )
        if not occupied and start is None:
            start = x
        if occupied and start is not None:
            runs.add((start, x))
            start = None
    if start is not None:
        runs.add((start, horizontal_edges[-1]))
    return runs


def filler_rectangles(squares: list[Square]) -> list[tuple[int, int, int, int]]:
    """Partition every uncovered part of the arrangement footprint into rectangles."""
    if not squares:
        return []
    width, height = bounds(squares)
    horizontal_edges = sorted(
        {0, width} | {edge for s in squares for edge in (s.x, s.x + s.size)}
    )
    vertical_edges = sorted(
        {0, height} | {edge for s in squares for edge in (s.y, s.y + s.size)}
    )
    fillers: list[tuple[int, int, int, int]] = []
    active: dict[tuple[int, int], int] = {}
    for y, next_y in zip(vertical_edges, vertical_edges[1:]):
        runs = _unoccupied_runs(squares, horizontal_edges, y, next_y)
        for (left, right), first_y in list(active.items()):
            if (left, right) not in runs:
                fillers.append((left, first_y, right - left, y - first_y))
                del active[(left, right)]
        for run in runs:
            active.setdefault(run, y)
    for (left, right), first_y in active.items():
        fillers.append((left, first_y, right - left, height - first_y))
    return sorted(fillers)


def page_placement(
    squares: list[Square],
    page_width_units: float,
    page_height_units: float,
    margin_units: float,
) -> tuple[float, float, float] | None:
    """Return the uniform scale and top-left offset for a non-empty arrangement."""
    if not squares:
        return None
    width, height = bounds(squares)
    scale = min(
        (page_width_units - 2 * margin_units) / width,
        (page_height_units - 2 * margin_units) / height,
    )
    return (
        scale,
        (page_width_units - width * scale) / 2,
        (page_height_units - height * scale) / 2,
    )


def scaled_square(
    square: Square, scale: float, left: float, top: float
) -> tuple[float, float, float]:
    """Return a square's scaled x/y position and side length on the output page."""
    return (left + square.x * scale, top + square.y * scale, square.size * scale)
