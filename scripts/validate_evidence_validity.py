#!/usr/bin/env python3
"""Fail-closed validation for Glaze UI conformance-evidence validity."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "contracts" / "glaze.conformance-evidence.schema.json"
DOC = ROOT / "docs" / "evidence-validity.md"
CONFORMANCE = ROOT / "CONFORMANCE.md"
VERSION = ROOT / "VERSION"
CURRENT_STABLE = "2.1.0"
EXPECTED_FORM_FACTORS = {
    "mobile",
    "tablet",
    "desktop",
    "tv",
    "web",
    "foldable",
    "wearable",
    "spatial",
}


def fail(message: str) -> None:
    raise SystemExit(f"Glaze UI evidence-validity validation failed: {message}")


def require_object(value: object, name: str) -> dict:
    if not isinstance(value, dict):
        fail(f"{name} must be an object")
    return value


def main() -> None:
    try:
        schema = require_object(json.loads(SCHEMA.read_text(encoding="utf-8")), "schema")
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"conformance evidence schema is unreadable or invalid JSON: {exc}")

    if schema.get("additionalProperties") is not False:
        fail("top-level evidence records must reject unknown properties")

    required = set(schema.get("required", []))
    for field in (
        "producer",
        "target",
        "observed_at",
        "valid_until",
        "claim",
        "acceptance",
        "evidence_references",
    ):
        if field not in required:
            fail(f"conformance evidence schema must require {field}")

    properties = require_object(schema.get("properties"), "schema properties")
    if require_object(properties.get("observed_at"), "observed_at").get("format") != "date-time":
        fail("observed_at must be a date-time")
    if require_object(properties.get("valid_until"), "valid_until").get("format") != "date-time":
        fail("valid_until must be a date-time")

    producer = require_object(properties.get("producer"), "producer")
    producer_props = require_object(producer.get("properties"), "producer properties")
    if require_object(producer_props.get("authoritative"), "producer.authoritative").get("const") is not True:
        fail("evidence producer must remain authoritative")

    target = require_object(properties.get("target"), "target")
    target_required = set(target.get("required", []))
    if "source_revision" not in target_required:
        fail("target must require an exact source revision")
    target_props = require_object(target.get("properties"), "target properties")
    source_revision = require_object(target_props.get("source_revision"), "target.source_revision")
    if source_revision.get("pattern") != "^[0-9a-f]{40}$":
        fail("target source_revision must remain an exact lowercase 40-character SHA")

    form_factors = require_object(target_props.get("form_factors"), "target.form_factors")
    items = require_object(form_factors.get("items"), "target.form_factors.items")
    configured_form_factors = set(items.get("enum", []))
    if configured_form_factors != EXPECTED_FORM_FACTORS:
        fail(
            "2.1 form-factor evidence set mismatch: "
            f"expected {sorted(EXPECTED_FORM_FACTORS)}, got {sorted(configured_form_factors)}"
        )

    acceptance = require_object(properties.get("acceptance"), "acceptance")
    acceptance_props = require_object(acceptance.get("properties"), "acceptance properties")
    current_stable_required = require_object(
        acceptance_props.get("current_stable_required"), "acceptance.current_stable_required"
    )
    if current_stable_required.get("const") is not True:
        fail("current Stable Glaze UI must remain required")

    version = VERSION.read_text(encoding="utf-8").strip()
    if re.fullmatch(r"\d+\.\d+\.\d+", version) is None:
        fail("VERSION must remain semantic")
    if version != CURRENT_STABLE:
        fail(f"evidence validator expects current Stable {CURRENT_STABLE}, found {version}")

    documentation = DOC.read_text(encoding="utf-8").lower()
    conformance = CONFORMANCE.read_text(encoding="utf-8").lower()
    for phrase in ("validity", "producer", "fails closed", "mesh", "extend"):
        if phrase not in documentation:
            fail(f"docs/evidence-validity.md is missing required concept: {phrase}")
    for phrase in (
        "exact design-system/application revision",
        "expired",
        "current stable",
        "application-specific native or real-device acceptance",
    ):
        if phrase not in conformance:
            fail(f"CONFORMANCE.md is missing current evidence rule: {phrase}")

    print(
        f"Glaze UI {version} evidence-validity contract validation passed "
        f"for {len(EXPECTED_FORM_FACTORS)} current form-factor roles."
    )


if __name__ == "__main__":
    main()
