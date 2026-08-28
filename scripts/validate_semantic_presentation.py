#!/usr/bin/env python3
"""Validate Glaze UI 1.6 Candidate semantic presentation."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "SEMANTIC_PRESENTATION.md"
TOKENS = ROOT / "tokens" / "semantic-presentation.candidate.json"
CSS = ROOT / "css" / "glaze.semantic-presentation.candidate.css"
REFERENCE = ROOT / "reference" / "candidate-1.6-semantic-presentation.html"

EXPECTED_STATES = {
    "information", "success", "warning", "danger", "privacy", "security",
    "protected", "restricted", "online", "offline", "syncing", "paused", "unavailable",
}
EXPECTED_PROFILES = {
    "enhanced-focus", "large-targets", "high-contrast",
    "reduced-transparency", "reduced-motion", "monochrome",
}


def fail(message: str) -> None:
    raise SystemExit(f"semantic presentation validation failed: {message}")


def require(text: str, markers: tuple[str, ...], source: str) -> None:
    for marker in markers:
        if marker not in text:
            fail(f"{source} missing required marker: {marker}")


def main() -> None:
    for path in (DOC, TOKENS, CSS, REFERENCE):
        if not path.is_file():
            fail(f"missing {path.relative_to(ROOT)}")

    try:
        data = json.loads(TOKENS.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid token JSON: {exc}")

    meta = data.get("meta", {})
    if meta.get("candidateVersion") != "1.6.0" or meta.get("status") != "Candidate":
        fail("semantic presentation must remain a 1.6.0 Candidate before promotion")
    if meta.get("stableBaseline") != "1.5.0":
        fail("Stable baseline must remain 1.5.0")

    states = data.get("states", {})
    if set(states) != EXPECTED_STATES:
        fail("semantic state family set changed unexpectedly")
    for name, spec in states.items():
        if not spec.get("symbolRole") or not spec.get("colorFamily"):
            fail(f"state {name} must bind both symbol and semantic color roles")
        if "label" not in spec.get("nonColorCue", ""):
            fail(f"state {name} must retain a visible/textual non-color companion")

    profiles = data.get("accessibilityProfiles", {})
    if set(profiles) != EXPECTED_PROFILES:
        fail("accessibility profile set changed unexpectedly")
    if profiles["large-targets"].get("nearViewMinimum") != 52:
        fail("large-target near-view minimum must remain 52")
    if profiles["large-targets"].get("tvMinimum") != 56:
        fail("TV target minimum must remain 56")
    if profiles["enhanced-focus"].get("focusWidth") != 4:
        fail("enhanced focus width must remain 4")

    invariants = data.get("invariants", {})
    for key in (
        "visibleLabelOrAccessibleName",
        "nonColorCompanion",
        "focusDistinctFromSelection",
        "osAccessibilityPreferenceNotWeakened",
        "identityAccentCannotOverrideProtectedSemantics",
        "presentationCannotUpgradeAuthority",
    ):
        if invariants.get(key) is not True:
            fail(f"invariant {key} must be true")

    if data.get("symbol", {}).get("registryStatus") != "Planned":
        fail("full System Icon Registry must not be represented as implemented")

    authority = data.get("authority", {})
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
    require(css, (
        ".glaze-semantic-status-candidate",
        ".glaze-semantic-symbol-candidate",
        "data-state=\"danger\"",
        "data-state=\"privacy\"",
        "data-state=\"security\"",
        "data-state=\"unavailable\"",
        "data-glaze-accessibility~=\"enhanced-focus\"",
        "data-glaze-accessibility~=\"large-targets\"",
        "data-glaze-accessibility~=\"high-contrast\"",
        "data-glaze-accessibility~=\"reduced-transparency\"",
        "data-glaze-accessibility~=\"reduced-motion\"",
        "data-glaze-accessibility~=\"monochrome\"",
        "@media (prefers-contrast: more)",
        "@media (prefers-reduced-transparency: reduce)",
        "@media (prefers-reduced-motion: reduce)",
        "@media (forced-colors: active)",
    ), "Candidate CSS")

    doc = DOC.read_text(encoding="utf-8")
    require(doc, (
        "Status: **Candidate**",
        "Meaning survives presentation changes.",
        "## Symbol-state binding",
        "## Non-color companion requirement",
        "## Explicit accessibility profiles",
        "## Monochrome presentation",
        "## Authority boundaries",
        "full System Icon Registry remains Planned",
    ), "documentation")

    reference = REFERENCE.read_text(encoding="utf-8")
    require(reference, (
        "Glaze UI 1.6 Candidate",
        "glaze.semantic-presentation.candidate.css",
        "data-glaze-accessibility=\"enhanced-focus large-targets\"",
        "glaze-semantic-status-candidate",
        "glaze-semantic-status-label-candidate",
        "aria-hidden=\"true\"",
        "Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Mesh",
    ), "reference")
    for state in EXPECTED_STATES:
        if f'data-state="{state}"' not in reference:
            fail(f"reference missing semantic state {state}")

    print("Glaze UI 1.6 Candidate semantic presentation validated")


if __name__ == "__main__":
    main()
