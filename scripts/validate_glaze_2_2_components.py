#!/usr/bin/env python3
"""Fail-closed validation for the Glaze UI 2.2 Foundation component contracts.

This validator checks objective machine-readable invariants for the bounded
Foundation tier. It does not create rendered, native, consumer, or human
Visual Excellence evidence and therefore does not by itself promote a
component to Candidate or Stable.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_DIR = ROOT / "contracts" / "components" / "2.2"
SCHEMA_PATH = ROOT / "schemas" / "component-contract-2.2.schema.json"
ERRORS: list[str] = []

FOUNDATION = {
    "glz-button.json": "GlzButton",
    "glz-icon-button.json": "GlzIconButton",
    "glz-text-field.json": "GlzTextField",
    "glz-select.json": "GlzSelect",
    "glz-checkbox.json": "GlzCheckbox",
    "glz-radio.json": "GlzRadio",
    "glz-switch.json": "GlzSwitch",
    "glz-slider.json": "GlzSlider",
}

STATE_PRIORITY = ["disabled", "error", "pressed", "focus", "selected", "hover", "rest"]
REQUIRED_BASE_STATES = {"rest", "hover", "focus", "pressed", "selected", "disabled", "error"}
REQUIRED_FORM_FACTORS = {"mobile", "tablet", "desktop", "wide-desktop", "tv", "foldable", "resizable"}
REQUIRED_DENSITIES = {"compact", "standard", "comfortable", "far-view"}


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
        fail(f"top-level JSON must be an object: {path.relative_to(ROOT)}")
        return {}
    return value


def require_keys(obj: dict[str, Any], keys: tuple[str, ...], label: str) -> None:
    for key in keys:
        if key not in obj:
            fail(f"{label} missing required key: {key}")


def require_nonempty_string(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        fail(f"{label} must be a non-empty string")


def validate_schema(schema: dict[str, Any]) -> None:
    require_keys(schema, ("$schema", "$id", "title", "type", "required", "properties"), "2.2 component schema")
    if schema.get("type") != "object" or schema.get("additionalProperties") is not False:
        fail("2.2 component schema must remain a closed object")
    required = set(schema.get("required", [])) if isinstance(schema.get("required"), list) else set()
    must_require = {
        "schemaVersion", "id", "name", "version", "lifecycle", "tier", "semanticRole",
        "variants", "sizes", "states", "statePriority", "material", "targets", "input",
        "accessibility", "density", "formFactors", "fallbacks", "api", "content", "testing", "visualReview",
    }
    missing = must_require - required
    if missing:
        fail(f"2.2 component schema does not require: {sorted(missing)}")


def validate_common(filename: str, expected_name: str, contract: dict[str, Any]) -> None:
    label = filename
    required = (
        "schemaVersion", "id", "name", "version", "lifecycle", "tier", "semanticRole", "variants",
        "sizes", "states", "statePriority", "material", "targets", "input", "accessibility", "density",
        "formFactors", "fallbacks", "api", "content", "testing", "visualReview",
    )
    require_keys(contract, required, label)

    if contract.get("schemaVersion") != 1:
        fail(f"{label} schemaVersion must be 1")
    if contract.get("name") != expected_name:
        fail(f"{label} name must be {expected_name}")
    if contract.get("version") != "2.2.0-candidate.1":
        fail(f"{label} version must be 2.2.0-candidate.1")
    if contract.get("lifecycle") not in {"planned", "candidate"}:
        fail(f"{label} lifecycle must remain Planned or Candidate during 2.2 buildout")
    if contract.get("tier") != "foundation":
        fail(f"{label} must remain in the Foundation tier")
    require_nonempty_string(contract.get("semanticRole"), f"{label} semanticRole")

    variants = contract.get("variants")
    if not isinstance(variants, list) or not variants or len(variants) != len(set(variants)):
        fail(f"{label} variants must be a non-empty unique list")

    sizes = contract.get("sizes")
    if not isinstance(sizes, list) or not sizes:
        fail(f"{label} sizes must be non-empty")
        sizes = []
    seen_size_names: set[str] = set()
    for size in sizes:
        if not isinstance(size, dict):
            fail(f"{label} size entry must be an object")
            continue
        name = size.get("name")
        if not isinstance(name, str) or not name:
            fail(f"{label} size name missing")
        elif name in seen_size_names:
            fail(f"{label} duplicate size name: {name}")
        else:
            seen_size_names.add(name)
        visual = size.get("visualHeightPx")
        hit = size.get("touchHitMinPx")
        if not isinstance(visual, int) or visual <= 0:
            fail(f"{label} {name} visualHeightPx must be positive integer")
        if not isinstance(hit, int) or hit < 48:
            fail(f"{label} {name} touchHitMinPx must preserve the 48px 2.2 floor")
        if isinstance(visual, int) and isinstance(hit, int) and hit < visual:
            fail(f"{label} {name} touch hit area cannot be smaller than visual height")

    states = set(contract.get("states", [])) if isinstance(contract.get("states"), list) else set()
    missing_states = REQUIRED_BASE_STATES - states
    if missing_states:
        fail(f"{label} missing shared component states: {sorted(missing_states)}")
    if contract.get("statePriority") != STATE_PRIORITY:
        fail(f"{label} statePriority drifted from shared 2.2 precedence")

    material = contract.get("material", {})
    if not isinstance(material, dict):
        fail(f"{label} material must be an object")
    else:
        if material.get("glazeIsExceptional") is not True:
            fail(f"{label} must explicitly keep Glaze exceptional")
        allowed = material.get("allowed", [])
        if material.get("default") not in allowed:
            fail(f"{label} default material must be included in allowed materials")
        require_nonempty_string(material.get("rule"), f"{label} material rule")

    targets = contract.get("targets", {})
    if not isinstance(targets, dict):
        fail(f"{label} targets must be an object")
    else:
        if targets.get("touchMinPx", 0) < 48:
            fail(f"{label} touchMinPx must be at least 48")
        if targets.get("touchAssistanceMinPx", 0) < 56:
            fail(f"{label} Touch Assistance floor must be at least 56")

    input_contract = contract.get("input", {})
    if not isinstance(input_contract, dict):
        fail(f"{label} input must be an object")
    else:
        for key in ("keyboard", "focus", "hover", "press"):
            require_nonempty_string(input_contract.get(key), f"{label} input.{key}")

    a11y = contract.get("accessibility", {})
    if not isinstance(a11y, dict):
        fail(f"{label} accessibility must be an object")
    else:
        for key in ("role", "name", "state", "value", "keyboard", "focus", "errorAssociation"):
            require_nonempty_string(a11y.get(key), f"{label} accessibility.{key}")
        if a11y.get("nonColorMeaning") is not True:
            fail(f"{label} must prohibit color-only meaning")
        for key in ("reducedMotion", "reducedTransparency", "increasedContrast", "forcedColors", "largeText"):
            require_nonempty_string(a11y.get(key), f"{label} accessibility.{key}")

    densities = set(contract.get("density", [])) if isinstance(contract.get("density"), list) else set()
    if densities != REQUIRED_DENSITIES:
        fail(f"{label} density coverage must be exactly {sorted(REQUIRED_DENSITIES)}")
    forms = set(contract.get("formFactors", [])) if isinstance(contract.get("formFactors"), list) else set()
    if forms != REQUIRED_FORM_FACTORS:
        fail(f"{label} form-factor coverage must be exactly {sorted(REQUIRED_FORM_FACTORS)}")

    fallbacks = contract.get("fallbacks", {})
    if not isinstance(fallbacks, dict):
        fail(f"{label} fallbacks must be an object")
    else:
        for key in ("reducedMotion", "reducedTransparency", "highContrast", "forcedColors", "performance"):
            require_nonempty_string(fallbacks.get(key), f"{label} fallbacks.{key}")

    api = contract.get("api", {})
    if not isinstance(api, dict):
        fail(f"{label} api must be an object")
    else:
        if api.get("rawVisualPropsPreferred") is not False:
            fail(f"{label} must prefer semantic APIs over raw visual props")
        for key in ("semanticProps", "events", "slots"):
            value = api.get(key)
            if not isinstance(value, list) or not value:
                fail(f"{label} api.{key} must be non-empty")
        for event in api.get("events", []):
            if not isinstance(event, str) or not event.startswith("on"):
                fail(f"{label} event must use semantic on* naming: {event!r}")

    content = contract.get("content", {})
    if not isinstance(content, dict):
        fail(f"{label} content must be an object")
    else:
        for key in ("overflow", "localization", "rtl"):
            require_nonempty_string(content.get(key), f"{label} content.{key}")
        expansion = content.get("textExpansionPercent")
        if expansion != [30, 50]:
            fail(f"{label} must tolerate the documented 30–50% localization expansion")

    testing = contract.get("testing", {})
    if not isinstance(testing, dict):
        fail(f"{label} testing must be an object")
    else:
        if set(testing.get("themes", [])) != {"light", "dark", "deep-dark"}:
            fail(f"{label} tests must cover light/dark/deep-dark")
        if set(testing.get("directions", [])) != {"ltr", "rtl"}:
            fail(f"{label} tests must cover LTR and RTL")
        if not {100, 200}.issubset(set(testing.get("textScalePercent", []))):
            fail(f"{label} tests must cover 100% and 200% text")
        if set(testing.get("motion", [])) != {"full", "reduced"}:
            fail(f"{label} tests must cover full and reduced motion")
        contrast = set(testing.get("contrast", []))
        if not {"standard", "high", "forced-colors"}.issubset(contrast):
            fail(f"{label} tests must cover standard/high/forced-colors")
        tested_states = set(testing.get("states", []))
        if not {"rest", "focus", "disabled", "error"}.issubset(tested_states):
            fail(f"{label} test matrix missing core states")

    review = contract.get("visualReview", {})
    if not isinstance(review, dict) or review.get("required") is not True or not review.get("criteria"):
        fail(f"{label} must require non-empty human Visual Excellence review")


def validate_specific(filename: str, contract: dict[str, Any]) -> None:
    variants = contract.get("variants")
    sizes = contract.get("sizes", [])
    size_map = {item.get("name"): item for item in sizes if isinstance(item, dict)}

    if filename == "glz-button.json":
        if variants != ["primary", "secondary", "quiet", "glaze", "danger"]:
            fail("GlzButton variants drifted from 2.2 specification")
        expected = {"xs": 28, "sm": 32, "md": 40, "lg": 48, "xl": 56}
        for name, height in expected.items():
            if size_map.get(name, {}).get("visualHeightPx") != height:
                fail(f"GlzButton {name} height must be {height}px")
    elif filename == "glz-icon-button.json":
        if variants != ["quiet", "surface", "glaze", "accent", "danger"]:
            fail("GlzIconButton variants drifted from 2.2 specification")
        expected = {"xs": 28, "sm": 32, "md": 40, "lg": 48, "xl": 56}
        for name, height in expected.items():
            if size_map.get(name, {}).get("visualHeightPx") != height:
                fail(f"GlzIconButton {name} height must be {height}px")
        if "tooltip" not in contract.get("api", {}).get("semanticProps", []):
            fail("GlzIconButton must expose tooltip semantics for ambiguous actions")
    elif filename == "glz-text-field.json":
        if variants != ["standard", "filled", "glaze"]:
            fail("GlzTextField variants drifted from 2.2 specification")
        expected = {"sm": 36, "md": 44, "lg": 52}
        for name, height in expected.items():
            if size_map.get(name, {}).get("visualHeightPx") != height:
                fail(f"GlzTextField {name} height must be {height}px")
        if "placeholder" not in contract.get("api", {}).get("semanticProps", []):
            fail("GlzTextField must explicitly model placeholder separately from label")
    elif filename == "glz-select.json":
        if "expanded" not in contract.get("states", []) or "collapsed" not in contract.get("states", []):
            fail("GlzSelect must model expanded and collapsed states")
        events = set(contract.get("api", {}).get("events", []))
        if not {"onOpen", "onClose", "onChange"}.issubset(events):
            fail("GlzSelect must expose semantic open/close/change events")
    elif filename == "glz-checkbox.json":
        if not {"checked", "unchecked", "indeterminate", "mixed"}.issubset(set(contract.get("states", []))):
            fail("GlzCheckbox must model checked/unchecked/indeterminate/mixed states")
        if contract.get("targets", {}).get("wholeLabelTargetWhenApplicable") is not True:
            fail("GlzCheckbox whole label row must be clickable")
    elif filename == "glz-radio.json":
        if not {"checked", "unchecked"}.issubset(set(contract.get("states", []))):
            fail("GlzRadio must model checked and unchecked states")
        if contract.get("targets", {}).get("wholeLabelTargetWhenApplicable") is not True:
            fail("GlzRadio whole label row must be clickable")
    elif filename == "glz-switch.json":
        if not {"checked", "unchecked"}.issubset(set(contract.get("states", []))):
            fail("GlzSwitch must model checked and unchecked states")
        role = str(contract.get("accessibility", {}).get("role", ""))
        if "switch" not in role.lower():
            fail("GlzSwitch must expose switch semantics")
    elif filename == "glz-slider.json":
        if variants != ["continuous", "stepped", "range"]:
            fail("GlzSlider variants drifted from 2.2 specification")
        if "dragging" not in contract.get("states", []):
            fail("GlzSlider must model dragging state")
        direct = str(contract.get("input", {}).get("directManipulation", ""))
        if "continu" not in direct.lower() or "track" not in direct.lower():
            fail("GlzSlider must require continuous direct-manipulation tracking")
        if "stylus" not in contract.get("testing", {}).get("inputs", []):
            fail("GlzSlider test matrix must cover stylus input")


def main() -> int:
    schema = read_json(SCHEMA_PATH)
    validate_schema(schema)

    ids: set[str] = set()
    names: set[str] = set()
    for filename, expected_name in FOUNDATION.items():
        contract = read_json(CONTRACT_DIR / filename)
        if not contract:
            continue
        validate_common(filename, expected_name, contract)
        validate_specific(filename, contract)
        cid = contract.get("id")
        name = contract.get("name")
        if cid in ids:
            fail(f"duplicate component id: {cid}")
        if name in names:
            fail(f"duplicate component name: {name}")
        if isinstance(cid, str):
            ids.add(cid)
        if isinstance(name, str):
            names.add(name)

    if ERRORS:
        print("Glaze UI 2.2 Foundation component validation: FAIL")
        for error in ERRORS:
            print(f"- {error}")
        return 1

    print("Glaze UI 2.2 Foundation component validation: PASS")
    print("Eight Foundation component contracts are structurally valid; lifecycle promotion remains separately gated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
