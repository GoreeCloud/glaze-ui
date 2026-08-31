#!/usr/bin/env python3
"""Validate mandatory Glaze UI 2.1 Stable consumer migration state and guidance."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
SHA40 = re.compile(r"^[0-9a-f]{40}$")
CONSUMER_LINE = re.compile(r"^- \*\*(?P<name>[^*]+)\*\* — (?P<body>.+)$")
EXPECTED = {
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


def req(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Glaze UI consumer registry validation failed: {message}")


def version_tuple(version: str) -> tuple[int, ...]:
    return tuple(map(int, version.split(".")))


def validate_guidance(data: dict[str, object], stable: str) -> None:
    guidance = (ROOT / "CONSUMERS.md").read_text(encoding="utf-8")
    req(
        f"Glaze UI **{stable}** is the current Stable baseline" in guidance,
        "CONSUMERS.md must identify the current Stable baseline",
    )
    req(
        f"only Glaze UI version that may satisfy current GoreeCloud application conformance" in guidance,
        "CONSUMERS.md must state the current-Stable production rule",
    )
    req(
        "No production exception" in guidance and "grandfathering rule" in guidance,
        "CONSUMERS.md must preserve the no-exception rule",
    )
    req(
        "2.0.0 as the current Stable" not in guidance,
        "CONSUMERS.md must not describe 2.0.0 as current Stable",
    )
    req(
        "2.1 as Candidate" not in guidance,
        "CONSUMERS.md must not describe promoted 2.1 as the current Candidate baseline",
    )

    assessment = data.get("candidateAssessment", {})
    req(isinstance(assessment, dict), "candidate assessment type")
    candidate = assessment.get("version")
    req(
        isinstance(candidate, str) and candidate in guidance,
        "CONSUMERS.md must preserve Candidate promotion provenance",
    )
    req(
        "historical readiness evidence only" in guidance,
        "CONSUMERS.md must keep Candidate evidence historical",
    )

    documented: dict[str, str] = {}
    for line in guidance.splitlines():
        match = CONSUMER_LINE.match(line.strip())
        if match:
            name = match.group("name")
            req(name not in documented, f"duplicate CONSUMERS.md entry for {name}")
            documented[name] = match.group("body")

    consumers = data.get("consumers", [])
    req(isinstance(consumers, list), "consumers list type")
    expected_names = {str(consumer.get("name")) for consumer in consumers if isinstance(consumer, dict)}
    req(set(documented) == expected_names, "CONSUMERS.md audited consumer set drift")

    for consumer in consumers:
        req(isinstance(consumer, dict), "consumer entry type")
        name = str(consumer.get("name"))
        status = str(consumer.get("status"))
        body = documented[name]
        req(f"`{status}`" in body, f"{name} documented status")
        if status == "migration-required":
            target = str(consumer.get("targetVersion"))
            req(f"recorded {target}" in body, f"{name} documented historical target")
            req(f"required {stable}" in body, f"{name} documented Stable target")
        elif status == "unverified":
            req("fresh repository-local 2.1" in body, f"{name} unverified evidence boundary")
        else:
            req(False, f"unsupported documented consumer status for {name}")


def main() -> None:
    stable = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    req(stable == "2.1.0", "Stable must be 2.1.0")

    data = json.loads((ROOT / "consumers/registry.json").read_text(encoding="utf-8"))
    lifecycle = json.loads((ROOT / "registry/lifecycle.json").read_text(encoding="utf-8"))

    req(data.get("schemaVersion") == 4, "schemaVersion")
    req(
        data.get("stableBaseline") == stable
        and data.get("requiredConsumerVersion") == stable,
        "Stable target",
    )

    historical = data.get("historicalStableVersions", [])
    req(
        isinstance(historical, list)
        and "2.0.0" in historical
        and all(isinstance(version, str) and SEMVER.fullmatch(version) for version in historical),
        "historical Stable list",
    )
    req(
        all(version_tuple(version) < version_tuple(stable) for version in historical),
        "historical versions must precede Stable",
    )

    req(
        lifecycle.get("currentStable") == stable and lifecycle.get("activeCandidate") is None,
        "lifecycle Stable state",
    )
    stable_release = [
        release
        for release in lifecycle.get("releases", [])
        if release.get("version") == stable
    ]
    req(
        len(stable_release) == 1 and stable_release[0].get("status") == "stable",
        "Stable release record",
    )
    promoted = stable_release[0].get("promotedFromCandidate")
    req(promoted == "2.1.0-candidate.1", "promotion source")

    assessment = data.get("candidateAssessment", {})
    req(
        assessment.get("version") == promoted and assessment.get("lifecycle") == "candidate",
        "preserved Candidate assessment",
    )
    req(
        assessment.get("consumerEligible") is False
        and assessment.get("productionEligible") is False,
        "Candidate assessment boundary",
    )

    consumers = data.get("consumers", [])
    seen: set[str] = set()
    for consumer in consumers:
        repo = consumer.get("repository")
        req(repo in EXPECTED and repo not in seen, f"invalid/duplicate {repo}")
        seen.add(repo)
        req(
            consumer.get("requiredTargetVersion") == stable,
            f"{repo} required target",
        )
        req(consumer.get("productionEligible") is False, f"{repo} must not auto-promote")

        status = consumer.get("status")
        target = consumer.get("targetVersion")
        if status == "migration-required":
            req(
                isinstance(target, str) and target in historical,
                f"{repo} migration source",
            )
            req(
                SHA40.fullmatch(str(consumer.get("referenceRevision", ""))) is not None,
                f"{repo} revision",
            )
            req(
                consumer.get("automatedContract") is True and consumer.get("evidence"),
                f"{repo} evidence",
            )
        elif status == "unverified":
            req(
                target is None
                and consumer.get("referenceRevision") is None
                and consumer.get("evidence") is None
                and consumer.get("automatedContract") is False,
                f"{repo} unverified boundary",
            )
        else:
            req(
                False,
                f"{repo} must remain migration-required or unverified immediately after Stable promotion",
            )

    req(seen == EXPECTED, "audit scope drift")
    validate_guidance(data, stable)
    print(
        f"Glaze UI consumer registry and guidance validated: {len(consumers)} consumers "
        f"require Stable {stable}; none auto-promoted"
    )


if __name__ == "__main__":
    main()
