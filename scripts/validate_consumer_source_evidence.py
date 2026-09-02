#!/usr/bin/env python3
"""Verify current-Stable consumer claims against immutable downstream source revisions."""
from __future__ import annotations

import json
import re
from pathlib import Path, PurePosixPath
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SHA40 = re.compile(r"^[0-9a-f]{40}$")
REPOSITORY = re.compile(r"^GoreeCloud/[A-Za-z0-9_.-]+$")
MAX_SOURCE_BYTES = 1_000_000
TIMEOUT_SECONDS = 15
USER_AGENT = "goreecloud-glaze-ui-consumer-evidence-validator/1"


def fail(message: str) -> None:
    raise SystemExit(f"Glaze UI consumer source evidence validation failed: {message}")


def req(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def safe_path(value: object, label: str) -> str:
    req(isinstance(value, str) and bool(value), f"{label} must be a non-empty path")
    path = PurePosixPath(value)
    req(not path.is_absolute(), f"{label} must be repository-relative")
    req(".." not in path.parts and "." not in path.parts, f"{label} contains unsafe traversal")
    req(":" not in value and "\\" not in value, f"{label} contains unsupported path syntax")
    return value


def fetch_exact_source(repository: str, revision: str, path: str) -> str:
    owner, name = repository.split("/", 1)
    url = (
        "https://raw.githubusercontent.com/"
        f"{quote(owner, safe='')}/{quote(name, safe='')}/{quote(revision, safe='')}/"
        f"{quote(path, safe='/')}"
    )
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/plain"})
    try:
        with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            req(getattr(response, "status", 200) == 200, f"unexpected HTTP status for {repository}@{revision}:{path}")
            payload = response.read(MAX_SOURCE_BYTES + 1)
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        fail(f"cannot retrieve {repository}@{revision}:{path}: {exc}")
    req(len(payload) <= MAX_SOURCE_BYTES, f"source evidence exceeds {MAX_SOURCE_BYTES} bytes: {repository}@{revision}:{path}")
    try:
        return payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail(f"source evidence is not UTF-8: {repository}@{revision}:{path}: {exc}")


def validate_candidate(consumer: dict[str, object], stable: str, historical: list[str]) -> None:
    repository = str(consumer.get("repository", ""))
    revision = str(consumer.get("referenceRevision", ""))
    req(REPOSITORY.fullmatch(repository) is not None, f"invalid repository for current-Stable evidence: {repository}")
    req(SHA40.fullmatch(revision) is not None, f"invalid exact revision for {repository}")

    evidence_path = safe_path(consumer.get("evidence"), f"{repository} evidence")
    contract_path = safe_path(consumer.get("automatedContractPath"), f"{repository} automated contract")
    req(evidence_path != contract_path, f"{repository} evidence and automated contract must be distinct files")

    evidence = fetch_exact_source(repository, revision, evidence_path)
    contract = fetch_exact_source(repository, revision, contract_path)

    required_evidence = (
        "Status: **Adoption Candidate**",
        f"Required Stable baseline: **Glaze UI {stable}**",
        "Production eligible on the Glaze UI gate: **no**",
        f"Glaze UI {stable} Stable is the production design-system authority.",
    )
    for marker in required_evidence:
        req(marker in evidence, f"{repository} exact evidence missing current-Stable marker: {marker}")

    for version in historical:
        stale_marker = f"Required Stable baseline: **Glaze UI {version}**"
        req(stale_marker not in evidence, f"{repository} exact evidence still declares superseded baseline {version}")

    required_contract = (
        evidence_path,
        stable,
        "Adoption Candidate",
        "Production eligible on the Glaze UI gate: **no**",
    )
    for marker in required_contract:
        req(marker in contract, f"{repository} automated contract does not enforce exact current-Stable evidence marker: {marker}")


def main() -> None:
    stable = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    registry = json.loads((ROOT / "consumers/registry.json").read_text(encoding="utf-8"))
    req(registry.get("stableBaseline") == stable and registry.get("requiredConsumerVersion") == stable, "registry Stable baseline differs from VERSION")

    historical = registry.get("historicalStableVersions", [])
    req(isinstance(historical, list) and all(isinstance(version, str) for version in historical), "historical Stable versions")

    consumers = registry.get("consumers", [])
    req(isinstance(consumers, list), "consumer list")
    candidates = [consumer for consumer in consumers if isinstance(consumer, dict) and consumer.get("status") == "adoption-candidate"]
    req(bool(candidates), "at least one evidence-backed Adoption Candidate is required")

    for consumer in candidates:
        req(consumer.get("targetVersion") == stable, f"{consumer.get('repository')} Adoption Candidate target differs from current Stable")
        req(consumer.get("automatedContract") is True, f"{consumer.get('repository')} Adoption Candidate must have an automated contract")
        req(consumer.get("productionEligible") is False, f"{consumer.get('repository')} Adoption Candidate cannot be production eligible")
        validate_candidate(consumer, stable, historical)

    print(
        "Glaze UI exact consumer source evidence validated: "
        f"{len(candidates)} Adoption Candidate(s) independently match immutable downstream {stable} evidence and automated contracts."
    )


if __name__ == "__main__":
    main()
