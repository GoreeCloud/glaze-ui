#!/usr/bin/env python3
"""Prepare one exact-source review bundle for the seven open Glaze UI V1.6 lanes.

The bundle combines the existing Human, Assistive Technology, and Performance
qualification surfaces under one root. It copies only fail-closed evidence
templates and never creates accepted evidence or lifecycle authority.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

SOURCE_REVISION = "c7509c79256b04b0aa67cb9dd0737d7588e0ae4a"
ACCEPTANCE_MODEL = "1.6.0-dev.12"
STABLE_BASELINE = "1.5.1"
EXPECTED_BLOCKERS = [
    "accessibility",
    "keyboard-navigation",
    "assistive-technology",
    "performance",
    "privacy-boundaries",
    "authority-boundaries",
    "representative-rendering",
]
SENTINEL = ".glaze-v1.6-remaining-qualification-root"

SESSIONS = [
    {
        "id": "human",
        "plan": "contracts/v1.6/qualification.human.plan.json",
        "preparer": "scripts/prepare_glaze_v1_6_human_qualification.py",
        "entrypoint": "reference/v1.6/human-qualification.html",
        "template": "acceptance/v1.6-human-evidence.template.json",
        "governedDestination": "acceptance/v1.6-human-evidence.json",
        "evidenceType": "human",
    },
    {
        "id": "assistive-technology",
        "plan": "contracts/v1.6/qualification.assistive-technology.plan.json",
        "preparer": "scripts/prepare_glaze_v1_6_assistive_technology_qualification.py",
        "entrypoint": "reference/v1.6/assistive-technology-qualification.html",
        "template": "acceptance/v1.6-assistive-technology-evidence.template.json",
        "governedDestination": "acceptance/v1.6-assistive-technology-evidence.json",
        "evidenceType": "assistive-technology",
    },
    {
        "id": "performance",
        "plan": "contracts/v1.6/qualification.performance.plan.json",
        "preparer": "scripts/prepare_glaze_v1_6_performance_qualification.py",
        "entrypoint": "reference/v1.6/performance-qualification.html",
        "template": "acceptance/v1.6-performance-evidence.template.json",
        "governedDestination": "acceptance/v1.6-performance-evidence.json",
        "evidenceType": "performance",
    },
]


class QualificationBundleError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise QualificationBundleError(message)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise QualificationBundleError(f"unable to read JSON {path}: {error}") from error


def run(root: Path, *args: str) -> str:
    result = subprocess.run(
        list(args),
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise QualificationBundleError(
            "command failed: " + " ".join(args) + (f"\n{detail}" if detail else "")
        )
    return result.stdout.strip()


def validate_template(path: Path, evidence_type: str) -> None:
    record = load_json(path)
    require(record.get("sourceRevision") == SOURCE_REVISION, f"{path.name} source revision mismatch")
    require(record.get("acceptanceModelVersion") == ACCEPTANCE_MODEL, f"{path.name} acceptance model mismatch")
    require(record.get("stableBaseline") == STABLE_BASELINE, f"{path.name} Stable baseline mismatch")
    require(record.get("reviewDecision") == "not-accepted", f"{path.name} must remain not-accepted")
    lane_evidence = record.get("laneEvidence")
    require(isinstance(lane_evidence, list) and lane_evidence, f"{path.name} laneEvidence missing")
    require(all(item.get("verified") is False for item in lane_evidence), f"{path.name} must not verify lanes")
    require(all(item.get("evidenceType") == evidence_type for item in lane_evidence), f"{path.name} evidence type mismatch")
    authority = record.get("authority", {})
    require(authority.get("lifecyclePromotionAutomatic") is False, f"{path.name} must not promote lifecycle")
    require(authority.get("stableStatusGranted") is False, f"{path.name} must not grant Stable")


def verify_authority(repo_root: Path) -> tuple[dict, dict[str, dict]]:
    acceptance = load_json(repo_root / "contracts/v1.6/acceptance.dev.json")
    intake = load_json(repo_root / "contracts/v1.6/qualification-evidence-intake.json")

    require(acceptance.get("version") == ACCEPTANCE_MODEL, "V1.6 acceptance model drifted")
    require(acceptance.get("stableBaseline") == STABLE_BASELINE, "V1.6 Stable baseline drifted")
    require(acceptance.get("consumerEligible") is False, "V1.6 Development must remain non-consumer-eligible")

    disposition = intake.get("currentDispositionWithoutExternalEvidence", {})
    require(intake.get("sourceRevision") == SOURCE_REVISION, "evidence intake source revision drifted")
    require(intake.get("acceptanceModelVersion") == ACCEPTANCE_MODEL, "evidence intake model drifted")
    require(intake.get("stableBaseline") == STABLE_BASELINE, "evidence intake Stable baseline drifted")
    require(disposition.get("verifiedCount") == 17, "current verified lane count must remain 17")
    require(disposition.get("unverifiedCount") == 7, "current unverified lane count must remain 7")
    require(disposition.get("notApplicableCount") == 0, "current not-applicable lane count must remain 0")
    require(disposition.get("qualificationEvidenceComplete") is False, "qualification must remain incomplete")
    require(disposition.get("readyForGovernedQualificationReview") is False, "qualification must not be review-ready yet")
    require(disposition.get("blockingLaneIds") == EXPECTED_BLOCKERS, "seven-lane blocker set drifted")

    plans: dict[str, dict] = {}
    for session in SESSIONS:
        plan_path = repo_root / session["plan"]
        plan = load_json(plan_path)
        require(plan.get("sourceRevision") == SOURCE_REVISION, f"{session['id']} plan source mismatch")
        require(plan.get("acceptanceModelVersion") == ACCEPTANCE_MODEL, f"{session['id']} plan model mismatch")
        require(plan.get("stableBaseline") == STABLE_BASELINE, f"{session['id']} plan Stable baseline mismatch")
        require(plan.get("evidenceType") == session["evidenceType"], f"{session['id']} plan evidence type mismatch")
        scenarios = plan.get("requiredReviewScenarios") or plan.get("representativeCoverage")
        require(isinstance(scenarios, list) and scenarios, f"{session['id']} plan review coverage missing")
        plans[session["id"]] = plan

    human_lanes = plans["human"].get("lanes")
    require(
        human_lanes == [
            "accessibility",
            "keyboard-navigation",
            "privacy-boundaries",
            "authority-boundaries",
            "representative-rendering",
        ],
        "human review lane set drifted",
    )
    require(plans["assistive-technology"].get("laneId") == "assistive-technology", "assistive-technology lane drifted")
    require(
        plans["assistive-technology"].get("mayAlsoSatisfyAccessibilityAlternativeGroup") is True,
        "assistive-technology accessibility alternative boundary drifted",
    )
    require(plans["performance"].get("laneId") == "performance", "performance lane drifted")

    for session in SESSIONS:
        validate_template(repo_root / session["template"], session["evidenceType"])

    return intake, plans


def prepare(repo_root: Path, output: Path, replace: bool) -> dict:
    repo_root = repo_root.resolve()
    output = output.resolve()

    require((repo_root / ".git").exists(), "repo root must be a Git checkout")
    run(repo_root, "git", "cat-file", "-e", SOURCE_REVISION + "^{commit}")
    run(repo_root, "git", "merge-base", "--is-ancestor", SOURCE_REVISION, "HEAD")
    tooling_revision = run(repo_root, "git", "rev-parse", "HEAD")
    require(len(tooling_revision) == 40, "unable to resolve exact tooling revision")

    intake, plans = verify_authority(repo_root)

    if output.exists():
        if not replace:
            raise QualificationBundleError("output already exists; choose another path or pass --replace")
        require((output / SENTINEL).is_file(), "refusing to replace directory without qualification-bundle sentinel")
        shutil.rmtree(output)

    output.mkdir(parents=True)
    (output / SENTINEL).write_text("Glaze UI V1.6 remaining qualification review bundle\n", encoding="utf-8")
    records_dir = output / "records"
    records_dir.mkdir()

    session_records = []
    for session in SESSIONS:
        preparer = repo_root / session["preparer"]
        require(preparer.is_file(), f"missing preparer {session['preparer']}")
        session_root = output / session["id"]
        run(
            repo_root,
            sys.executable,
            str(preparer),
            "--repo-root",
            str(repo_root),
            "--out",
            str(session_root),
        )

        source_manifest = load_json(session_root / "qualification-source.json")
        require(source_manifest.get("sourceRevision") == SOURCE_REVISION, f"{session['id']} prepared source mismatch")
        require(source_manifest.get("acceptanceModelVersion") == ACCEPTANCE_MODEL, f"{session['id']} prepared model mismatch")
        require(source_manifest.get("stableBaseline") == STABLE_BASELINE, f"{session['id']} prepared Stable baseline mismatch")
        require(source_manifest.get("toolingRevision") == tooling_revision, f"{session['id']} tooling revision mismatch")

        entrypoint = session_root / session["entrypoint"]
        require(entrypoint.is_file(), f"{session['id']} review entrypoint missing")

        source_template = repo_root / session["template"]
        copied_template = records_dir / source_template.name
        shutil.copy2(source_template, copied_template)
        validate_template(copied_template, session["evidenceType"])

        plan = plans[session["id"]]
        lane_ids = plan.get("lanes") or [plan.get("laneId")]
        record = {
            "id": session["id"],
            "evidenceType": session["evidenceType"],
            "laneIds": lane_ids,
            "requiredReviewScenarios": plan.get("requiredReviewScenarios") or plan.get("representativeCoverage"),
            "reviewRoot": session["id"],
            "entrypoint": f"{session['id']}/{session['entrypoint']}",
            "workingTemplate": f"records/{copied_template.name}",
            "governedRecordDestination": session["governedDestination"],
            "acceptedEvidenceClaimed": False,
        }
        if session["id"] == "assistive-technology":
            record["mayAlsoSatisfyAccessibilityAlternativeGroup"] = True
        session_records.append(record)

    manifest = {
        "schemaVersion": 1,
        "recordType": "glaze-v1.6-remaining-qualification-session",
        "lifecycle": "DevelopmentQualification",
        "sourceRevision": SOURCE_REVISION,
        "toolingRevision": tooling_revision,
        "acceptanceModelVersion": ACCEPTANCE_MODEL,
        "stableBaseline": STABLE_BASELINE,
        "currentDisposition": {
            "verifiedCount": 17,
            "unverifiedCount": 7,
            "notApplicableCount": 0,
            "qualificationEvidenceComplete": False,
            "readyForGovernedQualificationReview": False,
            "blockingLaneIds": EXPECTED_BLOCKERS,
        },
        "sessions": session_records,
        "authority": {
            "bundleIsEvidence": False,
            "humanEvidenceClaimed": False,
            "assistiveTechnologyEvidenceClaimed": False,
            "performanceEvidenceClaimed": False,
            "physicalDeviceEvidenceClaimed": False,
            "qualificationCompletionClaimed": False,
            "lifecyclePromotionAutomatic": False,
            "candidateStatusGranted": False,
            "releaseCandidateStatusGranted": False,
            "stableStatusGranted": False,
            "consumerAcceptanceAutomatic": False,
            "deploymentAcceptanceAutomatic": False,
            "productionAcceptanceAutomatic": False,
        },
        "instructions": {
            "serveFromBundleRoot": True,
            "recommendedLocalPort": 8765,
            "recordingRule": (
                "Complete real review sessions first. Working templates remain not-accepted until an authorized "
                "reviewer records actual findings, durable references, and an accepted review decision. Governed "
                "reconciliation counts only committed records under acceptance/ that pass the external evidence validator."
            ),
        },
        "boundary": (
            "Preparation only. This bundle coordinates the three real evidence sessions needed for the seven current "
            "V1.6 blockers. It creates no accepted evidence and does not change the 17 verified / 7 unverified matrix."
        ),
    }

    (output / "qualification-session.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def validate_bundle(output: Path) -> dict:
    output = output.resolve()
    require((output / SENTINEL).is_file(), "qualification bundle sentinel missing")
    manifest = load_json(output / "qualification-session.json")
    require(manifest.get("recordType") == "glaze-v1.6-remaining-qualification-session", "bundle record type mismatch")
    require(manifest.get("sourceRevision") == SOURCE_REVISION, "bundle source revision mismatch")
    require(manifest.get("acceptanceModelVersion") == ACCEPTANCE_MODEL, "bundle acceptance model mismatch")
    require(manifest.get("stableBaseline") == STABLE_BASELINE, "bundle Stable baseline mismatch")
    require(manifest.get("currentDisposition", {}).get("blockingLaneIds") == EXPECTED_BLOCKERS, "bundle blocker set mismatch")
    require(manifest.get("currentDisposition", {}).get("unverifiedCount") == 7, "bundle unverified count mismatch")
    require(manifest.get("authority", {}).get("bundleIsEvidence") is False, "bundle must never be evidence")
    require(manifest.get("authority", {}).get("stableStatusGranted") is False, "bundle must never grant Stable")

    sessions = manifest.get("sessions")
    require(isinstance(sessions, list) and [x.get("id") for x in sessions] == [x["id"] for x in SESSIONS], "bundle session set mismatch")
    for item, expected in zip(sessions, SESSIONS):
        require((output / item["entrypoint"]).is_file(), f"{item['id']} entrypoint missing")
        template = output / item["workingTemplate"]
        require(template.is_file(), f"{item['id']} working template missing")
        validate_template(template, expected["evidenceType"])
        require(item.get("acceptedEvidenceClaimed") is False, f"{item['id']} must not claim accepted evidence")

    return manifest


def self_test(repo_root: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="glaze-v16-remaining-qualification-") as temp:
        root = Path(temp) / "bundle"
        manifest = prepare(repo_root, root, False)
        validated = validate_bundle(root)
        require(validated["toolingRevision"] == manifest["toolingRevision"], "self-test tooling revision mismatch")
    print("GLAZE UI V1.6 remaining qualification bundle: PASS")
    print("Coverage: 7 open lanes coordinated through Human, Assistive Technology, and Performance sessions.")
    print("Boundary: preparation only; accepted evidence and lifecycle promotion remain separate governed actions.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out", default="_v16-remaining-qualification")
    parser.add_argument("--replace", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root)
    if args.self_test:
        self_test(repo_root.resolve())
        return

    manifest = prepare(repo_root, Path(args.out), args.replace)
    validate_bundle(Path(args.out))

    print("GLAZE UI V1.6 remaining qualification bundle prepared")
    print("Frozen source: " + manifest["sourceRevision"])
    print("Tooling revision: " + manifest["toolingRevision"])
    print("Current disposition: 17 verified / 7 unverified / 0 not applicable")
    print("Serve all three review surfaces with one local server:")
    print("  python3 -m http.server 8765 --bind 127.0.0.1 --directory " + args.out)
    for session in manifest["sessions"]:
        print("  http://127.0.0.1:8765/" + session["entrypoint"])
    print("Boundary: no human, assistive-technology, performance, Candidate, RC, Stable, deployment, or production acceptance is created.")


if __name__ == "__main__":
    try:
        main()
    except QualificationBundleError as error:
        raise SystemExit("GLAZE UI V1.6 remaining qualification preparation FAILED: " + str(error))
