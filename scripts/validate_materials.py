#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / "tokens" / "materials.json"
DOC = ROOT / "MATERIALS.md"
CSS = ROOT / "css" / "glaze.materials.css"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Glaze UI material validation failed: {message}")


def main() -> None:
    require(TOKENS.exists(), "tokens/materials.json is missing")
    require(DOC.exists(), "MATERIALS.md is missing")
    require(CSS.exists(), "css/glaze.materials.css is missing")

    data = json.loads(TOKENS.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")

    meta = data.get("meta", {})
    require(meta.get("status") == "Candidate", "material token status must remain Candidate")
    require(meta.get("stableBaseline") == "1.4.0", "material Candidate must preserve the 1.4.0 Stable baseline")
    require(meta.get("contract") == "MATERIALS.md", "material token contract must bind to MATERIALS.md")

    required_roles = {"canvas", "solid", "raised", "functionalGlass", "clearGlass", "overlay"}
    roles = data.get("roles", {})
    require(required_roles.issubset(roles), f"missing semantic material roles: {sorted(required_roles - set(roles))}")
    require(roles["solid"].get("backdropSampling") is False, "Solid must not depend on backdrop sampling")
    require(roles["functionalGlass"].get("backdropSampling") is True, "Functional Glass must declare bounded backdrop sampling")
    require(roles["clearGlass"].get("defaultContentMaterial") is False, "Clear Glass must never be the default content material")
    require(roles["overlay"].get("scrimRequiredWhenModal") is True, "modal Overlay must require semantic separation")

    required_depth = {"base": 0, "raised": 10, "navigation": 100, "scrim": 900, "overlay": 1000, "toast": 1100}
    require(data.get("depth") == required_depth, "semantic depth map changed without contract review")

    fallback = data.get("fallbacks", {})
    reduced = fallback.get("reducedTransparency", {})
    require(fallback.get("unsupportedBackdrop") == "solid-or-raised", "unsupported backdrop must fall back to Solid/Raised semantics")
    require(reduced.get("blurPx") == 0, "reduced transparency must remove blur")
    require(reduced.get("preserveHierarchy") is True, "reduced transparency must preserve hierarchy")
    require(reduced.get("preserveInformation") is True, "reduced transparency must preserve information")
    require(reduced.get("webAdapter") == "data-glaze-reduced-transparency=true", "portable web reduced-transparency adapter metadata missing")
    require(reduced.get("mediaQuery") == "progressive-enhancement-only", "reduced-transparency media query must remain progressive enhancement")

    accessibility = data.get("accessibility", {})
    require(accessibility.get("blurAloneMayProvideContrast") is False, "blur may not be the only contrast mechanism")
    require(accessibility.get("criticalContentPrefersStableSurface") is True, "critical content must prefer stable surfaces")
    require(accessibility.get("worstPermittedBackdropMustRemainLegible") is True, "worst permitted backdrop legibility must be required")
    require(accessibility.get("reducedTransparencyIndependentOfReducedMotion") is True, "reduced transparency must remain independent of reduced motion")

    performance = data.get("performance", {})
    require(performance.get("allowNestedBackdropStacks") is False, "nested backdrop stacks must remain disallowed")
    require(performance.get("continuousDecorativeRefractionAllowed") is False, "continuous decorative refraction must remain disallowed")

    authority = data.get("authority", {})
    require(authority.get("privacy") == "Privacy Shield", "Privacy Shield authority boundary missing")
    require(authority.get("security") == "Wardveil Security", "Wardveil Security authority boundary missing")
    require(authority.get("resilience") == "Everkeep", "Everkeep authority boundary missing")
    require(authority.get("coordination") == "GoreeCloud Mesh", "GoreeCloud Mesh authority boundary missing")
    require(authority.get("presentation") == "Glaze UI", "Glaze UI presentation authority missing")

    for phrase in (
        "Ordinary content defaults to **Solid** or **Raised**",
        "Reduced transparency is independent from reduced motion",
        "explicit semantic preference path is the portable contract",
        "Performance degradation must fall back toward Solid/Raised semantics",
        "Privacy Shield",
        "Wardveil Security",
        "Everkeep",
        "GoreeCloud Mesh",
    ):
        require(phrase in doc, f"MATERIALS.md missing required contract phrase: {phrase}")

    for selector in (
        ".glaze-material-solid",
        ".glaze-material-raised",
        ".glaze-material-functional-glass",
        ".glaze-material-clear-glass",
        ".glaze-material-overlay",
        "prefers-reduced-transparency",
        "data-glaze-reduced-transparency",
        "data-glaze-performance",
        "@supports not",
    ):
        require(selector in css, f"material CSS missing required primitive/fallback: {selector}")

    print("Glaze UI 1.5 material and depth Candidate validation passed.")


if __name__ == "__main__":
    main()