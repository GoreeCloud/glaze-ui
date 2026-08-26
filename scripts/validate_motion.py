#!/usr/bin/env python3
"""Validate the Glaze UI 1.5 Candidate motion and interaction contract."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / "tokens" / "motion.json"
DOC = ROOT / "MOTION.md"
CSS = ROOT / "css" / "glaze.motion.css"


def fail(message: str) -> None:
    raise SystemExit(f"motion validation failed: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> None:
    for path in (TOKENS, DOC, CSS):
        require(path.is_file(), f"missing required artifact: {path.relative_to(ROOT)}")

    data = json.loads(TOKENS.read_text(encoding="utf-8"))
    meta = data.get("glazeUi", {})
    require(meta.get("version") == "1.5.0-candidate", "unexpected candidate version")
    require(meta.get("status") == "candidate", "motion contract must remain Candidate")
    require(meta.get("domain") == "motion-and-interaction", "unexpected motion domain")

    durations = data.get("durationsMs", {})
    expected = {
        "instant": 0,
        "micro": 90,
        "short": 160,
        "medium": 240,
        "long": 360,
        "ambient": 700,
    }
    require(durations == expected, "duration roles do not match the canonical contract")
    require(list(durations.values()) == sorted(durations.values()), "duration roles must be monotonic")

    easing = data.get("easing", {})
    for role in ("standard", "enter", "exit", "emphasized", "linear"):
        require(role in easing, f"missing easing role: {role}")

    rules = data.get("rules", {})
    require(rules.get("interruptibleUserTransitions") is True, "user transitions must be interruptible")
    require(rules.get("hoverRequiredForCriticalInformation") is False, "critical information cannot depend on hover")
    require(rules.get("decorativeInfiniteLoopsForCoreUi") is False, "core UI cannot use decorative infinite loops")
    require(rules.get("falseDeterminateProgress") is False, "false determinate progress must be prohibited")
    require(rules.get("prematureAuthoritativeStateAnimation") is False, "premature authoritative-state animation must be prohibited")
    require(set(rules.get("preferCompositorProperties", [])) == {"opacity", "transform"}, "compositor preference must be opacity and transform")
    require(rules.get("gestureTransitionsProgressLinked") is True, "gesture transitions must be progress-linked")

    reduced = data.get("reducedMotion", {})
    require(reduced.get("required") is True, "reduced motion must be mandatory")
    require(reduced.get("durationMs") == 0, "reduced-motion duration must collapse to zero")
    for key in (
        "removeDecorativeTranslation",
        "removeDecorativeScale",
        "disableParallax",
        "disableDecorativeLoops",
        "preserveStaticStateCues",
        "mustNotDelayTaskCompletion",
    ):
        require(reduced.get(key) is True, f"reduced-motion invariant missing: {key}")

    authority = data.get("authority", {})
    expected_authority = {
        "presentation": "Glaze UI",
        "privacyTruth": "Privacy Shield",
        "securityTruth": "Wardveil Security",
        "resilienceTruth": "Everkeep",
        "coordinationTruth": "GoreeCloud Mesh",
    }
    require(authority == expected_authority, "platform authority mapping changed")

    doc = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Glaze UI 1.5 Candidate",
        "Reduced-motion contract",
        "Privacy Shield",
        "Wardveil Security",
        "Everkeep",
        "GoreeCloud Mesh",
        "interruptible",
    ):
        require(phrase in doc, f"MOTION.md missing required contract text: {phrase}")

    css = CSS.read_text(encoding="utf-8")
    for token in (
        "--glaze-motion-instant: 0ms",
        "--glaze-motion-micro: 90ms",
        "--glaze-motion-short: 160ms",
        "--glaze-motion-medium: 240ms",
        "--glaze-motion-long: 360ms",
        "--glaze-motion-ambient: 700ms",
        "@media (prefers-reduced-motion: reduce)",
        "animation: none !important",
    ):
        require(token in css, f"CSS missing required motion primitive: {token}")

    print("Glaze UI motion Candidate validation passed")


if __name__ == "__main__":
    main()
