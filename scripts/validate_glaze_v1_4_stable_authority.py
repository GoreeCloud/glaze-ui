#!/usr/bin/env python3
"""Validate the canonical GLAZE UI V1.4 Stable release boundary."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"GLAZE UI V1.4 Stable authority: FAIL: {message}")


def main() -> None:
    version = read("VERSION").strip()
    require(version == "1.4.0", f"VERSION must be 1.4.0, got {version!r}")

    lifecycle = json.loads(read("registry/lifecycle.json"))
    require(lifecycle.get("currentOfficial") == "1.4.0", "currentOfficial must be 1.4.0")
    require(lifecycle.get("currentStable") == "1.4.0", "currentStable must be 1.4.0")
    require(lifecycle.get("activeCandidate") is None, "activeCandidate must be null")
    require(lifecycle.get("plannedNext") == "1.4.1-candidate", "plannedNext must be 1.4.1-candidate")

    releases = {release.get("version"): release for release in lifecycle.get("releases", [])}
    release = releases.get("1.4.0")
    require(isinstance(release, dict), "lifecycle must contain release 1.4.0")
    require(release.get("status") == "stable", "release 1.4.0 must be stable")
    require(release.get("consumerEligible") is True, "release 1.4.0 must be consumer eligible")
    require(release.get("stableBaseline") == "1.3.0", "V1.4 stableBaseline must be 1.3.0")
    require(release.get("webEntrypoint") == "css/glaze-v1.4.0.css", "wrong V1.4 web entrypoint")
    require(release.get("runtimeEntrypoint") == "js/glaze-v1.4.0.mjs", "wrong V1.4 runtime entrypoint")
    require(release.get("humanQualificationDeferredTo") == "1.4.1", "human qualification must defer to 1.4.1")

    required_files = [
        "GLAZE_UI_V1_4.md",
        "GLAZE_UI_V1_4_1_HARDENING.md",
        "acceptance/1.4.0.md",
        "acceptance/v1.4-deferred-qualification.md",
        "css/glaze-v1.4.0.css",
        "js/glaze-v1.4.0.mjs",
        "tokens/glaze-v1.4-optical-material.candidate.json",
        "contracts/v1.4/semantic-optical-runtime.candidate.json",
        "contracts/v1.4/accessibility-composition.candidate.json",
        "contracts/v1.4/browser-capabilities.candidate.json",
    ]
    for path in required_files:
        require((ROOT / path).is_file(), f"missing required release file: {path}")

    contract = read("GLAZE_UI_V1_4.md")
    require("**Lifecycle:** Official Stable" in contract, "V1.4 contract must declare Official Stable")
    require("V1.4.1" in contract, "V1.4 contract must name V1.4.1 deferred qualification")
    require("remain explicitly deferred/unverified" in contract, "V1.4 contract must preserve deferred evidence truth")

    acceptance = read("acceptance/1.4.0.md")
    require("Stable Acceptance Record" in acceptance, "acceptance record heading missing")
    require("None are represented as passed by V1.4.0" in acceptance, "acceptance record must reject false human-pass claims")

    deferred = read("acceptance/v1.4-deferred-qualification.md")
    require("Deferral is not acceptance" in deferred, "deferred record must state truth boundary")
    require("deferred / unverified" in deferred, "deferred record must preserve unverified state")

    css = read("css/glaze-v1.4.0.css")
    require('official Stable web entrypoint' in css, "Stable CSS marker missing")
    require('@import url("./glaze-v1.3.0.css");' in css, "Stable CSS must inherit V1.3")
    require('@import url("./glaze-v1.4-optical-runtime.candidate.css");' in css, "Stable CSS must include V1.4 optical source")

    runtime = read("js/glaze-v1.4.0.mjs")
    require('export * from "./glaze-v1.3.0.mjs";' in runtime, "Stable runtime must inherit V1.3")
    require("glazeV14Stable" in runtime, "Stable runtime metadata missing")
    require("deferredHumanEvidenceIsPassed: false" in runtime, "Stable runtime must not claim deferred human evidence passed")

    v13 = releases.get("1.3.0")
    require(isinstance(v13, dict) and v13.get("status") == "stable", "V1.3 must remain a historical Stable rollback target")

    print("GLAZE UI V1.4 Stable authority: PASS")


if __name__ == "__main__":
    main()
