#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime, timezone
import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "evaluate_glaze_v1_4_native_renderer_parity.py"
spec = importlib.util.spec_from_file_location("native_parity", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)

NOW = datetime(2026, 9, 12, 12, 0, 0, tzinfo=timezone.utc)
REV = "a" * 40
TREE = "b" * 40


def record() -> dict:
    return {
        "schemaVersion": module.SCHEMA_VERSION,
        "candidateVersion": module.CANDIDATE_VERSION,
        "sourceRevision": REV,
        "sourceTreeRevision": TREE,
        "platformFamily": "android",
        "environment": {
            "runtime": "Android runtime",
            "nativeRenderer": "Compose renderer",
            "referenceRenderer": "Glaze reference web renderer",
            "deviceClass": "phone",
            "osVersion": "Android 16",
        },
        "capturedAt": "2026-09-12T11:00:00.000Z",
        "comparisonContract": {
            "authority": "Glaze qualification owner",
            "method": "Paired captures from the same governed scene and state.",
            "acceptanceCriteria": "Owner-defined semantic and optical parity acceptance for this target.",
        },
        "scenes": [{
            "id": "settings.material-card",
            "referenceEvidence": "evidence+sha256:" + "1" * 64 + ":reference.png",
            "nativeEvidence": "evidence+sha256:" + "2" * 64 + ":native.png",
            "disposition": "accepted",
            "rationale": "Reviewed against the owner-selected target criteria.",
        }],
        "reviewer": {
            "authority": "Glaze qualification reviewer",
            "disposition": "accepted",
            "rationale": "Scene evidence accepted for parity qualification.",
        },
        "result": "passed",
        "lifecycleAcceptance": False,
    }


def evaluate(payload: dict, **kwargs) -> dict:
    return module.evaluate(
        payload,
        expected_source_revision=kwargs.get("expected_source_revision", REV),
        expected_source_tree_revision=kwargs.get("expected_source_tree_revision", TREE),
        max_evidence_age_ms=kwargs.get("max_evidence_age_ms", 7_200_000),
        evaluated_at=kwargs.get("evaluated_at", NOW),
    )


def main() -> None:
    accepted = evaluate(record())
    assert accepted["acceptedForNativeRendererParityQualification"] is True
    assert accepted["acceptedForLifecycleGate"] is False
    assert accepted["reasonCodes"] == []

    missing_expectations = module.evaluate(record(), evaluated_at=NOW)
    assert missing_expectations["acceptedForNativeRendererParityQualification"] is False
    assert set(missing_expectations["reasonCodes"]) == {
        "source_revision_expectation_missing",
        "source_tree_revision_expectation_missing",
        "evidence_age_expectation_missing",
    }

    pending = record()
    pending["scenes"][0]["disposition"] = "pending"
    pending["reviewer"]["disposition"] = "pending"
    pending["result"] = "blocked"
    reasons = set(evaluate(pending)["reasonCodes"])
    assert {"scene_parity_not_accepted", "review_not_accepted", "record_not_marked_passed"} <= reasons

    stale = evaluate(record(), max_evidence_age_ms=1_000)
    assert "parity_evidence_stale" in stale["reasonCodes"]

    mismatch = evaluate(record(), expected_source_revision="c" * 40)
    assert "source_revision_mismatch" in mismatch["reasonCodes"]

    invalid_ref = record()
    invalid_ref["scenes"][0]["nativeEvidence"] = "artifact:latest"
    try:
        evaluate(invalid_ref)
    except ValueError as exc:
        assert "content-addressed" in str(exc)
    else:
        raise AssertionError("mutable evidence reference was accepted")

    duplicate = record()
    duplicate["scenes"].append(copy.deepcopy(duplicate["scenes"][0]))
    try:
        evaluate(duplicate)
    except ValueError as exc:
        assert "duplicate scene id" in str(exc)
    else:
        raise AssertionError("duplicate scene id was accepted")

    lifecycle = record()
    lifecycle["lifecycleAcceptance"] = True
    try:
        evaluate(lifecycle)
    except ValueError as exc:
        assert "cannot grant lifecycle acceptance" in str(exc)
    else:
        raise AssertionError("lifecycle promotion was accepted")

    future = record()
    future["capturedAt"] = "2026-09-12T13:00:00.000Z"
    try:
        evaluate(future)
    except ValueError as exc:
        assert "future-dated" in str(exc)
    else:
        raise AssertionError("future-dated evidence was accepted")

    template = json.loads((ROOT / "evidence/v1.4/templates/native-renderer-parity-record.candidate.json").read_text())
    template_result = module.evaluate(template, evaluated_at=NOW)
    assert template_result["acceptedForNativeRendererParityQualification"] is False
    assert template_result["acceptedForLifecycleGate"] is False

    print("Glaze V1.4 native renderer parity qualification regressions: PASS")


if __name__ == "__main__":
    main()
