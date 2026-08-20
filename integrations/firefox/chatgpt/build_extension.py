#!/usr/bin/env python3
"""Build a deterministic unsigned Firefox XPI for local GoreeCloud ChatGPT testing."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parent
DEFAULT_OUT = ROOT / "dist" / "goreecloud-glaze-ui-chatgpt.xpi"
FIXED_DATE = (2026, 1, 1, 0, 0, 0)
EXCLUDED_PARTS = {"dist", "__pycache__"}
EXCLUDED_NAMES = {"ACCEPTANCE.md", "README.md", "build_extension.py"}


def package_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if any(part in EXCLUDED_PARTS for part in rel.parts):
            continue
        if rel.as_posix() in EXCLUDED_NAMES:
            continue
        files.append(path)
    return sorted(files, key=lambda p: p.relative_to(ROOT).as_posix())


def canonical_manifest_bytes() -> bytes:
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    return (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def write_member(archive: ZipFile, name: str, data: bytes) -> None:
    info = ZipInfo(name, date_time=FIXED_DATE)
    info.compress_type = ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = 0o644 << 16
    archive.writestr(info, data)


def build(output: Path) -> str:
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w") as archive:
        for path in package_files():
            rel = path.relative_to(ROOT).as_posix()
            data = canonical_manifest_bytes() if rel == "manifest.json" else path.read_bytes()
            write_member(archive, rel, data)

    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(output.suffix + ".sha256").write_text(
        f"{digest}  {output.name}\n", encoding="utf-8"
    )
    return digest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    digest = build(args.output.resolve())
    print(f"built {args.output} sha256={digest}")


if __name__ == "__main__":
    main()
