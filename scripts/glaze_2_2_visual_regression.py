#!/usr/bin/env python3
"""Capture and compare Glaze UI 2.2 Candidate visual snapshots.

The automated visual gate is source-pinned. A baseline source revision is rendered
on the same Chromium runner as the exact current revision, then pixel-compared.
Capture output is evidence only and cannot self-approve Human Visual Excellence.
"""
from __future__ import annotations

import argparse
import json
import shutil
import struct
import tempfile
import urllib.parse
import zlib
from pathlib import Path

from validate_rendered_reference import (
    FORCED_COLORS_VIRTUAL_TIME_BUDGET_MS,
    VIRTUAL_TIME_BUDGET_MS,
    find_browser,
    run_browser,
    serve_root,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "contracts/regression/visual-baselines-2.2.json"


def load_manifest() -> dict:
    value = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if value.get("id") != "glaze-ui-2.2-visual-baselines":
        raise SystemExit("Glaze UI 2.2 visual regression manifest identity mismatch")
    if value.get("humanVisualExcellenceAccepted") is True:
        raise SystemExit("Candidate visual regression must not self-certify Human Visual Excellence")
    return value


def case_url(port: int, case: dict) -> str:
    query = urllib.parse.urlencode({
        "state": case.get("state", "workspace"),
        "appearance": case.get("appearance", "light"),
        "mode": case.get("mode", "normal"),
        "direction": case.get("direction", "ltr"),
    })
    return f"http://127.0.0.1:{port}/reference/candidate-2.2-snapshot.html?{query}"


def ready_command(browser: str, url: str, profile_dir: str, case: dict) -> list[str]:
    """Build a deterministic DOM-ready probe without inventing mode semantics.

    Reduced Transparency and Large Text are query-driven by the snapshot page, so
    the DOM probe must not route them through the generic rendered-harness mode
    mapper. Only browser-native media features need Chromium flags here.
    """
    mode = case.get("mode", "normal")
    virtual_time = FORCED_COLORS_VIRTUAL_TIME_BUDGET_MS if mode == "forced-colors" else VIRTUAL_TIME_BUDGET_MS
    command = [
        browser, "--headless=new", "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage",
        "--disable-background-networking", "--disable-background-timer-throttling",
        "--disable-backgrounding-occluded-windows", "--disable-renderer-backgrounding",
        "--disable-default-apps", "--disable-extensions", "--disable-sync",
        "--mute-audio", "--no-first-run", "--run-all-compositor-stages-before-draw",
        "--force-device-scale-factor=1", f"--virtual-time-budget={virtual_time}",
        f"--user-data-dir={profile_dir}", f"--window-size={case['width']},{case['height']}",
        "--dump-dom",
    ]
    if case.get("appearance", "light") == "dark":
        command.append("--force-dark-mode")
    if mode == "reduced-motion":
        command.append("--force-prefers-reduced-motion")
    elif mode == "forced-colors":
        command.append("--force-high-contrast")
    command.append(url)
    return command


def screenshot_command(browser: str, url: str, profile_dir: str, output: Path, case: dict) -> list[str]:
    mode = case.get("mode", "normal")
    virtual_time = FORCED_COLORS_VIRTUAL_TIME_BUDGET_MS if mode == "forced-colors" else VIRTUAL_TIME_BUDGET_MS
    command = [
        browser, "--headless=new", "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage",
        "--disable-background-networking", "--disable-background-timer-throttling",
        "--disable-backgrounding-occluded-windows", "--disable-renderer-backgrounding",
        "--disable-default-apps", "--disable-extensions", "--disable-sync", "--hide-scrollbars",
        "--mute-audio", "--no-first-run", "--run-all-compositor-stages-before-draw",
        "--force-device-scale-factor=1", f"--virtual-time-budget={virtual_time}",
        f"--user-data-dir={profile_dir}", f"--window-size={case['width']},{case['height']}",
        f"--screenshot={output}",
    ]
    appearance = case.get("appearance", "light")
    if appearance == "dark":
        command.append("--force-dark-mode")
    if mode == "reduced-motion":
        command.append("--force-prefers-reduced-motion")
    elif mode == "forced-colors":
        command.append("--force-high-contrast")
    command.append(url)
    return command


def capture_case(browser: str, port: int, case: dict, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    url = case_url(port, case)
    with tempfile.TemporaryDirectory(prefix="glaze-22-visual-ready-") as profile:
        ready = run_browser(ready_command(browser, url, profile, case))
    if ready.returncode != 0 or 'data-snapshot-ready="true"' not in ready.stdout:
        raise SystemExit(
            f"Glaze UI 2.2 visual snapshot did not reach ready state for {case['id']}\n"
            f"{(ready.stdout or ready.stderr)[-2000:]}"
        )
    with tempfile.TemporaryDirectory(prefix="glaze-22-visual-shot-") as profile:
        completed = run_browser(screenshot_command(browser, url, profile, output, case))
    if completed.returncode != 0:
        raise SystemExit(
            f"Glaze UI 2.2 visual capture failed for {case['id']}: browser exited {completed.returncode}\n"
            f"{completed.stderr[-2000:]}"
        )
    if not output.is_file() or output.stat().st_size < 256:
        raise SystemExit(f"Glaze UI 2.2 visual capture failed for {case['id']}: PNG was not created")
    print(f"Captured Glaze UI 2.2 visual case: {case['id']} -> {output}")


def paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    return a if pa <= pb and pa <= pc else b if pb <= pc else c


def decode_png(path: Path) -> tuple[int, int, bytes]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path} is not a PNG")
    pos, ihdr, compressed = 8, None, bytearray()
    while pos < len(data):
        if pos + 12 > len(data):
            raise ValueError(f"truncated PNG chunk in {path}")
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        kind = data[pos + 4:pos + 8]
        chunk = data[pos + 8:pos + 8 + length]
        pos += 12 + length
        if kind == b"IHDR":
            ihdr = chunk
        elif kind == b"IDAT":
            compressed.extend(chunk)
        elif kind == b"IEND":
            break
    if ihdr is None or len(ihdr) != 13:
        raise ValueError(f"missing/invalid IHDR in {path}")
    width, height, bit_depth, color_type, compression, filter_method, interlace = struct.unpack(">IIBBBBB", ihdr)
    if bit_depth != 8 or compression != 0 or filter_method != 0 or interlace != 0:
        raise ValueError(f"unsupported PNG encoding in {path}: depth={bit_depth}, interlace={interlace}")
    channels = {0: 1, 2: 3, 4: 2, 6: 4}.get(color_type)
    if channels is None:
        raise ValueError(f"unsupported PNG color type {color_type} in {path}")
    raw = zlib.decompress(bytes(compressed))
    stride = width * channels
    if len(raw) != height * (stride + 1):
        raise ValueError(f"unexpected PNG raster size in {path}")
    rows, offset, previous = [], 0, bytearray(stride)
    for _ in range(height):
        filter_type = raw[offset]
        offset += 1
        scan = bytearray(raw[offset:offset + stride])
        offset += stride
        for i in range(stride):
            left = scan[i - channels] if i >= channels else 0
            up = previous[i]
            up_left = previous[i - channels] if i >= channels else 0
            if filter_type == 1:
                scan[i] = (scan[i] + left) & 255
            elif filter_type == 2:
                scan[i] = (scan[i] + up) & 255
            elif filter_type == 3:
                scan[i] = (scan[i] + ((left + up) // 2)) & 255
            elif filter_type == 4:
                scan[i] = (scan[i] + paeth(left, up, up_left)) & 255
            elif filter_type != 0:
                raise ValueError(f"unsupported PNG filter {filter_type} in {path}")
        rows.append(bytes(scan))
        previous = scan
    rgb = bytearray(width * height * 3)
    out = 0
    for row in rows:
        for x in range(width):
            i = x * channels
            if color_type in (0, 4):
                r = g = b = row[i]
            else:
                r, g, b = row[i:i + 3]
            rgb[out:out + 3] = bytes((r, g, b))
            out += 3
    return width, height, bytes(rgb)


def write_diff_ppm(path: Path, width: int, height: int, baseline: bytes, current: bytes, tolerance: int) -> None:
    pixels = bytearray(width * height * 3)
    for p in range(width * height):
        i = p * 3
        delta = max(abs(current[i + c] - baseline[i + c]) for c in range(3))
        if delta > tolerance:
            pixels[i:i + 3] = b"\xff\x00\x00"
        else:
            gray = sum(current[i:i + 3]) // 6 + 64
            pixels[i:i + 3] = bytes((gray, gray, gray))
    path.write_bytes(f"P6\n{width} {height}\n255\n".encode("ascii") + pixels)


def compare_case(case: dict, baseline: Path, current: Path, thresholds: dict, output_dir: Path) -> None:
    if not baseline.is_file():
        raise SystemExit(f"missing source-pinned Glaze UI 2.2 visual baseline for {case['id']}: {baseline}")
    bw, bh, bp = decode_png(baseline)
    cw, ch, cp = decode_png(current)
    if (bw, bh) != (cw, ch):
        raise SystemExit(f"visual regression {case['id']} dimensions changed: baseline {bw}x{bh}, current {cw}x{ch}")
    if (bw, bh) != (case["width"], case["height"]):
        raise SystemExit(
            f"visual baseline {case['id']} dimensions {bw}x{bh} do not match manifest "
            f"{case['width']}x{case['height']}"
        )
    tolerance = int(thresholds["perChannelTolerance"])
    changed = total_delta = 0
    pixels = bw * bh
    for p in range(pixels):
        i = p * 3
        diffs = [abs(cp[i + c] - bp[i + c]) for c in range(3)]
        total_delta += sum(diffs)
        if max(diffs) > tolerance:
            changed += 1
    ratio = changed / pixels if pixels else 0.0
    mean_delta = total_delta / (pixels * 3) if pixels else 0.0
    max_ratio = float(thresholds["maxChangedPixelRatio"])
    max_mean = float(thresholds["maxMeanAbsoluteChannelDelta"])
    print(
        f"Visual diff {case['id']}: changed={ratio:.6%} (limit {max_ratio:.6%}), "
        f"mean-channel-delta={mean_delta:.4f} (limit {max_mean:.4f})"
    )
    if ratio > max_ratio or mean_delta > max_mean:
        diff = output_dir / f"{case['id']}.diff.ppm"
        write_diff_ppm(diff, bw, bh, bp, cp, tolerance)
        raise SystemExit(
            f"Glaze UI 2.2 visual regression failed for {case['id']}: changed ratio {ratio:.6%}, "
            f"mean channel delta {mean_delta:.4f}; diff written to {diff}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("capture", "compare"))
    parser.add_argument("--output-dir", default=".artifacts/glaze-2.2-visual")
    parser.add_argument("--baseline-dir", help="Source-pinned baseline PNG directory; required for compare mode.")
    args = parser.parse_args()
    if args.mode == "compare" and not args.baseline_dir:
        raise SystemExit("compare mode requires --baseline-dir so current output cannot bless itself")

    manifest = load_manifest()
    output_dir = (ROOT / args.output_dir).resolve()
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)
    browser = find_browser()
    baseline_dir = (ROOT / args.baseline_dir).resolve() if args.baseline_dir else None

    with serve_root() as port:
        for case in manifest.get("cases", []):
            current = output_dir / f"{case['id']}.png"
            capture_case(browser, port, case, current)
            if args.mode == "compare":
                baseline = baseline_dir / case["baselineFile"]
                compare_case(case, baseline, current, manifest["thresholds"], output_dir)

    if args.mode == "capture":
        print(
            "Glaze UI 2.2 Candidate screenshot capture completed. This output is rendered evidence only; "
            "it is not self-accepted as a visual baseline or Human Visual Excellence approval."
        )
    else:
        revision = manifest.get("baselineRevision")
        if not isinstance(revision, str) or len(revision) != 40:
            raise SystemExit("compare mode requires a pinned 40-character baselineRevision")
        print(
            "Glaze UI 2.2 Candidate screenshot pixel regression passed against source-pinned baseline "
            f"revision {revision}. Human Visual Excellence remains separately required."
        )


if __name__ == "__main__":
    main()
