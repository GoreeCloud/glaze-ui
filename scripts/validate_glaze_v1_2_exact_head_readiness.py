#!/usr/bin/env python3
"""Fail-closed exact-head readiness reporting for GLAZE UI V1.2 Candidate."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/glaze-v1.2-exact-head-readiness.json"
CONTRACT = ROOT / "contracts/v1.2/exact-head-readiness.candidate.json"
VERSION = ROOT / "VERSION"
LIFECYCLE = ROOT / "registry/lifecycle.json"
MIGRATION = ROOT / "contracts/v1.2/migration.candidate.json"
REFERENCE_SCENES = ROOT / "contracts/v1.2/reference-scenes.candidate.json"
ACCESSIBILITY = ROOT / "contracts/v1.2/accessibility-testing.candidate.json"
PERFORMANCE = ROOT / "contracts/v1.2/performance-testing.candidate.json"
VISUAL = ROOT / "contracts/v1.2/visual-regression.candidate.json"
PERFORMANCE_BUDGET = ROOT / "contracts/performance/glaze-v1-performance-budget.json"
V11_CONFORMANCE_SCHEMA = ROOT / "contracts/glaze.conformance-evidence.schema.json"
PROMOTION_GATES = ROOT / "acceptance/v1.2-promotion-gates.candidate.md"
WORKFLOW = ROOT / ".github/workflows/glaze-v1.2-exact-head-readiness.yml"
EXPECTED_GATES = [f"G{i}" for i in range(8)]


class ReadinessError(RuntimeError):
    pass


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ReadinessError(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"expected object in {path.relative_to(ROOT)}")
    return value


def head_revision() -> str:
    value = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    require(re.fullmatch(r"[0-9a-f]{40}", value) is not None, f"invalid Git HEAD revision: {value!r}")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_digests(paths: list[Path]) -> dict[str, str]:
    return {str(path.relative_to(ROOT)): sha256(path) for path in paths}


def release(lifecycle: dict[str, Any], version: str) -> dict[str, Any]:
    matches = [item for item in lifecycle.get("releases", []) if isinstance(item, dict) and item.get("version") == version]
    require(len(matches) == 1, f"lifecycle release entry missing/ambiguous for {version}")
    return matches[0]


def validate_source() -> tuple[dict[str, Any], dict[str, Any]]:
    paths = [
        CONTRACT, VERSION, LIFECYCLE, MIGRATION, REFERENCE_SCENES, ACCESSIBILITY,
        PERFORMANCE, VISUAL, PERFORMANCE_BUDGET, V11_CONFORMANCE_SCHEMA,
        PROMOTION_GATES, WORKFLOW,
    ]
    for path in paths:
        require(path.is_file(), f"missing {path.relative_to(ROOT)}")

    contract = load_json(CONTRACT)
    lifecycle = load_json(LIFECYCLE)
    migration = load_json(MIGRATION)
    scenes = load_json(REFERENCE_SCENES)
    accessibility = load_json(ACCESSIBILITY)
    performance = load_json(PERFORMANCE)
    visual = load_json(VISUAL)
    budget = load_json(PERFORMANCE_BUDGET)
    v11_schema = load_json(V11_CONFORMANCE_SCHEMA)

    require(contract.get("version") == "1.2.0-candidate", "readiness contract version drifted")
    require(contract.get("lifecycle") == "candidate" and contract.get("stableBaseline") == "1.1.0", "readiness lifecycle boundary drifted")
    require(contract.get("consumerEligible") is False and contract.get("reportKind") == "candidate-readiness-not-conformance", "readiness report overclaimed conformance")
    require(contract.get("gateOrder") == EXPECTED_GATES, "readiness gate order drifted")
    require(contract.get("runtimeRevisionBinding", {}).get("source") == "git rev-parse HEAD", "readiness runtime revision binding drifted")
    require(contract.get("runtimeRevisionBinding", {}).get("exactHeadRequired") is True, "exact-head binding is no longer required")
    require(contract.get("runtimeRevisionBinding", {}).get("staticSourceRevisionInContractProhibited") is True, "static revision prohibition drifted")
    require(re.search(r"\b[0-9a-f]{40}\b", CONTRACT.read_text(encoding="utf-8")) is None, "readiness contract must not embed a self-referential static Git revision")

    claims = contract.get("requiredOutputClaims", {})
    require(claims == {
        "promotionReady": False,
        "rcReady": False,
        "stableReady": False,
        "productionReady": False,
        "consumerEligible": False,
        "consumerConformanceClaim": False,
        "reportStatus": "fail-closed-blocked",
    }, "required fail-closed output claims drifted")

    rules = contract.get("rules", {})
    for key in (
        "exactRevisionRequired", "evidenceCategoriesRemainIndependent",
        "automatedChecksMayNotSubstituteHumanOpticalReview",
        "browserAccessibilityEvidenceMayNotSubstituteRealAssistiveTechnologyAcceptance",
        "browserPerformanceObservationsMayNotSubstituteAcceptedProductionBudgets",
        "emulatorEvidenceMayNotSubstitutePhysicalDeviceAcceptance",
        "v11ConformanceSchemaMustRemainV11Only", "consumerClaimBlocked",
    ):
        require(rules.get(key) is True, f"readiness safety rule drifted: {key}")
    for key in (
        "candidateReadinessReportIsConsumerConformance",
        "candidateReadinessReportIsReleaseCandidateAcceptance",
        "candidateReadinessReportIsStableAcceptance",
        "greenReadinessWorkflowMayAutoPromote",
    ):
        require(rules.get(key) is False, f"readiness overclaim prohibition drifted: {key}")

    gate_reporting = contract.get("gateReporting", {})
    require(list(gate_reporting.keys()) == EXPECTED_GATES, "readiness gate reporting order drifted")
    require([gate_reporting[g].get("status") for g in EXPECTED_GATES] == [
        "bounded-evidence-present", "bounded-evidence-present", "bounded-evidence-present",
        "blocked", "blocked", "blocked", "not-eligible", "not-eligible",
    ], "readiness gate statuses must remain fail closed")

    require(VERSION.read_text(encoding="utf-8").strip() == "1.1.0", "VERSION moved away from Stable 1.1.0")
    require(lifecycle.get("currentOfficial") == "1.1.0" and lifecycle.get("currentStable") == "1.1.0", "lifecycle Stable authority moved")
    require(lifecycle.get("activeCandidate") == "1.2.0-candidate", "active Candidate identity drifted")
    stable = release(lifecycle, "1.1.0")
    candidate = release(lifecycle, "1.2.0-candidate")
    require(stable.get("status") == "stable" and stable.get("consumerEligible") is True, "V1.1 Stable release authority drifted")
    require(candidate.get("status") == "candidate" and candidate.get("consumerEligible") is False and candidate.get("stableBaseline") == "1.1.0", "V1.2 Candidate isolation drifted")

    stable_baseline = migration.get("stableBaseline", {})
    target = migration.get("target", {})
    governance = migration.get("governance", {})
    require(stable_baseline.get("version") == "1.1.0" and stable_baseline.get("consumerEligible") is True, "migration Stable baseline drifted")
    require(target.get("version") == "1.2.0-candidate" and target.get("consumerEligible") is False and target.get("optInOnly") is True, "migration Candidate boundary drifted")
    require(target.get("stablePromotionRequiredBeforeProductionMigration") is True, "production migration no longer requires Stable promotion")
    require(governance.get("exactHeadValidationRequired") is True and governance.get("stableAuthorityMayNotMoveInThisChangeSet") is True and governance.get("versionFileMayNotChangeInThisChangeSet") is True and governance.get("downstreamConformanceClaimsAllowed") is False, "migration governance boundary drifted")
    migration_gates = migration.get("acceptanceGates", [])
    require([item.get("id") for item in migration_gates] == EXPECTED_GATES and all(item.get("blocking") is True for item in migration_gates), "migration G0-G7 blocking order drifted")

    require(scenes.get("version") == "1.2.0-candidate" and scenes.get("consumerEligible") is False, "Reference Scenes Candidate boundary drifted")
    require(scenes.get("requiredSceneCount") == 16 and scenes.get("boundedEstablishedCount") == 15, "Reference Scene accounting drifted")
    require(scenes.get("phase5ReferenceScenesComplete") is False and scenes.get("openSceneIds") == ["application-icon-ecosystem-wall"], "Reference Scenes must remain fail closed while Ecosystem Wall is open")

    access_boundary = accessibility.get("evidenceBoundary", {})
    require(accessibility.get("consumerEligible") is False and accessibility.get("rules", {}).get("consumerClaimBlocked") is True, "Accessibility Testing consumer boundary drifted")
    require(access_boundary.get("boundedAutomatedAccessibilityTestingEstablished") is True and access_boundary.get("phase5AccessibilityTestingComplete") is False, "Accessibility Testing completion boundary drifted")
    access_missing = set(access_boundary.get("notEstablished", []))
    require({"screen-reader-acceptance", "talkback-acceptance", "voiceover-acceptance", "physical-device-accessibility-acceptance", "complete-native-platform-accessibility-parity"}.issubset(access_missing), "Accessibility Testing blockers were promoted away")

    perf_boundary = performance.get("evidenceBoundary", {})
    require(performance.get("consumerEligible") is False and performance.get("rules", {}).get("consumerClaimBlocked") is True, "Performance Testing consumer boundary drifted")
    require(perf_boundary.get("boundedBrowserCiMeasurementsEstablished") is True and perf_boundary.get("phase5PerformanceTestingComplete") is False, "Performance Testing completion boundary drifted")
    perf_missing = set(perf_boundary.get("notEstablished", []))
    require({"accepted-numeric-runtime-budget", "accepted-platform-performance-budget", "physical-device-performance-acceptance", "production-performance-acceptance", "complete-native-platform-performance-parity"}.issubset(perf_missing), "Performance Testing blockers were promoted away")
    require(budget.get("status") == "revalidation-required", "canonical performance budget no longer requires revalidation")
    require("must be regenerated and accepted against exact V1 revisions" in budget.get("note", ""), "performance budget regeneration requirement drifted")

    provisional = visual.get("provisionalReference", {})
    comparison = visual.get("comparison", {})
    visual_boundaries = visual.get("boundaries", {})
    require(provisional.get("humanApproved") is False and provisional.get("canonicalScreenshotBaseline") is False and provisional.get("acceptanceAuthority") is False, "provisional visual reference gained authority")
    require(comparison.get("pixelDifferenceAloneIsHumanAcceptanceAuthority") is False and comparison.get("humanOpticalReviewRemainsAuthoritative") is True, "human optical authority drifted")
    require(visual_boundaries.get("provisionalReferenceCountsAsReleaseAcceptance") is False and visual_boundaries.get("automatedRegressionReplacesHumanReview") is False and visual_boundaries.get("referenceScenesComplete") is False and visual_boundaries.get("consumerClaimBlocked") is True, "visual-regression fail-closed boundary drifted")

    require(v11_schema.get("title") == "GLAZE UI V1.1 Conformance Evidence Record", "Stable conformance schema identity drifted")
    version_const = v11_schema.get("properties", {}).get("target", {}).get("properties", {}).get("glaze_version", {}).get("const")
    require(version_const == "1.1.0", "V1.1 conformance schema was broadened to a Candidate")

    promotion = PROMOTION_GATES.read_text(encoding="utf-8")
    for marker in ("G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "human", "native"):
        require(marker.lower() in promotion.lower(), f"promotion-gate authority marker missing: {marker}")

    implementation = contract.get("implementation", {})
    require(implementation == {
        "validator": "scripts/validate_glaze_v1_2_exact_head_readiness.py",
        "workflow": ".github/workflows/glaze-v1.2-exact-head-readiness.yml",
        "artifact": "artifacts/glaze-v1.2-exact-head-readiness.json",
    }, "readiness implementation bindings drifted")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    require("validate_glaze_v1_2_exact_head_readiness.py" in workflow_text and "github.event.pull_request.head.sha || github.sha" in workflow_text, "readiness workflow exact-head binding drifted")

    boundary = contract.get("evidenceBoundary", {})
    require(boundary.get("boundedExactHeadReadinessReportingEstablished") is True and boundary.get("phase5ExactRevisionConformanceEvidenceComplete") is False, "readiness evidence boundary overclaimed Phase 5 completion")

    return contract, {
        "lifecycle": lifecycle,
        "migration": migration,
        "referenceScenes": scenes,
        "accessibility": accessibility,
        "performance": performance,
        "visualRegression": visual,
        "performanceBudget": budget,
        "v11ConformanceSchema": v11_schema,
        "sourcePaths": paths,
    }


def build_report(contract: dict[str, Any], sources: dict[str, Any]) -> dict[str, Any]:
    revision = head_revision()
    lifecycle = sources["lifecycle"]
    scenes = sources["referenceScenes"]
    accessibility = sources["accessibility"]
    performance = sources["performance"]
    visual = sources["visualRegression"]
    budget = sources["performanceBudget"]
    claims = dict(contract["requiredOutputClaims"])

    blockers = [
        {
            "id": "reference-scenes-incomplete",
            "gate": "G3",
            "evidence": {
                "required": scenes["requiredSceneCount"],
                "boundedEstablished": scenes["boundedEstablishedCount"],
                "openSceneIds": scenes["openSceneIds"],
            },
        },
        {
            "id": "human-visual-acceptance-incomplete",
            "gate": "G3",
            "evidence": {
                "provisionalHumanApproved": visual["provisionalReference"]["humanApproved"],
                "canonicalScreenshotBaseline": visual["provisionalReference"]["canonicalScreenshotBaseline"],
                "humanOpticalReviewAuthoritative": visual["comparison"]["humanOpticalReviewRemainsAuthoritative"],
            },
        },
        {
            "id": "assistive-technology-and-physical-accessibility-incomplete",
            "gate": "G4",
            "evidence": {
                "phase5AccessibilityTestingComplete": accessibility["evidenceBoundary"]["phase5AccessibilityTestingComplete"],
                "notEstablished": accessibility["evidenceBoundary"]["notEstablished"],
            },
        },
        {
            "id": "production-performance-evidence-incomplete",
            "gate": "G4",
            "evidence": {
                "performanceBudgetStatus": budget["status"],
                "phase5PerformanceTestingComplete": performance["evidenceBoundary"]["phase5PerformanceTestingComplete"],
                "notEstablished": performance["evidenceBoundary"]["notEstablished"],
            },
        },
        {
            "id": "rc-exact-head-acceptance-incomplete",
            "gate": "G5",
            "evidence": {
                "dependsOn": ["G3", "G4"],
                "humanOpticalReviewApprovedForExactCandidate": False,
                "completeSupportedPlatformEvidenceEstablished": False,
                "governedRcLifecycleActionRecorded": False,
            },
        },
    ]

    return {
        "schemaVersion": 1,
        "reportKind": contract["reportKind"],
        "sourceRevision": revision,
        "observedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "product": contract["product"],
        "candidateVersion": contract["version"],
        "stableBaseline": contract["stableBaseline"],
        **claims,
        "lifecycleSnapshot": {
            "currentOfficial": lifecycle["currentOfficial"],
            "currentStable": lifecycle["currentStable"],
            "activeCandidate": lifecycle["activeCandidate"],
            "candidateStatus": release(lifecycle, "1.2.0-candidate")["status"],
            "candidateConsumerEligible": release(lifecycle, "1.2.0-candidate")["consumerEligible"],
        },
        "gateOrder": contract["gateOrder"],
        "gates": [
            {"id": gate_id, **contract["gateReporting"][gate_id]}
            for gate_id in contract["gateOrder"]
        ],
        "blockers": blockers,
        "v11ConformanceSchemaIsolation": {
            "title": sources["v11ConformanceSchema"]["title"],
            "glazeVersionConst": sources["v11ConformanceSchema"]["properties"]["target"]["properties"]["glaze_version"]["const"],
            "usedForV12CandidateClaim": False,
        },
        "sourceDigestsSha256": source_digests(sources["sourcePaths"]),
        "evidenceBoundary": contract["evidenceBoundary"],
    }


def validate_report(report: dict[str, Any], contract: dict[str, Any]) -> None:
    require(re.fullmatch(r"[0-9a-f]{40}", str(report.get("sourceRevision", ""))) is not None, "report lacks exact 40-character source revision")
    require(report.get("sourceRevision") == head_revision(), "report source revision does not match checked-out HEAD")
    for key, expected in contract["requiredOutputClaims"].items():
        require(report.get(key) == expected, f"report overclaimed {key}: {report.get(key)!r}")
    require(report.get("gateOrder") == EXPECTED_GATES, "report gate order drifted")
    gates = report.get("gates", [])
    require([gate.get("id") for gate in gates] == EXPECTED_GATES, "report gate list drifted")
    require([gate.get("status") for gate in gates] == [
        "bounded-evidence-present", "bounded-evidence-present", "bounded-evidence-present",
        "blocked", "blocked", "blocked", "not-eligible", "not-eligible",
    ], "report gate statuses are not fail closed")
    require(len(report.get("blockers", [])) >= 5, "readiness report lost required blocker classes")
    isolation = report.get("v11ConformanceSchemaIsolation", {})
    require(isolation.get("glazeVersionConst") == "1.1.0" and isolation.get("usedForV12CandidateClaim") is False, "V1.1 conformance schema isolation failed")


def main() -> int:
    try:
        contract, sources = validate_source()
        report = build_report(contract, sources)
        validate_report(report, contract)
        ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
        ARTIFACT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        require(ARTIFACT.stat().st_size > 1000, "readiness artifact unexpectedly small")
        print(f"PASS: GLAZE UI V1.2 exact-head readiness report is fail-closed at {report['sourceRevision']}; RC/Stable/production/consumer readiness remain false.")
        return 0
    except Exception as error:
        print(f"GLAZE UI V1.2 exact-head readiness validation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
