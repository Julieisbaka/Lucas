# Printable Lucas squares

Create a 12 × 9-inch (landscape) SVG of squares whose side lengths follow the Lucas sequence **2, 1, 3, 4, 7, 11, …**. No spiral curve is drawn. Python 3 is the only requirement.

From this folder, run `python lucas_squares.py --iterations 8`. This writes `lucas_squares.svg`; open it in a browser or vector editor and print at **100% / actual size** on 12 × 9-inch paper (disable “fit to page”). The page has a small white margin. The outlines are black and the background is white.

Options:

- `--iterations N`: number of squares, starting with 2; valid values are 1–70 (default: 8).
- `--count-mode exact|auto`: `exact` always draws N squares (default). `auto` tries counts from 1 through N and chooses the arrangement with an enclosing width:height ratio closest to **12:9 (4:3)**; ties favor less empty area, then more squares. The command prints the chosen count and ratio.
- `--layout turning|fit`: `turning` places squares around the outer edge in the familiar outward-turning arrangement (default). `fit` rearranges the squares into rows and searches for a footprint closer to the page ratio. Neither layout draws an arc.
- `--labels`: add Lucas numbers inside squares large enough for legible text; omitted by default.
- `--output FILE`: SVG filename (default: `lucas_squares.svg`).

For example, `python lucas_squares.py --iterations 12 --count-mode auto --layout fit --labels --output fitted.svg` tries up to twelve squares with row packing and prints their numbers.

**Note:** The reported ratio describes the *bounding footprint* of the squares, not the ratio of each square or the whole page. Lucas squares need not fill that footprint perfectly: white gaps are normal. The drawing is uniformly scaled and centered, never stretched, so all squares remain squares even when the footprint differs from 4:3. Auto mode may select fewer than N squares when an early count matches the paper better.

Run the checks with `python -m unittest discover`.
