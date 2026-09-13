#!/usr/bin/env python3
"""Evaluate bounded Glaze UI V1.4 native-renderer parity evidence.

The evaluator validates exact-source-bound, content-addressed parity evidence.
It does not compare pixels itself and cannot promote V1.4 into a lifecycle gate.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys

SCHEMA_VERSION = "glaze.v1.4.native-renderer-parity-evidence.candidate.v1"
CANDIDATE_VERSION = "1.4.0-candidate"
SHA = re.compile(r"^[0-9a-f]{40}$")
SCENE_ID = re.compile(r"^[a-z0-9][a-z0-9._-]{0,79}$")
EVIDENCE_REFERENCE = re.compile(r"^evidence\+sha256:[0-9a-f]{64}:\S{1,175}$")
CONTROL = re.compile(r"[\x00-\x1f\x7f-\x9f]")
PLATFORMS = {"android", "ios", "linux", "windows", "macos", "chromeos", "other"}
ROOT_FIELDS = {
    "schemaVersion",
    "candidateVersion",
    "sourceRevision",
    "sourceTreeRevision",
    "platformFamily",
    "environment",
    "capturedAt",
    "comparisonContract",
    "scenes",
    "reviewer",
    "result",
    "lifecycleAcceptance",
}


def _object(value, name: str) -> dict:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be an object")
    return value


def _closed(value: dict, allowed: set[str], name: str) -> None:
    extra = sorted(set(value) - allowed)
    if extra:
        raise ValueError(f"{name} contains unsupported fields: {', '.join(extra)}")


def _text(value, name: str, maximum: int) -> str:
    if (
        not isinstance(value, str)
        or not value
        or len(value) > maximum
        or value != value.strip()
        or CONTROL.search(value)
    ):
        raise ValueError(f"{name} must be bounded canonical text")
    return value


def _revision(value, name: str) -> str:
    value = _text(value, name, 40)
    if SHA.fullmatch(value) is None:
        raise ValueError(f"{name} must be an immutable 40-character lowercase revision")
    return value


def _evidence_reference(value, name: str) -> str:
    value = _text(value, name, 256)
    if EVIDENCE_REFERENCE.fullmatch(value) is None:
        raise ValueError(f"{name} must be a content-addressed evidence+sha256 reference")
    return value


def _timestamp(value, name: str) -> str:
    value = _text(value, name, 40)
    if not value.endswith("Z"):
        raise ValueError(f"{name} must be canonical UTC with Z suffix")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ValueError(f"{name} must be a valid ISO date-time") from exc
    normalized = parsed.isoformat(timespec="milliseconds").replace("+00:00", "Z")
    if value != normalized:
        raise ValueError(f"{name} must be canonical UTC with millisecond precision")
    return value


def _positive_int(value, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value


def evaluate(
    record: dict,
    *,
    expected_source_revision: str | None = None,
    expected_source_tree_revision: str | None = None,
    max_evidence_age_ms: int | None = None,
    evaluated_at: datetime | None = None,
) -> dict:
    record = _object(record, "native renderer parity record")
    _closed(record, ROOT_FIELDS, "native renderer parity record")
    missing = sorted(ROOT_FIELDS - set(record))
    if missing:
        raise ValueError(f"native renderer parity record missing fields: {', '.join(missing)}")

    if record["schemaVersion"] != SCHEMA_VERSION:
        raise ValueError("unsupported native renderer parity schemaVersion")
    if record["candidateVersion"] != CANDIDATE_VERSION:
        raise ValueError("candidateVersion must remain 1.4.0-candidate")
    source_revision = _revision(record["sourceRevision"], "sourceRevision")
    source_tree_revision = _revision(record["sourceTreeRevision"], "sourceTreeRevision")
    if record["platformFamily"] not in PLATFORMS:
        raise ValueError("platformFamily must identify a native target family")

    environment = _object(record["environment"], "environment")
    environment_fields = {"runtime", "nativeRenderer", "referenceRenderer", "deviceClass", "osVersion"}
    _closed(environment, environment_fields, "environment")
    if set(environment) != environment_fields:
        raise ValueError("environment is incomplete")
    for key in environment_fields:
        _text(environment[key], f"environment.{key}", 160)

    captured_at = _timestamp(record["capturedAt"], "capturedAt")
    assessment_time = evaluated_at or datetime.now(timezone.utc)
    if assessment_time.tzinfo is None or assessment_time.utcoffset() is None:
        raise ValueError("evaluated_at must be timezone-aware")
    assessment_time_utc = assessment_time.astimezone(timezone.utc)
    captured_time = datetime.fromisoformat(captured_at[:-1] + "+00:00")
    if captured_time > assessment_time_utc:
        raise ValueError("capturedAt cannot be future-dated")

    comparison = _object(record["comparisonContract"], "comparisonContract")
    comparison_fields = {"authority", "method", "acceptanceCriteria"}
    _closed(comparison, comparison_fields, "comparisonContract")
    if set(comparison) != comparison_fields:
        raise ValueError("comparisonContract is incomplete")
    _text(comparison["authority"], "comparisonContract.authority", 200)
    _text(comparison["method"], "comparisonContract.method", 500)
    _text(comparison["acceptanceCriteria"], "comparisonContract.acceptanceCriteria", 800)

    scenes = record["scenes"]
    if not isinstance(scenes, list) or not 1 <= len(scenes) <= 64:
        raise ValueError("scenes must contain between 1 and 64 comparisons")
    scene_ids: set[str] = set()
    evidence_refs: set[str] = set()
    scene_results: list[dict] = []
    for index, scene in enumerate(scenes):
        scene = _object(scene, f"scenes[{index}]")
        fields = {"id", "referenceEvidence", "nativeEvidence", "disposition", "rationale"}
        _closed(scene, fields, f"scenes[{index}]")
        if set(scene) != fields:
            raise ValueError(f"scenes[{index}] is incomplete")
        scene_id = _text(scene["id"], f"scenes[{index}].id", 80)
        if SCENE_ID.fullmatch(scene_id) is None:
            raise ValueError(f"scenes[{index}].id must be a canonical scene identifier")
        if scene_id in scene_ids:
            raise ValueError(f"duplicate scene id: {scene_id}")
        scene_ids.add(scene_id)
        for key in ("referenceEvidence", "nativeEvidence"):
            ref = _evidence_reference(scene[key], f"scenes[{index}].{key}")
            if ref in evidence_refs:
                raise ValueError("native renderer parity evidence references must be unique")
            evidence_refs.add(ref)
        if scene["disposition"] not in {"pending", "accepted", "rejected"}:
            raise ValueError(f"scenes[{index}].disposition is unsupported")
        _text(scene["rationale"], f"scenes[{index}].rationale", 500)
        scene_results.append({"id": scene_id, "accepted": scene["disposition"] == "accepted"})

    reviewer = _object(record["reviewer"], "reviewer")
    reviewer_fields = {
        "authority",
        "authorityEvidence",
        "reviewEvidence",
        "reviewedAt",
        "disposition",
        "rationale",
    }
    _closed(reviewer, reviewer_fields, "reviewer")
    if set(reviewer) != reviewer_fields:
        raise ValueError("reviewer is incomplete")
    _text(reviewer["authority"], "reviewer.authority", 200)
    authority_evidence = _evidence_reference(reviewer["authorityEvidence"], "reviewer.authorityEvidence")
    review_evidence = _evidence_reference(reviewer["reviewEvidence"], "reviewer.reviewEvidence")
    if authority_evidence == review_evidence:
        raise ValueError("reviewer authority and review evidence references must be distinct")
    if authority_evidence in evidence_refs or review_evidence in evidence_refs:
        raise ValueError("reviewer evidence references must be distinct from scene evidence")
    evidence_refs.add(authority_evidence)
    evidence_refs.add(review_evidence)

    reviewed_at = _timestamp(reviewer["reviewedAt"], "reviewer.reviewedAt")
    reviewed_time = datetime.fromisoformat(reviewed_at[:-1] + "+00:00")
    if reviewed_time < captured_time:
        raise ValueError("reviewer.reviewedAt cannot precede capturedAt")
    if reviewed_time > assessment_time_utc:
        raise ValueError("reviewer.reviewedAt cannot be future-dated")
    if reviewer["disposition"] not in {"pending", "accepted", "rejected"}:
        raise ValueError("reviewer.disposition is unsupported")
    _text(reviewer["rationale"], "reviewer.rationale", 500)

    if record["result"] not in {"blocked", "passed", "failed"}:
        raise ValueError("result is unsupported")
    if record["lifecycleAcceptance"] is not False:
        raise ValueError("native renderer parity evidence cannot grant lifecycle acceptance")

    reasons: list[str] = []
    if expected_source_revision is None:
        reasons.append("source_revision_expectation_missing")
    else:
        expected_source_revision = _revision(expected_source_revision, "expected source revision")
        if source_revision != expected_source_revision:
            reasons.append("source_revision_mismatch")
    if expected_source_tree_revision is None:
        reasons.append("source_tree_revision_expectation_missing")
    else:
        expected_source_tree_revision = _revision(expected_source_tree_revision, "expected source tree revision")
        if source_tree_revision != expected_source_tree_revision:
            reasons.append("source_tree_revision_mismatch")
    if max_evidence_age_ms is None:
        reasons.append("evidence_age_expectation_missing")
    else:
        max_evidence_age_ms = _positive_int(max_evidence_age_ms, "max_evidence_age_ms")
        evidence_age_ms = (assessment_time_utc - captured_time).total_seconds() * 1000
        if evidence_age_ms > max_evidence_age_ms:
            reasons.append("parity_evidence_stale")
    if not all(item["accepted"] for item in scene_results):
        reasons.append("scene_parity_not_accepted")
    if reviewer["disposition"] != "accepted":
        reasons.append("review_not_accepted")
    if record["result"] != "passed":
        reasons.append("record_not_marked_passed")

    accepted = not reasons
    return {
        "schemaVersion": SCHEMA_VERSION,
        "candidateVersion": CANDIDATE_VERSION,
        "sourceRevision": source_revision,
        "sourceTreeRevision": source_tree_revision,
        "reviewedAt": reviewed_at,
        "evaluatorDisposition": "accepted" if accepted else "blocked",
        "acceptedForNativeRendererParityQualification": accepted,
        "acceptedForLifecycleGate": False,
        "reasonCodes": reasons,
        "scenes": scene_results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    parser.add_argument("--expected-source-revision")
    parser.add_argument("--expected-source-tree-revision")
    parser.add_argument("--max-evidence-age-ms", type=int)
    args = parser.parse_args()
    try:
        payload = json.loads(args.record.read_text(encoding="utf-8"))
        result = evaluate(
            payload,
            expected_source_revision=args.expected_source_revision,
            expected_source_tree_revision=args.expected_source_tree_revision,
            max_evidence_age_ms=args.max_evidence_age_ms,
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({
            "evaluatorDisposition": "blocked",
            "acceptedForNativeRendererParityQualification": False,
            "acceptedForLifecycleGate": False,
            "error": str(exc),
        }, indent=2))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
