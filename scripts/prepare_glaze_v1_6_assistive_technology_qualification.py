#!/usr/bin/env python3
"""Prepare an exact-source local root for Glaze UI V1.6 assistive-technology review."""
from __future__ import annotations

import argparse
import io
import json
from datetime import datetime, timezone
from pathlib import Path
import shutil
import subprocess
import tarfile

SOURCE_REVISION = "c7509c79256b04b0aa67cb9dd0737d7588e0ae4a"
STABLE_BASELINE = "1.5.1"
ACCEPTANCE_MODEL = "1.6.0-dev.12"
HARNESS = Path("reference/v1.6/assistive-technology-qualification.html")
SENTINEL = ".glaze-v1.6-assistive-technology-review-root"


class PreparationError(RuntimeError):
    pass


def run_git(root: Path, *args: str, binary: bool = False):
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        text=not binary,
        check=False,
    )
    if result.returncode != 0:
        stderr = result.stderr.decode() if binary else result.stderr
        raise PreparationError("git " + " ".join(args) + " failed: " + stderr.strip())
    return result.stdout


def safe_extract_tar(data: bytes, destination: Path) -> None:
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:") as archive:
        root = destination.resolve()
        for member in archive.getmembers():
            target = (destination / member.name).resolve()
            if root != target and root not in target.parents:
                raise PreparationError("archive contains path outside destination: " + member.name)
        archive.extractall(destination)


def prepare(repo_root: Path, output: Path, replace: bool) -> dict:
    repo_root = repo_root.resolve()
    output = output.resolve()
    harness = repo_root / HARNESS

    if not harness.is_file():
        raise PreparationError("missing assistive-technology review harness: " + str(harness))

    run_git(repo_root, "cat-file", "-e", SOURCE_REVISION + "^{commit}")
    tooling_revision = run_git(repo_root, "rev-parse", "HEAD").strip()

    if output.exists():
        sentinel = output / SENTINEL
        if not replace:
            raise PreparationError("output already exists; choose another path or pass --replace")
        if not sentinel.is_file():
            raise PreparationError("refusing to replace a directory without the review-root sentinel")
        shutil.rmtree(output)

    output.mkdir(parents=True)
    (output / SENTINEL).write_text(
        "Glaze UI V1.6 exact-source assistive-technology review root\n",
        encoding="utf-8",
    )

    archive = run_git(repo_root, "archive", "--format=tar", SOURCE_REVISION, "js", binary=True)
    safe_extract_tar(archive, output)

    target_harness = output / HARNESS
    target_harness.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(harness, target_harness)

    manifest = {
        "schemaVersion": 1,
        "recordType": "glaze-v1.6-assistive-technology-review-source",
        "sourceRevision": SOURCE_REVISION,
        "toolingRevision": tooling_revision,
        "stableBaseline": STABLE_BASELINE,
        "acceptanceModelVersion": ACCEPTANCE_MODEL,
        "preparedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "repositoryLocalOnly": True,
        "assistiveTechnologyEvidenceClaimed": False,
        "humanEvidenceClaimed": False,
        "physicalDeviceEvidenceClaimed": False,
        "performanceEvidenceClaimed": False,
        "lifecyclePromotionAutomatic": False,
    }
    (output / "qualification-source.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out", default="_v16-assistive-technology-review")
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args()

    manifest = prepare(Path(args.repo_root), Path(args.out), args.replace)
    print("GLAZE UI V1.6 assistive-technology review root prepared")
    print("Frozen source: " + manifest["sourceRevision"])
    print("Tooling revision: " + manifest["toolingRevision"])
    print("Serve locally, for example:")
    print("  python3 -m http.server 8767 --bind 127.0.0.1 --directory " + args.out)
    print("Then open:")
    print("  http://127.0.0.1:8767/reference/v1.6/assistive-technology-qualification.html")
    print("Boundary: review surface only; no assistive-technology evidence or lifecycle acceptance is created.")


if __name__ == "__main__":
    try:
        main()
    except PreparationError as error:
        raise SystemExit("GLAZE UI V1.6 assistive-technology review preparation FAILED: " + str(error))
