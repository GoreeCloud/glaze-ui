#!/usr/bin/env python3
"""Rendered web acceptance for the GLAZE UI V1.2 Frosted Neutral Candidate.

Runs the actual Candidate references in headless Chrome and validates the rendered
material hierarchy, five-region System Shell, 32-component gallery coverage,
accessibility fallbacks, target floors, neutral glass substrates, and responsive
reflow. Passing this gate is bounded rendered web evidence only; it does not
promote V1.2, certify native platforms, or make downstream consumers eligible.
"""

from __future__ import annotations

import base64
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
HOST = "127.0.0.1"
WEB_PORT = 8782
DRIVER_PORT = 9532
SERVER_BASE = f"http://{HOST}:{WEB_PORT}"
DRIVER_BASE = f"http://{HOST}:{DRIVER_PORT}"
ENTRYPOINT = "glaze-v1.2.0-candidate.css"
TAB_KEY = "\ue004"

REFERENCES = {
    "material": "reference/v1.2/frosted-neutral.html",
    "components": "reference/v1.2/component-gallery.html",
    "shell": "reference/v1.2/system-shell.html",
}


class RenderedAcceptanceError(RuntimeError):
    pass


def require(value: bool, message: str) -> None:
    if not value:
        raise RenderedAcceptanceError(message)


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
        raise RenderedAcceptanceError(f"WebDriver HTTP {error.code} for {path}: {detail}") from error
    except (URLError, TimeoutError) as error:
        raise RenderedAcceptanceError(f"WebDriver request failed for {path}: {error}") from error
    if not raw:
        return None
    value = json.loads(raw.decode("utf-8")).get("value")
    if isinstance(value, dict) and value.get("error"):
        raise RenderedAcceptanceError(f"WebDriver {value.get('error')}: {value.get('message', '')}")
    return value


def wait_http(url: str, seconds: float = 15) -> None:
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
    raise RenderedAcceptanceError(f"HTTP endpoint did not become ready: {url}: {last}")


def chromedriver() -> str:
    for candidate in (
        shutil.which("chromedriver"),
        "/usr/bin/chromedriver",
        "/usr/local/share/chromedriver-linux64/chromedriver",
    ):
        if candidate and Path(candidate).is_file():
            return str(candidate)
    raise RenderedAcceptanceError("chromedriver is unavailable on the runner")


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
    raise RenderedAcceptanceError(f"chromedriver did not become ready: {last}")


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
                            "--window-size=1440,1000",
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
    return request("POST", f"/session/{session_id}/execute/sync", {"script": script, "args": []})


def cdp(session_id: str, command: str, params: dict[str, Any] | None = None) -> Any:
    return request("POST", f"/session/{session_id}/goog/cdp/execute", {"cmd": command, "params": params or {}})


def set_viewport(session_id: str, width: int, height: int, mobile: bool = False) -> None:
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


def emulate_media(session_id: str, features: list[dict[str, str]]) -> None:
    cdp(session_id, "Emulation.setEmulatedMedia", {"media": "screen", "features": features})


def navigate(session_id: str, relative: str) -> None:
    request("POST", f"/session/{session_id}/url", {"url": f"{SERVER_BASE}/{relative}"})
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        if execute(session_id, "return document.readyState") == "complete":
            return
        time.sleep(0.1)
    raise RenderedAcceptanceError(f"Page did not finish loading: {relative}")


def screenshot(session_id: str, name: str) -> Path:
    encoded = request("GET", f"/session/{session_id}/screenshot")
    require(isinstance(encoded, str) and bool(encoded), f"Chrome did not return screenshot bytes for {name}")
    ARTIFACTS.mkdir(exist_ok=True)
    path = ARTIFACTS / f"glaze-v1.2-{name}.png"
    path.write_bytes(base64.b64decode(encoded))
    require(path.stat().st_size > 10_000, f"Screenshot appears empty or invalid: {path}")
    return path


def rgba(value: str) -> tuple[int, int, int, float]:
    match = re.fullmatch(
        r"rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})(?:\s*,\s*(0(?:\.\d+)?|1(?:\.0+)?))?\s*\)",
        value,
    )
    require(match is not None, f"Expected rendered rgb/rgba color, got {value!r}")
    assert match is not None
    return int(match.group(1)), int(match.group(2)), int(match.group(3)), float(match.group(4) or 1)


def require_neutral(value: str, label: str, tolerance: int = 6) -> None:
    r, g, b, _ = rgba(value)
    require(max(r, g, b) - min(r, g, b) <= tolerance, f"{label} is not neutral: {value}")


def page_state(session_id: str) -> dict[str, Any]:
    value = execute(
        session_id,
        r"""
        const root=document.documentElement;
        const rootStyle=getComputedStyle(root);
        const stylesheets=[...document.styleSheets].map(s=>s.href||'').filter(Boolean);
        return {
          ready:document.readyState,
          width:innerWidth,
          height:innerHeight,
          scrollWidth:document.documentElement.scrollWidth,
          scrollHeight:document.documentElement.scrollHeight,
          version:root.getAttribute('data-glaze-version'),
          upgrade:root.getAttribute('data-glaze-upgrade'),
          appearance:root.getAttribute('data-glz-appearance'),
          stylesheets,
          glassBase:rootStyle.getPropertyValue('--glz12-glass-base').trim(),
          glassRaised:rootStyle.getPropertyValue('--glz12-glass-raised').trim(),
          glassOverlay:rootStyle.getPropertyValue('--glz12-glass-overlay').trim(),
          glassPanel:rootStyle.getPropertyValue('--glz12-glass-panel').trim(),
        };
        """,
    )
    require(isinstance(value, dict), f"Could not read rendered page state: {value!r}")
    return value


def validate_candidate_page(state: dict[str, Any], width: int, label: str) -> None:
    require(state.get("ready") == "complete", f"{label}: document is not complete")
    require(abs(int(state.get("width", 0)) - width) <= 1, f"{label}: viewport width mismatch: {state}")
    require(int(state.get("scrollWidth", width + 2)) <= width + 1, f"{label}: root horizontal overflow: {state}")
    require(state.get("version") == "1.1", f"{label}: V1.1 Stable baseline activation is missing")
    require(state.get("upgrade") == "v1.2-frosted-neutral", f"{label}: V1.2 Frosted Neutral activation is missing")
    require(any(ENTRYPOINT in href for href in state.get("stylesheets", [])), f"{label}: V1.2 candidate entrypoint is not active")
    for key in ("glassBase", "glassRaised", "glassOverlay", "glassPanel"):
        value = state.get(key)
        require(isinstance(value, str) and bool(value), f"{label}: rendered material token {key} is empty")
        require_neutral(value, f"{label}.{key}")


def shell_state(session_id: str) -> dict[str, Any]:
    value = execute(
        session_id,
        r"""
        const q=s=>document.querySelector(s);
        const cs=e=>e?getComputedStyle(e):null;
        const filt=e=>{const s=cs(e);return s?(s.backdropFilter||s.webkitBackdropFilter||'none'):'missing'};
        const cc=q('[data-glz-shell-region="control-center"]');
        const nav=q('[data-glz-shell-region="navigation"]');
        const critical=q('[data-glz-shell-region="critical-system"]');
        const entry=q('[data-glz-shell-region="universal-search"] .glz1-search-entry');
        const panel=q('[data-glz-shell-region="universal-search"] .glz1-search-panel');
        const result=q('[data-glz-shell-region="universal-search"] .glz1-search-result');
        const tile=q('.glz12-control-tile[aria-pressed="false"]');
        const activeTile=q('.glz12-control-tile[aria-pressed="true"]');
        const controls=[...document.querySelectorAll('.glz12-shell-button,.glz12-control-tile,.glz12-control-range')]
          .filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0;})
          .map(e=>({name:(e.textContent||e.getAttribute('aria-label')||e.tagName).trim(),height:e.getBoundingClientRect().height,width:e.getBoundingClientRect().width}));
        const regions=[...document.querySelectorAll('[data-glz-shell-region]')].map(e=>e.getAttribute('data-glz-shell-region'));
        const ccStyle=cs(cc), tileStyle=cs(tile), activeStyle=cs(activeTile), criticalStyle=cs(critical);
        return {
          regions,
          ccFilter:filt(cc),navFilter:filt(nav),entryFilter:filt(entry),panelFilter:filt(panel),resultFilter:filt(result),
          tileFilter:filt(tile),activeTileFilter:filt(activeTile),criticalFilter:filt(critical),
          ccBackground:ccStyle&&ccStyle.backgroundColor,
          tileBackground:tileStyle&&tileStyle.backgroundColor,
          activeTileBackground:activeStyle&&activeStyle.backgroundColor,
          criticalBackground:criticalStyle&&criticalStyle.backgroundColor,
          ccShadow:ccStyle&&ccStyle.boxShadow,
          criticalShadow:criticalStyle&&criticalStyle.boxShadow,
          controls,
          controlGrid:q('.glz12-control-grid')?cs(q('.glz12-control-grid')).gridTemplateColumns:'',
          activeTag:document.activeElement&&document.activeElement.tagName,
          activeOutline:document.activeElement?cs(document.activeElement).outlineStyle:'none',
          activeOutlineWidth:document.activeElement?cs(document.activeElement).outlineWidth:'0px',
        };
        """,
    )
    require(isinstance(value, dict), f"Could not read System Shell state: {value!r}")
    return value


def validate_shell_normal(state: dict[str, Any], minimum_target: float = 47.5) -> None:
    regions = state.get("regions") or []
    require(len(regions) == 5 and len(set(regions)) == 5, f"System Shell must render five unique regions: {regions}")
    require(set(regions) == {"workspace", "navigation", "universal-search", "control-center", "critical-system"}, f"System Shell region set drifted: {regions}")
    require(state.get("ccFilter") not in {"none", "missing"}, f"Control Center must render parent Deep Glaze: {state}")
    require(state.get("navFilter") not in {"none", "missing"}, f"Floating navigation must render Glaze: {state}")
    require(state.get("entryFilter") not in {"none", "missing"}, f"Universal Search entry must render Glaze: {state}")
    require(state.get("panelFilter") not in {"none", "missing"}, f"Universal Search panel must render Deep Glaze: {state}")
    require(state.get("resultFilter") == "none", f"Search result row must not add nested backdrop blur: {state}")
    require(state.get("tileFilter") == "none" and state.get("activeTileFilter") == "none", f"Control Center tiles must not add nested backdrop blur: {state}")
    require(state.get("criticalFilter") == "none", f"Critical System must remain non-backdrop-dependent: {state}")
    require_neutral(str(state.get("ccBackground")), "Control Center substrate")
    require_neutral(str(state.get("tileBackground")), "Inactive Control Center tile")
    controls = state.get("controls") or []
    require(bool(controls), "System Shell has no rendered controls")
    too_small = [control for control in controls if float(control.get("height", 0)) < minimum_target]
    require(not too_small, f"System Shell control below target floor {minimum_target}: {too_small}")


def send_tab(session_id: str) -> None:
    request(
        "POST",
        f"/session/{session_id}/actions",
        {"actions": [{"type": "key", "id": "keyboard", "actions": [{"type": "keyDown", "value": TAB_KEY}, {"type": "keyUp", "value": TAB_KEY}]}]},
    )


def validate_keyboard_focus(session_id: str) -> None:
    execute(session_id, "document.activeElement && document.activeElement.blur(); return true;")
    send_tab(session_id)
    state = shell_state(session_id)
    require(state.get("activeTag") in {"BUTTON", "INPUT", "A"}, f"Tab did not reach an interactive shell control: {state}")
    require(state.get("activeOutline") != "none", f"Focused shell control has no visible outline: {state}")
    width = float(str(state.get("activeOutlineWidth") or "0").replace("px", ""))
    require(width >= 2.5, f"Focused shell control outline is below V1 focus floor: {state}")


def validate_touch_assistance(session_id: str) -> None:
    execute(session_id, "document.documentElement.setAttribute('data-glz-touch-assistance','true'); return true;")
    validate_shell_normal(shell_state(session_id), minimum_target=55.5)
    execute(session_id, "document.documentElement.removeAttribute('data-glz-touch-assistance'); return true;")


def validate_reduced_transparency(session_id: str) -> None:
    execute(session_id, "document.documentElement.setAttribute('data-glz-transparency','reduced'); return true;")
    state = shell_state(session_id)
    require(state.get("ccFilter") == "none", f"Reduced Transparency did not remove Control Center blur: {state}")
    require(state.get("navFilter") == "none", f"Reduced Transparency did not remove floating-navigation blur: {state}")
    require(state.get("criticalFilter") == "none", f"Critical System unexpectedly gained blur under Reduced Transparency: {state}")
    screenshot(session_id, "system-shell-reduced-transparency")
    execute(session_id, "document.documentElement.removeAttribute('data-glz-transparency'); return true;")


def validate_increased_contrast(session_id: str) -> None:
    execute(session_id, "document.documentElement.setAttribute('data-mode','increased-contrast'); return true;")
    value = execute(
        session_id,
        "return {cc:getComputedStyle(document.querySelector('.glz12-control-center')).borderTopWidth,tile:getComputedStyle(document.querySelector('.glz12-control-tile')).borderTopWidth};",
    )
    require(isinstance(value, dict), f"Could not read Increased Contrast state: {value!r}")
    for key in ("cc", "tile"):
        width = float(str(value.get(key) or "0").replace("px", ""))
        require(width >= 1.9, f"Increased Contrast did not strengthen {key} boundary: {value}")
    execute(session_id, "document.documentElement.removeAttribute('data-mode'); return true;")


def validate_200_text(session_id: str, width: int) -> None:
    execute(
        session_id,
        "document.documentElement.setAttribute('data-glz-text-scale','200');document.documentElement.style.fontSize='200%';return true;",
    )
    state = page_state(session_id)
    require(int(state.get("scrollWidth", width + 2)) <= width + 1, f"200% text creates root horizontal overflow: {state}")
    shell = shell_state(session_id)
    columns = str(shell.get("controlGrid") or "").split()
    require(len(columns) == 1, f"Control Center must reflow to one column at 200% text: {shell.get('controlGrid')}")
    execute(session_id, "document.documentElement.removeAttribute('data-glz-text-scale');document.documentElement.style.fontSize='';return true;")


def validate_forced_colors(session_id: str) -> None:
    emulate_media(session_id, [{"name": "forced-colors", "value": "active"}])
    state = shell_state(session_id)
    require(state.get("ccFilter") == "none" and state.get("navFilter") == "none", f"Forced Colors did not remove shell backdrop effects: {state}")
    require(state.get("ccShadow") == "none", f"Forced Colors did not remove custom Control Center shadow: {state}")
    screenshot(session_id, "system-shell-forced-colors")
    emulate_media(session_id, [])


def validate_component_gallery(session_id: str) -> None:
    value = execute(
        session_id,
        r"""
        const samples=[...document.querySelectorAll('[data-component]')];
        const names=samples.map(e=>e.getAttribute('data-component'));
        const frosted=[...document.querySelectorAll('.glz1-dock,.glz1-popover,.glz1-menu,.glz1-sheet,.glz1-toast,.glz1-capsule,.glz1-smart-rail,.glz1-search-entry,.glz1-search-panel')]
          .filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0;})
          .map(e=>getComputedStyle(e).backdropFilter||getComputedStyle(e).webkitBackdropFilter||'none');
        const dialog=document.querySelector('.glz1-dialog');
        return {count:samples.length,unique:new Set(names).size,frosted,dialogFilter:dialog?(getComputedStyle(dialog).backdropFilter||getComputedStyle(dialog).webkitBackdropFilter||'none'):'missing'};
        """,
    )
    require(isinstance(value, dict), f"Could not read component gallery: {value!r}")
    require(value.get("count") == 32 and value.get("unique") == 32, f"Component gallery must render exactly 32 unique samples: {value}")
    filters = value.get("frosted") or []
    require(filters and any(item not in {"none", "missing"} for item in filters), f"Component gallery renders no Frosted Neutral components: {value}")
    require(value.get("dialogFilter") == "none", f"Dialog must remain non-backdrop-dependent in component gallery: {value}")


def main() -> int:
    http_process: subprocess.Popen[str] | None = None
    driver_process: subprocess.Popen[str] | None = None
    session_id: str | None = None
    try:
        ARTIFACTS.mkdir(exist_ok=True)
        http_process = subprocess.Popen(
            [sys.executable, "-m", "http.server", str(WEB_PORT), "--bind", HOST, "--directory", str(ROOT)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        wait_http(f"{SERVER_BASE}/{REFERENCES['shell']}")
        driver_process = subprocess.Popen(
            [chromedriver(), f"--port={DRIVER_PORT}", "--allowed-ips=127.0.0.1"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        wait_driver()
        session_id = create_session()

        set_viewport(session_id, 1440, 1000)
        emulate_media(session_id, [])
        navigate(session_id, REFERENCES["material"])
        validate_candidate_page(page_state(session_id), 1440, "material-reference")
        screenshot(session_id, "material-light")

        navigate(session_id, REFERENCES["components"])
        validate_candidate_page(page_state(session_id), 1440, "component-gallery")
        validate_component_gallery(session_id)
        screenshot(session_id, "component-gallery-light")

        navigate(session_id, REFERENCES["shell"])
        validate_candidate_page(page_state(session_id), 1440, "system-shell")
        validate_shell_normal(shell_state(session_id))
        validate_keyboard_focus(session_id)
        validate_touch_assistance(session_id)
        screenshot(session_id, "system-shell-light")

        execute(session_id, "document.documentElement.setAttribute('data-glz-appearance','dark');return true;")
        dark = page_state(session_id)
        require(dark.get("appearance") == "dark", "Dark appearance did not activate")
        for key in ("glassBase", "glassRaised", "glassOverlay", "glassPanel"):
            require_neutral(str(dark.get(key)), f"dark.{key}")
        validate_shell_normal(shell_state(session_id))
        screenshot(session_id, "system-shell-dark")

        execute(session_id, "document.documentElement.setAttribute('data-glz-appearance','deep-dark');return true;")
        deep = page_state(session_id)
        require(deep.get("appearance") == "deep-dark", "Deep Dark appearance did not activate")
        for key in ("glassBase", "glassRaised", "glassOverlay", "glassPanel"):
            require_neutral(str(deep.get(key)), f"deep-dark.{key}")
        validate_shell_normal(shell_state(session_id))
        screenshot(session_id, "system-shell-deep-dark")

        execute(session_id, "document.documentElement.setAttribute('data-glz-appearance','light');return true;")
        validate_reduced_transparency(session_id)
        validate_increased_contrast(session_id)
        validate_200_text(session_id, 1440)
        validate_forced_colors(session_id)

        set_viewport(session_id, 390, 844, mobile=True)
        navigate(session_id, REFERENCES["shell"])
        validate_candidate_page(page_state(session_id), 390, "system-shell-mobile")
        validate_shell_normal(shell_state(session_id))
        validate_200_text(session_id, 390)
        screenshot(session_id, "system-shell-mobile")

        print("GLAZE UI V1.2 Frosted Neutral rendered web Candidate acceptance: PASS")
        print("Evidence: material, 32-component gallery, System Shell Light/Dark/Deep Dark, Reduced Transparency, Forced Colors, and mobile screenshots written to artifacts/.")
        print("Coverage: neutral glass substrates, exact five-region shell, 32 components, no nested blur, 48/56px targets, keyboard focus, Increased Contrast, 200% text reflow, responsive rendering, and critical-system separation.")
        print("Boundary: bounded rendered web Candidate evidence only; V1.1 remains Stable and native/human-optical/downstream-production acceptance remains separate.")
        return 0
    except Exception as error:
        print(f"GLAZE UI V1.2 Frosted Neutral rendered Candidate acceptance FAILED: {error}")
        return 1
    finally:
        if session_id:
            try:
                request("DELETE", f"/session/{session_id}")
            except Exception:
                pass
        for process in (driver_process, http_process):
            if process and process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()


if __name__ == "__main__":
    sys.exit(main())
