#!/usr/bin/env python3
"""Validate preserved Glaze UI 2.1.0 historical regression authority.

Glaze UI 2.1.0 is no longer the current Stable target after 2.2.0 promotion,
but its release artifacts, acceptance records, entrypoints, visual baseline and
rollback value must remain intact and testable.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def req(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Glaze UI 2.1 historical validation failed: {message}")


def main() -> None:
    req((ROOT / "VERSION").read_text(encoding="utf-8").strip() == "2.2.0", "current Stable must be 2.2.0")

    lifecycle = json.loads((ROOT / "registry/lifecycle.json").read_text(encoding="utf-8"))
    req(lifecycle.get("currentStable") == "2.2.0", "lifecycle currentStable must be 2.2.0")
    releases = lifecycle.get("releases", [])
    prior = [r for r in releases if isinstance(r, dict) and r.get("version") == "2.1.0"]
    current = [r for r in releases if isinstance(r, dict) and r.get("version") == "2.2.0"]
    req(len(prior) == 1, "2.1.0 release record must be preserved")
    req(prior[0].get("status") == "historical", "2.1.0 must be historical after 2.2 promotion")
    req(prior[0].get("consumerEligible") is False, "2.1.0 must not satisfy current consumer conformance")
    req(prior[0].get("supersededBy") == "2.2.0", "2.1.0 must identify 2.2.0 as successor")
    req(len(current) == 1 and current[0].get("rollbackVersion") == "2.1.0", "2.2.0 must preserve 2.1.0 as rollback")

    for path in (
        "GLAZE_UI_2_1_STABLE.md",
        "acceptance/2.1-stable.md",
        "css/glaze-2.1.0.css",
        "js/glaze-2.1.0.mjs",
        "contracts/regression/visual-baselines.json",
        "reference/native/android/buildable",
        "scripts/validate_glaze_2_1_rendered.py",
        "scripts/validate_glaze_2_1_expanded_rendered.py",
        "scripts/validate_glaze_2_1_resilience_rendered.py",
        "scripts/validate_glaze_2_1_android_runtime.py",
        "tests/glaze-2.1-runtime.test.mjs",
    ):
        req((ROOT / path).exists(), f"preserved 2.1 artifact missing: {path}")

    visual = json.loads((ROOT / "contracts/regression/visual-baselines.json").read_text(encoding="utf-8"))
    req(visual.get("baselineRevision") == "5b46903c18660ae78e7f1aaea39a93136efacda7", "2.1 approved visual baseline source drifted")
    req(len(visual.get("cases", [])) == 6, "2.1 visual regression case count must remain six")

    stable_doc = (ROOT / "GLAZE_UI_2_1_STABLE.md").read_text(encoding="utf-8")
    acceptance = (ROOT / "acceptance/2.1-stable.md").read_text(encoding="utf-8")
    req("2.1.0" in stable_doc and "Stable" in stable_doc, "2.1 Stable contract identity drifted")
    req("2.1.0" in acceptance, "2.1 acceptance identity drifted")

    print("Glaze UI 2.1.0 historical release authority validated; retained runtime/rendered/native regression gates remain mandatory")


if __name__ == "__main__":
    main()
