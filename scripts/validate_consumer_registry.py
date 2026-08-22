#!/usr/bin/env python3
"""Validate the central Glaze UI consumer compatibility registry."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "consumers" / "registry.json"
CONSUMERS_DOC = ROOT / "CONSUMERS.md"
VERSION = ROOT / "VERSION"
ALLOWED_STATUS = {
    "aligned-current-stable",
    "aligned-older-stable",
    "adoption-candidate",
    "unverified",
}
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
SHA40 = re.compile(r"^[0-9a-f]{40}$")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Glaze UI consumer registry validation failed: {message}")


def version_tuple(value: str) -> tuple[int, int, int]:
    require(SEMVER.fullmatch(value) is not None, f"invalid semantic version: {value}")
    return tuple(int(part) for part in value.split("."))


def require_versioned_evidence(name: str, target, revision, evidence, automated: bool) -> None:
    require(isinstance(target, str) and SEMVER.fullmatch(target) is not None, f"versioned consumer {name} needs a semantic target version")
    require(isinstance(revision, str) and SHA40.fullmatch(revision) is not None, f"versioned consumer {name} needs a 40-character reviewed revision")
    require(isinstance(evidence, str) and evidence.strip(), f"versioned consumer {name} needs repository-local evidence")
    require(automated, f"versioned consumer {name} must record an automated contract")


def main() -> None:
    require(REGISTRY.is_file(), "missing consumers/registry.json")
    require(CONSUMERS_DOC.is_file(), "missing CONSUMERS.md")
    require(VERSION.is_file(), "missing VERSION")

    stable_version = VERSION.read_text(encoding="utf-8").strip()
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    consumer_doc = CONSUMERS_DOC.read_text(encoding="utf-8")

    for marker in (
        "Aligned — current Stable",
        "Aligned — older Stable",
        "Adoption Candidate",
        "Unverified",
        "consumers/registry.json",
        "must not silently depend on Candidate or Experimental",
    ):
        require(marker in consumer_doc, f"CONSUMERS.md missing required contract marker: {marker}")

    require(data.get("schemaVersion") == 1, "unsupported registry schemaVersion")
    require(data.get("stableBaseline") == stable_version, "registry Stable baseline differs from VERSION")
    require(set(data.get("statusVocabulary", [])) == ALLOWED_STATUS, "status vocabulary differs from canonical lifecycle")
    require(re.fullmatch(r"\d{4}-\d{2}-\d{2}", data.get("auditedAt", "")) is not None, "auditedAt must use YYYY-MM-DD")

    consumers = data.get("consumers")
    require(isinstance(consumers, list) and consumers, "consumer registry must contain at least one audited consumer")

    repositories: set[str] = set()
    names: set[str] = set()
    for consumer in consumers:
        require(isinstance(consumer, dict), "every consumer entry must be an object")
        name = consumer.get("name")
        repository = consumer.get("repository")
        status = consumer.get("status")
        target = consumer.get("targetVersion")
        revision = consumer.get("referenceRevision")
        evidence = consumer.get("evidence")
        automated = consumer.get("automatedContract")
        acceptance = consumer.get("visualAcceptance")
        notes = consumer.get("notes")

        require(isinstance(name, str) and name.strip(), "consumer name is missing")
        require(isinstance(repository, str) and repository.startswith("GoreeCloud/"), f"invalid repository for {name}")
        require(repository not in repositories, f"duplicate consumer repository: {repository}")
        require(name not in names, f"duplicate consumer name: {name}")
        repositories.add(repository)
        names.add(name)

        require(status in ALLOWED_STATUS, f"invalid status for {name}: {status}")
        require(isinstance(automated, bool), f"automatedContract must be boolean for {name}")
        require(isinstance(acceptance, str) and acceptance.strip(), f"visualAcceptance is missing for {name}")
        require(isinstance(notes, str) and notes.strip(), f"notes are missing for {name}")

        if status == "aligned-current-stable":
            require_versioned_evidence(name, target, revision, evidence, automated)
            require(target == stable_version, f"current-Stable consumer {name} must target {stable_version}")
        elif status == "aligned-older-stable":
            require_versioned_evidence(name, target, revision, evidence, automated)
            require(version_tuple(target) < version_tuple(stable_version), f"older-Stable consumer {name} must target a version older than {stable_version}")
        elif status == "adoption-candidate":
            require_versioned_evidence(name, target, revision, evidence, automated)
            require(target == stable_version, f"Adoption Candidate {name} must target current Stable {stable_version}")
            lowered_acceptance = acceptance.lower()
            require(
                any(marker in lowered_acceptance for marker in ("pending", "required", "not complete", "not established")),
                f"Adoption Candidate {name} must retain an explicit incomplete final-acceptance boundary",
            )
        else:
            require(target is None, f"unverified consumer {name} must not claim a target version")
            require(revision is None, f"unverified consumer {name} must not claim a reviewed revision")
            require(evidence is None, f"unverified consumer {name} must not claim repository-local conformance evidence")
            require(not automated, f"unverified consumer {name} must not claim an automated Glaze contract")

    require("GoreeCloud/goreecloud-manager" in repositories, "initial registry must retain GoreeCloud Manager")
    require("GoreeCloud/goreecloud-website" in repositories, "initial registry must retain GoreeCloud Website")

    print(f"Glaze UI consumer registry validated: {len(consumers)} audited consumers; Stable baseline {stable_version}")


if __name__ == "__main__":
    main()
