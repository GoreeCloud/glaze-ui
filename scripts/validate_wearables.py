#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "WEARABLES.md"
TOKENS = ROOT / "tokens" / "wearable.candidate.tokens.json"

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


def fail(message: str) -> None:
    raise SystemExit(f"wearable candidate validation failed: {message}")


def main() -> None:
    if not DOC.is_file():
        fail("WEARABLES.md is missing")
    if not TOKENS.is_file():
        fail("candidate token file is missing")

    text = DOC.read_text(encoding="utf-8")
    for phrase in REQUIRED_DOC_PHRASES + REQUIRED_ACCEPTANCE:
        if phrase not in text:
            fail(f"required contract phrase missing: {phrase}")

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

    print("Glaze UI wearable Development Candidate contract validated.")


if __name__ == "__main__":
    main()
