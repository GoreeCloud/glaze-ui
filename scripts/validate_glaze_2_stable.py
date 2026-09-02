#!/usr/bin/env python3
"""Validate Glaze UI 2.1.0 Stable and preserved 2.0/2.1 Candidate provenance.

A separately governed future Candidate may coexist with 2.1.0 Stable. That
Candidate must not alter VERSION, currentStable, the 2.1 Stable release record,
or the preserved promotion provenance validated here.
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def req(condition, message):
    if not condition:
        raise SystemExit(f"Glaze UI 2.1 Stable validation failed: {message}")


def txt(path):
    return (ROOT / path).read_text(encoding="utf-8")


def main():
    req(txt("VERSION").strip() == "2.1.0", "VERSION")
    for path in (
        "GLAZE_UI_2_1_STABLE.md",
        "GLAZE_UI_2_STABLE.md",
        "GLAZE_UI_2_1_CANDIDATE.md",
        "acceptance/2.1-candidate.md",
        "acceptance/2.1-stable.md",
        "css/glaze-2.1.0.css",
        "js/glaze-2.1.0.mjs",
        "css/glaze-2.1.reference.css",
        "css/glaze-2.1.visual-excellence.css",
        "js/glaze-2.1.candidate.mjs",
    ):
        req((ROOT / path).is_file(), f"missing {path}")

    req(
        '@import url("./glaze-2.1.reference.css");' in txt("css/glaze-2.1.0.css"),
        "Stable CSS must bind 2.1 reference source",
    )
    req(
        '@import url("./glaze-2.1.visual-excellence.css");' in txt("css/glaze-2.1.0.css"),
        "Stable CSS must bind approved Visual Excellence layer",
    )
    req(
        'export * from "./glaze-2.1.candidate.mjs";' in txt("js/glaze-2.1.0.mjs"),
        "Stable runtime must bind preserved Candidate implementation",
    )

    doc = txt("GLAZE_UI_2_1_STABLE.md")
    for marker in (
        "Stable semantic version:** 2.1.0",
        "Previous Stable implementation baseline:** Glaze UI 2.0.0",
        "Approve Visual Excellence",
        "Glaze Motion remains separately governed and Experimental",
    ):
        req(marker in doc, f"missing {marker}")

    candidate = txt("acceptance/2.1-candidate.md")
    req(
        "Approve Visual Excellence" in candidate
        and "a21601691dc412baa6a889533d6fa5b3a7996dc2" in candidate,
        "approved Candidate provenance missing",
    )

    lifecycle = json.loads(txt("registry/lifecycle.json"))
    req(lifecycle.get("currentStable") == "2.1.0", "currentStable must remain 2.1.0")

    releases = lifecycle.get("releases", [])
    stable = [
        record
        for record in releases
        if isinstance(record, dict) and record.get("version") == "2.1.0"
    ]
    req(len(stable) == 1, "2.1 Stable release record missing or duplicated")
    req(stable[0].get("status") == "stable", "2.1 release record must remain Stable")
    req(stable[0].get("consumerEligible") is True, "2.1 Stable must remain consumer eligible")
    req(
        stable[0].get("promotedFromCandidate") == "2.1.0-candidate.1",
        "2.1 promotion provenance changed",
    )
    req(
        stable[0].get("acceptance") == "acceptance/2.1-stable.md",
        "2.1 Stable acceptance binding changed",
    )

    active_candidate = lifecycle.get("activeCandidate")
    if active_candidate is not None:
        req(
            re.fullmatch(r"\d+\.\d+\.\d+-candidate\.\d+", active_candidate) is not None,
            "future activeCandidate has invalid lifecycle version",
        )
        future = [
            record
            for record in releases
            if isinstance(record, dict) and record.get("version") == active_candidate
        ]
        req(len(future) == 1, "future Candidate release record missing or duplicated")
        req(future[0].get("status") == "candidate", "future activeCandidate must remain Candidate")
        req(future[0].get("consumerEligible") is False, "future Candidate must not be consumer eligible")
        req(active_candidate != "2.1.0", "future Candidate must not replace the Stable VERSION")

    print("Glaze UI 2.1.0 Stable contract and preserved promotion provenance validated")


if __name__ == "__main__":
    main()
