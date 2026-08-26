#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "ICON_CONSTRUCTION.md"
TOKENS = ROOT / "tokens" / "icon-construction.json"
SCHEMA = ROOT / "schemas" / "icon-manifest.schema.json"
EXAMPLE = ROOT / "examples" / "icon-manifest.example.json"


def fail(message: str) -> None:
    raise SystemExit(f"icon construction validation failed: {message}")


def main() -> None:
    for path in (DOC, TOKENS, SCHEMA, EXAMPLE):
        if not path.is_file():
            fail(f"missing required file: {path.relative_to(ROOT)}")

    data = json.loads(TOKENS.read_text(encoding="utf-8"))
    meta = data.get("meta", {})
    if meta.get("status") != "candidate" or meta.get("stableBaseline") != "1.4.0":
        fail("construction contract must remain isolated 1.5 Candidate over Stable 1.4.0")

    canvas = data.get("canvas", {})
    if (canvas.get("width"), canvas.get("height"), canvas.get("origin")) != (1024, 1024, [512, 512]):
        fail("master canvas or optical origin changed")
    if canvas.get("zones") != {
        "canvasBoundaryPercent": 100,
        "presentationPercent": 90,
        "opticalSafePercent": 76,
        "coreIdentityPercent": 60,
    }:
        fail("construction-zone percentages changed")
    if canvas.get("opticalCorrection") is not True or canvas.get("controlledOvershoot") is not True:
        fail("optical correction and controlled overshoot are required")

    if data.get("keylines") != ["circular", "continuous-square", "vertical", "horizontal", "compact-object", "freeform"]:
        fail("keyline family contract changed")
    if data.get("curvatureLevels") != ["subtle", "standard", "expressive", "full"]:
        fail("curvature levels changed")
    if data.get("materialHierarchy") != ["background", "structural", "identity", "highlight"]:
        fail("material hierarchy changed")
    if data.get("applicationLayers") != ["foundation", "material", "identity", "detail", "light"]:
        fail("application layer sequence changed")
    if data.get("opticalRepresentations") != ["display", "standard", "compact", "micro"]:
        fail("optical representation sequence changed")
    if data.get("detailReductionSequence") != ["material-richness", "structural-clarity", "silhouette", "identity"]:
        fail("detail reduction sequence changed")
    if data.get("motionGrammar") != ["state-transition", "progress", "activity", "attention", "confirmation"]:
        fail("motion grammar changed")

    lock = data.get("identityLock", {})
    if lock.get("required") is not True:
        fail("Identity Lock must remain required")
    required_lock_fields = {"primary-geometry", "silhouette", "orientation", "negative-space", "proportions", "essential-color-relationships"}
    if set(lock.get("fields", [])) != required_lock_fields:
        fail("Identity Lock fields are incomplete")

    states = data.get("states", {})
    for key in ["selectionPrefersSurroundingSurfaceTreatment", "disabledDistinctFromUnavailable", "progressSeparateFromIdentity", "notificationDistinctFromSemanticBadge"]:
        if states.get(key) is not True:
            fail(f"state invariant missing: {key}")

    expected_validation = {"launcher-grid", "squint-blur", "grayscale", "micro", "badge-collision", "background-stress", "light-dark", "high-contrast", "reduced-transparency", "reduced-motion", "color-vision", "monochrome"}
    if set(data.get("validation", [])) != expected_validation:
        fail("validation matrix is incomplete")

    manifest = data.get("manifest", {})
    if manifest.get("schema") != "schemas/icon-manifest.schema.json" or manifest.get("example") != "examples/icon-manifest.example.json" or manifest.get("requiredForProductionPackage") is not True:
        fail("manifest binding changed")

    planned = data.get("plannedCapabilities", {})
    if "iconStudio" in planned:
        fail("Icon Studio must not remain in the construction roadmap")
    for name, status in planned.items():
        if status != "planned":
            fail(f"planned capability {name} must remain Planned")
    authoring = data.get("authoring", {})
    if authoring.get("dedicatedIconStudioPlanned") is not False:
        fail("dedicated Icon Studio must remain retired unless a new explicit project decision is made")
    if authoring.get("reviewAndExportRemainToolAgnostic") is not True:
        fail("icon review and export must remain tool-agnostic")

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    if schema.get("title") != "Glaze UI Icon Manifest":
        fail("icon manifest schema title changed")
    required = set(schema.get("required", []))
    for field in ["schemaVersion", "identity", "source", "opticalVariants", "identityLock", "accessibility", "badgeClearance", "adaptiveAppearance"]:
        if field not in required:
            fail(f"manifest schema missing required field {field}")
    optical_required = set(schema["properties"]["opticalVariants"].get("required", []))
    if optical_required != {"display", "standard", "compact", "micro"}:
        fail("manifest schema must require all four optical variants")

    example = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    if example.get("schemaVersion") != "1.0-candidate":
        fail("example manifest schema version changed")
    if example.get("source", {}).get("masterCanvas") != [1024, 1024]:
        fail("example manifest must use 1024 × 1024 source canvas")
    if set(example.get("opticalVariants", {})) != {"display", "standard", "compact", "micro"}:
        fail("example manifest must contain all optical variants")
    access = example.get("accessibility", {})
    if access.get("grayscaleRecognizable") is not True or access.get("colorIndependentRecognition") is not True:
        fail("example manifest must preserve non-color recognition")

    doc = DOC.read_text(encoding="utf-8")
    for phrase in [
        "1024 × 1024",
        "Presentation Zone",
        "Optical Safe Zone",
        "Core Identity Zone",
        "Subtle",
        "Standard",
        "Expressive",
        "Full",
        "Material richness → structural clarity → silhouette → identity",
        "responsive visual identity asset",
        "schemas/icon-manifest.schema.json",
        "does **not** plan a dedicated Icon Studio application",
        "Planned",
    ]:
        if phrase not in doc:
            fail(f"documentation invariant missing: {phrase}")

    print("Glaze UI icon construction Candidate validation passed")


if __name__ == "__main__":
    main()
