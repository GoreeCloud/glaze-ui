#!/usr/bin/env python3
"""Fail-closed validator for the current GLAZE UI V1 release line."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = "1.1.0"
PREVIOUS = "1.0.0"


def fail(message: str) -> None:
    raise SystemExit(f"GLAZE UI V1 validation failed: {message}")


def load_json(path: str):
    with (ROOT / path).open(encoding="utf-8") as handle:
        return json.load(handle)


def require_file(path: str) -> Path:
    target = ROOT / path
    if not target.is_file():
        fail(f"missing required V1 artifact: {path}")
    return target


if require_file("VERSION").read_text(encoding="utf-8").strip() != EXPECTED:
    fail(f"VERSION must be {EXPECTED}")

required = [
    "README.md",
    "SPECIFICATIONS.md",
    "FEATURES.md",
    "BENEFITS.md",
    "COMPETITIVE-OBJECTIVES.md",
    "BRANDING.md",
    "GLAZE_UI_V1_0.md",
    "GLAZE_UI_V1_1.md",
    "css/glaze-v1.0.0.css",
    "css/glaze-v1.1.0.css",
    "css/glaze-v1.1.optical.css",
    "js/glaze-v1.1.0.mjs",
    "js/glaze-v1.1.runtime.mjs",
    "contracts/system-shell/glaze-system-shell-v1.json",
    "contracts/performance/glaze-v1-performance-budget.json",
    "contracts/regression/visual-baselines-v1.json",
    "acceptance/v1.1-stable.md",
]
for rel in required:
    require_file(rel)

lifecycle = load_json("registry/lifecycle.json")
if lifecycle.get("schemaVersion", 0) < 2:
    fail("lifecycle schema must be V1.1-aware")

candidate_mode = lifecycle.get("activeCandidate") == EXPECTED
stable_mode = lifecycle.get("currentStable") == EXPECTED and lifecycle.get("currentOfficial") == EXPECTED
if candidate_mode == stable_mode:
    fail("exactly one of Release Candidate or Stable lifecycle mode must be active for V1.1")

release = next((item for item in lifecycle.get("releases", []) if item.get("version") == EXPECTED), None)
if not release:
    fail("lifecycle is missing the V1.1 release record")
if release.get("contract") != "GLAZE_UI_V1_1.md" or release.get("acceptance") != "acceptance/v1.1-stable.md":
    fail("V1.1 lifecycle release paths mismatch")
if candidate_mode:
    if lifecycle.get("currentOfficial") != PREVIOUS or lifecycle.get("currentStable") is not None:
        fail("Release Candidate mode must preserve V1.0 as current official reset baseline with no Stable release")
    if release.get("status") != "release-candidate" or release.get("consumerEligible") is not False:
        fail("V1.1 candidate must remain non-consumer-eligible")
else:
    if lifecycle.get("officialProductLabel") != "GLAZE UI V1.1":
        fail("Stable lifecycle must name GLAZE UI V1.1 as official product label")
    if lifecycle.get("activeCandidate") is not None:
        fail("Stable lifecycle must clear activeCandidate")
    if release.get("status") != "stable" or release.get("consumerEligible") is not True:
        fail("Stable V1.1 release must be consumer eligible")

entrypoint = require_file("css/glaze-v1.1.0.css").read_text(encoding="utf-8").lower()
if "glaze-v1.0.0.css" not in entrypoint or "glaze-v1.1.optical.css" not in entrypoint:
    fail("V1.1 web entrypoint must incrementally import the V1.0 baseline and V1.1 optical layer")

optical = require_file("css/glaze-v1.1.optical.css").read_text(encoding="utf-8").lower()
required_optical_literals = {
    "#081016": "Canvas Black",
    "#101a20": "Deep Graphite",
    "#18252b": "Slate Graphite",
    "#0f6b6f": "Deep Teal",
    "#1c8a8d": "Mineral Teal",
    "#8fd6d2": "Soft Aqua",
    "#d9a35f": "Soft Amber",
    "#e7c78a": "Champagne Gold",
    "#f2d7a6": "Warm Glow",
    "data-glz-performance=\"constrained\"": "constrained performance fallback",
    "forced-colors: active": "Forced Colors fallback",
    "prefers-reduced-motion: reduce": "Reduced Motion fallback",
    "prefers-contrast: more": "Increased Contrast fallback",
    "data-glz-transparency=\"reduced\"": "Reduced Transparency fallback",
    "--glz1-environment-color": "Environmental Color Memory input",
    "--glz1-radius-micro": "curvature grammar",
    "data-glz-depth=\"6\"": "depth grammar",
    "data-glz-density=\"productive\"": "density profiles",
}
for literal, label in required_optical_literals.items():
    if literal not in optical:
        fail(f"V1.1 optical layer missing {label}")
for forbidden in ("#7657f6", "rgba(126,92,255", "neon cyan", "rainbow glass"):
    if forbidden in optical:
        fail(f"V1.1 optical layer contains prohibited default atmosphere: {forbidden}")

runtime = require_file("js/glaze-v1.1.runtime.mjs").read_text(encoding="utf-8")
for symbol in ("setGlazeAura", "setGlazeDensity", "setGlazePerformance", "setEnvironmentalColor", "clearEnvironmentalColor"):
    if f"function {symbol}" not in runtime:
        fail(f"V1.1 runtime missing {symbol}")
for network_marker in ("fetch(", "XMLHttpRequest", "WebSocket", "sendBeacon", "analytics"):
    if network_marker in runtime:
        fail(f"V1.1 optical runtime must remain local-only: {network_marker}")

performance = load_json("contracts/performance/glaze-v1-performance-budget.json")
if performance.get("product") != "GLAZE UI V1.1" or performance.get("version") != EXPECTED:
    fail("performance budget is not bound to V1.1")
rules = performance.get("rules", {})
expected_limits = {
    "nestedBackdropBlurAllowed": False,
    "dominantGlazePanelsMax": 1,
    "smallFloatingGlazeControlsMax": 3,
    "concurrentAuraFieldsMax": 2,
    "environmentalColorInfluencePercentMax": 12,
    "overlayBackdropBlurPxMax": 22,
    "panelBackdropBlurPxMax": 28,
    "microInteractionDurationMsMax": 220,
    "connectedTransitionDurationMsMax": 360,
    "reducedMotionDurationMsMax": 120,
    "constrainedModeBackdropBlurPx": 0,
    "constrainedModeAuraFieldsMax": 0,
}
for key, expected in expected_limits.items():
    if rules.get(key) != expected:
        fail(f"V1.1 performance budget mismatch: {key}")

visual = load_json("contracts/regression/visual-baselines-v1.json")
if visual.get("product") != "GLAZE UI V1.1" or visual.get("version") != EXPECTED:
    fail("visual-regression contract is not bound to V1.1")
cases = visual.get("cases") or []
required_case_ids = {
    "design-center-mobile-320-light",
    "design-center-mobile-390-light",
    "design-center-mobile-390-dark",
}
if {case.get("id") for case in cases if case.get("required")} != required_case_ids:
    fail("V1.1 visual-regression required case set mismatch")
if stable_mode:
    baseline = visual.get("baselineRevision")
    if not isinstance(baseline, str) or len(baseline) != 40:
        fail("Stable V1.1 requires an exact reviewed baselineRevision")
    if visual.get("reviewState") != "reviewed":
        fail("Stable V1.1 requires reviewed visual baselines")

# The reset-era active tree must not retain live claims that a pre-reset release is current.
# Immutable Git history and CHANGELOG.md remain the audit trail.
active_scan_exclusions = {
    "CHANGELOG.md",
    "GLAZE_UI_V1_0.md",
    "acceptance/v1.0-stable.md",
    "scripts/validate_glaze_v1.py",
}
stale_markers = (
    "current stable remains 2.1.0",
    "current stable remains glaze ui 2.1.0",
    "2.2 performance contract",
    "glaze ui 2.2.0 is the current stable",
)
for path in ROOT.rglob("*"):
    if not path.is_file() or ".git" in path.parts:
        continue
    rel = path.relative_to(ROOT).as_posix()
    if rel in active_scan_exclusions or path.suffix.lower() not in {".css", ".html", ".json", ".md", ".mjs", ".py", ".yaml", ".yml"}:
        continue
    text = path.read_text(encoding="utf-8", errors="replace").lower()
    for marker in stale_markers:
        if marker in text:
            fail(f"stale pre-reset current-release statement remains in active source: {rel}: {marker}")

acceptance = require_file("acceptance/v1.1-stable.md").read_text(encoding="utf-8")
if stable_mode:
    for pending in ("Reviewed implementation revision: `PENDING`", "Final Stable release revision: `PENDING`", "Stable release/tag: `PENDING`", "Stable accepted: `No`"):
        if pending in acceptance:
            fail(f"Stable lifecycle cannot retain unresolved acceptance field: {pending}")
    native = lifecycle.get("capabilities", {}).get("native-reference", {})
    if native.get("status") in {None, "revalidation-required", "unknown", "pending"}:
        fail("Stable V1.1 requires resolved native-reference lifecycle state")

print(f"GLAZE UI V1.1 {'Stable' if stable_mode else 'Release Candidate'} contract: OK")
