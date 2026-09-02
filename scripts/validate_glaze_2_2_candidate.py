#!/usr/bin/env python3
"""Fail-closed structural validation for the Glaze UI 2.2 Candidate foundation.

This validator proves objective repository invariants for the bounded
2.2.0-candidate.1 line. It does not manufacture rendered, native,
physical-device, consumer, or human Visual Excellence evidence.
"""

from __future__ import annotations

import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def read_text(path: str) -> str:
    target = ROOT / path
    if not target.is_file():
        fail(f"missing required file: {path}")
        return ""
    return target.read_text(encoding="utf-8")


def read_json(path: str) -> dict[str, Any]:
    raw = read_text(path)
    if not raw:
        return {}
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path}: {exc}")
        return {}
    if not isinstance(value, dict):
        fail(f"expected top-level object in {path}")
        return {}
    return value


def require_keys(obj: dict[str, Any], keys: tuple[str, ...], label: str) -> None:
    for key in keys:
        if key not in obj:
            fail(f"{label} missing required key: {key}")


def require_markers(text: str, markers: tuple[str, ...], label: str) -> None:
    for marker in markers:
        if marker not in text:
            fail(f"{label} missing required marker: {marker}")


def require_numeric_range(
    value: Any,
    label: str,
    *,
    expected: tuple[float, float] | None = None,
    minimum: float | None = None,
    maximum: float | None = None,
) -> None:
    if not isinstance(value, list) or len(value) != 2:
        fail(f"{label} must be a two-number range")
        return
    lo, hi = value
    if not isinstance(lo, (int, float)) or not isinstance(hi, (int, float)):
        fail(f"{label} values must be numeric")
        return
    if lo > hi:
        fail(f"{label} lower bound exceeds upper bound")
    if minimum is not None and lo < minimum:
        fail(f"{label} lower bound must be >= {minimum}")
    if maximum is not None and hi > maximum:
        fail(f"{label} upper bound must be <= {maximum}")
    if expected is not None and (lo, hi) != expected:
        fail(f"{label} must equal {list(expected)}, got {value}")


def validate_lifecycle(registry: dict[str, Any]) -> None:
    require_keys(
        registry,
        (
            "schemaVersion",
            "currentStable",
            "activeCandidate",
            "lifecycleDefinitions",
            "releases",
            "capabilities",
            "promotionRules",
        ),
        "lifecycle registry",
    )
    if registry.get("currentStable") != "2.1.0":
        fail("Glaze UI 2.2 Candidate must keep currentStable at 2.1.0")
    if registry.get("activeCandidate") != "2.2.0-candidate.1":
        fail("activeCandidate must be 2.2.0-candidate.1")

    releases = registry.get("releases")
    if not isinstance(releases, list):
        fail("lifecycle releases must be an array")
        releases = []
    stable = [r for r in releases if isinstance(r, dict) and r.get("version") == "2.1.0"]
    candidate = [r for r in releases if isinstance(r, dict) and r.get("version") == "2.2.0-candidate.1"]
    if len(stable) != 1:
        fail("lifecycle registry must contain exactly one 2.1.0 release")
    elif stable[0].get("status") != "stable" or stable[0].get("consumerEligible") is not True:
        fail("2.1.0 must remain consumer-eligible Stable")
    if len(candidate) != 1:
        fail("lifecycle registry must contain exactly one 2.2.0-candidate.1 release")
    elif candidate[0].get("status") != "candidate" or candidate[0].get("consumerEligible") is not False:
        fail("2.2.0-candidate.1 must be non-consumer-eligible Candidate")

    capabilities = registry.get("capabilities")
    if not isinstance(capabilities, dict):
        fail("lifecycle capabilities must be an object")
        capabilities = {}

    expected_candidate = {
        "glaze-ui-2.2-foundation-contract": "GLAZE_UI_2_2_CANDIDATE.md",
        "glaze-ui-2.2-core-token-contract": "tokens/glaze-2.2.candidate.json",
        "system-shell-contract-schema-2.2": "schemas/system-shell-contract.schema.json",
        "system-shell-foundation-2.2": "contracts/system-shell/glaze-system-shell-2.2.json",
        "web-candidate-foundation-2.2": "css/glaze-2.2.candidate.css",
        "candidate-validation-2.2": "scripts/validate_glaze_2_2_candidate.py",
    }
    for capability, implementation in expected_candidate.items():
        record = capabilities.get(capability)
        if not isinstance(record, dict):
            fail(f"missing lifecycle capability: {capability}")
            continue
        if record.get("status") != "candidate":
            fail(f"{capability} must be Candidate")
        if record.get("implementation") != implementation:
            fail(f"{capability} must point to {implementation}")
        if record.get("since") != "2.2.0-candidate.1":
            fail(f"{capability} must declare since=2.2.0-candidate.1")

    for planned in (
        "component-library-2.2-complete",
        "universal-search-runtime-2.2",
        "control-center-runtime-2.2",
        "native-system-shell-reference-2.2",
        "rendered-reference-acceptance-2.2",
        "visual-regression-2.2",
        "migration-2.1-to-2.2",
    ):
        record = capabilities.get(planned)
        if not isinstance(record, dict) or record.get("status") != "planned":
            fail(f"unimplemented 2.2 capability must remain Planned: {planned}")

    if capabilities.get("glaze-motion", {}).get("status") != "experimental":
        fail("Glaze Motion must remain Experimental unless separately promoted")

    rules = registry.get("promotionRules")
    if not isinstance(rules, dict):
        fail("promotionRules must be an object")
        return
    if rules.get("candidateMaySatisfyStableConsumerConformance") is not False:
        fail("Candidate must not satisfy Stable consumer conformance")
    if rules.get("stableVersionFileMustRemain") != "2.1.0":
        fail("stableVersionFileMustRemain must pin VERSION to 2.1.0")
    for required_true in (
        "requiresExactFinalRevisionCI",
        "requiresRenderedAcceptance",
        "requiresAccessibilityAndResilienceAcceptance",
        "requiresNativeOrDeviceEvidenceWhereApplicable",
        "requiresHumanVisualExcellenceReview",
    ):
        if rules.get(required_true) is not True:
            fail(f"promotion rule must require {required_true}")


def validate_tokens(tokens: dict[str, Any]) -> None:
    require_keys(
        tokens,
        (
            "meta",
            "interaction",
            "surface",
            "color",
            "geometry",
            "spacingPx",
            "targetPx",
            "typographyPx",
            "system",
            "motion",
            "material",
            "accessibility",
            "identity",
            "implementation",
        ),
        "2.2 token contract",
    )
    meta = tokens.get("meta", {})
    if meta.get("version") != "2.2.0-candidate.1":
        fail("2.2 tokens must declare candidate version 2.2.0-candidate.1")
    if meta.get("status") != "candidate":
        fail("2.2 tokens must remain Candidate")
    if meta.get("stableBaseline") != "2.1.0":
        fail("2.2 tokens must preserve stableBaseline 2.1.0")
    if meta.get("consumerEligible") is not False:
        fail("2.2 Candidate tokens must not be consumer eligible")

    interaction = tokens.get("interaction", {})
    if interaction.get("states") != ["rest", "hover", "focus", "pressed", "selected", "disabled", "loading", "error"]:
        fail("2.2 shared state vocabulary drifted")
    if interaction.get("statePriority") != ["disabled", "error", "pressed", "focus", "selected", "hover", "rest"]:
        fail("2.2 state priority drifted")
    layers = interaction.get("stateLayerOpacity", {})
    require_numeric_range(layers.get("hover"), "hover state opacity", expected=(0.03, 0.06), minimum=0, maximum=1)
    require_numeric_range(layers.get("pressed"), "pressed state opacity", expected=(0.07, 0.12), minimum=0, maximum=1)
    require_numeric_range(layers.get("selected"), "selected state opacity", expected=(0.08, 0.16), minimum=0, maximum=1)

    surface = tokens.get("surface", {})
    if surface.get("systemHierarchy") != ["workspace", "application", "system-overlay", "system-panel", "critical-system"]:
        fail("2.2 system surface hierarchy drifted")
    if surface.get("contentRule") != "Solid where you read. Glazed where you interact.":
        fail("2.2 content/material rule drifted")

    color = tokens.get("color", {})
    deep_dark = color.get("deepDark", {})
    if deep_dark.get("canvas") != "#05070A":
        fail("Deep Dark Canvas must be #05070A")
    if deep_dark.get("base") != "#0D1015":
        fail("Deep Dark Base must be #0D1015")
    if deep_dark.get("raised") != "#171C23":
        fail("Deep Dark Raised must be #171C23")
    require_numeric_range(color.get("ambientTintPercent"), "ambient tint percent", expected=(4, 10), minimum=0, maximum=100)
    if color.get("wallpaperSemanticOverrideAllowed") is not False:
        fail("wallpaper must not override semantic colors")

    targets = tokens.get("targetPx", {})
    if targets.get("touchShellMin", 0) < 48:
        fail("touch shell target floor must be at least 48px")
    if targets.get("touchAssistanceMin", 0) < 56:
        fail("Touch Assistance target floor must be at least 56px")
    if targets.get("farViewMin", 0) < 56:
        fail("far-view target floor must be at least 56px")

    typography = tokens.get("typographyPx", {})
    for key, expected in {
        "shellLabel": (13, 15),
        "panelTitle": (18, 22),
        "workspaceTitle": (22, 28),
        "lockTime": (56, 88),
        "systemSymbol": (20, 24),
    }.items():
        require_numeric_range(typography.get(key), f"typography {key}", expected=expected, minimum=1)

    system = tokens.get("system", {})
    budget = system.get("shellGlazeBudget", {})
    if budget.get("dominantPanelsMax") != 1:
        fail("system Glaze budget allows more than one dominant panel")
    if budget.get("smallFloatingControlsMin") != 1 or budget.get("smallFloatingControlsMax") != 3:
        fail("system small floating Glaze control budget must be 1–3")
    if budget.get("exceptionRequiresExplicitContext") is not True:
        fail("system Glaze budget exceptions must require explicit context")
    if system.get("blurStackRule") != "content -> single environmental diffusion -> foreground material":
        fail("system blur stack rule drifted")

    motion = tokens.get("motion", {})
    for key, expected in {
        "popoverMs": (160, 200),
        "controlCenterMs": (220, 280),
        "searchMs": (240, 320),
        "workspaceMs": (320, 420),
        "unlockMs": (280, 420),
    }.items():
        require_numeric_range(motion.get(key), f"motion {key}", expected=expected, minimum=0)
    if motion.get("directManipulationTracksInput") is not True:
        fail("direct manipulation must track input immediately")

    material = tokens.get("material", {})
    if material.get("workspace", {}).get("translucent") is not False:
        fail("Workspace foundation must not require translucency")
    if material.get("application", {}).get("translucent") is not False:
        fail("Application content foundation must not require translucency")
    if material.get("criticalSystem", {}).get("blurPx") != 0:
        fail("Critical System foundation must not require backdrop blur")

    accessibility = tokens.get("accessibility", {})
    required_independence = {"precision-gestures", "color", "transparency", "animation", "sound", "hover"}
    if not required_independence.issubset(set(accessibility.get("alternativePathMustNotDependOn", []))):
        fail("accessibility alternative-path independence is incomplete")
    for key in ("reducedTransparency", "reducedMotion", "increasedContrast", "forcedColors", "largeText", "keyboard", "touch", "pointer"):
        if accessibility.get(key) is not True:
            fail(f"2.2 token contract must support accessibility mode/input: {key}")
    if accessibility.get("semanticMeaningColorOnly") is not False:
        fail("semantic meaning must not be color-only")


def validate_shell_contract(shell: dict[str, Any]) -> None:
    require_keys(
        shell,
        (
            "schemaVersion",
            "id",
            "name",
            "version",
            "lifecycle",
            "stableBaseline",
            "consumerEligible",
            "scope",
            "surfaceClasses",
            "materialHierarchy",
            "glazeBudget",
            "motion",
            "targets",
            "accessibility",
            "privacy",
            "security",
            "responsive",
            "fallbacks",
            "implementation",
            "validation",
        ),
        "system shell contract",
    )
    if shell.get("version") != "2.2.0-candidate.1" or shell.get("lifecycle") != "candidate":
        fail("system shell contract must remain 2.2.0-candidate.1 Candidate")
    if shell.get("stableBaseline") != "2.1.0" or shell.get("consumerEligible") is not False:
        fail("system shell contract must preserve 2.1.0 Stable consumer boundary")
    if shell.get("surfaceClasses") != ["workspace", "application", "system-overlay", "system-panel", "critical-system"]:
        fail("system shell surface classes drifted")
    if shell.get("materialHierarchy", {}).get("nestedBackdropBlurAllowed") is not False:
        fail("nested backdrop blur must not be allowed")
    budget = shell.get("glazeBudget", {})
    if budget.get("dominantPanelMax") != 1 or budget.get("smallFloatingControlsMax") != 3:
        fail("system shell Glaze budget drifted")
    if shell.get("motion", {}).get("keyboardTraversalWaitsForAnimation") is not False:
        fail("keyboard traversal must not wait for animation")
    if shell.get("motion", {}).get("directManipulationTracksInput") is not True:
        fail("direct manipulation must track input")

    privacy = shell.get("privacy", {})
    for key in ("stateVisible", "stateUnderstandable", "stateActionable", "recordingIndicatorPersistent", "sensorUseDiscoverable"):
        if privacy.get(key) is not True:
            fail(f"system privacy contract missing required truth/presentation rule: {key}")
    security = shell.get("security", {})
    if security.get("criticalSurfacesBecomeMoreSolid") is not True:
        fail("critical system surfaces must become more solid")
    if security.get("explicitLanguageIncreasesWithStakes") is not True:
        fail("security language must become more explicit as stakes increase")
    if security.get("decorativeTransparencyRequired") is not False:
        fail("critical security UI must not require decorative transparency")

    not_claimed = set(shell.get("scope", {}).get("notClaimed", []))
    for boundary in ("operating-system-runtime", "native-system-shell-certification", "downstream-consumer-conformance", "stable-promotion"):
        if boundary not in not_claimed:
            fail(f"system shell contract must preserve explicit non-claim: {boundary}")


def validate_schema(schema: dict[str, Any]) -> None:
    require_keys(schema, ("$schema", "$id", "title", "type", "required", "properties", "$defs"), "system shell schema")
    required = set(schema.get("required", [])) if isinstance(schema.get("required"), list) else set()
    expected = {
        "schemaVersion", "id", "name", "version", "lifecycle", "stableBaseline", "consumerEligible",
        "scope", "surfaceClasses", "materialHierarchy", "glazeBudget", "motion", "targets",
        "accessibility", "privacy", "security", "responsive", "fallbacks", "implementation", "validation",
    }
    if not expected.issubset(required):
        fail(f"system shell schema does not require: {sorted(expected - required)}")


def validate_css(css: str) -> None:
    require_markers(
        css,
        (
            "Glaze UI 2.2 Candidate Foundation",
            "--glz22-canvas: #f5f7fa",
            "#05070a",
            "#0d1015",
            "#171c23",
            ".glz22-workspace",
            ".glz22-application",
            ".glz22-system-overlay",
            ".glz22-system-panel",
            ".glz22-critical-system",
            ".glz22-capsule",
            ".glz22-system-status",
            ".glz22-shell-control:focus-visible",
            "prefers-reduced-motion: reduce",
            "prefers-reduced-transparency: reduce",
            "prefers-contrast: more",
            "forced-colors: active",
            "data-glz-touch-assistance",
        ),
        "2.2 Candidate CSS",
    )
    if "@import" in css:
        fail("2.2 Candidate CSS must not depend on remote/imported presentation")
    if "http://" in css or "https://" in css:
        fail("2.2 Candidate CSS must remain local and must not contain remote presentation URLs")
    critical_start = css.find(".glz22-critical-system {")
    critical_end = css.find("}", critical_start)
    critical_block = css[critical_start:critical_end] if critical_start >= 0 and critical_end >= 0 else ""
    if "backdrop-filter: none" not in critical_block:
        fail("Critical System CSS must explicitly disable backdrop blur")


def main() -> int:
    version = read_text("VERSION").strip()
    if version != "2.1.0":
        fail(f"2.2 Candidate must not change Stable VERSION; expected 2.1.0, got {version!r}")

    stable_contract = read_text("GLAZE_UI_2_1_STABLE.md")
    require_markers(stable_contract, ("Lifecycle status:** Stable", "Stable semantic version:** 2.1.0"), "2.1 Stable contract")

    candidate = read_text("GLAZE_UI_2_2_CANDIDATE.md")
    require_markers(
        candidate,
        (
            "Lifecycle status:** Candidate",
            "2.2.0-candidate.1",
            "Current Stable remains:** 2.1.0",
            "Consumer eligible:** No",
            "Solid where you read. Glazed where you interact.",
            "Accessibility can simplify every visual effect without reducing capability.",
            "Security interfaces prioritize certainty over beauty.",
            "If any applicable gate is incomplete, Glaze UI 2.2 remains Candidate.",
            "No downstream GoreeCloud application is promoted by declaration.",
        ),
        "2.2 Candidate contract",
    )

    tokens = read_json("tokens/glaze-2.2.candidate.json")
    schema = read_json("schemas/system-shell-contract.schema.json")
    shell = read_json("contracts/system-shell/glaze-system-shell-2.2.json")
    registry = read_json("registry/lifecycle.json")
    css = read_text("css/glaze-2.2.candidate.css")
    acceptance = read_text("acceptance/2.2-candidate.md")
    workflow = read_text(".github/workflows/glaze-2.2-candidate.yml")

    validate_tokens(tokens)
    validate_schema(schema)
    validate_shell_contract(shell)
    validate_lifecycle(registry)
    validate_css(css)

    require_markers(
        acceptance,
        (
            "2.2.0-candidate.1",
            "Current Stable:** 2.1.0",
            "does not establish Stable promotion",
            "Optical Reachability static + 15-case rendered acceptance: **Passed**",
            "Android-native 2.2 Candidate emulator acceptance: **Passed**",
            "Active-presentation source-pinned pixel regression: **Pending new approved baseline**",
            "Human Visual Excellence review for the active Optical Reachability presentation: **Pending**",
            "Complete cross-platform native System Shell implementation: **Pending / Planned**",
            "Final-release exact-final-revision rendered/visual regression and lifecycle promotion checks: **Pending**",
        ),
        "2.2 Candidate acceptance record",
    )
    require_markers(
        workflow,
        (
            "name: Glaze UI 2.2 Candidate Foundation",
            "Check out exact source revision",
            "python3 scripts/validate_glaze_2_2_candidate.py",
            "python3 scripts/validate_release_state.py",
        ),
        "2.2 Candidate workflow",
    )

    if ERRORS:
        print("Glaze UI 2.2 Candidate foundation validation: FAIL", file=sys.stderr)
        for error in ERRORS:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Glaze UI 2.2 Candidate foundation validation: PASS")
    print("Stable consumer target remains 2.1.0; 2.2.0-candidate.1 is not consumer eligible.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
