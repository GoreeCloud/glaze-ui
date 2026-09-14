#!/usr/bin/env python3
"""Validate a downstream GoreeCloud consumer against the current Glaze UI Stable authority.

This gate is deliberately narrow: it proves that a consumer is targeting the current
central Stable release and that any claimed Glaze acceptance is backed by repository-local,
hash-bound evidence for every enumerated user-facing platform. It does not replace product,
security, privacy, accessibility, native-platform, performance, rollback, or release authority.
"""
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import tempfile
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
REPOSITORY = re.compile(r"^GoreeCloud/.+$")
PLACEHOLDERS = {"", "todo", "tbd", "unknown", "n/a", "na", "placeholder", "example", "none", "null"}
STATUSES = {"adoption-required", "unverified", "accepted-v1"}
PLATFORMS = {"web", "desktop", "mobile", "tablet", "tv", "smartwatch", "other-user-facing"}
PLATFORM_STATUSES = {"accepted", "pending", "unverified", "blocked"}
EXPECTED_KEYS = {
    "schemaVersion", "recordType", "consumerName", "repository", "targetVersion",
    "status", "stableClaim", "coverage", "platforms", "notes",
}


class GateError(RuntimeError):
    pass


def req(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def read_json(path: Path, label: str | None = None) -> dict[str, Any]:
    shown = label or str(path)
    req(path.is_file(), f"missing JSON file: {shown}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise GateError(f"invalid JSON {shown}: {exc}") from exc
    req(isinstance(value, dict), f"{shown} must contain a JSON object")
    return value


def meaningful(value: Any, label: str) -> str:
    req(isinstance(value, str), f"{label} must be a string")
    text = value.strip()
    req(text.lower() not in PLACEHOLDERS, f"{label} contains a placeholder value")
    req("REPLACE_WITH_" not in text, f"{label} contains an unresolved template placeholder")
    return text


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_repo_file(root: Path, relative: Any, label: str) -> Path:
    text = meaningful(relative, label)
    raw = Path(text)
    req(not raw.is_absolute(), f"{label} must be repository-relative")
    req(".." not in raw.parts, f"{label} may not traverse outside the repository")
    resolved_root = root.resolve()
    resolved = (resolved_root / raw).resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise GateError(f"{label} resolves outside the repository") from exc
    req(resolved.is_file(), f"{label} does not exist as a file: {text}")
    return resolved


def central_authority() -> tuple[str, dict[str, Any], dict[str, Any]]:
    stable = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    req(SEMVER.fullmatch(stable) is not None, "central VERSION must be semantic Stable version")
    lifecycle = read_json(ROOT / "registry/lifecycle.json", "registry/lifecycle.json")
    registry = read_json(ROOT / "consumers/registry.json", "consumers/registry.json")
    req(lifecycle.get("currentStable") == stable, "central lifecycle currentStable must match VERSION")
    req(lifecycle.get("currentOfficial") == stable, "central lifecycle currentOfficial must match VERSION")
    req(registry.get("officialBaseline") == stable, "consumer registry officialBaseline must match VERSION")
    req(registry.get("requiredConsumerVersion") == stable, "consumer registry requiredConsumerVersion must match VERSION")
    enforcement = registry.get("enforcement")
    req(isinstance(enforcement, dict), "consumer registry enforcement object is required")
    req(enforcement.get("officialCurrentRequired") is True, "central officialCurrentRequired must be true")
    req(enforcement.get("productionExceptionsAllowed") is False, "central productionExceptionsAllowed must be false")
    releases = lifecycle.get("releases")
    req(isinstance(releases, list), "central lifecycle releases must be an array")
    matches = [item for item in releases if isinstance(item, dict) and item.get("version") == stable]
    req(len(matches) == 1, "central lifecycle must contain exactly one current Stable release record")
    req(matches[0].get("status") == "stable", "current central release must have Stable status")
    req(matches[0].get("consumerEligible") is True, "current central Stable must be consumer-eligible")
    return stable, lifecycle, registry


def validate_schema_parity() -> None:
    schema = read_json(ROOT / "schemas/downstream-current-stable-conformance.schema.json")
    req(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "downstream schema must use Draft 2020-12")
    properties = schema.get("properties")
    req(isinstance(properties, dict), "downstream schema properties are required")
    req(set(schema.get("required", [])) == EXPECTED_KEYS, "downstream schema required-field set drifted")
    req(properties.get("schemaVersion", {}).get("const") == 1, "downstream schemaVersion must remain 1")
    req(properties.get("recordType", {}).get("const") == "goreecloud-glaze-ui-current-stable-conformance", "downstream recordType schema drifted")
    req(set(properties.get("status", {}).get("enum", [])) == STATUSES, "downstream status vocabulary drifted")
    platform_enum = schema.get("$defs", {}).get("platform", {}).get("properties", {}).get("id", {}).get("enum", [])
    req(set(platform_enum) == PLATFORMS, "downstream platform vocabulary drifted")
    platform_status = schema.get("$defs", {}).get("platform", {}).get("properties", {}).get("status", {}).get("enum", [])
    req(set(platform_status) == PLATFORM_STATUSES, "downstream platform-status vocabulary drifted")


def validate_manifest(
    manifest: dict[str, Any],
    *,
    consumer_root: Path,
    expected_repository: str | None,
    current_revision: str | None,
    force_stable_claim: bool,
) -> dict[str, Any]:
    stable, lifecycle, registry = central_authority()
    validate_schema_parity()

    req(set(manifest) == EXPECTED_KEYS, "manifest field set drifted")
    req(manifest.get("schemaVersion") == 1, "manifest schemaVersion must be 1")
    req(manifest.get("recordType") == "goreecloud-glaze-ui-current-stable-conformance", "manifest recordType mismatch")
    meaningful(manifest.get("consumerName"), "consumerName")
    repository = meaningful(manifest.get("repository"), "repository")
    req(REPOSITORY.fullmatch(repository) is not None, "repository must be a GoreeCloud owner/name identifier")
    if expected_repository is not None:
        req(repository == expected_repository, f"manifest repository {repository} does not match workflow repository {expected_repository}")

    target = manifest.get("targetVersion")
    req(isinstance(target, str) and SEMVER.fullmatch(target) is not None, "targetVersion must be semantic version")
    req(target == stable, f"consumer targets Glaze UI {target}; current required Stable is {stable}")

    status = manifest.get("status")
    req(status in STATUSES, "manifest status is invalid")
    stable_claim = manifest.get("stableClaim")
    req(isinstance(stable_claim, bool), "stableClaim must be boolean")
    strict_stable = force_stable_claim or stable_claim
    if force_stable_claim:
        req(stable_claim is True, "Stable-claim workflow mode requires manifest stableClaim=true")

    coverage = manifest.get("coverage")
    req(isinstance(coverage, dict), "coverage must be an object")
    req(set(coverage) == {"allUserFacingPlatformsEnumerated", "statement"}, "coverage field set drifted")
    all_enumerated = coverage.get("allUserFacingPlatformsEnumerated")
    req(isinstance(all_enumerated, bool), "coverage.allUserFacingPlatformsEnumerated must be boolean")
    meaningful(coverage.get("statement"), "coverage.statement")

    platforms = manifest.get("platforms")
    req(isinstance(platforms, list) and platforms, "platforms must be a non-empty array")
    seen: set[str] = set()
    normalized: list[dict[str, Any]] = []
    accepted_count = 0
    for index, item in enumerate(platforms):
        label = f"platforms[{index}]"
        req(isinstance(item, dict), f"{label} must be an object")
        req(set(item) == {"id", "status", "evidence"}, f"{label} field set drifted")
        platform = item.get("id")
        req(platform in PLATFORMS, f"{label}.id is invalid")
        req(platform not in seen, f"duplicate platform declaration: {platform}")
        seen.add(platform)
        platform_status = item.get("status")
        req(platform_status in PLATFORM_STATUSES, f"{label}.status is invalid")
        evidence = item.get("evidence")
        evidence_report = None
        if evidence is not None:
            req(isinstance(evidence, dict), f"{label}.evidence must be object or null")
            req(set(evidence) == {"path", "sha256"}, f"{label}.evidence field set drifted")
            expected_hash = meaningful(evidence.get("sha256"), f"{label}.evidence.sha256")
            req(SHA256.fullmatch(expected_hash) is not None, f"{label}.evidence.sha256 must be 64 lowercase hex characters")
            evidence_path = safe_repo_file(consumer_root, evidence.get("path"), f"{label}.evidence.path")
            actual_hash = sha256_file(evidence_path)
            req(actual_hash == expected_hash, f"{platform} evidence hash mismatch: expected {expected_hash}, got {actual_hash}")
            evidence_report = {"path": str(evidence.get("path")), "sha256": actual_hash}
        if platform_status == "accepted":
            accepted_count += 1
            req(evidence_report is not None, f"accepted platform {platform} requires repository-local hash-bound evidence")
        normalized.append({"id": platform, "status": platform_status, "evidence": evidence_report})

    if status == "accepted-v1":
        req(all_enumerated is True, "accepted-v1 requires an explicit assertion that all user-facing platforms are enumerated")
        req(accepted_count == len(platforms), "accepted-v1 requires every enumerated user-facing platform to be accepted")
    else:
        req(stable_claim is False, f"status {status} cannot carry stableClaim=true")

    if strict_stable:
        req(status == "accepted-v1", "Stable claim requires status=accepted-v1")
        req(all_enumerated is True, "Stable claim requires complete user-facing platform enumeration")
        req(accepted_count == len(platforms), "Stable claim requires every user-facing platform to have accepted current-Stable Glaze evidence")

    meaningful(manifest.get("notes"), "notes")
    if current_revision is not None:
        req(SHA40.fullmatch(current_revision) is not None, "workflow source revision must be 40 lowercase hex characters")

    return {
        "schemaVersion": 1,
        "recordType": "goreecloud-glaze-ui-current-stable-gate-report",
        "verifiedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "repository": repository,
        "sourceRevision": current_revision,
        "consumerName": manifest["consumerName"],
        "glazeUi": {
            "currentStable": stable,
            "currentOfficial": lifecycle.get("currentOfficial"),
            "requiredConsumerVersion": registry.get("requiredConsumerVersion"),
            "targetVersion": target,
        },
        "stableClaimRequested": strict_stable,
        "coverage": {
            "allUserFacingPlatformsEnumerated": all_enumerated,
            "platformCount": len(platforms),
            "acceptedPlatformCount": accepted_count,
        },
        "platforms": normalized,
        "decision": "pass",
        "authorityBoundary": "This report proves only current-Stable Glaze UI targeting and declared repository-local Glaze evidence integrity. Product Stable/production authority remains independent.",
    }


def sample_manifest(root: Path, stable: str) -> dict[str, Any]:
    evidence_path = root / "acceptance" / "glaze.json"
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_path.write_text('{"synthetic":true,"acceptance":false}\n', encoding="utf-8")
    digest = sha256_file(evidence_path)
    return {
        "schemaVersion": 1,
        "recordType": "goreecloud-glaze-ui-current-stable-conformance",
        "consumerName": "Synthetic Consumer",
        "repository": "GoreeCloud/synthetic-consumer",
        "targetVersion": stable,
        "status": "accepted-v1",
        "stableClaim": True,
        "coverage": {
            "allUserFacingPlatformsEnumerated": True,
            "statement": "Synthetic self-test declares one synthetic web surface; this is not product evidence.",
        },
        "platforms": [
            {
                "id": "web",
                "status": "accepted",
                "evidence": {"path": "acceptance/glaze.json", "sha256": digest},
            }
        ],
        "notes": "Synthetic validator self-test only; never downstream acceptance evidence.",
    }


def expect_reject(manifest: dict[str, Any], root: Path, label: str, *, force_stable: bool = False, repository: str = "GoreeCloud/synthetic-consumer") -> None:
    try:
        validate_manifest(
            manifest,
            consumer_root=root,
            expected_repository=repository,
            current_revision="a" * 40,
            force_stable_claim=force_stable,
        )
    except GateError:
        return
    raise GateError(f"self-test expected rejection but accepted {label}")


def self_test() -> None:
    stable, _, _ = central_authority()
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        valid = sample_manifest(root, stable)
        validate_manifest(valid, consumer_root=root, expected_repository=valid["repository"], current_revision="a" * 40, force_stable_claim=True)

        stale = copy.deepcopy(valid)
        stale["targetVersion"] = "0.0.0" if stable != "0.0.0" else "9.9.9"
        expect_reject(stale, root, "stale target", force_stable=True)

        pending = copy.deepcopy(valid)
        pending["status"] = "adoption-required"
        pending["stableClaim"] = False
        pending["platforms"][0]["status"] = "pending"
        pending["platforms"][0]["evidence"] = None
        expect_reject(pending, root, "forced Stable claim against pending adoption", force_stable=True)

        missing_coverage = copy.deepcopy(valid)
        missing_coverage["coverage"]["allUserFacingPlatformsEnumerated"] = False
        expect_reject(missing_coverage, root, "incomplete Stable platform coverage", force_stable=True)

        no_evidence = copy.deepcopy(valid)
        no_evidence["platforms"][0]["evidence"] = None
        expect_reject(no_evidence, root, "accepted platform without evidence", force_stable=True)

        bad_hash = copy.deepcopy(valid)
        bad_hash["platforms"][0]["evidence"]["sha256"] = "0" * 64
        expect_reject(bad_hash, root, "evidence hash mismatch", force_stable=True)

        duplicate = copy.deepcopy(valid)
        duplicate["platforms"].append(copy.deepcopy(duplicate["platforms"][0]))
        expect_reject(duplicate, root, "duplicate platform", force_stable=True)

        traversal = copy.deepcopy(valid)
        traversal["platforms"][0]["evidence"]["path"] = "../outside.json"
        expect_reject(traversal, root, "evidence path traversal", force_stable=True)

        wrong_repo = copy.deepcopy(valid)
        expect_reject(wrong_repo, root, "repository mismatch", force_stable=True, repository="GoreeCloud/other")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--consumer-root", type=Path)
    parser.add_argument("--repository")
    parser.add_argument("--revision")
    parser.add_argument("--stable-claim", action="store_true")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--source-only", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    stable, _, _ = central_authority()
    validate_schema_parity()
    print(f"Current Glaze UI consumer authority validated: {stable}")

    if args.self_test:
        self_test()
        print("Downstream current-Stable gate synthetic self-test passed. Synthetic data is not consumer acceptance evidence.")

    if args.manifest:
        consumer_root = (args.consumer_root or args.manifest.parent).expanduser().resolve()
        manifest_path = args.manifest.expanduser().resolve()
        manifest = read_json(manifest_path, str(manifest_path))
        report = validate_manifest(
            manifest,
            consumer_root=consumer_root,
            expected_repository=args.repository,
            current_revision=args.revision,
            force_stable_claim=args.stable_claim,
        )
        report["manifestSha256"] = sha256_file(manifest_path)
        if args.report:
            report_path = args.report.expanduser().resolve()
            report_path.parent.mkdir(parents=True, exist_ok=True)
            report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            print(f"Wrote Glaze UI current-Stable gate report: {report_path}")
        mode = "Stable-claim" if report["stableClaimRequested"] else "current-target"
        print(f"{mode} Glaze UI gate passed for {report['repository']} at target {stable}")
        print("Product Stable/production eligibility remains independently governed.")
    elif not args.self_test and not args.source_only:
        print("No downstream manifest supplied; source protocol only was validated.")


if __name__ == "__main__":
    try:
        main()
    except GateError as exc:
        raise SystemExit(f"Glaze UI downstream current-Stable gate failed: {exc}")
