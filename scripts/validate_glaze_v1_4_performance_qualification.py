#!/usr/bin/env python3
"""Validate the V1.4 performance-qualification evidence contract boundary."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "contracts" / "v1.4" / "performance-qualification-evidence.schema.candidate.json"
EVALUATOR = ROOT / "scripts" / "evaluate_glaze_v1_4_performance_qualification.py"
TEST = ROOT / "tests" / "test_glaze_v1_4_performance_qualification.py"
DOC = ROOT / "docs" / "GLAZE_UI_V1_4_PERFORMANCE_QUALIFICATION.md"
EVIDENCE_PATTERN = r"^evidence\+sha256:[0-9a-f]{64}:[^\s]{1,175}$"


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
    assert schema["properties"]["evidenceRefs"]["uniqueItems"] is True
    assert schema["properties"]["evidenceRefs"]["items"]["pattern"] == EVIDENCE_PATTERN

    reviewer = schema["properties"]["reviewer"]
    assert reviewer["additionalProperties"] is False
    assert set(reviewer["required"]) == {
        "authority", "authorityEvidence", "reviewEvidence", "reviewedAt", "disposition", "rationale"
    }
    assert reviewer["properties"]["authorityEvidence"]["pattern"] == EVIDENCE_PATTERN
    assert reviewer["properties"]["reviewEvidence"]["pattern"] == EVIDENCE_PATTERN
    assert reviewer["properties"]["reviewedAt"]["format"] == "date-time"
    assert set(reviewer["properties"]["disposition"]["enum"]) == {"pending", "accepted", "rejected"}

    evaluator = EVALUATOR.read_text(encoding="utf-8")
    for token in (
        "acceptedForPerformanceQualification",
        '"acceptedForLifecycleGate": False',
        "EVIDENCE_REFERENCE",
        "must be a content-addressed evidence+sha256 reference",
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
        "authorityEvidence",
        "reviewEvidence",
        "reviewedAt",
        "reviewer authority and review evidence references must be distinct",
        "reviewer evidence references must be distinct from measurement evidence",
        "reviewer.reviewedAt cannot precede measuredAt",
        "reviewer.reviewedAt cannot be future-dated",
    ):
        assert token in evaluator, f"performance evaluator missing invariant: {token}"

    test_text = TEST.read_text(encoding="utf-8")
    for token in (
        "passing measured evidence with immutable review provenance can qualify performance without granting lifecycle acceptance",
        "performance qualification must require exact source, tree, and measurement-age expectations",
        "accepted flag cannot contradict the measured value and budget",
        "duplicate metrics fail closed",
        "exact source mismatch blocks otherwise passing evidence",
        "exact source-tree mismatch blocks otherwise passing evidence",
        "future-dated performance measurements must fail closed",
        "caller-selected measurement freshness must block stale performance evidence",
        "measurement freshness policy must be a positive integer",
        "performance qualification must reject mutable or non-content-addressed measurement evidence references",
        "performance qualification must reject malformed content-addressed measurement evidence references",
        "performance qualification must reject mutable reviewer authority evidence",
        "performance qualification must reject mutable review attestation evidence",
        "review authority and review attestation evidence must be distinct",
        "review provenance must be distinct from measurement evidence",
        "performance review cannot predate the measurements it accepts",
        "future-dated performance review must fail closed",
    ):
        assert token in test_text, f"performance tests missing invariant: {token}"

    doc_text = DOC.read_text(encoding="utf-8")
    for token in (
        "review authority evidence",
        "review attestation evidence",
        "distinct from measurement evidence",
        "cannot predate the measurements",
        "cannot be future-dated",
        "does not prove that the named reviewer is genuinely authorized",
    ):
        assert token in doc_text, f"performance qualification documentation missing invariant: {token}"

    print("Glaze V1.4 performance qualification contract validated.")


if __name__ == "__main__":
    main()
