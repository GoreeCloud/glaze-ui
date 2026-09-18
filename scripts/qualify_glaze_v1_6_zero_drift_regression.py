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
import zlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

import capture_glaze_v1_6_rendered_qualification as rendered

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
                pixels.extend((row[i], row[i], row[i + 1], 255))
        else:
            for value in row:
                pixels.extend((value, value, value, 255))
    return int(width), int(height), bytes(pixels)


def validate_scene_evidence(evidence: Any, scene_id: str) -> dict[str, Any]:
    require(isinstance(evidence, dict), f"scene produced no evidence object: {scene_id}")
    require(evidence.get("passed") is True, f"scene assertions failed: {scene_id}: {evidence.get('assertions')}")
    require(evidence.get("scene") == scene_id, f"scene identity mismatch: {scene_id}")
    require(evidence.get("sourceRevisionParameter") == SOURCE_REVISION, f"source binding failed: {scene_id}")
    require(evidence.get("aggregateVersion") == "1.6.0-dev.12", f"aggregate mismatch: {scene_id}")
    require(evidence.get("lifecycle") == "development", f"lifecycle mismatch: {scene_id}")
    require(evidence.get("stableBaseline") == "1.5.1", f"Stable baseline mismatch: {scene_id}")
    authority = evidence.get("authority")
    require(isinstance(authority, dict) and authority.get("renderedBrowserOnly") is True, f"authority boundary missing: {scene_id}")
    for key in (
        "humanEvidenceClaimed",
        "assistiveTechnologyEvidenceClaimed",
        "physicalDeviceEvidenceClaimed",
        "nativePlatformEvidenceClaimed",
        "representativePerformanceEvidenceClaimed",
        "regressionBaselineClaimed",
        "lifecyclePromotionAutomatic",
    ):
        require(authority.get(key) is False, f"scene authority drift for {scene_id}: {key}")
    return evidence


def capture_reload(
    session_id: str,
    scene: dict[str, Any],
    output: Path,
) -> dict[str, Any]:
    scene_id = str(scene["id"])
    width, height = [int(value) for value in scene["viewport"]]
    mobile = bool(scene.get("mobile", False))
    rendered.set_viewport(session_id, width, height, mobile)
    rendered.set_media(session_id, list(scene.get("mediaFeatures", [])))
    query = urlencode(
        {
            "scene": scene_id,
            "revision": SOURCE_REVISION,
            "environment": str(scene["environment"]),
            "mode": str(scene["mode"]),
        }
    )
    rendered.webdriver_request(
        "POST",
        f"/session/{session_id}/url",
        {"url": f"{rendered.SERVER}/{scene['harness']}?{query}"},
    )
    rendered.wait_ready(session_id)

    evidence = validate_scene_evidence(
        rendered.execute(session_id, "return window.__glazeV16RenderedEvidence;"),
        scene_id,
    )
    dimensions = rendered.execute(
        session_id,
        "return [innerWidth,innerHeight,document.documentElement.scrollWidth,document.documentElement.scrollHeight];",
    )
    require(isinstance(dimensions, list) and len(dimensions) == 4, f"invalid viewport dimensions: {scene_id}")
    require(abs(int(dimensions[0]) - width) <= 1, f"viewport width drift: {scene_id}: {dimensions}")
    require(abs(int(dimensions[1]) - height) <= 1, f"viewport height drift: {scene_id}: {dimensions}")
    require(int(dimensions[2]) <= width + 1, f"horizontal overflow: {scene_id}: {dimensions}")

    rendered.freeze_after_measurement(session_id)
    output.parent.mkdir(parents=True, exist_ok=True)
    rendered.screenshot(session_id, output)
    return evidence


def compare_scene(base_path: Path, repeat_path: Path, scene_id: str) -> dict[str, Any]:
    bw, bh, bp = decode_png(base_path)
    rw, rh, rp = decode_png(repeat_path)
    require((bw, bh) == (rw, rh), f"dimension drift for {scene_id}: {(bw, bh)} != {(rw, rh)}")
    require(len(bp) == len(rp), f"decoded pixel length drift for {scene_id}")
    changed = 0
    maximum = 0
    for i in range(0, len(bp), 4):
        delta = max(abs(bp[i + channel] - rp[i + channel]) for channel in range(4))
        if delta:
            changed += 1
            maximum = max(maximum, delta)
    return {
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


def qualify(
    tooling_root: Path,
    render_root: Path,
    source_root: Path,
    plan_path: Path,
    output: Path,
) -> dict[str, Any]:
    plan = load_json(plan_path)
    rendered_plan = load_json(tooling_root / str(plan["renderedQualificationPlan"]))
    require(plan.get("sourceRevision") == SOURCE_REVISION, "regression plan source revision drifted")
    require(plan.get("acceptanceLaneId") == "regression-testing", "regression plan lane drifted")
    comparison = plan.get("comparison")
    require(isinstance(comparison, dict), "regression comparison missing")
    require(comparison.get("mode") == "same-browser-process-reload-zero-decoded-pixel-drift", "regression comparison mode drifted")
    require(comparison.get("changedPixelTolerance") == 0, "changed-pixel tolerance must remain zero")
    require(comparison.get("maximumChannelDeltaTolerance") == 0, "channel-delta tolerance must remain zero")
    require(comparison.get("compareDecodedRgba") is True, "decoded RGBA comparison must remain required")
    require(comparison.get("browserProcessMustRemainSame") is True, "same-browser-process requirement must remain enabled")
    require(comparison.get("reloadBetweenReferenceAndRepeat") is True, "reload requirement must remain enabled")
    require(comparison.get("sameRunnerRequired") is True, "same-runner requirement must remain enabled")

    actual_source = rendered.git_revision(source_root)
    require(actual_source == SOURCE_REVISION, f"frozen source mismatch: {actual_source}")
    require(rendered.git_clean(source_root), "frozen source worktree has tracked modifications")
    tooling_revision = rendered.git_revision(tooling_root)
    harness = render_root / str(rendered_plan["harness"])
    require(harness.is_file(), f"render root missing qualification harness: {harness}")
    require((render_root / "js/glaze-v1.6-development.mjs").is_file(), "render root missing frozen V1.6 aggregate")
    require((render_root / "css/glaze-v1.4.1.css").is_file(), "render root missing Stable CSS dependency")

    scene_ids = list(plan.get("requiredSceneIds") or [])
    scenes = list(rendered_plan.get("scenes") or [])
    require(len(scene_ids) == int(plan.get("requiredSceneCount", -1)) == 9, "regression scene set must contain nine scenes")
    require(len(set(scene_ids)) == 9, "regression scene IDs must be unique")
    require(sorted(scene_ids) == sorted(str(scene["id"]) for scene in scenes), "regression scene set drifted from rendered plan")

    if output.exists():
        shutil.rmtree(output)
    baseline_dir = output / "baseline"
    repeat_dir = output / "repeat"
    baseline_scene_dir = output / "baseline-scenes"
    repeat_scene_dir = output / "repeat-scenes"
    output.mkdir(parents=True, exist_ok=True)

    http = driver = None
    session_id: str | None = None
    comparisons: list[dict[str, Any]] = []
    semantic_pairs: list[dict[str, Any]] = []
    try:
        http = subprocess.Popen(
            [sys.executable, "-m", "http.server", str(rendered.WEB_PORT), "--bind", rendered.HOST, "--directory", str(render_root)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        rendered.wait_http(f"{rendered.SERVER}/{rendered_plan['harness']}")
        driver = subprocess.Popen(
            [rendered.chromedriver(), f"--port={rendered.DRIVER_PORT}", "--allowed-ips=127.0.0.1"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        rendered.wait_driver()
        session_id = rendered.create_session()
        browser = rendered.cdp(session_id, "Browser.getVersion")

        for scene in scenes:
            scene = dict(scene)
            scene["harness"] = rendered_plan["harness"]
            scene_id = str(scene["id"])
            baseline_path = baseline_dir / f"{scene_id}.png"
            repeat_path = repeat_dir / f"{scene_id}.png"

            baseline_evidence = capture_reload(session_id, scene, baseline_path)
            repeat_evidence = capture_reload(session_id, scene, repeat_path)
            require(baseline_evidence == repeat_evidence, f"semantic evidence drift across reloads: {scene_id}")

            baseline_scene_dir.mkdir(parents=True, exist_ok=True)
            repeat_scene_dir.mkdir(parents=True, exist_ok=True)
            base_json = baseline_scene_dir / f"{scene_id}.json"
            repeat_json = repeat_scene_dir / f"{scene_id}.json"
            base_json.write_text(json.dumps(baseline_evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            repeat_json.write_text(json.dumps(repeat_evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")

            item = compare_scene(baseline_path, repeat_path, scene_id)
            comparisons.append(item)
            semantic_pairs.append(
                {
                    "sceneId": scene_id,
                    "baselineEvidenceSha256": hashlib.sha256(base_json.read_bytes()).hexdigest(),
                    "repeatEvidenceSha256": hashlib.sha256(repeat_json.read_bytes()).hexdigest(),
                    "identical": base_json.read_bytes() == repeat_json.read_bytes(),
                }
            )

        failures = [
            item for item in comparisons
            if item["changedPixels"] != 0 or item["maximumChannelDelta"] != 0
        ]
        semantic_failures = [item for item in semantic_pairs if not item["identical"]]
        evidence = {
            "schemaVersion": 1,
            "recordType": "glaze-v1.6-zero-drift-rendered-regression-qualification",
            "status": "failed" if failures or semantic_failures else "passed",
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
                "semanticFailureSceneIds": [item["sceneId"] for item in semantic_failures],
                "sameBrowserProcess": True,
                "reloadBetweenReferenceAndRepeat": True,
            },
            "browser": browser,
            "comparisons": comparisons,
            "semanticEvidencePairs": semantic_pairs,
            "renderedRegressionEvidenceEligible": not failures and not semantic_failures,
            "authority": {
                "regressionRenderedEvidenceClaimed": not failures and not semantic_failures,
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
                "Reference and repeat renders are reloaded inside one Chromium process and compared at zero decoded-pixel tolerance. "
                "A pass is eligible only as rendered evidence for regression-testing on the exact frozen source. "
                "Cross-process compositor variance is not treated as source regression evidence. "
                "No human, assistive-technology, physical-device/native-platform, representative-performance, lifecycle, "
                "consumer, deployment, or production acceptance is established."
            ),
        }
        evidence_path = output / "evidence.json"
        evidence_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        require(not semantic_failures, "semantic regression evidence drift: " + ", ".join(item["sceneId"] for item in semantic_failures))
        require(not failures, "zero-drift regression failed: " + "; ".join(
            f"{item['sceneId']}={item['changedPixels']} pixels/max {item['maximumChannelDelta']}" for item in failures
        ))
        require(rendered.git_clean(source_root), "frozen source worktree changed during regression qualification")
        return evidence
    finally:
        if session_id:
            try:
                rendered.webdriver_request("DELETE", f"/session/{session_id}", timeout=5)
            except Exception:
                pass
        for process in (driver, http):
            if process:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()


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
    print("Decoded-pixel drift: 0 changed pixels / 0 maximum channel delta across every reload pair.")
    print("Boundary: same-renderer rendered regression evidence only; qualification/lifecycle remains independently governed.")


if __name__ == "__main__":
    try:
        main()
    except (RegressionError, subprocess.CalledProcessError, OSError, json.JSONDecodeError, zlib.error, rendered.QualificationError) as error:
        print(f"GLAZE UI V1.6 zero-drift rendered regression FAILED: {error}", file=sys.stderr)
        raise SystemExit(1)
