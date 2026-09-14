#!/usr/bin/env python3
"""Validate preserved GLAZE UI V1.2 Stable historical regression authority.

V1.2 remains a real historical Stable release, but it is no longer the repository's
current lifecycle authority. This validator protects V1.2 release provenance and
entrypoints without asserting that VERSION, currentOfficial, currentStable, consumer
targets, or later qualification plans still equal their V1.2-era values.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.2.0"
PRODUCT = "GLAZE UI V1.2 — Living Frosted"


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []

    def req(ok: bool, message: str) -> None:
        if not ok:
            errors.append(message)

    lifecycle = load("registry/lifecycle.json")
    releases = lifecycle.get("releases", [])
    release = next((item for item in releases if isinstance(item, dict) and item.get("version") == VERSION), None)
    req(isinstance(release, dict), "lifecycle must preserve a V1.2 / 1.2.0 release record")
    if isinstance(release, dict):
        req(release.get("label") == PRODUCT, "historical V1.2 product label drifted")
        req(release.get("status") == "stable", "historical V1.2 release must remain recorded as Stable")
        req(release.get("consumerEligible") is True, "historical V1.2 release must preserve its original consumer-eligible status")
        req(release.get("contract") == "GLAZE_UI_V1_2.md", "historical V1.2 contract pointer drifted")
        req(release.get("acceptance") == "acceptance/v1.2-stable.md", "historical V1.2 acceptance pointer drifted")
        req(release.get("webEntrypoint") == "css/glaze-v1.2.0.css", "historical V1.2 web entrypoint drifted")
        req(release.get("runtimeEntrypoint") == "js/glaze-v1.2.0.mjs", "historical V1.2 runtime entrypoint drifted")

    required = (
        "GLAZE_UI_V1_2.md",
        "GLAZE_UI_V1_2_CANDIDATE.md",
        "css/glaze-v1.2.0.css",
        "css/glaze-v1.2.0-candidate.css",
        "js/glaze-v1.2.0.mjs",
        "acceptance/v1.2-stable.md",
        "GLAZE_UI_V1_1.md",
        "acceptance/v1.1-stable.md",
    )
    for path in required:
        req((ROOT / path).is_file(), f"missing preserved V1.2 authority/audit file: {path}")

    if (ROOT / "css/glaze-v1.2.0.css").is_file():
        css = (ROOT / "css/glaze-v1.2.0.css").read_text(encoding="utf-8")
        req('@import url("./glaze-v1.2.0-candidate.css")' in css, "historical V1.2 Stable CSS wrapper must preserve the promoted Candidate rendering source")

    if (ROOT / "js/glaze-v1.2.0.mjs").is_file():
        runtime = (ROOT / "js/glaze-v1.2.0.mjs").read_text(encoding="utf-8")
        req('export * from "./glaze-v1.1.0.mjs"' in runtime, "historical V1.2 runtime must preserve inherited V1.1 runtime")
        req("glaze-v1.2-living-glaze.candidate.mjs" in runtime, "historical V1.2 runtime must preserve Living Glaze export")
        req("glaze-v1.2-personalization.candidate.mjs" in runtime, "historical V1.2 runtime must preserve Personalization export")

    if (ROOT / "GLAZE_UI_V1_2.md").is_file():
        contract = (ROOT / "GLAZE_UI_V1_2.md").read_text(encoding="utf-8")
        req("V1.2" in contract and "Stable" in contract, "historical V1.2 contract must remain identifiable as V1.2 Stable authority")

    if (ROOT / "acceptance/v1.2-stable.md").is_file():
        acceptance = (ROOT / "acceptance/v1.2-stable.md").read_text(encoding="utf-8")
        req("V1.2" in acceptance and "Stable" in acceptance, "historical V1.2 acceptance record must remain identifiable")
        req("does not" in acceptance.lower() and "V1.3" in acceptance, "historical V1.2 acceptance must preserve the V1.3 deferred-evidence boundary")

    current_version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    req(bool(current_version), "current VERSION authority must remain present")
    req(lifecycle.get("currentStable") == current_version, "current lifecycle Stable authority must remain internally consistent while V1.2 is checked historically")
    req(lifecycle.get("currentOfficial") == current_version, "current lifecycle Official authority must remain internally consistent while V1.2 is checked historically")

    if errors:
        print("GLAZE UI V1.2 historical Stable regression validation FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("GLAZE UI V1.2 historical Stable regression authority: PASS")
    print(f"Preserved historical release: {VERSION}; current lifecycle authority remains {current_version}.")
    print("Boundary: this validator protects V1.2 provenance and does not make V1.2 current again.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
