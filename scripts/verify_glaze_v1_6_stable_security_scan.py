#!/usr/bin/env python3
"""Verify exact-head Stable security acceptance for GLAZE UI V1.6.

Fails closed. The release-blocking dependency boundary is the Gradle-selected
build/runtime graph. A broader verification-metadata scan remains mandatory
diagnostic evidence; any diagnostic vulnerable coordinate that is also selected
immediately fails acceptance.
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
    require(path.is_file(), f"missing required evidence: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise SecurityEvidenceError(f"invalid JSON evidence {path}: {error}") from error


def exact_head() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def read_exit_code(path: Path, label: str) -> int:
    require(path.is_file(), f"missing {label} exit-code evidence: {path}")
    raw = path.read_text(encoding="utf-8").strip()
    require(re.fullmatch(r"\d+", raw) is not None, f"{label} exit code is malformed: {raw!r}")
    return int(raw)


def summarize_inventory(report: dict) -> tuple[int, set[str]]:
    results = report.get("results", [])
    require(isinstance(results, list), "selected dependency inventory results must be a list")
    package_entries = 0
    coordinates: set[str] = set()
    for result in results:
        require(isinstance(result, dict), "selected dependency result must be an object")
        packages = result.get("packages", [])
        require(isinstance(packages, list), "selected dependency packages must be a list")
        for entry in packages:
            require(isinstance(entry, dict), "selected dependency package entry must be an object")
            package = entry.get("package")
            require(isinstance(package, dict), "selected dependency package metadata missing")
            name = package.get("name")
            version = package.get("version")
            ecosystem = package.get("ecosystem")
            require(isinstance(name, str) and name, "selected dependency name missing")
            require(isinstance(version, str) and version, f"selected dependency version missing for {name}")
            require(ecosystem == "Maven", f"unexpected selected dependency ecosystem for {name}: {ecosystem!r}")
            package_entries += 1
            coordinates.add(f"{name}:{version}")
            require(not entry.get("vulnerabilities"), "selected inventory must contain package identity only")
    return package_entries, coordinates


def summarize_osv(report: dict) -> tuple[int, set[str], set[str]]:
    results = report.get("results", [])
    require(isinstance(results, list), "OSV report results must be a list")
    package_entries = 0
    vulnerability_ids: set[str] = set()
    vulnerable_coordinates: set[str] = set()
    for result in results:
        require(isinstance(result, dict), "OSV result entry must be an object")
        packages = result.get("packages", [])
        require(isinstance(packages, list), "OSV result packages must be a list")
        for entry in packages:
            package_entries += 1
            package = entry.get("package")
            require(isinstance(package, dict), "OSV package metadata missing")
            name = package.get("name")
            version = package.get("version")
            require(isinstance(name, str) and name, "OSV package name missing")
            require(isinstance(version, str) and version, f"OSV package version missing for {name}")
            vulnerabilities = entry.get("vulnerabilities", [])
            require(isinstance(vulnerabilities, list), f"OSV vulnerabilities malformed for {name}")
            if vulnerabilities:
                vulnerable_coordinates.add(f"{name}:{version}")
            for vulnerability in vulnerabilities:
                require(isinstance(vulnerability, dict), "OSV vulnerability entry must be an object")
                vulnerability_id = vulnerability.get("id")
                require(isinstance(vulnerability_id, str) and vulnerability_id, "OSV vulnerability ID missing")
                vulnerability_ids.add(vulnerability_id)
    return package_entries, vulnerability_ids, vulnerable_coordinates


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-sha", required=True)
    parser.add_argument("--gitleaks-report", required=True)
    parser.add_argument("--gitleaks-exit-code", required=True)
    parser.add_argument("--dependency-inventory", required=True)
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

    qualification = load_json(ROOT / "acceptance/v1.6-stable-qualification-review.json")
    require(qualification.get("decision") == "blocked-remain-release-candidate", "overall Stable review must remain blocked during security closure")
    require(qualification.get("stablePromotionAuthorized") is False, "security closure must not authorize Stable promotion")

    false_positive_review = load_json(ROOT / "acceptance/v1.6-gitleaks-false-positive-review.json")
    require(false_positive_review.get("disposition") == "verified-false-positives", "Gitleaks false-positive review must be accepted")
    require(false_positive_review.get("findingCount") == 21, "Gitleaks false-positive review count mismatch")
    ignore_path = ROOT / ".gitleaksignore"
    require(ignore_path.is_file(), ".gitleaksignore is missing")
    ignore_entries = [
        line.strip()
        for line in ignore_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    reviewed_fingerprints = false_positive_review.get("suppression", {}).get("fingerprints")
    require(isinstance(reviewed_fingerprints, list), "reviewed Gitleaks fingerprints missing")
    require(len(ignore_entries) == 21 and len(set(ignore_entries)) == 21, "Gitleaks ignore set must contain exactly 21 unique fingerprints")
    require(set(ignore_entries) == set(reviewed_fingerprints), ".gitleaksignore must match the exact reviewed fingerprint set")

    classification = load_json(ROOT / "acceptance/v1.6-dependency-vulnerability-classification.json")
    security_review = load_json(ROOT / "acceptance/v1.6-stable-security-review.json")
    require(classification.get("decision") == "resolved-selected-build-tooling-vulnerabilities", "dependency classification must record remediation")
    require(classification.get("stableSecurityAcceptanceSupported") is True, "dependency classification must support security acceptance")
    require(classification.get("stablePromotionAuthorized") is False, "dependency classification must not authorize Stable promotion")
    require(security_review.get("overallDecision") == "accepted-security-gate", "security review must accept only the security gate")
    require(security_review.get("stableSecurityAcceptanceGranted") is True, "Stable security acceptance must be granted")
    require(security_review.get("stablePromotionAuthorized") is False, "security review must not authorize Stable promotion")
    require(security_review.get("secretHistory", {}).get("result") == "passed", "secret-history disposition must pass")
    require(security_review.get("dependencySupplyChain", {}).get("result") == "passed", "dependency/supply-chain disposition must pass")

    gitleaks_exit = read_exit_code(Path(args.gitleaks_exit_code), "Gitleaks")
    require(gitleaks_exit == 0, f"Gitleaks must pass with exit 0, got {gitleaks_exit}")
    gitleaks = load_json(Path(args.gitleaks_report))
    require(isinstance(gitleaks, list), "Gitleaks JSON report must be a list")
    require(len(gitleaks) == 0, f"unreviewed secret findings remain: {len(gitleaks)}")

    selected_inventory = load_json(Path(args.dependency_inventory))
    selected_entry_count, selected_coordinates = summarize_inventory(selected_inventory)
    selected_summary = classification.get("selectedGraphSummary", {})
    require(selected_entry_count == selected_summary.get("selectedPackageEntryCount") == 426, "selected package-entry count mismatch")
    require(len(selected_coordinates) == selected_summary.get("distinctSelectedCoordinateCount") == 206, "distinct selected coordinate count mismatch")

    selected_osv_exit = read_exit_code(Path(args.osv_exit_code), "selected OSV-Scanner")
    require(selected_osv_exit == 0, f"selected OSV scan must pass with exit 0, got {selected_osv_exit}")
    selected_osv = load_json(Path(args.osv_report))
    selected_vulnerable_entries, selected_advisories, selected_vulnerable_coordinates = summarize_osv(selected_osv)
    require(selected_vulnerable_entries == 0, "selected OSV report unexpectedly contains package entries")
    require(not selected_advisories, f"selected dependency advisories remain: {sorted(selected_advisories)}")
    require(not selected_vulnerable_coordinates, f"selected vulnerable coordinates remain: {sorted(selected_vulnerable_coordinates)}")
    require(selected_summary.get("vulnerablePackageEntryCount") == 0, "governed selected vulnerable-package count must be zero")
    require(selected_summary.get("distinctAdvisoryCount") == 0, "governed selected advisory count must be zero")

    selected_sbom_exit = read_exit_code(Path(args.sbom_exit_code), "selected SBOM")
    require(selected_sbom_exit == 0, f"selected SBOM generation must pass with exit 0, got {selected_sbom_exit}")
    selected_sbom = load_json(Path(args.sbom))
    require(selected_sbom.get("bomFormat") == "CycloneDX", "selected SBOM must use CycloneDX")
    require(selected_sbom.get("specVersion") == "1.5", "selected SBOM must use CycloneDX 1.5")
    selected_components = selected_sbom.get("components", [])
    selected_sbom_vulns = selected_sbom.get("vulnerabilities", [])
    require(isinstance(selected_components, list) and len(selected_components) == 206, "selected CycloneDX component count mismatch")
    require(isinstance(selected_sbom_vulns, list) and len(selected_sbom_vulns) == 0, "selected CycloneDX must contain zero vulnerabilities")

    diagnostic_report_path = ROOT / "artifacts/v1.6-security/osv-report.json"
    diagnostic_exit_path = ROOT / "artifacts/v1.6-security/osv-exit-code.txt"
    diagnostic_sbom_path = ROOT / "artifacts/v1.6-security/cyclonedx-1.5.json"
    diagnostic_sbom_exit_path = ROOT / "artifacts/v1.6-security/sbom-exit-code.txt"
    diagnostic_exit = read_exit_code(diagnostic_exit_path, "diagnostic OSV-Scanner")
    require(diagnostic_exit in (0, 1), f"diagnostic OSV scanner error: exit {diagnostic_exit}")
    diagnostic_report = load_json(diagnostic_report_path)
    diagnostic_package_entries, diagnostic_advisories, diagnostic_vulnerable_coordinates = summarize_osv(diagnostic_report)
    diagnostic_summary = classification.get("diagnosticVerificationMetadataSummary", {})
    require(diagnostic_package_entries == diagnostic_summary.get("packageEntryCount") == 780, "diagnostic package-entry count mismatch")
    require(len(diagnostic_vulnerable_coordinates) == diagnostic_summary.get("vulnerableCoordinateCount") == 4, "diagnostic vulnerable-coordinate count mismatch")
    require(len(diagnostic_advisories) == diagnostic_summary.get("distinctAdvisoryCount") == 6, "diagnostic advisory count mismatch")
    require(sorted(diagnostic_vulnerable_coordinates) == sorted(diagnostic_summary.get("vulnerableCoordinates", [])), "diagnostic vulnerable-coordinate set mismatch")
    require(sorted(diagnostic_advisories) == sorted(diagnostic_summary.get("distinctAdvisoryIds", [])), "diagnostic advisory set mismatch")
    require(diagnostic_vulnerable_coordinates.isdisjoint(selected_coordinates), "diagnostic vulnerable coordinate is selected by Gradle; non-applicability invalid")

    replacements = classification.get("remediatedSelectedCoordinates", {})
    for name, version in replacements.items():
        require(f"{name}:{version}" in selected_coordinates, f"expected remediated selected coordinate missing: {name}:{version}")

    diagnostic_sbom_exit = read_exit_code(diagnostic_sbom_exit_path, "diagnostic SBOM")
    require(diagnostic_sbom_exit in (0, 1), f"diagnostic SBOM error: exit {diagnostic_sbom_exit}")
    diagnostic_sbom = load_json(diagnostic_sbom_path)
    require(diagnostic_sbom.get("bomFormat") == "CycloneDX", "diagnostic SBOM must use CycloneDX")
    require(diagnostic_sbom.get("specVersion") == "1.5", "diagnostic SBOM must use CycloneDX 1.5")
    require(len(diagnostic_sbom.get("components", [])) == diagnostic_summary.get("cyclonedxComponentCount") == 372, "diagnostic CycloneDX component count mismatch")
    require(len(diagnostic_sbom.get("vulnerabilities", [])) == diagnostic_summary.get("cyclonedxVulnerabilityCount") == 6, "diagnostic CycloneDX vulnerability count mismatch")

    for label, digest in (
        ("gitleaks", args.gitleaks_sha256),
        ("osv-scanner", args.osv_sha256),
        ("gradle", args.gradle_sha256),
    ):
        require(re.fullmatch(r"[0-9a-f]{64}", digest) is not None, f"{label} SHA-256 must be lowercase hex")

    output = {
        "schemaVersion": 2,
        "kind": "goreecloud-glaze-v1.6-stable-security-scan-evidence",
        "result": "passed",
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
            "findingCount": 0,
            "reviewedHistoricalFalsePositiveCount": 21,
            "result": "passed",
        },
        "selectedDependencyScan": {
            "tool": "osv-scanner",
            "version": args.osv_version,
            "binarySha256": args.osv_sha256,
            "selectedPackageEntryCount": selected_entry_count,
            "distinctSelectedCoordinateCount": len(selected_coordinates),
            "vulnerabilityIds": [],
            "result": "passed",
        },
        "selectedSbom": {
            "format": "CycloneDX",
            "specVersion": "1.5",
            "componentCount": len(selected_components),
            "vulnerabilityCount": 0,
            "result": "passed",
        },
        "diagnosticVerificationMetadata": {
            "packageEntryCount": diagnostic_package_entries,
            "vulnerableCoordinates": sorted(diagnostic_vulnerable_coordinates),
            "vulnerabilityIds": sorted(diagnostic_advisories),
            "selectedCoordinateOverlap": [],
            "disposition": "non-applicable-superseded-unselected-coordinates",
        },
        "dependencyResolution": {
            "tool": "Gradle",
            "version": args.gradle_version,
            "distributionSha256": args.gradle_sha256,
        },
        "governedDisposition": {
            "overallDecision": "accepted-security-gate",
            "stableSecurityAcceptanceGranted": True,
            "stablePromotionAuthorized": False,
        },
        "limitations": [
            "Scanner acceptance is limited to the exact checked-out revision and discoverable inputs; advisory databases are not guaranteed exhaustive.",
            "Broad verification metadata may preserve requested versions superseded by Gradle; non-applicability is valid only while the exact selected graph proves those vulnerable coordinates are absent.",
            "Security acceptance does not grant overall Stable status, publication acceptance, downstream consumer acceptance, deployment, or production acceptance.",
        ],
        "generatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("GLAZE UI V1.6 Stable security scan evidence: PASSED")
    print(f"Exact revision: {head}")
    print("Unreviewed secret findings: 0")
    print(f"Selected package entries scanned: {selected_entry_count}")
    print(f"Distinct selected coordinates: {len(selected_coordinates)}")
    print("Known selected dependency vulnerability advisories: 0")
    print(f"Diagnostic vulnerable coordinates (all unselected): {len(diagnostic_vulnerable_coordinates)}")
    print("Stable security acceptance granted: true")
    print("Stable promotion authorized: false")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SecurityEvidenceError as error:
        print(f"FAIL: {error}")
        raise SystemExit(1)
