#!/usr/bin/env python3
"""Validate the retained Glaze UI 1.6 adaptive workspace contract under current 2.2 Stable."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / "tokens" / "workspace-navigation.candidate.json"
CSS = ROOT / "css" / "glaze.workspace.candidate.css"
DOC = ROOT / "WORKSPACE_NAVIGATION.md"
REFERENCE = ROOT / "reference" / "candidate-1.6-workspace.html"
ACCEPTANCE = ROOT / "reference" / "candidate-1.6-workspace-acceptance.html"
RENDERED_VALIDATOR = ROOT / "scripts" / "validate_candidate_1_6_rendered.py"
ACCEPTANCE_RECORD = ROOT / "acceptance" / "1.6.0.md"
VERSION = ROOT / "VERSION"


def fail(message: str) -> None:
    raise SystemExit(f"workspace/navigation validation failed: {message}")


def require_text(text: str, markers: tuple[str, ...], source: str) -> None:
    for marker in markers:
        if marker not in text:
            fail(f"{source} missing required marker: {marker}")


def main() -> None:
    for path in (TOKENS, CSS, DOC, REFERENCE, ACCEPTANCE, RENDERED_VALIDATOR, ACCEPTANCE_RECORD, VERSION):
        if not path.is_file():
            fail(f"missing required file {path.relative_to(ROOT)}")

    if VERSION.read_text(encoding="utf-8").strip() != "2.2.0":
        fail("current repository Stable target must be 2.2.0")

    try:
        data = json.loads(TOKENS.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid token JSON: {exc}")

    meta = data.get("meta", {})
    if meta.get("candidateVersion") != "1.6.0":
        fail("historical candidateVersion must remain 1.6.0 for compatibility")
    if meta.get("status") != "Stable":
        fail("workspace layer must remain Stable after 1.6.0 promotion")
    if meta.get("stableBaseline") != "1.6.0":
        fail("historical workspace Stable baseline must remain 1.6.0")

    expected_regions = {"window", "title", "navigation", "toolbar", "content", "inspector", "status", "overlay"}
    if set(data.get("regions", {})) != expected_regions:
        fail("workspace semantic region set changed unexpectedly")

    targets = data.get("targets", {})
    expected_targets = {
        "precisionPointerMinimum": 40,
        "mixedInputMinimum": 44,
        "coarsePointerMinimum": 48,
        "tvMinimum": 56,
    }
    for key, value in expected_targets.items():
        if targets.get(key) != value:
            fail(f"{key} must equal {value}")

    density = data.get("density", {})
    if set(density) != {"comfortable", "compact", "spacious"}:
        fail("density modes must be comfortable, compact, and spacious")

    transforms = data.get("navigationTransform", {})
    if set(transforms) != {"mobile", "tablet", "desktop", "tv"}:
        fail("navigation transformations must cover mobile, tablet, desktop, and tv")

    adaptation = data.get("adaptation", {})
    for invariant in (
        "preserveSemanticOrder",
        "preserveFocusOrder",
        "preserveCurrentDestination",
        "preserveActionState",
    ):
        if adaptation.get(invariant) is not True:
            fail(f"adaptation invariant {invariant} must be true")

    accessibility = data.get("accessibility", {})
    for invariant in (
        "focusVisible",
        "iconOnlyAccessibleName",
        "reducedMotion",
        "reducedTransparency",
        "forcedColors",
        "keyboardDesktopWeb",
        "noHoverOnlyPrimaryAction",
        "nonColorStateCue",
    ):
        if accessibility.get(invariant) is not True:
            fail(f"accessibility invariant {invariant} must be true")

    authority = data.get("authority", {})
    if authority.get("presentationOnly") is not True:
        fail("workspace Stable contract must remain presentation-only")
    for key, value in {
        "privacy": "Privacy Shield",
        "security": "Wardveil Security",
        "continuity": "Everkeep",
        "coordination": "GoreeCloud Mesh",
        "applicationState": "application logic",
    }.items():
        if authority.get(key) != value:
            fail(f"authority binding {key} must remain {value}")

    css = CSS.read_text(encoding="utf-8")
    require_text(
        css,
        (
            ".glaze-workspace-candidate",
            ".glaze-workspace-nav-candidate",
            ".glaze-workspace-toolbar-candidate",
            ".glaze-workspace-content-candidate",
            ".glaze-workspace-inspector-candidate",
            "@media (pointer: fine)",
            "@media (pointer: coarse)",
            'data-form-factor="tv"',
            'data-reduced-transparency="true"',
            'data-performance="constrained"',
            "@media (prefers-reduced-motion: reduce)",
            "@media (prefers-reduced-transparency: reduce)",
            "@media (forced-colors: active)",
        ),
        "retained workspace CSS",
    )

    doc = DOC.read_text(encoding="utf-8")
    require_text(
        doc,
        (
            "Status: **Stable in Glaze UI 1.6.0** and retained in the current **Glaze UI 2.2.0** compatibility and production-conformance baseline.",
            "## Navigation transformation",
            "## Input-aware targets",
            "## Accessibility and resilience",
            "## State and authority boundaries",
            "## Stable implementation",
            "## Stable rendered acceptance matrix",
            "## Stable release boundary",
            "Evidence Presentation and Authority Surfaces contract is also Stable",
            "downstream applications must adopt **Glaze UI 2.2.0**",
        ),
        "workspace documentation",
    )
    if "The separate Glaze UI 1.6 Evidence Presentation Candidate" in doc:
        fail("workspace documentation still declares Evidence Presentation Candidate after Stable promotion")

    reference = REFERENCE.read_text(encoding="utf-8")
    require_text(
        reference,
        (
            "Glaze UI 1.6 Candidate",
            "data-glaze-candidate=\"1.6\"",
            "glaze.workspace.candidate.css",
            "glaze-workspace-candidate",
            "class=\"glaze-workspace-nav-candidate\"",
            "class=\"glaze-workspace-toolbar-candidate\"",
            "class=\"glaze-workspace-content-candidate\"",
            "class=\"glaze-workspace-inspector-candidate\"",
            "aria-current=\"page\"",
            "formFactor",
            "reduced-transparency",
            "performance-constrained",
        ),
        "historical workspace reference",
    )

    acceptance = ACCEPTANCE.read_text(encoding="utf-8")
    require_text(
        acceptance,
        (
            "Glaze UI 1.6 Candidate workspace acceptance",
            "Mobile overlay navigation and inspector sheet rendered",
            "Tablet adaptive navigation and contextual inspector rendered",
            "Desktop persistent navigation and inspector rendered",
            "Wide Desktop expanded workspace rendered",
            "TV far-view workspace rendered independently of Wide Desktop",
            "reduced-transparency opaque fallback rendered",
            "forced-colors selection treatment rendered",
        ),
        "historical workspace rendered acceptance harness",
    )

    rendered_validator = RENDERED_VALIDATOR.read_text(encoding="utf-8")
    for marker in (
        '(390, 844, "mobile")',
        '(820, 1180, "tablet")',
        '(1280, 900, "desktop")',
        '(1600, 1000, "wide-desktop")',
        '(1920, 1080, "tv")',
        'mode="reduced-motion"',
        'mode="reduced-transparency"',
        'mode="performance-constrained"',
        'mode="forced-colors"',
    ):
        if marker not in rendered_validator:
            fail(f"rendered validator missing required case: {marker}")

    acceptance_record = ACCEPTANCE_RECORD.read_text(encoding="utf-8")
    require_text(
        acceptance_record,
        (
            "Stable version: `1.6.0`",
            "Previous Stable baseline: `1.5.0`",
            "mandatory current Stable target",
            "Adaptive Workspace rendered matrix does not substitute",
        ),
        "1.6 Stable acceptance record",
    )

    print("Glaze UI retained 1.6 adaptive workspace/navigation contract validated under current 2.2 Stable")


if __name__ == "__main__":
    main()
