#!/usr/bin/env python3
"""Build the deterministic, non-publishing GLAZE UI V1.6 final artifact candidate.

This builder prepares the bytes intended for the eventual GLAZE UI 1.6.0
release without publishing them and without changing repository lifecycle
authority. The repository remains at 1.6.0-rc.1 / current Stable 1.5.1 until
separate governed publication readback and Stable promotion complete.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import subprocess
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RC_VERSION = "1.6.0-rc.1"
TARGET_VERSION = "1.6.0"
TARGET_TAG = "v1.6.0"
ARCHIVE_NAME = f"glaze-ui-v{TARGET_VERSION}-source-runtime.tar.gz"
QUALIFICATION_SOURCE = "c7509c79256b04b0aa67cb9dd0737d7588e0ae4a"
QUALIFICATION_INTEGRATION = "354f5759385c28596fcfec26a3ad525e89fb1c35"
RULESET_ID = 23699829


class FinalArtifactError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FinalArtifactError(message)


def git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(rel: str) -> dict:
    path = ROOT / rel
    require(path.is_file(), f"missing required JSON source: {rel}")
    return json.loads(path.read_text(encoding="utf-8"))


def tracked_source_paths() -> list[str]:
    paths = {"LICENSE", "js/glaze-v1.6-development.mjs"}

    for path in sorted((ROOT / "js").glob("glaze-v1.6*.mjs")):
        if not path.is_file():
            continue
        rel = str(path.relative_to(ROOT))
        if rel in {"js/glaze-v1.6.0-rc.1.mjs", "js/glaze-v1.6.0.mjs"}:
            continue
        paths.add(rel)

    for path in sorted((ROOT / "contracts" / "v1.6").rglob("*")):
        if not path.is_file():
            continue
        rel = str(path.relative_to(ROOT))
        if rel in {
            "contracts/v1.6/release-candidate.json",
            "contracts/v1.6/stable-release.json",
        }:
            continue
        paths.add(rel)

    tracked = set(git("ls-files").splitlines())
    for rel in sorted(paths):
        require(rel in tracked, f"artifact source is not Git-tracked: {rel}")
        require((ROOT / rel).is_file(), f"artifact source is missing: {rel}")
    return sorted(paths)


def stable_wrapper() -> bytes:
    text = f"""/* GLAZE UI V1.6.0 — Stable release artifact entrypoint.
 *
 * This file is generated deterministically from the governed V1.6 Release
 * Candidate source. Its Stable identity becomes authoritative only after the
 * exact artifact bytes are security-accepted, immutably published, read back,
 * and followed by the separate repository lifecycle promotion.
 */

export * from './glaze-v1.6-development.mjs';

export const glazeV160 = Object.freeze({{
  version: '{TARGET_VERSION}',
  lifecycle: 'stable',
  stableBaseline: '1.5.1',
  releaseCandidateSource: '{RC_VERSION}',
  sourceQualificationAnchor: '{QUALIFICATION_SOURCE}',
  qualificationEvidenceIntegrationCommit: '{QUALIFICATION_INTEGRATION}',
  qualificationEvidenceComplete: true,
  verifiedQualificationLanes: 24,
  consumerEligible: true,
  presentationOnly: true,
  authorizationInferred: false,
  permissionRequestAutomatic: false,
  automaticNavigationAllowed: false,
  consequentialExecutionAutomatic: false,
  fallbackExecutionAutomatic: false,
  downstreamConsumerAcceptanceAutomatic: false,
  deploymentAcceptanceAutomatic: false,
  productionAcceptanceAutomatic: false,
  activationRequiresImmutablePublicationReadback: true,
  activationRequiresRepositoryLifecyclePromotion: true
}});
"""
    return text.encode("utf-8")


def stable_contract() -> bytes:
    contract = {
        "schemaVersion": 1,
        "contractId": "goreecloud.glaze-ui.v1.6.stable-release",
        "product": "GLAZE UI V1.6",
        "version": TARGET_VERSION,
        "releaseLifecycle": "Stable",
        "stableBaseline": "1.5.1",
        "releaseCandidateSource": RC_VERSION,
        "consumerEligible": True,
        "sourceQualificationAnchor": QUALIFICATION_SOURCE,
        "qualificationEvidenceIntegrationCommit": QUALIFICATION_INTEGRATION,
        "runtimeEntrypoint": "js/glaze-v1.6.0.mjs",
        "qualification": {
            "verifiedCount": 24,
            "unverifiedCount": 0,
            "notApplicableCount": 0,
            "evidenceComplete": True,
        },
        "authority": {
            "presentationOnly": True,
            "authorizationInferred": False,
            "permissionRequestAutomatic": False,
            "automaticNavigationAllowed": False,
            "consequentialExecutionAutomatic": False,
            "fallbackExecutionAutomatic": False,
            "downstreamConsumerAcceptanceAutomatic": False,
            "deploymentAcceptanceAutomatic": False,
            "productionAcceptanceAutomatic": False,
            "effectiveOnlyAfterImmutablePublicationReadback": True,
            "effectiveOnlyAfterRepositoryLifecyclePromotion": True,
        },
        "rollback": {
            "knownGoodStable": "1.5.1",
            "runtimeEntrypoint": "js/glaze-v1.5.1.mjs",
        },
        "boundary": (
            "This generated contract describes the intended GLAZE UI 1.6.0 "
            "Stable release artifact. It is not current repository authority "
            "until the exact artifact bytes pass final security acceptance, "
            "are immutably published and read back, and the separate lifecycle "
            "promotion is verified."
        ),
    }
    return (json.dumps(contract, indent=2, sort_keys=True) + "\n").encode("utf-8")


def build_archive(output_dir: Path, archive_files: dict[str, bytes]) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / ARCHIVE_NAME

    with tempfile.TemporaryDirectory(prefix="glaze-v16-final-artifact-") as tmp:
        tar_path = Path(tmp) / "artifact.tar"
        with tarfile.open(tar_path, "w", format=tarfile.PAX_FORMAT) as tar:
            for rel in sorted(archive_files):
                data = archive_files[rel]
                info = tarfile.TarInfo(name=f"glaze-ui-v{TARGET_VERSION}/{rel}")
                info.size = len(data)
                info.mode = 0o644
                info.mtime = 0
                info.uid = 0
                info.gid = 0
                info.uname = ""
                info.gname = ""
                tar.addfile(info, io.BytesIO(data))

        with tar_path.open("rb") as source, archive.open("wb") as target:
            with gzip.GzipFile(
                filename="",
                mode="wb",
                fileobj=target,
                compresslevel=9,
                mtime=0,
            ) as zipped:
                while True:
                    chunk = source.read(1024 * 1024)
                    if not chunk:
                        break
                    zipped.write(chunk)

    require(archive.is_file() and archive.stat().st_size > 0, "final artifact archive was not produced")
    return archive


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-sha", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    head = git("rev-parse", "HEAD")
    require(head == args.expected_sha, f"exact-head mismatch: checkout={head} expected={args.expected_sha}")
    require(len(head) == 40, "source revision must be a full commit SHA")
    tree = git("rev-parse", "HEAD^{tree}")

    lifecycle = load_json("registry/lifecycle.json")
    require(lifecycle.get("currentOfficial") == "1.5.1", "current Official must remain 1.5.1")
    require(lifecycle.get("currentStable") == "1.5.1", "current Stable must remain 1.5.1")
    require(lifecycle.get("activeCandidate") == RC_VERSION, "active V1.6 RC identity mismatch")

    review = load_json("acceptance/v1.6-stable-qualification-review.json")
    require(review.get("decision") == "blocked-remain-release-candidate", "Stable review must remain blocked during artifact preparation")
    require(review.get("stablePromotionAuthorized") is False, "artifact preparation must not authorize Stable")
    require(review.get("remainingBlockerCount") in (1, 2), "artifact preparation expects the governed pre- or post-security blocker count")
    protection = review.get("repositoryProtectionEvidence", {})
    require(protection.get("rulesetId") == RULESET_ID, "verified repository ruleset mismatch")
    require(protection.get("enforcement") == "active", "repository ruleset must be recorded active")
    require(protection.get("branchProtected") is True, "authoritative main protection must be verified")
    require(protection.get("bypassActors") == [], "repository protection bypass list must be empty")

    security = load_json("acceptance/v1.6-stable-security-review.json")
    require(security.get("repositorySecurityGateEnforcement", {}).get("result") == "passed", "repository security-gate enforcement must be passed")
    security_decision = security.get("overallDecision")
    require(security_decision in ("blocked", "passed"), "final Stable security review state is unsupported")
    selected_for_publication = False
    if security_decision == "blocked":
        require(security.get("stableSecurityAcceptanceGranted") is False, "pre-acceptance Stable security state must remain false")
        remaining_security = security.get("remainingReleaseSecurityBlockers", [])
        require(
            [item.get("id") for item in remaining_security] == ["final-artifact-source-provenance"],
            "pre-acceptance artifact/source provenance must be the only remaining release-security blocker",
        )
    else:
        require(security.get("stableSecurityAcceptanceGranted") is True, "post-acceptance Stable security state must remain true")
        require(security.get("remainingReleaseSecurityBlockers") == [], "post-acceptance Stable security blocker list must be empty")
        accepted = load_json("acceptance/v1.6-final-artifact-acceptance.json")
        accepted_source = accepted.get("candidate", {}).get("sourceRevision")
        require(accepted_source == "a7180679ea851389e0f3004515f9a25f420e716d", "accepted publication source mismatch")
        ancestry = subprocess.run(
            ["git", "merge-base", "--is-ancestor", accepted_source, head],
            cwd=ROOT,
            check=False,
        )
        require(ancestry.returncode == 0, "accepted publication source must be an ancestor of this build")
        selected_for_publication = head == accepted_source

    source_paths = tracked_source_paths()
    archive_files: dict[str, bytes] = {
        rel: (ROOT / rel).read_bytes()
        for rel in source_paths
    }
    archive_files["VERSION"] = f"{TARGET_VERSION}\n".encode("utf-8")
    archive_files["js/glaze-v1.6.0.mjs"] = stable_wrapper()
    archive_files["contracts/v1.6/stable-release.json"] = stable_contract()

    source_manifest = {
        "schemaVersion": 1,
        "product": "GLAZE UI V1.6",
        "targetVersion": TARGET_VERSION,
        "targetTag": TARGET_TAG,
        "sourceRevision": head,
        "sourceTree": tree,
        "sourceQualificationAnchor": QUALIFICATION_SOURCE,
        "qualificationEvidenceIntegrationCommit": QUALIFICATION_INTEGRATION,
        "selectedForPublication": selected_for_publication,
        "trackedSources": [
            {
                "path": rel,
                "size": len(archive_files[rel]),
                "sha256": sha256_bytes(archive_files[rel]),
            }
            for rel in source_paths
        ],
        "generatedReleaseFiles": [
            {
                "path": rel,
                "size": len(archive_files[rel]),
                "sha256": sha256_bytes(archive_files[rel]),
            }
            for rel in [
                "VERSION",
                "js/glaze-v1.6.0.mjs",
                "contracts/v1.6/stable-release.json",
            ]
        ],
    }
    archive_files["SOURCE_MANIFEST.json"] = (
        json.dumps(source_manifest, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    archive = build_archive(args.output_dir, archive_files)

    components = [
        {
            "type": "file",
            "bom-ref": f"file:{rel}",
            "name": rel,
            "hashes": [{"alg": "SHA-256", "content": sha256_bytes(data)}],
        }
        for rel, data in sorted(archive_files.items())
    ]
    component_ref = f"goreecloud:goreecloud-glaze-ui:{TARGET_VERSION}"
    sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "serialNumber": f"urn:uuid:00000000-0000-0000-0000-{head[:12]}",
        "version": 1,
        "metadata": {
            "component": {
                "type": "library",
                "bom-ref": component_ref,
                "name": "GLAZE UI",
                "version": TARGET_VERSION,
                "properties": [
                    {"name": "goreecloud.source.commit", "value": head},
                    {"name": "goreecloud.source.tree", "value": tree},
                    {"name": "goreecloud.release.candidate", "value": RC_VERSION},
                    {"name": "goreecloud.target.lifecycle", "value": "stable"},
                    {"name": "goreecloud.current.repository.lifecycle", "value": "release-candidate"},
                    {"name": "goreecloud.runtime.external-dependencies", "value": "0"},
                    {"name": "goreecloud.publication.authorized", "value": "false"},
                ],
            }
        },
        "components": components,
        "dependencies": [{"ref": component_ref, "dependsOn": []}],
    }
    sbom_path = args.output_dir / "cyclonedx-1.5.json"
    sbom_path.write_text(json.dumps(sbom, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    builder_rel = "scripts/build_glaze_v1_6_final_artifact.py"
    provenance = {
        "schemaVersion": 1,
        "kind": "goreecloud-glaze-v1.6-final-artifact-preparation",
        "product": "GLAZE UI V1.6",
        "currentRepositoryLifecycle": "release-candidate",
        "currentRepositoryVersion": RC_VERSION,
        "targetReleaseVersion": TARGET_VERSION,
        "intendedImmutableTag": TARGET_TAG,
        "finalStableArtifactCandidate": True,
        "selectedForPublication": selected_for_publication,
        "sourceRevision": head,
        "sourceTree": tree,
        "sourceQualificationAnchor": QUALIFICATION_SOURCE,
        "qualificationEvidenceIntegrationCommit": QUALIFICATION_INTEGRATION,
        "builder": {
            "path": builder_rel,
            "sha256": sha256_file(ROOT / builder_rel),
        },
        "archive": {
            "name": archive.name,
            "format": "tar+gzip",
            "size": archive.stat().st_size,
            "sha256": sha256_file(archive),
            "deterministic": True,
            "prefix": f"glaze-ui-v{TARGET_VERSION}/",
            "includedFileCount": len(archive_files),
        },
        "runtimeBoundary": {
            "entrypoint": "js/glaze-v1.6.0.mjs",
            "externalRuntimeDependencies": [],
            "selectedBuildToolDependencySecurityEvidence": "acceptance/v1.6-dependency-vulnerability-classification.json",
        },
        "repositoryProtection": {
            "rulesetId": RULESET_ID,
            "rulesetName": protection.get("rulesetName"),
            "enforcement": protection.get("enforcement"),
            "strictRequiredStatusChecksPolicy": protection.get("strictRequiredStatusChecksPolicy"),
            "requiredStatusChecks": protection.get("requiredStatusChecks"),
            "bypassActors": protection.get("bypassActors"),
        },
        "publication": {
            "authorized": False,
            "tagCreated": False,
            "githubReleaseCreated": False,
            "artifactPublished": False,
            "mustReuseTheseAcceptedBytes": True,
        },
        "lifecycleAuthority": {
            "stablePromotionAuthorized": False,
            "consumerEligibilityGrantedByThisBuild": False,
            "repositoryCurrentStableRemains": "1.5.1",
            "repositoryActiveCandidateRemains": RC_VERSION,
        },
        "rollback": {
            "knownGoodStable": "1.5.1",
            "runtimeEntrypoint": "js/glaze-v1.5.1.mjs",
        },
    }
    provenance_path = args.output_dir / "provenance.json"
    provenance_path.write_text(json.dumps(provenance, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    sums = {
        archive.name: sha256_file(archive),
        sbom_path.name: sha256_file(sbom_path),
        provenance_path.name: sha256_file(provenance_path),
    }
    sums_path = args.output_dir / "SHA256SUMS"
    sums_path.write_text(
        "".join(f"{digest}  {name}\n" for name, digest in sorted(sums.items())),
        encoding="utf-8",
    )

    summary = {
        "sourceRevision": head,
        "sourceTree": tree,
        "currentRepositoryVersion": RC_VERSION,
        "targetReleaseVersion": TARGET_VERSION,
        "intendedImmutableTag": TARGET_TAG,
        "archive": archive.name,
        "archiveSha256": sums[archive.name],
        "sbomSha256": sums[sbom_path.name],
        "provenanceSha256": sums[provenance_path.name],
        "includedFileCount": len(archive_files),
        "publicationAuthorized": False,
        "stablePromotionAuthorized": False,
        "mustReuseAcceptedArtifactBytesForPublication": True,
        "selectedForPublication": selected_for_publication,
    }
    (args.output_dir / "final-artifact-summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except FinalArtifactError as error:
        print(f"FAIL: {error}")
        raise SystemExit(1)
