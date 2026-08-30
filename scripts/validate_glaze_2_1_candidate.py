#!/usr/bin/env python3
"""Fail-closed structural validation for the Glaze UI 2.1 Candidate foundation.

This validator intentionally checks objective repository invariants only. Human Visual
Excellence review remains separate evidence and is never manufactured by this script.
"""

from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

ERRORS: list[str] = []
RECOMMENDATIONS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def recommend(message: str) -> None:
    RECOMMENDATIONS.append(message)


def read_text(path: str) -> str:
    target = ROOT / path
    if not target.is_file():
        fail(f"missing required file: {path}")
        return ""
    return target.read_text(encoding="utf-8")


def read_json(path: str) -> dict:
    raw = read_text(path)
    if not raw:
        return {}
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path}: {exc}")
        return {}
    if not isinstance(value, dict):
        fail(f"expected object at top level: {path}")
        return {}
    return value


def require_keys(obj: dict, keys: tuple[str, ...], label: str) -> None:
    for key in keys:
        if key not in obj:
            fail(f"{label} missing required key: {key}")


def main() -> int:
    version = read_text("VERSION").strip()
    if version != "2.0.0":
        fail(f"2.1 Candidate must not change current Stable VERSION; expected 2.0.0, got {version!r}")

    candidate = read_text("GLAZE_UI_2_1_CANDIDATE.md")
    visual = read_text("VISUAL_EXCELLENCE.md")
    registry = read_json("registry/lifecycle.json")
    schema = read_json("schemas/component-contract.schema.json")
    capsule = read_json("contracts/components/navigation-capsule.json")

    candidate_markers = (
        "Status: **Candidate**",
        "2.1.0-candidate.1",
        "Current Stable remains: **2.0.0**",
        "Make interaction feel tangible. Make every interface feel intentional. Make GoreeCloud beautiful.",
        "Visual Excellence",
        "Accessibility Resolution Matrix",
        "Material Budgets",
        "Glaze Recipes",
        "Nothing teleports.",
        "2.0.0 remains the only current Stable Glaze UI consumer target",
    )
    for marker in candidate_markers:
        if marker not in candidate:
            fail(f"Candidate contract missing required marker: {marker}")

    visual_markers = (
        "Objective conformance",
        "Human visual review",
        "Optical correctness",
        "Accessibility-mode beauty",
        "Performance fallback beauty",
        "does not change the current Stable target from 2.0.0",
    )
    for marker in visual_markers:
        if marker not in visual:
            fail(f"Visual Excellence contract missing required marker: {marker}")

    require_keys(registry, ("schemaVersion", "currentStable", "activeCandidate", "lifecycleDefinitions", "releases", "capabilities", "promotionRules"), "lifecycle registry")
    if registry.get("currentStable") != "2.0.0":
        fail("lifecycle registry currentStable must remain 2.0.0")
    if registry.get("activeCandidate") != "2.1.0-candidate.1":
        fail("lifecycle registry activeCandidate must be 2.1.0-candidate.1")

    releases = registry.get("releases", [])
    if not isinstance(releases, list):
        fail("lifecycle registry releases must be an array")
        releases = []
    stable = [r for r in releases if isinstance(r, dict) and r.get("version") == "2.0.0"]
    candidate_release = [r for r in releases if isinstance(r, dict) and r.get("version") == "2.1.0-candidate.1"]
    if len(stable) != 1 or stable[0].get("status") != "stable" or stable[0].get("consumerEligible") is not True:
        fail("registry must contain exactly one consumer-eligible Stable 2.0.0 release")
    if len(candidate_release) != 1 or candidate_release[0].get("status") != "candidate" or candidate_release[0].get("consumerEligible") is not False:
        fail("registry must contain exactly one non-consumer-eligible 2.1.0-candidate.1 release")

    capabilities = registry.get("capabilities", {})
    if not isinstance(capabilities, dict):
        fail("lifecycle registry capabilities must be an object")
        capabilities = {}
    allowed_lifecycles = {"stable", "candidate", "experimental", "planned", "deprecated", "historical"}
    for name, record in capabilities.items():
        if not isinstance(record, dict):
            fail(f"capability {name} must be an object")
            continue
        if record.get("status") not in allowed_lifecycles:
            fail(f"capability {name} has invalid lifecycle status: {record.get('status')!r}")

    for required_candidate in (
        "visual-excellence-gate",
        "canonical-lifecycle-registry",
        "machine-readable-component-contracts",
        "navigation-capsule-2.1",
        "material-budgets",
        "accessibility-resolution-matrix",
        "glaze-recipes",
        "performance-profiles",
        "expanded-conformance-linter",
    ):
        if capabilities.get(required_candidate, {}).get("status") != "candidate":
            fail(f"required 2.1 foundation capability is not Candidate: {required_candidate}")

    if capabilities.get("glaze-motion", {}).get("status") != "experimental":
        fail("Glaze Motion must remain Experimental unless separately promoted")

    rules = registry.get("promotionRules", {})
    if not isinstance(rules, dict):
        fail("promotionRules must be an object")
        rules = {}
    if rules.get("candidateMaySatisfyStableConsumerConformance") is not False:
        fail("Candidate must not satisfy Stable consumer conformance")
    if rules.get("stableVersionFileMustRemain") != "2.0.0":
        fail("promotion rule must pin Stable VERSION to 2.0.0 during Candidate work")
    if rules.get("requiresHumanVisualExcellenceReview") is not True:
        fail("2.1 promotion must require human Visual Excellence review")

    require_keys(schema, ("$schema", "$id", "title", "type", "required", "properties"), "component schema")
    schema_required = set(schema.get("required", [])) if isinstance(schema.get("required"), list) else set()
    contract_required = {
        "schemaVersion", "id", "name", "lifecycle", "semanticRole", "materialRole",
        "geometry", "states", "targets", "input", "accessibility", "density",
        "formFactors", "fallbacks", "visualReview",
    }
    missing_schema_requirements = contract_required - schema_required
    if missing_schema_requirements:
        fail(f"component schema does not require: {sorted(missing_schema_requirements)}")

    require_keys(capsule, tuple(contract_required), "Navigation Capsule contract")
    if capsule.get("lifecycle") != "candidate":
        fail("Navigation Capsule 2.1 contract must remain Candidate")
    materials = capsule.get("materialRole", {})
    if materials.get("default") != "soft-glaze":
        fail("Navigation Capsule default material must be Soft Glaze")
    targets = capsule.get("targets", {})
    if not isinstance(targets.get("touchMinPx"), int) or targets.get("touchMinPx", 0) < 48:
        fail("Navigation Capsule touch target must preserve the 48px Stable floor")
    if not isinstance(targets.get("tvMinPx"), int) or targets.get("tvMinPx", 0) < 56:
        fail("Navigation Capsule TV target must preserve the 56px Stable floor")

    expected_forms = {"mobile", "tablet", "desktop", "wide-desktop", "tv", "foldable", "resizable"}
    forms = set(capsule.get("formFactors", [])) if isinstance(capsule.get("formFactors"), list) else set()
    if not expected_forms.issubset(forms):
        fail(f"Navigation Capsule contract missing form factors: {sorted(expected_forms - forms)}")

    a11y = capsule.get("accessibility", {})
    for key in ("semantics", "reducedMotion", "reducedTransparency", "increasedContrast", "largeText", "forcedColors"):
        if not isinstance(a11y.get(key), str) or not a11y.get(key).strip():
            fail(f"Navigation Capsule accessibility mapping missing: {key}")

    review = capsule.get("visualReview", {})
    if review.get("required") is not True or not review.get("criteria"):
        fail("Navigation Capsule must require non-empty human visual review criteria")

    # These are intentionally recommendations, not deterministic failures.
    recommend("Add rendered 2.1 reference flows before Stable promotion.")
    recommend("Add Accessibility Resolution Matrix fixtures and combination tests before Stable promotion.")
    recommend("Add Material Budget metrics and visual regression coverage before Stable promotion.")
    recommend("Record human Visual Excellence evidence against exact promotion revisions before Stable promotion.")

    if RECOMMENDATIONS:
        print("Glaze UI 2.1 Candidate review recommendations:")
        for item in RECOMMENDATIONS:
            print(f"  - {item}")

    if ERRORS:
        print("Glaze UI 2.1 Candidate validation FAILED:", file=sys.stderr)
        for item in ERRORS:
            print(f"  - {item}", file=sys.stderr)
        return 1

    print("Glaze UI 2.1 Candidate foundation validation passed.")
    print("Current Stable remains 2.0.0; no Stable consumer promotion is implied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
