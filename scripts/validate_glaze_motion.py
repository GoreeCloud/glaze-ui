#!/usr/bin/env python3
"""Fail-closed validation for Glaze Motion 0.4 Experimental Motion Core."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / "tokens" / "glaze-motion.json"
DOC = ROOT / "GLAZE_MOTION.md"
NATIVE = ROOT / "NATIVE_MOTION_MAPPINGS.md"
CSS = ROOT / "css" / "glaze.motion.core.css"
RUNTIME = ROOT / "js" / "glaze.motion.js"
ACCESSIBILITY = ROOT / "js" / "glaze.motion.accessibility.js"
CORE_ENTRY = ROOT / "js" / "glaze.motion.core.js"
RUNTIME_TEST = ROOT / "tests" / "glaze-motion-runtime.test.mjs"
INTERACTION_TEST = ROOT / "tests" / "glaze-motion-interaction.test.mjs"
ACCESSIBILITY_TEST = ROOT / "tests" / "glaze-motion-accessibility.test.mjs"
CONSUMER = ROOT / "reference" / "glaze-motion-consumer.mjs"
CONSUMER_TEST = ROOT / "tests" / "glaze-motion-consumer.test.mjs"
RENDERED = ROOT / "scripts" / "validate_glaze_motion_rendered.py"
REFERENCE = ROOT / "reference" / "glaze-motion.html"
ACCEPTANCE = ROOT / "acceptance" / "glaze-motion-0.4-experimental.md"
REGISTRY = ROOT / "consumers" / "registry.json"


def fail(message: str) -> None:
    raise SystemExit(f"Glaze Motion validation failed: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> None:
    required = (TOKENS, DOC, NATIVE, CSS, RUNTIME, ACCESSIBILITY, CORE_ENTRY, RUNTIME_TEST, INTERACTION_TEST, ACCESSIBILITY_TEST, CONSUMER, CONSUMER_TEST, RENDERED, REFERENCE, ACCEPTANCE, REGISTRY)
    for path in required:
        require(path.is_file(), f"missing required artifact: {path.relative_to(ROOT)}")

    data = json.loads(TOKENS.read_text(encoding="utf-8"))
    meta = data.get("glazeMotion", {})
    require(meta.get("version") == "0.4.0", "unexpected Glaze Motion version")
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
    require(accessible.get("reorderCommands") == ["directional", "home", "end"], "reorder command contract changed")
    require(accessible.get("reorderResultMetadata") == ["moved", "itemKey", "fromIndex", "toIndex", "position", "total", "items"], "reorder result metadata changed")
    require(accessible.get("hardCodedAnnouncementCopyProhibited") is True, "design-system announcement copy must remain localization-neutral")
    require(accessible.get("localizationOwnedByConsumer") is True, "consumer must own localized announcement copy")
    require(accessible.get("swipeResultVocabulary") == ["none", "start", "end"], "swipe vocabulary changed")
    require(accessible.get("cancellationMustPreserveValidState") is True, "cancellation state invariant missing")

    runtime = data.get("runtime", {})
    require(runtime.get("entrypoint") == "js/glaze.motion.core.js", "0.4 aggregate runtime entry point changed")
    require(runtime.get("compatibilityBase") == "js/glaze.motion.js", "compatibility runtime base changed")
    require(runtime.get("stateIndependentOfAnimationCompletion") is True, "state must remain independent of animation completion")

    performance = data.get("performance", {})
    require(performance.get("targetFps") == 60, "fps target changed")
    require(performance.get("frameBudgetMs", 99) <= 16.7, "frame budget weakened")
    require(performance.get("maxLongTaskMs", 99) <= 50, "long-task budget weakened")
    require(performance.get("maxConcurrentSettlingAnimations") == 12, "settling concurrency budget changed")
    require(performance.get("persistentWillChangeForCoreUi") is False, "persistent will-change prohibited")
    instrumentation = performance.get("instrumentation", {})
    require(instrumentation.get("localOnly") is True and instrumentation.get("networkReporting") is False, "performance instrumentation must remain local-only")
    settling = performance.get("settlingBudget", {})
    for key in ("localOnly", "rejectUnderReducedMotion", "rejectWhenExhausted", "stateUpdatesMustContinue"):
        require(settling.get(key) is True, f"missing settling-budget invariant: {key}")

    native = data.get("nativeMappings", {})
    require(native.get("requiredForCandidatePromotion") is True, "native mapping evidence must be required before Candidate")
    require(native.get("semanticParityRequired") is True, "native semantic parity required")
    require(native.get("document") == "NATIVE_MOTION_MAPPINGS.md", "native mapping document changed")

    consumer = data.get("consumerEvidence", {})
    require(consumer.get("referenceHarness") == "reference/glaze-motion-consumer.mjs", "reference consumer harness changed")
    require(consumer.get("renderedReference") == "reference/glaze-motion.html", "rendered reference changed")
    require(consumer.get("productionConsumerCertification") is False, "reference harness cannot certify production consumers")
    require(consumer.get("downstreamExperimentalAdoptionBlockedUntilStableBaselineConformance") is True, "downstream Stable-baseline gate missing")

    rendered_contract = data.get("renderedAcceptance", {})
    require(rendered_contract.get("profiles") == ["mobile", "desktop", "tv"], "rendered profile matrix changed")
    require(rendered_contract.get("modes") == ["normal", "reduced-motion"], "rendered mode matrix changed")
    require(rendered_contract.get("nativeDeviceCertification") is False, "web rendered evidence cannot claim native certification")
    for key in ("assertDirectManipulationInReducedMotion", "assertAdapterDurationsCollapse", "assertAccessibleReorderMetadata", "assertSettlingBudget", "assertLocalPerformanceProbe"):
        require(rendered_contract.get(key) is True, f"missing rendered assertion: {key}")

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
    for phrase in ("Experimental foundation (0.4.0)", "accessible gestures", "settling budget", "Native mappings", "Reference consumer evidence", "Rendered acceptance", "Motion Studio — Planned", "Motion Spatial — Planned"):
        require(phrase in doc, f"GLAZE_MOTION.md missing: {phrase}")

    native_doc = NATIVE.read_text(encoding="utf-8")
    for phrase in ("Mobile and tablet native", "Desktop native", "TV native", "Performance evidence", "Authority boundary"):
        require(phrase in native_doc, f"native mapping guidance missing: {phrase}")

    css = CSS.read_text(encoding="utf-8")
    require("Glaze Motion 0.3 Experimental" in css, "retained 0.3 CSS compatibility marker missing")
    require("will-change:" not in css, "persistent will-change prohibited")
    require("@media (prefers-reduced-motion: reduce)" in css, "CSS reduced-motion gate missing")

    source = RUNTIME.read_text(encoding="utf-8")
    for phrase in ('GLAZE_MOTION_VERSION = "0.3.0"', "createReorderModel", "resolveSwipeAction", "resolveDirectionalMove", "createPanZoomState", "createFrameBudgetProbe", "createDragSession", "startSharedTransition"):
        require(phrase in source, f"compatibility runtime missing: {phrase}")

    accessibility_source = ACCESSIBILITY.read_text(encoding="utf-8")
    for phrase in ('GLAZE_MOTION_ACCESSIBILITY_VERSION = "0.4.0"', "resolveReorderCommand", "createAccessibleReorderController", "createSettlingBudget", 'reason: "reduced-motion"', 'reason: "budget-exhausted"'):
        require(phrase in accessibility_source, f"0.4 accessibility runtime missing: {phrase}")
    require("announcement:" not in accessibility_source, "runtime must not hard-code localized reorder announcement copy")

    core_source = CORE_ENTRY.read_text(encoding="utf-8")
    for phrase in ('export * from "./glaze.motion.js"', 'export * from "./glaze.motion.accessibility.js"', 'GLAZE_MOTION_CORE_VERSION = "0.4.0"'):
        require(phrase in core_source, f"aggregate runtime missing: {phrase}")

    consumer_source = CONSUMER.read_text(encoding="utf-8")
    require("not production certification" in consumer_source.lower(), "reference consumer certification boundary missing")
    require("createReferenceQueue" in consumer_source, "reference consumer API missing")

    reference_source = REFERENCE.read_text(encoding="utf-8")
    for phrase in ("Glaze Motion 0.4 Experimental Acceptance", "createAccessibleReorderController", "createSettlingBudget", "createFrameBudgetProbe"):
        require(phrase in reference_source, f"rendered reference missing: {phrase}")

    rendered = RENDERED.read_text(encoding="utf-8")
    require("Glaze Motion 0.4 Experimental" in rendered, "rendered validator version marker missing")
    require("--force-prefers-reduced-motion" in rendered, "rendered reduced-motion case missing")
    for viewport in ((390, 844), (1280, 900), (1920, 1080)):
        compact = f"{viewport[0]},{viewport[1]}"
        spaced = f"{viewport[0]}, {viewport[1]}"
        require(compact in rendered or spaced in rendered, f"rendered viewport missing: {viewport[0]}x{viewport[1]}")
    compact_rendered = rendered.replace(" ", "")
    require("run_case(browser,port,1280,900,True)" in compact_rendered, "desktop reduced-motion rendered case missing")
    require("run_case(browser,port,1920,1080,True)" in compact_rendered, "TV reduced-motion rendered case missing")

    print("Glaze Motion 0.4 Experimental source validation passed")


if __name__ == "__main__":
    main()
