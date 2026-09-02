#!/usr/bin/env python3
"""Fail closed when canonical Glaze UI release-state authorities drift."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def req(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Glaze UI release-state validation failed: {message}")


def text(path: str) -> str:
    target = ROOT / path
    req(target.is_file(), f"missing required file: {path}")
    return target.read_text(encoding="utf-8")


def main() -> None:
    version = text("VERSION").strip()
    req(re.fullmatch(r"\d+\.\d+\.\d+", version) is not None, "VERSION must be semantic")
    req(version == "2.2.0", "current Stable VERSION must be 2.2.0")

    lifecycle = json.loads(text("registry/lifecycle.json"))
    req(lifecycle.get("currentStable") == version, "lifecycle currentStable differs from VERSION")
    req(lifecycle.get("activeCandidate") is None, "Stable 2.2 release state must not have an active Candidate")
    releases = lifecycle.get("releases", [])
    req(isinstance(releases, list), "lifecycle releases must be an array")

    stable = [r for r in releases if isinstance(r, dict) and r.get("version") == version]
    req(len(stable) == 1 and stable[0].get("status") == "stable" and stable[0].get("consumerEligible") is True, "2.2.0 Stable release record missing")
    req(stable[0].get("promotedFromCandidate") == "2.2.0-candidate.1", "2.2 Stable promotion-source Candidate missing")
    req(stable[0].get("acceptance") == "acceptance/2.2-stable.md", "2.2 Stable acceptance path missing")
    req(stable[0].get("rollbackVersion") == "2.1.0", "2.2 rollback must be 2.1.0")

    candidate = [r for r in releases if isinstance(r, dict) and r.get("version") == "2.2.0-candidate.1"]
    req(len(candidate) == 1 and candidate[0].get("status") == "historical" and candidate[0].get("consumerEligible") is False, "2.2 Candidate must be historical and non-consumer-eligible")
    req(candidate[0].get("promotedTo") == version, "2.2 Candidate must point to promoted Stable version")

    previous = [r for r in releases if isinstance(r, dict) and r.get("version") == "2.1.0"]
    req(len(previous) == 1 and previous[0].get("status") == "historical", "2.1.0 must be retained as historical Stable")
    req(previous[0].get("supersededBy") == version, "2.1.0 must identify 2.2.0 as successor")

    for path in ("GLAZE_UI_2_2_STABLE.md", "acceptance/2.2-stable.md", "css/glaze-2.2.0.css", "js/glaze-2.2.0.mjs"):
        req((ROOT / path).is_file(), f"2.2 Stable artifact missing: {path}")

    registry = json.loads(text("consumers/registry.json"))
    req(registry.get("stableBaseline") == version and registry.get("requiredConsumerVersion") == version, "consumer mandatory Stable target differs from VERSION")
    req("2.1.0" in registry.get("historicalStableVersions", []), "2.1.0 must be historical consumer baseline")
    for consumer in registry.get("consumers", []):
        req(consumer.get("requiredTargetVersion") == version, f"{consumer.get('repository')} required target must be 2.2.0")
        req(consumer.get("productionEligible") is False, "design-system Stable promotion must not auto-promote downstream consumers")

    enforcement = json.loads(text("tokens/enforcement.json"))
    req(enforcement.get("meta", {}).get("currentStable") == version, "enforcement currentStable differs from VERSION")

    print("Glaze UI 2.2.0 canonical release state validated; downstream consumers remain separately gated")


if __name__ == "__main__":
    main()
