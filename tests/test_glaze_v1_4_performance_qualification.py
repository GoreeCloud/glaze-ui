#!/usr/bin/env python3
"""Regression tests for V1.4 performance-qualification evidence evaluation."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from evaluate_glaze_v1_4_performance_qualification import evaluate

SOURCE = "1" * 40
TREE = "2" * 40


def record() -> dict:
    return {
        "schemaVersion": "glaze.v1.4.performance-qualification-evidence.candidate.v1",
        "candidateVersion": "1.4.0-candidate",
        "sourceRevision": SOURCE,
        "sourceTreeRevision": TREE,
        "platformFamily": "web",
        "environment": {
            "runtime": "Chromium candidate harness",
            "renderer": "Blink",
            "deviceClass": "reference desktop",
        },
        "measuredAt": "2026-09-12T23:30:00.000Z",
        "metrics": [
            {
                "name": "runtime_init_ms",
                "unit": "ms",
                "measured": 8.5,
                "budget": 10.0,
                "sampleCount": 50,
                "accepted": True,
            },
            {
                "name": "memory_peak_mib",
                "unit": "MiB",
                "measured": 18.0,
                "budget": 24.0,
                "sampleCount": 50,
                "accepted": True,
            },
        ],
        "evidenceRefs": ["artifact:performance-run:example"],
        "reviewer": {
            "authority": "Glaze performance qualification reviewer",
            "disposition": "accepted",
            "rationale": "Bounded test fixture demonstrating evaluator semantics.",
        },
        "result": "passed",
        "lifecycleAcceptance": False,
    }


def check_raises(fn, message: str) -> None:
    try:
        fn()
    except ValueError:
        return
    raise AssertionError(message)


def main() -> None:
    accepted = evaluate(record(), expected_source_revision=SOURCE, expected_source_tree_revision=TREE)
    assert accepted["acceptedForPerformanceQualification"] is True, "passing measured evidence can qualify performance without granting lifecycle acceptance"
    assert accepted["acceptedForLifecycleGate"] is False, "performance evidence must never self-promote the lifecycle gate"
    assert accepted["evaluatorDisposition"] == "accepted"

    over_budget = record()
    over_budget["metrics"][0]["measured"] = 11.0
    over_budget["metrics"][0]["accepted"] = False
    over_budget["result"] = "failed"
    result = evaluate(over_budget, expected_source_revision=SOURCE, expected_source_tree_revision=TREE)
    assert result["acceptedForPerformanceQualification"] is False
    assert "metric_budget_exceeded" in result["reasonCodes"]

    contradictory = record()
    contradictory["metrics"][0]["measured"] = 11.0
    check_raises(
        lambda: evaluate(contradictory),
        "accepted flag cannot contradict the measured value and budget",
    )

    duplicate = record()
    duplicate["metrics"].append(deepcopy(duplicate["metrics"][0]))
    check_raises(lambda: evaluate(duplicate), "duplicate metrics fail closed")

    source_mismatch = evaluate(
        record(),
        expected_source_revision="3" * 40,
        expected_source_tree_revision=TREE,
    )
    assert source_mismatch["acceptedForPerformanceQualification"] is False, "exact source mismatch blocks otherwise passing evidence"
    assert "source_revision_mismatch" in source_mismatch["reasonCodes"]

    pending_review = record()
    pending_review["reviewer"]["disposition"] = "pending"
    pending_review["result"] = "blocked"
    result = evaluate(pending_review, expected_source_revision=SOURCE, expected_source_tree_revision=TREE)
    assert result["acceptedForPerformanceQualification"] is False
    assert "review_not_accepted" in result["reasonCodes"]

    missing_evidence = record()
    missing_evidence["evidenceRefs"] = []
    result = evaluate(missing_evidence)
    assert result["acceptedForPerformanceQualification"] is False
    assert "measurement_evidence_missing" in result["reasonCodes"]

    extra = record()
    extra["stable"] = True
    check_raises(lambda: evaluate(extra), "unknown root fields must fail closed")

    promotion = record()
    promotion["lifecycleAcceptance"] = True
    check_raises(lambda: evaluate(promotion), "performance evidence cannot grant lifecycle acceptance")

    print("Glaze V1.4 performance qualification regression tests passed.")


if __name__ == "__main__":
    main()
