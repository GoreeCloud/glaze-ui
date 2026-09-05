#!/usr/bin/env python3
"""Fresh Android handheld emulator acceptance for GLAZE UI V1.2 Frosted Neutral Candidate.

The gate proves a bounded framework-native Android implementation of the Candidate
material hierarchy, neutral substrate contract, target geometry, interaction,
Reduced Transparency, Touch Assistance, large-text reachability, and exact-source
screenshot evidence. It does not promote V1.2 to Stable or establish OEM-wide blur
fidelity, physical-device, TalkBack, signing/distribution, downstream application,
or production acceptance.
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
OUT = ROOT / ".artifacts" / "glaze-v1.2-android-native"
SOURCE = ROOT / "reference/v1.2/native/android/app/src/main/java/com/goreecloud/glazeui/reference/v12/MainActivity.java"
PACKAGE = "com.goreecloud.glazeui.reference.v12"
ACTIVITY = f"{PACKAGE}/.MainActivity"
BOUNDS = re.compile(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]")
SHA40 = re.compile(r"^[0-9a-f]{40}$")
NEUTRAL_SURFACE = re.compile(
    r"\b(base|raised|overlay|panel)\s*=\s*Color\.argb\(\d+\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)"
)
NEUTRAL_CRITICAL = re.compile(
    r"\bcritical\s*=\s*Color\.rgb\((\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)"
)


def run(*args: str, text: bool = True, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(args, check=check, text=text, capture_output=True)


def adb(serial: str, *args: str, text: bool = True, check: bool = True) -> subprocess.CompletedProcess:
    return run("adb", "-s", serial, *args, text=text, check=check)


def validate_neutral_surface_source() -> dict:
    source = SOURCE.read_text(encoding="utf-8")
    surfaces = NEUTRAL_SURFACE.findall(source)
    if len(surfaces) < 12:
        raise SystemExit(f"expected explicit neutral base/raised/overlay/panel mappings for all appearances; found {len(surfaces)}")
    checked: list[str] = []
    for role, r, g, b in surfaces:
        channels = tuple(map(int, (r, g, b)))
        if len(set(channels)) != 1:
            raise SystemExit(f"{role} substrate is chromatically tinted in Android Candidate source: {channels}")
        checked.append(f"{role}:{channels[0]}")

    criticals = NEUTRAL_CRITICAL.findall(source)
    if len(criticals) < 3:
        raise SystemExit("expected explicit neutral Critical System mappings for all appearances")
    for r, g, b in criticals:
        channels = tuple(map(int, (r, g, b)))
        if len(set(channels)) != 1:
            raise SystemExit(f"Critical System substrate is chromatically tinted: {channels}")

    required_phrases = (
        "Frosted Neutral, not tinted glass.",
        "Substrate: neutral",
        "Color role: accent only",
        "Neutral translucent glass",
        "Neutral opaque fallback",
    )
    for phrase in required_phrases:
        if phrase not in source:
            raise SystemExit(f"Android Candidate source missing material contract phrase: {phrase}")

    return {"neutralSurfaceAssignments": len(surfaces), "neutralCriticalAssignments": len(criticals)}


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
    path = "/sdcard/glaze-v12.xml"
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


def find_desc_prefix(root: ET.Element, prefix: str) -> ET.Element | None:
    for node in root.iter("node"):
        if node.attrib.get("content-desc", "").startswith(prefix):
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


def swipe_forward(serial: str) -> None:
    adb(serial, "shell", "input", "swipe", "520", "1750", "520", "650", "240")
    time.sleep(0.25)


def swipe_backward(serial: str) -> None:
    adb(serial, "shell", "input", "swipe", "520", "700", "520", "1750", "240")
    time.sleep(0.25)


def require_reachable_contains(serial: str, fragment: str, attempts: int = 14) -> None:
    for index in range(attempts + 1):
        if contains(dump_ui(serial), fragment):
            return
        if index % 5 == 4:
            swipe_backward(serial)
        else:
            swipe_forward(serial)
    raise SystemExit(f"required reachable native UI fragment not found: {fragment}")


def find_reachable_desc(serial: str, value: str, attempts: int = 12) -> ET.Element:
    for index in range(attempts + 1):
        ui = dump_ui(serial)
        node = find_desc(ui, value)
        if node is not None:
            return node
        if index % 4 == 3:
            swipe_backward(serial)
        else:
            swipe_forward(serial)
    raise SystemExit(f"native UI element did not become reachable: {value}")


def find_reachable_prefix(serial: str, prefix: str, attempts: int = 12) -> ET.Element:
    for index in range(attempts + 1):
        ui = dump_ui(serial)
        node = find_desc_prefix(ui, prefix)
        if node is not None:
            return node
        if index % 4 == 3:
            swipe_backward(serial)
        else:
            swipe_forward(serial)
    raise SystemExit(f"native UI element did not become reachable: {prefix}")


def require_target(serial: str, desc: str, dpi: int, floor: float) -> float:
    node = find_reachable_desc(serial, desc)
    measured = height_dp(node, dpi)
    if measured < floor - 1.0:
        for _ in range(4):
            adb(serial, "shell", "input", "swipe", "520", "1500", "520", "1150", "180")
            time.sleep(0.2)
            refreshed = find_desc(dump_ui(serial), desc)
            if refreshed is not None:
                measured = height_dp(refreshed, dpi)
                if measured >= floor - 1.0:
                    break
    if measured < floor - 1.0:
        raise SystemExit(f"{desc} target below {floor:.0f} dp floor: {measured:.2f} dp")
    return measured


def require_prefix_target(serial: str, prefix: str, dpi: int, floor: float) -> float:
    node = find_reachable_prefix(serial, prefix)
    measured = height_dp(node, dpi)
    if measured < floor - 1.0:
        raise SystemExit(f"{prefix} target below {floor:.0f} dp floor: {measured:.2f} dp")
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
        raise SystemExit(f"native V1.2 activity launch failed:\n{result}")
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
    for fragment in (
        "GLAZE UI V1.2 CANDIDATE",
        "Lifecycle: V1.2 Candidate",
        "Appearance: Light",
        "Material: Neutral translucent glass",
        "Substrate: neutral",
        "Color role: accent only",
    ):
        require_contains(ui, fragment)
    primary_dp = require_target(serial, "Primary action", dpi, 48.0)
    wifi_dp = require_prefix_target(serial, "Wi‑Fi:", dpi, 76.0)
    tap_desc(serial, "Primary action")
    require_contains(dump_ui(serial), "Action: Complete")
    name, digest = screenshot(serial, "android-v1.2-frosted-neutral-light.png")
    return {"id": "light", "primaryTargetDp": round(primary_dp, 2), "wifiTileDp": round(wifi_dp, 2), "screenshot": name, "sha256": digest}


def case_dark_reduced(serial: str, dpi: int) -> dict:
    launch(serial, appearance="dark", reduced=True)
    ui = dump_ui(serial)
    for fragment in (
        "Appearance: Dark",
        "Material: Neutral opaque fallback",
        "Reduced Transparency: enabled",
        "Target floor: 48 dp",
    ):
        require_contains(ui, fragment)
    primary_dp = require_target(serial, "Primary action", dpi, 48.0)
    name, digest = screenshot(serial, "android-v1.2-dark-reduced-transparency.png")
    return {"id": "dark-reduced-transparency", "primaryTargetDp": round(primary_dp, 2), "screenshot": name, "sha256": digest}


def case_deep_dark_touch(serial: str, dpi: int) -> dict:
    adb(serial, "shell", "settings", "put", "system", "font_scale", "2.0")
    launch(serial, appearance="deep-dark", touch=True)
    for fragment in (
        "Appearance: Deep Dark",
        "Touch Assistance: 56 dp minimum target",
        "Target floor: 56 dp",
        "Critical System high opacity non backdrop dependent surface",
    ):
        require_reachable_contains(serial, fragment)
    primary_dp = require_target(serial, "Primary action", dpi, 56.0)
    secondary_dp = require_target(serial, "Secondary action", dpi, 56.0)
    name, digest = screenshot(serial, "android-v1.2-deep-dark-large-text-touch.png")
    return {"id": "deep-dark-large-text-touch", "primaryTargetDp": round(primary_dp, 2), "secondaryTargetDp": round(secondary_dp, 2), "screenshot": name, "sha256": digest}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    source_contract = validate_neutral_surface_source()
    revision = exact_revision()
    serial = serial_from_adb()
    dpi = density(serial)
    try:
        cases = [case_light(serial, dpi), case_dark_reduced(serial, dpi), case_deep_dark_touch(serial, dpi)]
    finally:
        adb(serial, "shell", "settings", "put", "system", "font_scale", "1.0", check=False)

    evidence = {
        "schemaVersion": 1,
        "product": "GLAZE UI V1.2 Frosted Neutral",
        "lifecycle": "Candidate native evidence",
        "sourceRevision": revision,
        "platform": "Android handheld emulator",
        "package": PACKAGE,
        "sdk": adb(serial, "shell", "getprop", "ro.build.version.sdk").stdout.strip(),
        "buildFingerprint": adb(serial, "shell", "getprop", "ro.build.fingerprint").stdout.strip(),
        "densityDpi": dpi,
        "sourceContract": source_contract,
        "cases": cases,
        "boundaries": [
            "not OEM-wide blur fidelity qualification",
            "not physical-device qualification",
            "not TalkBack certification",
            "not signing or distribution acceptance",
            "not downstream application conformance",
            "not production deployment acceptance",
            "not V1.2 Stable promotion"
        ]
    }
    evidence_path = OUT / "android-native-evidence.json"
    evidence_path.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evidence, indent=2))
    print("GLAZE UI V1.2 Frosted Neutral Android handheld emulator acceptance: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
