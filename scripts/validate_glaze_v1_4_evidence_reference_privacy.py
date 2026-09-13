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
    print("Glaze V1.4 evidence-reference privacy boundary validated across performance, parity, and accessibility.")


if __name__ == "__main__":
    main()
