#!/usr/bin/env python3
"""Validate the canonical Glaze UI repository without third-party dependencies."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / "tokens" / "glaze.tokens.json"
REQUIRED = [
    ROOT / name
    for name in (
        "README.md",
        "LICENSE",
        "VERSION",
        "CHANGELOG.md",
        "COMPONENTS.md",
        "CONFORMANCE.md",
        "ADOPTION.md",
        "ACCEPTANCE.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
    )
]
REQUIRED += [
    ROOT / "tokens" / "README.md",
    TOKENS,
    ROOT / "css" / "glaze.css",
    ROOT / "css" / "glaze.controls.css",
    ROOT / "css" / "glaze.accessibility.css",
    ROOT / "reference" / "index.html",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Glaze UI validation failed: {message}")


def main() -> None:
    for path in REQUIRED:
        require(path.is_file(), f"missing required file: {path.relative_to(ROOT)}")

    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    require(re.fullmatch(r"\d+\.\d+\.\d+", version) is not None, "VERSION must use semantic versioning")

    data = json.loads(TOKENS.read_text(encoding="utf-8"))
    require(data["meta"]["version"] == version, "VERSION and token version differ")
    require(data["meta"]["name"] == "Glaze UI", "token identity is not Glaze UI")

    required_colors = (
        "canvas",
        "canvasAccent",
        "surface",
        "surfaceStrong",
        "surfaceMuted",
        "text",
        "muted",
        "line",
        "accent",
        "accentSecondary",
        "onAccent",
        "info",
        "success",
        "warning",
        "danger",
        "scrim",
        "focusRing",
        "selection",
    )
    for theme in ("light", "dark"):
        colors = data["color"][theme]
        for name in required_colors:
            require(name in colors, f"missing {theme} semantic color: {name}")

    for state in ("hover", "pressed", "focus", "selected"):
        require(0 < data["stateLayer"][state] < 1, f"invalid state-layer opacity: {state}")
    require(
        data["stateLayer"]["hover"] < data["stateLayer"]["pressed"] <= data["stateLayer"]["focus"],
        "state layers are not ordered",
    )

    require(data["target"]["minimum"] >= 44, "minimum target size must remain at least 44px")
    require(
        data["target"]["comfortable"] >= data["target"]["minimum"],
        "comfortable target is smaller than minimum",
    )
    require(list(data["icon"].values()) == sorted(data["icon"].values()), "icon sizes are not ordered")
    require(0 < data["opacity"]["placeholder"] <= 1, "placeholder opacity must be within (0, 1]")
    require(data["control"]["fieldGap"] > 0, "field gap must be positive")
    require(data["control"]["groupGap"] >= data["control"]["fieldGap"], "group gap must not be smaller than field gap")

    motion = data["motion"]
    require(
        motion["instant"] < motion["fast"] < motion["standard"] < motion["emphasized"],
        "motion durations are not ordered",
    )
    bp = data["breakpoint"]
    require(bp["mediumMin"] == bp["compactMax"] + 1, "Compact/Medium breakpoint gap")
    require(bp["expandedMin"] == bp["mediumMax"] + 1, "Medium/Expanded breakpoint gap")
    require(bp["wideMin"] == bp["expandedMax"] + 1, "Expanded/Wide breakpoint gap")
    layout = data["layout"]
    require(
        layout["gutterCompact"] <= layout["gutterMedium"] <= layout["gutterExpanded"] <= layout["gutterWide"],
        "adaptive gutters are not ordered",
    )

    css = (ROOT / "css" / "glaze.css").read_text(encoding="utf-8")
    controls = (ROOT / "css" / "glaze.controls.css").read_text(encoding="utf-8")
    accessibility = (ROOT / "css" / "glaze.accessibility.css").read_text(encoding="utf-8")
    reference = (ROOT / "reference" / "index.html").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    components = (ROOT / "COMPONENTS.md").read_text(encoding="utf-8")
    conformance = (ROOT / "CONFORMANCE.md").read_text(encoding="utf-8")
    adoption = (ROOT / "ADOPTION.md").read_text(encoding="utf-8")
    acceptance = (ROOT / "ACCEPTANCE.md").read_text(encoding="utf-8")

    required_css_tokens = (
        "--glaze-canvas",
        "--glaze-surface",
        "--glaze-surface-strong",
        "--glaze-accent",
        "--glaze-accent-2",
        "--glaze-on-accent",
        "--glaze-info",
        "--glaze-scrim",
        "--glaze-state-hover",
        "--glaze-state-pressed",
        "--glaze-state-focus",
        "--glaze-state-selected",
        "--glaze-icon-md",
        "--glaze-gutter",
        "--glaze-radius-xl",
        "--glaze-motion-standard",
        "--glaze-target-min",
        "--glaze-focus-width",
    )
    for token in required_css_tokens:
        require(token in css, f"canonical CSS missing {token}")

    for surface in (
        ".glaze-canvas",
        ".glaze-surface-solid",
        ".glaze-surface-raised",
        ".glaze-surface",
        ".glaze-overlay",
    ):
        require(surface in css, f"canonical CSS missing surface role {surface}")
    for primitive in (
        ".glaze-scrim",
        ".glaze-nav-item",
        ".glaze-toolbar",
        ".glaze-dialog",
        ".glaze-menu",
        ".glaze-toast",
        ".glaze-badge",
        ".glaze-safe-area",
    ):
        require(primitive in css, f"canonical CSS missing core primitive {primitive}")

    required_control_tokens = (
        "--glaze-focus-ring",
        "--glaze-selection",
        "--glaze-field-gap",
        "--glaze-group-gap",
        "--glaze-opacity-placeholder",
    )
    for token in required_control_tokens:
        require(token in controls, f"controls CSS missing {token}")

    for primitive in (
        ".glaze-field",
        ".glaze-field-label",
        ".glaze-field-message",
        ".glaze-textarea",
        ".glaze-choice",
        ".glaze-switch",
        ".glaze-segmented",
        ".glaze-progress",
        ".glaze-banner",
    ):
        require(primitive in controls, f"controls CSS missing 1.2 primitive {primitive}")

    require("accent-color: var(--glaze-accent)" in controls, "native checkbox/radio accent mapping missing")
    require("input:checked + .glaze-switch-track" in controls, "switch checked-state styling missing")
    require("aria-selected=\"true\"" in controls, "segmented selected-state semantic missing")
    require("--glaze-progress-value" in controls, "progress value semantic missing")

    required_state_usage = (
        "opacity: var(--glaze-state-hover)",
        "opacity: var(--glaze-state-pressed)",
        "var(--glaze-state-focus)",
        "var(--glaze-state-selected)",
    )
    for marker in required_state_usage:
        require(marker in css, f"canonical CSS does not apply state-layer semantic: {marker}")

    require(
        '.glaze-button[data-variant="primary"]' in css and ".glaze-button::after" in css,
        "primary button interaction layer is missing",
    )
    require("color: var(--glaze-on-accent)" in css, "primary controls must use the semantic on-accent role")

    for contract in (
        "prefers-reduced-motion",
        "prefers-reduced-transparency",
        "prefers-contrast",
        "forced-colors",
        "@supports not",
    ):
        require(contract in accessibility, f"accessibility CSS missing {contract}")

    for marker in (
        ".glaze-textarea",
        ".glaze-switch-track",
        ".glaze-segmented",
        ".glaze-progress",
        ".glaze-banner",
        "input:checked + .glaze-switch-track",
        "[aria-selected=\"true\"]",
        ".glaze-progress > span",
        "forced-color-adjust: none",
    ):
        require(marker in accessibility, f"accessibility CSS missing 1.2 control fallback: {marker}")

    forbidden_remote_markers = (
        "fonts.googleapis",
        "fonts.gstatic",
        "cdn.jsdelivr",
        "unpkg.com",
        "cdnjs.cloudflare",
        "google-analytics",
        "googletagmanager",
    )
    lowered_reference = reference.lower()
    for marker in forbidden_remote_markers:
        require(marker not in lowered_reference, f"reference page contains forbidden remote dependency marker: {marker}")
    require("http://" not in lowered_reference and "https://" not in lowered_reference, "reference page must remain network-independent")
    require(f"Glaze UI {version}" in reference, "reference page exact Glaze UI version identity missing")
    require("glaze.controls.css" in reference, "reference page must load the 1.2 controls layer")
    require("Beauty is a requirement" in readme, "README must preserve the visual-quality principle")
    require("selection controls" in components.lower(), "component contract must document selection controls")
    require("persistent" in components.lower() and "label" in components.lower(), "component contract must require persistent field labels")
    require(f"Glaze UI {version.rsplit('.', 1)[0]} conformant" in conformance, "conformance claim does not match current minor version")
    require("native platform controls" in adoption.lower(), "adoption guide must protect native control semantics")

    for marker in (
        "390 × 844",
        "1280 × 900",
        "forced-colors: active",
        "200% browser zoom",
        "persistent field labels",
        "textarea behavior",
        "checkbox and radio choices",
        "switches",
        "segmented controls/tabs",
        "progress indicators",
        "If any required check cannot be executed, the release remains a candidate.",
    ):
        require(marker in acceptance, f"acceptance protocol missing release gate: {marker}")

    require("MIT License" in (ROOT / "LICENSE").read_text(encoding="utf-8"), "MIT license text missing")

    print(f"Glaze UI {version} repository validated")


if __name__ == "__main__":
    main()
