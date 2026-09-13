#!/usr/bin/env python3
"""Run immutable GoreeCloud Care V1.2 validators in their historical registry context.

GLAZE UI V1.4 is the current required Stable consumer baseline. The Care V1.2
validators predate that promotion and intentionally assert the registry state that was
current when the V1.2 acceptance was issued. This compatibility runner preserves those
historical validators unchanged while proving, before and after the historical check,
that the live registry still requires V1.4 and merely retains the V1.2 acceptance as
historical provenance.

The temporary registry rewrite exists only in the CI working tree. The exact original
bytes are restored in a finally block and the current registry validator is rerun.
"""
from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "consumers" / "registry.json"
CURRENT_VALIDATOR = ROOT / "scripts" / "validate_consumer_registry.py"

CURRENT_GLAZE = "1.4.0"
HISTORICAL_GLAZE = "1.2.0"
CARE_SOURCE = "bbc4779454c2887b810aa0ddc9e8a686a4c68ebd"
CARE_EVIDENCE = "acceptance/goreecloud-care-v1.2-0.1.0-exact-source-bridge.json"
ALLOWED_VALIDATORS = {
    "prequalification": ROOT / "scripts" / "validate_goreecloud_care_v1_2_prequalification.py",
    "final-acceptance": ROOT / "scripts" / "validate_goreecloud_care_v1_2_final_acceptance.py",
}


def fail(message: str) -> None:
    raise SystemExit(f"Care V1.2 historical validation compatibility boundary failed: {message}")


def load_registry(raw: str) -> dict:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail(f"consumer registry is invalid JSON: {exc}")
    if not isinstance(value, dict):
        fail("consumer registry must contain an object")
    return value


def care_entry(registry: dict) -> dict:
    consumers = registry.get("consumers")
    if not isinstance(consumers, list):
        fail("consumer registry list is missing")
    matches = [item for item in consumers if isinstance(item, dict) and item.get("name") == "GoreeCloud Care"]
    if len(matches) != 1:
        fail("consumer registry must contain exactly one GoreeCloud Care entry")
    return matches[0]


def validate_current_registry(registry: dict) -> None:
    if registry.get("schemaVersion") != 8:
        fail("current registry schemaVersion must remain 8")
    if registry.get("officialBaseline") != CURRENT_GLAZE:
        fail("current officialBaseline must remain 1.4.0")
    if registry.get("requiredConsumerVersion") != CURRENT_GLAZE:
        fail("current requiredConsumerVersion must remain 1.4.0")

    care = care_entry(registry)
    expected = {
        "status": "adoption-required",
        "targetVersion": HISTORICAL_GLAZE,
        "requiredTargetVersion": CURRENT_GLAZE,
        "referenceRevision": CARE_SOURCE,
        "evidence": CARE_EVIDENCE,
        "productionEligible": False,
    }
    for key, value in expected.items():
        if care.get(key) != value:
            fail(f"current GoreeCloud Care {key} must remain {value!r}")


def historical_registry(current: dict) -> dict:
    historical = copy.deepcopy(current)
    historical["officialBaseline"] = HISTORICAL_GLAZE
    historical["requiredConsumerVersion"] = HISTORICAL_GLAZE
    care = care_entry(historical)
    care["status"] = "accepted-v1"
    care["targetVersion"] = HISTORICAL_GLAZE
    care["requiredTargetVersion"] = HISTORICAL_GLAZE
    care["referenceRevision"] = CARE_SOURCE
    care["evidence"] = CARE_EVIDENCE
    care["productionEligible"] = False
    return historical


def run(path: Path) -> None:
    subprocess.run([sys.executable, str(path)], cwd=ROOT, check=True)


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in ALLOWED_VALIDATORS:
        allowed = ", ".join(sorted(ALLOWED_VALIDATORS))
        fail(f"usage: {Path(sys.argv[0]).name} <{allowed}>")

    original_raw = REGISTRY.read_text(encoding="utf-8")
    current = load_registry(original_raw)
    validate_current_registry(current)
    run(CURRENT_VALIDATOR)

    temporary = historical_registry(current)
    validator = ALLOWED_VALIDATORS[sys.argv[1]]

    try:
        REGISTRY.write_text(json.dumps(temporary, indent=2) + "\n", encoding="utf-8")
        run(validator)
    finally:
        REGISTRY.write_text(original_raw, encoding="utf-8")

    restored_raw = REGISTRY.read_text(encoding="utf-8")
    if restored_raw != original_raw:
        fail("consumer registry was not restored byte-for-byte")
    validate_current_registry(load_registry(restored_raw))
    run(CURRENT_VALIDATOR)

    print(
        "GoreeCloud Care V1.2 historical acceptance lineage: PASS; "
        "current GLAZE UI V1.4 adoption-required registry state restored and revalidated."
    )


if __name__ == "__main__":
    main()
