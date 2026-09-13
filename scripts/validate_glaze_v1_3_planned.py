#!/usr/bin/env python3
"""Validate preserved V1.3 Stable provenance and its V1.3.1 evidence boundary."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STABLE = "1.3.0"
QUALITY = "contracts/v1.3/quality-rules.candidate.json"
RULE_IDS = {f"quality-{i:02d}" for i in range(1, 56)}


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main():
    errors = []

    def req(ok, msg):
        if not ok:
            errors.append(msg)

    for path in [
        "acceptance/v1.3-stable.md",
        "acceptance/v1.3-deferred-qualification.md",
        "GLAZE_UI_V1_3_1_HARDENING.md",
        "contracts/v1.3/deferred-qualification.plan.json",
        "contracts/v1.3/qualification-matrix.json",
        "contracts/v1.3/qualification-evidence.schema.json",
        QUALITY,
        "registry/lifecycle.json",
        "consumers/registry.json",
    ]:
        req((ROOT / path).is_file(), f"missing V1.3/V1.3.1 authority: {path}")

    if errors:
        print("GLAZE UI V1.3 historical release/deferred qualification validation FAILED:")
        for e in errors:
            print(f"- {e}")
        return 1

    lifecycle = load("registry/lifecycle.json")
    release = next((x for x in lifecycle.get("releases", []) if x.get("version") == STABLE), None)
    req(bool(release) and release.get("status") == "stable", "1.3.0 release record must remain Stable")
    req(bool(release) and release.get("consumerEligible") is True, "1.3.0 must remain consumer-eligible as a historical Stable release")
    req(bool(release) and release.get("stableBaseline") == "1.2.0", "V1.3 Stable baseline must remain 1.2.0")
    req(bool(release) and release.get("contract") == "GLAZE_UI_V1_3.md", "V1.3 contract binding drifted")
    req(bool(release) and release.get("webEntrypoint") == "css/glaze-v1.3.0.css", "V1.3 web entrypoint drifted")
    req(bool(release) and release.get("runtimeEntrypoint") == "js/glaze-v1.3.0.mjs", "V1.3 runtime entrypoint drifted")
    req(lifecycle.get("activeCandidate") != "1.3.0-candidate", "V1.3 must not return as an active Candidate after Stable promotion")

    consumers = load("consumers/registry.json")
    req(consumers.get("requiredConsumerVersion") == lifecycle.get("currentStable"), "shared required consumer target must follow the current Stable lifecycle")
    req(not any(item.get("productionEligible") is True for item in consumers.get("consumers", [])), "later design-system promotion must not auto-accept consumers")

    quality = load(QUALITY)
    qrules = quality.get("rules", [])
    req(len(qrules) == 55 and {x.get("id") for x in qrules if isinstance(x, dict)} == RULE_IDS,
        "quality contract must retain exactly quality-01 through quality-55")
    req(quality.get("humanReviewRequired") is True, "historical V1.3 human quality-review requirement must remain recorded")
    req(quality.get("automatedValidationSufficient") is False, "historical V1.3 evidence must not rewrite automation as sufficient human review")

    schema = load("contracts/v1.3/qualification-evidence.schema.json")
    props = schema.get("properties", {})
    req(props.get("schema_version", {}).get("const") == 2, "V1.3 evidence schema_version must remain 2")

    stable_acceptance = (ROOT / "acceptance/v1.3-stable.md").read_text(encoding="utf-8")
    deferred = (ROOT / "acceptance/v1.3-deferred-qualification.md").read_text(encoding="utf-8")
    hardening = (ROOT / "GLAZE_UI_V1_3_1_HARDENING.md").read_text(encoding="utf-8")
    for text, name in [(stable_acceptance, "Stable acceptance"), (deferred, "deferred qualification"), (hardening, "V1.3.1 hardening")]:
        req("V1.3.1" in text, f"{name} must identify V1.3.1 follow-up")
    req("not represented as passed" in stable_acceptance, "V1.3 Stable acceptance must not fabricate deferred passes")
    req("does **not** manufacture" in deferred, "V1.3 deferred qualification must preserve evidence integrity")

    if errors:
        print("GLAZE UI V1.3 historical release/deferred qualification validation FAILED:")
        for e in errors:
            print(f"- {e}")
        return 1

    print("GLAZE UI V1.3 historical release/deferred qualification boundary: PASS")
    print(f"V1.3.0 remains preserved Stable provenance; current shared lifecycle target is {lifecycle.get('currentStable')}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
