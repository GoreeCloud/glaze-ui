#!/usr/bin/env python3
"""Fail-closed validation for Glaze Motion 0.6 Experimental Motion Core."""
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
ACCEPTANCE = ROOT / "acceptance" / "glaze-motion-0.6-experimental.md"
REGISTRY = ROOT / "consumers" / "registry.json"

LAUNCHER_REPO = "GoreeCloud/goreecloud-launcher"
LAUNCHER_HEAD = "3095b9320b660f5e166465990d5d2bee061d7422"
LAUNCHER_MERGE = "23a389b3b24db726ceab5e328f9f8157fa7655ae"
KEYBOARD_REPO = "GoreeCloud/goreecloud-keyboard"
KEYBOARD_HEAD = "80de7bd2dcff6d07b06b19f8250e37d20155d7ff"
KEYBOARD_MERGE = "c9c0500263b40640339cf7a46f1a029d9a2ac240"


def fail(message: str) -> None:
    raise SystemExit(f"Glaze Motion validation failed: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def require_phrases(text: str, phrases: tuple[str, ...], label: str) -> None:
    for phrase in phrases:
        require(phrase in text, f"{label} missing: {phrase}")


def evaluation_by_repo(evaluations: list[dict], repo: str) -> dict:
    found = [entry for entry in evaluations if entry.get("repository") == repo]
    require(len(found) == 1, f"expected exactly one first-party evaluation for {repo}")
    return found[0]


def registry_by_repo(registry: dict, repo: str) -> dict:
    found = [entry for entry in registry.get("consumers", []) if entry.get("repository") == repo]
    require(len(found) == 1, f"expected exactly one registry entry for {repo}")
    return found[0]


def validate_common_evaluation(entry: dict, *, name: str, repo: str, motion: str, pr: int, head: str, merge: str, ci: int) -> None:
    require(entry.get("consumer") == name, f"{name} consumer name changed")
    require(entry.get("repository") == repo, f"{name} repository changed")
    require(entry.get("consumerState") == "adoption-candidate", f"{name} historical evaluation state changed")
    require(entry.get("targetGlazeUi") == "1.5.0", f"{name} historical evaluated Glaze UI target changed")
    require(entry.get("evaluatedMotionVersion") == motion, f"{name} evaluated Motion version changed")
    require(entry.get("pullRequest") == pr, f"{name} PR evidence changed")
    require(entry.get("validatedHead") == head, f"{name} exact validated head changed")
    require(entry.get("mergeRevision") == merge, f"{name} merge evidence changed")
    require(entry.get("ciRun") == ci, f"{name} CI evidence changed")
    require(entry.get("evaluationMode") == "native-android-test-only", f"{name} evaluation must remain native Android test-only")
    require(entry.get("productionDependency") is False, f"Experimental Motion cannot become a {name} production dependency")
    require(entry.get("nativeDeviceCertification") is False, f"{name} cannot claim native-device certification")
    require(entry.get("candidatePromotionSufficient") is False, f"{name} evaluation cannot independently satisfy Candidate promotion")


def main() -> None:
    required = (
        TOKENS, DOC, NATIVE, CSS, RUNTIME, ACCESSIBILITY, CORE_ENTRY,
        RUNTIME_TEST, INTERACTION_TEST, ACCESSIBILITY_TEST, CONSUMER,
        CONSUMER_TEST, RENDERED, REFERENCE, ACCEPTANCE, REGISTRY,
    )
    for path in required:
        require(path.is_file(), f"missing required artifact: {path.relative_to(ROOT)}")

    data = json.loads(TOKENS.read_text(encoding="utf-8"))
    meta = data.get("glazeMotion", {})
    require(meta.get("version") == "0.6.0", "unexpected Glaze Motion version")
    require(meta.get("status") == "experimental", "Glaze Motion must remain Experimental")
    require(meta.get("extendsGlazeUi") == "1.5.0", "Glaze Motion 0.6 historical evaluation baseline changed")
    require(meta.get("runtimeCompatibilityBaseline") == "0.4.0", "0.6 must retain the 0.4 runtime compatibility baseline")

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
    require(gestures.get("settlingMotionCollapsesUnderReducedMotion") is True, "settling must collapse under reduced motion")
    require(gestures.get("keyboardAndRemoteAlternativesRequired") is True, "keyboard/remote alternatives required")
    require(gestures.get("semanticResultIndependentOfInputModality") is True, "semantic result must not depend on input modality")

    accessible = data.get("accessibleInteraction", {})
    require(accessible.get("reorderRequiresStableKeys") is True, "reorder stable-key contract missing")
    require(accessible.get("directionalMoveOrientations") == ["vertical", "horizontal"], "directional mapping changed")
    require(accessible.get("reorderCommands") == ["directional", "home", "end"], "reorder command contract changed")
    require(accessible.get("reorderResultMetadata") == ["moved", "itemKey", "fromIndex", "toIndex", "position", "total", "items"], "reorder metadata changed")
    require(accessible.get("hardCodedAnnouncementCopyProhibited") is True, "announcement copy must remain localization-neutral")
    require(accessible.get("localizationOwnedByConsumer") is True, "consumer must own localized feedback")
    require(accessible.get("cancellationMustPreserveValidState") is True, "cancellation invariant missing")

    runtime = data.get("runtime", {})
    require(runtime.get("entrypoint") == "js/glaze.motion.core.js", "aggregate runtime entry point changed")
    require(runtime.get("compatibilityBase") == "js/glaze.motion.js", "compatibility runtime base changed")
    require(runtime.get("implementationVersion") == "0.4.0", "0.6 must not imply a new runtime implementation")
    require(runtime.get("stateIndependentOfAnimationCompletion") is True, "state must remain independent of animation completion")
    require(runtime.get("gestureStateMustNotDependOnAnimation") is True, "gesture state must not depend on animation")

    performance = data.get("performance", {})
    require(performance.get("targetFps") == 60, "fps target changed")
    require(performance.get("frameBudgetMs", 99) <= 16.7, "frame budget weakened")
    require(performance.get("maxLongTaskMs", 99) <= 50, "long-task budget weakened")
    require(performance.get("maxConcurrentSettlingAnimations") == 12, "settling concurrency changed")
    require(performance.get("persistentWillChangeForCoreUi") is False, "persistent will-change prohibited")
    instrumentation = performance.get("instrumentation", {})
    require(instrumentation.get("localOnly") is True and instrumentation.get("networkReporting") is False, "performance evidence must remain local-only")
    settling = performance.get("settlingBudget", {})
    for key in ("localOnly", "rejectUnderReducedMotion", "rejectWhenExhausted", "stateUpdatesMustContinue"):
        require(settling.get(key) is True, f"missing settling-budget invariant: {key}")

    native_contract = data.get("nativeMappings", {})
    require(native_contract.get("requiredForCandidatePromotion") is True, "native mapping evidence must remain required")
    require(native_contract.get("semanticParityRequired") is True, "native semantic parity required")
    require(native_contract.get("document") == "NATIVE_MOTION_MAPPINGS.md", "native mapping document changed")

    consumer = data.get("consumerEvidence", {})
    require(consumer.get("referenceHarness") == "reference/glaze-motion-consumer.mjs", "reference consumer harness changed")
    require(consumer.get("renderedReference") == "reference/glaze-motion.html", "rendered reference changed")
    require(consumer.get("productionConsumerCertification") is False, "reference harness cannot certify production consumers")
    require(consumer.get("downstreamExperimentalAdoptionBlockedUntilStableBaselineConformance") is True, "Stable-baseline gate missing")
    require(consumer.get("downstreamProductionAdoptionBlockedUntilConsumerAcceptance") is True, "production-acceptance gate missing")
    require("firstPartyEvaluation" not in consumer, "deprecated singular first-party evidence object must not remain")
    evaluations = consumer.get("firstPartyEvaluations")
    require(isinstance(evaluations, list) and len(evaluations) == 2, "0.6 requires exactly two governed first-party evaluations")

    launcher_eval = evaluation_by_repo(evaluations, LAUNCHER_REPO)
    validate_common_evaluation(
        launcher_eval, name="GoreeCloud Launcher", repo=LAUNCHER_REPO,
        motion="0.4.0", pr=22, head=LAUNCHER_HEAD, merge=LAUNCHER_MERGE, ci=67,
    )
    keyboard_eval = evaluation_by_repo(evaluations, KEYBOARD_REPO)
    validate_common_evaluation(
        keyboard_eval, name="GoreeCloud Keyboard", repo=KEYBOARD_REPO,
        motion="0.5.0", pr=4, head=KEYBOARD_HEAD, merge=KEYBOARD_MERGE, ci=15,
    )
    require(keyboard_eval.get("runtimeProfile") == "android-15-api-35-x86_64", "Keyboard runtime profile changed")
    require(keyboard_eval.get("reducedMotionSettingValidated") is True, "Keyboard reduced-motion setting evidence missing")

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

    require(data.get("authority", {}) == {
        "presentation": "Glaze UI / Glaze Motion",
        "privacyTruth": "Privacy Shield",
        "securityTruth": "Wardveil Security",
        "resilienceTruth": "Everkeep",
        "coordinationTruth": "GoreeCloud Mesh",
    }, "authority mapping changed")

    current_stable = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    require(registry.get("stableBaseline") == current_stable, "consumer Stable baseline changed")
    for repo, merge in ((LAUNCHER_REPO, LAUNCHER_MERGE), (KEYBOARD_REPO, KEYBOARD_MERGE)):
        entry = registry_by_repo(registry, repo)
        require(entry.get("status") == "migration-required", f"{repo} must become Migration Required after Stable advances")
        require(entry.get("targetVersion") == "1.5.0", f"{repo} historical evaluated target changed")
        require(entry.get("requiredTargetVersion") == current_stable, f"{repo} required target must match current Stable")
        require(entry.get("referenceRevision") == merge, f"{repo} registry merge evidence changed")
        require(entry.get("evidence") == "docs/glaze-ui-adoption.md", f"{repo} evidence path changed")
        require(entry.get("automatedContract") is True, f"{repo} automated contract missing")
        require(entry.get("productionEligible") is False, f"{repo} must remain production-ineligible")
        require("pending" in entry.get("visualAcceptance", "").lower(), f"{repo} incomplete acceptance boundary missing")
    for entry in registry.get("consumers", []):
        if entry.get("status") == "migration-required":
            require(entry.get("productionEligible") is False, f"migration-required consumer marked production-eligible: {entry.get('name')}")

    doc = DOC.read_text(encoding="utf-8")
    require_phrases(doc, (
        "Experimental foundation (0.6.0)", "Runtime implementation baseline",
        "Direct manipulation and accessible gestures", "settling budget", "Native mappings",
        "First-party downstream evidence", "GoreeCloud Launcher", "GoreeCloud Keyboard",
        "Rendered acceptance", "Motion Studio — Planned", "Motion Spatial — Planned",
        "two test-only native Android evaluations are still insufficient",
    ), "GLAZE_MOTION.md")
    require(LAUNCHER_HEAD in doc and LAUNCHER_MERGE in doc, "documentation missing exact Launcher evidence")
    require(KEYBOARD_HEAD in doc and KEYBOARD_MERGE in doc, "documentation missing exact Keyboard evidence")

    native_doc = NATIVE.read_text(encoding="utf-8")
    require_phrases(native_doc, (
        "Mobile and tablet native", "Desktop native", "TV native",
        "First-party native evaluation evidence", "GoreeCloud Launcher", "GoreeCloud Keyboard",
        "Performance evidence", "Authority boundary", "Settings.Global.ANIMATOR_DURATION_SCALE",
    ), "native mapping guidance")
    require(LAUNCHER_MERGE in native_doc and KEYBOARD_MERGE in native_doc, "native mapping guidance missing consumer merge evidence")

    acceptance = ACCEPTANCE.read_text(encoding="utf-8")
    require_phrases(acceptance, (
        "Experimental evidence/governance iteration", "First-party downstream evidence",
        "GoreeCloud Launcher", "GoreeCloud Keyboard", "What 0.6 does not prove",
        "Runtime compatibility boundary", "Promotion boundary",
        "This evidence remains insufficient for Candidate promotion.",
    ), "0.6 acceptance record")
    require(LAUNCHER_HEAD in acceptance and LAUNCHER_MERGE in acceptance and "Android CI: **#67**" in acceptance, "acceptance missing exact Launcher evidence")
    require(KEYBOARD_HEAD in acceptance and KEYBOARD_MERGE in acceptance and "Android CI: **#15**" in acceptance, "acceptance missing exact Keyboard evidence")

    css = CSS.read_text(encoding="utf-8")
    require("Glaze Motion 0.3 Experimental" in css, "retained 0.3 CSS compatibility marker missing")
    require("will-change:" not in css, "persistent will-change prohibited")
    require("@media (prefers-reduced-motion: reduce)" in css, "CSS reduced-motion gate missing")

    runtime_source = RUNTIME.read_text(encoding="utf-8")
    require_phrases(runtime_source, (
        'GLAZE_MOTION_VERSION = "0.3.0"', "createReorderModel", "resolveSwipeAction",
        "resolveDirectionalMove", "createPanZoomState", "createFrameBudgetProbe",
        "createDragSession", "startSharedTransition",
    ), "compatibility runtime")

    accessibility_source = ACCESSIBILITY.read_text(encoding="utf-8")
    require_phrases(accessibility_source, (
        'GLAZE_MOTION_ACCESSIBILITY_VERSION = "0.4.0"', "resolveReorderCommand",
        "createAccessibleReorderController", "createSettlingBudget",
        'reason: "reduced-motion"', 'reason: "budget-exhausted"',
    ), "0.4 accessibility runtime")
    require("announcement:" not in accessibility_source, "runtime must not hard-code localized reorder announcement copy")

    core_source = CORE_ENTRY.read_text(encoding="utf-8")
    require_phrases(core_source, (
        'export * from "./glaze.motion.js"',
        'export * from "./glaze.motion.accessibility.js"',
        'GLAZE_MOTION_CORE_VERSION = "0.4.0"',
    ), "0.4 aggregate runtime")

    consumer_source = CONSUMER.read_text(encoding="utf-8")
    require("not production certification" in consumer_source.lower(), "reference consumer certification boundary missing")
    require("createReferenceQueue" in consumer_source, "reference consumer API missing")

    reference_source = REFERENCE.read_text(encoding="utf-8")
    require_phrases(reference_source, (
        "Glaze Motion 0.4 Experimental Acceptance", "createAccessibleReorderController",
        "createSettlingBudget",
    ), "rendered reference")

    print("Glaze Motion 0.6 Experimental validated: retained 0.4 runtime, Launcher + Keyboard historical native test-only evidence, Candidate gate remains closed")


if __name__ == "__main__":
    main()
