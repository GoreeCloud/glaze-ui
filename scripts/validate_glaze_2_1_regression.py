#!/usr/bin/env python3
"""Fail-closed structural validation for Glaze UI 2.1 Candidate visual/interaction regression."""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
BASELINE_REVISION = "609dc8e9e76c8e0fe306bb46961e1242bcdad86f"
ARTIFACT_DIGEST = "sha256:9b1ed13f4c18da681cdf2a5d6e5224499e65d76d76b581e5b078fa3a498d0d52"
EXPECTED_HASHES = {
    "settings-desktop-light": "8b836ed117528d5468db1786783ae697e27f52b74389647b92064eda51c18f22",
    "files-mobile-reduced-transparency": "b152219d444c1bd77971abeba38fa5b43cf0d3f1a31efddf2c8652381a8c01d7",
    "search-command-open-deep-dark": "7931c1d2b2ee09290fb2838cddeba7e9f55839c257e46ac04301f77beef88097",
    "communication-tablet-sent-large-text": "403a840c6b8f5607a5523fbdc5cd4cbb5ad212396531ad9a042aec530c00fb4b",
    "media-tv-playing": "b49b592640f2e236e25a18eb24e3c1d40d379445159f95423fbf87c13bdc6717",
    "resilience-desktop-light": "301c71c828d597fb2a36c4d6210ec5e224c2e04263bd75248f92ef176faf9ed7",
}


def fail(message: str) -> None:
    ERRORS.append(message)


def read_text(path: str) -> str:
    target = ROOT / path
    if not target.is_file():
        fail(f"missing required file: {path}")
        return ""
    return target.read_text(encoding="utf-8")


def read_json(path: str) -> dict:
    raw = read_text(path)
    if not raw:
        return {}
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path}: {exc}")
        return {}
    if not isinstance(value, dict):
        fail(f"top level must be an object: {path}")
        return {}
    return value


def main() -> int:
    if read_text("VERSION").strip() != "2.0.0":
        fail("Glaze UI 2.1 Candidate regression must not change Stable VERSION from 2.0.0")

    contract = read_json("contracts/regression/reference-invariants.json")
    manifest = read_json("contracts/regression/visual-baselines.json")
    registry = read_json("registry/lifecycle.json")
    workflow = read_text(".github/workflows/glaze-2.1-candidate.yml")
    css = read_text("css/glaze-2.1.expanded-reference.css")
    base_css = read_text("css/glaze-2.1.reference.css")
    resilience_css = read_text("css/glaze-2.1.resilience-reference.css")
    snapshot = read_text("reference/candidate-2.1-snapshot.html")
    visual_script = read_text("scripts/glaze_2_1_visual_regression.py")

    if contract.get("lifecycle") != "candidate": fail("reference regression contract must remain Candidate")
    if contract.get("scope") != "computed-layout-style-and-interaction-invariants": fail("reference regression scope must remain computed layout/style/interaction invariants")
    if contract.get("pixelBaselineStatus") != "source-pinned-candidate": fail("pixel baseline status must be source-pinned-candidate after exact baseline promotion")

    expected = {
        "settings-preferences": ("reference/candidate-2.1-settings.html", "productivity"),
        "file-management": ("reference/candidate-2.1-files.html", "productivity"),
        "search-command": ("reference/candidate-2.1-search.html", "productivity"),
        "communication-live-activity": ("reference/candidate-2.1-communication.html", "communication"),
        "media-playback": ("reference/candidate-2.1-media.html", "media"),
        "resilience-exception-states": ("reference/candidate-2.1-resilience.html", "administration"),
    }
    flows = contract.get("flows", {})
    combined = ""
    if set(flows) != set(expected): fail(f"regression contract flow set must be exactly {sorted(expected)}")
    for marker, (path, recipe) in expected.items():
        record = flows.get(marker, {})
        if record.get("path") != path: fail(f"{marker} path must be {path}")
        if record.get("recipe") != recipe: fail(f"{marker} recipe must be {recipe}")
        baseline = record.get("visualBaseline")
        if not isinstance(baseline, str) or not baseline.endswith("-v1"): fail(f"{marker} must define a v1 visual baseline identifier")
        page = read_text(path); combined += "\n" + page
        if f'data-reference-flow="{marker}"' not in page: fail(f"{path} missing canonical flow marker {marker}")
        if marker in {"search-command", "communication-live-activity", "media-playback", "resilience-exception-states"}:
            if f'data-visual-baseline="{baseline}"' not in page: fail(f"{path} missing declared visual baseline {baseline}")
            if "measureVisibleMaterialBudget" not in page or "applyReferenceRuntime" not in page: fail(f"{path} must execute shared 2.1 runtime and Material Budget")
        for state in record.get("requiredStates", []):
            if f'data-regression-state="{state}"' not in page: fail(f"{path} missing required regression state {state}")

    required_states = {"default","hover","focus","pressed","selected","disabled","loading","sending","success","warning","error","offline","protected","restricted","empty","unavailable","conflict","expired","destructive","degraded"}
    vocabulary = set(contract.get("stateVocabulary", []))
    if not required_states.issubset(vocabulary): fail(f"state vocabulary missing {sorted(required_states - vocabulary)}")
    for state in ("loading","sending","success","warning","error","offline","protected","restricted","empty","unavailable","conflict","expired","destructive","degraded"):
        if f'data-regression-state="{state}"' not in combined: fail(f"expanded reference flows do not visibly exercise state {state}")

    for selector in (":hover",":focus-visible",":active",":disabled",'[aria-current="page"]','[aria-pressed="true"]'):
        if selector not in css and selector not in base_css: fail(f"reference CSS missing state selector {selector}")
    for marker in (".exception-grid",'data-regression-state="conflict"','data-regression-state="destructive"',"@media(forced-colors:active)"):
        if marker not in resilience_css: fail(f"resilience CSS missing marker: {marker}")

    scenarios = contract.get("interactionScenarios", [])
    scenario_map = {item.get("id"): item for item in scenarios if isinstance(item, dict)}
    expected_scenarios = {"command-open-select":"search-command","message-send":"communication-live-activity","playback-toggle":"media-playback"}
    if set(scenario_map) != set(expected_scenarios): fail(f"interaction scenarios must remain exactly {sorted(expected_scenarios)}")
    for scenario, flow in expected_scenarios.items():
        record = scenario_map.get(scenario, {})
        if record.get("flow") != flow: fail(f"{scenario} must target {flow}")
        if not isinstance(record.get("trigger"), str) or not record.get("trigger"): fail(f"{scenario} must declare a trigger selector")
    if not isinstance(contract.get("visualInvariants"), list) or len(contract.get("visualInvariants", [])) < 11: fail("reference regression contract must define at least eleven visual invariants")

    capabilities = registry.get("capabilities", {})
    reference = capabilities.get("canonical-reference-flows-2.1", {})
    coverage = set(reference.get("coverage", [])); implementations = set(reference.get("implementations", []))
    if not set(expected).issubset(coverage): fail(f"lifecycle registry reference-flow coverage missing {sorted(set(expected) - coverage)}")
    for path, _ in expected.values():
        if path not in implementations: fail(f"lifecycle registry missing reference implementation {path}")

    expanded = capabilities.get("expanded-acceptance-matrix-2.1", {}); interaction = capabilities.get("interaction-regression-2.1", {}); visual = capabilities.get("rendered-visual-invariant-regression-2.1", {}); pixel = capabilities.get("visual-regression-2.1", {})
    if expanded.get("status") != "candidate" or expanded.get("implementation") != "contracts/regression/reference-invariants.json": fail("expanded acceptance matrix must remain Candidate and point to regression contract")
    if expanded.get("resilienceAcceptance") != "scripts/validate_glaze_2_1_resilience_rendered.py": fail("expanded acceptance matrix must point to resilience rendered acceptance")
    if interaction.get("status") != "candidate" or interaction.get("implementation") != "reference/candidate-2.1-expanded-acceptance.html": fail("interaction regression must remain Candidate and point to expanded rendered harness")
    if visual.get("status") != "candidate" or visual.get("implementation") != "contracts/regression/reference-invariants.json": fail("rendered visual-invariant regression must remain Candidate")
    if visual.get("resilienceAcceptance") != "scripts/validate_glaze_2_1_resilience_rendered.py": fail("rendered visual-invariant regression must point to resilience acceptance")

    if pixel.get("status") != "candidate": fail("screenshot visual regression must be Candidate after source-pinned comparison is implemented")
    expected_pixel = {"manifest":"contracts/regression/visual-baselines.json","implementation":"scripts/glaze_2_1_visual_regression.py","snapshotHarness":"reference/candidate-2.1-snapshot.html","baselineStrategy":"source-revision-same-run-render","baselineRevision":BASELINE_REVISION}
    for key, value in expected_pixel.items():
        if pixel.get(key) != value: fail(f"visual-regression-2.1 {key} must be {value}")
    if pixel.get("baselineCaseCount") != 6: fail("visual-regression-2.1 baselineCaseCount must be 6")

    if manifest.get("lifecycle") != "candidate" or manifest.get("status") != "source-pinned-candidate": fail("visual baseline manifest must be Candidate/source-pinned-candidate")
    if manifest.get("baselineStrategy") != "source-revision-same-run-render": fail("visual baseline strategy must be source-revision-same-run-render")
    if manifest.get("baselineRevision") != BASELINE_REVISION: fail(f"visual baseline revision must be {BASELINE_REVISION}")
    provenance = manifest.get("captureProvenance", {})
    if provenance.get("workflowRunId") != 33326116037 or provenance.get("artifactId") != 9736279015: fail("visual baseline capture provenance run/artifact identity changed")
    if provenance.get("artifactDigest") != ARTIFACT_DIGEST: fail("visual baseline capture provenance artifact digest changed")
    if "not human Visual Excellence acceptance" not in str(provenance.get("note", "")): fail("visual baseline provenance must explicitly keep human Visual Excellence separate")

    thresholds = manifest.get("thresholds", {})
    if not isinstance(thresholds.get("perChannelTolerance"), int) or not 0 <= thresholds.get("perChannelTolerance", -1) <= 32: fail("visual per-channel tolerance must be an integer from 0 to 32")
    if not isinstance(thresholds.get("maxChangedPixelRatio"), (int,float)) or not 0 < thresholds.get("maxChangedPixelRatio", 0) <= 0.02: fail("visual changed-pixel ratio must be >0 and <=2%")
    if not isinstance(thresholds.get("maxMeanAbsoluteChannelDelta"), (int,float)) or not 0 < thresholds.get("maxMeanAbsoluteChannelDelta", 0) <= 4: fail("visual mean channel delta must be >0 and <=4")

    cases = manifest.get("cases", []); case_map = {case.get("id"): case for case in cases if isinstance(case, dict)}
    if set(case_map) != set(EXPECTED_HASHES): fail(f"visual baseline manifest case set must be exactly {sorted(EXPECTED_HASHES)}")
    for case_id, expected_hash in EXPECTED_HASHES.items():
        case = case_map.get(case_id, {})
        if case.get("flow") not in {"settings","files","search","communication","media","resilience"}: fail(f"visual case {case_id} has invalid flow")
        if not isinstance(case.get("width"), int) or not isinstance(case.get("height"), int) or case.get("width", 0) < 320 or case.get("height", 0) < 640: fail(f"visual case {case_id} has invalid viewport")
        if case.get("baselineFile") != f"{case_id}.png": fail(f"visual case {case_id} baselineFile must be {case_id}.png")
        capture_hash = case.get("captureArtifactSha256")
        if capture_hash != expected_hash or not re.fullmatch(r"[0-9a-f]{64}", str(capture_hash)): fail(f"visual case {case_id} capture artifact hash changed")
        if not (ROOT / str(case.get("path", ""))).is_file(): fail(f"visual case {case_id} target path is missing: {case.get('path')}")

    for marker in ('data-snapshot-ready="pending"',"command-open","message-sent","playing","candidate-2.1-resilience.html"):
        if marker not in snapshot: fail(f"snapshot harness missing marker: {marker}")
    for marker in ("decode_png","compare_case","--force-device-scale-factor=1",'data-snapshot-ready="true"',"--baseline-dir"):
        if marker not in visual_script: fail(f"visual regression script missing marker: {marker}")
    if 'choices=("capture", "compare")' not in visual_script: fail("visual regression script must preserve separate capture and compare modes")
    if "compare mode requires --baseline-dir" not in visual_script: fail("visual regression compare mode must fail closed without an external baseline directory")

    workflow_markers = ("scripts/validate_glaze_2_1_regression.py","scripts/validate_glaze_2_1_expanded_rendered.py","scripts/validate_glaze_2_1_resilience_rendered.py","scripts/glaze_2_1_visual_regression.py",f"ref: {BASELINE_REVISION}","path: .glaze-2.1-visual-baseline-source","Render pinned Glaze UI 2.1 visual baseline source","compare --baseline-dir .artifacts/glaze-2.1-visual-baseline-reference","actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02")
    for marker in workflow_markers:
        if marker not in workflow: fail(f"2.1 workflow missing source-pinned regression marker: {marker}")
    if "Capture Glaze UI 2.1 visual baseline candidates" in workflow: fail("normal Candidate CI must not retain capture-only screenshot acceptance after source-pinned promotion")

    if "reference/candidate-2.1-expanded-acceptance.html" not in read_text("scripts/validate_glaze_2_1_expanded_rendered.py"): fail("expanded rendered validator must invoke expanded acceptance harness")
    if "reference/candidate-2.1-resilience-acceptance.html" not in read_text("scripts/validate_glaze_2_1_resilience_rendered.py"): fail("resilience validator must invoke resilience acceptance harness")

    if ERRORS:
        print("Glaze UI 2.1 source-pinned regression validation FAILED", file=sys.stderr)
        for error in ERRORS: print(f"- {error}", file=sys.stderr)
        return 1
    print("Glaze UI 2.1 source-pinned screenshot + interaction regression structure passed; Stable remains 2.0.0")
    print(f"Candidate screenshot baseline source revision: {BASELINE_REVISION}")
    print("Human Visual Excellence, native/device acceptance and Stable promotion remain separately gated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
