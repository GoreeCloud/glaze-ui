#!/usr/bin/env python3
"""Validate credential-safe Glaze UI V1.4 evidence references across qualification planes."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
WORKFLOWS = ROOT / ".github" / "workflows"
DOCUMENTATION = ROOT / "docs" / "GLAZE_UI_V1_4_EVIDENCE_REFERENCE_PRIVACY.md"
SELF_PATH = "scripts/validate_glaze_v1_4_evidence_reference_privacy.py"
CANONICAL_OPTICAL_VALIDATOR = "scripts/validate_glaze_v1.4_optical_material.py"
OBSOLETE_OPTICAL_VALIDATORS = (
    "scripts/validate_glaze_v1_4_optical_material.py",
    "scripts/validate_glaze-v1.4_optical_material.py",
)

EXPECTED_PATTERN = (
    r"^evidence\+sha256:[0-9a-f]{64}:"
    r"[A-Za-z0-9][A-Za-z0-9._+-]*"
    r"(?::[A-Za-z0-9][A-Za-z0-9._+-]*)*"
    r"(?:/[A-Za-z0-9][A-Za-z0-9._+-]*"
    r"(?::[A-Za-z0-9][A-Za-z0-9._+-]*)*)*$"
)

EVALUATORS = {
    "performance": SCRIPTS / "evaluate_glaze_v1_4_performance_qualification.py",
    "native_renderer_parity": SCRIPTS / "evaluate_glaze_v1_4_native_renderer_parity.py",
    "accessibility": SCRIPTS / "evaluate_glaze_v1_4_accessibility_qualification.py",
}
SCHEMAS = {
    "performance": ROOT / "contracts" / "v1.4" / "performance-qualification-evidence.schema.candidate.json",
    "native_renderer_parity": ROOT / "contracts" / "v1.4" / "native-renderer-parity-evidence.schema.candidate.json",
    "accessibility": ROOT / "contracts" / "v1.4" / "accessibility-qualification-evidence.schema.candidate.json",
}
APPLICABLE_WORKFLOWS = (
    "glaze-v1.4-performance-qualification.yml",
    "glaze-v1.4-native-renderer-parity.yml",
    "glaze-v1.4-optical-material.yml",
    "glaze-v1.4-v1.3-compatibility.yml",
    "glaze-v1.3-stable-authority.yml",
    "glaze-v1.4-evidence-reference-privacy.yml",
)
OPTICAL_VALIDATOR_WORKFLOWS = (
    "glaze-v1.4-optical-material.yml",
    "glaze-v1.4-v1.3-compatibility.yml",
)

SAFE_LOCATORS = (
    "run-1",
    "review:authority",
    "reports/performance/run-1.json",
    "native/reference-scene-01.png",
    "accessibility/screen-reader:observation-1.json",
)
UNSAFE_LOCATORS = (
    "https://evidence.example/report",
    "report?sig=opaque",
    "report#fragment",
    "user@example",
    "report%2Fsecret",
    "report&sig=opaque",
    "report=opaque",
    "report\\child",
    "report child",
)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(f"glaze_evidence_privacy_{name}", path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"could not load {path.relative_to(ROOT)}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def assert_schema_patterns() -> None:
    performance = json.loads(SCHEMAS["performance"].read_text(encoding="utf-8"))
    perf_props = performance["properties"]
    assert perf_props["evidenceRefs"]["items"]["pattern"] == EXPECTED_PATTERN
    assert perf_props["reviewer"]["properties"]["authorityEvidence"]["pattern"] == EXPECTED_PATTERN
    assert perf_props["reviewer"]["properties"]["reviewEvidence"]["pattern"] == EXPECTED_PATTERN

    parity = json.loads(SCHEMAS["native_renderer_parity"].read_text(encoding="utf-8"))
    parity_scene = parity["properties"]["scenes"]["items"]["properties"]
    assert parity_scene["referenceEvidence"]["pattern"] == EXPECTED_PATTERN
    assert parity_scene["nativeEvidence"]["pattern"] == EXPECTED_PATTERN
    parity_reviewer = parity["properties"]["reviewer"]["properties"]
    assert parity_reviewer["authorityEvidence"]["pattern"] == EXPECTED_PATTERN
    assert parity_reviewer["reviewEvidence"]["pattern"] == EXPECTED_PATTERN

    accessibility = json.loads(SCHEMAS["accessibility"].read_text(encoding="utf-8"))
    assert accessibility["$defs"]["evidenceReference"]["pattern"] == EXPECTED_PATTERN


def assert_workflow_applicability() -> None:
    for workflow_name in APPLICABLE_WORKFLOWS:
        text = (WORKFLOWS / workflow_name).read_text(encoding="utf-8")
        assert SELF_PATH in text, f"{workflow_name} is not triggered by shared evidence-reference privacy changes"


def assert_optical_validator_path_integrity() -> None:
    canonical_path = ROOT / CANONICAL_OPTICAL_VALIDATOR
    assert canonical_path.is_file(), f"canonical optical validator is missing: {CANONICAL_OPTICAL_VALIDATOR}"
    for obsolete_path in OBSOLETE_OPTICAL_VALIDATORS:
        assert not (ROOT / obsolete_path).exists(), f"obsolete optical validator path unexpectedly exists: {obsolete_path}"
    for workflow_name in OPTICAL_VALIDATOR_WORKFLOWS:
        text = (WORKFLOWS / workflow_name).read_text(encoding="utf-8")
        assert CANONICAL_OPTICAL_VALIDATOR in text, f"{workflow_name} does not reference the canonical optical validator path"
        for obsolete_path in OBSOLETE_OPTICAL_VALIDATORS:
            assert obsolete_path not in text, f"{workflow_name} still references obsolete optical validator path: {obsolete_path}"


def assert_documented_boundary() -> None:
    text = DOCUMENTATION.read_text(encoding="utf-8")
    for phrase in (
        "A SHA-256 digest proves which evidence bytes a record names. It does **not** make the remaining locator safe to retain.",
        "Retrieval credentials, signed URLs, bearer material, cookies, provider tokens, temporary access grants, and equivalent secrets belong outside the retained qualification record.",
        "Stable V1.3 / `1.3.0` remains the consumer target",
    ):
        assert phrase in text, f"evidence-reference privacy documentation missing governing boundary: {phrase}"


def main() -> None:
    compiled = re.compile(EXPECTED_PATTERN)
    digest = "a" * 64

    for name, path in EVALUATORS.items():
        module = load_module(name, path)
        candidate = getattr(module, "EVIDENCE_REFERENCE", None)
        assert candidate is not None, f"{name} evaluator missing EVIDENCE_REFERENCE"
        assert candidate.pattern == EXPECTED_PATTERN, f"{name} evaluator evidence-reference grammar drifted"

    for locator in SAFE_LOCATORS:
        reference = f"evidence+sha256:{digest}:{locator}"
        assert compiled.fullmatch(reference), f"safe logical locator was rejected: {locator}"

    for locator in UNSAFE_LOCATORS:
        reference = f"evidence+sha256:{digest}:{locator}"
        assert compiled.fullmatch(reference) is None, f"unsafe credential-bearing locator was accepted: {locator}"

    assert_schema_patterns()
    assert_workflow_applicability()
    assert_optical_validator_path_integrity()
    assert_documented_boundary()
    print("Glaze V1.4 evidence-reference privacy boundary validated across performance, parity, accessibility, compatibility, Stable authority, and optical-validator workflow integrity.")


if __name__ == "__main__":
    main()
