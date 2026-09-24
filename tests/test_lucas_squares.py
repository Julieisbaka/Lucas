"""Regression tests for the printable Lucas square generator."""

import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from lucas_squares import (
    TARGET_RATIO,
    bounds,
    choose_squares,
    filler_rectangles,
    layout_score,
    lucas_numbers,
    render_svg,
)


class LucasSquareTests(unittest.TestCase):
    def test_sequence_and_count_validation(self):
        self.assertEqual(lucas_numbers(1), [2])
        self.assertEqual(lucas_numbers(8), [2, 1, 3, 4, 7, 11, 18, 29])
        with self.assertRaises(ValueError):
            lucas_numbers(0)
        with self.assertRaises(ValueError):
            lucas_numbers(71)

    def test_layouts_are_nonoverlapping_and_squares_keep_their_sides(self):
        for layout in ("turning", "fit"):
            for count in range(1, 18):
                with self.subTest(layout=layout, count=count):
                    squares = choose_squares(count, layout, "exact")
                    self.assertEqual([s.size for s in squares], lucas_numbers(count))
                    width, height = bounds(squares)
                    self.assertGreaterEqual(width, height)
                    for s in squares:
                        self.assertGreaterEqual(s.x, 0)
                        self.assertGreaterEqual(s.y, 0)
                        self.assertLessEqual(s.x + s.size, width)
                        self.assertLessEqual(s.y + s.size, height)
                    for i, first in enumerate(squares):
                        for second in squares[i + 1 :]:
                            overlap = (
                                first.x < second.x + second.size
                                and second.x < first.x + first.size
                                and first.y < second.y + second.size
                                and second.y < first.y + first.size
                            )
                            self.assertFalse(overlap, (layout, count, first, second))

    def test_auto_finds_best_count_within_limit(self):
        for layout in ("turning", "fit"):
            selected = choose_squares(12, layout, "auto")
            candidates = [choose_squares(i, layout, "exact") for i in range(1, 13)]
            self.assertEqual(
                selected,
                min(
                    candidates,
                    key=lambda squares: (*layout_score(squares), -len(squares)),
                ),
            )
            self.assertLessEqual(
                layout_score(selected)[0], layout_score(candidates[-1])[0]
            )
            self.assertAlmostEqual(TARGET_RATIO, 4 / 3)

    def test_turning_squares_share_an_edge_with_preceding_square(self):
        squares = choose_squares(18, "turning", "exact")
        for previous, current in zip(squares, squares[1:]):
            horizontal_contact = (
                previous.x + previous.size == current.x
                or current.x + current.size == previous.x
            ) and max(previous.y, current.y) < min(
                previous.y + previous.size, current.y + current.size
            )
            vertical_contact = (
                previous.y + previous.size == current.y
                or current.y + current.size == previous.y
            ) and max(previous.x, current.x) < min(
                previous.x + previous.size, current.x + current.size
            )
            self.assertTrue(horizontal_contact or vertical_contact, (previous, current))

    def test_fillers_cover_only_unoccupied_area(self):
        for layout in ("turning", "fit"):
            for count in (1, 2, 4, 8, 12):
                with self.subTest(layout=layout, count=count):
                    squares = choose_squares(count, layout, "exact")
                    width, height = bounds(squares)
                    fillers = filler_rectangles(squares)
                    self.assertEqual(
                        sum(w * h for _, _, w, h in fillers),
                        width * height - sum(s.size**2 for s in squares),
                    )
                    for i, (x, y, w, h) in enumerate(fillers):
                        self.assertTrue(0 <= x < x + w <= width)
                        self.assertTrue(0 <= y < y + h <= height)
                        others = [(s.x, s.y, s.size, s.size) for s in squares]
                        others += fillers[i + 1 :]
                        for ox, oy, ow, oh in others:
                            self.assertFalse(
                                x < ox + ow
                                and ox < x + w
                                and y < oy + oh
                                and oy < y + h
                            )

    def test_svg_physical_size_squares_and_optional_labels(self):
        squares = choose_squares(5, "turning", "exact")
        ns = "{http://www.w3.org/2000/svg}"
        for labeled in (False, True):
            for alignment in ("seamless", "edges"):
                root = ET.fromstring(render_svg(squares, labeled, alignment))
                self.assertEqual(
                    (root.attrib["width"], root.attrib["height"]), ("12in", "9in")
                )
                self.assertEqual(root.attrib["viewBox"], "0 0 1200 900")
                geometry = root.find(f"{ns}g")
                self.assertIsNotNone(geometry)
                assert geometry is not None
                self.assertIn("scale(", geometry.attrib["transform"])
                lucas = geometry.find(f"{ns}g[@id='lucas']")
                assert lucas is not None
                self.assertEqual(len(lucas.findall(f"{ns}rect")), len(squares))
                self.assertEqual(lucas[0].attrib["width"], str(squares[0].size))
                fillers = geometry.find(f"{ns}g[@id='fillers']")
                self.assertEqual(fillers is not None, alignment == "seamless")
                if fillers is not None:
                    self.assertEqual(
                        len(fillers.findall(f"{ns}rect")),
                        len(filler_rectangles(squares)),
                    )
                self.assertEqual(bool(root.findall(f"{ns}text")), labeled)
                self.assertFalse(root.findall(f".//{ns}path"))

    def test_cli_writes_svg_and_reports_selected_count(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "art.svg"
            result = subprocess.run(
                [
                    sys.executable,
                    str(Path(__file__).with_name("lucas_squares.py")),
                    "--iterations",
                    "6",
                    "--layout",
                    "fit",
                    "--count-mode",
                    "auto",
                    "--alignment",
                    "edges",
                    "--labels",
                    "--output",
                    str(output),
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertIn("squares; footprint", result.stdout)
            ET.parse(output)

    def test_maximum_iterations_keep_nonzero_svg_scale(self):
        root = ET.fromstring(render_svg(choose_squares(70, "turning", "exact")))
        geometry = root.find("{http://www.w3.org/2000/svg}g")
        self.assertIsNotNone(geometry)
        assert geometry is not None
        transform = geometry.attrib["transform"]
        self.assertGreater(float(transform.split("scale(")[1].split(")")[0]), 0)


if __name__ == "__main__":
    unittest.main()
