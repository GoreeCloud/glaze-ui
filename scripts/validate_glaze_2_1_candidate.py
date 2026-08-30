#!/usr/bin/env python3
"""Fail-closed structural validation for the Glaze UI 2.1 Candidate foundation.

This validator checks objective repository invariants only. Human Visual Excellence
review and rendered/native acceptance remain separate evidence and are never
manufactured by this script.
"""

from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

ERRORS: list[str] = []
RECOMMENDATIONS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def recommend(message: str) -> None:
    RECOMMENDATIONS.append(message)


def read_text(path: str) -> str:
    target = ROOT / path
    if not target.is_file():
        fail(f"missing required file: {path}")
        return ""
    return target.read_text(encoding="utf-8")


def read_json(path: str) -> dict:
    raw = read_text(path)
    if not raw:
        return {}
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path}: {exc}")
        return {}
    if not isinstance(value, dict):
        fail(f"expected object at top level: {path}")
        return {}
    return value


def require_keys(obj: dict, keys: tuple[str, ...], label: str) -> None:
    for key in keys:
        if key not in obj:
            fail(f"{label} missing required key: {key}")


def require_nonempty_string(value: object, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        fail(f"{label} must be a non-empty string")


def check_range(value: object, label: str, *, minimum: float = 0.0, maximum: float | None = None) -> None:
    if not isinstance(value, list) or len(value) != 2:
        fail(f"{label} must be a two-number range")
        return
    lo, hi = value
    if not isinstance(lo, (int, float)) or not isinstance(hi, (int, float)):
        fail(f"{label} range values must be numeric")
        return
    if lo > hi:
        fail(f"{label} lower bound must not exceed upper bound")
    if lo < minimum:
        fail(f"{label} lower bound must be >= {minimum}")
    if maximum is not None and hi > maximum:
        fail(f"{label} upper bound must be <= {maximum}")


def main() -> int:
    version = read_text("VERSION").strip()
    if version != "2.0.0":
        fail(f"2.1 Candidate must not change current Stable VERSION; expected 2.0.0, got {version!r}")

    candidate = read_text("GLAZE_UI_2_1_CANDIDATE.md")
    visual = read_text("VISUAL_EXCELLENCE.md")
    registry = read_json("registry/lifecycle.json")
    component_schema = read_json("schemas/component-contract.schema.json")
    material_schema = read_json("schemas/material-contract.schema.json")
    a11y_schema = read_json("schemas/accessibility-resolution.schema.json")
    capsule = read_json("contracts/components/navigation-capsule.json")
    material = read_json("contracts/materials/glaze-material-2.1.json")
    a11y = read_json("contracts/accessibility/resolution-matrix.json")

    candidate_markers = (
        "Status: **Candidate**",
        "2.1.0-candidate.1",
        "Current Stable remains: **2.0.0**",
        "Make interaction feel tangible. Make every interface feel intentional. Make GoreeCloud beautiful.",
        "Visual Excellence",
        "Accessibility Resolution Matrix",
        "Material Budgets",
        "Glaze Recipes",
        "Nothing teleports.",
        "2.0.0 remains the only current Stable Glaze UI consumer target",
    )
    for marker in candidate_markers:
        if marker not in candidate:
            fail(f"Candidate contract missing required marker: {marker}")

    visual_markers = (
        "Objective conformance",
        "Human visual review",
        "Optical correctness",
        "Accessibility-mode beauty",
        "Performance fallback beauty",
        "does not change the current Stable target from 2.0.0",
    )
    for marker in visual_markers:
        if marker not in visual:
            fail(f"Visual Excellence contract missing required marker: {marker}")

    require_keys(
        registry,
        ("schemaVersion", "currentStable", "activeCandidate", "lifecycleDefinitions", "releases", "capabilities", "promotionRules"),
        "lifecycle registry",
    )
    if registry.get("currentStable") != "2.0.0":
        fail("lifecycle registry currentStable must remain 2.0.0")
    if registry.get("activeCandidate") != "2.1.0-candidate.1":
        fail("lifecycle registry activeCandidate must be 2.1.0-candidate.1")

    releases = registry.get("releases", [])
    if not isinstance(releases, list):
        fail("lifecycle registry releases must be an array")
        releases = []
    stable = [r for r in releases if isinstance(r, dict) and r.get("version") == "2.0.0"]
    candidate_release = [r for r in releases if isinstance(r, dict) and r.get("version") == "2.1.0-candidate.1"]
    if len(stable) != 1 or stable[0].get("status") != "stable" or stable[0].get("consumerEligible") is not True:
        fail("registry must contain exactly one consumer-eligible Stable 2.0.0 release")
    if len(candidate_release) != 1 or candidate_release[0].get("status") != "candidate" or candidate_release[0].get("consumerEligible") is not False:
        fail("registry must contain exactly one non-consumer-eligible 2.1.0-candidate.1 release")

    capabilities = registry.get("capabilities", {})
    if not isinstance(capabilities, dict):
        fail("lifecycle registry capabilities must be an object")
        capabilities = {}
    allowed_lifecycles = {"stable", "candidate", "experimental", "planned", "deprecated", "historical"}
    for name, record in capabilities.items():
        if not isinstance(record, dict):
            fail(f"capability {name} must be an object")
            continue
        if record.get("status") not in allowed_lifecycles:
            fail(f"capability {name} has invalid lifecycle status: {record.get('status')!r}")

    required_candidate_impl = {
        "visual-excellence-gate": "VISUAL_EXCELLENCE.md",
        "canonical-lifecycle-registry": "registry/lifecycle.json",
        "machine-readable-component-contracts": "schemas/component-contract.schema.json",
        "navigation-capsule-2.1": "contracts/components/navigation-capsule.json",
        "machine-readable-material-contracts": "schemas/material-contract.schema.json",
        "material-budgets": "contracts/materials/glaze-material-2.1.json",
        "deterministic-material-behavior": "contracts/materials/glaze-material-2.1.json",
        "adaptive-optical-engine": "contracts/materials/glaze-material-2.1.json",
        "machine-readable-accessibility-resolution": "schemas/accessibility-resolution.schema.json",
        "accessibility-resolution-matrix": "contracts/accessibility/resolution-matrix.json",
        "performance-profiles": "contracts/materials/glaze-material-2.1.json",
    }
    for capability, implementation in required_candidate_impl.items():
        record = capabilities.get(capability, {})
        if record.get("status") != "candidate":
            fail(f"required 2.1 capability is not Candidate: {capability}")
        if record.get("implementation") != implementation:
            fail(f"{capability} must point to {implementation}")

    for required_candidate in ("glaze-recipes", "expanded-conformance-linter"):
        if capabilities.get(required_candidate, {}).get("status") != "candidate":
            fail(f"required 2.1 foundation capability is not Candidate: {required_candidate}")

    if capabilities.get("glaze-motion", {}).get("status") != "experimental":
        fail("Glaze Motion must remain Experimental unless separately promoted")

    rules = registry.get("promotionRules", {})
    if not isinstance(rules, dict):
        fail("promotionRules must be an object")
        rules = {}
    if rules.get("candidateMaySatisfyStableConsumerConformance") is not False:
        fail("Candidate must not satisfy Stable consumer conformance")
    if rules.get("stableVersionFileMustRemain") != "2.0.0":
        fail("promotion rule must pin Stable VERSION to 2.0.0 during Candidate work")
    if rules.get("requiresHumanVisualExcellenceReview") is not True:
        fail("2.1 promotion must require human Visual Excellence review")

    require_keys(component_schema, ("$schema", "$id", "title", "type", "required", "properties"), "component schema")
    schema_required = set(component_schema.get("required", [])) if isinstance(component_schema.get("required"), list) else set()
    contract_required = {
        "schemaVersion", "id", "name", "lifecycle", "semanticRole", "materialRole",
        "geometry", "states", "targets", "input", "accessibility", "density",
        "formFactors", "fallbacks", "visualReview",
    }
    missing_schema_requirements = contract_required - schema_required
    if missing_schema_requirements:
        fail(f"component schema does not require: {sorted(missing_schema_requirements)}")

    require_keys(capsule, tuple(contract_required), "Navigation Capsule contract")
    if capsule.get("lifecycle") != "candidate":
        fail("Navigation Capsule 2.1 contract must remain Candidate")
    materials = capsule.get("materialRole", {})
    if materials.get("default") != "soft-glaze":
        fail("Navigation Capsule default material must be Soft Glaze")
    targets = capsule.get("targets", {})
    if not isinstance(targets.get("touchMinPx"), int) or targets.get("touchMinPx", 0) < 48:
        fail("Navigation Capsule touch target must preserve the 48px Stable floor")
    if not isinstance(targets.get("tvMinPx"), int) or targets.get("tvMinPx", 0) < 56:
        fail("Navigation Capsule TV target must preserve the 56px Stable floor")

    expected_forms = {"mobile", "tablet", "desktop", "wide-desktop", "tv", "foldable", "resizable"}
    forms = set(capsule.get("formFactors", [])) if isinstance(capsule.get("formFactors"), list) else set()
    if not expected_forms.issubset(forms):
        fail(f"Navigation Capsule contract missing form factors: {sorted(expected_forms - forms)}")

    capsule_a11y = capsule.get("accessibility", {})
    for key in ("semantics", "reducedMotion", "reducedTransparency", "increasedContrast", "largeText", "forcedColors"):
        if not isinstance(capsule_a11y.get(key), str) or not capsule_a11y.get(key).strip():
            fail(f"Navigation Capsule accessibility mapping missing: {key}")

    review = capsule.get("visualReview", {})
    if review.get("required") is not True or not review.get("criteria"):
        fail("Navigation Capsule must require non-empty human visual review criteria")

    require_keys(material_schema, ("$schema", "$id", "title", "type", "required", "properties", "$defs"), "material schema")
    require_keys(
        material,
        ("schemaVersion", "id", "lifecycle", "materialLevels", "clarityProfiles", "performanceProfiles",
         "materialBudgets", "adaptiveOpticalInputs", "fallbackChain", "accessibilityOverrides", "invariants", "visualReview"),
        "material contract",
    )
    if material.get("lifecycle") != "candidate":
        fail("Glaze Material 2.1 contract must remain Candidate")

    expected_material_levels = {"canvas", "surface", "soft-glaze", "glaze", "deep-glaze", "live-glaze"}
    material_levels = material.get("materialLevels", {})
    if set(material_levels) != expected_material_levels:
        fail(f"material contract levels must be exactly {sorted(expected_material_levels)}")
    for name in expected_material_levels:
        level = material_levels.get(name, {})
        require_keys(level, ("role", "opacity", "blurPx", "saturation", "tintStrength", "refraction", "distortion", "boundary", "depth"), f"material level {name}")
        require_nonempty_string(level.get("role"), f"material level {name} role")
        check_range(level.get("opacity"), f"{name} opacity", minimum=0, maximum=1)
        check_range(level.get("blurPx"), f"{name} blurPx", minimum=0)
        check_range(level.get("saturation"), f"{name} saturation", minimum=0)
        check_range(level.get("tintStrength"), f"{name} tintStrength", minimum=0, maximum=1)

    if material_levels.get("canvas", {}).get("opacity") != [1.0, 1.0]:
        fail("Canvas must remain fully opaque")
    if material_levels.get("canvas", {}).get("blurPx") != [0, 0]:
        fail("Canvas must not depend on blur")
    if material_levels.get("surface", {}).get("refraction") != "none":
        fail("Surface must not depend on refraction")

    clarity = material.get("clarityProfiles", {})
    if set(clarity) != {"clear", "balanced", "solid"}:
        fail("Material Clarity profiles must be exactly Clear, Balanced and Solid")
    solid = clarity.get("solid", {})
    if solid.get("blurMultiplier") != 0.0 or solid.get("refractionEnabled") is not False or solid.get("distortionEnabled") is not False:
        fail("Solid clarity must disable blur scaling, refraction and distortion")

    performance = material.get("performanceProfiles", {})
    expected_performance = ["full", "balanced", "constrained", "minimal"]
    if set(performance) != set(expected_performance):
        fail("performance profiles must be exactly Full, Balanced, Constrained and Minimal")
    blur_caps: list[float] = []
    for name in expected_performance:
        profile = performance.get(name, {})
        require_keys(profile, ("maxBlurPx", "environmentSampling", "refraction", "distortion", "shadowComplexity", "motionComplexity", "lightingResponse"), f"performance profile {name}")
        cap = profile.get("maxBlurPx")
        if not isinstance(cap, (int, float)) or cap < 0:
            fail(f"performance profile {name} maxBlurPx must be non-negative")
        else:
            blur_caps.append(float(cap))
    if len(blur_caps) == 4 and blur_caps != sorted(blur_caps, reverse=True):
        fail("performance maxBlurPx must degrade monotonically Full → Balanced → Constrained → Minimal")
    minimal = performance.get("minimal", {})
    if minimal.get("maxBlurPx") != 0 or minimal.get("refraction") != "off" or minimal.get("distortion") != "off":
        fail("Minimal performance profile must disable blur, refraction and distortion")

    if material.get("fallbackChain") != ["advanced-glaze", "simplified-glaze", "tonal-surface", "solid-surface"]:
        fail("material fallback chain must be Advanced Glaze → Simplified Glaze → Tonal Surface → Solid Surface")

    budgets = material.get("materialBudgets", {})
    if budgets.get("metric") != "simultaneous-high-intensity-viewport-area-percent":
        fail("material budgets must use the canonical simultaneous viewport-area metric")
    recipe_budgets = budgets.get("recipes", {})
    expected_recipes = {"productivity", "communication", "media", "administration", "creative"}
    if set(recipe_budgets) != expected_recipes:
        fail("material budgets must define all five Glaze Recipes")
    for name in expected_recipes:
        budget = recipe_budgets.get(name, {})
        require_keys(budget, ("maxPercent", "maxDeepGlazeSurfaces", "maxLiveGlazeSurfaces"), f"material budget {name}")
        pct = budget.get("maxPercent")
        if not isinstance(pct, (int, float)) or not 0 <= pct <= 50:
            fail(f"material budget {name} maxPercent must be between 0 and 50")
    if recipe_budgets.get("administration", {}).get("maxPercent", 101) > recipe_budgets.get("productivity", {}).get("maxPercent", -1):
        fail("Administration material budget must not exceed Productivity")

    optical_inputs = set(material.get("adaptiveOpticalInputs", []))
    required_optical_inputs = {
        "background-complexity", "background-luminance", "foreground-contrast", "appearance",
        "material-clarity", "increased-contrast", "reduced-transparency", "display-capability",
        "performance-profile", "interaction-state", "surface-size", "ambient-color",
        "contextual-color", "interaction-direction",
    }
    if not required_optical_inputs.issubset(optical_inputs):
        fail(f"Adaptive Optical Engine missing inputs: {sorted(required_optical_inputs - optical_inputs)}")

    material_a11y = material.get("accessibilityOverrides", {})
    for key in ("reducedTransparency", "forcedColors"):
        override = material_a11y.get(key, {})
        if override.get("effectiveClarity") != "solid" or override.get("maxBlurPx") != 0:
            fail(f"{key} material override must force Solid and zero blur")
        if override.get("refraction") is not False or override.get("distortion") is not False:
            fail(f"{key} material override must disable refraction and distortion")

    material_review = material.get("visualReview", {})
    if material_review.get("required") is not True or not material_review.get("criteria"):
        fail("Glaze Material 2.1 must require human visual review")

    require_keys(a11y_schema, ("$schema", "$id", "title", "type", "required", "properties"), "accessibility resolution schema")
    require_keys(a11y, ("schemaVersion", "id", "lifecycle", "resolutionOrder", "preferences", "combinationRules", "protectedSemantics", "testCases", "visualReview"), "accessibility resolution matrix")
    if a11y.get("lifecycle") != "candidate":
        fail("Accessibility Resolution Matrix must remain Candidate")

    expected_preferences = {
        "reducedMotion", "reducedTransparency", "increasedContrast", "largeText", "showBoundaries",
        "touchAssistance", "forcedColors", "materialClarity", "accentPersonalization", "expressionLevel",
    }
    prefs = a11y.get("preferences", {})
    missing_prefs = expected_preferences - set(prefs)
    if missing_prefs:
        fail(f"Accessibility Resolution Matrix missing preferences: {sorted(missing_prefs)}")
    for name in expected_preferences:
        pref = prefs.get(name, {})
        require_nonempty_string(pref.get("source"), f"accessibility preference {name} source")
        if not isinstance(pref.get("effects"), list) or not pref.get("effects"):
            fail(f"accessibility preference {name} must define effects")

    order = a11y.get("resolutionOrder", [])
    if not isinstance(order, list) or not order or order[0] != "protected-semantic-meaning":
        fail("Accessibility resolution must preserve protected semantic meaning first")
    if "forced-colors" not in order or "expression-and-accent" not in order or order.index("forced-colors") > order.index("expression-and-accent"):
        fail("Forced Colors must resolve before expression/accent personalization")

    protected = set(a11y.get("protectedSemantics", []))
    required_protected = {"error", "warning", "destructive", "success", "privacy", "security", "focus", "protected", "restricted", "identity-trust", "offline", "unavailable"}
    if not required_protected.issubset(protected):
        fail(f"Accessibility matrix missing protected semantics: {sorted(required_protected - protected)}")

    cases = a11y.get("testCases", [])
    case_ids = {case.get("id") for case in cases if isinstance(case, dict)}
    expected_case_ids = {"rt-clear", "rm-expressive", "fc-accent", "large-compact", "touch-compact", "contrast-boundaries"}
    if not expected_case_ids.issubset(case_ids):
        fail(f"Accessibility resolution fixtures missing: {sorted(expected_case_ids - case_ids)}")

    a11y_review = a11y.get("visualReview", {})
    if a11y_review.get("required") is not True or not a11y_review.get("criteria"):
        fail("Accessibility Resolution Matrix must require human visual review")

    recommend("Add rendered reference-flow evidence for Clear, Balanced and Solid material modes before Stable promotion.")
    recommend("Exercise the accessibility resolution fixtures in native/web rendering harnesses and 200% text-scale acceptance before Stable promotion.")
    recommend("Add runtime Material Budget instrumentation and visual regression thresholds before Stable promotion.")
    recommend("Record human Visual Excellence evidence against exact promotion revisions before Stable promotion.")

    if RECOMMENDATIONS:
        print("Glaze UI 2.1 Candidate review recommendations:")
        for item in RECOMMENDATIONS:
            print(f"  - {item}")

    if ERRORS:
        print("Glaze UI 2.1 Candidate validation FAILED:", file=sys.stderr)
        for item in ERRORS:
            print(f"  - {item}", file=sys.stderr)
        return 1

    print("Glaze UI 2.1 Candidate foundation validation passed.")
    print("Material and accessibility contracts are structurally accepted at Candidate scope.")
    print("Current Stable remains 2.0.0; no Stable consumer promotion is implied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
