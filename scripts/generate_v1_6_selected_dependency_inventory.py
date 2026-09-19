#!/usr/bin/env python3
"""Generate an OSV custom lockfile from Gradle's resolved dependency reports.

The V1.6 security experiment deliberately distinguishes dependency versions
selected by Gradle from requested coordinates retained in verification metadata.
OSV recommends resolved lockfiles/inventories when determining the dependency
versions selected for an environment.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

COORDINATE = re.compile(
    r"([A-Za-z0-9_.-]+):([A-Za-z0-9_.-]+):([^\s]+)(?:\s+->\s+([^\s]+))?"
)


class InventoryError(RuntimeError):
    pass


def parse_report(path: Path) -> dict[tuple[str, str], str]:
    if not path.is_file():
        raise InventoryError(f"missing Gradle dependency report: {path}")
    selected: dict[tuple[str, str], str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        match = COORDINATE.search(raw)
        if not match:
            continue
        group, artifact, requested, resolved = match.groups()

        # Gradle marks pure dependency constraints with "(c)". A constraint is
        # not itself a selected component unless another non-constraint line
        # resolves the component, so do not manufacture a package from it.
        if resolved is None and raw.rstrip().endswith("(c)"):
            continue

        version = resolved or requested
        if not version or version.startswith("("):
            continue
        selected[(group, artifact)] = version
    if not selected:
        raise InventoryError(f"no selected Maven dependencies parsed from {path}")
    return selected


def self_check() -> None:
    cases = {
        "org.example:plain:1.2.3": ("org.example", "plain", "1.2.3", None),
        "org.example:resolved:1.0 -> 2.0": ("org.example", "resolved", "1.0", "2.0"),
        "org.example:repeat:3.0 (*)": ("org.example", "repeat", "3.0", None),
        "org.example:constraint:4.0 (c)": ("org.example", "constraint", "4.0", None),
    }
    for text, expected in cases.items():
        match = COORDINATE.search(text)
        if match is None or match.groups() != expected:
            raise InventoryError(
                f"coordinate parser self-check failed for {text!r}: "
                f"{None if match is None else match.groups()!r} != {expected!r}"
            )


def main() -> int:
    self_check()
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", action="append", nargs=3, metavar=("NAME", "BUILD_ENV", "RUNTIME"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    results = []
    summary_projects = []
    all_coordinates: set[str] = set()

    for name, build_env, runtime in args.project:
        merged: dict[tuple[str, str], str] = {}
        sources = []
        for scope, filename in (("buildscript", build_env), ("runtime", runtime)):
            deps = parse_report(Path(filename))
            sources.append({"scope": scope, "path": filename, "selectedCount": len(deps)})
            merged.update(deps)

        coordinates = [
            f"{group}:{artifact}:{version}"
            for (group, artifact), version in sorted(merged.items())
        ]
        all_coordinates.update(coordinates)
        results.append({
            "source": {"path": name, "type": "gradle-resolved-selection"},
            "packages": [
                {
                    "package": {
                        "name": f"{group}:{artifact}",
                        "version": version,
                        "ecosystem": "Maven",
                    }
                }
                for (group, artifact), version in sorted(merged.items())
            ],
        })
        summary_projects.append({
            "project": name,
            "sources": sources,
            "selectedCoordinates": coordinates,
            "selectedCoordinateCount": len(coordinates),
        })

    args.output.write_text(json.dumps({"results": results}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.summary.write_text(
        json.dumps(
            {
                "schemaVersion": 1,
                "kind": "goreecloud-glaze-v1.6-selected-gradle-dependency-inventory",
                "projects": summary_projects,
                "distinctSelectedCoordinates": sorted(all_coordinates),
                "distinctSelectedCoordinateCount": len(all_coordinates),
                "boundary": (
                    "This inventory is derived from Gradle buildEnvironment and debugRuntimeClasspath "
                    "reports and records selected Maven versions after Gradle conflict resolution. "
                    "It supplements, rather than deletes, the broader verification-metadata scan."
                ),
            },
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )
    print(f"selected-dependency-inventory: {len(all_coordinates)} distinct Maven coordinates")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except InventoryError as error:
        print(f"FAIL: {error}")
        raise SystemExit(1)
