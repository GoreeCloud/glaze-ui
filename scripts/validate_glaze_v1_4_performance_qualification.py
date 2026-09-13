#!/usr/bin/env python3
"""Validate the V1.4 performance-qualification evidence contract boundary."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "contracts" / "v1.4" / "performance-qualification-evidence.schema.candidate.json"
EVALUATOR = ROOT / "scripts" / "evaluate_glaze_v1_4_performance_qualification.py"
TEST = ROOT / "tests" / "test_glaze_v1_4_performance_qualification.py"


def main() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    assert schema["$id"] == "urn:goreecloud:glaze-ui:v1.4:performance-qualification-evidence:candidate:v1"
    assert schema["additionalProperties"] is False
    assert schema["properties"]["schemaVersion"]["const"] == "glaze.v1.4.performance-qualification-evidence.candidate.v1"
    assert schema["properties"]["candidateVersion"]["const"] == "1.4.0-candidate"
    assert schema["properties"]["lifecycleAcceptance"]["const"] is False
    assert schema["properties"]["metrics"]["minItems"] == 1
    assert schema["properties"]["metrics"]["maxItems"] == 32
    assert schema["properties"]["evidenceRefs"]["maxItems"] == 50
    assert set(schema["properties"]["reviewer"]["properties"]["disposition"]["enum"]) == {"pending", "accepted", "rejected"}

    evaluator = EVALUATOR.read_text(encoding="utf-8")
    for token in (
        "acceptedForPerformanceQualification",
        '"acceptedForLifecycleGate": False',
        "metric_budget_exceeded",
        "source_revision_mismatch",
        "source_tree_revision_mismatch",
        "source_revision_expectation_missing",
        "source_tree_revision_expectation_missing",
        "measurement_age_expectation_missing",
        "measurement_evidence_stale",
        "max_measurement_age_ms",
        "measuredAt cannot be future-dated",
        "measurement_evidence_missing",
        "review_not_accepted",
    ):
        assert token in evaluator, f"performance evaluator missing invariant: {token}"

    test_text = TEST.read_text(encoding="utf-8")
    for token in (
        "passing measured evidence can qualify performance without granting lifecycle acceptance",
        "performance qualification must require exact source, tree, and measurement-age expectations",
        "accepted flag cannot contradict the measured value and budget",
        "duplicate metrics fail closed",
        "exact source mismatch blocks otherwise passing evidence",
        "exact source-tree mismatch blocks otherwise passing evidence",
        "future-dated performance measurements must fail closed",
        "caller-selected measurement freshness must block stale performance evidence",
        "measurement freshness policy must be a positive integer",
    ):
        assert token in test_text, f"performance tests missing invariant: {token}"

    print("Glaze V1.4 performance qualification contract validated.")


if __name__ == "__main__":
    main()