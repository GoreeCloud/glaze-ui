#!/usr/bin/env python3
"""Fail-closed repository validation for Glaze UI 2.2.0 Stable promotion.

This validator proves promotion-state invariants. Candidate implementation,
rendered, visual-regression, performance, interaction and Android-native gates
remain separate mandatory workflow steps so this file cannot self-certify them.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def req(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Glaze UI 2.2 Stable validation failed: {message}")


def text(path: str) -> str:
    target = ROOT / path
    req(target.is_file(), f"missing required file: {path}")
    return target.read_text(encoding="utf-8")


def data(path: str) -> dict:
    value = json.loads(text(path))
    req(isinstance(value, dict), f"{path} must contain a top-level object")
    return value


def main() -> None:
    version = text("VERSION").strip()
    req(version == "2.2.0", "VERSION must be exactly 2.2.0")

    stable_doc = text("GLAZE_UI_2_2_STABLE.md")
    acceptance = text("acceptance/2.2-stable.md")
    visual_review = text("acceptance/2.2-visual-review.md")
    css_entry = text("css/glaze-2.2.0.css")
    js_entry = text("js/glaze-2.2.0.mjs")

    for marker in (
        "Lifecycle status:** Stable",
        "Stable semantic version:** 2.2.0",
        "Previous Stable implementation baseline:** Glaze UI 2.1.0",
        "0411b0f6dd877aea30e2c5674e1acde0105fd97b",
        "No downstream application is promoted by declaration",
        "Rollback baseline:** 2.1.0",
    ):
        req(marker in stable_doc, f"Stable contract missing marker: {marker}")

    for marker in (
        "2.2.0-candidate.1",
        "7fb817e28a3f6e9d36f55e7af7acb281813d08f4",
        "0411b0f6dd877aea30e2c5674e1acde0105fd97b",
        "48 px",
        "56 px",
        "Human Visual Excellence",
        "rollback",
    ):
        req(marker in acceptance, f"Stable acceptance missing marker: {marker}")

    req("**Decision:** `Accepted`" in visual_review, "human visual decision must be Accepted")
    req("0411b0f6dd877aea30e2c5674e1acde0105fd97b" in visual_review, "visual-review source revision drifted")

    required_css_sources = (
        "glaze-2.2.candidate.css",
        "glaze-2.2.components.candidate.css",
        "glaze-2.2.components.adaptive.candidate.css",
        "glaze-2.2.components.runtime.candidate.css",
        "glaze-2.2.structure.candidate.css",
        "glaze-2.2.overlay.candidate.css",
        "glaze-2.2.advanced.candidate.css",
        "glaze-2.2.visual-refinement.candidate.css",
        "glaze-2.2.optical-reachability.candidate.css",
    )
    for source in required_css_sources:
        req(source in css_entry, f"Stable CSS entrypoint missing promotion source: {source}")
        req((ROOT / "css" / source).is_file(), f"preserved Candidate CSS source missing: {source}")

    for source in ("glaze-2.2.candidate.mjs", "glaze-2.2.system-interactions.candidate.mjs"):
        req(source in js_entry, f"Stable runtime entrypoint missing promotion source: {source}")
        req((ROOT / "js" / source).is_file(), f"preserved Candidate runtime source missing: {source}")

    lifecycle = data("registry/lifecycle.json")
    req(lifecycle.get("currentStable") == version, "lifecycle currentStable must equal VERSION")
    req(lifecycle.get("activeCandidate") is None, "2.2 Stable must not retain an active 2.2 Candidate")
    releases = lifecycle.get("releases", [])
    req(isinstance(releases, list), "lifecycle releases must be an array")
    stable = [r for r in releases if isinstance(r, dict) and r.get("version") == "2.2.0"]
    candidate = [r for r in releases if isinstance(r, dict) and r.get("version") == "2.2.0-candidate.1"]
    previous = [r for r in releases if isinstance(r, dict) and r.get("version") == "2.1.0"]
    req(len(stable) == 1 and stable[0].get("status") == "stable" and stable[0].get("consumerEligible") is True, "2.2.0 Stable release record invalid")
    req(stable[0].get("promotedFromCandidate") == "2.2.0-candidate.1", "Stable promotion source missing")
    req(stable[0].get("rollbackVersion") == "2.1.0", "Stable rollback version must be 2.1.0")
    req(len(candidate) == 1 and candidate[0].get("status") == "historical" and candidate[0].get("consumerEligible") is False and candidate[0].get("promotedTo") == "2.2.0", "2.2 Candidate provenance must be historical and non-consumer-eligible")
    req(len(previous) == 1 and previous[0].get("status") == "historical" and previous[0].get("supersededBy") == "2.2.0", "2.1.0 must be retained as superseded historical Stable")

    capabilities = lifecycle.get("capabilities", {})
    req(isinstance(capabilities, dict), "lifecycle capabilities must be an object")
    for key in (
        "system-shell-runtime-2.2",
        "bounded-component-contract-catalog-2.2",
        "foundation-component-contracts-2.2",
        "structure-component-contracts-2.2",
        "overlay-component-contracts-2.2",
        "signature-component-contracts-2.2",
        "intelligence-component-contracts-2.2",
        "bounded-universal-search-runtime-reference-2.2",
        "bounded-control-center-runtime-reference-2.2",
        "migration-compatibility-assessment-2.2",
        "performance-glaze-budget-evidence-2.2",
        "android-native-reference-2.2",
        "android-handheld-emulator-acceptance-2.2",
        "bounded-source-pinned-visual-regression-2.2",
        "optical-reachability-component-presentation-2.2",
        "stable-validation-2.2",
        "stable-web-entrypoint-2.2",
        "stable-runtime-entrypoint-2.2",
        "consumer-conformance-registry-2.2",
        "visual-regression-2.2",
        "migration-2.1-to-2.2",
    ):
        record = capabilities.get(key)
        req(isinstance(record, dict) and record.get("status") == "stable", f"Stable capability missing or not Stable: {key}")
    req(capabilities.get("glaze-motion", {}).get("status") == "experimental", "Glaze Motion must remain Experimental")

    rules = lifecycle.get("promotionRules", {})
    req(rules.get("stableVersionFileMustRemain") == "2.2.0", "promotion rules must pin Stable version 2.2.0")
    req(rules.get("candidateMaySatisfyStableConsumerConformance") is False, "Candidate must never satisfy Stable consumer conformance")
    req(rules.get("downstreamConsumerAutoPromotionAllowed") is False, "downstream auto-promotion must remain forbidden")
    req(rules.get("rollbackVersion") == "2.1.0", "promotion rules must identify 2.1.0 rollback")
    for key in ("requiresExactFinalRevisionCI","requiresRenderedAcceptance","requiresAccessibilityAndResilienceAcceptance","requiresNativeOrDeviceEvidenceWhereApplicable","requiresHumanVisualExcellenceReview","requiresImmutableReleaseTag"):
        req(rules.get(key) is True, f"promotion rule must require {key}")

    tokens = data("tokens/glaze.tokens.json")
    meta = tokens.get("meta", {})
    contract = tokens.get("currentContract", {})
    req(meta.get("version") == version and meta.get("stableBaseline") == version and meta.get("status") == "Stable", "canonical Stable token metadata must equal VERSION")
    req(meta.get("currentWebLayer") == "css/glaze-2.2.0.css", "canonical token web layer must use the 2.2 Stable entrypoint")
    req(meta.get("currentRuntime") == "js/glaze-2.2.0.mjs", "canonical token runtime must use the 2.2 Stable entrypoint")
    req(meta.get("promotionSource") == "2.2.0-candidate.1", "canonical tokens must preserve Candidate promotion provenance")
    req(meta.get("approvedVisualSource") == "0411b0f6dd877aea30e2c5674e1acde0105fd97b", "canonical tokens must preserve approved visual source")
    req(contract.get("major") == 2 and contract.get("minor") == 2, "canonical token contract version must be 2.2")
    req(contract.get("componentContractCount") == 32, "canonical token contract must record 32 component contracts")
    req(contract.get("systemSurfaceHierarchy") == ["workspace","application","system-overlay","system-panel","critical-system"], "canonical token System Shell hierarchy drifted")
    budget = contract.get("systemGlazeBudget", {})
    req(budget.get("dominantPanelsMax") == 1 and budget.get("smallFloatingControlsMax") == 3 and budget.get("nestedBackdropBlurAllowed") is False, "canonical token System Glaze budget drifted")
    req(contract.get("touchMinimum") == 48 and contract.get("touchAssistanceMinimum") == 56, "canonical token target floors drifted")
    req(contract.get("downstreamConsumerAutoPromotion") is False, "canonical token authority must not auto-promote consumers")

    consumers = data("consumers/registry.json")
    req(consumers.get("stableBaseline") == version, "consumer stableBaseline must be 2.2.0")
    req(consumers.get("requiredConsumerVersion") == version, "consumer required version must be 2.2.0")
    req("2.1.0" in consumers.get("historicalStableVersions", []), "2.1.0 must be a historical consumer baseline")
    for consumer in consumers.get("consumers", []):
        req(consumer.get("requiredTargetVersion") == version, f"{consumer.get('repository')} must target 2.2.0")
        req(consumer.get("productionEligible") is False, f"{consumer.get('repository')} must not auto-promote to production")

    enforcement = data("tokens/enforcement.json")
    req(enforcement.get("meta", {}).get("currentStable") == version, "enforcement authority must be 2.2.0")

    visual = data("contracts/regression/visual-baselines-2.2.json")
    req(visual.get("lifecycle") == "stable", "2.2 visual baseline lifecycle must be Stable")
    req(visual.get("baselineRevision") == "0411b0f6dd877aea30e2c5674e1acde0105fd97b", "approved visual baseline revision drifted")
    req(visual.get("humanVisualExcellenceAccepted") is True and visual.get("humanDecision") == "Accepted", "human visual acceptance is not recorded")
    boundary = visual.get("promotionBoundary", {})
    req(boundary.get("currentStable") == "2.2.0" and boundary.get("stablePromotionAuthorized") is True, "visual promotion boundary is not Stable-authorized")
    req(boundary.get("rollbackVersion") == "2.1.0", "visual promotion boundary rollback drifted")

    for preserved in (
        "GLAZE_UI_2_2_CANDIDATE.md",
        "acceptance/2.2-candidate.md",
        "tokens/glaze-2.2.candidate.json",
        "contracts/system-shell/glaze-system-shell-2.2.json",
        "contracts/migration/glaze-2.1-to-2.2.json",
        "contracts/performance/glaze-2.2-performance-budget.json",
    ):
        req((ROOT / preserved).exists(), f"promotion provenance missing: {preserved}")

    print("Glaze UI 2.2.0 Stable promotion state validated; canonical tokens are aligned and presentation/native/source gates remain separately mandatory")


if __name__ == "__main__":
    main()
