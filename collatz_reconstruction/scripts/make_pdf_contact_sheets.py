"""Create deterministic labelled contact sheets from rendered PDF page PNGs."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def page_number(path: Path) -> int:
    match = re.search(r"(\d+)$", path.stem)
    if match is None:
        raise ValueError(f"rendered page has no numeric suffix: {path}")
    return int(match.group(1))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--per-sheet", type=int, default=8)
    parser.add_argument("--columns", type=int, default=4)
    parser.add_argument("--thumb-width", type=int, default=480)
    args = parser.parse_args()

    pages = sorted(args.input_dir.glob("*.png"), key=page_number)
    if not pages:
        raise SystemExit("no rendered PNG pages found")
    if args.per_sheet <= 0 or args.columns <= 0:
        raise SystemExit("per-sheet and columns must be positive")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for old in args.output_dir.glob("contact-*.png"):
        old.unlink()

    font = ImageFont.load_default()
    gap = 16
    label_height = 24
    rows = (args.per_sheet + args.columns - 1) // args.columns

    with Image.open(pages[0]) as first:
        thumb_height = round(args.thumb_width * first.height / first.width)

    sheet_width = gap + args.columns * (args.thumb_width + gap)
    sheet_height = gap + rows * (label_height + thumb_height + gap)

    for sheet_index, start in enumerate(range(0, len(pages), args.per_sheet), 1):
        group = pages[start : start + args.per_sheet]
        sheet = Image.new("RGB", (sheet_width, sheet_height), "#303030")
        draw = ImageDraw.Draw(sheet)
        for offset, path in enumerate(group):
            row, column = divmod(offset, args.columns)
            x = gap + column * (args.thumb_width + gap)
            y = gap + row * (label_height + thumb_height + gap)
            label = f"page {page_number(path)}"
            draw.text((x, y + 4), label, fill="white", font=font)
            with Image.open(path) as page:
                thumb = page.convert("RGB")
                thumb.thumbnail((args.thumb_width, thumb_height), Image.Resampling.LANCZOS)
                sheet.paste(thumb, (x, y + label_height))
        target = args.output_dir / f"contact-{sheet_index:02d}.png"
        sheet.save(target, optimize=True)

    print(
        f"pages={len(pages)} sheets={(len(pages) + args.per_sheet - 1) // args.per_sheet} "
        f"columns={args.columns} per_sheet={args.per_sheet}"
    )


if __name__ == "__main__":
    main()
