#!/usr/bin/env python3
"""Runtime acceptance for the Glaze UI 2.1 Android handheld Candidate reference.

This executes only against an attached Android target through adb. The hosted CI
workflow is explicitly emulator evidence; this script does not turn emulator
execution into physical-device, TalkBack, release-signing, or human Visual
Excellence acceptance.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".artifacts" / "glaze-2.1-android-native"
PACKAGE = "com.goreecloud.glazeui.reference.android"
ACTIVITY = f"{PACKAGE}/.MainActivity"
BOUNDS = re.compile(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]")
SHA40 = re.compile(r"^[0-9a-f]{40}$")


def run(*args: str, text: bool = True, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(args, check=check, text=text, capture_output=True)


def adb(serial: str, *args: str, text: bool = True, check: bool = True) -> subprocess.CompletedProcess:
    return run("adb", "-s", serial, *args, text=text, check=check)


def exact_source_revision() -> str:
    revision = run("git", "-C", str(ROOT), "rev-parse", "HEAD").stdout.strip()
    if not SHA40.fullmatch(revision):
        raise SystemExit(f"could not resolve exact checked-out source revision: {revision!r}")
    expected = os.environ.get("GLAZE_SOURCE_REVISION", "").strip()
    if expected:
        if not SHA40.fullmatch(expected):
            raise SystemExit(f"invalid expected Glaze source revision: {expected!r}")
        if expected != revision:
            raise SystemExit(
                f"checked-out source revision {revision} does not match expected exact head {expected}"
            )
    return revision


def serial_from_adb() -> str:
    explicit = os.environ.get("ANDROID_SERIAL", "").strip()
    if explicit:
        return explicit
    result = run("adb", "devices")
    devices: list[str] = []
    for line in result.stdout.splitlines()[1:]:
        cols = line.split()
        if len(cols) >= 2 and cols[1] == "device":
            devices.append(cols[0])
    if len(devices) != 1:
        raise SystemExit(f"expected exactly one ready Android target, found {devices}")
    return devices[0]


def prop(serial: str, name: str) -> str:
    return adb(serial, "shell", "getprop", name).stdout.strip()


def density(serial: str) -> int:
    result = adb(serial, "shell", "wm", "density").stdout
    matches = re.findall(r"(?:Override|Physical) density:\s*(\d+)", result)
    if matches:
        return int(matches[-1])
    raw = prop(serial, "ro.sf.lcd_density")
    if raw.isdigit():
        return int(raw)
    raise SystemExit(f"could not resolve Android density from: {result!r}")


def dump_ui(serial: str) -> ET.Element:
    adb(serial, "shell", "uiautomator", "dump", "/sdcard/glaze-ui.xml")
    raw = adb(serial, "exec-out", "cat", "/sdcard/glaze-ui.xml").stdout
    return ET.fromstring(raw)


def find_text(root: ET.Element, value: str) -> ET.Element | None:
    for node in root.iter("node"):
        if node.attrib.get("text") == value:
            return node
    return None


def assert_contains(root: ET.Element, fragment: str) -> None:
    for node in root.iter("node"):
        if fragment in node.attrib.get("text", ""):
            return
    raise SystemExit(f"required UI fragment not found: {fragment}")


def bounds(node: ET.Element) -> tuple[int, int, int, int]:
    match = BOUNDS.fullmatch(node.attrib.get("bounds", ""))
    if not match:
        raise SystemExit(f"invalid/missing UI bounds: {node.attrib.get('bounds')!r}")
    return tuple(map(int, match.groups()))


def screenshot(serial: str, path: Path) -> str:
    result = adb(serial, "exec-out", "screencap", "-p", text=False)
    path.write_bytes(result.stdout)
    payload = path.read_bytes()
    if not payload.startswith(b"\x89PNG\r\n\x1a\n"):
        raise SystemExit(f"invalid screenshot PNG: {path}")
    return hashlib.sha256(payload).hexdigest()


def launch(serial: str, extras: list[str]) -> None:
    adb(serial, "shell", "am", "force-stop", PACKAGE)
    result = adb(serial, "shell", "am", "start", "-W", "-n", ACTIVITY, *extras).stdout
    if "Status: ok" not in result:
        raise SystemExit(f"activity launch failed:\n{result}")
    time.sleep(1.0)


def target_height_dp(node: ET.Element, dpi: int) -> float:
    _, y1, _, y2 = bounds(node)
    return (y2 - y1) * 160.0 / dpi


def visible_after_scroll(serial: str, value: str, attempts: int = 5) -> tuple[ET.Element, ET.Element]:
    for _ in range(attempts + 1):
        ui = dump_ui(serial)
        node = find_text(ui, value)
        if node is not None:
            return ui, node
        adb(serial, "shell", "input", "swipe", "500", "1500", "500", "450", "300")
        time.sleep(0.3)
    raise SystemExit(f"UI element did not become reachable after scrolling: {value}")


def case_light(serial: str, dpi: int) -> dict:
    launch(serial, ["--es", "appearance", "light"])
    ui, button = visible_after_scroll(serial, "Continue")
    assert_contains(ui, "Appearance: Light")
    assert_contains(ui, "Material Clarity: Balanced")
    assert_contains(ui, "Target floor: 48 dp")
    assert_contains(ui, "no live GoreeCloud state")
    height = target_height_dp(button, dpi)
    if height < 47.0:
        raise SystemExit(f"Continue target below 48 dp floor: {height:.2f} dp")
    x1, y1, x2, y2 = bounds(button)
    adb(serial, "shell", "input", "tap", str((x1 + x2) // 2), str((y1 + y2) // 2))
    time.sleep(0.4)
    ui = dump_ui(serial)
    assert_contains(ui, "Reference action state: Completed")
    sha = screenshot(serial, OUT / "android-light-balanced.png")
    return {"id": "light-balanced-action", "targetDp": round(height, 2), "screenshotSha256": sha}


def case_deep_dark(serial: str, dpi: int) -> dict:
    launch(serial, [
        "--es", "appearance", "deep-dark",
        "--ez", "reducedTransparency", "true",
    ])
    ui, button = visible_after_scroll(serial, "Continue")
    assert_contains(ui, "Appearance: Deep Dark")
    assert_contains(ui, "Material Clarity: Solid")
    assert_contains(ui, "Canvas: true black")
    assert_contains(ui, "Reduced Transparency: Solid interaction treatment")
    height = target_height_dp(button, dpi)
    if height < 47.0:
        raise SystemExit(f"Deep Dark target below 48 dp floor: {height:.2f} dp")
    sha = screenshot(serial, OUT / "android-deep-dark-solid.png")
    return {"id": "deep-dark-reduced-transparency", "targetDp": round(height, 2), "screenshotSha256": sha}


def case_large_text_touch(serial: str, dpi: int) -> dict:
    adb(serial, "shell", "settings", "put", "system", "font_scale", "2.0")
    launch(serial, [
        "--es", "appearance", "dark",
        "--ez", "touchAssistance", "true",
    ])
    ui = dump_ui(serial)
    assert_contains(ui, "Glaze UI 2.1")
    assert_contains(ui, "Appearance: Dark")
    assert_contains(ui, "Touch Assistance: 56 dp minimum target")
    assert_contains(ui, "Target floor: 56 dp")
    sha = screenshot(serial, OUT / "android-large-text-touch-assistance.png")
    ui, button = visible_after_scroll(serial, "Continue", attempts=7)
    height = target_height_dp(button, dpi)
    if height < 55.0:
        raise SystemExit(f"Touch Assistance target below 56 dp floor: {height:.2f} dp")
    return {"id": "large-text-touch-assistance", "targetDp": round(height, 2), "screenshotSha256": sha}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    source_revision = exact_source_revision()
    serial = serial_from_adb()
    dpi = density(serial)
    original_font_scale = adb(serial, "shell", "settings", "get", "system", "font_scale").stdout.strip() or "1.0"

    try:
        adb(serial, "shell", "settings", "put", "system", "font_scale", "1.0")
        cases = [
            case_light(serial, dpi),
            case_deep_dark(serial, dpi),
            case_large_text_touch(serial, dpi),
        ]
    finally:
        adb(serial, "shell", "settings", "put", "system", "font_scale", original_font_scale, check=False)
        adb(serial, "shell", "am", "force-stop", PACKAGE, check=False)

    evidence = {
        "schemaVersion": 1,
        "candidateVersion": "2.1.0-candidate.1",
        "sourceRevision": source_revision,
        "platform": "android-handheld-emulator",
        "physicalDevice": False,
        "talkBackAccepted": False,
        "humanVisualExcellenceAccepted": False,
        "device": {
            "serial": serial,
            "model": prop(serial, "ro.product.model"),
            "release": prop(serial, "ro.build.version.release"),
            "sdk": prop(serial, "ro.build.version.sdk"),
            "fingerprint": prop(serial, "ro.build.fingerprint"),
            "densityDpi": dpi,
        },
        "cases": cases,
        "boundary": (
            "Emulator install/launch/layout/action evidence only; not physical-device, "
            "TalkBack, OEM, production-signing, distribution, or human Visual Excellence acceptance."
        ),
    }
    (OUT / "android-native-evidence.json").write_text(
        json.dumps(evidence, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Glaze UI 2.1 Android native emulator acceptance passed: {len(cases)} cases at {source_revision}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
