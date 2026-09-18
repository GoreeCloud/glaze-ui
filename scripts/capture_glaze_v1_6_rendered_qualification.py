#!/usr/bin/env python3
"""Capture exact-source GLAZE UI V1.6 rendered-browser qualification evidence."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

HOST = "127.0.0.1"
WEB_PORT = 8816
DRIVER_PORT = 9566
SERVER = f"http://{HOST}:{WEB_PORT}"
DRIVER = f"http://{HOST}:{DRIVER_PORT}"
SOURCE_REVISION = "c7509c79256b04b0aa67cb9dd0737d7588e0ae4a"


class QualificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise QualificationError(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing JSON file: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"JSON root must be an object: {path}")
    return value


def webdriver_request(method: str, path: str, payload: dict[str, Any] | None = None, timeout: int = 30) -> Any:
    request = Request(
        f"{DRIVER}{path}",
        data=None if payload is None else json.dumps(payload).encode("utf-8"),
        method=method,
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            raw = response.read()
    except HTTPError as error:
        body = error.read().decode(errors="replace")
        raise QualificationError(f"WebDriver HTTP {error.code}: {body}") from error
    except (URLError, TimeoutError) as error:
        raise QualificationError(f"WebDriver request failed: {error}") from error
    if not raw:
        return None
    decoded = json.loads(raw.decode("utf-8"))
    value = decoded.get("value")
    if isinstance(value, dict) and value.get("error"):
        raise QualificationError(f"WebDriver {value.get('error')}: {value.get('message', '')}")
    return value


def wait_http(url: str, seconds: float = 15) -> None:
    end = time.monotonic() + seconds
    last: Exception | None = None
    while time.monotonic() < end:
        try:
            with urlopen(url, timeout=1) as response:
                if response.status == 200:
                    return
        except Exception as error:  # pragma: no cover - diagnostic path
            last = error
        time.sleep(0.15)
    raise QualificationError(f"HTTP endpoint not ready: {last}")


def chromedriver() -> str:
    candidates = (
        shutil.which("chromedriver"),
        "/usr/bin/chromedriver",
        "/usr/local/share/chromedriver-linux64/chromedriver",
    )
    for item in candidates:
        if item and Path(item).is_file():
            return str(item)
    raise QualificationError("chromedriver unavailable")


def wait_driver() -> None:
    end = time.monotonic() + 15
    last: Exception | None = None
    while time.monotonic() < end:
        try:
            status = webdriver_request("GET", "/status")
            if isinstance(status, dict) and status.get("ready"):
                return
        except Exception as error:  # pragma: no cover - diagnostic path
            last = error
        time.sleep(0.2)
    raise QualificationError(f"chromedriver not ready: {last}")


def create_session() -> str:
    value = webdriver_request(
        "POST",
        "/session",
        {
            "capabilities": {
                "alwaysMatch": {
                    "browserName": "chrome",
                    "goog:chromeOptions": {
                        "args": [
                            "--headless=new",
                            "--no-sandbox",
                            "--disable-dev-shm-usage",
                            "--disable-background-networking",
                            "--disable-component-update",
                            "--disable-default-apps",
                            "--disable-extensions",
                            "--disable-sync",
                            "--metrics-recording-only",
                            "--no-first-run",
                            "--hide-scrollbars",
                            "--window-size=1440,1200",
                        ]
                    },
                }
            }
        },
        timeout=60,
    )
    require(isinstance(value, dict) and isinstance(value.get("sessionId"), str), "Chrome returned no session id")
    return value["sessionId"]


def execute(session_id: str, script: str) -> Any:
    return webdriver_request(
        "POST",
        f"/session/{session_id}/execute/sync",
        {"script": script, "args": []},
    )


def cdp(session_id: str, command: str, params: dict[str, Any] | None = None) -> Any:
    return webdriver_request(
        "POST",
        f"/session/{session_id}/goog/cdp/execute",
        {"cmd": command, "params": params or {}},
    )


def set_viewport(session_id: str, width: int, height: int, mobile: bool) -> None:
    cdp(
        session_id,
        "Emulation.setDeviceMetricsOverride",
        {
            "width": width,
            "height": height,
            "deviceScaleFactor": 1,
            "mobile": mobile,
            "screenWidth": width,
            "screenHeight": height,
        },
    )
    cdp(
        session_id,
        "Emulation.setTouchEmulationEnabled",
        {"enabled": mobile, "maxTouchPoints": 5 if mobile else 1},
    )


def set_media(session_id: str, features: list[dict[str, str]]) -> None:
    cdp(session_id, "Emulation.setEmulatedMedia", {"media": "screen", "features": features})


def wait_ready(session_id: str, seconds: float = 20) -> None:
    end = time.monotonic() + seconds
    last: Any = None
    while time.monotonic() < end:
        last = execute(
            session_id,
            "return document.readyState==='complete' && window.__glazeV16RenderedReady===true;",
        )
        if last is True:
            return
        time.sleep(0.1)
    raise QualificationError(f"rendered qualification scene did not become ready: {last}")


def screenshot(session_id: str, path: Path) -> None:
    encoded = webdriver_request("GET", f"/session/{session_id}/screenshot")
    require(isinstance(encoded, str) and encoded, f"no screenshot bytes for {path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(base64.b64decode(encoded))
    require(path.stat().st_size > 5000, f"invalid screenshot: {path}")


def git_revision(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True, stderr=subprocess.STDOUT
        ).strip()
    except Exception as error:
        raise QualificationError(f"could not resolve git revision for {root}: {error}") from error


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


def freeze_after_measurement(session_id: str) -> None:
    result = execute(
        session_id,
        """
let style=document.getElementById('glz16-capture-freeze');
if(!style){
  style=document.createElement('style');
  style.id='glz16-capture-freeze';
  style.textContent='*,*::before,*::after{animation:none!important;transition:none!important;caret-color:transparent!important;scroll-behavior:auto!important}';
  document.head.appendChild(style);
}
window.scrollTo(0,0);
return true;
""",
    )
    require(result is True, "could not freeze scene for deterministic screenshot")
    execute(session_id, "return new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(()=>resolve(true))));")


def capture(
    render_root: Path,
    source_root: Path,
    tooling_root: Path,
    plan_path: Path,
    output: Path,
) -> dict[str, Any]:
    plan = load_json(plan_path)
    require(plan.get("sourceRevision") == SOURCE_REVISION, "rendered plan source revision drifted")
    require(plan.get("networkPolicy") == "repository-local-only", "rendered plan network policy drifted")
    scenes = plan.get("scenes")
    require(isinstance(scenes, list) and len(scenes) == 9, "rendered plan must contain exactly nine scenes")

    actual_source = git_revision(source_root)
    require(actual_source == SOURCE_REVISION, f"frozen source mismatch: expected {SOURCE_REVISION}, got {actual_source}")
    require(git_clean(source_root), "frozen source worktree has tracked modifications")
    tooling_revision = git_revision(tooling_root)
    harness = render_root / str(plan["harness"])
    require(harness.is_file(), f"render root missing qualification harness: {harness}")
    require((render_root / "js/glaze-v1.6-development.mjs").is_file(), "render root missing frozen V1.6 aggregate")
    require((render_root / "css/glaze-v1.4.1.css").is_file(), "render root missing Stable CSS dependency")

    output.mkdir(parents=True, exist_ok=True)
    screenshots = output / "screenshots"
    scene_records = output / "scenes"

    http = driver = None
    session_id: str | None = None
    captured: list[dict[str, Any]] = []
    try:
        http = subprocess.Popen(
            [sys.executable, "-m", "http.server", str(WEB_PORT), "--bind", HOST, "--directory", str(render_root)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        wait_http(f"{SERVER}/{plan['harness']}")

        driver = subprocess.Popen(
            [chromedriver(), f"--port={DRIVER_PORT}", "--allowed-ips=127.0.0.1"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        wait_driver()
        session_id = create_session()
        browser = cdp(session_id, "Browser.getVersion")

        for scene in scenes:
            scene_id = str(scene["id"])
            width, height = [int(value) for value in scene["viewport"]]
            mobile = bool(scene.get("mobile", False))
            set_viewport(session_id, width, height, mobile)
            set_media(session_id, list(scene.get("mediaFeatures", [])))

            query = urlencode(
                {
                    "scene": scene_id,
                    "revision": SOURCE_REVISION,
                    "environment": str(scene["environment"]),
                    "mode": str(scene["mode"]),
                }
            )
            webdriver_request(
                "POST",
                f"/session/{session_id}/url",
                {"url": f"{SERVER}/{plan['harness']}?{query}"},
            )
            wait_ready(session_id)

            evidence = execute(session_id, "return window.__glazeV16RenderedEvidence;")
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
                require(authority.get(key) is False, f"authority boundary drift for {scene_id}: {key}")

            dimensions = execute(
                session_id,
                "return [innerWidth,innerHeight,document.documentElement.scrollWidth,document.documentElement.scrollHeight];",
            )
            require(isinstance(dimensions, list) and len(dimensions) == 4, f"invalid viewport dimensions: {scene_id}")
            require(abs(int(dimensions[0]) - width) <= 1, f"viewport width drift: {scene_id}: {dimensions}")
            require(abs(int(dimensions[1]) - height) <= 1, f"viewport height drift: {scene_id}: {dimensions}")
            require(int(dimensions[2]) <= width + 1, f"horizontal overflow: {scene_id}: {dimensions}")

            scene_records.mkdir(parents=True, exist_ok=True)
            scene_json = scene_records / f"{scene_id}.json"
            scene_json.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")

            freeze_after_measurement(session_id)
            image = screenshots / f"{scene_id}.png"
            screenshot(session_id, image)

            captured.append(
                {
                    "id": scene_id,
                    "laneIds": list(scene["laneIds"]),
                    "viewport": [width, height],
                    "mobile": mobile,
                    "environment": scene["environment"],
                    "mode": scene["mode"],
                    "mediaFeatures": list(scene.get("mediaFeatures", [])),
                    "evidence": str(scene_json.relative_to(output)),
                    "evidenceSha256": hashlib.sha256(scene_json.read_bytes()).hexdigest(),
                    "screenshot": str(image.relative_to(output)),
                    "screenshotSha256": hashlib.sha256(image.read_bytes()).hexdigest(),
                    "passed": True,
                }
            )

        manifest = {
            "schemaVersion": 1,
            "recordType": "glaze-v1.6-rendered-browser-capture",
            "lifecycle": "DevelopmentQualification",
            "sourceRevision": SOURCE_REVISION,
            "toolingRevision": tooling_revision,
            "acceptanceModelVersion": plan["acceptanceModelVersion"],
            "stableBaseline": "1.5.1",
            "observedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "browser": browser,
            "plan": str(plan_path.relative_to(tooling_root)),
            "planSha256": hashlib.sha256(plan_path.read_bytes()).hexdigest(),
            "harness": plan["harness"],
            "networkPolicy": plan["networkPolicy"],
            "renderedEvidenceLaneIds": list(plan["eligibleRenderedEvidenceLaneIds"]),
            "sceneCount": len(captured),
            "scenes": captured,
            "passed": all(scene["passed"] for scene in captured),
            "authority": {
                "renderedBrowserOnly": True,
                "humanEvidenceClaimed": False,
                "assistiveTechnologyEvidenceClaimed": False,
                "physicalDeviceEvidenceClaimed": False,
                "nativePlatformEvidenceClaimed": False,
                "representativePerformanceEvidenceClaimed": False,
                "regressionBaselineClaimed": False,
                "lifecyclePromotionAutomatic": False,
                "stableStatusGranted": False,
                "consumerAcceptanceAutomatic": False,
                "deploymentAcceptanceAutomatic": False,
                "productionAcceptanceAutomatic": False,
            },
        }
        manifest_path = output / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        require(manifest["passed"] is True, "rendered capture manifest did not pass")
        return manifest
    finally:
        if session_id:
            try:
                webdriver_request("DELETE", f"/session/{session_id}", timeout=5)
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
    parser.add_argument("--plan", default="contracts/v1.6/qualification.rendered.plan.json")
    parser.add_argument("--out", default="artifacts/v1.6-rendered")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tooling_root = Path(args.tooling_root).resolve()
    source_root = Path(args.source_root).resolve()
    render_root = Path(args.render_root).resolve()
    plan_path = (tooling_root / args.plan).resolve()
    output = (tooling_root / args.out).resolve()
    manifest = capture(render_root, source_root, tooling_root, plan_path, output)
    print(
        "GLAZE UI V1.6 rendered-browser capture: PASS "
        f"({manifest['sceneCount']} scenes, source {manifest['sourceRevision']})"
    )
    print(
        "Boundary: rendered Chromium-class evidence only; human, assistive-technology, physical-device, "
        "native-platform, representative-performance, regression-baseline, lifecycle, consumer, deployment, "
        "and production acceptance remain unclaimed."
    )


if __name__ == "__main__":
    try:
        main()
    except QualificationError as error:
        print(f"GLAZE UI V1.6 rendered-browser capture FAILED: {error}", file=sys.stderr)
        raise SystemExit(1)
