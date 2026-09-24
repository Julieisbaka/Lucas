"""Draw printable Lucas squares on a 12-by-9-inch SVG page."""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from pathlib import Path


PAGE_WIDTH = 1200  # 100 SVG units per printed inch
PAGE_HEIGHT = 900
MARGIN = 45
TARGET_RATIO = PAGE_WIDTH / PAGE_HEIGHT
MAX_ITERATIONS = 70


@dataclass(frozen=True)
class Square:
    index: int
    size: int
    x: int
    y: int


def lucas_numbers(count: int) -> list[int]:
    """Return count Lucas numbers, starting with 2, 1."""
    if not 1 <= count <= MAX_ITERATIONS:
        raise ValueError(f"iterations must be between 1 and {MAX_ITERATIONS}")
    numbers = [2, 1]
    for _ in range(2, count):
        numbers.append(numbers[-1] + numbers[-2])
    return numbers[:count]


def bounds(squares: list[Square]) -> tuple[int, int]:
    return (max(s.x + s.size for s in squares),
            max(s.y + s.size for s in squares))


def normalize(squares: list[Square]) -> list[Square]:
    min_x = min(s.x for s in squares)
    min_y = min(s.y for s in squares)
    return [Square(s.index, s.size, s.x - min_x, s.y - min_y) for s in squares]


def landscape(squares: list[Square]) -> list[Square]:
    """Rotate a tall arrangement to better suit landscape paper."""
    width, height = bounds(squares)
    if width >= height:
        return squares
    return [Square(s.index, s.size, height - s.y - s.size, s.x)
            for s in squares]


def turning_layout(numbers: list[int]) -> list[Square]:
    """Place successive squares around the current outside edge, without an arc."""
    squares = [Square(0, numbers[0], 0, 0)]
    if len(numbers) > 1:
        squares.append(Square(1, numbers[1], numbers[0], 0))
    # Above, left, below, right, then repeat. Lucas squares can leave gaps.
    for index in range(2, len(numbers)):
        side = numbers[index]
        current = normalize(squares)
        width, height = bounds(current)
        direction = (index - 2) % 4
        if direction == 0:  # above
            x, y = 0, -side
        elif direction == 1:  # left
            x, y = -side, height - side
        elif direction == 2:  # below
            x, y = 0, height
        else:  # right
            x, y = width, 0
        squares = current + [Square(index, side, x, y)]
    return landscape(normalize(squares))


def shelf_layout(numbers: list[int], max_row_width: float) -> list[Square]:
    """Pack descending squares into edge-aligned rows of a given width."""
    result: list[Square] = []
    x = y = row_height = 0
    for index, side in sorted(enumerate(numbers), key=lambda item: -item[1]):
        if x and x + side > max_row_width:
            y += row_height
            x = row_height = 0
        result.append(Square(index, side, x, y))
        x += side
        row_height = max(row_height, side)
    return landscape(sorted(result, key=lambda square: square.index))


def layout_score(squares: list[Square]) -> tuple[float, float]:
    width, height = bounds(squares)
    occupied_area = sum(s.size * s.size for s in squares)
    return (abs(width / height - TARGET_RATIO),
            -occupied_area / (width * height))


def fit_layout(numbers: list[int]) -> list[Square]:
    """Try row widths and keep the closest, then most-filled 4:3 footprint."""
    descending = sorted(numbers, reverse=True)
    total_area = sum(side * side for side in numbers)
    ideal_width = math.sqrt(total_area * TARGET_RATIO)
    widths: set[float] = {ideal_width * factor for factor in
                          (0.5, 0.75, 1, 1.25, 1.5, 2)}
    running_width = 0
    for side in descending:
        running_width += side
        widths.add(float(running_width))
    return min((shelf_layout(numbers, width) for width in sorted(widths)),
               key=layout_score)


def choose_squares(iterations: int, layout: str, count_mode: str) -> list[Square]:
    """Pick exactly iterations squares, or the best count up to iterations."""
    lucas_numbers(iterations)  # Validate even if a different count is selected.
    place = turning_layout if layout == "turning" else fit_layout
    if count_mode == "exact":
        return place(lucas_numbers(iterations))
    if count_mode == "auto":
        return min((place(lucas_numbers(n)) for n in range(1, iterations + 1)),
                   key=lambda squares: (*layout_score(squares), -len(squares)))
    raise ValueError("count_mode must be 'exact' or 'auto'")


def filler_rectangles(squares: list[Square]) -> list[tuple[int, int, int, int]]:
    """Partition every uncovered part of the footprint into rectangles."""
    width, height = bounds(squares)
    xs = sorted({0, width} | {edge for s in squares for edge in (s.x, s.x + s.size)})
    ys = sorted({0, height} | {edge for s in squares for edge in (s.y, s.y + s.size)})
    fillers: list[tuple[int, int, int, int]] = []
    active: dict[tuple[int, int], int] = {}
    for y, next_y in zip(ys, ys[1:]):
        runs: set[tuple[int, int]] = set()
        start: int | None = None
        for x, next_x in zip(xs, xs[1:]):
            occupied = any(s.x <= x and next_x <= s.x + s.size and
                           s.y <= y and next_y <= s.y + s.size for s in squares)
            if not occupied and start is None:
                start = x
            if occupied and start is not None:
                runs.add((start, x))
                start = None
        if start is not None:
            runs.add((start, width))
        for (left, right), first_y in list(active.items()):
            if (left, right) not in runs:
                fillers.append((left, first_y, right - left, y - first_y))
                del active[(left, right)]
        for run in runs:
            active.setdefault(run, y)
    for (left, right), first_y in active.items():
        fillers.append((left, first_y, right - left, height - first_y))
    return sorted(fillers)


def render_svg(squares: list[Square], labels: bool = False,
               alignment: str = "seamless") -> str:
    """Render exact shared square edges; optionally fill unused footprint."""
    if alignment not in ("seamless", "edges"):
        raise ValueError("alignment must be 'seamless' or 'edges'")
    width, height = bounds(squares)
    scale = min((PAGE_WIDTH - 2 * MARGIN) / width,
                (PAGE_HEIGHT - 2 * MARGIN) / height)
    left = (PAGE_WIDTH - width * scale) / 2
    top = (PAGE_HEIGHT - height * scale) / 2
    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="12in" height="9in" '
        'viewBox="0 0 1200 900">',
        '<rect width="1200" height="900" fill="white"/>',
        f'<g transform="translate({left:.10f} {top:.10f}) scale({scale:.10f})">',
    ]
    if alignment == "seamless":
        lines.append('<g id="fillers" fill="#e8e8e8">')
        for x, y, filler_width, filler_height in filler_rectangles(squares):
            lines.append(f'<rect x="{x}" y="{y}" width="{filler_width}" '
                         f'height="{filler_height}"/>')
        lines.append('</g>')
    lines.append(f'<g id="lucas" fill="none" stroke="black" '
                 f'stroke-width="{1.5 / scale:.12g}">')
    for square in squares:
        lines.append(f'<rect x="{square.x}" y="{square.y}" '
                     f'width="{square.size}" height="{square.size}"/>')
    lines.append('</g>')
    if alignment == "seamless":
        lines.append(f'<rect width="{width}" height="{height}" fill="none" '
                     f'stroke="black" stroke-width="{1.5 / scale:.12g}"/>')
    lines.append('</g>')
    for square in squares:
        side = square.size * scale
        if labels and side >= 15:
            x = left + square.x * scale
            y = top + square.y * scale
            font_size = min(side * 0.45, side * 1.35 / len(str(square.size)), 32)
            lines.append(f'<text x="{x + side / 2:.4f}" y="{y + side / 2:.4f}" '
                         f'text-anchor="middle" dominant-baseline="central" '
                         f'font-family="sans-serif" font-size="{font_size:.4f}" '
                         f'fill="black">{square.size}</text>')
    lines.append('</svg>')
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iterations", type=int, default=8,
                        help="number of squares, or maximum count in auto mode (default: 8)")
    parser.add_argument("--count-mode", choices=("exact", "auto"), default="exact",
                        help="draw exactly N squares or choose the best ratio up to N")
    parser.add_argument("--layout", choices=("turning", "fit"), default="turning",
                        help="outward-turning arrangement or row-packed page fit")
    parser.add_argument("--alignment", choices=("seamless", "edges"),
                        default="seamless",
                        help="fill gaps for a solid rectangular footprint (default), "
                             "or draw only Lucas square edges")
    parser.add_argument("--labels", action="store_true",
                        help="print Lucas numbers inside squares when legible")
    parser.add_argument("--output", type=Path, default=Path("lucas_squares.svg"),
                        help="SVG file to create (default: lucas_squares.svg)")
    args = parser.parse_args()
    try:
        squares = choose_squares(args.iterations, args.layout, args.count_mode)
    except ValueError as error:
        parser.error(str(error))
    args.output.write_text(render_svg(squares, args.labels, args.alignment),
                           encoding="utf-8")
    width, height = bounds(squares)
    print(f"Wrote {args.output} ({len(squares)} squares; footprint "
          f"{width}:{height} = {width / height:.5f}; page 12:9 = {TARGET_RATIO:.5f})")


if __name__ == "__main__":
    main()