#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse

try:
    import cairosvg
except ImportError as exc:
    raise SystemExit("cairosvg is required to generate identity assets") from exc

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "identity" / "official" / "facet"
DEFAULT_OUT = SOURCE / "generated"
MARK_SIZES = (16, 24, 32, 48, 64, 128, 256, 512, 1024)
PROFILE_SIZES = (512, 1024)


def svg_to_png(source: Path, destination: Path, *, width: int, height: int | None = None) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    cairosvg.svg2png(
        url=str(source),
        write_to=str(destination),
        output_width=width,
        output_height=height,
    )


def generate(out: Path) -> None:
    mark = SOURCE / "glaze-ui-mark.svg"

    for size in MARK_SIZES:
        svg_to_png(mark, out / "mark" / f"glaze-ui-mark-{size}.png", width=size, height=size)

    for size in PROFILE_SIZES:
        svg_to_png(mark, out / "profile" / f"glaze-ui-profile-{size}.png", width=size, height=size)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate deterministic Glaze UI Facet identity derivatives.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    generate(args.out)
    print(f"Generated Glaze UI Facet identity assets in {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
