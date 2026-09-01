#!/usr/bin/env python3
"""Fail-closed validation for bounded Glaze UI 2.2 Structure contracts.

This validates objective contract structure and canonical component invariants.
It does not provide rendered, native/device, consumer, migration, or human
Visual Excellence evidence and therefore cannot by itself promote Structure
components to Candidate or Stable.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_DIR = ROOT / "contracts" / "components" / "2.2"
SCHEMA_PATH = ROOT / "schemas" / "component-contract-2.2.schema.json"
ERRORS: list[str] = []

STRUCTURE = {
    "glz-card.json": "GlzCard",
    "glz-list.json": "GlzList",
    "glz-table.json": "GlzTable",
    "glz-tabs.json": "GlzTabs",
    "glz-sidebar.json": "GlzSidebar",
    "glz-navigation-rail.json": "GlzNavigationRail",
    "glz-dock.json": "GlzDock",
    "glz-toolbar.json": "GlzToolbar",
}
STATE_PRIORITY = ["disabled", "error", "pressed", "focus", "selected", "hover", "rest"]
BASE_STATES = {"rest", "hover", "focus", "pressed", "selected", "disabled", "loading", "error"}
DENSITIES = {"compact", "standard", "comfortable", "far-view"}
FORM_FACTORS = {"mobile", "tablet", "desktop", "wide-desktop", "tv", "foldable", "resizable"}
TOP_LEVEL_REQUIRED = {
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


def size_map(contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    sizes = contract.get("sizes", [])
    if not isinstance(sizes, list):
        return {}
    return {item.get("name"): item for item in sizes if isinstance(item, dict) and isinstance(item.get("name"), str)}


def validate_schema(schema: dict[str, Any]) -> None:
    if schema.get("type") != "object" or schema.get("additionalProperties") is not False:
        fail("2.2 component schema must remain a closed object")
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        fail("2.2 component schema properties must be an object")
        return
    if "$schema" not in properties:
        fail("2.2 component schema must permit the contract-local $schema declaration")
    required = set(schema.get("required", [])) if isinstance(schema.get("required"), list) else set()
    missing = (TOP_LEVEL_REQUIRED - {"$schema"}) - required
    if missing:
        fail(f"2.2 component schema does not require: {sorted(missing)}")


def validate_common(filename: str, expected_name: str, contract: dict[str, Any], schema: dict[str, Any]) -> None:
    missing = TOP_LEVEL_REQUIRED - set(contract)
    if missing:
        fail(f"{filename} missing required keys: {sorted(missing)}")

    schema_props = schema.get("properties", {}) if isinstance(schema.get("properties"), dict) else {}
    allowed = set(schema_props)
    extras = set(contract) - allowed
    if extras:
        fail(f"{filename} has properties not permitted by the 2.2 schema: {sorted(extras)}")

    if contract.get("$schema") != "../../../schemas/component-contract-2.2.schema.json":
        fail(f"{filename} must reference the canonical local 2.2 component schema")
    if contract.get("schemaVersion") != 1:
        fail(f"{filename} schemaVersion must be 1")
    if contract.get("name") != expected_name:
        fail(f"{filename} name must be {expected_name}")
    expected_id = filename.removesuffix(".json").replace("glz-", "glz-") + "-2-2"
    if contract.get("id") != expected_id:
        fail(f"{filename} id must be {expected_id}")
    if contract.get("version") != "2.2.0-candidate.1":
        fail(f"{filename} version must remain 2.2.0-candidate.1")
    if contract.get("lifecycle") != "planned":
        fail(f"{filename} must remain Planned until separate Structure rendered evidence is accepted")
    if contract.get("tier") != "structure":
        fail(f"{filename} must remain in the Structure tier")
    nonempty(contract.get("semanticRole"), f"{filename} semanticRole")

    variants = contract.get("variants")
    if not isinstance(variants, list) or not variants or len(variants) != len(set(variants)):
        fail(f"{filename} variants must be a non-empty unique list")

    sizes = contract.get("sizes")
    if not isinstance(sizes, list) or not sizes:
        fail(f"{filename} sizes must be non-empty")
    else:
        seen: set[str] = set()
        for item in sizes:
            if not isinstance(item, dict):
                fail(f"{filename} size entries must be objects")
                continue
            name = item.get("name")
            if not isinstance(name, str) or not name:
                fail(f"{filename} size name missing")
                continue
            if name in seen:
                fail(f"{filename} duplicate size name: {name}")
            seen.add(name)
            visual = item.get("visualHeightPx")
            hit = item.get("touchHitMinPx")
            if not isinstance(visual, int) or visual <= 0:
                fail(f"{filename} {name} visualHeightPx must be a positive integer")
            if not isinstance(hit, int) or hit < 48:
                fail(f"{filename} {name} must preserve the 48px effective target floor")

    states = set(contract.get("states", [])) if isinstance(contract.get("states"), list) else set()
    if not BASE_STATES.issubset(states):
        fail(f"{filename} missing shared Structure states: {sorted(BASE_STATES - states)}")
    if contract.get("statePriority") != STATE_PRIORITY:
        fail(f"{filename} state priority drifted from shared 2.2 precedence")

    material = contract.get("material")
    if not isinstance(material, dict):
        fail(f"{filename} material must be an object")
    else:
        if material.get("glazeIsExceptional") is not True:
            fail(f"{filename} must explicitly keep Glaze exceptional")
        allowed_materials = material.get("allowed", [])
        if not isinstance(allowed_materials, list) or material.get("default") not in allowed_materials:
            fail(f"{filename} default material must be in allowed materials")
        nonempty(material.get("rule"), f"{filename} material.rule")

    targets = contract.get("targets")
    if not isinstance(targets, dict):
        fail(f"{filename} targets must be an object")
    else:
        if targets.get("touchMinPx", 0) < 48:
            fail(f"{filename} touchMinPx must be at least 48")
        if targets.get("touchAssistanceMinPx", 0) < 56:
            fail(f"{filename} Touch Assistance floor must be at least 56")

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
    if not isinstance(content, dict):
        fail(f"{filename} content must be an object")
    else:
        for key in ("overflow", "localization", "rtl"):
            nonempty(content.get(key), f"{filename} content.{key}")
        if content.get("textExpansionPercent") != [30, 50]:
            fail(f"{filename} must tolerate the documented 30–50% locale expansion")

    testing = contract.get("testing")
    if not isinstance(testing, dict):
        fail(f"{filename} testing must be an object")
    else:
        if set(testing.get("themes", [])) != {"light", "dark", "deep-dark"}:
            fail(f"{filename} must test light/dark/deep-dark")
        if set(testing.get("directions", [])) != {"ltr", "rtl"}:
            fail(f"{filename} must test LTR and RTL")
        if not {100, 200}.issubset(set(testing.get("textScalePercent", []))):
            fail(f"{filename} must test 100% and 200% text")
        if set(testing.get("motion", [])) != {"full", "reduced"}:
            fail(f"{filename} must test full and reduced motion")
        if not {"standard", "high", "forced-colors"}.issubset(set(testing.get("contrast", []))):
            fail(f"{filename} must test standard/high/forced-colors")
        if not {"mouse", "touch", "keyboard"}.issubset(set(testing.get("inputs", []))):
            fail(f"{filename} must test mouse, touch, and keyboard")

    review = contract.get("visualReview")
    if not isinstance(review, dict) or review.get("required") is not True or not review.get("criteria"):
        fail(f"{filename} must require non-empty human Visual Excellence review")


def validate_specific(filename: str, contract: dict[str, Any]) -> None:
    variants = contract.get("variants")
    sizes = size_map(contract)
    api = contract.get("api", {}) if isinstance(contract.get("api"), dict) else {}
    material = contract.get("material", {}) if isinstance(contract.get("material"), dict) else {}
    semantic = str(contract.get("semanticRole", "")).lower()
    content = contract.get("content", {}) if isinstance(contract.get("content"), dict) else {}

    if filename == "glz-card.json":
        if variants != ["plain", "raised", "interactive", "selected", "hero"]:
            fail("GlzCard variants drifted from sections 514–518")
        if material.get("default") != "surface" or "regular-glaze" not in material.get("allowed", []):
            fail("GlzCard must remain solid by default with Glaze only as an exceptional allowed variant")
        if sizes.get("standard", {}).get("radiusPx") != 20:
            fail("GlzCard standard radius must remain 20px")
        if not {"interactive", "selected"}.issubset(set(api.get("semanticProps", []))):
            fail("GlzCard API must expose semantic interactive and selected state")
    elif filename == "glz-list.json":
        if variants != ["plain", "inset", "grouped", "selectable", "reorderable"]:
            fail("GlzList variants drifted from sections 519–522")
        if [sizes.get(k, {}).get("visualHeightPx") for k in ("compact", "standard", "touch")] != [32, 40, 48]:
            fail("GlzList row heights must remain 32/40/48px")
        if "onReorder" not in api.get("events", []) or "dragHandle" not in api.get("slots", []):
            fail("GlzList reorderable contract must retain semantic event and drag-handle slot")
    elif filename == "glz-table.json":
        if variants != ["standard", "compact", "comfortable", "selectable"]:
            fail("GlzTable variants drifted from sections 525–528")
        if material.get("default") != "surface" or any(x in material.get("allowed", []) for x in ("thin-glaze", "regular-glaze", "thick-glaze")):
            fail("GlzTable data surfaces must remain solid/readability-first")
        direct = str(contract.get("input", {}).get("directManipulation", ""))
        if "8" not in direct or "12" not in direct or "1px" not in direct:
            fail("GlzTable must retain the visible 1px / 8–12px resize affordance contract")
        if not {"onSort", "onResize"}.issubset(set(api.get("events", []))):
            fail("GlzTable API must expose sort and resize semantics")
    elif filename == "glz-tabs.json":
        if variants != ["underline", "surface", "glaze"]:
            fail("GlzTabs variants drifted from sections 529–532")
        if "tablist" not in str(contract.get("accessibility", {}).get("role", "")).lower():
            fail("GlzTabs must retain the tablist/tab/tabpanel accessibility pattern")
        if "panel" not in api.get("slots", []) or "onSelect" not in api.get("events", []):
            fail("GlzTabs API must retain panel and selection semantics")
    elif filename == "glz-sidebar.json":
        rule = str(material.get("rule", ""))
        if "220" not in rule or "320" not in rule:
            fail("GlzSidebar must retain the 220–320px desktop width intent")
        if not {"collapsed", "expanded", "dragging"}.issubset(set(contract.get("states", []))):
            fail("GlzSidebar must model collapsed, expanded, and resizing/dragging states")
        if not {"width", "minWidth", "maxWidth", "resizable"}.issubset(set(api.get("semanticProps", []))):
            fail("GlzSidebar API must expose semantic width and resize constraints")
    elif filename == "glz-navigation-rail.json":
        rule = str(material.get("rule", ""))
        if "64" not in rule or "72" not in rule or "four to seven" not in semantic:
            fail("GlzNavigationRail must retain 64–72px width and four-to-seven primary destinations")
        if [sizes.get(k, {}).get("visualHeightPx") for k in ("compact", "standard", "touch")] != [44, 48, 56]:
            fail("GlzNavigationRail visual targets must remain 44/48/56px with effective floors")
        if "primaryNav" not in api.get("slots", []):
            fail("GlzNavigationRail must keep a stable primary navigation slot")
    elif filename == "glz-dock.json":
        if "three to five" not in semantic:
            fail("GlzDock must remain constrained to three to five primary destinations")
        if material.get("default") != "regular-glaze":
            fail("GlzDock floating default must remain restrained Regular Glaze")
        if [sizes.get(k, {}).get("visualHeightPx") for k in ("compact", "standard")] != [64, 72]:
            fail("GlzDock heights must remain 64/72px")
        if "safeAreaInset" not in api.get("semanticProps", []):
            fail("GlzDock must expose safe-area semantics")
    elif filename == "glz-toolbar.json":
        if [sizes.get(k, {}).get("visualHeightPx") for k in ("compact", "standard", "touch")] != [44, 52, 60]:
            fail("GlzToolbar container heights must remain 44/52/60px")
        if not {"priorities", "overflow"}.issubset(set(api.get("semanticProps", []))):
            fail("GlzToolbar must expose priority and overflow semantics")
        overflow = str(content.get("overflow", ""))
        if not all(marker in overflow for marker in ("P1", "P2", "P3", "P4")):
            fail("GlzToolbar must retain the P1/P2/P3/P4 responsive priority model")


def main() -> int:
    schema = read_json(SCHEMA_PATH)
    validate_schema(schema)

    for filename, expected_name in STRUCTURE.items():
        contract = read_json(CONTRACT_DIR / filename)
        if contract:
            validate_common(filename, expected_name, contract, schema)
            validate_specific(filename, contract)

    if ERRORS:
        print("Glaze UI 2.2 Structure contract validation failed:")
        for error in ERRORS:
            print(f"- {error}")
        return 1

    print("Glaze UI 2.2 Structure contract validation passed.")
    print("Validated eight Planned Structure contracts; no Candidate/Stable promotion is inferred.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
