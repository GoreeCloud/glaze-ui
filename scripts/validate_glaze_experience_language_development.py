#!/usr/bin/env python3
"""Fail-closed source validation for the Glaze UI Experience Language Development foundation."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "experience-language.dev.json"
SCHEMA = ROOT / "schemas" / "experience-language.schema.json"
TOKENS = ROOT / "tokens" / "glaze-experience-language.dev.json"
SPEC = ROOT / "GLAZE_UI_VISUAL_SPATIAL_INTERACTION_LANGUAGE.md"
VERSION = ROOT / "VERSION"
LIFECYCLE = ROOT / "registry" / "lifecycle.json"

EXPECTED_LAYERS = {
    "visualLanguage": ["color", "typography", "iconography", "shape", "materials", "surfaces", "depth", "imagery", "illustration", "brand-identity"],
    "spatialLanguage": ["layout", "grid", "spacing", "sizing", "density", "responsive-behavior"],
    "interactionLanguage": ["motion", "gestures", "feedback", "states", "haptics", "sound"],
    "componentLanguage": ["navigation", "controls", "containers", "inputs", "feedback", "data-visualization", "system-components"],
    "experienceStandards": ["accessibility", "responsiveness", "adaptability", "content-language", "theming", "personalization", "brand-consistency"],
}
EXPECTED_TOKEN_CATEGORIES = ["color", "typography", "spacing", "radius", "border", "shadow", "elevation", "opacity", "blur", "motion", "size", "icon", "breakpoint"]
EXPECTED_STATES = ["default", "hovered", "focused", "pressed", "selected", "active", "dragged", "disabled", "loading", "success", "warning", "error"]
EXPECTED_DENSITIES = ["comfortable", "standard", "compact"]
EXPECTED_MOTION = ["instant", "fast", "standard", "emphasized", "long"]
EXPECTED_ELEVATION = ["background", "base-surface", "content-container", "raised-control", "floating-panel", "menu-or-popover", "dialog", "critical-system-overlay"]
EXPECTED_ACCESSIBILITY = ["high-contrast", "adjustable-typography", "screen-readers", "keyboard-navigation", "focus-indicators", "switch-navigation", "voice-interaction", "reduced-motion", "reduced-transparency", "large-touch-targets", "color-independent-status", "semantic-interface-structure", "accessible-data-visualization"]
EXPECTED_TITLES = [
    "Visual Language", "Typography", "Iconography", "Shape Language", "Materials and Surfaces",
    "Elevation and Depth", "Imagery", "Illustration and Artwork", "Brand Identity", "Spatial Language",
    "Spacing System", "Density", "Responsive Layouts", "Component Language", "Interaction Language",
    "Motion System", "Motion Tokens", "Reduced Motion", "Gestures", "Haptics", "Sound",
    "Feedback and Status", "Data Visualization", "Content Language", "Accessibility", "Adaptive Behavior",
    "Theming", "Application Personalization", "Design Tokens", "Glaze UI Design Layers", "Core Glaze UI Principle",
]


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"FAIL: cannot read valid JSON from {path.relative_to(ROOT)}: {exc}")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


contract = load_json(CONTRACT)
schema = load_json(SCHEMA)
tokens = load_json(TOKENS)
lifecycle = load_json(LIFECYCLE)
stable = VERSION.read_text(encoding="utf-8").strip()
spec = SPEC.read_text(encoding="utf-8")

require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "schema must use JSON Schema 2020-12")
require(contract.get("$schema") == "../schemas/experience-language.schema.json", "contract must bind to the repository schema")
require(contract.get("schemaVersion") == 1, "contract schemaVersion must be 1")
require(contract.get("lifecycle") == "Development", "experience language must remain Development")
require(contract.get("consumerEligible") is False, "Development contract must not be consumer eligible")
require(lifecycle.get("currentOfficial") == stable and lifecycle.get("currentStable") == stable, "VERSION and lifecycle current authority must agree")
current_release = next((item for item in lifecycle.get("releases", []) if item.get("version") == stable), None)
require(current_release is not None and current_release.get("status") == "stable" and current_release.get("consumerEligible") is True, "live current Stable must remain a consumer-eligible Stable release")
require(contract.get("stableBaseline") == "1.5.1", "Development contract must retain its frozen V1.5.1 qualification baseline")
require(tokens.get("stableBaseline") == "1.5.1", "Development token map must retain its frozen V1.5.1 qualification baseline")
require(tokens.get("lifecycle") == "Development" and tokens.get("mode") == "reference-only" and tokens.get("consumerEligible") is False, "token ownership map must stay Development/reference-only/non-consumer-eligible")

authority = contract.get("authority", {})
require(authority.get("boundary") == "presentation-only", "authority boundary must remain presentation-only")
for key in [
    "authorizationInferred", "permissionOrConsentGrantedByGlaze", "permissionRequestAutomatic",
    "consequentialExecutionAutomatic", "fallbackExecutionAutomatic", "navigationAutomatic",
    "providerPrecedenceInferred",
]:
    require(authority.get(key) is False, f"{key} must remain false")

require(contract.get("layers") == EXPECTED_LAYERS, "five design layers must match the governed composition")
require(contract.get("designTokens", {}).get("categories") == EXPECTED_TOKEN_CATEGORIES, "design-token category order/coverage mismatch")
require(list(tokens.get("categories", {}).keys()) == EXPECTED_TOKEN_CATEGORIES, "token ownership map category order/coverage mismatch")
require(contract.get("interactionLanguage", {}).get("states") == EXPECTED_STATES, "interaction state grammar mismatch")
require(contract.get("spatialLanguage", {}).get("densities") == EXPECTED_DENSITIES, "density grammar mismatch")
require(contract.get("interactionLanguage", {}).get("motionTokens") == EXPECTED_MOTION, "motion token grammar mismatch")
require(contract.get("visualLanguage", {}).get("elevationHierarchy") == EXPECTED_ELEVATION, "elevation hierarchy mismatch")
require(contract.get("accessibility", {}).get("requirements") == EXPECTED_ACCESSIBILITY, "accessibility requirement set mismatch")
require(contract.get("accessibility", {}).get("precedesVisualRichness") is True, "accessibility must precede visual richness")
require(contract.get("accessibility", {}).get("essentialInformationMayDependExclusivelyOnColor") is False, "essential information must not depend on color only")
require(contract.get("accessibility", {}).get("essentialInformationMayDependExclusivelyOnMotion") is False, "essential information must not depend on motion only")
require(contract.get("accessibility", {}).get("essentialInformationMayDependExclusivelyOnSound") is False, "essential information must not depend on sound only")
require(len(contract.get("componentLanguage", {}).get("coreComponents", [])) >= 36, "core component catalog must include all requested components")

requirements = contract.get("requirements", [])
require(len(requirements) == 31, "contract must contain exactly 31 numbered requirements")
require([entry.get("id") for entry in requirements] == list(range(1, 32)), "requirement IDs must be exactly 1..31")
require([entry.get("title") for entry in requirements] == EXPECTED_TITLES, "requirement titles must match the documented language")
for number, title in enumerate(EXPECTED_TITLES, start=1):
    require(f"## {number}. {title}" in spec, f"human specification is missing section {number}: {title}")

referenced = set()
for paths in tokens.get("categories", {}).values():
    referenced.update(paths)
for paths in tokens.get("compositionSources", {}).values():
    referenced.update(paths)
for source in sorted(referenced):
    require((ROOT / source).is_file(), f"referenced token source does not exist: {source}")

print(
    "PASS: Glaze UI Experience Language Development foundation "
    f"(31/31 requirements, {len(EXPECTED_TOKEN_CATEGORIES)}/13 token categories, "
    f"{len(EXPECTED_STATES)}/12 interaction states, {len(EXPECTED_ACCESSIBILITY)}/13 accessibility requirements)"
)
