#!/usr/bin/env python3
"""Validate the Glaze UI semantic color contract."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "tokens" / "semantic-colors.json"
DOC = ROOT / "COLOR.md"

REQUIRED_ROLES = {
    "accent", "surface", "selected", "focus", "success", "information",
    "warning", "danger", "protected", "restricted", "online", "offline",
    "syncing", "unavailable",
}

REQUIRED_MODES = {
    "light", "dark", "high-contrast", "grayscale",
    "color-vision-deficiency", "custom-theme",
}

REQUIRED_INVARIANTS = {
    "material-state-has-non-color-companion",
    "semantic-meaning-survives-theme-adaptation",
    "branding-does-not-redefine-system-semantics",
    "danger-is-distinct-from-accent",
    "warning-is-distinct-from-information-and-success",
    "protected-is-distinct-from-restricted",
    "online-is-distinct-from-offline-and-unavailable",
    "unknown-or-unverified-evidence-is-not-upgraded-to-positive-state",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def main() -> None:
    if not CONTRACT.is_file():
        fail("semantic color token contract is missing")
    if not DOC.is_file():
        fail("COLOR.md semantic color documentation is missing")

    try:
        data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid semantic color JSON: {exc}")

    if data.get("schema_version") != "1.0.0":
        fail("unexpected semantic color schema version")
    if data.get("design_system") != "Glaze UI":
        fail("semantic color contract must identify Glaze UI")
    if data.get("color_only_communication_allowed") is not False:
        fail("color-only communication must remain forbidden")
    if data.get("branding_may_override_semantics") is not False:
        fail("branding must not override semantic color meaning")

    roles = data.get("roles")
    if not isinstance(roles, dict):
        fail("roles must be an object")
    if set(roles) != REQUIRED_ROLES:
        missing = sorted(REQUIRED_ROLES - set(roles))
        extra = sorted(set(roles) - REQUIRED_ROLES)
        fail(f"semantic role mismatch; missing={missing}, extra={extra}")

    for name, role in roles.items():
        if not isinstance(role, dict) or not role.get("category") or not role.get("meaning"):
            fail(f"role {name!r} must define category and meaning")

    if roles["protected"].get("authoritative_evidence_required") is not True:
        fail("protected state must require authoritative evidence")

    modes = set(data.get("required_accessibility_modes", []))
    if modes != REQUIRED_MODES:
        fail("required accessibility-mode set is incomplete or unexpected")

    invariants = set(data.get("required_invariants", []))
    if invariants != REQUIRED_INVARIANTS:
        fail("required semantic-color invariants are incomplete or unexpected")

    doc = DOC.read_text(encoding="utf-8").lower()
    for phrase in (
        "color alone",
        "branding and semantic separation",
        "centralized token rule",
        "high-contrast",
        "grayscale",
        "color-vision",
        "authoritative producer",
    ):
        if phrase not in doc:
            fail(f"COLOR.md missing required concept: {phrase}")

    print("Glaze UI semantic color contract validation passed.")


if __name__ == "__main__":
    main()
