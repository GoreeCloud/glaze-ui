#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "WEARABLES.md"
COMPONENTS = ROOT / "WEARABLE_COMPONENTS.md"
TOKENS = ROOT / "tokens" / "wearable.candidate.tokens.json"
CSS = ROOT / "css" / "glaze.wearable.candidate.css"
REFERENCE = ROOT / "reference" / "wearable-candidate.html"

REQUIRED_DOC_PHRASES = [
    "Status: **Development Candidate**",
    "Current Stable remains: **Glaze UI 1.4.0**",
    "not a shrunken phone UI",
    "48 dp Wear OS minimum actionable target baseline",
    "Rotary/crown input is a first-class enhancement",
    "Reduced-transparency/solid fallback",
    "Real-device validation before application production approval",
    "Passing this validator proves repository consistency only",
]

REQUIRED_ACCEPTANCE = [
    "Compact round display",
    "Compact rectangular display",
    "Touch-only task completion",
    "Rotary/crown-enhanced navigation",
    "Large-text accessibility",
    "Reduced-motion behavior",
    "Glanceable system-hosted surfaces",
    "Interruption and task-state restoration",
    "Native platform rendering",
    "Real-device validation",
]

REQUIRED_COMPONENT_PHRASES = [
    "Wearable action",
    "Wearable list item",
    "Wearable status card",
    "Wearable glance surface",
    "Reduced-transparency behavior",
    "real-device validation",
]


def fail(message: str) -> None:
    raise SystemExit(f"wearable candidate validation failed: {message}")


def main() -> None:
    for path in (DOC, COMPONENTS, TOKENS, CSS, REFERENCE):
        if not path.is_file():
            fail(f"required candidate asset is missing: {path.relative_to(ROOT)}")

    text = DOC.read_text(encoding="utf-8")
    for phrase in REQUIRED_DOC_PHRASES + REQUIRED_ACCEPTANCE:
        if phrase not in text:
            fail(f"required contract phrase missing: {phrase}")

    component_text = COMPONENTS.read_text(encoding="utf-8")
    for phrase in REQUIRED_COMPONENT_PHRASES:
        if phrase not in component_text:
            fail(f"required component mapping missing: {phrase}")

    data = json.loads(TOKENS.read_text(encoding="utf-8"))
    candidate = data.get("glaze", {}).get("wearableCandidate", {})
    if candidate.get("status", {}).get("$value") != "development-candidate":
        fail("token lifecycle status must remain development-candidate")

    minimum = candidate.get("target", {}).get("minimumWearOs", {}).get("$value", {})
    if minimum != {"value": 48, "unit": "dp"}:
        fail("Wear OS minimum target must remain 48 dp in this candidate")

    resilience = candidate.get("resilience", {})
    for key in ("reducedMotion", "reducedTransparency", "solidFallback", "largeText"):
        if resilience.get(key, {}).get("$value") is not True:
            fail(f"required resilience token is not enabled: {key}")

    stable_tokens = json.loads((ROOT / "tokens" / "glaze.tokens.json").read_text(encoding="utf-8"))
    if "wearableCandidate" in stable_tokens.get("glaze", {}):
        fail("candidate wearable tokens must not be injected into Stable glaze.tokens.json")

    css = CSS.read_text(encoding="utf-8")
    for marker in ('data-glaze-wearable-candidate', 'prefers-reduced-motion', 'forced-colors', '--glaze-wearable-target: 48px'):
        if marker not in css:
            fail(f"required candidate CSS behavior missing: {marker}")

    reference = REFERENCE.read_text(encoding="utf-8")
    for marker in ('data-glaze-watch-shape="round"', 'data-glaze-watch-shape="rectangular"', 'Development Candidate only', 'does not constitute native-platform or real-device acceptance'):
        if marker not in reference:
            fail(f"required reference evidence marker missing: {marker}")

    if 'glaze.wearable.candidate.css' in (ROOT / 'css' / 'glaze.css').read_text(encoding='utf-8'):
        fail("candidate wearable CSS must not be imported by Stable glaze.css")

    print("Glaze UI wearable Development Candidate contract, mappings, and reference validated.")


if __name__ == "__main__":
    main()
