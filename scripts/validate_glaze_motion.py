#!/usr/bin/env python3
"""Fail-closed validation for Glaze Motion 0.3 Experimental Motion Core."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / "tokens" / "glaze-motion.json"
DOC = ROOT / "GLAZE_MOTION.md"
NATIVE = ROOT / "NATIVE_MOTION_MAPPINGS.md"
CSS = ROOT / "css" / "glaze.motion.core.css"
RUNTIME = ROOT / "js" / "glaze.motion.js"
RUNTIME_TEST = ROOT / "tests" / "glaze-motion-runtime.test.mjs"
INTERACTION_TEST = ROOT / "tests" / "glaze-motion-interaction.test.mjs"
CONSUMER = ROOT / "reference" / "glaze-motion-consumer.mjs"
CONSUMER_TEST = ROOT / "tests" / "glaze-motion-consumer.test.mjs"
RENDERED = ROOT / "scripts" / "validate_glaze_motion_rendered.py"
REFERENCE = ROOT / "reference" / "glaze-motion.html"
ACCEPTANCE = ROOT / "acceptance" / "glaze-motion-0.3-experimental.md"
REGISTRY = ROOT / "consumers" / "registry.json"


def fail(message: str) -> None:
    raise SystemExit(f"Glaze Motion validation failed: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> None:
    required = (TOKENS, DOC, NATIVE, CSS, RUNTIME, RUNTIME_TEST, INTERACTION_TEST, CONSUMER, CONSUMER_TEST, RENDERED, REFERENCE, ACCEPTANCE, REGISTRY)
    for path in required:
        require(path.is_file(), f"missing required artifact: {path.relative_to(ROOT)}")

    data = json.loads(TOKENS.read_text(encoding="utf-8"))
    meta = data.get("glazeMotion", {})
    require(meta.get("version") == "0.3.0", "unexpected Glaze Motion version")
    require(meta.get("status") == "experimental", "Glaze Motion must remain Experimental")
    require(meta.get("extendsGlazeUi") == "1.5.0", "Glaze Motion must extend current Glaze UI Stable")

    tiers = data.get("tiers", {})
    require(tiers.get("core", {}).get("status") == "experimental", "Motion Core must remain Experimental")
    require(tiers.get("studio", {}).get("status") == "planned", "Motion Studio must remain Planned")
    require(tiers.get("spatial", {}).get("status") == "planned", "Motion Spatial must remain Planned")

    require(data.get("durationsMs") == {"instant": 0, "micro": 90, "short": 160, "medium": 240, "long": 360, "ambient": 700}, "duration roles changed")
    for name, spring in data.get("springs", {}).items():
        require(spring.get("mass", 0) > 0 and spring.get("stiffness", 0) > 0 and spring.get("damping", 0) > 0, f"{name} spring physics invalid")
        require(0 <= spring.get("maxOvershoot", 1) <= 0.1, f"{name} overshoot unbounded")

    gestures = data.get("gestures", {})
    require(gestures.get("slopPx") == 4, "gesture slop changed")
    require(gestures.get("velocityWindowMs") == 120, "velocity window changed")
    require(gestures.get("swipeThresholdRatio") == 0.33, "swipe threshold changed")
    require(gestures.get("directManipulationSurvivesReducedMotion") is True, "direct manipulation must survive reduced motion")
    require(gestures.get("keyboardAndRemoteAlternativesRequired") is True, "keyboard/remote alternatives required")
    require(gestures.get("semanticResultIndependentOfInputModality") is True, "semantic result must not depend on input modality")

    accessible = data.get("accessibleInteraction", {})
    require(accessible.get("reorderRequiresStableKeys") is True, "reorder stable-key contract missing")
    require(accessible.get("directionalMoveOrientations") == ["vertical", "horizontal"], "directional mapping contract changed")
    require(accessible.get("swipeResultVocabulary") == ["none", "start", "end"], "swipe vocabulary changed")
    require(accessible.get("cancellationMustPreserveValidState") is True, "cancellation state invariant missing")

    performance = data.get("performance", {})
    require(performance.get("targetFps") == 60, "fps target changed")
    require(performance.get("frameBudgetMs", 99) <= 16.7, "frame budget weakened")
    require(performance.get("maxLongTaskMs", 99) <= 50, "long-task budget weakened")
    require(performance.get("persistentWillChangeForCoreUi") is False, "persistent will-change prohibited")
    instrumentation = performance.get("instrumentation", {})
    require(instrumentation.get("localOnly") is True and instrumentation.get("networkReporting") is False, "performance instrumentation must remain local-only")

    native = data.get("nativeMappings", {})
    require(native.get("requiredForCandidatePromotion") is True, "native mapping evidence must be required before Candidate")
    require(native.get("semanticParityRequired") is True, "native semantic parity required")
    require(native.get("document") == "NATIVE_MOTION_MAPPINGS.md", "native mapping document changed")

    consumer = data.get("consumerEvidence", {})
    require(consumer.get("referenceHarness") == "reference/glaze-motion-consumer.mjs", "reference consumer harness changed")
    require(consumer.get("productionConsumerCertification") is False, "reference harness cannot certify production consumers")
    require(consumer.get("downstreamExperimentalAdoptionBlockedUntilStableBaselineConformance") is True, "downstream Stable-baseline gate missing")

    reduced = data.get("reducedMotion", {})
    for key in ("required", "removeDecorativeTranslation", "removeDecorativeScale", "disableParallax", "disableDecorativeLoops", "preserveStaticStateCues", "mustNotDelayTaskCompletion", "preserveDirectManipulationTracking", "removePostGestureInertia"):
        require(reduced.get(key) is True, f"missing reduced-motion invariant: {key}")
    require(reduced.get("durationMs") == 0, "reduced durations must collapse")

    require(data.get("authority", {}) == {"presentation": "Glaze UI / Glaze Motion", "privacyTruth": "Privacy Shield", "securityTruth": "Wardveil Security", "resilienceTruth": "Everkeep", "coordinationTruth": "GoreeCloud Mesh"}, "authority mapping changed")

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    require(registry.get("stableBaseline") == "1.5.0", "consumer Stable baseline changed unexpectedly")
    for entry in registry.get("consumers", []):
        if entry.get("status") == "migration-required":
            require(entry.get("productionEligible") is False, f"migration-required consumer marked production-eligible: {entry.get('name')}")

    doc = DOC.read_text(encoding="utf-8")
    for phrase in ("Experimental foundation (0.3.0)", "accessible gestures", "Performance instrumentation", "Native mappings", "Reference consumer evidence", "Motion Studio — Planned", "Motion Spatial — Planned"):
        require(phrase in doc, f"GLAZE_MOTION.md missing: {phrase}")

    native_doc = NATIVE.read_text(encoding="utf-8")
    for phrase in ("Mobile and tablet native", "Desktop native", "TV native", "Performance evidence", "Authority boundary"):
        require(phrase in native_doc, f"native mapping guidance missing: {phrase}")

    css = CSS.read_text(encoding="utf-8")
    require("Glaze Motion 0.3 Experimental" in css, "CSS version marker missing")
    require("will-change:" not in css, "persistent will-change prohibited")
    require("@media (prefers-reduced-motion: reduce)" in css, "CSS reduced-motion gate missing")

    source = RUNTIME.read_text(encoding="utf-8")
    for phrase in ('GLAZE_MOTION_VERSION = "0.3.0"', "createReorderModel", "resolveSwipeAction", "resolveDirectionalMove", "createPanZoomState", "createFrameBudgetProbe", "createDragSession", "startSharedTransition"):
        require(phrase in source, f"runtime missing: {phrase}")

    consumer_source = CONSUMER.read_text(encoding="utf-8")
    require("not production certification" in consumer_source.lower(), "reference consumer certification boundary missing")
    require("createReferenceQueue" in consumer_source, "reference consumer API missing")

    rendered = RENDERED.read_text(encoding="utf-8")
    require("--force-prefers-reduced-motion" in rendered, "rendered reduced-motion case missing")
    require(("390, 844" in rendered or "390,844" in rendered) and ("1280, 900" in rendered or "1280,900" in rendered), "rendered mobile/desktop cases missing")

    print("Glaze Motion 0.3 Experimental source validation passed")


if __name__ == "__main__":
    main()
