#!/usr/bin/env python3
"""Fresh Android handheld emulator acceptance for the GLAZE UI V1.1 release candidate.

This gate proves bounded framework-native appearance mapping, target geometry,
Reduced Transparency fallback, basic native interaction, and exact-revision
emulator evidence. It does not establish OEM-wide, physical-device, TalkBack,
signing/distribution, downstream application, or production-deployment acceptance.
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
OUT = ROOT / ".artifacts" / "glaze-v1.1-android-native"
PACKAGE = "com.goreecloud.glazeui.reference.v11"
ACTIVITY = f"{PACKAGE}/.MainActivity"
BOUNDS = re.compile(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]")
SHA40 = re.compile(r"^[0-9a-f]{40}$")


def run(*args: str, text: bool = True, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(args, check=check, text=text, capture_output=True)


def adb(serial: str, *args: str, text: bool = True, check: bool = True) -> subprocess.CompletedProcess:
    return run("adb", "-s", serial, *args, text=text, check=check)


def exact_revision() -> str:
    revision = run("git", "-C", str(ROOT), "rev-parse", "HEAD").stdout.strip()
    if not SHA40.fullmatch(revision):
        raise SystemExit(f"could not resolve exact source revision: {revision!r}")
    expected = os.environ.get("GLAZE_SOURCE_REVISION", "").strip()
    if expected and expected != revision:
        raise SystemExit(f"exact source mismatch: checkout={revision}, expected={expected}")
    return revision


def serial_from_adb() -> str:
    explicit = os.environ.get("ANDROID_SERIAL", "").strip()
    if explicit:
        return explicit
    devices: list[str] = []
    for line in run("adb", "devices").stdout.splitlines()[1:]:
        columns = line.split()
        if len(columns) >= 2 and columns[1] == "device":
            devices.append(columns[0])
    if len(devices) != 1:
        raise SystemExit(f"expected exactly one ready Android target, found {devices}")
    return devices[0]


def density(serial: str) -> int:
    result = adb(serial, "shell", "wm", "density").stdout
    matches = re.findall(r"(?:Override|Physical) density:\s*(\d+)", result)
    if matches:
        return int(matches[-1])
    raw = adb(serial, "shell", "getprop", "ro.sf.lcd_density").stdout.strip()
    if raw.isdigit():
        return int(raw)
    raise SystemExit(f"could not resolve Android density: {result!r}")


def dump_ui(serial: str) -> ET.Element:
    path = "/sdcard/glaze-v11.xml"
    adb(serial, "shell", "uiautomator", "dump", path)
    raw = adb(serial, "exec-out", "cat", path).stdout
    return ET.fromstring(raw)


def contains(root: ET.Element, fragment: str) -> bool:
    for node in root.iter("node"):
        if fragment in node.attrib.get("text", "") or fragment in node.attrib.get("content-desc", ""):
            return True
    return False


def require_contains(root: ET.Element, fragment: str) -> None:
    if not contains(root, fragment):
        raise SystemExit(f"required native UI fragment not found: {fragment}")


def find_desc(root: ET.Element, value: str) -> ET.Element | None:
    for node in root.iter("node"):
        if node.attrib.get("content-desc") == value:
            return node
    return None


def bounds(node: ET.Element) -> tuple[int, int, int, int]:
    match = BOUNDS.fullmatch(node.attrib.get("bounds", ""))
    if not match:
        raise SystemExit(f"invalid UI bounds: {node.attrib.get('bounds')!r}")
    return tuple(map(int, match.groups()))


def height_dp(node: ET.Element, dpi: int) -> float:
    _, y1, _, y2 = bounds(node)
    return (y2 - y1) * 160.0 / dpi


def find_reachable_desc(serial: str, value: str, attempts: int = 10) -> ET.Element:
    for index in range(attempts + 1):
        ui = dump_ui(serial)
        node = find_desc(ui, value)
        if node is not None:
            return node
        if index % 4 == 3:
            adb(serial, "shell", "input", "swipe", "520", "700", "520", "1750", "240")
        else:
            adb(serial, "shell", "input", "swipe", "520", "1750", "520", "650", "240")
        time.sleep(0.25)
    raise SystemExit(f"native UI element did not become reachable: {value}")


def require_target(serial: str, desc: str, dpi: int, floor: float) -> float:
    node = find_reachable_desc(serial, desc)
    measured = height_dp(node, dpi)
    if measured < floor - 1.0:
        # UIAutomator clips a partially visible node at the ScrollView edge.
        for _ in range(4):
            adb(serial, "shell", "input", "swipe", "520", "1500", "520", "1150", "180")
            time.sleep(0.2)
            refreshed = find_desc(dump_ui(serial), desc)
            if refreshed is not None:
                node = refreshed
                measured = height_dp(node, dpi)
                if measured >= floor - 1.0:
                    break
    if measured < floor - 1.0:
        raise SystemExit(f"{desc} target below {floor:.0f} dp floor: {measured:.2f} dp")
    return measured


def tap_desc(serial: str, desc: str) -> None:
    node = find_reachable_desc(serial, desc)
    x1, y1, x2, y2 = bounds(node)
    adb(serial, "shell", "input", "tap", str((x1 + x2) // 2), str((y1 + y2) // 2))
    time.sleep(0.4)


def launch(serial: str, *, appearance: str, reduced: bool = False, touch: bool = False) -> None:
    adb(serial, "shell", "am", "force-stop", PACKAGE)
    args = ["shell", "am", "start", "-W", "-n", ACTIVITY, "--es", "appearance", appearance]
    if reduced:
        args += ["--ez", "reducedTransparency", "true"]
    if touch:
        args += ["--ez", "touchAssistance", "true"]
    result = adb(serial, *args).stdout
    if "Status: ok" not in result:
        raise SystemExit(f"native V1.1 activity launch failed:\n{result}")
    time.sleep(0.8)


def screenshot(serial: str, name: str) -> tuple[str, str]:
    path = OUT / name
    result = adb(serial, "exec-out", "screencap", "-p", text=False)
    path.write_bytes(result.stdout)
    payload = path.read_bytes()
    if not payload.startswith(b"\x89PNG\r\n\x1a\n"):
        raise SystemExit(f"invalid screenshot PNG: {path}")
    return path.name, hashlib.sha256(payload).hexdigest()


def case_light(serial: str, dpi: int) -> dict:
    launch(serial, appearance="light")
    ui = dump_ui(serial)
    for fragment in ("GLAZE UI V1.1", "Lifecycle: Release Candidate", "Appearance: Light", "Target floor: 48 dp", "bounded Deep Teal + Soft Amber"):
        require_contains(ui, fragment)
    primary_dp = require_target(serial, "Primary action", dpi, 48.0)
    secondary_dp = require_target(serial, "Secondary action", dpi, 48.0)
    tap_desc(serial, "Primary action")
    require_contains(dump_ui(serial), "Action: Complete")
    name, digest = screenshot(serial, "android-v1.1-light.png")
    return {"id": "light", "primaryTargetDp": round(primary_dp, 2), "secondaryTargetDp": round(secondary_dp, 2), "screenshot": name, "sha256": digest}


def case_dark_reduced(serial: str, dpi: int) -> dict:
    launch(serial, appearance="dark", reduced=True)
    ui = dump_ui(serial)
    for fragment in ("Appearance: Dark", "Reduced Transparency: atmosphere suppressed", "Target floor: 48 dp"):
        require_contains(ui, fragment)
    primary_dp = require_target(serial, "Primary action", dpi, 48.0)
    name, digest = screenshot(serial, "android-v1.1-dark-reduced-transparency.png")
    return {"id": "dark-reduced-transparency", "primaryTargetDp": round(primary_dp, 2), "screenshot": name, "sha256": digest}


def case_deep_dark_touch(serial: str, dpi: int) -> dict:
    adb(serial, "shell", "settings", "put", "system", "font_scale", "2.0")
    launch(serial, appearance="deep-dark", touch=True)
    ui = dump_ui(serial)
    for fragment in ("Appearance: Deep Dark", "Touch Assistance: 56 dp minimum target", "Target floor: 56 dp"):
        require_contains(ui, fragment)
    primary_dp = require_target(serial, "Primary action", dpi, 56.0)
    secondary_dp = require_target(serial, "Secondary action", dpi, 56.0)
    name, digest = screenshot(serial, "android-v1.1-deep-dark-large-text-touch.png")
    return {"id": "deep-dark-large-text-touch", "primaryTargetDp": round(primary_dp, 2), "secondaryTargetDp": round(secondary_dp, 2), "screenshot": name, "sha256": digest}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    revision = exact_revision()
    serial = serial_from_adb()
    dpi = density(serial)
    try:
        cases = [case_light(serial, dpi), case_dark_reduced(serial, dpi), case_deep_dark_touch(serial, dpi)]
    finally:
        adb(serial, "shell", "settings", "put", "system", "font_scale", "1.0", check=False)

    evidence = {
        "schemaVersion": 1,
        "product": "GLAZE UI V1.1",
        "lifecycle": "Release Candidate evidence",
        "sourceRevision": revision,
        "platform": "Android handheld emulator",
        "package": PACKAGE,
        "sdk": adb(serial, "shell", "getprop", "ro.build.version.sdk").stdout.strip(),
        "buildFingerprint": adb(serial, "shell", "getprop", "ro.build.fingerprint").stdout.strip(),
        "densityDpi": dpi,
        "cases": cases,
        "boundaries": [
            "not OEM-wide qualification",
            "not physical-device qualification",
            "not TalkBack certification",
            "not signing or distribution acceptance",
            "not downstream application conformance",
            "not production deployment acceptance"
        ]
    }
    evidence_path = OUT / "android-native-evidence.json"
    evidence_path.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evidence, indent=2))
    print("GLAZE UI V1.1 Android handheld emulator acceptance: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
