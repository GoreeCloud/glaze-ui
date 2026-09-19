#!/usr/bin/env python3
"""Build deterministic, non-publishing GLAZE UI V1.6 RC artifact evidence.

This is a release-preparation rehearsal only. It must not create a tag, GitHub
Release, Stable lifecycle state, consumer eligibility, deployment, or production
acceptance.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.6.0-rc.1"
ARCHIVE_NAME = f"glaze-ui-v{VERSION}-source-runtime.tar.gz"


class ArtifactEvidenceError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ArtifactEvidenceError(message)


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


def collect_files() -> list[str]:
    fixed = [
        "LICENSE",
        "README.md",
        "SECURITY.md",
        "VERSION",
        "GLAZE_UI_V1_6_PLANNED.md",
        "goreecloud.platform.yaml",
        "registry/lifecycle.json",
        "acceptance/v1.6-qualification-review.json",
        "acceptance/v1.6-production-readiness-review.json",
        "acceptance/v1.6-production-applicability.json",
        "acceptance/v1.6-rc.1.json",
        "contracts/v1.6/release-candidate.json",
    ]

    dynamic = []
    dynamic.extend(
        str(path.relative_to(ROOT))
        for path in sorted((ROOT / "js").glob("glaze-v1.6*.mjs"))
        if path.is_file()
    )
    dynamic.extend(
        str(path.relative_to(ROOT))
        for path in sorted((ROOT / "contracts" / "v1.6").rglob("*"))
        if path.is_file()
    )

    paths = sorted(set(fixed + dynamic))
    require(paths, "release artifact file set is empty")

    tracked = set(git("ls-files").splitlines())
    for rel in paths:
        path = ROOT / rel
        require(path.is_file(), f"required artifact source is missing: {rel}")
        require(rel in tracked, f"artifact source is not Git-tracked: {rel}")
    return paths


def build_archive(output_dir: Path, paths: list[str]) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / ARCHIVE_NAME

    with tempfile.TemporaryDirectory(prefix="glaze-v16-artifact-") as tmp:
        tar_path = Path(tmp) / "artifact.tar"
        with tar_path.open("wb") as handle:
            subprocess.run(
                [
                    "git",
                    "archive",
                    "--format=tar",
                    f"--prefix=glaze-ui-v{VERSION}/",
                    "HEAD",
                    "--",
                    *paths,
                ],
                cwd=ROOT,
                check=True,
                stdout=handle,
            )

        with tar_path.open("rb") as source, archive.open("wb") as target:
            with gzip.GzipFile(
                filename="",
                mode="wb",
                fileobj=target,
                compresslevel=9,
                mtime=0,
            ) as zipped:
                shutil.copyfileobj(source, zipped)

    require(archive.is_file() and archive.stat().st_size > 0, "artifact archive was not produced")
    return archive


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-sha", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    head = git("rev-parse", "HEAD")
    require(head == args.expected_sha, f"exact-head mismatch: checkout={head} expected={args.expected_sha}")
    tree = git("rev-parse", "HEAD^{tree}")

    lifecycle = json.loads((ROOT / "registry/lifecycle.json").read_text(encoding="utf-8"))
    require(lifecycle.get("currentOfficial") == "1.5.1", "current Official must remain 1.5.1")
    require(lifecycle.get("currentStable") == "1.5.1", "current Stable must remain 1.5.1")
    require(lifecycle.get("activeCandidate") == VERSION, "active V1.6 RC identity mismatch")

    rc = json.loads((ROOT / "contracts/v1.6/release-candidate.json").read_text(encoding="utf-8"))
    require(rc.get("version") == VERSION, "V1.6 RC contract version mismatch")
    require(rc.get("releaseLifecycle") == "Release Candidate", "artifact rehearsal must remain Release Candidate")
    require(rc.get("consumerEligible") is False, "artifact rehearsal must not grant consumer eligibility")

    files = collect_files()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    archive = build_archive(args.output_dir, files)

    included = []
    for rel in files:
        path = ROOT / rel
        included.append({
            "path": rel,
            "size": path.stat().st_size,
            "sha256": sha256_file(path),
        })

    component_ref = f"goreecloud:goreecloud-glaze-ui:{VERSION}"
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
                "version": VERSION,
                "properties": [
                    {"name": "goreecloud.source.commit", "value": head},
                    {"name": "goreecloud.source.tree", "value": tree},
                    {"name": "goreecloud.lifecycle", "value": "release-candidate"},
                    {"name": "goreecloud.stable-baseline", "value": "1.5.1"},
                    {"name": "goreecloud.runtime.external-dependencies", "value": "0"},
                    {"name": "goreecloud.publication-authorized", "value": "false"},
                ],
            }
        },
        "components": [
            {
                "type": "file",
                "bom-ref": f"file:{entry['path']}",
                "name": entry["path"],
                "hashes": [{"alg": "SHA-256", "content": entry["sha256"]}],
            }
            for entry in included
        ],
        "dependencies": [{"ref": component_ref, "dependsOn": []}],
    }

    sbom_path = args.output_dir / "cyclonedx-1.5.json"
    sbom_path.write_text(json.dumps(sbom, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    provenance = {
        "schemaVersion": 1,
        "kind": "goreecloud-glaze-v1.6-artifact-provenance-rehearsal",
        "product": "GLAZE UI V1.6",
        "version": VERSION,
        "lifecycle": "release-candidate",
        "rehearsal": True,
        "finalStableArtifact": False,
        "sourceRevision": head,
        "sourceTree": tree,
        "stableBaseline": "1.5.1",
        "archive": {
            "name": archive.name,
            "format": "tar+gzip",
            "size": archive.stat().st_size,
            "sha256": sha256_file(archive),
            "deterministic": True,
            "prefix": f"glaze-ui-v{VERSION}/",
        },
        "includedFiles": included,
        "runtimeBoundary": {
            "entrypoint": "js/glaze-v1.6.0-rc.1.mjs",
            "externalRuntimeDependencies": [],
            "buildToolSecurityEvidenceSeparate": True,
        },
        "publication": {
            "tagCreated": False,
            "githubReleaseCreated": False,
            "artifactPublished": False,
            "stablePromotionAuthorized": False,
            "consumerEligibilityGranted": False,
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
        "version": VERSION,
        "lifecycle": "release-candidate",
        "includedFileCount": len(included),
        "archive": archive.name,
        "archiveSha256": sums[archive.name],
        "sbomSha256": sums[sbom_path.name],
        "provenanceSha256": sums[provenance_path.name],
        "stablePromotionAuthorized": False,
        "publicationAuthorized": False,
    }
    (args.output_dir / "rehearsal-summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ArtifactEvidenceError as error:
        print(f"FAIL: {error}")
        raise SystemExit(1)
