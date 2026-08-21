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
        "COMPONENT_STATUS.md",
        "STABILITY.md",
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
    ROOT / "css" / "glaze.expressive.css",
    ROOT / "css" / "glaze.accessibility.css",
    ROOT / "reference" / "index.html",
    ROOT / "reference" / "acceptance.html",
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
    lineage = data["meta"].get("lineage", "")
    for marker in ("One UI 8.5", "Liquid Glass", "Material 3 Expressive", "GoreeCloud"):
        require(marker in lineage, f"1.3 design lineage missing {marker}")

    required_colors = (
        "canvas", "canvasAccent", "surface", "surfaceStrong", "surfaceMuted", "text", "muted", "line",
        "accent", "accentSecondary", "onAccent", "info", "success", "warning", "danger", "scrim", "focusRing", "selection",
    )
    for theme in ("light", "dark"):
        colors = data["color"][theme]
        for name in required_colors:
            require(name in colors, f"missing {theme} semantic color: {name}")

    for state in ("hover", "pressed", "focus", "selected"):
        require(0 < data["stateLayer"][state] < 1, f"invalid state-layer opacity: {state}")
    require(data["stateLayer"]["hover"] < data["stateLayer"]["pressed"] <= data["stateLayer"]["focus"], "state layers are not ordered")

    require(data["target"]["minimum"] >= 44, "minimum target size must remain at least 44px")
    require(data["target"]["comfortable"] >= data["target"]["minimum"], "comfortable target is smaller than minimum")
    require(list(data["icon"].values()) == sorted(data["icon"].values()), "icon sizes are not ordered")
    require(0 < data["opacity"]["placeholder"] <= 1, "placeholder opacity must be within (0, 1]")
    require(data["control"]["fieldGap"] > 0, "field gap must be positive")
    require(data["control"]["groupGap"] >= data["control"]["fieldGap"], "group gap must not be smaller than field gap")

    shapes = data["shape"]
    require(shapes["compact"] < shapes["standard"] < shapes["expressive"] < shapes["hero"], "expressive shape scale is not ordered")
    require(shapes["pressed"] <= shapes["standard"], "pressed shape must remain tighter than standard geometry")

    material = data["material"]
    for role in ("functionalGlass", "clearGlass"):
        require(material[role]["blur"] > 0, f"{role} blur must be positive")
        require(material[role]["saturation"] >= 100, f"{role} saturation must not desaturate content")
        require(0 < material[role]["opacity"] < 1, f"{role} opacity must be translucent")
    require(material["clearGlass"]["opacity"] < material["functionalGlass"]["opacity"], "Clear Glass must remain more transparent than Functional Glass")
    require("Solid" in material["contentRule"] and "Raised" in material["contentRule"], "content material rule must preserve Solid/Raised defaults")

    motion = data["motion"]
    require(motion["instant"] < motion["fast"] < motion["standard"] < motion["emphasized"], "base motion durations are not ordered")
    require(motion["effectsFast"] < motion["effectsStandard"], "effects motion durations are not ordered")
    require(motion["spatialFast"] < motion["spatialStandard"] < motion["spatialEmphasized"], "spatial motion durations are not ordered")

    bp = data["breakpoint"]
    require(bp["mediumMin"] == bp["compactMax"] + 1, "Compact/Medium breakpoint gap")
    require(bp["expandedMin"] == bp["mediumMax"] + 1, "Medium/Expanded breakpoint gap")
    require(bp["wideMin"] == bp["expandedMax"] + 1, "Expanded/Wide breakpoint gap")
    layout = data["layout"]
    require(layout["gutterCompact"] <= layout["gutterMedium"] <= layout["gutterExpanded"] <= layout["gutterWide"], "adaptive gutters are not ordered")
    require(layout["reachZoneGap"] > 0 and "keyboard" in layout["compactReachability"], "compact reachability contract is incomplete")

    css = (ROOT / "css" / "glaze.css").read_text(encoding="utf-8")
    controls = (ROOT / "css" / "glaze.controls.css").read_text(encoding="utf-8")
    expressive = (ROOT / "css" / "glaze.expressive.css").read_text(encoding="utf-8")
    accessibility = (ROOT / "css" / "glaze.accessibility.css").read_text(encoding="utf-8")
    reference = (ROOT / "reference" / "index.html").read_text(encoding="utf-8")
    rendered_harness = (ROOT / "reference" / "acceptance.html").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    components = (ROOT / "COMPONENTS.md").read_text(encoding="utf-8")
    component_status = (ROOT / "COMPONENT_STATUS.md").read_text(encoding="utf-8")
    stability = (ROOT / "STABILITY.md").read_text(encoding="utf-8")
    conformance = (ROOT / "CONFORMANCE.md").read_text(encoding="utf-8")
    adoption = (ROOT / "ADOPTION.md").read_text(encoding="utf-8")
    acceptance = (ROOT / "ACCEPTANCE.md").read_text(encoding="utf-8")

    required_css_tokens = (
        "--glaze-canvas", "--glaze-surface", "--glaze-surface-strong", "--glaze-accent", "--glaze-accent-2",
        "--glaze-on-accent", "--glaze-info", "--glaze-scrim", "--glaze-state-hover", "--glaze-state-pressed",
        "--glaze-state-focus", "--glaze-state-selected", "--glaze-icon-md", "--glaze-gutter", "--glaze-radius-xl",
        "--glaze-motion-standard", "--glaze-target-min", "--glaze-focus-width",
    )
    for token in required_css_tokens:
        require(token in css, f"canonical CSS missing {token}")

    for surface in (".glaze-canvas", ".glaze-surface-solid", ".glaze-surface-raised", ".glaze-surface", ".glaze-overlay"):
        require(surface in css, f"canonical CSS missing surface role {surface}")
    for primitive in (".glaze-scrim", ".glaze-nav-item", ".glaze-toolbar", ".glaze-dialog", ".glaze-menu", ".glaze-toast", ".glaze-badge", ".glaze-safe-area"):
        require(primitive in css, f"canonical CSS missing core primitive {primitive}")

    required_control_tokens = ("--glaze-focus-ring", "--glaze-selection", "--glaze-field-gap", "--glaze-group-gap", "--glaze-opacity-placeholder")
    for token in required_control_tokens:
        require(token in controls, f"controls CSS missing {token}")
    for primitive in (".glaze-field", ".glaze-field-label", ".glaze-field-message", ".glaze-textarea", ".glaze-choice", ".glaze-switch", ".glaze-segmented", ".glaze-progress", ".glaze-banner"):
        require(primitive in controls, f"controls CSS missing retained 1.2 primitive {primitive}")
    require("accent-color: var(--glaze-accent)" in controls, "native checkbox/radio accent mapping missing")
    require("input:checked + .glaze-switch-track" in controls, "switch checked-state styling missing")
    require("aria-selected=\"true\"" in controls, "segmented selected-state semantic missing")
    require("--glaze-progress-value" in controls, "progress value semantic missing")

    for marker in (
        "--glaze-glass-regular-blur", "--glaze-glass-clear-opacity", "--glaze-shape-expressive", "--glaze-motion-effects-fast",
        "--glaze-motion-spatial-standard", ".glaze-glass-functional", ".glaze-glass-clear", ".glaze-expressive-action",
        ".glaze-expressive-tile", ".glaze-button-group", ".glaze-reach-layout", ".glaze-reach-actions", ".glaze-hero-type",
        "prefers-reduced-motion", "prefers-reduced-transparency", "forced-colors", "@supports not",
    ):
        require(marker in expressive, f"1.3 expressive CSS missing {marker}")

    for marker in ("opacity: var(--glaze-state-hover)", "opacity: var(--glaze-state-pressed)", "var(--glaze-state-focus)", "var(--glaze-state-selected)"):
        require(marker in css, f"canonical CSS does not apply state-layer semantic: {marker}")
    require('.glaze-button[data-variant="primary"]' in css and ".glaze-button::after" in css, "primary button interaction layer is missing")
    require("color: var(--glaze-on-accent)" in css, "primary controls must use the semantic on-accent role")

    for contract in ("prefers-reduced-motion", "prefers-reduced-transparency", "prefers-contrast", "forced-colors", "@supports not"):
        require(contract in accessibility, f"accessibility CSS missing {contract}")
    for marker in (".glaze-textarea", ".glaze-switch-track", ".glaze-segmented", ".glaze-progress", ".glaze-banner", "input:checked + .glaze-switch-track", "[aria-selected=\"true\"]", ".glaze-progress > span", "forced-color-adjust: none"):
        require(marker in accessibility, f"accessibility CSS missing retained 1.2 control fallback: {marker}")

    forbidden_remote_markers = ("fonts.googleapis", "fonts.gstatic", "cdn.jsdelivr", "unpkg.com", "cdnjs.cloudflare", "google-analytics", "googletagmanager")
    lowered_reference = reference.lower()
    for marker in forbidden_remote_markers:
        require(marker not in lowered_reference, f"reference page contains forbidden remote dependency marker: {marker}")
    require("http://" not in lowered_reference and "https://" not in lowered_reference, "reference page must remain network-independent")
    require(f"Glaze UI {version}" in reference, "reference page exact Glaze UI version identity missing")
    require("glaze.controls.css" in reference and "glaze.expressive.css" in reference, "reference page must load controls and expressive layers")
    for marker in ("glaze-glass-functional", "glaze-glass-clear", "glaze-button-group", "glaze-reach-layout", "glaze-hero-type", "glaze-segmented", "glaze-progress", "glaze-overlay"):
        require(marker in reference, f"reference page missing 1.3/retained acceptance role: {marker}")

    require("Beauty is a requirement" in readme, "README must preserve the visual-quality principle")
    require("One UI 8.5" in readme and "Liquid Glass" in readme and "Material 3 Expressive" in readme, "README design lineage is incomplete")
    require("## Stability priority" in readme, "README must make stabilization-first policy explicit")
    require("STABILITY.md" in readme and "COMPONENT_STATUS.md" in readme, "README must link stability governance")
    require("selection controls" in components.lower(), "component contract must document selection controls")
    require("persistent" in components.lower() and "label" in components.lower(), "component contract must require persistent field labels")
    require("Functional Glass" in components and "Clear Glass" in components, "component contract missing material boundaries")

    for marker in ("### Stable", "### Candidate", "### Experimental", "### Planned", "Glaze UI 1.3 Stable foundations", "Candidate form-factor layer", "Experimental and roadmap boundary"):
        require(marker in component_status, f"component lifecycle record missing {marker}")
    require("Glaze Intelligence Layer" in component_status and "Planned/roadmap concepts" in component_status, "roadmap concepts must remain non-shipping in lifecycle record")

    for marker in ("Stable baseline", "Glaze UI 1.3.0", "Stable promotion gate", "If any applicable gate is incomplete, the release remains Candidate.", "Regression blockers", "Consumer compatibility"):
        require(marker in stability, f"stability contract missing {marker}")
    require("speculative intelligence" in stability.lower() and "roadmap concept" in stability.lower(), "stability contract must exclude speculative roadmap features from Stable")

    require(f"Glaze UI {version.rsplit('.', 1)[0]} conformant" in conformance, "conformance claim does not match current minor version")
    require("form-factor fidelity" in conformance.lower(), "conformance contract missing form-factor fidelity gate")
    require("phone" in conformance.lower() and "tablet" in conformance.lower() and "desktop" in conformance.lower(), "conformance contract missing phone/tablet/desktop coverage")
    require("Stability and lifecycle" in conformance, "conformance contract missing stability/lifecycle gate")
    require("COMPONENT_STATUS.md" in conformance and "STABILITY.md" in conformance, "conformance must bind lifecycle and stability records")
    require("native platform controls" in adoption.lower(), "adoption guide must protect native control semantics")
    require("## 8. Design explicitly for phone, tablet, and desktop" in adoption, "adoption guide missing explicit form-factor guidance")
    require("shrunken tablet or desktop" in adoption.lower(), "phone anti-scaling rule missing")
    require("stretched phone" in adoption.lower(), "tablet anti-scaling rule missing")
    require("enlarged mobile" in adoption.lower(), "desktop anti-scaling rule missing")

    for marker in (
        "390 × 844", "820 × 1180", "1280 × 900", "1600 × 1000", "forced-colors: active", "200% browser zoom",
        "persistent field labels", "textarea behavior", "checkbox and radio choices", "switches", "segmented controls/tabs",
        "progress indicators", "Functional Glass", "Clear Glass", "adaptive button-group emphasis", "compact reachability",
        "Form-factor fidelity acceptance", "Phone", "Tablet", "Desktop", "representative task flow",
        "Stability promotion acceptance", "COMPONENT_STATUS.md", "STABILITY.md",
        "If any required check cannot be executed, the release remains a candidate.",
    ):
        require(marker in acceptance, f"acceptance protocol missing release gate: {marker}")
    for marker in ("functional glass did not render", "clear glass did not render", "1.3 expressive roles rendered"):
        require(marker in rendered_harness, f"rendered acceptance harness missing 1.3 check: {marker}")

    require("MIT License" in (ROOT / "LICENSE").read_text(encoding="utf-8"), "MIT license text missing")
    print(f"Glaze UI {version} repository validated")


if __name__ == "__main__":
    main()
