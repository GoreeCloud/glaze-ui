#!/usr/bin/env python3
"""Capture and compare Glaze UI 2.1 Candidate screenshot baselines without third-party image libraries."""
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
    browser_command,
    find_browser,
    run_browser,
    serve_root,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "contracts/regression/visual-baselines.json"


def load_manifest() -> dict:
    value = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if value.get("id") != "glaze-ui-2.1-visual-baselines":
        raise SystemExit("visual regression manifest identity mismatch")
    return value


def case_url(port: int, case: dict) -> str:
    query = urllib.parse.urlencode({
        "flow": case["flow"],
        "appearance": case.get("appearance", "light"),
        "clarity": case.get("clarity", "balanced"),
        "density": case.get("density", "standard"),
        "performance": case.get("performance", "balanced"),
        "formFactor": case.get("formFactor", "desktop"),
        "mode": case.get("mode", "normal"),
        "snapshotState": case.get("snapshotState", "idle"),
    })
    return f"http://127.0.0.1:{port}/reference/candidate-2.1-snapshot.html?{query}"


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
    if mode == "reduced-motion":
        command.append("--force-prefers-reduced-motion")
    elif mode == "forced-colors":
        command.append("--force-high-contrast")
    command.append(url)
    return command


def capture_case(browser: str, port: int, case: dict, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    url = case_url(port, case)
    with tempfile.TemporaryDirectory(prefix="glaze-21-visual-ready-") as profile:
        ready = run_browser(browser_command(browser, url, profile, width=case["width"], height=case["height"], mode=case.get("mode", "normal")))
    if ready.returncode != 0 or 'data-snapshot-ready="true"' not in ready.stdout:
        raise SystemExit(f"visual snapshot did not reach ready state for {case['id']}\n{(ready.stdout or ready.stderr)[-2000:]}")
    with tempfile.TemporaryDirectory(prefix="glaze-21-visual-shot-") as profile:
        completed = run_browser(screenshot_command(browser, url, profile, output, case))
    if completed.returncode != 0:
        raise SystemExit(f"visual capture failed for {case['id']}: browser exited {completed.returncode}\n{completed.stderr[-2000:]}")
    if not output.is_file() or output.stat().st_size < 256:
        raise SystemExit(f"visual capture failed for {case['id']}: PNG was not created")
    print(f"Captured Glaze UI 2.1 visual case: {case['id']} -> {output}")


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
        if kind == b"IHDR": ihdr = chunk
        elif kind == b"IDAT": compressed.extend(chunk)
        elif kind == b"IEND": break
    if ihdr is None or len(ihdr) != 13:
        raise ValueError(f"missing/invalid IHDR in {path}")
    width, height, bit_depth, color_type, compression, filter_method, interlace = struct.unpack(">IIBBBBB", ihdr)
    if bit_depth != 8 or compression != 0 or filter_method != 0 or interlace != 0:
        raise ValueError(f"unsupported PNG encoding in {path}: depth={bit_depth}, interlace={interlace}")
    channels = {0: 1, 2: 3, 4: 2, 6: 4}.get(color_type)
    if channels is None:
        raise ValueError(f"unsupported PNG color type {color_type} in {path}")
    raw = zlib.decompress(bytes(compressed)); stride = width * channels
    if len(raw) != height * (stride + 1):
        raise ValueError(f"unexpected PNG raster size in {path}")
    rows, offset, previous = [], 0, bytearray(stride)
    for _ in range(height):
        filter_type = raw[offset]; offset += 1
        scan = bytearray(raw[offset:offset + stride]); offset += stride
        for i in range(stride):
            left = scan[i - channels] if i >= channels else 0; up = previous[i]; up_left = previous[i - channels] if i >= channels else 0
            if filter_type == 1: scan[i] = (scan[i] + left) & 255
            elif filter_type == 2: scan[i] = (scan[i] + up) & 255
            elif filter_type == 3: scan[i] = (scan[i] + ((left + up) // 2)) & 255
            elif filter_type == 4: scan[i] = (scan[i] + paeth(left, up, up_left)) & 255
            elif filter_type != 0: raise ValueError(f"unsupported PNG filter {filter_type} in {path}")
        rows.append(bytes(scan)); previous = scan
    rgb = bytearray(width * height * 3); out = 0
    for row in rows:
        for x in range(width):
            i = x * channels
            if color_type in (0, 4): r = g = b = row[i]
            else: r, g, b = row[i:i + 3]
            rgb[out:out + 3] = bytes((r, g, b)); out += 3
    return width, height, bytes(rgb)


def write_diff_ppm(path: Path, width: int, height: int, baseline: bytes, current: bytes, tolerance: int) -> None:
    pixels = bytearray(width * height * 3)
    for p in range(width * height):
        i = p * 3; delta = max(abs(current[i + c] - baseline[i + c]) for c in range(3))
        if delta > tolerance: pixels[i:i + 3] = b"\xff\x00\x00"
        else:
            gray = sum(current[i:i + 3]) // 6 + 64; pixels[i:i + 3] = bytes((gray, gray, gray))
    path.write_bytes(f"P6\n{width} {height}\n255\n".encode("ascii") + pixels)


def compare_case(case: dict, current: Path, thresholds: dict, output_dir: Path) -> None:
    baseline = ROOT / case["baseline"]
    if not baseline.is_file(): raise SystemExit(f"missing visual baseline for {case['id']}: {case['baseline']}")
    bw, bh, bp = decode_png(baseline); cw, ch, cp = decode_png(current)
    if (bw, bh) != (cw, ch): raise SystemExit(f"visual regression {case['id']} dimensions changed: baseline {bw}x{bh}, current {cw}x{ch}")
    if (bw, bh) != (case["width"], case["height"]): raise SystemExit(f"visual baseline {case['id']} dimensions {bw}x{bh} do not match manifest {case['width']}x{case['height']}")
    tolerance = int(thresholds["perChannelTolerance"]); changed = total_delta = 0; pixels = bw * bh
    for p in range(pixels):
        i = p * 3; diffs = [abs(cp[i + c] - bp[i + c]) for c in range(3)]; total_delta += sum(diffs)
        if max(diffs) > tolerance: changed += 1
    ratio = changed / pixels if pixels else 0.0; mean_delta = total_delta / (pixels * 3) if pixels else 0.0
    max_ratio = float(thresholds["maxChangedPixelRatio"]); max_mean = float(thresholds["maxMeanAbsoluteChannelDelta"])
    print(f"Visual diff {case['id']}: changed={ratio:.6%} (limit {max_ratio:.6%}), mean-channel-delta={mean_delta:.4f} (limit {max_mean:.4f})")
    if ratio > max_ratio or mean_delta > max_mean:
        diff = output_dir / f"{case['id']}.diff.ppm"; write_diff_ppm(diff, bw, bh, bp, cp, tolerance)
        raise SystemExit(f"visual regression failed for {case['id']}: changed ratio {ratio:.6%}, mean channel delta {mean_delta:.4f}; diff written to {diff}")


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("mode", choices=("capture", "compare")); parser.add_argument("--output-dir", default=".artifacts/glaze-2.1-visual"); args = parser.parse_args()
    manifest = load_manifest(); output_dir = ROOT / args.output_dir
    if output_dir.exists(): shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True); browser = find_browser()
    with serve_root() as port:
        for case in manifest.get("cases", []):
            current = output_dir / f"{case['id']}.png"; capture_case(browser, port, case, current)
            if args.mode == "compare": compare_case(case, current, manifest["thresholds"], output_dir)
    if args.mode == "capture": print("Glaze UI 2.1 screenshot capture completed. These PNGs are review inputs, not accepted baselines.")
    else: print("Glaze UI 2.1 screenshot pixel regression passed against committed Candidate baselines.")

if __name__ == "__main__": main()
