# Printable Lucas squares

Create a 12 × 9-inch (landscape) SVG of squares whose side lengths follow the Lucas sequence **2, 1, 3, 4, 7, 11, …**. No spiral curve is drawn. Python 3 is the only requirement.

From this folder, run `python lucas_squares.py --iterations 8`. This writes `lucas_squares.svg`; open it in a browser or vector editor and print at **100% / actual size** on 12 × 9-inch paper (disable “fit to page”). The page has a small white margin. Lucas-square outlines are black; the optional filler shapes are light gray.

Options:

- `--iterations N`: number of squares, starting with 2; valid values are 1–70 by default (default: 8).
- `--max-iterations N` (also `--override-max-iterations N`): change the 70-square safety limit when you need more or fewer squares. For example, use `--iterations 80 --max-iterations 80`. Higher values create extremely large Lucas numbers and can make the SVG slow to generate or render.
- `--count-mode exact|auto`: `exact` always draws N squares (default). `auto` tries counts from 1 through N and chooses the arrangement with an enclosing width:height ratio closest to **12:9 (4:3)**; ties favor less empty area, then more squares. The command prints the chosen count and ratio.
- `--layout turning|fit`: `turning` places squares around the outer edge in the familiar outward-turning arrangement (default). `fit` rearranges the squares into rows and searches for a footprint closer to the page ratio. Neither layout draws an arc.
- `--alignment seamless|edges`: `seamless` (default) fills all unused space *inside the square arrangement's enclosing rectangle* with light-gray filler rectangles, leaving no gaps in the footprint. `edges` draws only Lucas square outlines; blank spaces remain. In both modes all square edges use one shared coordinate system, so touching edges line up exactly.
- `--width INCHES` and `--height INCHES`: printed page dimensions (defaults: `12` and `9`). Decimals are accepted, so US Letter portrait is `--width 8.5 --height 11`. Only their ratio affects layout; use any consistent shared unit for scaling.
- `--margin VALUE`: white margin in the same unit as `--width` and `--height` (default: `0.45`). It must be non-negative and leave printable space on both axes.
- `--svg-units-per-inch N`: number of internal SVG viewBox units per printed inch (default: `100`). This changes SVG coordinate resolution, not the printed page size or square proportions.
- `--labels`: add Lucas numbers inside squares large enough for legible text; omitted by default.
- `--output FILE`: SVG filename (default: `lucas_squares.svg`).

For example, `python lucas_squares.py --iterations 12 --count-mode auto --layout fit --width 8.5 --height 11 --labels --output fitted.svg` tries up to twelve squares with row packing for US Letter portrait and prints their numbers.

**Note:** The reported ratio describes the *bounding footprint* of the squares, not the ratio of each square or the whole page. Lucas squares alone need not tile a rectangle, so a seamless footprint requires filler shapes that are **not** Lucas squares. The drawing is uniformly scaled and centered, never stretched, so all squares remain squares even when the footprint differs from the requested page ratio. Filler shapes cover the footprint, not the white margins of the paper. Auto mode may select fewer than N squares when an early count matches the paper better.

Run the checks with `python -m unittest discover -s tests`.
