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


def fail(message: str) -> None:
    raise SystemExit(f"Glaze UI evidence-validity validation failed: {message}")


def main() -> None:
    try:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"conformance evidence schema is unreadable or invalid JSON: {exc}")
    if not isinstance(schema, dict):
        fail("conformance evidence schema must contain an object")

    required = set(schema.get("required", []))
    for field in ("producer", "target", "observed_at", "valid_until", "claim", "acceptance", "evidence_references"):
        if field not in required:
            fail(f"conformance evidence schema must require {field}")
    properties = schema.get("properties", {})
    if properties.get("observed_at", {}).get("format") != "date-time":
        fail("observed_at must be a date-time")
    if properties.get("valid_until", {}).get("format") != "date-time":
        fail("valid_until must be a date-time")
    if properties.get("producer", {}).get("properties", {}).get("authoritative", {}).get("const") is not True:
        fail("evidence producer must remain authoritative")
    if properties.get("acceptance", {}).get("properties", {}).get("current_stable_required", {}).get("const") is not True:
        fail("current Stable Glaze UI must remain required")

    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if re.fullmatch(r"\d+\.\d+\.\d+", version) is None:
        fail("VERSION must remain semantic")

    documentation = DOC.read_text(encoding="utf-8").lower()
    conformance = CONFORMANCE.read_text(encoding="utf-8").lower()
    for phrase in ("validity", "producer", "fail", "mesh", "extend"):
        if phrase not in documentation:
            fail(f"docs/evidence-validity.md is missing required concept: {phrase}")
    for phrase in ("current stable", "validity deadline", "missing when required", "has expired"):
        if phrase not in conformance:
            fail(f"CONFORMANCE.md is missing current evidence rule: {phrase}")

    print(f"Glaze UI {version} evidence-validity contract validation passed.")


if __name__ == "__main__":
    main()
