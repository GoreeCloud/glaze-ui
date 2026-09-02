#!/usr/bin/env python3
"""Fail-closed validation for Glaze UI 2.2 Signature + Intelligence components.

Passing proves the ten advanced component contracts are present and satisfy the
bounded Candidate contract invariants. It does not establish full-release
rendered acceptance, native/device acceptance, migration, performance,
Human Visual Excellence, consumer eligibility, or Stable promotion.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_DIR = ROOT / "contracts" / "components" / "2.2"
SCHEMA_PATH = ROOT / "schemas" / "component-contract-2.2.schema.json"
ERRORS: list[str] = []

COMPONENTS = {
    "glz-capsule.json": ("GlzCapsule", "signature"),
    "glz-morph-card.json": ("GlzMorphCard", "signature"),
    "glz-smart-rail.json": ("GlzSmartRail", "signature"),
    "glz-aurora-surface.json": ("GlzAuroraSurface", "signature"),
    "glz-universal-search.json": ("GlzUniversalSearch", "signature"),
    "glz-ai-action.json": ("GlzAIAction", "intelligence"),
    "glz-ai-suggestion.json": ("GlzAISuggestion", "intelligence"),
    "glz-ai-answer.json": ("GlzAIAnswer", "intelligence"),
    "glz-smart-summary.json": ("GlzSmartSummary", "intelligence"),
    "glz-source-chip.json": ("GlzSourceChip", "intelligence"),
}
STATE_PRIORITY = ["disabled", "error", "pressed", "focus", "selected", "hover", "rest"]
DENSITIES = {"compact", "standard", "comfortable", "far-view"}
FORM_FACTORS = {"mobile", "tablet", "desktop", "wide-desktop", "tv", "foldable", "resizable"}
REQUIRED = {
    "$schema","schemaVersion","id","name","version","lifecycle","tier","semanticRole",
    "variants","sizes","states","statePriority","material","targets","input","accessibility",
    "density","formFactors","fallbacks","api","content","testing","visualReview",
}

def fail(message: str) -> None: ERRORS.append(message)

def read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}"); return {}
    try: value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}"); return {}
    if not isinstance(value, dict):
        fail(f"top-level JSON must be an object: {path.relative_to(ROOT)}"); return {}
    return value

def text(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip(): fail(f"{label} must be non-empty")

def validate_schema(schema: dict[str, Any]) -> None:
    props = schema.get("properties", {}) if isinstance(schema.get("properties"), dict) else {}
    if schema.get("type") != "object" or schema.get("additionalProperties") is not False:
        fail("2.2 component schema must remain a closed object")
    tiers = props.get("tier", {}).get("enum", []) if isinstance(props.get("tier"), dict) else []
    if not {"signature","intelligence"}.issubset(set(tiers)):
        fail("2.2 component schema must retain Signature and Intelligence tiers")

def validate_common(filename: str, expected_name: str, expected_tier: str, c: dict[str, Any], schema: dict[str, Any]) -> None:
    missing = REQUIRED - set(c)
    if missing: fail(f"{filename} missing required keys: {sorted(missing)}")
    allowed = set(schema.get("properties", {})) if isinstance(schema.get("properties"), dict) else set()
    extras = set(c) - allowed
    if extras: fail(f"{filename} has schema-forbidden keys: {sorted(extras)}")
    if c.get("$schema") != "../../../schemas/component-contract-2.2.schema.json": fail(f"{filename} schema reference drifted")
    if c.get("schemaVersion") != 1: fail(f"{filename} schemaVersion must be 1")
    if c.get("id") != filename.removesuffix(".json") + "-2-2": fail(f"{filename} id drifted")
    if c.get("name") != expected_name: fail(f"{filename} name must be {expected_name}")
    if c.get("version") != "2.2.0-candidate.1" or c.get("lifecycle") != "candidate":
        fail(f"{filename} must remain 2.2.0-candidate.1 Candidate")
    if c.get("tier") != expected_tier: fail(f"{filename} tier must be {expected_tier}")
    text(c.get("semanticRole"), f"{filename} semanticRole")
    if c.get("statePriority") != STATE_PRIORITY: fail(f"{filename} state priority drifted")
    if set(c.get("density", [])) != DENSITIES: fail(f"{filename} density coverage is incomplete")
    if set(c.get("formFactors", [])) != FORM_FACTORS: fail(f"{filename} form-factor coverage is incomplete")
    variants = c.get("variants")
    if not isinstance(variants, list) or not variants or len(variants) != len(set(variants)): fail(f"{filename} variants must be unique and non-empty")
    sizes = c.get("sizes")
    if not isinstance(sizes, list) or not sizes: fail(f"{filename} sizes must be non-empty")
    else:
        names: set[str] = set()
        for size in sizes:
            if not isinstance(size, dict): fail(f"{filename} size entries must be objects"); continue
            name = size.get("name")
            if not isinstance(name, str) or not name or name in names: fail(f"{filename} size names must be unique")
            else: names.add(name)
            if not isinstance(size.get("visualHeightPx"), int) or size["visualHeightPx"] <= 0: fail(f"{filename} {name} visualHeightPx must be positive")
            if not isinstance(size.get("touchHitMinPx"), int) or size["touchHitMinPx"] < 48: fail(f"{filename} {name} must preserve 48px effective touch target")
    target = c.get("targets", {})
    if not isinstance(target, dict) or target.get("touchMinPx", 0) < 48 or target.get("touchAssistanceMinPx", 0) < 56:
        fail(f"{filename} must preserve 48px touch and 56px Touch Assistance floors")
    material = c.get("material", {})
    if not isinstance(material, dict) or material.get("default") not in material.get("allowed", []): fail(f"{filename} material default must be allowed")
    else: text(material.get("rule"), f"{filename} material.rule")
    for block, keys in {
        "input": ("keyboard","focus","hover","press"),
        "accessibility": ("role","name","state","value","keyboard","focus","errorAssociation","reducedMotion","reducedTransparency","increasedContrast","forcedColors","largeText"),
        "fallbacks": ("reducedMotion","reducedTransparency","highContrast","forcedColors","performance"),
    }.items():
        value = c.get(block)
        if not isinstance(value, dict): fail(f"{filename} {block} must be an object"); continue
        for key in keys: text(value.get(key), f"{filename} {block}.{key}")
    if c.get("accessibility", {}).get("nonColorMeaning") is not True: fail(f"{filename} must prohibit color-only meaning")
    api = c.get("api", {})
    if not isinstance(api, dict) or api.get("rawVisualPropsPreferred") is not False: fail(f"{filename} must prefer semantic APIs")
    else:
        for key in ("semanticProps","events","slots"):
            values = api.get(key)
            if not isinstance(values, list) or not values or len(values) != len(set(values)): fail(f"{filename} api.{key} must be unique and non-empty")
        for event in api.get("events", []):
            if not isinstance(event, str) or not event.startswith("on"): fail(f"{filename} event must use on* naming: {event!r}")
    if c.get("content", {}).get("textExpansionPercent") != [30, 50]: fail(f"{filename} must preserve 30–50% localization expansion")
    testing = c.get("testing", {})
    if not isinstance(testing, dict): fail(f"{filename} testing must be an object")
    else:
        if set(testing.get("themes", [])) != {"light","dark","deep-dark"}: fail(f"{filename} theme matrix incomplete")
        if set(testing.get("directions", [])) != {"ltr","rtl"}: fail(f"{filename} direction matrix incomplete")
        if not {100,200}.issubset(set(testing.get("textScalePercent", []))): fail(f"{filename} must test 100% and 200% text")
        if set(testing.get("motion", [])) != {"full","reduced"}: fail(f"{filename} motion matrix incomplete")
        if not {"standard","high","forced-colors"}.issubset(set(testing.get("contrast", []))): fail(f"{filename} contrast matrix incomplete")
        if not {"mouse","touch","keyboard"}.issubset(set(testing.get("inputs", []))): fail(f"{filename} input matrix incomplete")
    review = c.get("visualReview")
    if not isinstance(review, dict) or review.get("required") is not True or not review.get("criteria"):
        fail(f"{filename} must require Human Visual Excellence review")

def has_all(container: list[Any], required: set[str]) -> bool:
    return required.issubset({x for x in container if isinstance(x, str)})

def validate_specific(filename: str, c: dict[str, Any]) -> None:
    variants = c.get("variants", [])
    api = c.get("api", {}) if isinstance(c.get("api"), dict) else {}
    material = c.get("material", {}) if isinstance(c.get("material"), dict) else {}
    semantic = str(c.get("semanticRole", "")).lower()
    visual = " ".join(c.get("visualReview", {}).get("criteria", [])).lower()
    if filename == "glz-capsule.json":
        if variants != ["search","media","selection","status","progress","quick-actions","command-entry"]: fail("GlzCapsule role variants drifted")
        if material.get("default") != "regular-glaze" or "one coherent" not in semantic: fail("GlzCapsule must remain one coherent temporary task on Regular Glaze")
        if not has_all(api.get("events", []), {"onExpand","onCollapse","onDismiss"}): fail("GlzCapsule expansion/dismiss semantics incomplete")
    elif filename == "glz-morph-card.json":
        if not has_all(api.get("semanticProps", []), {"sharedElementId","accentIdentity","selected","expanded"}): fail("GlzMorphCard shared identity contract incomplete")
        if "crossfade" not in str(c.get("accessibility", {}).get("reducedMotion", "")).lower(): fail("GlzMorphCard must define Reduced Motion crossfade")
    elif filename == "glz-smart-rail.json":
        if not has_all(api.get("semanticProps", []), {"destinations","activeDestination","contextActions"}): fail("GlzSmartRail navigation/context API incomplete")
        if "do not jump" not in visual and "do not jump" not in str(c.get("content", {}).get("overflow", "")).lower(): fail("GlzSmartRail must explicitly preserve core destination position")
    elif filename == "glz-aurora-surface.json":
        if variants != ["subtle","standard","hero"]: fail("GlzAuroraSurface intensity levels must remain subtle/standard/hero")
        rule = str(material.get("rule", ""))
        for marker in ("8–10%","10–16%","16–24%"):
            if marker not in rule: fail(f"GlzAuroraSurface missing documented intensity marker {marker}")
        if material.get("default") != "surface": fail("GlzAuroraSurface must preserve a readable neutral Surface base")
    elif filename == "glz-universal-search.json":
        if not has_all(api.get("semanticProps", []), {"query","scope","groups","generatedAnswer","preview"}): fail("GlzUniversalSearch semantic model incomplete")
        keyboard = str(c.get("accessibility", {}).get("keyboard", ""))
        for marker in ("Ctrl/Command+K","arrows","Enter","Escape","second explicit step"):
            if marker.lower() not in keyboard.lower(): fail(f"GlzUniversalSearch keyboard/destructive rule missing: {marker}")
        if "generated" not in visual or "deterministic" not in visual: fail("GlzUniversalSearch must preserve deterministic-results-first visual hierarchy")
    elif filename == "glz-ai-action.json":
        if variants != ["quiet","surface","primary"] or "aurora spark" not in (semantic + " " + str(material.get("rule", "")).lower()): fail("GlzAIAction must be a restrained, explicitly identified AI action")
    elif filename == "glz-ai-suggestion.json":
        if "dismissible" not in semantic or "onDismiss" not in api.get("events", []): fail("GlzAISuggestion must remain dismissible")
    elif filename == "glz-ai-answer.json":
        if not has_all(api.get("semanticProps", []), {"answer","generated","confidenceLanguage","sources"}): fail("GlzAIAnswer provenance/confidence contract incomplete")
        if not has_all(api.get("slots", []), {"identifier","answer","sources","actions","feedback"}): fail("GlzAIAnswer anatomy incomplete")
    elif filename == "glz-smart-summary.json":
        if not has_all(api.get("semanticProps", []), {"summary","signals","sourceCount","expanded"}): fail("GlzSmartSummary anatomy incomplete")
    elif filename == "glz-source-chip.json":
        if not has_all(api.get("semanticProps", []), {"sourceId","title","location","kind"}): fail("GlzSourceChip provenance API incomplete")
        if "reveal" not in semantic: fail("GlzSourceChip activation must reveal the relevant source")

def main() -> None:
    schema = read_json(SCHEMA_PATH); validate_schema(schema)
    seen_ids: set[str] = set()
    for filename, (name, tier) in COMPONENTS.items():
        c = read_json(CONTRACT_DIR / filename)
        if not c: continue
        validate_common(filename, name, tier, c, schema); validate_specific(filename, c)
        cid = c.get("id")
        if cid in seen_ids: fail(f"duplicate advanced component id: {cid}")
        if isinstance(cid, str): seen_ids.add(cid)
    if len(seen_ids) != len(COMPONENTS): fail("advanced component set must contain ten unique canonical contracts")
    if ERRORS:
        print("Glaze UI 2.2 advanced component validation failed:")
        for error in ERRORS: print(f"- {error}")
        raise SystemExit(1)
    print("Glaze UI 2.2 Signature + Intelligence component validation passed (Candidate lifecycle enforced)")

if __name__ == "__main__": main()
