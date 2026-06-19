#!/usr/bin/env python3
"""Geometry helper for the carousel skill.

GPT Image 2 makes the pixels; this script does the deterministic parts the
model can't be trusted with: slicing a 3x3 concept board into 9 cells, and
producing an exact 1080x1080 JPG in Facebook's format.

Subcommands
-----------
  split   preview.png  -> cells/cell-1.png .. cell-9.png  (row-major: left-to-
          right, top-to-bottom; numbering matches the table shown to the user)

  fbjpg   slide.png    -> slide-N.jpg  (center-cropped square, resized, JPEG)

Usage
-----
  carousel.py split --in preview.png --out-dir cells/ [--rows 3 --cols 3]
                    [--inset 0.0]
  carousel.py fbjpg --in slide.png --out slide-1.jpg [--size 1080]
                    [--quality 85]

--inset shaves that fraction off every edge of each cell to drop grid
gutters/borders the model draws between tiles. Default 0.015 cleanly clears
GPT Image 2's flush grids; raise toward 0.03 if borders still bleed in.

Exit codes: 0 ok, 2 bad args, 3 PIL missing, 4 input file missing.
"""
import argparse
import os
import sys

try:
    from PIL import Image
except ImportError:
    sys.stderr.write("Pillow (PIL) not installed: pip install Pillow\n")
    sys.exit(3)


def _require_file(path):
    if not os.path.isfile(path):
        sys.stderr.write(f"input file not found: {path}\n")
        sys.exit(4)


def split(args):
    _require_file(args.inp)
    rows, cols = args.rows, args.cols
    if rows < 1 or cols < 1:
        sys.stderr.write("--rows/--cols must be >= 1\n")
        sys.exit(2)
    if not 0.0 <= args.inset < 0.5:
        sys.stderr.write("--inset must be in [0, 0.5)\n")
        sys.exit(2)

    img = Image.open(args.inp)
    W, H = img.size
    cell_w, cell_h = W // cols, H // rows
    os.makedirs(args.out_dir, exist_ok=True)

    written = []
    for r in range(rows):
        for c in range(cols):
            left, top = c * cell_w, r * cell_h
            right, bottom = left + cell_w, top + cell_h
            if args.inset:
                dx, dy = int(cell_w * args.inset), int(cell_h * args.inset)
                left, top, right, bottom = left + dx, top + dy, right - dx, bottom - dy
            n = r * cols + c + 1
            out = os.path.join(args.out_dir, f"cell-{n}.png")
            img.crop((left, top, right, bottom)).save(out)
            written.append(out)
    print("\n".join(written))


def fbjpg(args):
    _require_file(args.inp)
    size, quality = args.size, args.quality
    if size < 1:
        sys.stderr.write("--size must be >= 1\n")
        sys.exit(2)

    img = Image.open(args.inp).convert("RGB")
    W, H = img.size
    side = min(W, H)
    left, top = (W - side) // 2, (H - side) // 2
    img = img.crop((left, top, left + side, top + side))
    if side != size:
        img = img.resize((size, size), Image.LANCZOS)
    img.save(args.out, "JPEG", quality=quality, optimize=True)
    print(args.out)


def main():
    p = argparse.ArgumentParser(prog="carousel.py")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("split", help="slice a grid image into cells")
    sp.add_argument("--in", dest="inp", required=True)
    sp.add_argument("--out-dir", required=True)
    sp.add_argument("--rows", type=int, default=3)
    sp.add_argument("--cols", type=int, default=3)
    sp.add_argument("--inset", type=float, default=0.015)
    sp.set_defaults(func=split)

    fp = sub.add_parser("fbjpg", help="center-crop square + resize to a JPG")
    fp.add_argument("--in", dest="inp", required=True)
    fp.add_argument("--out", required=True)
    fp.add_argument("--size", type=int, default=1080)
    fp.add_argument("--quality", type=int, default=85)
    fp.set_defaults(func=fbjpg)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
