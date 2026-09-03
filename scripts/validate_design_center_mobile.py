#!/usr/bin/env python3
"""Rendered mobile acceptance for the public GLAZE UI Design Center.

This gate uses a real Chromium-class browser through ChromeDriver, exercises
mobile device metrics and touch input, validates the exact built revision at
representative narrow portrait widths, and captures reviewable light/dark
screenshots as CI artifacts.
"""

from __future__ import annotations

import base64
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "website" / "dist"
ARTIFACTS = ROOT / "artifacts"
HOST = "127.0.0.1"
WEB_PORT = 8778
DRIVER_PORT = 9528
TARGET = f"http://{HOST}:{WEB_PORT}/"
DRIVER_BASE = f"http://{HOST}:{DRIVER_PORT}"
VIEWPORTS = ((320, 844), (345, 844), (390, 844), (412, 915))


class MobileAcceptanceError(RuntimeError):
    pass


def require(value: bool, message: str) -> None:
    if not value:
        raise MobileAcceptanceError(message)


def request(method: str, path: str, payload: dict[str, Any] | None = None, timeout: int = 30) -> Any:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    req = Request(
        f"{DRIVER_BASE}{path}",
        data=body,
        method=method,
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urlopen(req, timeout=timeout) as response:
            raw = response.read()
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise MobileAcceptanceError(f"WebDriver HTTP {error.code} for {path}: {detail}") from error
    except (URLError, TimeoutError) as error:
        raise MobileAcceptanceError(f"WebDriver request failed for {path}: {error}") from error
    if not raw:
        return None
    value = json.loads(raw.decode("utf-8")).get("value")
    if isinstance(value, dict) and value.get("error"):
        raise MobileAcceptanceError(f"WebDriver {value.get('error')}: {value.get('message', '')}")
    return value


def wait_url(url: str, seconds: float = 15) -> None:
    deadline = time.monotonic() + seconds
    last: Exception | None = None
    while time.monotonic() < deadline:
        try:
            with urlopen(url, timeout=1) as response:
                if response.status == 200:
                    return
        except Exception as error:
            last = error
        time.sleep(0.15)
    raise MobileAcceptanceError(f"Design Center server did not become ready: {last}")


def chromedriver() -> str:
    for candidate in (
        shutil.which("chromedriver"),
        "/usr/bin/chromedriver",
        "/usr/local/share/chromedriver-linux64/chromedriver",
    ):
        if candidate and Path(candidate).is_file():
            return str(candidate)
    raise MobileAcceptanceError("chromedriver is unavailable on the runner")


def wait_driver() -> None:
    deadline = time.monotonic() + 15
    last: Exception | None = None
    while time.monotonic() < deadline:
        try:
            state = request("GET", "/status")
            if isinstance(state, dict) and state.get("ready"):
                return
        except Exception as error:
            last = error
        time.sleep(0.2)
    raise MobileAcceptanceError(f"chromedriver did not become ready: {last}")


def create_session() -> str:
    value = request(
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
                            "--window-size=1180,900",
                        ]
                    },
                }
            }
        },
    )
    require(isinstance(value, dict), f"Unexpected Chrome session response: {value!r}")
    session_id = value.get("sessionId")
    require(isinstance(session_id, str) and bool(session_id), "Chrome did not return a session id")
    return session_id


def execute(session_id: str, script: str) -> Any:
    return request(
        "POST",
        f"/session/{session_id}/execute/sync",
        {"script": script, "args": []},
    )


def cdp(session_id: str, command: str, params: dict[str, Any] | None = None) -> Any:
    return request(
        "POST",
        f"/session/{session_id}/goog/cdp/execute",
        {"cmd": command, "params": params or {}},
    )


def set_mobile_viewport(session_id: str, width: int, height: int) -> None:
    cdp(
        session_id,
        "Emulation.setDeviceMetricsOverride",
        {
            "width": width,
            "height": height,
            "deviceScaleFactor": 2,
            "mobile": True,
            "screenWidth": width,
            "screenHeight": height,
        },
    )
    cdp(session_id, "Emulation.setTouchEmulationEnabled", {"enabled": True, "maxTouchPoints": 5})
    execute(session_id, "window.scrollTo(0,0); return {width:innerWidth,height:innerHeight};")


def row_capacity(rects: list[dict[str, float]]) -> int:
    if not rects:
        return 0
    return max(
        sum(1 for candidate in rects if abs(float(candidate["top"]) - float(rect["top"])) <= 2)
        for rect in rects
    )


def read_state(session_id: str) -> dict[str, Any]:
    value = execute(
        session_id,
        """
        const q=s=>document.querySelector(s);
        const rects=s=>[...document.querySelectorAll(s)]
          .map(el=>el.getBoundingClientRect())
          .filter(r=>r.width>0&&r.height>0)
          .map(r=>({left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height}));
        const header=q('.site-header').getBoundingClientRect();
        const hero=q('.hero').getBoundingClientRect();
        const h1=q('.hero h1');
        const heroButton=q('.hero .glaze-button');
        const heroButtonStyle=getComputedStyle(heroButton);
        const navRects=rects('.nav-wrap nav a');
        const themeRects=rects('.theme-group button');
        const heroButtons=rects('.hero .glaze-button');
        const surfaces=rects('.surface-card');
        const demos=rects('.demo-grid > *');
        const shortBrand=getComputedStyle(q('.brand-label-short')).display;
        const longBrand=getComputedStyle(q('.brand-label-long')).display;
        return {
          ready:document.readyState,
          width:innerWidth,
          height:innerHeight,
          scrollWidth:document.documentElement.scrollWidth,
          headerPosition:getComputedStyle(q('.site-header')).position,
          headerHeight:header.height,
          heroHeight:hero.height,
          h1Font:parseFloat(getComputedStyle(h1).fontSize),
          navRects,
          themeRects,
          heroButtons,
          surfaces,
          demos,
          buttonDisplay:heroButtonStyle.display,
          buttonAlign:heroButtonStyle.alignItems,
          buttonJustify:heroButtonStyle.justifyContent,
          shortBrand,
          longBrand,
        };
        """,
    )
    require(isinstance(value, dict), f"Could not read rendered Design Center state: {value!r}")
    return value


def validate_state(state: dict[str, Any], requested_width: int) -> None:
    width = int(state.get("width", 0))
    require(abs(width - requested_width) <= 1, f"CSS viewport is {width}px; expected {requested_width}px: {state}")
    require(state.get("ready") == "complete", f"Design Center did not finish loading at {width}px")
    require(int(state.get("scrollWidth", width + 10)) <= width + 1, f"Horizontal overflow at {width}px: {state}")
    require(state.get("headerPosition") not in {"fixed", "sticky"}, f"Header overlays mobile content at {width}px: {state}")
    require(float(state.get("headerHeight", 999)) <= 145, f"Mobile header is disproportionately tall at {width}px: {state}")
    require(float(state.get("heroHeight", 9999)) <= 650, f"Mobile hero is viewport-inflated at {width}px: {state}")
    require(34 <= float(state.get("h1Font", 0)) <= 46, f"Mobile hero type is outside the intended readable scale at {width}px: {state}")
    require(state.get("shortBrand") != "none" and state.get("longBrand") == "none", f"Compact mobile brand is not active at {width}px: {state}")

    nav_rects = state.get("navRects") or []
    require(len(nav_rects) == 4, f"Expected four primary mobile section links at {width}px: {state}")
    require(row_capacity(nav_rects) == 4, f"Primary mobile navigation is not one compact row at {width}px: {state}")
    require(min(float(rect["height"]) for rect in nav_rects) >= 47.5, f"Primary navigation target below 48px at {width}px: {state}")
    require(min(float(rect["left"]) for rect in nav_rects) >= -1, f"Primary navigation escapes left viewport edge at {width}px: {state}")
    require(max(float(rect["right"]) for rect in nav_rects) <= width + 1, f"Primary navigation escapes right viewport edge at {width}px: {state}")

    theme_rects = state.get("themeRects") or []
    require(len(theme_rects) == 3, f"Appearance controls missing at {width}px: {state}")
    require(min(float(rect["height"]) for rect in theme_rects) >= 47.5, f"Appearance target below 48px at {width}px: {state}")

    hero_buttons = state.get("heroButtons") or []
    require(len(hero_buttons) == 2, f"Hero actions missing at {width}px: {state}")
    require(min(float(rect["height"]) for rect in hero_buttons) >= 47.5, f"Hero action below 48px at {width}px: {state}")
    require(max(float(rect["height"]) for rect in hero_buttons) <= 64, f"Hero action became an oversized block at {width}px: {state}")
    require(state.get("buttonDisplay") in {"flex", "inline-flex"}, f"Hero button is not flex-centered at {width}px: {state}")
    require(state.get("buttonAlign") == "center" and state.get("buttonJustify") == "center", f"Hero button label is not centered at {width}px: {state}")

    surfaces = state.get("surfaces") or []
    require(len(surfaces) == 5, f"System Shell surfaces missing at {width}px: {state}")
    require(max(float(rect["height"]) for rect in surfaces) <= 96, f"System Shell cards regained excessive mobile dead space at {width}px: {state}")
    require(row_capacity(surfaces) == 1, f"System Shell does not recompose to one readable mobile column at {width}px: {state}")

    demos = state.get("demos") or []
    require(bool(demos), f"Component/adaptation cards did not render at {width}px: {state}")
    require(row_capacity(demos) == 1, f"Content cards are compressed into multiple phone columns at {width}px: {state}")


def choose_theme(session_id: str, choice: str) -> None:
    result = execute(
        session_id,
        f"""
        const button=[...document.querySelectorAll('[data-theme-choice]')]
          .find(el=>el.dataset.themeChoice==={json.dumps(choice)});
        if(!button) return null;
        button.click();
        return {{pressed:button.getAttribute('aria-pressed'),theme:document.documentElement.dataset.theme||''}};
        """,
    )
    require(isinstance(result, dict) and result.get("pressed") == "true", f"Could not activate {choice} appearance: {result!r}")


def capture_full_page(session_id: str, output: Path) -> None:
    metrics = cdp(session_id, "Page.getLayoutMetrics")
    require(isinstance(metrics, dict), f"Could not read page layout metrics: {metrics!r}")
    size = metrics.get("cssContentSize") or metrics.get("contentSize")
    require(isinstance(size, dict), f"Could not resolve page content size: {metrics!r}")
    width = float(size.get("width", 0))
    height = float(size.get("height", 0))
    require(width > 0 and height > 0, f"Invalid screenshot content size: {size!r}")
    value = cdp(
        session_id,
        "Page.captureScreenshot",
        {
            "format": "png",
            "fromSurface": True,
            "captureBeyondViewport": True,
            "clip": {"x": 0, "y": 0, "width": width, "height": height, "scale": 1},
        },
    )
    require(isinstance(value, dict) and isinstance(value.get("data"), str), "Chrome did not return screenshot data")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(base64.b64decode(value["data"]))


def exercise(session_id: str) -> None:
    request("POST", f"/session/{session_id}/timeouts", {"implicit": 0, "pageLoad": 15000, "script": 10000})
    request("POST", f"/session/{session_id}/url", {"url": TARGET})

    for width, height in VIEWPORTS:
        set_mobile_viewport(session_id, width, height)
        validate_state(read_state(session_id), width)

    set_mobile_viewport(session_id, 390, 844)
    for choice in ("light", "dark", "system"):
        choose_theme(session_id, choice)
        validate_state(read_state(session_id), 390)
        if choice in {"light", "dark"}:
            capture_full_page(session_id, ARTIFACTS / f"design-center-mobile-390-{choice}.png")

    set_mobile_viewport(session_id, 320, 844)
    choose_theme(session_id, "light")
    validate_state(read_state(session_id), 320)
    capture_full_page(session_id, ARTIFACTS / "design-center-mobile-320-light.png")


def main() -> int:
    server: subprocess.Popen[bytes] | None = None
    driver: subprocess.Popen[bytes] | None = None
    session_id: str | None = None
    log_path: str | None = None
    try:
        subprocess.run([sys.executable, str(ROOT / "website" / "build.py")], cwd=ROOT, check=True)
        require((DIST / "index.html").is_file(), "Design Center build did not produce index.html")
        ARTIFACTS.mkdir(parents=True, exist_ok=True)

        server = subprocess.Popen(
            [sys.executable, "-m", "http.server", str(WEB_PORT), "--bind", HOST, "--directory", str(DIST)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        wait_url(TARGET)

        with tempfile.NamedTemporaryFile(prefix="glaze-design-center-chrome-", suffix=".log", delete=False) as log_file:
            log_path = log_file.name
            driver = subprocess.Popen(
                [chromedriver(), f"--port={DRIVER_PORT}", "--allowed-ips=127.0.0.1"],
                stdout=log_file,
                stderr=subprocess.STDOUT,
            )
        wait_driver()
        session_id = create_session()
        exercise(session_id)
        print(
            "Design Center rendered mobile acceptance passed at 320/345/390/412px with mobile/touch metrics, "
            "48px controls, compact navigation and hero geometry, one-column content recomposition, no horizontal "
            "overflow, and reviewable light/dark screenshots."
        )
        return 0
    except Exception as error:
        print(f"Design Center rendered mobile acceptance failed: {error}")
        if log_path:
            try:
                text = Path(log_path).read_text(encoding="utf-8", errors="replace")
            except OSError:
                text = ""
            if text:
                print(text[-8000:])
        return 1
    finally:
        if session_id:
            try:
                request("DELETE", f"/session/{session_id}")
            except Exception:
                pass
        for process in (driver, server):
            if process:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)
        if log_path:
            try:
                Path(log_path).unlink()
            except OSError:
                pass


if __name__ == "__main__":
    raise SystemExit(main())
