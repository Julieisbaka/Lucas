# Printable Lucas squares

Generate a printable SVG of squares whose side lengths follow the Lucas sequence **2, 1, 3, 4, 7, 11, …**. The generator never draws a spiral. It needs only Python 3.

By default, it creates an eight-square, 12 × 9-inch landscape SVG named `lucas_squares.svg`:

`python lucas_squares.py --iterations 8`

Open the SVG in a browser or vector editor and print it at **100% / actual size**; disable any “fit to page” print option. Lucas-square outlines are black. Seamless filler shapes, when enabled, are light gray.

## Page size and scale

`--width` and `--height` set the printed SVG dimensions in inches, defaulting to `12` and `9`. Their ratio determines the layout target, so a common scale change preserves the layout. For example, `--width 8.5 --height 11` produces US Letter portrait and makes the `fit` layout seek a portrait footprint.

`--margin` controls the white margin in the same units as the width and height; its default is `0.45`. It must be non-negative, and the width and height must both be greater than twice the margin.

`--svg-units-per-inch` changes only the internal SVG `viewBox` coordinate density, defaulting to `100`. For example, `--svg-units-per-inch 72` produces a 612 × 792 viewBox for an 8.5 × 11-inch page. It does not change the printed size, page ratio, or the squares’ proportions.

## Layout controls

- `--iterations N` — number of Lucas squares to include, starting at `2`; `0` creates a valid blank page and `1` creates only the `2 × 2` Lucas square. Default: `8`.
- `--max-iterations N` or `--override-max-iterations N` — change the default safety ceiling of `70`. To create 80 squares, specify both `--iterations 80 --max-iterations 80`; `--max-iterations 0` permits only a blank page. Large values create enormous Lucas numbers and can make the SVG slow to generate or render.
- `--count-mode exact|auto` — `exact` always draws N squares. `auto` examines every count from 1 through N and chooses the footprint closest to the requested page ratio; ties favor less empty space, then more squares.
- `--layout turning|fit` — `turning` uses the outward-turning arrangement. `fit` packs rows and chooses the footprint closest to the requested page ratio. Neither mode draws an arc.
- `--alignment seamless|edges` — `seamless` fills unused parts of the arrangement’s enclosing rectangle with light-gray filler rectangles. `edges` draws only Lucas squares, leaving unused space blank. Both use shared coordinates, so touching square edges meet exactly.
- `--labels` — show each Lucas value inside a square when there is enough room to read it.
- `--format svg|png|pdf` — output format; default: `svg`. SVG and PDF retain vector lines. PNG is rasterized at the requested DPI.
- `--dpi N` — PNG output resolution in dots per inch; default: `300`. It has no effect on SVG or PDF.
- `--output FILE` — output filename. When omitted, it is `lucas_squares.svg`, `lucas_squares.png`, or `lucas_squares.pdf`, according to `--format`.

## Examples

- A numbered US Letter portrait page with a tight, row-packed arrangement: `python lucas_squares.py --iterations 12 --count-mode auto --layout fit --width 8.5 --height 11 --margin 0.25 --labels --output letter.svg`
- Lucas-square outlines only, without filler shapes: `python lucas_squares.py --iterations 8 --alignment edges --output outlines.svg`
- A 72-unit-per-inch SVG: `python lucas_squares.py --width 8.5 --height 11 --svg-units-per-inch 72 --output letter-72.svg`
- A 300-DPI PNG: `python lucas_squares.py --format png --dpi 300 --output lucas.png`
- A print-ready vector PDF: `python lucas_squares.py --format pdf --output lucas.pdf`

## Notes

The printed page ratio and the squares’ enclosing-footprint ratio are separate. The generator uniformly scales and centers the footprint, never stretches it, so every Lucas shape remains a true square. Lucas squares alone do not necessarily tile a rectangle; the `seamless` option adds non-Lucas filler rectangles only inside the footprint, never in the page margins.

Run the tests with `python -m unittest discover -s tests`.

PNG and PDF export require the packages listed in `requirements.txt`; install them with `python -m pip install -r requirements.txt`.
