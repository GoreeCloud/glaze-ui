#!/usr/bin/env python3
"""Regression tests for V1.4 performance-qualification evidence evaluation."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from evaluate_glaze_v1_4_performance_qualification import evaluate

SOURCE = "1" * 40
TREE = "2" * 40
EVALUATED_AT = datetime(2026, 9, 12, 23, 31, tzinfo=timezone.utc)
MAX_MEASUREMENT_AGE_MS = 5 * 60 * 1000


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


def evaluate_bound(
    payload: dict,
    *,
    source: str = SOURCE,
    tree: str = TREE,
    max_age_ms: int = MAX_MEASUREMENT_AGE_MS,
) -> dict:
    return evaluate(
        payload,
        expected_source_revision=source,
        expected_source_tree_revision=tree,
        max_measurement_age_ms=max_age_ms,
        evaluated_at=EVALUATED_AT,
    )


def check_raises(fn, message: str) -> None:
    try:
        fn()
    except ValueError:
        return
    raise AssertionError(message)


def main() -> None:
    accepted = evaluate_bound(record())
    assert accepted["acceptedForPerformanceQualification"] is True, "passing measured evidence can qualify performance without granting lifecycle acceptance"
    assert accepted["acceptedForLifecycleGate"] is False, "performance evidence must never self-promote the lifecycle gate"
    assert accepted["evaluatorDisposition"] == "accepted"

    unbound = evaluate(record(), evaluated_at=EVALUATED_AT)
    assert unbound["acceptedForPerformanceQualification"] is False, "performance qualification must require exact source, tree, and measurement-age expectations"
    assert "source_revision_expectation_missing" in unbound["reasonCodes"]
    assert "source_tree_revision_expectation_missing" in unbound["reasonCodes"]
    assert "measurement_age_expectation_missing" in unbound["reasonCodes"]

    over_budget = record()
    over_budget["metrics"][0]["measured"] = 11.0
    over_budget["metrics"][0]["accepted"] = False
    over_budget["result"] = "failed"
    result = evaluate_bound(over_budget)
    assert result["acceptedForPerformanceQualification"] is False
    assert "metric_budget_exceeded" in result["reasonCodes"]

    contradictory = record()
    contradictory["metrics"][0]["measured"] = 11.0
    check_raises(
        lambda: evaluate_bound(contradictory),
        "accepted flag cannot contradict the measured value and budget",
    )

    duplicate = record()
    duplicate["metrics"].append(deepcopy(duplicate["metrics"][0]))
    check_raises(lambda: evaluate_bound(duplicate), "duplicate metrics fail closed")

    source_mismatch = evaluate_bound(record(), source="3" * 40)
    assert source_mismatch["acceptedForPerformanceQualification"] is False, "exact source mismatch blocks otherwise passing evidence"
    assert "source_revision_mismatch" in source_mismatch["reasonCodes"]

    tree_mismatch = evaluate_bound(record(), tree="4" * 40)
    assert tree_mismatch["acceptedForPerformanceQualification"] is False, "exact source-tree mismatch blocks otherwise passing evidence"
    assert "source_tree_revision_mismatch" in tree_mismatch["reasonCodes"]

    future_measurement = record()
    future_measurement["measuredAt"] = "2026-09-12T23:31:00.001Z"
    check_raises(
        lambda: evaluate_bound(future_measurement),
        "future-dated performance measurements must fail closed",
    )

    stale_measurement = record()
    stale_measurement["measuredAt"] = "2026-09-12T23:20:00.000Z"
    result = evaluate_bound(stale_measurement)
    assert result["acceptedForPerformanceQualification"] is False, "caller-selected measurement freshness must block stale performance evidence"
    assert "measurement_evidence_stale" in result["reasonCodes"]

    check_raises(
        lambda: evaluate_bound(record(), max_age_ms=0),
        "measurement freshness policy must be a positive integer",
    )

    pending_review = record()
    pending_review["reviewer"]["disposition"] = "pending"
    pending_review["result"] = "blocked"
    result = evaluate_bound(pending_review)
    assert result["acceptedForPerformanceQualification"] is False
    assert "review_not_accepted" in result["reasonCodes"]

    missing_evidence = record()
    missing_evidence["evidenceRefs"] = []
    result = evaluate_bound(missing_evidence)
    assert result["acceptedForPerformanceQualification"] is False
    assert "measurement_evidence_missing" in result["reasonCodes"]

    extra = record()
    extra["stable"] = True
    check_raises(lambda: evaluate_bound(extra), "unknown root fields must fail closed")

    promotion = record()
    promotion["lifecycleAcceptance"] = True
    check_raises(lambda: evaluate_bound(promotion), "performance evidence cannot grant lifecycle acceptance")

    print("Glaze V1.4 performance qualification regression tests passed.")


if __name__ == "__main__":
    main()