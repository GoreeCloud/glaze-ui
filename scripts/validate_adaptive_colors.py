#!/usr/bin/env python3
"""Validate the GLAZE UI V1.0 adaptive color stable contract."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / "tokens" / "adaptive-colors.json"
DOC = ROOT / "COLOR_ARCHITECTURE.md"
CSS = ROOT / "css" / "glaze.color.css"

FAMILIES = {
    "accent", "success", "information", "warning", "danger", "privacy",
    "security", "online", "offline", "syncing", "protected", "restricted",
    "unavailable",
}
PROMINENCE = ["subtle", "standard", "prominent", "critical"]
MODES = {
    "light", "dark", "high-contrast", "forced-colors", "grayscale",
    "color-vision-deficiency", "reduced-transparency",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Adaptive color validation failed: {message}")


def main() -> None:
    for path in (TOKENS, DOC, CSS):
        require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    data = json.loads(TOKENS.read_text(encoding="utf-8"))
    require(data.get("schemaVersion") == 1, "schemaVersion must be 1")
    require(data.get("designSystem") == "Glaze UI", "design system mismatch")
    require(data.get("stableRelease") == "1.5.0", "stable release must be 1.5.0")
    require(data.get("stableBaseline") == "1.5.0", "Stable baseline must remain 1.5.0")
    require(data.get("status") == "stable", "adaptive colors must remain Stable")
    require(data.get("colorOnlyCommunicationAllowed") is False, "color-only communication must remain forbidden")
    require(data.get("identityMayOverrideSemantics") is False, "identity may not override semantics")
    require(data.get("prominenceLevels") == PROMINENCE, "prominence level order mismatch")
    require(set(data.get("families", {})) == FAMILIES, "semantic family set mismatch")
    require(data["families"]["privacy"].get("authority") == "privacy-shield", "Privacy Shield must remain privacy authority")
    require(data["families"]["security"].get("authority") == "wardveil-security", "Wardveil must remain security authority")
    require(data["families"]["protected"].get("evidenceRequired") is True, "protected state must require evidence")
    require(set(data.get("accessibilityModes", [])) == MODES, "accessibility mode set mismatch")
    accent = data.get("adaptiveAccent", {})
    require(accent.get("decorativeOnly") is True, "adaptive accent inputs must remain decorative")
    require("danger" in accent.get("protectedFamilies", []), "danger must be protected from accent recoloring")
    require(data.get("materials", {}).get("solidFallbackRequired") is True, "material sampling must have solid fallback")
    require(data.get("motion", {}).get("reducedMotionAlternativeRequired") is True, "reduced-motion alternative required")
    require(data.get("motion", {}).get("flashingRequired") is False, "flashing must never be required")

    doc = DOC.read_text(encoding="utf-8").lower()
    for phrase in (
        "semantic tonal families", "adaptive accent coloring", "materials and depth",
        "motion and color", "accessibility architecture", "promotion boundary",
        "selection.glaze",
    ):
        require(phrase in doc, f"documentation missing {phrase}")

    css = CSS.read_text(encoding="utf-8")
    for phrase in ("prefers-reduced-motion", "prefers-contrast", "forced-colors", "color-mix"):
        require(phrase in css, f"CSS missing {phrase}")

    print("GLAZE UI V1.0 adaptive color stable validation passed; Stable remains 1.5.0")


if __name__ == "__main__":
    main()
