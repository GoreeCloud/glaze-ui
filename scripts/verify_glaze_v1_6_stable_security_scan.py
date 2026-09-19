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
    parser.add_argument("--osv-report", required=True)
    parser.add_argument("--sbom", required=True)
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

    gitleaks = load_json(Path(args.gitleaks_report))
    require(isinstance(gitleaks, list), "Gitleaks JSON report must be a list")
    secret_findings = len(gitleaks)
    require(secret_findings == 0, f"Gitleaks found {secret_findings} potential secret finding(s)")

    osv = load_json(Path(args.osv_report))
    package_count, vulnerability_ids = summarize_osv(osv)
    require(package_count > 0, "OSV scan discovered zero dependency packages; coverage is not established")
    require(
        not vulnerability_ids,
        "known dependency vulnerabilities found: " + ", ".join(vulnerability_ids),
    )

    sbom = load_json(Path(args.sbom))
    require(sbom.get("bomFormat") == "CycloneDX", "SBOM must use CycloneDX")
    require(sbom.get("specVersion") == "1.5", "SBOM must use CycloneDX 1.5")
    components = sbom.get("components", [])
    require(isinstance(components, list) and components, "CycloneDX SBOM contains no components")
    sbom_vulnerabilities = sbom.get("vulnerabilities", [])
    require(isinstance(sbom_vulnerabilities, list), "CycloneDX vulnerabilities must be a list")
    require(not sbom_vulnerabilities, "CycloneDX SBOM reports known vulnerabilities")

    for label, digest in (
        ("gitleaks", args.gitleaks_sha256),
        ("osv-scanner", args.osv_sha256),
        ("gradle", args.gradle_sha256),
    ):
        require(re.fullmatch(r"[0-9a-f]{64}", digest) is not None, f"{label} SHA-256 must be lowercase hex")

    output = {
        "schemaVersion": 1,
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
            "scope": "complete fetched Git history for the exact repository checkout",
            "findingCount": secret_findings,
            "result": "passed",
        },
        "dependencyVulnerabilityScan": {
            "tool": "osv-scanner",
            "version": args.osv_version,
            "binarySha256": args.osv_sha256,
            "input": "generated Gradle verification metadata plus recursively discovered supported lockfiles/manifests",
            "packageCount": package_count,
            "vulnerabilityIds": vulnerability_ids,
            "result": "passed",
        },
        "sbom": {
            "format": "CycloneDX",
            "specVersion": "1.5",
            "componentCount": len(components),
            "vulnerabilityCount": len(sbom_vulnerabilities),
            "result": "passed",
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
        "limitations": [
            "This record proves the scanners completed successfully for the exact checked-out revision and their discoverable dependency inputs; it does not prove that advisory databases contain every vulnerability.",
            "The primary Glaze UI JavaScript runtime has no npm/pnpm/yarn or Python package manifest in this repository; Android/Wear dependencies are resolved from the buildable reference projects into verification metadata for scanning.",
            "Passing security scans do not grant Stable, production readiness, production acceptance, publication, or downstream consumer acceptance.",
        ],
        "generatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("GLAZE UI V1.6 Stable security scan evidence: PASS")
    print(f"Exact revision: {head}")
    print(f"Secret findings: {secret_findings}")
    print(f"Dependency packages scanned: {package_count}")
    print("Known dependency vulnerabilities: 0")
    print(f"CycloneDX components: {len(components)}")
    print("Stable promotion authorized: false")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SecurityEvidenceError as error:
        print(f"FAIL: {error}")
        raise SystemExit(1)
