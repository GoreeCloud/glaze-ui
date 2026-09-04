#!/usr/bin/env python3
"""Fail closed when the GLAZE UI V1.2 Frosted Neutral Candidate drifts."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKEN_PATH = ROOT / "tokens/glaze-v1.2-frosted-neutral.candidate.json"
CSS_PATH = ROOT / "css/glaze-v1.2-frosted-neutral.candidate.css"
ENTRYPOINT_PATH = ROOT / "css/glaze-v1.2.0-candidate.css"
REFERENCE_PATH = ROOT / "reference/v1.2/frosted-neutral.html"
CONTRACT_PATH = ROOT / "GLAZE_UI_V1_2_CANDIDATE.md"


def req(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"GLAZE UI V1.2 Candidate validation failed: {message}")


def text(path: Path) -> str:
    req(path.is_file(), f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def rgba_channels(value: str) -> tuple[int, int, int, float]:
    match = re.fullmatch(
        r"rgba\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(0(?:\.\d+)?|1(?:\.0+)?)\s*\)",
        value,
    )
    req(match is not None, f"expected rgba token, got {value!r}")
    assert match is not None
    r, g, b = (int(match.group(i)) for i in range(1, 4))
    alpha = float(match.group(4))
    req(all(0 <= channel <= 255 for channel in (r, g, b)), f"invalid rgba channel in {value!r}")
    req(0 <= alpha <= 1, f"invalid alpha in {value!r}")
    return r, g, b, alpha


def near_neutral(value: str, tolerance: int = 4) -> bool:
    r, g, b, _ = rgba_channels(value)
    return max(r, g, b) - min(r, g, b) <= tolerance


def main() -> None:
    tokens = json.loads(text(TOKEN_PATH))
    css = text(CSS_PATH)
    entrypoint = text(ENTRYPOINT_PATH)
    reference = text(REFERENCE_PATH)
    contract = text(CONTRACT_PATH)

    req(tokens.get("lifecycle") == "candidate", "token lifecycle must remain Candidate")
    req(tokens.get("stableBaseline") == "1.1.0", "Candidate must remain based on V1.1 Stable")
    req(tokens.get("currentStableToken") is False, "Candidate token must not claim Stable authority")
    req(
        tokens.get("governingRule") == "Neutral glass is the material. Color is an accent.",
        "governing visual rule drifted",
    )

    materials = tokens.get("materials", {})
    for appearance in ("light", "dark", "deepDark"):
        role = materials.get(appearance)
        req(isinstance(role, dict), f"missing {appearance} material tokens")
        assert isinstance(role, dict)
        for key in ("baseGlass", "raisedGlass", "overlayGlass", "panelGlass"):
            value = role.get(key)
            req(isinstance(value, str), f"missing {appearance}.{key}")
            assert isinstance(value, str)
            req(near_neutral(value), f"{appearance}.{key} must remain chromatically neutral: {value}")

    chroma = tokens.get("chromaticMaterialPolicy", {})
    req(chroma.get("defaultChromaticMaterialTint") == 0, "default chromatic substrate tint must be zero")
    for key in (
        "tealAsBaseMaterialAllowed",
        "greenAsBaseMaterialAllowed",
        "aquaAsBaseMaterialAllowed",
        "amberAsBaseMaterialAllowed",
        "brandColorMayDefineSubstrate",
        "semanticColorMayDefineSubstrate",
    ):
        req(chroma.get(key) is False, f"{key} must remain false")

    hierarchy = tokens.get("hierarchyRules", {})
    req(hierarchy.get("depthBeforeHue") is True, "depth-before-hue invariant missing")
    req(hierarchy.get("nestedBackdropBlurDefaultAllowed") is False, "nested backdrop blur must remain disabled by default")
    req(hierarchy.get("dominantGlazeRegionsMax") == 1, "dominant Glaze budget changed")
    req(hierarchy.get("smallFloatingGlazeControlsMax") == 3, "floating Glaze budget changed")

    accessibility = tokens.get("accessibility", {})
    req(accessibility.get("reducedTransparency", {}).get("backdropBlur") == "off", "Reduced Transparency must disable blur")
    req(accessibility.get("forcedColors", {}).get("customMaterialPigmentation") == "off", "Forced Colors must disable custom material pigmentation")

    activation = 'html[data-glaze-version="1.1"][data-glaze-upgrade="v1.2-frosted-neutral"]'
    req(activation in css, "Candidate CSS activation selector missing")
    req("--glz11-tint-glaze-teal: transparent" in css, "V1.1 teal material tint is not neutralized")
    req("--glz11-tint-glaze-amber: transparent" in css, "V1.1 amber material tint is not neutralized")
    req("background-image: none" in css, "inherited chromatic background images are not explicitly removed")
    req("@media (forced-colors: active)" in css, "Forced Colors fallback missing")
    req('data-glz-transparency="reduced"' in css, "Reduced Transparency fallback missing")
    req("backdrop-filter: none" in css, "no-backdrop fallback missing")

    req('@import url("./glaze-v1.1.0.css")' in entrypoint, "Candidate entrypoint must inherit V1.1 Stable")
    req(
        '@import url("./glaze-v1.2-frosted-neutral.candidate.css")' in entrypoint,
        "Candidate entrypoint must import Frosted Neutral layer",
    )

    req('data-glaze-upgrade="v1.2-frosted-neutral"' in reference, "reference does not activate Candidate")
    req("../../css/glaze-v1.2.0-candidate.css" in reference, "reference does not use Candidate entrypoint")
    req("Neutral glass is the material." in reference, "reference does not state the governing rule")
    req("Quick Settings" in reference, "reference must exercise a system-panel control surface")

    req("Neutral glass is the material. Color is an accent." in contract, "Candidate contract governing rule missing")
    req("default material tint from teal, aqua, green, or amber is `0`" in contract, "Candidate contract substrate rule missing")
    req("V1.1 / 1.1.0" in contract, "Candidate contract Stable baseline missing")

    print("GLAZE UI V1.2 Frosted Neutral Candidate validated; V1.1 remains current Stable")


if __name__ == "__main__":
    main()
