#!/usr/bin/env python3
"""Verify exact-head Stable security scan outputs for GLAZE UI V1.6.

This verifier intentionally fails closed. It accepts no vulnerability threshold:
any discovered secret finding or known dependency vulnerability blocks the
recorded security evidence until separately reviewed and resolved under
GoreeCloud security governance.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


class SecurityEvidenceError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SecurityEvidenceError(message)


def load_json(path: Path):
    require(path.is_file(), f"missing required scan output: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise SecurityEvidenceError(f"invalid JSON scan output {path}: {error}") from error


def exact_head() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def summarize_osv(report: dict) -> tuple[int, list[str]]:
    results = report.get("results", [])
    require(isinstance(results, list), "OSV report results must be a list")

    package_count = 0
    vulnerability_ids: set[str] = set()
    for result in results:
        require(isinstance(result, dict), "OSV result entry must be an object")
        packages = result.get("packages", [])
        require(isinstance(packages, list), "OSV result packages must be a list")
        for entry in packages:
            require(isinstance(entry, dict), "OSV package entry must be an object")
            package = entry.get("package")
            require(isinstance(package, dict), "OSV package metadata missing")
            name = package.get("name")
            version = package.get("version")
            ecosystem = package.get("ecosystem")
            require(isinstance(name, str) and name, "OSV package name missing")
            require(isinstance(version, str) and version, f"OSV package version missing for {name}")
            require(isinstance(ecosystem, str) and ecosystem, f"OSV package ecosystem missing for {name}")
            package_count += 1

            vulnerabilities = entry.get("vulnerabilities", [])
            require(isinstance(vulnerabilities, list), f"OSV vulnerabilities malformed for {name}")
            for vulnerability in vulnerabilities:
                require(isinstance(vulnerability, dict), "OSV vulnerability entry must be an object")
                vulnerability_id = vulnerability.get("id")
                require(
                    isinstance(vulnerability_id, str) and vulnerability_id,
                    f"OSV vulnerability ID missing for {name}",
                )
                vulnerability_ids.add(vulnerability_id)

    return package_count, sorted(vulnerability_ids)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-sha", required=True)
    parser.add_argument("--gitleaks-report", required=True)
    parser.add_argument("--gitleaks-exit-code", required=True)
    parser.add_argument("--osv-report", required=True)
    parser.add_argument("--osv-exit-code", required=True)
    parser.add_argument("--sbom", required=True)
    parser.add_argument("--sbom-exit-code", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--gitleaks-version", required=True)
    parser.add_argument("--gitleaks-sha256", required=True)
    parser.add_argument("--osv-version", required=True)
    parser.add_argument("--osv-sha256", required=True)
    parser.add_argument("--gradle-version", required=True)
    parser.add_argument("--gradle-sha256", required=True)
    args = parser.parse_args()

    require(SHA_RE.fullmatch(args.expected_sha) is not None, "expected SHA must be a 40-character commit SHA")
    head = exact_head()
    require(head == args.expected_sha, f"exact-head mismatch: checkout={head} expected={args.expected_sha}")

    lifecycle = load_json(ROOT / "registry/lifecycle.json")
    require(lifecycle.get("currentStable") == "1.5.1", "current Stable must remain 1.5.1")
    require(lifecycle.get("currentOfficial") == "1.5.1", "current Official must remain 1.5.1")
    require(lifecycle.get("activeCandidate") == "1.6.0-rc.1", "active V1.6 candidate must remain 1.6.0-rc.1")

    review = load_json(ROOT / "acceptance/v1.6-stable-qualification-review.json")
    require(review.get("decision") == "blocked-remain-release-candidate", "Stable review must remain blocked")
    require(review.get("stablePromotionAuthorized") is False, "security scan must not authorize Stable promotion")

    def read_exit_code(path: str, label: str) -> int:
        source = Path(path)
        require(source.is_file(), f"missing {label} exit-code evidence: {source}")
        raw = source.read_text(encoding="utf-8").strip()
        require(re.fullmatch(r"\d+", raw) is not None, f"{label} exit code is malformed: {raw!r}")
        return int(raw)

    gitleaks_exit = read_exit_code(args.gitleaks_exit_code, "Gitleaks")
    osv_exit = read_exit_code(args.osv_exit_code, "OSV-Scanner")
    sbom_exit = read_exit_code(args.sbom_exit_code, "OSV-Scanner SBOM")
    require(gitleaks_exit in (0, 1), f"Gitleaks scanner error: exit {gitleaks_exit}")
    require(osv_exit in (0, 1), f"OSV-Scanner error: exit {osv_exit}")
    require(sbom_exit in (0, 1), f"OSV-Scanner SBOM error: exit {sbom_exit}")

    false_positive_review = load_json(ROOT / "acceptance/v1.6-gitleaks-false-positive-review.json")
    require(false_positive_review.get("disposition") == "verified-false-positives", "Gitleaks false-positive review must be accepted")
    require(false_positive_review.get("findingCount") == 21, "Gitleaks false-positive review count mismatch")

    dependency_classification = load_json(ROOT / "acceptance/v1.6-dependency-vulnerability-classification.json")
    security_review = load_json(ROOT / "acceptance/v1.6-stable-security-review.json")
    require(
        dependency_classification.get("decision") == "blocked-unresolved-build-tooling-vulnerabilities",
        "dependency classification must remain blocking",
    )
    require(security_review.get("overallDecision") == "blocked", "Stable security review must remain blocked")
    require(security_review.get("stableSecurityAcceptanceGranted") is False, "Stable security acceptance must remain false")
    require(security_review.get("stablePromotionAuthorized") is False, "security review must not authorize Stable promotion")
    require(security_review.get("secretHistory", {}).get("result") == "passed", "secret-history disposition must be passed")
    require(security_review.get("dependencySupplyChain", {}).get("result") == "blocked", "dependency disposition must remain blocked")
    require(
        dependency_classification.get("stablePromotionAuthorized") is False,
        "dependency classification must not authorize Stable promotion",
    )
    prior_summary = dependency_classification.get("scanSummary", {})
    require(prior_summary.get("osvPackageEntryCount") == 1104, "dependency classification package-count provenance mismatch")
    require(prior_summary.get("distinctAdvisoryCount") == 50, "dependency classification advisory-count provenance mismatch")
    require(prior_summary.get("recordedRuntimeMatchedVulnerableEntryCount") == 0, "dependency classification runtime-boundary mismatch")
    ignore_path = ROOT / ".gitleaksignore"
    require(ignore_path.is_file(), ".gitleaksignore is missing")
    ignore_entries = [
        line.strip()
        for line in ignore_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    require(len(ignore_entries) == 21, "Gitleaks ignore file must contain exactly the 21 reviewed fingerprints")
    require(len(set(ignore_entries)) == 21, "Gitleaks ignore fingerprints must be unique")
    reviewed_fingerprints = false_positive_review.get("suppression", {}).get("fingerprints")
    require(isinstance(reviewed_fingerprints, list), "Gitleaks false-positive review must bind the reviewed fingerprints")
    require(len(reviewed_fingerprints) == 21, "Gitleaks false-positive review fingerprint count mismatch")
    require(len(set(reviewed_fingerprints)) == 21, "Gitleaks reviewed fingerprints must be unique")
    require(set(ignore_entries) == set(reviewed_fingerprints), ".gitleaksignore must match the exact reviewed fingerprint set")

    gitleaks = load_json(Path(args.gitleaks_report))
    require(isinstance(gitleaks, list), "Gitleaks JSON report must be a list")
    secret_findings = len(gitleaks)
    require(
        (gitleaks_exit == 0 and secret_findings == 0)
        or (gitleaks_exit == 1 and secret_findings > 0),
        f"Gitleaks exit/report inconsistency: exit={gitleaks_exit} findings={secret_findings}",
    )

    osv = load_json(Path(args.osv_report))
    package_count, vulnerability_ids = summarize_osv(osv)
    require(package_count > 0, "OSV scan discovered zero dependency packages; coverage is not established")
    require(
        (osv_exit == 0 and not vulnerability_ids)
        or (osv_exit == 1 and bool(vulnerability_ids)),
        f"OSV exit/report inconsistency: exit={osv_exit} vulnerabilities={len(vulnerability_ids)}",
    )
    expected_advisories = dependency_classification.get("distinctAdvisoryIds")
    require(isinstance(expected_advisories, list), "dependency classification advisory set missing")
    require(len(expected_advisories) == 50, "dependency classification must retain the reviewed 50-advisory set")
    require(
        vulnerability_ids == sorted(expected_advisories),
        "live OSV advisory set differs from the governed dependency classification",
    )
    require(
        package_count == dependency_classification.get("scanSummary", {}).get("osvPackageEntryCount"),
        "live OSV package-entry count differs from governed classification",
    )

    sbom = load_json(Path(args.sbom))
    require(sbom.get("bomFormat") == "CycloneDX", "SBOM must use CycloneDX")
    require(sbom.get("specVersion") == "1.5", "SBOM must use CycloneDX 1.5")
    components = sbom.get("components", [])
    require(isinstance(components, list) and components, "CycloneDX SBOM contains no components")
    sbom_vulnerabilities = sbom.get("vulnerabilities", [])
    require(isinstance(sbom_vulnerabilities, list), "CycloneDX vulnerabilities must be a list")
    require(
        (sbom_exit == 0 and not sbom_vulnerabilities)
        or (sbom_exit == 1 and bool(sbom_vulnerabilities)),
        f"SBOM exit/report inconsistency: exit={sbom_exit} vulnerabilities={len(sbom_vulnerabilities)}",
    )
    for label, digest in (
        ("gitleaks", args.gitleaks_sha256),
        ("osv-scanner", args.osv_sha256),
        ("gradle", args.gradle_sha256),
    ):
        require(re.fullmatch(r"[0-9a-f]{64}", digest) is not None, f"{label} SHA-256 must be lowercase hex")

    blocked_reasons = []
    if secret_findings:
        blocked_reasons.append(f"unreviewed secret findings: {secret_findings}")
    if vulnerability_ids:
        blocked_reasons.append(f"known dependency vulnerability advisories: {len(vulnerability_ids)}")
    if sbom_vulnerabilities:
        blocked_reasons.append(f"CycloneDX vulnerability entries: {len(sbom_vulnerabilities)}")

    require(secret_findings == 0, "unreviewed secret findings are not an accepted blocked-state condition")
    require(len(vulnerability_ids) == 50, "expected governed dependency blocker count is 50")
    require(len(sbom_vulnerabilities) == 50, "CycloneDX vulnerability count must match the governed 50-advisory blocker")
    require(
        dependency_classification.get("scanSummary", {}).get("recordedRuntimeMatchedVulnerableEntryCount") == 0,
        "runtime-boundary classification must remain zero matched vulnerable entries",
    )

    output = {
        "schemaVersion": 1,
        "kind": "goreecloud-glaze-v1.6-stable-security-scan-evidence",
        "result": "blocked" if blocked_reasons else "passed",
        "sourceRevision": head,
        "lifecycle": {
            "currentStable": "1.5.1",
            "activeCandidate": "1.6.0-rc.1",
            "stablePromotionAuthorized": False,
        },
        "secretHistoryScan": {
            "tool": "gitleaks",
            "version": args.gitleaks_version,
            "binarySha256": args.gitleaks_sha256,
            "scope": "complete fetched Git history for the exact repository checkout",
            "findingCount": secret_findings,
            "reviewedHistoricalFalsePositiveCount": false_positive_review.get("findingCount"),
            "suppressionMethod": false_positive_review.get("suppression", {}).get("method"),
            "result": "passed" if secret_findings == 0 else "blocked",
        },
        "dependencyVulnerabilityScan": {
            "tool": "osv-scanner",
            "version": args.osv_version,
            "binarySha256": args.osv_sha256,
            "input": "generated Gradle verification metadata plus recursively discovered supported lockfiles/manifests",
            "packageCount": package_count,
            "vulnerabilityIds": vulnerability_ids,
            "result": "passed" if not vulnerability_ids else "blocked",
        },
        "sbom": {
            "format": "CycloneDX",
            "specVersion": "1.5",
            "componentCount": len(components),
            "vulnerabilityCount": len(sbom_vulnerabilities),
            "result": "passed" if not sbom_vulnerabilities else "blocked",
        },
        "dependencyResolution": {
            "tool": "Gradle",
            "version": args.gradle_version,
            "distributionSha256": args.gradle_sha256,
            "referenceProjects": [
                "reference/v1.1/native/android",
                "reference/v1.2/native/android",
                "reference/native/wear-os/buildable",
            ],
        },
        "blockedReasons": blocked_reasons,
        "limitations": [
            "This record proves the scanners completed successfully for the exact checked-out revision and their discoverable dependency inputs; it does not prove that advisory databases contain every vulnerability.",
            "The primary Glaze UI JavaScript runtime has no npm/pnpm/yarn or Python package manifest in this repository; Android/Wear dependencies are resolved from the buildable reference projects into verification metadata for scanning.",
            "Passing security scans do not grant Stable, production readiness, production acceptance, publication, or downstream consumer acceptance.",
        ],
        "governedDisposition": {
            "securityReview": "acceptance/v1.6-stable-security-review.json",
            "dependencyClassification": "acceptance/v1.6-dependency-vulnerability-classification.json",
            "overallDecision": security_review.get("overallDecision"),
            "stableSecurityAcceptanceGranted": security_review.get("stableSecurityAcceptanceGranted"),
            "evidenceCollectionValidated": True,
        },
        "generatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"GLAZE UI V1.6 Stable security scan evidence: {output['result'].upper()}")
    print(f"Exact revision: {head}")
    print(f"Unreviewed secret findings: {secret_findings}")
    print(f"Reviewed historical false positives: {false_positive_review.get('findingCount')}")
    print(f"Dependency packages scanned: {package_count}")
    print(f"Known dependency vulnerability advisories: {len(vulnerability_ids)}")
    print(f"CycloneDX components: {len(components)}")
    print("Stable promotion authorized: false")
    if output["result"] == "blocked":
        require(
            security_review.get("overallDecision") == "blocked"
            and security_review.get("dependencySupplyChain", {}).get("advisoryCount") == 50,
            "live blocked scan is not represented by the governed security review",
        )
        print("Governed evidence disposition: VALIDATED BLOCKED")
        return 0

    raise SecurityEvidenceError(
        "security scan no longer matches the governed blocked review; update the security review before acceptance"
    )


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SecurityEvidenceError as error:
        print(f"FAIL: {error}")
        raise SystemExit(1)
