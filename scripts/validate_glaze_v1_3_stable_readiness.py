#!/usr/bin/env python3
"""Validate preserved V1.3 Stable/readiness provenance without claiming it is current."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STABLE = "1.3.0"


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main():
    errors = []

    def req(ok, msg):
        if not ok:
            errors.append(msg)

    required = [
        "contracts/v1.3/stable-readiness.plan.json",
        "js/glaze-v1.3-stable-readiness.candidate.mjs",
        "scripts/evaluate_glaze_v1_3_stable_readiness.mjs",
        "tests/glaze-v1.3-stable-readiness.test.mjs",
        "acceptance/v1.3-stable.md",
        "acceptance/v1.3-deferred-qualification.md",
        "GLAZE_UI_V1_3_1_HARDENING.md",
        "registry/lifecycle.json",
        "css/glaze-v1.3.0.css",
        "js/glaze-v1.3.0.mjs",
    ]
    for path in required:
        req((ROOT / path).is_file(), f"missing V1.3 Stable/readiness artifact: {path}")

    if errors:
        print("GLAZE UI V1.3 historical Stable/readiness validation FAILED:")
        for e in errors:
            print(f"- {e}")
        return 1

    lifecycle = load("registry/lifecycle.json")
    release = next((x for x in lifecycle.get("releases", []) if x.get("version") == STABLE), None)
    req(bool(release) and release.get("status") == "stable", "1.3.0 release record must remain Stable")
    req(bool(release) and release.get("consumerEligible") is True, "1.3.0 historical record must preserve consumer eligibility")
    req(bool(release) and release.get("acceptance") == "acceptance/v1.3-stable.md", "V1.3 Stable acceptance authority mismatch")
    req(bool(release) and release.get("webEntrypoint") == "css/glaze-v1.3.0.css", "V1.3 web entrypoint drift")
    req(bool(release) and release.get("runtimeEntrypoint") == "js/glaze-v1.3.0.mjs", "V1.3 runtime entrypoint drift")

    runtime = (ROOT / "js/glaze-v1.3-stable-readiness.candidate.mjs").read_text()
    for symbol in ["evaluateStableReadiness", "STABLE_CLEANUP_WORKSTREAM", "stableReadinessCandidate"]:
        req(symbol in runtime, f"historical Stable-readiness runtime missing API: {symbol}")
    for token in ["fetch(", "XMLHttpRequest", "sendBeacon", "WebSocket(", "localStorage", "sessionStorage", "indexedDB", "child_process", "node:fs"]:
        req(token not in runtime, f"Stable-readiness runtime contains forbidden side-effect primitive: {token}")

    acceptance = (ROOT / "acceptance/v1.3-stable.md").read_text()
    deferred = (ROOT / "acceptance/v1.3-deferred-qualification.md").read_text()
    hardening = (ROOT / "GLAZE_UI_V1_3_1_HARDENING.md").read_text()
    req("Official Stable release" in acceptance, "V1.3 Stable acceptance must remain recorded")
    req("V1.3.1" in acceptance and "V1.3.1" in deferred and "V1.3.1" in hardening, "V1.3.1 follow-up provenance must remain visible")
    req(
        "not represented as passed" in acceptance or "not rewritten as a pass" in acceptance,
        "V1.3 evidence boundary must reject fabricated readiness",
    )

    if errors:
        print("GLAZE UI V1.3 historical Stable/readiness validation FAILED:")
        for e in errors:
            print(f"- {e}")
        return 1

    print("GLAZE UI V1.3 historical Stable/readiness provenance: PASS")
    print("1.3.0 remains a preserved Stable rollback record; this validator does not claim it is the current release.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
