#!/usr/bin/env python3
"""Fail-closed source validator for GLAZE UI V1.1 Stable authority."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.1.0"
PRODUCT = "GLAZE UI V1.1"
STABLE_ACTIVATION = 'html[data-glaze-version="1.1"]'
CANDIDATE_ACTIVATION = 'html[data-glaze-version-candidate="1.1"]'


def load(path: str):
    with (ROOT / path).open(encoding="utf-8") as handle:
        return json.load(handle)


def stable_optical(candidate: str) -> str:
    candidate = re.sub(
        r"\A/\*.*?\*/\n",
        "/*\n * GLAZE UI V1.1 — Stable optical refinement layer.\n * Activation: html[data-glaze-version=\\\"1.1\\\"] only.\n * Inherits the GLAZE UI V1.0 structural material baseline without adding\n * nested backdrop blur, semantic-state authority, content sampling, or remote assets.\n */\n",
        candidate,
        count=1,
        flags=re.DOTALL,
    )
    candidate = candidate.replace('@import url("./glaze-v1.0.0.css");\n\n', "", 1)
    return candidate.replace(CANDIDATE_ACTIVATION, STABLE_ACTIVATION)


def stable_appearance(candidate: str) -> str:
    candidate = re.sub(
        r"\A/\*.*?\*/\n",
        "/*\n * GLAZE UI V1.1 — Stable explicit appearance adapter.\n * Maps Light, Dark, and Deep Dark to inherited V1 structural surface/text roles.\n * Protected semantic-state colors remain producer-authoritative and unchanged.\n */\n",
        candidate,
        count=1,
        flags=re.DOTALL,
    )
    return candidate.replace(CANDIDATE_ACTIVATION, STABLE_ACTIVATION)


def main() -> int:
    errors: list[str] = []
    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    require((ROOT / "VERSION").read_text(encoding="utf-8").strip() == VERSION, "VERSION must be 1.1.0")
    lifecycle = load("registry/lifecycle.json")
    require(lifecycle.get("officialProductLabel") == PRODUCT, "lifecycle official product must be GLAZE UI V1.1")
    require(lifecycle.get("currentOfficial") == VERSION, "lifecycle currentOfficial must be 1.1.0")
    require(lifecycle.get("currentStable") == VERSION, "lifecycle currentStable must be 1.1.0")
    release = next((item for item in lifecycle.get("releases", []) if item.get("version") == VERSION), None)
    require(bool(release) and release.get("status") == "stable", "lifecycle must contain Stable 1.1.0 release")
    require(bool(release) and release.get("consumerEligible") is True, "Stable design-system release must be consumer-adoptable")

    for path in (
        "GLAZE_UI_V1_1.md",
        "contracts/v1.1/optical-refinement.json",
        "tokens/glaze-v1.1-atmosphere.json",
        "css/glaze-v1.1.css",
        "css/glaze-v1.1-appearance.css",
        "css/glaze-v1.1.0.css",
        "js/glaze-v1.1.0.mjs",
        "acceptance/v1.1-stable.md",
        "contracts/v1.1/release.json",
    ):
        require((ROOT / path).is_file(), f"missing Stable V1.1 authority artifact: {path}")

    stable_contract = load("contracts/v1.1/optical-refinement.json")
    require(stable_contract.get("product") == PRODUCT and stable_contract.get("version") == VERSION, "Stable optical contract identity mismatch")
    require(stable_contract.get("lifecycle") == "stable", "Stable optical contract lifecycle mismatch")
    boundary = stable_contract.get("releaseBoundary", {})
    require(boundary.get("currentTarget") is True, "Stable optical contract must be current target")
    require(boundary.get("downstreamConsumerConformanceAutomatic") is False, "Stable release must not auto-conform consumers")

    atmosphere = load("tokens/glaze-v1.1-atmosphere.json")
    require(atmosphere.get("product") == PRODUCT and atmosphere.get("version") == VERSION, "Stable atmosphere identity mismatch")
    require(atmosphere.get("lifecycle") == "stable" and atmosphere.get("currentV1Token") is True, "Stable atmosphere lifecycle mismatch")
    require(atmosphere.get("primitives", {}).get("deepTeal") == "#0F6B6F", "Deep Teal primitive drift")
    require(atmosphere.get("primitives", {}).get("softAmber") == "#D9A35F", "Soft Amber primitive drift")
    require(atmosphere.get("semanticPrecedence", {}).get("atmosphereIsLowestPriority") is True, "atmosphere must remain lowest priority")

    stable_css = (ROOT / "css/glaze-v1.1.css").read_text(encoding="utf-8")
    stable_appearance_css = (ROOT / "css/glaze-v1.1-appearance.css").read_text(encoding="utf-8")
    candidate_css = (ROOT / "css/glaze-v1.1-candidate.css").read_text(encoding="utf-8")
    candidate_appearance = (ROOT / "css/glaze-v1.1-appearance.candidate.css").read_text(encoding="utf-8")
    require(stable_css.rstrip() == stable_optical(candidate_css).rstrip(), "Stable optical CSS must be deterministic promotion of human-approved candidate CSS")
    require(stable_appearance_css.rstrip() == stable_appearance(candidate_appearance).rstrip(), "Stable appearance CSS must be deterministic promotion of approved candidate adapter")
    require(CANDIDATE_ACTIVATION not in stable_css and STABLE_ACTIVATION in stable_css, "Stable optical CSS activation namespace mismatch")
    require(CANDIDATE_ACTIVATION not in stable_appearance_css and STABLE_ACTIVATION in stable_appearance_css, "Stable appearance activation namespace mismatch")
    require("backdrop-filter" not in stable_css.lower(), "Stable V1.1 optical layer must not add nested backdrop filtering")
    require("@keyframes" not in stable_css.lower(), "Stable V1.1 optical layer must not add decorative keyframes")
    require("http://" not in stable_css.lower() and "https://" not in stable_css.lower(), "Stable V1.1 optical layer must not depend on remote assets")

    entry = (ROOT / "css/glaze-v1.1.0.css").read_text(encoding="utf-8")
    for marker in ('@import url("./glaze-v1.0.0.css")', '@import url("./glaze-v1.1.css")', '@import url("./glaze-v1.1-appearance.css")'):
        require(marker in entry, f"Stable web entrypoint missing {marker}")
    runtime = (ROOT / "js/glaze-v1.1.0.mjs").read_text(encoding="utf-8")
    require('export * from "./glaze-v1.runtime.mjs"' in runtime, "Stable runtime must preserve V1 runtime export")
    require('export * from "./glaze-v1.system-interactions.mjs"' in runtime, "Stable runtime must preserve V1 system interaction export")

    baseline = load("contracts/regression/visual-baselines-v1.json")
    require(baseline.get("product") == PRODUCT and baseline.get("version") == VERSION, "current visual baseline identity mismatch")
    require(baseline.get("status") == "stable-human-approved-source-pinned", "current visual baseline must be human-approved and source-pinned")
    require(len(baseline.get("cases", {})) == 5, "Stable V1.1 visual baseline must retain five approved cases")

    consumers = load("consumers/registry.json")
    require(consumers.get("officialBaseline") == VERSION and consumers.get("requiredConsumerVersion") == VERSION, "consumer registry must require 1.1.0")
    require(consumers.get("officialProductLabel") == PRODUCT, "consumer registry product label mismatch")
    require(all(item.get("requiredTargetVersion") == VERSION for item in consumers.get("consumers", [])), "every listed consumer must require 1.1.0")
    require(not any(item.get("productionEligible") is True for item in consumers.get("consumers", [])), "Stable design-system promotion must not auto-mark consumers production eligible")

    evidence_schema = load("contracts/glaze.conformance-evidence.schema.json")
    target = evidence_schema.get("properties", {}).get("target", {}).get("properties", {})
    require(target.get("glaze_version", {}).get("const") == VERSION, "conformance evidence schema must target 1.1.0")

    token_manifest = load("tokens/glaze-v1.json")
    require(token_manifest.get("product") == PRODUCT and token_manifest.get("version") == VERSION and token_manifest.get("status") == "stable", "current token manifest mismatch")

    docs = {
        "README.md": (PRODUCT, VERSION, "current Stable"),
        "SPECIFICATIONS.md": (PRODUCT, VERSION, "Stable"),
        "BRANDING.md": (PRODUCT, VERSION, "Stable"),
        "ACCEPTANCE.md": (PRODUCT, VERSION, "Stable"),
        "GLAZE_UI_V1_1.md": (PRODUCT, VERSION, "Stable"),
        "website/index.html": (PRODUCT, "1.1.0", "Current Stable"),
        "website/404.html": (PRODUCT,),
    }
    for path, markers in docs.items():
        text = (ROOT / path).read_text(encoding="utf-8")
        for marker in markers:
            require(marker in text, f"{path} missing current Stable marker {marker!r}")

    require((ROOT / "GLAZE_UI_V1_0.md").is_file(), "historical V1.0 contract must remain available for audit")
    require((ROOT / "contracts/v1.1/optical-refinement.candidate.json").is_file(), "candidate machine contract must remain as audit evidence")
    require((ROOT / "contracts/v1.1/release-candidate.rc.json").is_file(), "release-candidate record must remain as audit evidence")

    if errors:
        print("GLAZE UI V1.1 Stable source validation FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("GLAZE UI V1.1 Stable source authority: PASS")
    print("Boundary: exact-head PR validation, governed merge, post-merge validation, v1.1.0 tag/GitHub Release, and canonical GoreeCloud documentation sync remain release-finalization gates.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
