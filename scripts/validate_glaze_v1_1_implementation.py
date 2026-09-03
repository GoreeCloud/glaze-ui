#!/usr/bin/env python3
"""Validate the isolated GLAZE UI V1.1 implementation candidate.

This gate proves source isolation and contract fidelity only. It does not prove
rendered acceptance, human optical review, native-platform fidelity, release
promotion, consumer conformance, or production stability.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURRENT_ENTRY = ROOT / "css" / "glaze-v1.0.0.css"
CANDIDATE_CSS = ROOT / "css" / "glaze-v1.1-candidate.css"
ATMOSPHERE = ROOT / "tokens" / "glaze-v1.1-atmosphere.candidate.json"
OPTICAL = ROOT / "contracts" / "v1.1" / "optical-refinement.candidate.json"
REFERENCE_DIR = ROOT / "reference" / "v1.1"
ACTIVATION = 'html[data-glaze-version-candidate="1.1"]'


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    errors: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    require(CURRENT_ENTRY.is_file(), "current V1.0 web entrypoint is missing")
    require(CANDIDATE_CSS.is_file(), "V1.1 candidate CSS is missing")
    require(ATMOSPHERE.is_file(), "V1.1 atmosphere token contract is missing")
    require(OPTICAL.is_file(), "V1.1 optical contract is missing")
    require(REFERENCE_DIR.is_dir(), "V1.1 reference directory is missing")
    if errors:
        for error in errors:
            print(f"- {error}")
        return 1

    current_entry = CURRENT_ENTRY.read_text(encoding="utf-8")
    css = CANDIDATE_CSS.read_text(encoding="utf-8")
    atmosphere = load_json(ATMOSPHERE)
    optical = load_json(OPTICAL)

    # Current consumers must remain unable to activate V1.1 accidentally.
    require("v1.1" not in current_entry.lower(), "current V1.0 entrypoint must not import or mention V1.1 candidate source")
    require('@import url("./glaze-v1.0.0.css");' in css, "V1.1 candidate must inherit the official V1.0 web entrypoint")
    require(ACTIVATION in css, "V1.1 candidate CSS must require an explicit root activation attribute")

    # Candidate CSS may refine presentation but must not add material sampling or hidden runtime behavior.
    require("backdrop-filter" not in css.lower(), "V1.1 candidate CSS must not add backdrop-filter declarations; inherit V1 material behavior")
    require("@keyframes" not in css.lower(), "V1.1 candidate must not introduce decorative keyframe animation")
    require("http://" not in css.lower() and "https://" not in css.lower(), "V1.1 candidate CSS must not depend on remote assets")
    require("javascript:" not in css.lower(), "V1.1 candidate CSS must not embed script URLs")

    protected_assignments = re.compile(
        r"--glz1-(?:focus|info|success|warning|critical|protected|restricted|online|offline|syncing|unavailable)\s*:",
        re.IGNORECASE,
    )
    require(not protected_assignments.search(css), "V1.1 optical candidate must not redefine current semantic/protected V1 variables")

    # Every candidate selector must be activation-gated. Declarations and at-rules are ignored.
    for line_number, line in enumerate(css.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith(("/*", "*", "*/", "@", "--")):
            continue
        if stripped.startswith(("html", ".", "body", "#", "[", ":")) and (stripped.endswith("{") or stripped.endswith(",")):
            require(stripped.startswith(ACTIVATION), f"candidate selector is not root-gated at CSS line {line_number}: {stripped}")

    # Frozen primitive palette must be represented exactly.
    for name, value in atmosphere["primitives"].items():
        require(value.lower() in css.lower(), f"candidate CSS is missing frozen primitive {name}={value}")

    geometry = optical["opticalGeometryReferencesPx"]
    expected_geometry = {
        "micro": "--glz11-radius-micro: 8px",
        "control": "--glz11-radius-control: 16px",
        "container": "--glz11-radius-container: 24px",
        "hero": "--glz11-radius-hero: 32px",
        "capsule": "--glz11-radius-capsule: 999px",
    }
    for role, marker in expected_geometry.items():
        require(geometry[role] == int(re.search(r"(\d+)px", marker).group(1)), f"machine geometry drift for {role}")
        require(marker in css, f"candidate CSS missing geometry marker for {role}")

    expected_aura_markers = {
        "light": ("rgba(15, 107, 111, 0.08)", "rgba(217, 163, 95, 0.04)"),
        "dark": ("rgba(15, 107, 111, 0.12)", "rgba(217, 163, 95, 0.06)"),
        "deepDark": ("rgba(15, 107, 111, 0.16)", "rgba(217, 163, 95, 0.08)"),
    }
    for appearance, (teal, amber) in expected_aura_markers.items():
        require(atmosphere["auraMaxCompositedAlpha"][appearance]["teal"] == float(teal.rsplit(" ", 1)[1][:-1]), f"machine teal Aura drift for {appearance}")
        require(atmosphere["auraMaxCompositedAlpha"][appearance]["amber"] == float(amber.rsplit(" ", 1)[1][:-1]), f"machine amber Aura drift for {appearance}")
        require(teal in css and amber in css, f"candidate CSS missing Aura caps for {appearance}")

    tint_markers = {
        "softGlaze": ("0.03", "0.01"),
        "glaze": ("0.05", "0.015"),
        "deepGlaze": ("0.07", "0.02"),
        "liveGlaze": ("0.08", "0.025"),
    }
    for role, (teal_alpha, amber_alpha) in tint_markers.items():
        values = atmosphere["materialTintMaxContribution"][role]
        require(values["teal"] == float(teal_alpha) and values["amber"] == float(amber_alpha), f"machine tint drift for {role}")
        require(f"rgba(15, 107, 111, {teal_alpha})" in css, f"candidate CSS missing teal tint cap for {role}")
        require(f"rgba(217, 163, 95, {amber_alpha})" in css, f"candidate CSS missing amber tint cap for {role}")

    # Required accessibility suppression paths must be explicit in the candidate layer.
    for marker in (
        'data-glz-transparency="reduced"',
        'data-mode="increased-contrast"',
        "prefers-reduced-motion: reduce",
        "forced-colors: active",
        "background-image: none !important",
    ):
        require(marker in css, f"candidate CSS missing accessibility fallback marker: {marker}")

    require("--glz11-target-min: 48px" in css, "candidate must preserve the V1 48px touch target floor")
    require("--glz11-target-min: 56px" in css, "candidate must preserve Touch Assistance 56px target behavior")

    # Reference families must explicitly opt in, remain local/static, and cover required form factors.
    references = {
        "desktop-workspace": REFERENCE_DIR / "desktop-workspace.html",
        "mobile-application": REFERENCE_DIR / "mobile-application.html",
        "tablet-dashboard": REFERENCE_DIR / "tablet-dashboard.html",
    }
    for scene, path in references.items():
        require(path.is_file(), f"missing V1.1 reference scene: {scene}")
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        require('data-glaze-version-candidate="1.1"' in text, f"{scene} must explicitly opt into V1.1 candidate")
        require('href="../../css/glaze-v1.1-candidate.css"' in text, f"{scene} must load candidate CSS directly")
        require(f'data-glz11-scene="{scene}"' in text, f"{scene} must identify its reference family")
        require("<script" not in text.lower(), f"{scene} must remain static and script-free in the first candidate")
        require("http://" not in text.lower() and "https://" not in text.lower(), f"{scene} must not depend on remote content")

    appearances = {
        "desktop-workspace": "dark",
        "mobile-application": "light",
        "tablet-dashboard": "deep-dark",
    }
    for scene, appearance in appearances.items():
        text = references[scene].read_text(encoding="utf-8")
        require(f'data-glz-appearance="{appearance}"' in text, f"{scene} must cover {appearance} appearance")

    # Optional Environmental Color Memory is deliberately not implemented yet.
    require(optical["environmentalColorMemory"]["requiredForConformance"] is False, "machine contract must keep Environmental Color Memory optional")
    require("environmental-color-memory" not in css.lower(), "first implementation candidate must not add environmental sampling behavior")

    if errors:
        print("GLAZE UI V1.1 implementation candidate validation FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("GLAZE UI V1.1 isolated implementation candidate: PASS")
    print("Boundary: source isolation and contract fidelity only; rendered/human/native/release acceptance remains separate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
