#!/usr/bin/env python3
"""Headless GTK4 acceptance for the GLAZE UI V1.2 Frosted Neutral Linux Candidate.

Runs the framework-native GTK reference in Xvfb, validates the neutral substrate
contract, native target geometry, runtime modes, basic interaction, and captures
bounded screenshot evidence. Passing this gate is not compositor-wide Wayland
blur fidelity, production shell integration, distribution, downstream conformance,
or V1.2 Stable promotion.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "reference/v1.2/native/linux-gtk"
APP = REFERENCE / "app.py"
CSS = REFERENCE / "glaze-v1.2-linux.css"
CONTRACT = REFERENCE / "material-contract.json"
OUT = ROOT / ".artifacts/glaze-v1.2-linux-native"
SHA40 = re.compile(r"^[0-9a-f]{40}$")


def run(*args: str, check: bool = True, text: bool = True, env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(args, check=check, text=text, capture_output=True, env=env)


def exact_revision() -> str:
    revision = run("git", "-C", str(ROOT), "rev-parse", "HEAD").stdout.strip()
    if not SHA40.fullmatch(revision):
        raise SystemExit(f"could not resolve exact source revision: {revision!r}")
    expected = os.environ.get("GLAZE_SOURCE_REVISION", "").strip()
    if expected and expected != revision:
        raise SystemExit(f"exact source mismatch: checkout={revision}, expected={expected}")
    return revision


def validate_source_contract() -> dict:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    css = CSS.read_text(encoding="utf-8")
    app = APP.read_text(encoding="utf-8")

    if contract.get("product") != "GLAZE UI V1.2 Frosted Neutral":
        raise SystemExit("Linux material contract product authority mismatch")
    if contract.get("lifecycle") != "Candidate":
        raise SystemExit("Linux material contract must remain Candidate")

    neutral_roles = 0
    for appearance in ("light", "dark", "deep-dark"):
        values = contract["appearances"][appearance]
        for role in ("base", "raised", "overlay", "panel", "critical"):
            rgb = values[role]["rgb"]
            if len(rgb) != 3 or len(set(rgb)) != 1:
                raise SystemExit(f"{appearance} {role} substrate is chromatically tinted: {rgb}")
            neutral_roles += 1

    minimum = contract["targets"]["minimumPx"]
    touch = contract["targets"]["touchAssistancePx"]
    tile = contract["targets"]["quickSettingPx"]
    if (minimum, touch, tile) != (48, 56, 76):
        raise SystemExit(f"unexpected Linux target contract: {(minimum, touch, tile)}")

    normalized_css = re.sub(r"\s+", "", css)
    required_css = (
        "rgba(255,255,255,0.58)",
        "rgba(31,31,31,0.68)",
        "rgba(24,24,24,0.68)",
        "rgba(250,250,250,0.88)",
        "rgba(54,54,54,0.90)",
        "rgba(46,46,46,0.90)",
        "rgb(255,255,255)",
        "rgb(30,30,30)",
        "rgb(25,25,25)",
        "min-height:48px",
        "min-height:56px",
        "min-height:76px",
    )
    for token in required_css:
        if token not in normalized_css:
            raise SystemExit(f"GTK Candidate CSS missing contract token: {token}")

    for legacy in ("rgb(15,107,111)", "rgb(28,138,141)", "rgb(143,214,210)"):
        if legacy in normalized_css:
            raise SystemExit(f"legacy teal substrate identity leaked into GTK Candidate CSS: {legacy}")

    required_app_phrases = (
        "Neutral glass is the material.",
        "Neutral panel · accent only on active state",
        "High-opacity clarity stays separate.",
        "not compositor-wide Wayland backdrop blur fidelity",
    )
    for phrase in required_app_phrases:
        if phrase not in app:
            raise SystemExit(f"GTK Candidate reference missing material phrase: {phrase}")

    return {
        "neutralRoleAssignments": neutral_roles,
        "minimumTargetPx": minimum,
        "touchAssistancePx": touch,
        "quickSettingPx": tile,
    }


def wait_for_file(path: Path, process: subprocess.Popen, timeout: float = 15.0) -> dict:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if path.exists() and path.stat().st_size > 0:
            return json.loads(path.read_text(encoding="utf-8"))
        code = process.poll()
        if code is not None:
            stdout, stderr = process.communicate(timeout=2)
            raise SystemExit(f"GTK Candidate exited before evidence was ready ({code})\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}")
        time.sleep(0.1)
    process.terminate()
    stdout, stderr = process.communicate(timeout=4)
    raise SystemExit(f"timed out waiting for GTK Candidate evidence\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}")


def screenshot(path: Path, env: dict[str, str]) -> str:
    result = run("import", "-window", "root", str(path), check=False, env=env)
    if result.returncode != 0:
        raise SystemExit(f"ImageMagick root screenshot failed:\n{result.stderr}")
    payload = path.read_bytes()
    if not payload.startswith(b"\x89PNG\r\n\x1a\n"):
        raise SystemExit(f"invalid Linux screenshot PNG: {path}")
    return hashlib.sha256(payload).hexdigest()


def require_target(name: str, value: int, floor: int) -> None:
    if value < floor:
        raise SystemExit(f"{name} target below {floor}px floor: {value}px")


def run_case(case_id: str, args: list[str], *, minimum: int, tile_floor: int, env: dict[str, str]) -> dict:
    case_dir = OUT / case_id
    case_dir.mkdir(parents=True, exist_ok=True)
    evidence_path = case_dir / "runtime.json"
    shot_path = OUT / f"linux-v1.2-{case_id}.png"
    if evidence_path.exists():
        evidence_path.unlink()

    command = [sys.executable, str(APP), *args, "--evidence-file", str(evidence_path), "--auto-interact"]
    process = subprocess.Popen(command, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        evidence = wait_for_file(evidence_path, process)
        if not evidence.get("ready"):
            raise SystemExit(f"{case_id} runtime did not report ready")
        if evidence.get("lifecycle") != "Candidate native evidence":
            raise SystemExit(f"{case_id} runtime lifecycle drift: {evidence.get('lifecycle')}")
        if evidence.get("materialAuthority") != "neutral substrate; color reserved for accent/state":
            raise SystemExit(f"{case_id} material authority mismatch")
        if evidence.get("criticalSystem") != "high-opacity; non-backdrop-dependent":
            raise SystemExit(f"{case_id} Critical System authority mismatch")
        if evidence.get("interactionState") != "Action: Complete":
            raise SystemExit(f"{case_id} native interaction did not complete")

        targets = evidence["targets"]
        require_target(f"{case_id} primary", int(targets["primary"]), minimum)
        require_target(f"{case_id} secondary", int(targets["secondary"]), minimum)
        require_target(f"{case_id} search", int(targets["search"]), minimum)
        for name, height in targets["tiles"].items():
            require_target(f"{case_id} {name}", int(height), tile_floor)

        win = evidence["window"]
        if int(win["width"]) < 740 or int(win["height"]) < 600:
            raise SystemExit(f"{case_id} window unexpectedly small: {win}")

        digest = screenshot(shot_path, env)
        return {
            "id": case_id,
            "appearance": evidence["appearance"],
            "reducedTransparency": evidence["reducedTransparency"],
            "touchAssistance": evidence["touchAssistance"],
            "largeText": evidence["largeText"],
            "gtkVersion": evidence["gtkVersion"],
            "window": win,
            "targets": targets,
            "interactionState": evidence["interactionState"],
            "screenshot": shot_path.name,
            "sha256": digest,
        }
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=4)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=2)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    source_contract = validate_source_contract()
    revision = exact_revision()

    env = os.environ.copy()
    env.setdefault("GDK_BACKEND", "x11")
    if not env.get("DISPLAY"):
        raise SystemExit("DISPLAY is required; run under xvfb-run or an X11 session")

    cases = [
        run_case("frosted-neutral-light", ["--appearance", "light"], minimum=48, tile_floor=76, env=env),
        run_case(
            "dark-reduced-transparency",
            ["--appearance", "dark", "--reduced-transparency"],
            minimum=48,
            tile_floor=76,
            env=env,
        ),
        run_case(
            "deep-dark-large-text-touch",
            ["--appearance", "deep-dark", "--large-text", "--touch-assistance"],
            minimum=56,
            tile_floor=76,
            env=env,
        ),
    ]

    evidence = {
        "schemaVersion": 1,
        "product": "GLAZE UI V1.2 Frosted Neutral",
        "lifecycle": "Candidate native evidence",
        "sourceRevision": revision,
        "platform": "Linux GTK4 under Xvfb",
        "sourceContract": source_contract,
        "cases": cases,
        "boundaries": [
            "not compositor-wide Wayland backdrop blur fidelity",
            "not production shell integration",
            "not distribution packaging acceptance",
            "not physical-display qualification",
            "not assistive-technology certification",
            "not downstream application conformance",
            "not V1.2 Stable promotion",
        ],
    }
    evidence_path = OUT / "linux-native-evidence.json"
    evidence_path.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evidence, indent=2))
    print("GLAZE UI V1.2 Frosted Neutral Linux GTK4 native acceptance: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
