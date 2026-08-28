#!/usr/bin/env python3
"""Validate the enforced Glaze UI 2.0 Candidate contract without dependencies."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "GLAZE_UI_2.md"
TOKENS = ROOT / "tokens" / "glaze-2.candidate.json"
CSS = ROOT / "css" / "glaze-2.candidate.css"
JS = ROOT / "js" / "glaze-2.candidate.js"
REFERENCE = ROOT / "reference" / "candidate-2.0.html"
RENDER_HARNESS = ROOT / "reference" / "candidate-2.0-acceptance.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Glaze UI 2.0 Candidate validation failed: {message}")


def main() -> None:
    for path in (CONTRACT, TOKENS, CSS, JS, REFERENCE, RENDER_HARNESS):
        require(path.is_file(), f"missing required Candidate artifact: {path.relative_to(ROOT)}")

    contract = CONTRACT.read_text(encoding="utf-8")
    data = json.loads(TOKENS.read_text(encoding="utf-8"))
    css = CSS.read_text(encoding="utf-8")
    js = JS.read_text(encoding="utf-8")
    reference = REFERENCE.read_text(encoding="utf-8")
    render_harness = RENDER_HARNESS.read_text(encoding="utf-8")

    meta = data["meta"]
    require(meta["name"] == "Glaze UI", "wrong token identity")
    require(meta["version"] == "2.0.0", "Candidate semantic version must be 2.0.0")
    require(meta["status"] == "Candidate", "new contract must remain Candidate before promotion")
    require(meta["designContractStatus"] == "enforced", "administrator-enforced design status missing")
    require(meta["stableImplementationBaseline"] == "1.6.0", "last validated Stable baseline must remain explicit")
    require(meta["productionEligible"] is False, "Candidate must not claim production eligibility")
    require(meta["requiresStablePromotion"] is True, "Stable promotion gate must remain required")
    require(meta["governingSentence"] == "Make interaction feel tangible.", "governing sentence drifted")

    expected_levels = [
        (0, "Canvas"),
        (1, "Surface"),
        (2, "Soft Glaze"),
        (3, "Glaze"),
        (4, "Deep Glaze"),
        (5, "Live Glaze"),
    ]
    levels = [(item["level"], item["name"]) for item in data["material"]["levels"]]
    require(levels == expected_levels, "Glaze Material level order drifted")
    require(data["material"]["clarityModes"] == ["clear", "balanced", "solid"], "clarity modes drifted")
    require(data["material"]["readabilityOverridesEffect"] is True, "readability must override visual effect")

    geometry = data["geometry"]
    require(geometry["radiusScalePx"] == [4, 8, 12, 16, 24, 32], "radius scale drifted")
    require(geometry["capsuleRadiusPx"] == 999, "capsule radius drifted")
    require(geometry["concentric"] is True, "concentric geometry requirement missing")

    require(data["space"]["baseGridPx"] == 4, "spacing base grid must be 4px")
    require(data["space"]["scalePx"] == [4, 8, 12, 16, 24, 32, 48, 64], "spacing scale drifted")

    motion = data["motion"]
    require(motion["noTeleport"] is True, "Nothing teleports invariant missing")
    require(motion["families"]["utilityMs"] == [100, 180], "Utility motion range drifted")
    require(motion["families"]["fluidMs"] == [180, 400], "Fluid motion range drifted")
    require(motion["families"]["expressiveMs"] == [400, 700], "Expressive motion range drifted")
    require(motion["implementationAliasesMs"] == {"fast": 140, "standard": 280, "expressive": 520}, "motion aliases drifted")

    require(data["layout"]["mobileZones"] == ["viewing", "working", "glaze-action"], "mobile zones drifted")
    require(data["layout"]["transformRatherThanResize"] is True, "adaptive transform invariant missing")
    require(data["layout"]["foldableFirstClass"] is True and data["layout"]["hingeAware"] is True, "foldable contract incomplete")

    require(data["buttons"]["roles"] == ["quiet", "soft", "glaze", "emphasis"], "button roles drifted")
    require(data["connectedTransformation"]["signaturePattern"] is True, "Connected Transformation must remain a signature pattern")
    require(data["intelligence"]["presentationOnly"] is True, "intelligence grammar must remain presentation-only")
    require(data["intelligence"]["createsExecutionAuthority"] is False, "Glaze must not create agent execution authority")
    require(data["intelligence"]["createsDomainTruth"] is False, "Glaze must not create domain truth")
    require(data["accessibility"]["usableWithoutAdvancedEffects"] is True, "effects-free usability invariant missing")
    require(data["personalization"]["expression"] == ["calm", "balanced", "expressive"], "expression scale drifted")

    expected_namespaces = {
        "glaze.color.*", "glaze.type.*", "glaze.space.*", "glaze.shape.*", "glaze.material.*", "glaze.motion.*",
        "glaze.depth.*", "glaze.opacity.*", "glaze.blur.*", "glaze.border.*", "glaze.haptic.*", "glaze.layout.*", "glaze.state.*",
    }
    require(set(data["tokenNamespaces"]) == expected_namespaces, "semantic token namespaces drifted")

    for marker in (
        "Make interaction feel tangible.",
        "Content is solid. Interaction is glazed.",
        "Nothing teleports.",
        "Connected Transformation",
        "Clear — Balanced — Solid",
        "Calm, Balanced, Expressive",
        "Glaze UI 1.6.0",
        "Candidate",
    ):
        require(marker in contract, f"contract missing normative marker: {marker}")

    required_css = (
        "--glaze-shape-control: 999px",
        "--glaze-shape-card: 24px",
        "--glaze-motion-fast: 140ms",
        "--glaze-motion-standard: 280ms",
        "--glaze-motion-expressive: 520ms",
        "--glaze-touch-min: 48px",
        ".glaze-material-soft",
        ".glaze-material-deep",
        ".glaze-material-live",
        ".glaze-navigation-capsule",
        ".glaze-connected",
        ".glaze-live-surface",
        "prefers-reduced-motion",
        "prefers-reduced-transparency",
        "prefers-contrast",
        "forced-colors",
        "@supports not",
    )
    for marker in required_css:
        require(marker in css, f"Candidate CSS missing: {marker}")

    for marker in (
        "setClarity",
        "setExpression",
        "setAppearance",
        "interactionPoint",
        "data-glaze-interactive",
        "setNavigationScrollState",
        "connectedTransform",
        "document.startViewTransition",
        "prefers-reduced-motion",
        "MutationObserver",
    ):
        require(marker in js, f"Candidate runtime missing: {marker}")

    lowered_js = js.lower()
    for forbidden in (
        "fetch(",
        "xmlhttprequest",
        "websocket",
        "eventsource",
        "webtransport",
        "navigator.sendbeacon",
        "localstorage",
        "sessionstorage",
        "indexeddb",
        "document.cookie",
        "caches.open",
        "analytics",
        "sentry",
        "amplitude",
        "mixpanel",
        "segment.com",
        "eval(",
        "new function(",
        ".innerhtml",
        "document.write(",
    ):
        require(forbidden not in lowered_js, f"Candidate runtime contains forbidden network/storage/telemetry/unsafe-code marker: {forbidden}")

    # Candidate presentation and acceptance artifacts must remain self-contained.
    # Relative same-repository CSS/JS imports are allowed; remote/CDN dependencies are not.
    for label, source in (
        ("Candidate CSS", css),
        ("Candidate runtime", js),
        ("Candidate rendered reference", reference),
        ("Candidate rendered harness", render_harness),
    ):
        lowered = source.lower()
        for forbidden in (
            "http://",
            "https://",
            "@import ",
            "@import\t",
            "url(//",
            "src=\"//",
            "src='//",
            "href=\"//",
            "href='//",
        ):
            require(forbidden not in lowered, f"{label} contains forbidden remote dependency marker: {forbidden}")

    # The reference may import only the Candidate's same-repository implementation files.
    require('href="../css/glaze-2.candidate.css"' in reference, "rendered reference must use local Candidate CSS")
    require("from '../js/glaze-2.candidate.js'" in reference, "rendered reference must use local Candidate runtime")

    print("Glaze UI 2.0 Candidate contract validation passed; dependency/privacy/security boundary intact")


if __name__ == "__main__":
    main()
