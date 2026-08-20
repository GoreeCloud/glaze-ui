#!/usr/bin/env python3
"""Build a deterministic unsigned Firefox theme package for local testing."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEME_DIR = ROOT / "theme"
MANIFEST = THEME_DIR / "manifest.json"
DEFAULT_DIST = ROOT / "dist"
FIXED_ZIP_TIME = (2020, 1, 1, 0, 0, 0)


def canonical_manifest_bytes() -> bytes:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return (json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def build(output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    version = manifest["version"]
    package = output_dir / f"glaze-ui-firefox-{version}.xpi"
    digest_file = package.with_suffix(package.suffix + ".sha256")

    info = zipfile.ZipInfo("manifest.json", date_time=FIXED_ZIP_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    info.create_system = 3

    with zipfile.ZipFile(package, "w") as archive:
        archive.writestr(info, canonical_manifest_bytes())

    digest = hashlib.sha256(package.read_bytes()).hexdigest()
    digest_file.write_text(f"{digest}  {package.name}\n", encoding="utf-8")
    return package, digest_file


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_DIST)
    args = parser.parse_args()
    package, digest = build(args.output_dir)
    print(package)
    print(digest)


if __name__ == "__main__":
    main()
