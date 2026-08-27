#!/usr/bin/env python3
"""Fail-closed validation for the Glaze Motion Experimental foundation."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / "tokens" / "glaze-motion.json"
DOC = ROOT / "GLAZE_MOTION.md"
CSS = ROOT / "css" / "glaze.motion.core.css"
RUNTIME = ROOT / "js" / "glaze.motion.js"
TEST = ROOT / "tests" / "glaze-motion-runtime.test.mjs"


def fail(message: str) -> None:
    raise SystemExit(f"Glaze Motion validation failed: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> None:
    for path in (TOKENS, DOC, CSS, RUNTIME, TEST):
        require(path.is_file(), f"missing required artifact: {path.relative_to(ROOT)}")

    data = json.loads(TOKENS.read_text(encoding="utf-8"))
    meta = data.get("glazeMotion", {})
    require(meta.get("version") == "0.1.0", "unexpected Glaze Motion foundation version")
    require(meta.get("status") == "experimental", "foundation must remain Experimental")
    require(meta.get("extendsGlazeUi") == "1.5.0", "foundation must extend current Glaze UI Stable")
    require(meta.get("domain") == "motion-animation-spatial-graphics", "unexpected Glaze Motion domain")

    tiers = data.get("tiers", {})
    require(tiers.get("core", {}).get("status") == "experimental", "Motion Core must be Experimental")
    require(tiers.get("core", {}).get("defaultForApplications") is True, "Motion Core must be the default application tier")
    require(tiers.get("studio", {}).get("status") == "planned", "Motion Studio must remain Planned")
    require(tiers.get("spatial", {}).get("status") == "planned", "Motion Spatial must remain Planned")
    require(tiers.get("spatial", {}).get("requiresAdvancedGraphicsRuntime") is True, "Motion Spatial must declare its advanced graphics boundary")

    durations = data.get("durationsMs", {})
    expected_durations = {
        "instant": 0,
        "micro": 90,
        "short": 160,
        "medium": 240,
        "long": 360,
        "ambient": 700,
    }
    require(durations == expected_durations, "Motion Core duration roles must inherit the Stable timing vocabulary")

    springs = data.get("springs", {})
    require(set(springs) == {"restrained", "standard", "expressive", "spatial"}, "spring preset set changed")
    for name, spring in springs.items():
        require(spring.get("mass", 0) > 0, f"{name} spring mass must be positive")
        require(spring.get("stiffness", 0) > 0, f"{name} spring stiffness must be positive")
        require(spring.get("damping", 0) > 0, f"{name} spring damping must be positive")
        require(0 <= spring.get("maxOvershoot", 1) <= 0.1, f"{name} spring overshoot must stay bounded")

    reduced = data.get("reducedMotion", {})
    require(reduced.get("required") is True, "reduced motion must be mandatory")
    require(reduced.get("durationMs") == 0, "reduced-motion durations must collapse to zero")
    for key in (
        "removeDecorativeTranslation",
        "removeDecorativeScale",
        "disableParallax",
        "disableDecorativeLoops",
        "preserveStaticStateCues",
        "mustNotDelayTaskCompletion",
    ):
        require(reduced.get(key) is True, f"missing reduced-motion invariant: {key}")

    runtime = data.get("runtime", {})
    require(runtime.get("interruptibleByDefault") is True, "Motion Core must be interruptible by default")
    require(runtime.get("stateIndependentOfAnimationCompletion") is True, "state must not depend on animation completion")
    require(runtime.get("allowAutonomousCoreUiLoops") is False, "autonomous Core UI loops must remain prohibited")
    require(set(runtime.get("preferCompositorProperties", [])) == {"opacity", "transform"}, "unexpected compositor preference")

    fallbacks = data.get("fallbacks", {})
    require(fallbacks.get("webgpu") == ["webgl2", "canvas-svg-css", "static-accessible"], "WebGPU fallback ladder changed")
    require(fallbacks.get("webgl2") == ["canvas-svg-css", "static-accessible"], "WebGL2 fallback ladder changed")

    authority = data.get("authority", {})
    expected_authority = {
        "presentation": "Glaze UI / Glaze Motion",
        "privacyTruth": "Privacy Shield",
        "securityTruth": "Wardveil Security",
        "resilienceTruth": "Everkeep",
        "coordinationTruth": "GoreeCloud Mesh",
    }
    require(authority == expected_authority, "platform authority mapping changed")

    doc = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Motion Core",
        "Motion Studio",
        "Motion Spatial",
        "Experimental",
        "prefers-reduced-motion",
        "WebGPU -> WebGL2 -> Canvas/SVG/CSS -> static accessible representation",
    ):
        require(phrase in doc, f"GLAZE_MOTION.md missing required contract text: {phrase}")

    css = CSS.read_text(encoding="utf-8")
    for phrase in (
        "Glaze Motion 0.1 Experimental",
        "--glaze-motion-core-medium: 240ms",
        ".glaze-motion-core-enter",
        ".glaze-motion-core-shared",
        "@media (prefers-reduced-motion: reduce)",
        "animation: none !important",
    ):
        require(phrase in css, f"Motion Core CSS missing required primitive: {phrase}")

    runtime_source = RUNTIME.read_text(encoding="utf-8")
    for phrase in (
        'GLAZE_MOTION_VERSION = "0.1.0"',
        "prefersReducedMotion",
        "resolveDuration",
        "createSpringKeyframes",
        "animate",
        "detectCapabilities",
        "selectSpatialBackend",
    ):
        require(phrase in runtime_source, f"runtime missing required primitive: {phrase}")

    print("Glaze Motion 0.1 Experimental foundation validation passed")


if __name__ == "__main__":
    main()
