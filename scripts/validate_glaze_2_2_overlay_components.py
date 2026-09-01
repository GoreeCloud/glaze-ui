#!/usr/bin/env python3
"""Fail-closed validation for the bounded Glaze UI 2.2 Overlay tier.

Overlay remains Planned while this validator is introduced. Passing this gate is
objective pre-promotion evidence only; it is not native/device acceptance,
consumer eligibility, Human Visual Excellence approval, or Stable promotion.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_DIR = ROOT / "contracts" / "components" / "2.2"
SCHEMA_PATH = ROOT / "schemas" / "component-contract-2.2.schema.json"
ERRORS: list[str] = []

OVERLAY = {
    "glz-tooltip.json": "GlzTooltip",
    "glz-popover.json": "GlzPopover",
    "glz-menu.json": "GlzMenu",
    "glz-dialog.json": "GlzDialog",
    "glz-sheet.json": "GlzSheet",
    "glz-toast.json": "GlzToast",
}
STATE_PRIORITY = ["disabled", "error", "pressed", "focus", "selected", "hover", "rest"]
DENSITIES = {"compact", "standard", "comfortable", "far-view"}
FORM_FACTORS = {"mobile", "tablet", "desktop", "wide-desktop", "tv", "foldable", "resizable"}
REQUIRED = {
    "$schema", "schemaVersion", "id", "name", "version", "lifecycle", "tier", "semanticRole",
    "variants", "sizes", "states", "statePriority", "material", "targets", "input", "accessibility",
    "density", "formFactors", "fallbacks", "api", "content", "testing", "visualReview",
}


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


def nonempty(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        fail(f"{label} must be a non-empty string")


def validate_schema(schema: dict[str, Any]) -> None:
    if schema.get("type") != "object" or schema.get("additionalProperties") is not False:
        fail("2.2 component schema must remain a closed object")
    props = schema.get("properties")
    if not isinstance(props, dict):
        fail("2.2 component schema properties must be an object")
        return
    tier = props.get("tier", {}) if isinstance(props.get("tier"), dict) else {}
    if "overlay" not in tier.get("enum", []):
        fail("2.2 component schema must retain Overlay as a valid tier")
    lifecycle = props.get("lifecycle", {}) if isinstance(props.get("lifecycle"), dict) else {}
    if "planned" not in lifecycle.get("enum", []) or "candidate" not in lifecycle.get("enum", []):
        fail("2.2 component schema must retain Planned and Candidate lifecycle states")


def validate_common(filename: str, expected_name: str, contract: dict[str, Any], schema: dict[str, Any]) -> None:
    missing = REQUIRED - set(contract)
    if missing:
        fail(f"{filename} missing required keys: {sorted(missing)}")
    allowed = set(schema.get("properties", {})) if isinstance(schema.get("properties"), dict) else set()
    extras = set(contract) - allowed
    if extras:
        fail(f"{filename} has schema-forbidden keys: {sorted(extras)}")
    if contract.get("$schema") != "../../../schemas/component-contract-2.2.schema.json":
        fail(f"{filename} must reference the canonical 2.2 component schema")
    if contract.get("schemaVersion") != 1:
        fail(f"{filename} schemaVersion must be 1")
    if contract.get("name") != expected_name:
        fail(f"{filename} name must be {expected_name}")
    expected_id = filename.removesuffix(".json") + "-2-2"
    if contract.get("id") != expected_id:
        fail(f"{filename} id must be {expected_id}")
    if contract.get("version") != "2.2.0-candidate.1":
        fail(f"{filename} version must remain 2.2.0-candidate.1")
    if contract.get("lifecycle") != "planned":
        fail(f"{filename} must remain Planned until exact-head Overlay pre-promotion evidence passes")
    if contract.get("tier") != "overlay":
        fail(f"{filename} must remain in the Overlay tier")
    nonempty(contract.get("semanticRole"), f"{filename} semanticRole")
    if contract.get("statePriority") != STATE_PRIORITY:
        fail(f"{filename} state priority drifted from shared 2.2 precedence")

    variants = contract.get("variants")
    if not isinstance(variants, list) or not variants or len(variants) != len(set(variants)):
        fail(f"{filename} variants must be a non-empty unique list")
    sizes = contract.get("sizes")
    if not isinstance(sizes, list) or not sizes:
        fail(f"{filename} sizes must be non-empty")
    else:
        names: set[str] = set()
        for item in sizes:
            if not isinstance(item, dict):
                fail(f"{filename} size entries must be objects")
                continue
            name = item.get("name")
            if not isinstance(name, str) or not name or name in names:
                fail(f"{filename} size names must be unique non-empty strings")
            names.add(name) if isinstance(name, str) else None
            if not isinstance(item.get("visualHeightPx"), int) or item.get("visualHeightPx", 0) <= 0:
                fail(f"{filename} {name} visualHeightPx must be positive")
            if not isinstance(item.get("touchHitMinPx"), int) or item.get("touchHitMinPx", 0) < 48:
                fail(f"{filename} {name} must preserve the 48px effective target floor")

    material = contract.get("material")
    if not isinstance(material, dict):
        fail(f"{filename} material must be an object")
    else:
        allowed_materials = material.get("allowed", [])
        if material.get("default") not in allowed_materials:
            fail(f"{filename} default material must be allowed")
        if material.get("glazeIsExceptional") is not False:
            fail(f"{filename} Overlay contract must explicitly allow Glaze as a primary transient material")
        nonempty(material.get("rule"), f"{filename} material.rule")

    targets = contract.get("targets")
    if not isinstance(targets, dict) or targets.get("touchMinPx", 0) < 48 or targets.get("touchAssistanceMinPx", 0) < 56:
        fail(f"{filename} must preserve 48px touch and 56px Touch Assistance floors")

    for block, keys in {
        "input": ("keyboard", "focus", "hover", "press"),
        "accessibility": ("role", "name", "state", "value", "keyboard", "focus", "errorAssociation", "reducedMotion", "reducedTransparency", "increasedContrast", "forcedColors", "largeText"),
        "fallbacks": ("reducedMotion", "reducedTransparency", "highContrast", "forcedColors", "performance"),
    }.items():
        value = contract.get(block)
        if not isinstance(value, dict):
            fail(f"{filename} {block} must be an object")
            continue
        for key in keys:
            nonempty(value.get(key), f"{filename} {block}.{key}")
    if isinstance(contract.get("accessibility"), dict) and contract["accessibility"].get("nonColorMeaning") is not True:
        fail(f"{filename} must prohibit color-only meaning")
    if set(contract.get("density", [])) != DENSITIES:
        fail(f"{filename} density coverage must be exactly {sorted(DENSITIES)}")
    if set(contract.get("formFactors", [])) != FORM_FACTORS:
        fail(f"{filename} form-factor coverage must be exactly {sorted(FORM_FACTORS)}")

    api = contract.get("api")
    if not isinstance(api, dict):
        fail(f"{filename} api must be an object")
    else:
        if api.get("rawVisualPropsPreferred") is not False:
            fail(f"{filename} must prefer semantic APIs over raw visual props")
        for key in ("semanticProps", "events", "slots"):
            values = api.get(key)
            if not isinstance(values, list) or not values or len(values) != len(set(values)):
                fail(f"{filename} api.{key} must be a non-empty unique list")
        for event in api.get("events", []):
            if not isinstance(event, str) or not event.startswith("on"):
                fail(f"{filename} event must use semantic on* naming: {event!r}")

    content = contract.get("content")
    if not isinstance(content, dict) or content.get("textExpansionPercent") != [30, 50]:
        fail(f"{filename} must preserve the 30–50% localization expansion contract")
    testing = contract.get("testing")
    if not isinstance(testing, dict):
        fail(f"{filename} testing must be an object")
    else:
        if set(testing.get("themes", [])) != {"light", "dark", "deep-dark"}: fail(f"{filename} must test light/dark/deep-dark")
        if set(testing.get("directions", [])) != {"ltr", "rtl"}: fail(f"{filename} must test LTR and RTL")
        if not {100, 200}.issubset(set(testing.get("textScalePercent", []))): fail(f"{filename} must test 100% and 200% text")
        if set(testing.get("motion", [])) != {"full", "reduced"}: fail(f"{filename} must test full and reduced motion")
        if not {"standard", "high", "forced-colors"}.issubset(set(testing.get("contrast", []))): fail(f"{filename} must test standard/high/forced-colors")
        if not {"mouse", "touch", "keyboard"}.issubset(set(testing.get("inputs", []))): fail(f"{filename} must test mouse, touch, and keyboard")
    review = contract.get("visualReview")
    if not isinstance(review, dict) or review.get("required") is not True or not review.get("criteria"):
        fail(f"{filename} must require human Visual Excellence review")


def validate_specific(filename: str, contract: dict[str, Any]) -> None:
    variants = contract.get("variants")
    material = contract.get("material", {}) if isinstance(contract.get("material"), dict) else {}
    api = contract.get("api", {}) if isinstance(contract.get("api"), dict) else {}
    acc = contract.get("accessibility", {}) if isinstance(contract.get("accessibility"), dict) else {}
    sizes = {x.get("name"): x for x in contract.get("sizes", []) if isinstance(x, dict)}
    if filename == "glz-tooltip.json":
        if variants != ["standard", "shortcut"]: fail("GlzTooltip variants drifted from the bounded Overlay contract")
        if material.get("default") != "thick-glaze": fail("GlzTooltip must use Thick Glaze with an opaque fallback")
        if "non-interactive" not in str(contract.get("semanticRole", "")).lower(): fail("GlzTooltip must remain explicitly non-interactive")
        if api.get("events") != ["onOpen", "onClose"]: fail("GlzTooltip cannot acquire action semantics")
    elif filename == "glz-popover.json":
        if variants != ["standard", "filter", "form", "help"]: fail("GlzPopover variants drifted")
        if material.get("default") != "thick-glaze" or "onEscape" not in api.get("events", []): fail("GlzPopover must keep Thick Glaze and Escape semantics")
        if "modal" not in api.get("semanticProps", []): fail("GlzPopover API must expose modality explicitly")
    elif filename == "glz-menu.json":
        if variants != ["standard", "context", "submenu"]: fail("GlzMenu variants drifted")
        if [sizes.get(k, {}).get("visualHeightPx") for k in ("compact", "standard", "touch")] != [32, 36, 48]: fail("GlzMenu item heights must remain 32/36/48px")
        if "menu" not in str(acc.get("role", "")).lower() or "onAction" not in api.get("events", []): fail("GlzMenu must preserve menu semantics and action event")
    elif filename == "glz-dialog.json":
        if variants != ["standard", "confirmation", "destructive"]: fail("GlzDialog variants drifted")
        if material.get("default") != "solid-glaze": fail("GlzDialog must default to Solid Glaze for focused modal clarity")
        if "modal" not in api.get("semanticProps", []) or "actions" not in api.get("slots", []): fail("GlzDialog must expose modality and actions")
    elif filename == "glz-sheet.json":
        if variants != ["bottom", "side"]: fail("GlzSheet variants must remain bottom/side")
        if list(sizes) != ["peek", "medium", "large"]: fail("GlzSheet detent sizes must remain peek/medium/large")
        if not {"detent", "detents"}.issubset(set(api.get("semanticProps", []))) or "onDetentChange" not in api.get("events", []): fail("GlzSheet must expose accessible detent semantics")
    elif filename == "glz-toast.json":
        if variants != ["confirmation", "status", "undo", "error"]: fail("GlzToast variants drifted")
        if material.get("default") != "raised": fail("GlzToast must default to a compact raised surface")
        if "status" not in str(acc.get("role", "")).lower() or "action" not in api.get("semanticProps", []): fail("GlzToast must preserve status semantics and optional recovery action")


def main() -> None:
    schema = read_json(SCHEMA_PATH)
    validate_schema(schema)
    for filename, name in OVERLAY.items():
        contract = read_json(CONTRACT_DIR / filename)
        if contract:
            validate_common(filename, name, contract, schema)
            validate_specific(filename, contract)
    if ERRORS:
        print("Glaze UI 2.2 Overlay contract validation failed:")
        for error in ERRORS: print(f"- {error}")
        raise SystemExit(1)
    print("Glaze UI 2.2 Overlay contract validation passed (Planned pre-promotion evidence)")


if __name__ == "__main__":
    main()
