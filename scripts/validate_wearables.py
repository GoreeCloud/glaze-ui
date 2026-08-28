#!/usr/bin/env python3
"""Validate wearable lifecycle separation and Glaze UI 2.0 Candidate mapping."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "WEARABLES.md"
COMPONENTS = ROOT / "WEARABLE_COMPONENTS.md"
CANDIDATE_TOKENS = ROOT / "tokens" / "glaze-2.candidate.json"
CANDIDATE_CSS = ROOT / "css" / "glaze-2.emerging.candidate.css"
CANDIDATE_RUNTIME = ROOT / "js" / "glaze-2.emerging.candidate.js"
CANDIDATE_REFERENCE = ROOT / "reference" / "candidate-2.0-emerging.html"
CANDIDATE_VALIDATOR = ROOT / "scripts" / "validate_candidate_2_emerging.py"
LEGACY_TOKENS = ROOT / "tokens" / "wearable.candidate.tokens.json"
LEGACY_CSS = ROOT / "css" / "glaze.wearable.candidate.css"
LEGACY_REFERENCE = ROOT / "reference" / "wearable-candidate.html"
LEGACY_EVIDENCE = ROOT / "acceptance" / "wearable-native-evidence.template.json"
WEAR_OS_REFERENCE = ROOT / "reference" / "native" / "wear-os"
WATCH_OS_REFERENCE = ROOT / "reference" / "native" / "watchos"
WEAR_OS_WORKFLOW = ROOT / ".github" / "workflows" / "wear-os-emulator.yml"
STABLE_CSS = ROOT / "css" / "glaze.css"
CORE_CANDIDATE_CSS = ROOT / "css" / "glaze-2.candidate.css"
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()


def fail(message: str) -> None:
    raise SystemExit(f"wearable lifecycle validation failed: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def require_phrases(path: Path, phrases: tuple[str, ...], label: str) -> None:
    text = path.read_text(encoding="utf-8")
    for phrase in phrases:
        require(phrase in text, f"{label} missing: {phrase}")


def main() -> None:
    required = (
        DOC, COMPONENTS, CANDIDATE_TOKENS, CANDIDATE_CSS, CANDIDATE_RUNTIME,
        CANDIDATE_REFERENCE, CANDIDATE_VALIDATOR, LEGACY_TOKENS, LEGACY_CSS,
        LEGACY_REFERENCE, LEGACY_EVIDENCE, WEAR_OS_WORKFLOW, STABLE_CSS,
        CORE_CANDIDATE_CSS,
    )
    for path in required:
        require(path.exists(), f"required artifact missing: {path.relative_to(ROOT)}")
    require(WEAR_OS_REFERENCE.is_dir(), "historical Wear OS reference directory missing")
    require(WATCH_OS_REFERENCE.is_dir(), "historical watchOS reference directory missing")

    require(VERSION == "1.6.0", "last validated Stable baseline must remain 1.6.0 while 2.0 is Candidate")

    require_phrases(DOC, (
        "Current enforced active-development design contract: **Glaze UI 2.0.0 Candidate**",
        "Last validated Stable implementation baseline: **Glaze UI 1.6.0**",
        "compact rotational navigation",
        "not a shrunken phone UI",
        "must not be reinterpreted as Glaze UI 2.0 native acceptance",
        "does not claim that a Wear OS crown, watchOS Digital Crown",
        "Neither validator certifies a physical wearable device",
    ), "WEARABLES.md")

    require_phrases(COMPONENTS, (
        "Glaze UI 2.0.0 Candidate is the enforced active-development contract",
        "rendered** interactive region below that floor",
        "Exactly one rotational-navigation item should be current/focusable at a time",
        "Canvas / Surface / Soft Glaze / Glaze / Deep Glaze / Live Glaze",
        "historical evidence only",
        "representative real-device operation",
    ), "WEARABLE_COMPONENTS.md")

    data = json.loads(CANDIDATE_TOKENS.read_text(encoding="utf-8"))
    meta = data.get("meta", {})
    require(meta.get("version") == "2.0.0", "2.0 wearable mapping must bind Candidate version 2.0.0")
    require(meta.get("status") == "Candidate", "2.0 wearable mapping must remain Candidate before promotion")
    require(meta.get("productionEligible") is False, "2.0 Candidate must remain production-ineligible")
    nav = data.get("layout", {}).get("navigationTransform", {})
    require(nav.get("wearable") == "compact-rotational-navigation", "2.0 wearable navigation transform drifted")
    require(nav.get("spatial") == "floating-control-surface", "2.0 spatial transform drifted")

    candidate_css = CANDIDATE_CSS.read_text(encoding="utf-8")
    for marker in (
        "--glaze-wearable-target: 48px",
        "--glaze-spatial-target: 56px",
        ".glaze-wearable-rotary-nav",
        ".glaze-spatial-stage",
        "prefers-reduced-motion",
        "forced-colors",
        "@supports not (transform-style: preserve-3d)",
    ):
        require(marker in candidate_css, f"2.0 emerging Candidate CSS missing: {marker}")

    runtime = CANDIDATE_RUNTIME.read_text(encoding="utf-8")
    for marker in ("bindRotaryNavigation", "setRotarySelection", "setSpatialDepth", "setSpatialFlat"):
        require(marker in runtime, f"2.0 emerging Candidate runtime missing: {marker}")

    reference = CANDIDATE_REFERENCE.read_text(encoding="utf-8")
    require("GlazeUI2Emerging.bindRotaryNavigation" in reference, "2.0 wearable reference is not bound to the emerging runtime")
    require("GlazeUI2Emerging.setSpatialFlat" in reference, "2.0 spatial flat fallback is not bound")

    legacy = json.loads(LEGACY_TOKENS.read_text(encoding="utf-8"))
    require(legacy.get("glaze", {}).get("wearableCandidate", {}).get("status", {}).get("$value") == "development-candidate", "historical wearable token package must preserve its Development Candidate evidence state")

    stable_css = STABLE_CSS.read_text(encoding="utf-8")
    core_candidate_css = CORE_CANDIDATE_CSS.read_text(encoding="utf-8")
    require("glaze.wearable.candidate.css" not in stable_css, "historical wearable Candidate CSS must not be imported by Stable 1.6 CSS")
    require("glaze.wearable.candidate.css" not in core_candidate_css, "historical 1.x wearable Candidate CSS must not be imported by Glaze UI 2.0 core Candidate CSS")

    workflow = WEAR_OS_WORKFLOW.read_text(encoding="utf-8")
    require("workflow_dispatch" in workflow, "historical Wear OS emulator workflow must remain explicitly manual")
    require("Deferred Manual Validation" in workflow, "historical Wear OS workflow must advertise its deferred/manual boundary")

    evidence = json.loads(LEGACY_EVIDENCE.read_text(encoding="utf-8"))
    require(evidence.get("status") == "template-only", "historical native evidence template must remain template-only")
    require(evidence.get("promotion", {}).get("stableEligible") is False, "historical native evidence template must remain promotion-ineligible")

    print("Glaze UI wearable lifecycle validated: 2.0 Candidate mapping active, 1.6 Stable retained, historical 1.x native evidence isolated, no native-device certification claimed")


if __name__ == "__main__":
    main()
