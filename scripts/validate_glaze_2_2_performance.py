#!/usr/bin/env python3
"""Fail-closed static validation for Glaze UI 2.2 performance / Glaze budgets.

This validator checks deterministic design-system complexity and fallback
contracts. It intentionally rejects hardware-dependent wall-clock timing as
promotion evidence; rendered/runtime validators prove the implemented behavior.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "performance" / "glaze-2.2-performance-budget.json"
TOKENS = ROOT / "tokens" / "glaze-2.2.candidate.json"
RUNTIME = ROOT / "js" / "glaze-2.2.candidate.mjs"
INTERACTIONS = ROOT / "js" / "glaze-2.2.system-interactions.candidate.mjs"
ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        fail(f"top-level JSON must be object: {path.relative_to(ROOT)}")
        return {}
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> None:
    contract = read_json(CONTRACT)
    tokens = read_json(TOKENS)
    runtime = RUNTIME.read_text(encoding="utf-8") if RUNTIME.is_file() else ""
    interactions = INTERACTIONS.read_text(encoding="utf-8") if INTERACTIONS.is_file() else ""

    require(contract.get("version") == "2.2.0-candidate.1", "performance contract version drifted")
    require(contract.get("lifecycle") == "candidate", "performance contract must remain Candidate")
    require(contract.get("stableBaseline") == "2.1.0", "performance contract must preserve 2.1.0 Stable baseline")
    require(contract.get("consumerEligible") is False, "performance contract must remain non-consumer-eligible")
    require(contract.get("measurementModel") == "deterministic-render-complexity-and-fallback-invariants", "performance measurement model drifted")
    require(contract.get("wallClockBenchmarkIsPromotionEvidence") is False, "wall-clock benchmark must not be treated as deterministic promotion evidence")

    profiles = contract.get("profiles", {})
    expected_profiles = {"full": 32, "balanced": 28, "constrained": 14, "minimal": 0}
    require(set(profiles) == set(expected_profiles), "performance profile set drifted")
    for name, cap in expected_profiles.items():
        require(profiles.get(name, {}).get("maxBlurPx") == cap, f"{name} maxBlurPx must be {cap}")
        require(f"{name}: Object.freeze({{ maxBlurPx: {cap} }})" in runtime, f"runtime performance cap missing for {name}")

    expected_surface = {"workspace": 0, "application": 0, "system-overlay": 22, "system-panel": 28, "critical-system": 0}
    require(contract.get("surfaceBlurPx") == expected_surface, "surface blur contract drifted")

    budget = contract.get("systemGlazeBudget", {})
    token_budget = tokens.get("system", {}).get("shellGlazeBudget", {})
    require(budget.get("dominantPanelsMax") == 1, "dominant panel maximum must be 1")
    require(budget.get("smallFloatingControlsMax") == 3, "small floating controls maximum must be 3")
    require(budget.get("exceptionRequiresExplicitContext") is True, "budget exceptions must require explicit context")
    require(budget.get("nestedBackdropBlurAllowed") is False, "nested backdrop blur must remain prohibited")
    require(token_budget.get("dominantPanelsMax") == 1 and token_budget.get("smallFloatingControlsMax") == 3, "token Glaze budget disagrees with performance contract")
    require(tokens.get("system", {}).get("blurStackRule") == "content -> single environmental diffusion -> foreground material", "token blur-stack rule drifted")

    fallbacks = contract.get("forcedFallbacks", {})
    for key in ("reducedTransparencyMaxBlurPx", "forcedColorsMaxBlurPx", "criticalSystemMaxBlurPx", "minimalProfileMaxBlurPx"):
        require(fallbacks.get(key) == 0, f"{key} must be zero")

    expected_order = [
        "remove-nonessential-morphing",
        "remove-decorative-ambient-gradients",
        "remove-decorative-shadows",
        "reduce-or-remove-backdrop-blur",
        "preserve-semantic-structure-target-geometry-focus-readable-contrast",
    ]
    require(contract.get("degradationOrder") == expected_order, "performance degradation order drifted")

    requirements = contract.get("runtimeRequirements", {})
    for key in (
        "directManipulationTracksInput",
        "oneDominantSystemPanelDuringSearchControlCenterSwitching",
        "hiddenSurfacesDoNotConsumeVisibleGlazeBudget",
        "effectsAreNeverRequiredForBasicUsability",
    ):
        require(requirements.get(key) is True, f"runtime performance requirement missing: {key}")
    require(requirements.get("keyboardTraversalWaitsForAnimation") is False, "keyboard traversal must never wait for animation")

    for marker in (
        "export function evaluateSystemGlazeBudget",
        "export function measureSystemGlazeBudget",
        "if (visible(node)) dominantPanels += 1",
        "if (visible(node)) smallFloatingControls += 1",
        "const forceSolid = base.critical || preferences.forcedColors || preferences.reducedTransparency",
        "keyboardTraversalWaitsForAnimation: false",
        "directManipulationTracksInput: true",
    ):
        require(marker in runtime, f"performance runtime missing marker: {marker}")
    require("bindExclusiveSystemPanels" in interactions, "system interaction runtime must coordinate exclusive dominant panels")

    required_rendered = {"full", "balanced", "constrained", "minimal", "reduced-transparency", "forced-colors"}
    require(required_rendered == set(contract.get("renderedProfiles", [])), "rendered performance profile matrix incomplete")

    if ERRORS:
        print("Glaze UI 2.2 performance / Glaze-budget validation failed:")
        for error in ERRORS:
            print(f"- {error}")
        raise SystemExit(1)
    print("Glaze UI 2.2 performance / Glaze-budget contract validation passed (deterministic Candidate evidence)")


if __name__ == "__main__":
    main()
