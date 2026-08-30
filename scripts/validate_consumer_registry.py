#!/usr/bin/env python3
"""Validate the mandatory Stable Glaze UI audit and bounded 2.1 Candidate assessments."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "consumers" / "registry.json"
DOC = ROOT / "CONSUMERS.md"
VERSION = ROOT / "VERSION"
LIFECYCLE = ROOT / "registry" / "lifecycle.json"
SCHEMA = ROOT / "schemas" / "consumer-registry.schema.json"

ALLOWED = {"aligned-current-stable", "adoption-candidate", "migration-required", "unverified"}
CANDIDATE_ALLOWED = {"evaluation-in-progress", "evaluation-complete", "blocked"}
EXPECTED_REPOS = {
    "GoreeCloud/goreecloud-manager",
    "GoreeCloud/goreecloud-website",
    "GoreeCloud/goreecloud-tasks",
    "GoreeCloud/goreecloud-launcher",
    "GoreeCloud/goreecloud-keyboard",
    "GoreeCloud/goreecloud-notes",
    "GoreeCloud/goreecloud-monitor",
    "GoreeCloud/goreecloud-browser",
    "GoreeCloud/goreecloud-wardveil-security",
    "GoreeCloud/goreecloud-privacy-shield",
}
REQUIRED_PLATFORMS = {"web", "desktop", "mobile", "tablet", "tv", "smartwatch", "other-user-facing"}
REQUIRED_CANDIDATE_EVIDENCE = {
    "repository-local-version-and-component-mapping",
    "exact-revision-automated-validation",
    "rendered-or-native-acceptance-as-applicable",
    "accessibility-acceptance",
    "representative-platform-acceptance",
    "human-visual-excellence-when-applicable",
}
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
SHA40 = re.compile(r"^[0-9a-f]{40}$")


def req(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Glaze UI consumer registry validation failed: {message}")


def vt(version: str) -> tuple[int, int, int]:
    req(bool(SEMVER.fullmatch(version)), f"invalid semantic version: {version}")
    return tuple(map(int, version.split(".")))


def evidence(name: str, target: object, revision: object, evidence_path: object, automated: object) -> None:
    req(isinstance(target, str) and bool(SEMVER.fullmatch(target)), f"{name} needs semantic target")
    req(isinstance(revision, str) and bool(SHA40.fullmatch(revision)), f"{name} needs reviewed revision")
    req(isinstance(evidence_path, str) and bool(evidence_path.strip()), f"{name} needs evidence")
    req(automated is True, f"{name} needs automated contract")


def main() -> None:
    req(REGISTRY.is_file() and DOC.is_file() and VERSION.is_file() and LIFECYCLE.is_file() and SCHEMA.is_file(), "required consumer files missing")
    stable = VERSION.read_text(encoding="utf-8").strip()
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    lifecycle = json.loads(LIFECYCLE.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    for marker in (
        "Aligned — current Stable",
        "Adoption Candidate",
        "Migration Required",
        "Unverified",
        "consumers/registry.json",
        "Audit completeness",
        "Mandatory current Stable target",
        "Candidate assessment layer",
        "must not silently depend on Candidate or Experimental",
    ):
        req(marker in doc, f"CONSUMERS.md missing {marker}")

    req(data.get("schemaVersion") == 4, "schemaVersion")
    req(schema.get("$id") == "https://goreecloud.dev/schemas/glaze-ui/consumer-registry.schema.json", "consumer registry schema id")
    req(schema.get("properties", {}).get("schemaVersion", {}).get("const") == 4, "consumer registry schema version")
    req(data.get("stableBaseline") == stable, "Stable baseline differs from VERSION")
    req(data.get("requiredConsumerVersion") == stable, "required consumer version differs from VERSION")
    req(set(data.get("statusVocabulary", [])) == ALLOWED, "status vocabulary")
    req(re.fullmatch(r"\d{4}-\d{2}-\d{2}", data.get("auditedAt", "")) is not None, "auditedAt")

    historical = data.get("historicalStableVersions")
    req(isinstance(historical, list), "historicalStableVersions must be a list")
    req(all(isinstance(v, str) and SEMVER.fullmatch(v) for v in historical), "historical versions must use semantic versioning")
    req(len(set(historical)) == len(historical), "historical Stable versions must be unique")
    req(historical == sorted(historical, key=vt), "historical Stable versions must be ordered")
    req(all(vt(v) < vt(stable) for v in historical), "historical Stable versions must precede current Stable")

    enforcement = data.get("enforcement", {})
    req(enforcement.get("currentStableRequired") is True, "currentStableRequired must be true")
    req(enforcement.get("productionExceptionsAllowed") is False, "production exceptions must be forbidden")
    req(REQUIRED_PLATFORMS.issubset(set(enforcement.get("platformScope", []))), "platform scope must include all mandatory user-facing classes")
    req("production-blocked" in enforcement.get("unsupportedPlatformRule", ""), "unsupported-platform rule must fail closed")

    active_candidate = lifecycle.get("activeCandidate")
    req(active_candidate == "2.1.0-candidate.1", "active Candidate must remain 2.1.0-candidate.1")
    releases = lifecycle.get("releases", [])
    candidate_release = [r for r in releases if isinstance(r, dict) and r.get("version") == active_candidate]
    req(len(candidate_release) == 1 and candidate_release[0].get("status") == "candidate", "active Candidate lifecycle record")
    req(candidate_release[0].get("consumerEligible") is False, "active Candidate must remain non-consumer-eligible")
    rules = lifecycle.get("promotionRules", {})
    req(rules.get("candidateMaySatisfyStableConsumerConformance") is False, "Candidate must not satisfy Stable consumer conformance")
    req(rules.get("stableVersionFileMustRemain") == stable, "Candidate promotion rule must retain current Stable VERSION")

    assessment = data.get("candidateAssessment")
    req(isinstance(assessment, dict), "candidateAssessment must be an object")
    req(assessment.get("version") == active_candidate, "candidateAssessment version must match lifecycle activeCandidate")
    req(assessment.get("lifecycle") == "candidate", "candidateAssessment lifecycle")
    req(assessment.get("consumerEligible") is False, "Candidate assessment cannot be consumer eligible")
    req(assessment.get("productionEligible") is False, "Candidate assessment cannot be production eligible")
    req(set(assessment.get("evaluationStatusVocabulary", [])) == CANDIDATE_ALLOWED, "Candidate evaluation status vocabulary")
    req(set(assessment.get("requiredEvidence", [])) == REQUIRED_CANDIDATE_EVIDENCE, "Candidate required-evidence vocabulary")
    req("unassessed" in assessment.get("coverageRule", "").lower(), "Candidate coverage rule must make absence unassessed")
    req("cannot satisfy" in assessment.get("rule", "").lower() and "stable" in assessment.get("rule", "").lower(), "Candidate rule must preserve Stable gate")
    evaluations = assessment.get("evaluations")
    req(isinstance(evaluations, list), "Candidate evaluations must be a list")
    candidate_seen: set[str] = set()
    for item in evaluations:
        req(isinstance(item, dict), "Candidate evaluation must be an object")
        repo = item.get("repository")
        req(repo in EXPECTED_REPOS and repo not in candidate_seen, f"invalid/duplicate Candidate assessment repo {repo}")
        candidate_seen.add(repo)
        req(item.get("status") in CANDIDATE_ALLOWED, f"invalid Candidate evaluation status for {repo}")
        req(item.get("targetVersion") == active_candidate, f"Candidate evaluation target mismatch for {repo}")
        req(isinstance(item.get("referenceRevision"), str) and SHA40.fullmatch(item["referenceRevision"]), f"Candidate evaluation needs exact revision for {repo}")
        req(isinstance(item.get("evidence"), str) and item["evidence"].strip(), f"Candidate evaluation needs evidence for {repo}")
        req(item.get("automatedContract") is True, f"Candidate evaluation needs automated validation for {repo}")
        req(item.get("productionEligible") is False, f"Candidate evaluation cannot make {repo} production eligible")
        req(item.get("stableConformanceUnaffected") is True, f"Candidate evaluation must not rewrite Stable state for {repo}")
        req(isinstance(item.get("acceptanceBoundary"), str) and item["acceptanceBoundary"].strip(), f"Candidate evaluation needs acceptance boundary for {repo}")

    consumers = data.get("consumers")
    req(isinstance(consumers, list) and consumers, "consumers must be a non-empty list")
    seen: set[str] = set()
    for consumer in consumers:
        name = consumer["name"]
        repo = consumer["repository"]
        status = consumer["status"]
        target = consumer.get("targetVersion")
        required = consumer.get("requiredTargetVersion")
        revision = consumer.get("referenceRevision")
        evidence_path = consumer.get("evidence")
        automated = consumer.get("automatedContract")
        eligible = consumer.get("productionEligible")
        acceptance = consumer.get("visualAcceptance")
        notes = consumer.get("notes")

        req(repo.startswith("GoreeCloud/") and repo not in seen, f"invalid/duplicate repo {repo}")
        seen.add(repo)
        req(status in ALLOWED, f"invalid status {name}")
        req(required == stable, f"{name} required target must equal current Stable {stable}")
        req(isinstance(acceptance, str) and acceptance.strip() and isinstance(notes, str) and notes.strip(), f"missing acceptance/notes {name}")
        if status == "aligned-current-stable":
            evidence(name, target, revision, evidence_path, automated)
            req(target == stable, f"{name} must target current Stable {stable}")
            req(eligible is True, f"{name} aligned current Stable must be production eligible")
        elif status == "adoption-candidate":
            evidence(name, target, revision, evidence_path, automated)
            req(target == stable, f"{name} adoption candidate must target current Stable {stable}")
            req(eligible is False, f"{name} candidate must not be production eligible")
            req(any(x in acceptance.lower() for x in ("pending", "required", "not complete", "not established", "remains pending")), f"{name} needs incomplete final-acceptance boundary")
        elif status == "migration-required":
            evidence(name, target, revision, evidence_path, automated)
            req(target in historical, f"{name} migration source target must be a historical Stable release")
            req(vt(target) < vt(stable), f"{name} migration source target must precede current Stable")
            req(eligible is False, f"{name} migration-required consumer must not be production eligible")
        else:
            req(target is None and revision is None and evidence_path is None and not automated, f"unverified {name} must not claim versioned evidence")
            req(eligible is False, f"unverified {name} must not be production eligible")

    req(seen == EXPECTED_REPOS, f"audit scope drift: expected {sorted(EXPECTED_REPOS)}, got {sorted(seen)}")
    req(candidate_seen.issubset(seen), "Candidate assessments must be a subset of the Stable audit scope")
    print(f"Glaze UI consumer registry validated: {len(consumers)} audited consumers; mandatory current Stable target {stable}; {len(evaluations)} explicit {active_candidate} evaluations")


if __name__ == "__main__":
    main()
