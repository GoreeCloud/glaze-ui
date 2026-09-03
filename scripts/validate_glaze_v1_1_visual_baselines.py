#!/usr/bin/env python3
"""Validate V1.1 rendered output against the human-approved source-pinned baseline."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "contracts" / "v1.1" / "visual-regression-baseline.rc.json"
ARTIFACTS = ROOT / "artifacts"


def main() -> int:
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    errors: list[str] = []

    if baseline.get("status") != "human-approved-source-pinned-baseline":
        errors.append("visual baseline is not human-approved and source-pinned")
    if baseline.get("approvedVisualSourceRevision") != "8ea1f789bbabf943c3359514dc1506b24fa3c51b":
        errors.append("approved visual source revision drifted")
    if baseline.get("releaseBoundary", {}).get("newOpticalPixelsRequireNewHumanApproval") is not True:
        errors.append("visual baseline must require new human approval for new optical pixels")

    cases = baseline.get("cases", {})
    if len(cases) != 5:
        errors.append(f"expected 5 baseline cases, found {len(cases)}")

    for filename, expected in cases.items():
        path = ARTIFACTS / filename
        if not path.is_file():
            errors.append(f"missing rendered baseline case: {filename}")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            errors.append(f"visual regression for {filename}: expected {expected}, got {actual}")

    if errors:
        print("GLAZE UI V1.1 visual regression baseline FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("GLAZE UI V1.1 human-approved source-pinned visual baseline: PASS")
    print(f"Approved visual source: {baseline['approvedVisualSourceRevision']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
