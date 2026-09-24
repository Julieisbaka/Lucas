"""Lucas number generation and square-layout strategies."""

from __future__ import annotations

import math

from .constants import DEFAULT_MAX_ITERATIONS, TARGET_RATIO
from .geometry import Square, bounds, normalize, orient_for_page


def lucas_numbers(count: int, max_iterations: int = DEFAULT_MAX_ITERATIONS) -> list[int]:
    """Return count Lucas numbers, starting with 2, 1."""
    if max_iterations < 0:
        raise ValueError("max iterations cannot be negative")
    if not 0 <= count <= max_iterations:
        raise ValueError(f"iterations must be between 0 and {max_iterations}")
    numbers = [2, 1]
    for _ in range(2, count):
        numbers.append(numbers[-1] + numbers[-2])
    return numbers[:count]


def turning_layout(numbers: list[int], target_ratio: float = TARGET_RATIO) -> list[Square]:
    """Place successive squares around the current outside edge, without an arc."""
    if not numbers:
        return []
    squares = [Square(0, numbers[0], 0, 0)]
    if len(numbers) > 1:
        squares.append(Square(1, numbers[1], numbers[0], 0))
    for index in range(2, len(numbers)):
        side = numbers[index]
        current = normalize(squares)
        width, height = bounds(current)
        direction = (index - 2) % 4
        if direction == 0:
            x, y = 0, -side
        elif direction == 1:
            x, y = -side, height - side
        elif direction == 2:
            x, y = 0, height
        else:
            x, y = width, 0
        squares = current + [Square(index, side, x, y)]
    return orient_for_page(normalize(squares), target_ratio)


def shelf_layout(numbers: list[int], max_row_width: float,
                 target_ratio: float) -> list[Square]:
    """Pack descending squares into edge-aligned rows of a given width."""
    if not numbers:
        return []
    result: list[Square] = []
    x = y = row_height = 0
    for index, side in sorted(enumerate(numbers), key=lambda item: -item[1]):
        if x and x + side > max_row_width:
            y += row_height
            x = row_height = 0
        result.append(Square(index, side, x, y))
        x += side
        row_height = max(row_height, side)
    return orient_for_page(sorted(result, key=lambda square: square.index), target_ratio)


def layout_score(squares: list[Square], target_ratio: float = TARGET_RATIO
                 ) -> tuple[float, float]:
    if not squares:
        return (float("inf"), 0.0)
    width, height = bounds(squares)
    occupied_area = sum(s.size * s.size for s in squares)
    return (abs(width / height - target_ratio), -occupied_area / (width * height))


def fit_layout(numbers: list[int], target_ratio: float = TARGET_RATIO) -> list[Square]:
    """Try row widths and keep the closest, then most-filled page footprint."""
    if not numbers:
        return []
    descending = sorted(numbers, reverse=True)
    ideal_width = math.sqrt(sum(side * side for side in numbers) * target_ratio)
    widths = {ideal_width * factor for factor in (0.5, 0.75, 1, 1.25, 1.5, 2)}
    running_width = 0
    for side in descending:
        running_width += side
        widths.add(float(running_width))
    return min((shelf_layout(numbers, width, target_ratio) for width in sorted(widths)),
               key=lambda squares: layout_score(squares, target_ratio))


def choose_squares(iterations: int, layout: str, count_mode: str,
                   target_ratio: float = TARGET_RATIO,
                   max_iterations: int = DEFAULT_MAX_ITERATIONS) -> list[Square]:
    """Pick exactly iterations squares, or the best count up to iterations."""
    lucas_numbers(iterations, max_iterations)
    if iterations == 0:
        return []
    place = turning_layout if layout == "turning" else fit_layout
    if count_mode == "exact":
        return place(lucas_numbers(iterations, max_iterations), target_ratio)
    if count_mode == "auto":
        return min((place(lucas_numbers(count, max_iterations), target_ratio)
                    for count in range(1, iterations + 1)),
                   key=lambda squares: (*layout_score(squares, target_ratio), -len(squares)))
    raise ValueError("count_mode must be 'exact' or 'auto'")