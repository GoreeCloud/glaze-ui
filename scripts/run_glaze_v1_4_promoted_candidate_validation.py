#!/usr/bin/env python3
"""Validate preserved V1.4 candidate artifacts after their promotion into Stable V1.4.

Several V1.4 source-candidate validators intentionally encode the repository-wide
lifecycle that existed while the artifacts were candidates: VERSION=1.3.0. The
artifacts themselves remain immutable historical promotion inputs, but the repository
is now officially Stable at 1.4.0.

This runner proves the current V1.4 Stable authority first, supplies the old VERSION
value only while an allowlisted historical candidate validator executes, restores the
exact Stable VERSION bytes in a finally block, and proves Stable authority again. It
therefore cannot turn candidate metadata into lifecycle authority or conceal a drift in
the current Stable release record.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = ROOT / "VERSION"
STABLE_AUTHORITY = ROOT / "scripts" / "validate_glaze_v1_4_stable_authority.py"
CURRENT_VERSION = "1.4.0"
HISTORICAL_CANDIDATE_BASELINE = "1.3.0"

ALLOWED_VALIDATORS = {
    "semantic-optical-runtime": ROOT / "scripts" / "validate_glaze_v1_4_semantic_optical_runtime.py",
    "browser-capabilities": ROOT / "scripts" / "validate_glaze_v1_4_browser_capabilities.py",
    "accessibility-composition": ROOT / "scripts" / "validate_glaze_v1_4_accessibility_composition.py",
    "accessibility-qualification": ROOT / "scripts" / "validate_glaze_v1_4_accessibility_qualification.py",
}


def fail(message: str) -> None:
    raise SystemExit(f"V1.4 promoted-candidate compatibility validation failed: {message}")


def run(path: Path) -> None:
    subprocess.run([sys.executable, str(path)], cwd=ROOT, check=True)


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in ALLOWED_VALIDATORS:
        allowed = ", ".join(sorted(ALLOWED_VALIDATORS))
        fail(f"usage: {Path(sys.argv[0]).name} <{allowed}>")

    original = VERSION.read_text(encoding="utf-8")
    if original.strip() != CURRENT_VERSION:
        fail(f"current VERSION must be {CURRENT_VERSION}, got {original.strip()!r}")

    # Prove that 1.4.0 is genuinely the repository's current Stable authority before
    # supplying any historical candidate-era context.
    run(STABLE_AUTHORITY)

    validator = ALLOWED_VALIDATORS[sys.argv[1]]
    try:
        VERSION.write_text(HISTORICAL_CANDIDATE_BASELINE + "\n", encoding="utf-8")
        run(validator)
    finally:
        VERSION.write_text(original, encoding="utf-8")

    restored = VERSION.read_text(encoding="utf-8")
    if restored != original:
        fail("VERSION was not restored byte-for-byte")

    # Re-prove current Stable authority after restoration so a passing legacy
    # validator can never substitute for the actual V1.4 release boundary.
    run(STABLE_AUTHORITY)

    print(
        f"Historical {sys.argv[1]} candidate artifact validation: PASS; "
        "current GLAZE UI V1.4 Stable authority restored and revalidated."
    )


if __name__ == "__main__":
    main()
