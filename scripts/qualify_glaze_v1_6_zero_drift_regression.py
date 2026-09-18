#!/usr/bin/env python3
"""Qualify exact-source GLAZE UI V1.6 rendered regression with zero decoded-pixel drift."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import struct
import subprocess
import sys
import time
import zlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
SOURCE_REVISION = "c7509c79256b04b0aa67cb9dd0737d7588e0ae4a"


class RegressionError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RegressionError(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing JSON file: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"JSON root must be an object: {path}")
    return value


def git_revision(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True, stderr=subprocess.STDOUT
        ).strip()
    except Exception as error:
        raise RegressionError(f"could not resolve git revision for {root}: {error}") from error


def git_clean(root: Path) -> bool:
    result = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    require(result.returncode == 0, f"could not inspect git status for {root}: {result.stderr}")
    return result.stdout.strip() == ""


def paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def decode_png(path: Path) -> tuple[int, int, bytes]:
    data = path.read_bytes()
    require(data.startswith(PNG_SIGNATURE), f"not a PNG: {path}")
    offset = len(PNG_SIGNATURE)
    width = height = bit_depth = color_type = interlace = None
    compressed = bytearray()
    while offset < len(data):
        require(offset + 12 <= len(data), f"truncated PNG chunk: {path}")
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        kind = data[offset + 4:offset + 8]
        payload = data[offset + 8:offset + 8 + length]
        offset += 12 + length
        if kind == b"IHDR":
            width, height, bit_depth, color_type, _compression, _filter, interlace = struct.unpack(">IIBBBBB", payload)
        elif kind == b"IDAT":
            compressed.extend(payload)
        elif kind == b"IEND":
            break
    require(all(x is not None for x in (width, height, bit_depth, color_type, interlace)), f"missing PNG IHDR: {path}")
    require(bit_depth == 8 and interlace == 0, f"unsupported PNG format in {path}: depth={bit_depth} interlace={interlace}")
    channels = {0: 1, 2: 3, 4: 2, 6: 4}.get(int(color_type))
    require(channels is not None, f"unsupported PNG color type {color_type}: {path}")
    stride = int(width) * int(channels)
    raw = zlib.decompress(bytes(compressed))
    require(len(raw) == (stride + 1) * int(height), f"unexpected PNG scanline size: {path}")
    previous = bytearray(stride)
    pixels = bytearray()
    cursor = 0
    for _row in range(int(height)):
        filter_type = raw[cursor]
        cursor += 1
        encoded = raw[cursor:cursor + stride]
        cursor += stride
        row = bytearray(stride)
        for i, value in enumerate(encoded):
            left = row[i - channels] if i >= channels else 0
            up = previous[i]
            upper_left = previous[i - channels] if i >= channels else 0
            if filter_type == 0:
                recon = value
            elif filter_type == 1:
                recon = (value + left) & 255
            elif filter_type == 2:
                recon = (value + up) & 255
            elif filter_type == 3:
                recon = (value + ((left + up) // 2)) & 255
            elif filter_type == 4:
                recon = (value + paeth(left, up, upper_left)) & 255
            else:
                raise RegressionError(f"unsupported PNG filter {filter_type}: {path}")
            row[i] = recon
        previous = row
        if color_type == 6:
            pixels.extend(row)
        elif color_type == 2:
            for i in range(0, len(row), 3):
                pixels.extend((row[i], row[i + 1], row[i + 2], 255))
        elif color_type == 4:
            for i in range(0, len(row), 2):
                pixels.extend((row[i], row[i], row[i], row[i + 1]))
        else:
            for value in row:
                pixels.extend((value, value, value, 255))
    return int(width), int(height), bytes(pixels)


def run_capture(tooling_root: Path, render_root: Path, source_root: Path, output: Path) -> None:
    command = [
        sys.executable,
        str(tooling_root / "scripts/capture_glaze_v1_6_rendered_qualification.py"),
        "--render-root", str(render_root),
        "--source-root", str(source_root),
        "--tooling-root", str(tooling_root),
        "--out", str(output.relative_to(tooling_root)),
    ]
    subprocess.run(command, cwd=tooling_root, check=True)


def compare(
    baseline: Path,
    repeat: Path,
    scene_ids: list[str],
) -> list[dict[str, Any]]:
    comparisons: list[dict[str, Any]] = []
    for scene_id in scene_ids:
        name = f"{scene_id}.png"
        base_path = baseline / "screenshots" / name
        repeat_path = repeat / "screenshots" / name
        require(base_path.is_file(), f"baseline missing screenshot: {name}")
        require(repeat_path.is_file(), f"repeat missing screenshot: {name}")
        bw, bh, bp = decode_png(base_path)
        rw, rh, rp = decode_png(repeat_path)
        require((bw, bh) == (rw, rh), f"dimension drift for {name}: {(bw, bh)} != {(rw, rh)}")
        require(len(bp) == len(rp), f"decoded pixel length drift for {name}")
        changed = 0
        maximum = 0
        for i in range(0, len(bp), 4):
            delta = max(abs(bp[i + channel] - rp[i + channel]) for channel in range(4))
            if delta:
                changed += 1
                maximum = max(maximum, delta)
        comparisons.append(
            {
                "sceneId": scene_id,
                "dimensions": [bw, bh],
                "totalPixels": bw * bh,
                "changedPixels": changed,
                "changedPixelPercent": (changed * 100.0 / (bw * bh)) if bw and bh else 0.0,
                "maximumChannelDelta": maximum,
                "baselinePngSha256": hashlib.sha256(base_path.read_bytes()).hexdigest(),
                "repeatPngSha256": hashlib.sha256(repeat_path.read_bytes()).hexdigest(),
                "baselineDecodedRgbaSha256": hashlib.sha256(bp).hexdigest(),
                "repeatDecodedRgbaSha256": hashlib.sha256(rp).hexdigest(),
            }
        )
    return comparisons


def qualify(
    tooling_root: Path,
    render_root: Path,
    source_root: Path,
    plan_path: Path,
    output: Path,
) -> dict[str, Any]:
    plan = load_json(plan_path)
    require(plan.get("sourceRevision") == SOURCE_REVISION, "regression plan source revision drifted")
    require(plan.get("acceptanceLaneId") == "regression-testing", "regression plan lane drifted")
    comparison = plan.get("comparison")
    require(isinstance(comparison, dict), "regression comparison missing")
    require(comparison.get("changedPixelTolerance") == 0, "changed-pixel tolerance must remain zero")
    require(comparison.get("maximumChannelDeltaTolerance") == 0, "channel-delta tolerance must remain zero")
    require(comparison.get("compareDecodedRgba") is True, "decoded RGBA comparison must remain required")
    require(comparison.get("sameRunnerRequired") is True, "same-runner requirement must remain enabled")

    actual_source = git_revision(source_root)
    require(actual_source == SOURCE_REVISION, f"frozen source mismatch: {actual_source}")
    require(git_clean(source_root), "frozen source worktree has tracked modifications")
    tooling_revision = git_revision(tooling_root)

    scene_ids = list(plan.get("requiredSceneIds") or [])
    require(len(scene_ids) == int(plan.get("requiredSceneCount", -1)) == 9, "regression scene set must contain nine scenes")
    require(len(set(scene_ids)) == 9, "regression scene IDs must be unique")

    baseline = output / "baseline"
    repeat = output / "repeat"
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)

    run_capture(tooling_root, render_root, source_root, baseline)
    time.sleep(1.0)
    run_capture(tooling_root, render_root, source_root, repeat)

    base_manifest = load_json(baseline / "manifest.json")
    repeat_manifest = load_json(repeat / "manifest.json")
    for manifest, label in ((base_manifest, "baseline"), (repeat_manifest, "repeat")):
        require(manifest.get("sourceRevision") == SOURCE_REVISION, f"{label} source revision mismatch")
        require(manifest.get("acceptanceModelVersion") == "1.6.0-dev.12", f"{label} acceptance model mismatch")
        require(manifest.get("stableBaseline") == "1.5.1", f"{label} Stable baseline mismatch")
        require(manifest.get("sceneCount") == 9 and manifest.get("passed") is True, f"{label} capture did not pass")
        require(manifest.get("toolingRevision") == tooling_revision, f"{label} tooling revision mismatch")
    base_browser = base_manifest.get("browser") or {}
    repeat_browser = repeat_manifest.get("browser") or {}
    require(base_browser.get("product") == repeat_browser.get("product"), "browser product drifted between captures")
    require(base_browser.get("revision") == repeat_browser.get("revision"), "browser revision drifted between captures")

    comparisons = compare(baseline, repeat, scene_ids)
    failures = [
        item for item in comparisons
        if item["changedPixels"] != 0 or item["maximumChannelDelta"] != 0
    ]

    evidence = {
        "schemaVersion": 1,
        "recordType": "glaze-v1.6-zero-drift-rendered-regression-qualification",
        "status": "failed" if failures else "passed",
        "lifecycle": "DevelopmentQualification",
        "sourceRevision": SOURCE_REVISION,
        "toolingRevision": tooling_revision,
        "acceptanceModelVersion": "1.6.0-dev.12",
        "stableBaseline": "1.5.1",
        "specificationSection": 83,
        "acceptanceLaneId": "regression-testing",
        "evidenceType": "rendered",
        "observedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "comparison": {
            "mode": comparison["mode"],
            "changedPixelTolerance": 0,
            "maximumChannelDeltaTolerance": 0,
            "sceneCount": len(comparisons),
            "failedSceneIds": [item["sceneId"] for item in failures],
        },
        "browser": {
            "baseline": base_browser,
            "repeat": repeat_browser,
            "sameProduct": base_browser.get("product") == repeat_browser.get("product"),
            "sameRevision": base_browser.get("revision") == repeat_browser.get("revision"),
        },
        "comparisons": comparisons,
        "baselineManifestSha256": hashlib.sha256((baseline / "manifest.json").read_bytes()).hexdigest(),
        "repeatManifestSha256": hashlib.sha256((repeat / "manifest.json").read_bytes()).hexdigest(),
        "renderedRegressionEvidenceEligible": not failures,
        "authority": {
            "regressionRenderedEvidenceClaimed": not failures,
            "humanEvidenceClaimed": False,
            "assistiveTechnologyEvidenceClaimed": False,
            "physicalDeviceEvidenceClaimed": False,
            "nativePlatformEvidenceClaimed": False,
            "representativePerformanceEvidenceClaimed": False,
            "candidateStatusGranted": False,
            "releaseCandidateStatusGranted": False,
            "stableStatusGranted": False,
            "consumerAcceptanceAutomatic": False,
            "deploymentAcceptanceAutomatic": False,
            "productionAcceptanceAutomatic": False,
        },
        "boundary": (
            "Independent same-runner Chromium sessions are compared at zero decoded-pixel tolerance. "
            "A pass is eligible only as rendered evidence for the regression-testing lane on the exact frozen source. "
            "It does not establish human, assistive-technology, physical-device/native-platform, representative-performance, "
            "lifecycle, consumer, deployment, or production acceptance."
        ),
    }
    evidence_path = output / "evidence.json"
    evidence_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    require(not failures, "zero-drift regression failed: " + "; ".join(
        f"{item['sceneId']}={item['changedPixels']} pixels/max {item['maximumChannelDelta']}" for item in failures
    ))
    require(git_clean(source_root), "frozen source worktree changed during regression qualification")
    return evidence


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--render-root", required=True)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--tooling-root", default=".")
    parser.add_argument("--plan", default="contracts/v1.6/regression.rendered.plan.json")
    parser.add_argument("--out", default="artifacts/v1.6-regression")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tooling_root = Path(args.tooling_root).resolve()
    render_root = Path(args.render_root).resolve()
    source_root = Path(args.source_root).resolve()
    plan_path = (tooling_root / args.plan).resolve()
    output = (tooling_root / args.out).resolve()
    evidence = qualify(tooling_root, render_root, source_root, plan_path, output)
    print(
        "GLAZE UI V1.6 zero-drift rendered regression: PASS "
        f"({evidence['comparison']['sceneCount']} scenes, source {evidence['sourceRevision']})"
    )
    print("Decoded-pixel drift: 0 changed pixels / 0 maximum channel delta across every scene.")
    print("Boundary: rendered regression evidence only; qualification/lifecycle remains independently governed.")


if __name__ == "__main__":
    try:
        main()
    except (RegressionError, subprocess.CalledProcessError, OSError, json.JSONDecodeError, zlib.error) as error:
        print(f"GLAZE UI V1.6 zero-drift rendered regression FAILED: {error}", file=sys.stderr)
        raise SystemExit(1)
