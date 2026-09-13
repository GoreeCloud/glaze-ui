#!/usr/bin/env python3
"""Validate the preserved GLAZE UI V1.2 historical Stable source authority.

V1.2 remains a real Stable release and audit/rollback artifact after later Stable
releases become current. This validator therefore protects the immutable V1.2
release record and source wrappers without requiring V1.2 to remain the global
current version or consumer target.
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
    release = next((item for item in lifecycle.get("releases", []) if item.get("version") == VERSION), None)
    req(bool(release) and release.get("status") == "stable", "lifecycle must retain Stable 1.2.0")
    req(bool(release) and release.get("consumerEligible") is True, "historical V1.2 Stable must remain consumer-adoptable")
    req(bool(release) and release.get("stableBaseline") == "1.1.0", "V1.2 Stable baseline must remain V1.1")
    req(bool(release) and release.get("contract") == "GLAZE_UI_V1_2.md", "V1.2 Stable contract binding drifted")
    req(bool(release) and release.get("webEntrypoint") == "css/glaze-v1.2.0.css", "V1.2 Stable web entrypoint drifted")
    req(bool(release) and release.get("runtimeEntrypoint") == "js/glaze-v1.2.0.mjs", "V1.2 Stable runtime entrypoint drifted")

    current = lifecycle.get("currentStable")
    req(isinstance(current, str) and current not in {"1.2.0-candidate", "1.1.1-rc.1"}, "global lifecycle must not regress to a V1.2 Candidate/patch RC")
    req(lifecycle.get("activeCandidate") != "1.2.0-candidate", "V1.2 must not reappear as an active Candidate after Stable promotion")

    required = (
        "GLAZE_UI_V1_2.md",
        "GLAZE_UI_V1_2_CANDIDATE.md",
        "css/glaze-v1.2.0.css",
        "css/glaze-v1.2.0-candidate.css",
        "js/glaze-v1.2.0.mjs",
        "acceptance/v1.2-stable.md",
        "tokens/glaze-v1.json",
        "GLAZE_UI_V1_1.md",
        "acceptance/v1.1-stable.md",
    )
    for path in required:
        req((ROOT / path).is_file(), f"missing V1.2 Stable authority/audit file: {path}")

    css = (ROOT / "css/glaze-v1.2.0.css").read_text(encoding="utf-8")
    req('@import url("./glaze-v1.2.0-candidate.css")' in css, "V1.2 Stable CSS wrapper must freeze the promoted V1.2 rendering source")
    runtime = (ROOT / "js/glaze-v1.2.0.mjs").read_text(encoding="utf-8")
    req('export * from "./glaze-v1.1.0.mjs"' in runtime, "V1.2 Stable runtime must preserve inherited V1 runtime")
    req("glaze-v1.2-living-glaze.candidate.mjs" in runtime, "V1.2 Stable runtime must export Living Glaze")
    req("glaze-v1.2-personalization.candidate.mjs" in runtime, "V1.2 Stable runtime must export Personalization")

    manifest = load("tokens/glaze-v1.json")
    req(manifest.get("version") == VERSION and manifest.get("status") == "stable", "V1.2 token snapshot must remain a Stable 1.2.0 artifact")

    acceptance = (ROOT / "acceptance/v1.2-stable.md").read_text(encoding="utf-8")
    req("does not" in acceptance.lower() and "V1.3" in acceptance, "V1.2 acceptance must preserve its original deferred-evidence boundary")

    consumers = load("consumers/registry.json")
    required_consumer = consumers.get("requiredConsumerVersion")
    req(required_consumer != "1.2.0-candidate", "consumer authority must never regress to V1.2 Candidate")
    req(not any(item.get("productionEligible") is True for item in consumers.get("consumers", [])), "shared design-system lifecycle changes must not auto-accept consumers")

    if errors:
        print("GLAZE UI V1.2 historical Stable source validation FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("GLAZE UI V1.2 historical Stable source authority: PASS")
    print(f"Boundary: V1.2 remains preserved while current lifecycle authority is {current}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
