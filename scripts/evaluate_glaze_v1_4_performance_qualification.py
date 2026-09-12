#!/usr/bin/env python3
"""Evaluate bounded Glaze UI V1.4 performance-qualification evidence.

This evaluator validates source-bound performance evidence. It deliberately
cannot promote the V1.4 candidate into the repository lifecycle gate.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import math
from pathlib import Path
import re
import sys

SCHEMA_VERSION = "glaze.v1.4.performance-qualification-evidence.candidate.v1"
CANDIDATE_VERSION = "1.4.0-candidate"
SHA = re.compile(r"^[0-9a-f]{40}$")
CONTROL = re.compile(r"[\x00-\x1f\x7f-\x9f]")
PLATFORMS = {"web", "android", "ios", "linux", "windows", "macos", "chromeos", "other"}
METRIC_UNITS = {
    "startup_ms": "ms",
    "runtime_init_ms": "ms",
    "stylesheet_parse_ms": "ms",
    "first_interaction_ms": "ms",
    "interaction_latency_p95_ms": "ms",
    "frame_p95_ms": "ms",
    "frame_p99_ms": "ms",
    "memory_peak_mib": "MiB",
}
ROOT_FIELDS = {
    "schemaVersion",
    "candidateVersion",
    "sourceRevision",
    "sourceTreeRevision",
    "platformFamily",
    "environment",
    "measuredAt",
    "metrics",
    "evidenceRefs",
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
        raise ValueError(f"{name} must be an immutable 40-character lowercase commit revision")
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


def _number(value, name: str, *, positive: bool) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    numeric = float(value)
    if positive and numeric <= 0:
        raise ValueError(f"{name} must be greater than zero")
    if not positive and numeric < 0:
        raise ValueError(f"{name} must not be negative")
    return numeric


def evaluate(record: dict, *, expected_source_revision: str | None = None, expected_source_tree_revision: str | None = None) -> dict:
    record = _object(record, "performance qualification record")
    _closed(record, ROOT_FIELDS, "performance qualification record")
    missing = sorted(ROOT_FIELDS - set(record))
    if missing:
        raise ValueError(f"performance qualification record missing fields: {', '.join(missing)}")

    if record["schemaVersion"] != SCHEMA_VERSION:
        raise ValueError("unsupported performance qualification schemaVersion")
    if record["candidateVersion"] != CANDIDATE_VERSION:
        raise ValueError("performance qualification candidateVersion must remain 1.4.0-candidate")
    source_revision = _revision(record["sourceRevision"], "sourceRevision")
    source_tree_revision = _revision(record["sourceTreeRevision"], "sourceTreeRevision")
    if record["platformFamily"] not in PLATFORMS:
        raise ValueError("platformFamily is unsupported")

    environment = _object(record["environment"], "environment")
    _closed(environment, {"runtime", "renderer", "deviceClass"}, "environment")
    if set(environment) != {"runtime", "renderer", "deviceClass"}:
        raise ValueError("environment must contain runtime, renderer, and deviceClass")
    for key in ("runtime", "renderer", "deviceClass"):
        _text(environment[key], f"environment.{key}", 160)

    _timestamp(record["measuredAt"], "measuredAt")

    metrics = record["metrics"]
    if not isinstance(metrics, list) or not 1 <= len(metrics) <= 32:
        raise ValueError("metrics must contain between 1 and 32 observations")
    names: set[str] = set()
    metric_results: list[dict] = []
    for index, metric in enumerate(metrics):
        metric = _object(metric, f"metrics[{index}]")
        fields = {"name", "unit", "measured", "budget", "sampleCount", "accepted"}
        _closed(metric, fields, f"metrics[{index}]")
        if set(metric) != fields:
            raise ValueError(f"metrics[{index}] is incomplete")
        name = metric["name"]
        if name not in METRIC_UNITS:
            raise ValueError(f"metrics[{index}].name is unsupported")
        if name in names:
            raise ValueError(f"duplicate performance metric: {name}")
        names.add(name)
        if metric["unit"] != METRIC_UNITS[name]:
            raise ValueError(f"metrics[{index}].unit does not match {name}")
        measured = _number(metric["measured"], f"metrics[{index}].measured", positive=False)
        budget = _number(metric["budget"], f"metrics[{index}].budget", positive=True)
        sample_count = metric["sampleCount"]
        if isinstance(sample_count, bool) or not isinstance(sample_count, int) or not 1 <= sample_count <= 1_000_000:
            raise ValueError(f"metrics[{index}].sampleCount is invalid")
        if not isinstance(metric["accepted"], bool):
            raise ValueError(f"metrics[{index}].accepted must be boolean")
        expected_accepted = measured <= budget
        if metric["accepted"] is not expected_accepted:
            raise ValueError(f"metrics[{index}].accepted contradicts measured value and budget")
        metric_results.append({"name": name, "accepted": expected_accepted})

    refs = record["evidenceRefs"]
    if not isinstance(refs, list) or len(refs) > 50:
        raise ValueError("evidenceRefs must contain at most 50 references")
    normalized_refs = [_text(value, f"evidenceRefs[{index}]", 256) for index, value in enumerate(refs)]
    if len(set(normalized_refs)) != len(normalized_refs):
        raise ValueError("evidenceRefs must be unique")

    reviewer = _object(record["reviewer"], "reviewer")
    _closed(reviewer, {"authority", "disposition", "rationale"}, "reviewer")
    if set(reviewer) != {"authority", "disposition", "rationale"}:
        raise ValueError("reviewer is incomplete")
    _text(reviewer["authority"], "reviewer.authority", 200)
    if reviewer["disposition"] not in {"pending", "accepted", "rejected"}:
        raise ValueError("reviewer.disposition is unsupported")
    _text(reviewer["rationale"], "reviewer.rationale", 500)

    if record["result"] not in {"blocked", "passed", "failed"}:
        raise ValueError("result is unsupported")
    if record["lifecycleAcceptance"] is not False:
        raise ValueError("performance qualification evidence cannot grant lifecycle acceptance")

    reasons: list[str] = []
    if expected_source_revision is not None:
        _revision(expected_source_revision, "expected source revision")
        if source_revision != expected_source_revision:
            reasons.append("source_revision_mismatch")
    if expected_source_tree_revision is not None:
        _revision(expected_source_tree_revision, "expected source tree revision")
        if source_tree_revision != expected_source_tree_revision:
            reasons.append("source_tree_revision_mismatch")
    if not all(item["accepted"] for item in metric_results):
        reasons.append("metric_budget_exceeded")
    if not normalized_refs:
        reasons.append("measurement_evidence_missing")
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
        "evaluatorDisposition": "accepted" if accepted else "blocked",
        "acceptedForPerformanceQualification": accepted,
        "acceptedForLifecycleGate": False,
        "reasonCodes": reasons,
        "metrics": metric_results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    parser.add_argument("--expected-source-revision")
    parser.add_argument("--expected-source-tree-revision")
    args = parser.parse_args()
    try:
        payload = json.loads(args.record.read_text(encoding="utf-8"))
        result = evaluate(
            payload,
            expected_source_revision=args.expected_source_revision,
            expected_source_tree_revision=args.expected_source_tree_revision,
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"evaluatorDisposition": "blocked", "acceptedForPerformanceQualification": False, "acceptedForLifecycleGate": False, "error": str(exc)}, indent=2))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
