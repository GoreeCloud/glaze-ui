#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / "tokens" / "iconography.json"
DOC = ROOT / "ICONOGRAPHY.md"


def fail(message: str) -> None:
    raise SystemExit(f"iconography validation failed: {message}")


def require_true(mapping: dict, keys: list[str], scope: str) -> None:
    for key in keys:
        if mapping.get(key) is not True:
            fail(f"{scope} invariant {key} must be true")


def main() -> None:
    if not TOKENS.is_file():
        fail("tokens/iconography.json is missing")
    if not DOC.is_file():
        fail("ICONOGRAPHY.md is missing")

    data = json.loads(TOKENS.read_text(encoding="utf-8"))
    meta = data.get("meta", {})
    if meta.get("status") != "stable":
        fail("iconography contract must remain Stable until promotion")
    if meta.get("stableBaseline") != "1.5.0":
        fail("Stable baseline must remain 1.5.0")
    if data.get("principle") != "identity remains stable while presentation adapts":
        fail("canonical final iconography rule changed unexpectedly")
    if data.get("visualGrammar") != "recognizable identity within a shared visual language":
        fail("canonical iconography visual grammar changed unexpectedly")

    grid = data.get("grid", {})
    if grid.get("canvas") != 1024 or grid.get("opticalCenter") != [512, 512]:
        fail("master icon grid must remain 1024 with a centered optical origin")
    for boundary in ["presentationBoundary", "safeArea", "primaryRegion", "coreIdentityZone"]:
        if not isinstance(grid.get(boundary, {}).get("inset"), int):
            fail(f"grid boundary {boundary} must define an integer inset")
    if not (
        grid["presentationBoundary"]["inset"]
        < grid["safeArea"]["inset"]
        < grid["primaryRegion"]["inset"]
        < grid["coreIdentityZone"]["inset"]
    ):
        fail("grid boundaries must become progressively more protected")
    require_true(grid, ["controlledOvershoot", "opticalCorrection"], "grid")
    required_keylines = {"circle", "square", "rounded-rectangle", "vertical", "horizontal", "freeform"}
    if set(grid.get("keylines", [])) != required_keylines:
        fail("master keyline families are incomplete")

    classes = data.get("classes", {})
    required_classes = {"application", "service", "system", "functional", "semantic", "file", "folder", "device"}
    if set(classes) != required_classes:
        fail("icon classes are incomplete or unexpected")
    app = classes["application"]
    if app.get("layerSequence") != ["foundation", "material", "identity", "detail", "light"]:
        fail("application five-layer sequence is required")
    if set(app.get("requiredLayers", [])) != {"foundation", "identity"}:
        fail("application Foundation and Identity layers must remain required")
    if set(app.get("optionalLayers", [])) != {"material", "detail", "light"}:
        fail("application optional layer set changed unexpectedly")
    if app.get("identityDominant") is not True:
        fail("application Identity layer must remain visually dominant")
    service = classes["service"]
    if service.get("layerSequence") != ["foundation", "capability-symbol", "state"]:
        fail("service hierarchy must remain Foundation, Capability Symbol, State")
    if service.get("launchable") is not False:
        fail("service visual category must remain non-launchable")
    if classes["device"].get("photorealistic") is not False:
        fail("device icons must remain simplified rather than photorealistic")

    required_materials = {"clearGlaze", "softGlaze", "denseGlaze", "tintedGlaze", "luminousGlaze", "solid"}
    if set(data.get("materials", {})) != required_materials:
        fail("Glaze icon material family is incomplete")
    lighting = data.get("lighting", {})
    for forbidden in ["harshSpotlight", "heavyDropShadow", "excessiveBloom", "plasticGloss"]:
        if lighting.get(forbidden) is not False:
            fail(f"lighting prohibition {forbidden} must remain false")

    required_color_roles = {
        "identity.primary", "identity.secondary", "identity.surface", "identity.highlight",
        "identity.glaze", "identity.foreground", "semantic.success", "semantic.information",
        "semantic.warning", "semantic.danger", "semantic.privacy", "semantic.security",
        "state.selected", "state.disabled", "state.unavailable"
    }
    if set(data.get("colorRoles", [])) != required_color_roles:
        fail("icon color-role contract is incomplete")

    identity_lock = data.get("identityLock", {})
    require_true(identity_lock, ["required", "mustSurviveAdaptivePresentation"], "identity lock")

    optical = data.get("opticalSizes", {})
    if list(optical) != ["display", "standard", "compact", "micro"]:
        fail("optical-size roles must be display, standard, compact, micro")
    sizes = [optical[k].get("minPx") for k in optical]
    if sizes != sorted(sizes, reverse=True):
        fail("optical-size minimums must descend from display to micro")
    for name, contract in optical.items():
        if contract.get("independentVariant") is not True:
            fail(f"optical size {name} must remain an independently authored variant")

    glyphs = data.get("glyphs", {})
    if glyphs.get("opticalSizes") != ["compact", "standard", "large", "display"]:
        fail("functional glyph optical-size family is incomplete")
    require_true(glyphs, ["strokeFamilyLimited", "filledStatePreservesPerceivedWeight"], "glyph")

    required_semantics = {"success", "information", "warning", "danger", "privacy", "security", "protected", "restricted", "online", "offline", "syncing", "paused", "unavailable"}
    if set(data.get("semanticRoles", [])) != required_semantics:
        fail("semantic icon roles are incomplete")
    if data.get("authority", {}).get("privacy") != "Privacy Shield":
        fail("Privacy Shield must remain authoritative for privacy truth")
    if data.get("authority", {}).get("security") != "Wardveil Security":
        fail("Wardveil Security must remain authoritative for security truth")

    badges = data.get("badges", {})
    if badges.get("maxVisibleCompact") != 1:
        fail("compact badge stacking must remain bounded to one visible priority badge")
    if badges.get("overflowTreatment") != "compound-or-expanded-labeled-status":
        fail("badge overflow must use compound or expanded labeled status treatment")
    if badges.get("priorityRule") != "semantic-severity-then-contextual-importance":
        fail("compound-state badge priority rule changed unexpectedly")
    require_true(badges, ["criticalSecurityOutranksSync", "ordinaryNotificationMustNotObscureError"], "badge priority")

    adaptive = data.get("adaptiveColor", {})
    require_true(adaptive, ["protectedSemantics", "stableRecognitionGeometry"], "adaptive color")
    if adaptive.get("darkModeSimpleInvert") is not False:
        fail("dark mode must not simply invert icon artwork")

    representations = data.get("representations", {})
    if representations.get("monochrome", {}).get("requiredForImportantApplicationAndService") is not True:
        fail("important application and service identities require monochrome representation")
    if representations.get("monochrome", {}).get("grayscaleConversionOnly") is not False:
        fail("monochrome representation must not be grayscale-only conversion")
    require_true(representations.get("highContrast", {}), ["purposeBuilt"], "high-contrast representation")
    require_true(representations.get("reducedTransparency", {}), ["replaceGlazeWithOpaqueEquivalent", "preserveLayerRelationships"], "reduced-transparency representation")

    access = data.get("accessibility", {})
    require_true(access, ["nonColorMeaningRequired", "accessibleNamesForInteractiveIcons", "grayscale", "highContrast", "reducedTransparency", "forcedColors", "reducedMotion", "silhouetteRecognition"], "accessibility")

    motion = data.get("motion", {})
    if motion.get("continuousDecorativeAnimation") is not False:
        fail("continuous decorative animation must remain prohibited")
    require_true(motion, ["purposeOnly", "objectContinuityPreferred", "continuousOnlyWhenActivityMeaningful", "interruptible", "staticReducedMotionAlternative", "returnsToStableStateNormally"], "motion")

    validation = data.get("validation", {})
    required_axes = {"recognition", "consistency", "adaptability", "craftsmanship"}
    if set(validation.get("qualityAxes", [])) != required_axes:
        fail("all four icon quality axes are required")
    required_checks = {"safe-area", "contrast", "optical-size-support", "badge-clearance", "monochrome-compatibility", "accessibility-behavior", "semantic-color-usage", "required-resolutions", "technical-asset-integrity"}
    if set(validation.get("checks", [])) != required_checks:
        fail("icon validation/certification checks are incomplete")

    certification = data.get("certification", {})
    if certification.get("status") != "planned":
        fail("Native Icon certification must remain Planned until implemented")

    authoring = data.get("authoring", {})
    if authoring.get("dedicatedIconStudioPlanned") is not False:
        fail("dedicated Icon Studio must remain retired unless a new explicit project decision is made")
    required_authoring_outcomes = {
        "master-grid-review", "keyline-review", "safe-area-review", "optical-boundary-review",
        "badge-collision-review", "appearance-preview", "accessibility-preview", "contrast-review",
        "fine-geometry-review", "launcher-grid-review", "optical-size-validation", "reproducible-export"
    }
    if set(authoring.get("requiredOutcomes", [])) != required_authoring_outcomes:
        fail("authoring and review outcomes are incomplete")

    tooling = data.get("tooling", {})
    if "iconStudio" in tooling:
        fail("Icon Studio must not remain in the tooling roadmap")
    if tooling.get("systemIconRegistry", {}).get("status") != "planned":
        fail("System Icon Registry must remain Planned until implemented")

    required_design_tokens = {
        "icon.size.micro", "icon.size.compact", "icon.size.standard", "icon.size.display",
        "icon.stroke.standard", "icon.corner.continuous", "icon.material.softGlaze",
        "icon.material.denseGlaze", "icon.identity.primary", "icon.state.selected",
        "icon.state.disabled", "icon.badge.notification", "icon.badge.semantic", "icon.motion.transition"
    }
    if set(data.get("designTokens", [])) != required_design_tokens:
        fail("semantic icon design-token contract is incomplete")

    if data.get("thirdParty", {}).get("mustNotFalselyRebrand") is not True:
        fail("third-party identity protection is required")

    doc = DOC.read_text(encoding="utf-8")
    for phrase in [
        "identity remains stable while presentation adapts",
        "1024 × 1024 master coordinate system",
        "Foundation → Capability Symbol → State",
        "Privacy Shield is authoritative for privacy truth",
        "Wardveil Security is authoritative for security truth",
        "Responsive iconography is not simple asset scaling",
        "Glaze UI Native Icon",
        "does **not** plan a dedicated Icon Studio application",
        "System Icon Registry",
        "Stable promotion boundary",
    ]:
        if phrase not in doc:
            fail(f"documentation invariant missing: {phrase}")

    print("Glaze UI iconography Stable production-contract validation passed")


if __name__ == "__main__":
    main()
