#!/usr/bin/env python3
from __future__ import annotations

import copy
import unittest
from datetime import UTC, datetime, timedelta

from validate_conformance_evidence import EvidenceError, validate_record

NOW = datetime(2026, 9, 1, 23, 55, tzinfo=UTC)
REVISION = "a" * 40


def integration(applicable: bool = True, valid: bool = True) -> dict[str, object]:
    if not applicable:
        return {
            "applicability": "not_applicable",
            "current_evidence_valid": False,
            "evidence_references": [],
        }
    return {
        "applicability": "applicable",
        "current_evidence_valid": valid,
        "evidence_references": ["evidence://integration/current"],
    }


def valid_record() -> dict[str, object]:
    return {
        "schema_version": 2,
        "producer": {"system": "goreecloud-acceptance", "authoritative": True},
        "target": {
            "application": "example-app",
            "glaze_version": "2.2.0",
            "source_revision": REVISION,
            "form_factors": ["mobile", "desktop"],
        },
        "observed_at": NOW.isoformat(),
        "valid_until": (NOW + timedelta(days=7)).isoformat(),
        "claim": {"kind": "conformance", "accepted": True},
        "acceptance": {
            "current_stable_required": True,
            "application_specific_acceptance_complete": True,
        },
        "integral_platform_integrations": {
            "identity": integration(),
            "privacy_shield": integration(),
            "wardveil_security": integration(),
            "everkeep": integration(),
            "goreecloud_mesh": integration(),
        },
        "evidence_references": ["evidence://glaze/current"],
    }


class EvidenceValidityTests(unittest.TestCase):
    def test_accepts_current_complete_evidence(self) -> None:
        record = valid_record()
        self.assertEqual(validate_record(record, now=NOW), record)

    def test_rejects_stale_glaze_version(self) -> None:
        record = valid_record()
        record["target"]["glaze_version"] = "2.1.0"  # type: ignore[index]
        with self.assertRaisesRegex(EvidenceError, "current Stable"):
            validate_record(record, now=NOW)

    def test_rejects_expired_evidence(self) -> None:
        record = valid_record()
        record["valid_until"] = (NOW - timedelta(seconds=1)).isoformat()
        with self.assertRaisesRegex(EvidenceError, "expired"):
            validate_record(record, now=NOW)

    def test_rejects_accepted_claim_without_application_acceptance(self) -> None:
        record = valid_record()
        record["acceptance"]["application_specific_acceptance_complete"] = False  # type: ignore[index]
        with self.assertRaisesRegex(EvidenceError, "application-specific acceptance"):
            validate_record(record, now=NOW)

    def test_rejects_accepted_claim_with_stale_integral_system_evidence(self) -> None:
        record = valid_record()
        record["integral_platform_integrations"]["wardveil_security"][  # type: ignore[index]
            "current_evidence_valid"
        ] = False
        with self.assertRaisesRegex(EvidenceError, "wardveil_security"):
            validate_record(record, now=NOW)

    def test_not_applicable_system_cannot_carry_acceptance_evidence(self) -> None:
        record = valid_record()
        record["integral_platform_integrations"]["everkeep"] = integration(False)  # type: ignore[index]
        validate_record(record, now=NOW)
        invalid = copy.deepcopy(record)
        invalid["integral_platform_integrations"]["everkeep"][  # type: ignore[index]
            "current_evidence_valid"
        ] = True
        with self.assertRaisesRegex(EvidenceError, "not_applicable"):
            validate_record(invalid, now=NOW)

    def test_rejects_unknown_fields_and_bad_revision(self) -> None:
        record = valid_record()
        record["unexpected"] = True
        with self.assertRaisesRegex(EvidenceError, "unknown field"):
            validate_record(record, now=NOW)

        record = valid_record()
        record["target"]["source_revision"] = "abc"  # type: ignore[index]
        with self.assertRaisesRegex(EvidenceError, "40-character SHA"):
            validate_record(record, now=NOW)


if __name__ == "__main__":
    unittest.main()
