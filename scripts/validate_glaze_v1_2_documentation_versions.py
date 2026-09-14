#!/usr/bin/env python3
"""Audit current Glaze UI lifecycle/version language across active front-door documents.

Historical release records may preserve language that was true when published. Current guidance,
however, must derive its authority from VERSION and registry/lifecycle.json rather than from a
hardcoded release number. The filename is retained for compatibility with existing workflow and
script references; the validator itself is current-version neutral.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LIFECYCLE = ROOT / "registry" / "lifecycle.json"
VERSION = ROOT / "VERSION"

CURRENT_AUTHORITY_DOCS = {
    "README.md": ("current Official", "Stable"),
    "CONTRIBUTING.md": ("current Official Stable",),
    "CONFORMANCE.md": ("current Official Stable", "conformance target"),
    "ACCEPTANCE.md": ("current Official Stable",),
    "ADOPTION.md": ("current Glaze UI adoption target",),
    "ENFORCEMENT.md": ("current Glaze UI enforcement",),
    "CONSUMERS.md": ("required target",),
    "website/README.md": ("current Official Stable",),
    "GLAZE_UI_V1_4.md": ("Official Stable",),
}

HISTORICAL_RELEASE_DOCS = (
    "GLAZE_UI_V1_0.md",
    "GLAZE_UI_V1_1.md",
    "GLAZE_UI_V1_1_CANDIDATE.md",
    "GLAZE_UI_V1_2.md",
    "GLAZE_UI_V1_2_CANDIDATE.md",
    "GLAZE_UI_V1_3.md",
)

STRONG_CURRENT_CLAIMS = (
    "current official",
    "current stable",
    "current product",
    "current application target",
    "current adoption target",
    "current conformance target",
    "current target",
    "current glaze ui",
)
HISTORICAL_QUALIFIERS = (
    "historical",
    "previous",
    "prior",
    "rollback",
    "superseded",
    "at publication",
    "at the time",
    "then-current",
    "not current",
    "does not override",
)


def fail(message: str) -> None:
    raise SystemExit(f"lifecycle-version-integrity: {message}")


def read_text(relative: str) -> str:
    path = ROOT / relative
    if not path.is_file():
        fail(f"required file missing: {relative}")
    return path.read_text(encoding="utf-8")


def release_for(lifecycle: dict[str, Any], version: str) -> dict[str, Any]:
    for release in lifecycle.get("releases", []):
        if isinstance(release, dict) and release.get("version") == version:
            return release
    fail(f"lifecycle release record missing for {version}")
    raise AssertionError("unreachable")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    lifecycle = json.loads(LIFECYCLE.read_text(encoding="utf-8"))
    version = VERSION.read_text(encoding="utf-8").strip()
    current_official = lifecycle.get("currentOfficial")
    current_stable = lifecycle.get("currentStable")

    if current_stable != version or current_official != version:
        fail("VERSION, currentStable, and currentOfficial must identify the same current Stable release")

    current_release = release_for(lifecycle, version)
    if current_release.get("status") != "stable" or current_release.get("consumerEligible") is not True:
        fail("current lifecycle release must be Stable and consumer-eligible")

    current_label = current_release.get("label")
    if not isinstance(current_label, str) or not current_label:
        fail("current Stable release label is missing")
    if lifecycle.get("officialProductLabel") != current_label:
        fail("officialProductLabel must match the current Stable release label")

    rollback_version = current_release.get("stableBaseline")
    if rollback_version is not None:
        rollback = release_for(lifecycle, rollback_version)
        if rollback.get("status") != "stable":
            fail(f"current rollback baseline {rollback_version} must remain recorded as Stable")

    historical_v12 = release_for(lifecycle, "1.2.0")
    if historical_v12.get("status") != "stable" or historical_v12.get("consumerEligible") is not True:
        fail("historical V1.2 release provenance must remain intact")

    older_markers: set[str] = set()
    for release in lifecycle.get("releases", []):
        if not isinstance(release, dict) or release.get("version") == version:
            continue
        release_version = release.get("version")
        release_label = release.get("label")
        if isinstance(release_version, str):
            older_markers.add(release_version.lower())
        if isinstance(release_label, str):
            older_markers.add(release_label.lower())

    stale_findings: list[dict[str, Any]] = []
    for relative, required_phrases in CURRENT_AUTHORITY_DOCS.items():
        text = read_text(relative)
        lowered_text = text.lower()
        if version.lower() not in lowered_text and current_label.lower() not in lowered_text:
            fail(f"{relative} does not identify current Stable authority {current_label} / {version}")
        for phrase in required_phrases:
            if phrase.lower() not in lowered_text:
                fail(f"{relative} missing lifecycle phrase {phrase!r}")

        for line_number, line in enumerate(text.splitlines(), start=1):
            lowered = line.lower()
            if not any(claim in lowered for claim in STRONG_CURRENT_CLAIMS):
                continue
            if not any(marker in lowered for marker in older_markers):
                continue
            if any(qualifier in lowered for qualifier in HISTORICAL_QUALIFIERS):
                continue
            stale_findings.append({"path": relative, "line": line_number, "text": line.strip()[:240]})

    if stale_findings:
        preview = "; ".join(f"{item['path']}:{item['line']} {item['text']}" for item in stale_findings[:20])
        fail(f"obsolete lifecycle/version authority language found in current guidance: {preview}")

    missing_history = [relative for relative in HISTORICAL_RELEASE_DOCS if not (ROOT / relative).is_file()]
    if missing_history:
        fail(f"historical release documentation missing: {', '.join(missing_history)}")

    report = {
        "schemaVersion": 7,
        "status": "pass",
        "currentOfficial": current_official,
        "currentStable": current_stable,
        "currentStableLabel": current_label,
        "activeCandidate": lifecycle.get("activeCandidate"),
        "plannedNext": lifecycle.get("plannedNext"),
        "rollbackBaseline": rollback_version,
        "currentAuthorityDocuments": sorted(CURRENT_AUTHORITY_DOCS),
        "historicalReleaseDocumentsPreserved": list(HISTORICAL_RELEASE_DOCS),
        "obsoleteLifecycleAuthorityFindings": 0,
        "scopeRule": "Current front-door guidance follows VERSION and registry/lifecycle.json; historical release records remain provenance and may preserve publication-era language.",
        "promotionRule": "A future Stable promotion must update current lifecycle authority and active guidance atomically rather than hardcoding this validator to a release number.",
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else ROOT / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
