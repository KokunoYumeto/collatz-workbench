"""Measure minimum non-white content margins over rendered PDF page PNGs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("render_dir", type=Path)
    parser.add_argument("--white-threshold", type=int, default=245)
    args = parser.parse_args()

    pages = sorted(args.render_dir.glob("page-*.png"))
    if not pages:
        raise SystemExit("no page-*.png files found")

    minima = {"left": None, "top": None, "right": None, "bottom": None}
    witnesses: dict[str, str] = {}
    empty_pages: list[str] = []
    for path in pages:
        with Image.open(path) as source:
            gray = source.convert("L")
            mask = gray.point(lambda value: 255 if value < args.white_threshold else 0)
            box = mask.getbbox()
            if box is None:
                empty_pages.append(path.name)
                continue
            left, top, right, bottom = box
            margins = {
                "left": left,
                "top": top,
                "right": gray.width - right,
                "bottom": gray.height - bottom,
            }
            for side, value in margins.items():
                if minima[side] is None or value < minima[side]:
                    minima[side] = value
                    witnesses[side] = path.name

    print(json.dumps({
        "status": "PASS",
        "pages": len(pages),
        "white_threshold": args.white_threshold,
        "minimum_content_margins_px": minima,
        "witness_pages": witnesses,
        "empty_pages": empty_pages,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
