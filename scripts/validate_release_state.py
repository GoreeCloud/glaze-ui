#!/usr/bin/env python3
"""Fail closed when the canonical Glaze UI release state drifts.

The current Stable release must always agree with VERSION. A future Candidate may
coexist with Stable only when it is explicitly registered, non-consumer-eligible,
and does not alter the mandatory Stable consumer target.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def req(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Glaze UI release-state validation failed: {message}")


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> None:
    version = text("VERSION").strip()
    req(version == "2.1.0", "current Stable VERSION must remain 2.1.0 during the 2.2 Candidate line")
    req(re.fullmatch(r"\d+\.\d+\.\d+", version) is not None, "VERSION must be semantic")

    lifecycle = json.loads(text("registry/lifecycle.json"))
    req(lifecycle.get("currentStable") == version, "lifecycle currentStable differs from VERSION")

    releases = lifecycle.get("releases", [])
    req(isinstance(releases, list), "lifecycle releases must be an array")

    stable = [r for r in releases if isinstance(r, dict) and r.get("version") == version]
    req(
        len(stable) == 1
        and stable[0].get("status") == "stable"
        and stable[0].get("consumerEligible") is True,
        "2.1 Stable release record missing",
    )
    req(stable[0].get("promotedFromCandidate") == "2.1.0-candidate.1", "promotion-source Candidate missing")

    old = [r for r in releases if isinstance(r, dict) and r.get("version") == "2.0.0"]
    req(len(old) == 1 and old[0].get("status") == "historical", "2.0 must be historical")

    active_candidate = lifecycle.get("activeCandidate")
    if active_candidate is not None:
        req(
            re.fullmatch(r"\d+\.\d+\.\d+-candidate\.\d+", active_candidate) is not None,
            "activeCandidate must use the x.y.z-candidate.n form",
        )
        candidates = [
            r for r in releases if isinstance(r, dict) and r.get("version") == active_candidate
        ]
        req(len(candidates) == 1, "active Candidate release record missing or duplicated")
        candidate = candidates[0]
        req(candidate.get("status") == "candidate", "active Candidate release must have Candidate status")
        req(candidate.get("consumerEligible") is False, "active Candidate must not be consumer eligible")
        req(candidate.get("version") != version, "active Candidate must not replace VERSION before promotion")
        contract = candidate.get("contract")
        req(isinstance(contract, str) and bool(contract.strip()), "active Candidate contract path missing")
        req((ROOT / contract).is_file(), "active Candidate contract file missing")
        acceptance_path = candidate.get("acceptance")
        if acceptance_path is not None:
            req(
                isinstance(acceptance_path, str)
                and bool(acceptance_path.strip())
                and (ROOT / acceptance_path).is_file(),
                "active Candidate acceptance path is invalid",
            )

    req((ROOT / "GLAZE_UI_2_1_STABLE.md").is_file() and (ROOT / "acceptance/2.1-stable.md").is_file(), "2.1 Stable contract/acceptance missing")
    req((ROOT / "css/glaze-2.1.0.css").is_file() and (ROOT / "js/glaze-2.1.0.mjs").is_file(), "versioned Stable entrypoints missing")

    stable_doc = text("GLAZE_UI_2_1_STABLE.md")
    for marker in (
        "Lifecycle status:** Stable",
        "Stable semantic version:** 2.1.0",
        "Previous Stable implementation baseline:** Glaze UI 2.0.0",
        "Content is solid. Interaction is glazed.",
        "Approve Visual Excellence",
        "No downstream application is promoted by declaration",
    ):
        req(marker in stable_doc, f"2.1 Stable contract missing {marker}")

    acceptance = text("acceptance/2.1-stable.md")
    for marker in (
        "Approve Visual Excellence",
        "5b46903c18660ae78e7f1aaea39a93136efacda7",
        "a21601691dc412baa6a889533d6fa5b3a7996dc2",
        "48 dp",
        "56 dp",
    ):
        req(marker in acceptance, f"2.1 Stable acceptance missing {marker}")

    registry = json.loads(text("consumers/registry.json"))
    req(
        registry.get("stableBaseline") == version
        and registry.get("requiredConsumerVersion") == version,
        "consumer mandatory Stable target differs from VERSION",
    )
    req("2.0.0" in registry.get("historicalStableVersions", []), "2.0 must be historical consumer baseline")
    for consumer in registry.get("consumers", []):
        req(consumer.get("requiredTargetVersion") == version, f"{consumer.get('repository')} required target must remain 2.1.0")
        req(consumer.get("productionEligible") is False, "design-system lifecycle changes must not auto-promote downstream consumers")

    enforcement = json.loads(text("tokens/enforcement.json"))
    req(enforcement.get("meta", {}).get("currentStable") == version, "enforcement currentStable differs from VERSION")

    if active_candidate is None:
        print("Glaze UI 2.1.0 Stable release state validated; no active Candidate; downstream consumers remain separately gated")
    else:
        print(
            f"Glaze UI 2.1.0 Stable release state validated with active {active_candidate}; "
            "Candidate is non-consumer-eligible and downstream consumers remain separately gated"
        )


if __name__ == "__main__":
    main()
