#!/usr/bin/env python3
"""Native Android emulator acceptance for the Glaze UI 2.2 Candidate reference.

This proves bounded framework-native System Shell, Universal Search, Control
Center, target-size and fallback behavior on an attached Android emulator. It
does not establish physical-device, TalkBack, OEM, signing/distribution, human
Visual Excellence, downstream-application, or Stable acceptance.
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
OUT = ROOT / ".artifacts" / "glaze-2.2-android-native"
PACKAGE = "com.goreecloud.glazeui.reference.android22"
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
        raise SystemExit(f"could not resolve exact source revision: {revision!r}")
    expected = os.environ.get("GLAZE_SOURCE_REVISION", "").strip()
    if expected and expected != revision:
        raise SystemExit(f"exact source mismatch: checkout={revision}, expected={expected}")
    return revision


def serial_from_adb() -> str:
    explicit = os.environ.get("ANDROID_SERIAL", "").strip()
    if explicit:
        return explicit
    devices = []
    for line in run("adb", "devices").stdout.splitlines()[1:]:
        columns = line.split()
        if len(columns) >= 2 and columns[1] == "device":
            devices.append(columns[0])
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
    raise SystemExit(f"could not resolve Android density: {result!r}")


def dump_ui(serial: str) -> ET.Element:
    adb(serial, "shell", "uiautomator", "dump", "/sdcard/glaze-ui-22.xml")
    raw = adb(serial, "exec-out", "cat", "/sdcard/glaze-ui-22.xml").stdout
    return ET.fromstring(raw)


def find_text(root: ET.Element, value: str) -> ET.Element | None:
    for node in root.iter("node"):
        if node.attrib.get("text") == value:
            return node
    return None


def find_desc(root: ET.Element, value: str) -> ET.Element | None:
    for node in root.iter("node"):
        if node.attrib.get("content-desc") == value:
            return node
    return None


def assert_contains(root: ET.Element, fragment: str) -> None:
    for node in root.iter("node"):
        if fragment in node.attrib.get("text", "") or fragment in node.attrib.get("content-desc", ""):
            return
    raise SystemExit(f"required native UI fragment not found: {fragment}")


def assert_absent_exact(root: ET.Element, value: str) -> None:
    if find_text(root, value) is not None:
        raise SystemExit(f"unexpected native UI element remained visible: {value}")


def bounds(node: ET.Element) -> tuple[int, int, int, int]:
    match = BOUNDS.fullmatch(node.attrib.get("bounds", ""))
    if not match:
        raise SystemExit(f"invalid UI bounds: {node.attrib.get('bounds')!r}")
    return tuple(map(int, match.groups()))


def target_height_dp(node: ET.Element, dpi: int) -> float:
    _, y1, _, y2 = bounds(node)
    return (y2 - y1) * 160.0 / dpi


def tap(serial: str, node: ET.Element) -> None:
    x1, y1, x2, y2 = bounds(node)
    adb(serial, "shell", "input", "tap", str((x1 + x2) // 2), str((y1 + y2) // 2))
    time.sleep(0.35)


def launch(serial: str, extras: list[str]) -> None:
    adb(serial, "shell", "am", "force-stop", PACKAGE)
    result = adb(serial, "shell", "am", "start", "-W", "-n", ACTIVITY, *extras).stdout
    if "Status: ok" not in result:
        raise SystemExit(f"native 2.2 activity launch failed:\n{result}")
    time.sleep(0.8)


def screenshot(serial: str, path: Path) -> str:
    result = adb(serial, "exec-out", "screencap", "-p", text=False)
    path.write_bytes(result.stdout)
    payload = path.read_bytes()
    if not payload.startswith(b"\x89PNG\r\n\x1a\n"):
        raise SystemExit(f"invalid screenshot PNG: {path}")
    return hashlib.sha256(payload).hexdigest()


def find_reachable(serial: str, value: str, *, desc: bool = False, attempts: int = 8) -> tuple[ET.Element, ET.Element]:
    finder = find_desc if desc else find_text
    directions = [
        ("500", "1600", "500", "500"),
        ("500", "1600", "500", "500"),
        ("500", "1600", "500", "500"),
        ("500", "500", "500", "1600"),
        ("500", "500", "500", "1600"),
        ("500", "500", "500", "1600"),
    ]
    for index in range(attempts + 1):
        ui = dump_ui(serial)
        node = finder(ui, value)
        if node is not None:
            return ui, node
        swipe = directions[index % len(directions)]
        adb(serial, "shell", "input", "swipe", *swipe, "250")
        time.sleep(0.25)
    raise SystemExit(f"native UI element did not become reachable: {value}")


def fully_revealed_target(
    serial: str,
    value: str,
    dpi: int,
    floor_dp: float,
    *,
    desc: bool = False,
    attempts: int = 8,
    reveal_attempts: int = 4,
) -> tuple[ET.Element, ET.Element, float]:
    """Return a reachable target only after its native bounds expose the full target.

    UIAutomator clips bounds at a ScrollView or IME viewport edge. A partially
    visible 48/56 dp control can therefore look smaller and its clipped center
    can land on the keyboard instead of the control. Keep the target floors
    unchanged and reveal the control before measuring or tapping it.
    """
    finder = find_desc if desc else find_text
    ui, node = find_reachable(serial, value, desc=desc, attempts=attempts)
    height = target_height_dp(node, dpi)
    required = floor_dp - 1.0

    for _ in range(reveal_attempts):
        if height >= required:
            return ui, node, height
        adb(serial, "shell", "input", "swipe", "500", "1550", "500", "1200", "220")
        time.sleep(0.25)
        ui = dump_ui(serial)
        refreshed = finder(ui, value)
        if refreshed is None:
            continue
        node = refreshed
        height = target_height_dp(node, dpi)

    return ui, node, height


def require_target(node: ET.Element, dpi: int, floor: float, label: str) -> float:
    height = target_height_dp(node, dpi)
    if height < floor - 1.0:
        raise SystemExit(f"{label} target below {floor:.0f} dp floor: {height:.2f} dp")
    return height


def dismiss_ime(serial: str) -> None:
    """Dismiss the software keyboard without closing the active Search panel."""
    adb(serial, "shell", "input", "keyevent", "4")
    time.sleep(0.35)
    ui = dump_ui(serial)
    assert_contains(ui, "Dominant panel: Universal Search")


def case_search_and_exclusivity(serial: str, dpi: int) -> dict:
    launch(serial, ["--es", "appearance", "light"])
    ui = dump_ui(serial)
    assert_contains(ui, "Glaze UI 2.2 Candidate")
    assert_contains(ui, "Current Stable: 2.1.0")
    assert_contains(ui, "Target floor: 48 dp")
    _, search_invoker, invoker_dp = fully_revealed_target(serial, "Open Search", dpi, 48.0)
    require_target(search_invoker, dpi, 48.0, "Open Search")
    tap(serial, search_invoker)
    ui = dump_ui(serial)
    assert_contains(ui, "Dominant panel: Universal Search")
    assert_contains(ui, "Generated answer · Source: Project Brief")
    search_input = find_desc(ui, "Search everything")
    if search_input is None or search_input.attrib.get("focused") != "true":
        raise SystemExit("Universal Search did not move native focus immediately to the query field")
    result = find_text(ui, "Project Brief")
    if result is None:
        raise SystemExit("deterministic Project Brief result missing")
    result_dp = require_target(result, dpi, 48.0, "Project Brief")

    dismiss_ime(serial)
    _, delete, delete_dp = fully_revealed_target(serial, "Delete local cache", dpi, 48.0)
    require_target(delete, dpi, 48.0, "Delete local cache")
    tap(serial, delete)
    ui, confirm, confirm_dp = fully_revealed_target(serial, "Confirm Delete local cache", dpi, 48.0)
    assert_contains(ui, "Search action: Confirmation required")
    require_target(confirm, dpi, 48.0, "Confirm Delete local cache")
    tap(serial, confirm)
    ui = dump_ui(serial)
    assert_contains(ui, "Search action: Deleted local cache")

    _, control_invoker, control_invoker_dp = fully_revealed_target(serial, "Open Control Center", dpi, 48.0)
    require_target(control_invoker, dpi, 48.0, "Open Control Center")
    tap(serial, control_invoker)
    ui = dump_ui(serial)
    assert_contains(ui, "Dominant panel: Control Center")
    assert_absent_exact(ui, "Universal Search")
    sha = screenshot(serial, OUT / "android-22-light-search-control-exclusivity.png")
    return {
        "id": "light-search-control-exclusivity",
        "invokerTargetDp": round(invoker_dp, 2),
        "resultTargetDp": round(result_dp, 2),
        "deleteTargetDp": round(delete_dp, 2),
        "confirmTargetDp": round(confirm_dp, 2),
        "controlInvokerTargetDp": round(control_invoker_dp, 2),
        "screenshotSha256": sha,
    }


def case_control_center_reduced_transparency(serial: str, dpi: int) -> dict:
    launch(serial, ["--es", "appearance", "dark", "--ez", "reducedTransparency", "true"])
    ui = dump_ui(serial)
    assert_contains(ui, "Appearance: Dark")
    assert_contains(ui, "Reduced Transparency: Solid system panels")
    _, control_invoker, _ = fully_revealed_target(serial, "Open Control Center", dpi, 48.0)
    tap(serial, control_invoker)
    ui, wifi, wifi_dp = fully_revealed_target(serial, "Wi-Fi: On", dpi, 48.0)
    require_target(wifi, dpi, 48.0, "Wi-Fi")
    tap(serial, wifi)
    ui = dump_ui(serial)
    assert_contains(ui, "Wi-Fi: Off")
    _, brightness, brightness_dp = fully_revealed_target(serial, "Brightness 64 percent", dpi, 48.0, desc=True)
    require_target(brightness, dpi, 48.0, "Brightness")
    assert_contains(ui, "Dominant panel: Control Center")
    sha = screenshot(serial, OUT / "android-22-dark-control-solid.png")
    return {"id": "dark-control-reduced-transparency", "wifiTargetDp": round(wifi_dp, 2), "rangeTargetDp": round(brightness_dp, 2), "screenshotSha256": sha}


def case_large_text_touch_assistance(serial: str, dpi: int) -> dict:
    adb(serial, "shell", "settings", "put", "system", "font_scale", "2.0")
    launch(serial, ["--es", "appearance", "deep-dark", "--ez", "touchAssistance", "true"])
    ui = dump_ui(serial)
    assert_contains(ui, "Glaze UI 2.2 Candidate")
    _, target_text = find_reachable(serial, "Target floor: 56 dp")
    if target_text is None:
        raise SystemExit("Touch Assistance target-floor label missing")
    _, search_invoker, invoker_dp = fully_revealed_target(serial, "Open Search", dpi, 56.0)
    require_target(search_invoker, dpi, 56.0, "Touch Assistance Open Search")
    tap(serial, search_invoker)

    ui = dump_ui(serial)
    assert_contains(ui, "Dominant panel: Universal Search")
    search_input = find_desc(ui, "Search everything")
    if search_input is None or search_input.attrib.get("focused") != "true":
        raise SystemExit("Large Text Universal Search did not focus the native query field")
    dismiss_ime(serial)
    _, result, result_dp = fully_revealed_target(serial, "Project Brief", dpi, 56.0)
    require_target(result, dpi, 56.0, "Touch Assistance Project Brief")
    # At 200% text, provenance may validly reflow below the result viewport. It
    # must remain reachable, but need not be simultaneously visible with Best Match.
    find_reachable(serial, "Generated answer · Source: Project Brief", attempts=8)
    sha = screenshot(serial, OUT / "android-22-large-text-touch-assistance.png")
    return {"id": "large-text-touch-assistance", "invokerTargetDp": round(invoker_dp, 2), "resultTargetDp": round(result_dp, 2), "screenshotSha256": sha}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    revision = exact_source_revision()
    serial = serial_from_adb()
    dpi = density(serial)
    original_font_scale = adb(serial, "shell", "settings", "get", "system", "font_scale").stdout.strip() or "1.0"
    try:
        adb(serial, "shell", "settings", "put", "system", "font_scale", "1.0")
        cases = [
            case_search_and_exclusivity(serial, dpi),
            case_control_center_reduced_transparency(serial, dpi),
            case_large_text_touch_assistance(serial, dpi),
        ]
    finally:
        adb(serial, "shell", "settings", "put", "system", "font_scale", original_font_scale, check=False)
        adb(serial, "shell", "am", "force-stop", PACKAGE, check=False)

    evidence = {
        "schemaVersion": 1,
        "candidateVersion": "2.2.0-candidate.1",
        "stableBaseline": "2.1.0",
        "consumerEligible": False,
        "sourceRevision": revision,
        "platform": "android-handheld-emulator",
        "physicalDevice": False,
        "talkBackAccepted": False,
        "switchAccessAccepted": False,
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
        "boundary": "Hosted Android emulator evidence for the bounded design-system reference only; not physical-device, OEM, TalkBack, Switch Access, signing/distribution, downstream application, or Human Visual Excellence acceptance.",
    }
    (OUT / "android-native-evidence.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(f"Glaze UI 2.2 Android native emulator acceptance passed: {len(cases)} cases at {revision}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
