#!/usr/bin/env python3
"""Bounded rendered-web acceptance for GLAZE UI V1.2 Motion and Connected Transformation Candidate."""
from __future__ import annotations

import base64
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
HOST = "127.0.0.1"
WEB_PORT = 8792
DRIVER_PORT = 9542
SERVER = f"http://{HOST}:{WEB_PORT}"
DRIVER = f"http://{HOST}:{DRIVER_PORT}"
REFERENCE = "reference/v1.2/motion.html"
CONTRACT = ROOT / "contracts/v1.2/motion.candidate.json"
TOKENS = ROOT / "tokens/glaze-v1.2-motion.candidate.json"
CSS = ROOT / "css/glaze-v1.2-motion.candidate.css"
ENTRYPOINT = ROOT / "css/glaze-v1.2.0-candidate.css"
WORKFLOW = ROOT / ".github/workflows/glaze-v1.2-motion.yml"
EXPERIMENT_DOC = ROOT / "GLAZE_MOTION.md"
EXPERIMENT_TOKENS = ROOT / "tokens/glaze-motion.json"
DURATIONS = {"instant": 80, "fast": 160, "standard": 240, "deliberate": 360, "spatial": 480}
RANGES = {"instant": (50, 100), "fast": (100, 180), "standard": (180, 280), "deliberate": (280, 420), "spatial": (400, 600)}
EASING = {
    "responsive": "cubic-bezier(0.2, 0, 0, 1)",
    "glide": "cubic-bezier(0.16, 1, 0.3, 1)",
    "settle": "cubic-bezier(0, 0, 0, 1)",
    "direct": "linear",
}


class AcceptanceError(RuntimeError):
    pass


def require(ok: bool, message: str) -> None:
    if not ok:
        raise AcceptanceError(message)


def validate_source() -> None:
    for path in (CONTRACT, TOKENS, CSS, ENTRYPOINT, WORKFLOW, ROOT / REFERENCE, EXPERIMENT_DOC, EXPERIMENT_TOKENS):
        require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    tokens = json.loads(TOKENS.read_text(encoding="utf-8"))
    experiment = json.loads(EXPERIMENT_TOKENS.read_text(encoding="utf-8"))
    experiment_doc = EXPERIMENT_DOC.read_text(encoding="utf-8")
    require(contract.get("version") == "1.2.0-candidate", "motion contract version drifted")
    require(contract.get("lifecycle") == "candidate" and contract.get("consumerEligible") is False, "motion Candidate boundary drifted")
    require(contract.get("stableBaseline") == "1.1.0", "motion Stable baseline drifted")
    require(contract.get("status") == "bounded-web-reference-implementation", "motion bounded status drifted")
    principles = contract.get("principles", {})
    for key in (
        "respondImmediately", "moveWithPurpose", "preserveContinuity", "settleQuietly", "userControlFirst",
        "stateIndependentOfAnimationCompletion", "focusMustNotWaitForMotion", "connectedIdentityPreferredWhenRelationshipClear",
        "directManipulationTracksInput", "userDrivenMotionInterruptible", "reducedMotionPreservesSemanticState",
        "reducedMotionPreservesDirectManipulationTracking",
    ):
        require(principles.get(key) is True, f"motion principle missing: {key}")
    for key in ("decorativeContinuousMotionAllowed", "routineLinearUiMotionAllowed", "excessiveBounceAllowed"):
        require(principles.get(key) is False, f"motion prohibition drifted: {key}")
    families = contract.get("durationFamilies", {})
    token_durations = tokens.get("durationsMs", {})
    for name, target in DURATIONS.items():
        item = families.get(name, {})
        low, high = RANGES[name]
        require(item.get("rangeMs") == [low, high], f"{name} proposal range drifted")
        require(item.get("candidateMs") == target and low <= target <= high, f"{name} Candidate duration drifted")
        require(token_durations.get(name) == target, f"{name} token duration drifted")
    require(families["spatial"].get("defaultAllowed") is False, "Spatial duration may not become default")
    require(contract.get("easingFamilies") == EASING, "motion easing contract drifted")
    require(tokens.get("easing") == EASING, "motion easing tokens drifted")
    profiles = tokens.get("profiles", {})
    require(profiles.get("full", {}).get("durationsMs") == DURATIONS, "full motion profile drifted")
    require(profiles.get("reduced", {}).get("durationsMs") == {
        "instant": 60, "fast": 120, "standard": 180, "deliberate": 270, "spatial": 360
    }, "reduced motion performance profile drifted")
    require(all(value == 0 for value in profiles.get("minimal", {}).get("durationsMs", {}).values()), "minimal profile must remove optional transition duration")
    experimental = contract.get("experimentalSubsystemRelationship", {})
    require(experimental.get("requiredStatus") == "experimental" and experimental.get("wholesalePromotion") is False, "Experimental Glaze Motion boundary drifted")
    require(experimental.get("runtimeDependencyIntroduced") is False, "V1.2 motion slice may not depend on Experimental runtime")
    require(experiment.get("glazeMotion", {}).get("status") == "experimental", "Glaze Motion token status was promoted")
    require("Experimental foundation" in experiment_doc and "remains **Experimental**" in experiment_doc, "Glaze Motion documentation no longer preserves Experimental boundary")
    bindings = contract.get("representativeBindings", {})
    require(bindings.get("search", {}).get("sameObjectContinuity") is True and bindings["search"].get("focusPreserved") is True, "Search continuity contract drifted")
    require(bindings.get("morphCard", {}).get("sameObjectContinuity") is True, "MorphCard continuity contract drifted")
    require(bindings.get("directManipulation", {}).get("tracksInputImmediately") is True, "direct manipulation contract drifted")
    impl = contract.get("implementation", {})
    expected_impl = {
        "tokens": "tokens/glaze-v1.2-motion.candidate.json",
        "webLayer": "css/glaze-v1.2-motion.candidate.css",
        "webEntrypoint": "css/glaze-v1.2.0-candidate.css",
        "reference": REFERENCE,
        "renderedValidator": "scripts/validate_glaze_v1_2_motion_rendered.py",
        "workflow": ".github/workflows/glaze-v1.2-motion.yml",
    }
    for key, value in expected_impl.items():
        require(impl.get(key) == value, f"motion implementation binding drifted: {key}")
    css = CSS.read_text(encoding="utf-8")
    for marker in (
        "--glz12-motion-instant: 80ms", "--glz12-motion-fast: 160ms", "--glz12-motion-standard: 240ms",
        "--glz12-motion-deliberate: 360ms", "--glz12-motion-spatial: 480ms", '[data-glz-connected="search"]',
        '[data-glz-connected="card-detail"]', '[data-glz-direct-manipulation="true"]', "prefers-reduced-motion: reduce", "forced-colors: active",
    ):
        require(marker in css, f"motion CSS marker missing: {marker}")
    lowered = css.lower()
    require("@keyframes" not in lowered, "bounded motion layer may not introduce autonomous keyframe loops")
    require("infinite" not in lowered, "bounded motion layer may not introduce infinite motion")
    require("will-change: auto" in lowered and "will-change:" not in lowered.replace("will-change: auto", ""), "bounded motion layer may not persistently reserve compositor layers")
    entry = ENTRYPOINT.read_text(encoding="utf-8")
    chain = [
        '@import url("./glaze-v1.2-depth-fallbacks.candidate.css")',
        '@import url("./glaze-v1.2-motion.candidate.css")',
        '@import url("./glaze-v1.2-accessibility.candidate.css")',
    ]
    require(all(item in entry for item in chain), "Candidate entrypoint missing motion import chain")
    require([entry.index(item) for item in chain] == sorted(entry.index(item) for item in chain), "motion/accessibility import order drifted")
    workflow = WORKFLOW.read_text(encoding="utf-8")
    require("validate_glaze_v1_2_motion_rendered.py" in workflow, "motion workflow does not invoke rendered validator")
    require("github.event.pull_request.head.sha || github.sha" in workflow, "motion workflow is not exact-head pinned")


def request(method: str, path: str, payload: dict[str, Any] | None = None, timeout: int = 30) -> Any:
    req = Request(f"{DRIVER}{path}", data=None if payload is None else json.dumps(payload).encode(), method=method, headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urlopen(req, timeout=timeout) as response:
            raw = response.read()
    except HTTPError as error:
        raise AcceptanceError(f"WebDriver HTTP {error.code}: {error.read().decode(errors='replace')}") from error
    except (URLError, TimeoutError) as error:
        raise AcceptanceError(f"WebDriver request failed: {error}") from error
    if not raw:
        return None
    value = json.loads(raw.decode()).get("value")
    if isinstance(value, dict) and value.get("error"):
        raise AcceptanceError(f"WebDriver {value.get('error')}: {value.get('message', '')}")
    return value


def wait_http(url: str, seconds: float = 15) -> None:
    end = time.monotonic() + seconds
    last: Exception | None = None
    while time.monotonic() < end:
        try:
            with urlopen(url, timeout=1) as response:
                if response.status == 200:
                    return
        except Exception as error:
            last = error
        time.sleep(.15)
    raise AcceptanceError(f"HTTP endpoint not ready: {last}")


def chromedriver() -> str:
    for item in (shutil.which("chromedriver"), "/usr/bin/chromedriver", "/usr/local/share/chromedriver-linux64/chromedriver"):
        if item and Path(item).is_file():
            return str(item)
    raise AcceptanceError("chromedriver unavailable")


def wait_driver() -> None:
    end = time.monotonic() + 15
    last: Exception | None = None
    while time.monotonic() < end:
        try:
            status = request("GET", "/status")
            if isinstance(status, dict) and status.get("ready"):
                return
        except Exception as error:
            last = error
        time.sleep(.2)
    raise AcceptanceError(f"chromedriver not ready: {last}")


def session() -> str:
    value = request("POST", "/session", {"capabilities": {"alwaysMatch": {"browserName": "chrome", "goog:chromeOptions": {"args": ["--headless=new", "--no-sandbox", "--disable-dev-shm-usage", "--disable-background-networking", "--disable-component-update", "--disable-extensions", "--disable-sync", "--metrics-recording-only", "--no-first-run", "--window-size=1280,1100"]}}}}, timeout=60)
    require(isinstance(value, dict) and isinstance(value.get("sessionId"), str), "Chrome returned no session id")
    return value["sessionId"]


def execute(sid: str, script: str) -> Any:
    return request("POST", f"/session/{sid}/execute/sync", {"script": script, "args": []})


def cdp(sid: str, cmd: str, params: dict[str, Any] | None = None) -> Any:
    return request("POST", f"/session/{sid}/goog/cdp/execute", {"cmd": cmd, "params": params or {}})


def viewport(sid: str, width: int, height: int) -> None:
    cdp(sid, "Emulation.setDeviceMetricsOverride", {"width": width, "height": height, "deviceScaleFactor": 1, "mobile": False, "screenWidth": width, "screenHeight": height})


def media(sid: str, features: list[dict[str, str]]) -> None:
    cdp(sid, "Emulation.setEmulatedMedia", {"media": "screen", "features": features})


def navigate(sid: str) -> None:
    request("POST", f"/session/{sid}/url", {"url": f"{SERVER}/{REFERENCE}"})
    end = time.monotonic() + 15
    while time.monotonic() < end:
        if execute(sid, "return document.readyState") == "complete" and execute(sid, "return document.documentElement.dataset.motionReferenceReady === 'true'"):
            return
        time.sleep(.1)
    raise AcceptanceError("motion reference did not finish loading")


def screenshot(sid: str, name: str) -> None:
    encoded = request("GET", f"/session/{sid}/screenshot")
    require(isinstance(encoded, str) and encoded, "no screenshot bytes")
    ARTIFACTS.mkdir(exist_ok=True)
    path = ARTIFACTS / f"glaze-v1.2-motion-{name}.png"
    path.write_bytes(base64.b64decode(encoded))
    require(path.stat().st_size > 7000, f"invalid screenshot {path}")


STATE_JS = r"""
const ms = value => {
  const parts = String(value || '').split(',').map(x => x.trim()).filter(Boolean);
  const values = parts.map(x => x.endsWith('ms') ? parseFloat(x) : (x.endsWith('s') ? parseFloat(x) * 1000 : 0));
  return values.length ? Math.max(...values) : 0;
};
const style = id => getComputedStyle(document.getElementById(id));
const root = getComputedStyle(document.documentElement);
const tx = id => { const t = style(id).transform; if (!t || t === 'none') return 0; return new DOMMatrix(t).m41; };
const ids = ['press-control','selection-indicator','motion-popover','motion-dialog','motion-sheet','search-panel','motion-search','motion-card','direct-object'];
const animations = {}; for (const id of ids) animations[id] = style(id).animationName;
const targets = [...document.querySelectorAll('.glz12-spatial-action')].map(el => { const r = el.getBoundingClientRect(); return {id:el.id,w:r.width,h:r.height}; });
return {
  ready: document.readyState, width: innerWidth, scrollWidth: document.documentElement.scrollWidth,
  appearance: document.documentElement.dataset.glzAppearance, performance: document.documentElement.dataset.glzMaterialPerformance,
  mode: document.documentElement.dataset.mode || '',
  canonical: {
    instant: ms(root.getPropertyValue('--glz12-motion-instant')), fast: ms(root.getPropertyValue('--glz12-motion-fast')),
    standard: ms(root.getPropertyValue('--glz12-motion-standard')), deliberate: ms(root.getPropertyValue('--glz12-motion-deliberate')),
    spatial: ms(root.getPropertyValue('--glz12-motion-spatial'))
  },
  effective: {
    instant: ms(root.getPropertyValue('--glz12-motion-instant-effective')), fast: ms(root.getPropertyValue('--glz12-motion-fast-effective')),
    standard: ms(root.getPropertyValue('--glz12-motion-standard-effective')), deliberate: ms(root.getPropertyValue('--glz12-motion-deliberate-effective')),
    spatial: ms(root.getPropertyValue('--glz12-motion-spatial-effective'))
  },
  transitionMs: {
    press: ms(style('press-control').transitionDuration), selection: ms(style('selection-indicator').transitionDuration),
    popover: ms(style('motion-popover').transitionDuration), dialog: ms(style('motion-dialog').transitionDuration),
    sheet: ms(style('motion-sheet').transitionDuration), searchPanel: ms(style('search-panel').transitionDuration),
    searchEntry: ms(getComputedStyle(document.querySelector('#motion-search .glz1-search-entry')).transitionDuration),
    morph: ms(style('motion-card').transitionDuration), direct: ms(style('direct-object').transitionDuration)
  },
  transforms: {
    selectionX: tx('selection-indicator'), popover: style('motion-popover').transform, dialog: style('motion-dialog').transform,
    sheet: style('motion-sheet').transform, searchPanel: style('search-panel').transform, directX: tx('direct-object')
  },
  states: {
    popover: document.getElementById('motion-popover').dataset.open, dialog: document.getElementById('motion-dialog').dataset.open,
    sheet: document.getElementById('motion-sheet').dataset.open, search: document.getElementById('motion-search').dataset.open,
    morph: document.getElementById('motion-card').getAttribute('aria-expanded'),
    selected: [...document.querySelectorAll('#selection-track [role="tab"]')].findIndex(x => x.getAttribute('aria-selected') === 'true'),
    activeId: document.activeElement && document.activeElement.id, query: document.getElementById('search-query').value,
    searchPanelDisplay: style('search-panel').display, searchPanelOpacity: parseFloat(style('search-panel').opacity),
    morphHeight: document.getElementById('motion-card').getBoundingClientRect().height
  }, animations, targets
};
"""


def state(sid: str) -> dict[str, Any]:
    value = execute(sid, STATE_JS)
    require(isinstance(value, dict), f"could not read motion state: {value!r}")
    return value


def require_no_overflow(s: dict[str, Any]) -> None:
    width = int(s.get("width", 0))
    require(int(s.get("scrollWidth", width + 2)) <= width + 1, f"horizontal overflow: {s}")


def approx(value: Any, target: float, tolerance: float = 2.0) -> bool:
    return isinstance(value, (int, float)) and abs(float(value) - target) <= tolerance


def assert_canonical(s: dict[str, Any]) -> None:
    require(s.get("ready") == "complete", "motion page not ready")
    for name, target in DURATIONS.items():
        require(approx(s.get("canonical", {}).get(name), target, .5), f"{name} canonical duration expected {target}, got {s.get('canonical', {}).get(name)}")
    require(all(value == "none" for value in s.get("animations", {}).values()), f"autonomous animation detected: {s.get('animations')}")
    require(all(float(t.get("w", 0)) >= 48 and float(t.get("h", 0)) >= 48 for t in s.get("targets", [])), f"48 px interaction floor drifted: {s.get('targets')}")
    require_no_overflow(s)


def assert_normal_timings(s: dict[str, Any]) -> None:
    expected = {"press": 80, "selection": 240, "popover": 160, "dialog": 240, "sheet": 360, "searchPanel": 360, "searchEntry": 360, "morph": 360, "direct": 0}
    for name, target in expected.items():
        require(approx(s.get("transitionMs", {}).get(name), target, 2), f"{name} transition expected {target}ms, got {s.get('transitionMs', {}).get(name)}")


def open_surface_immediate(sid: str, button_id: str, surface_id: str) -> None:
    result = execute(sid, f"""const button=document.getElementById('{button_id}'); const surface=document.getElementById('{surface_id}'); button.click(); return {{open:surface.dataset.open, expanded:button.getAttribute('aria-expanded')}};""")
    require(result == {"open": "true", "expanded": "true"}, f"{surface_id} semantic state waited for animation: {result}")


def main() -> int:
    http = driver = None
    sid: str | None = None
    try:
        validate_source()
        ARTIFACTS.mkdir(exist_ok=True)
        http = subprocess.Popen([sys.executable, "-m", "http.server", str(WEB_PORT), "--bind", HOST, "--directory", str(ROOT)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        wait_http(f"{SERVER}/{REFERENCE}")
        driver = subprocess.Popen([chromedriver(), f"--port={DRIVER_PORT}", "--allowed-ips=127.0.0.1"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        wait_driver()
        sid = session()
        media(sid, [])
        viewport(sid, 1280, 1100)
        navigate(sid)
        initial = state(sid)
        assert_canonical(initial)
        assert_normal_timings(initial)
        require(initial["states"]["selected"] == 0, f"initial selection drifted: {initial['states']}")

        selected = execute(sid, """document.getElementById('select-three').click(); return [...document.querySelectorAll('#selection-track [role="tab"]')].findIndex(x => x.getAttribute('aria-selected') === 'true');""")
        require(selected == 2, f"selection semantics waited for motion: {selected}")
        time.sleep(.3)
        after_selection = state(sid)
        require(after_selection["transforms"]["selectionX"] > 120, f"selection indicator did not move: {after_selection}")

        open_surface_immediate(sid, "popover-toggle", "motion-popover")
        open_surface_immediate(sid, "dialog-toggle", "motion-dialog")
        open_surface_immediate(sid, "sheet-toggle", "motion-sheet")
        time.sleep(.4)
        opened = state(sid)
        for key in ("popover", "dialog", "sheet"):
            require(opened["states"][key] == "true", f"{key} did not remain open")
            require(opened["transforms"][key] == "none", f"{key} did not settle: {opened['transforms'][key]}")

        execute(sid, "window.__motionQuery = document.getElementById('search-query'); window.__motionQuery.value='continuity'; return true;")
        search_open = execute(sid, """document.getElementById('search-toggle').click(); return {open:document.getElementById('motion-search').dataset.open,same:window.__motionQuery===document.getElementById('search-query'),value:document.getElementById('search-query').value,active:document.activeElement.id};""")
        require(search_open == {"open": "true", "same": True, "value": "continuity", "active": "search-query"}, f"Search continuity failed on open: {search_open}")
        time.sleep(.4)
        search_settled = state(sid)
        require(search_settled["states"]["searchPanelDisplay"] == "block" and search_settled["states"]["searchPanelOpacity"] > .98, f"Search panel did not settle open: {search_settled['states']}")
        search_close = execute(sid, """document.getElementById('search-toggle').click(); return {open:document.getElementById('motion-search').dataset.open,same:window.__motionQuery===document.getElementById('search-query'),value:document.getElementById('search-query').value,active:document.activeElement.id};""")
        require(search_close == {"open": "false", "same": True, "value": "continuity", "active": "search-query"}, f"Search continuity failed on close: {search_close}")

        execute(sid, "window.__motionTitle = document.getElementById('motion-card-title'); return true;")
        base_height = state(sid)["states"]["morphHeight"]
        morph_immediate = execute(sid, """const card=document.getElementById('motion-card'); card.click(); const first=card.getAttribute('aria-expanded'); card.click(); const second=card.getAttribute('aria-expanded'); card.click(); return {first,second,final:card.getAttribute('aria-expanded'),same:window.__motionTitle===document.getElementById('motion-card-title')};""")
        require(morph_immediate == {"first": "true", "second": "false", "final": "true", "same": True}, f"MorphCard interruption/reversal failed: {morph_immediate}")
        time.sleep(.4)
        morph_open = state(sid)
        require(morph_open["states"]["morphHeight"] > base_height + 40, f"MorphCard did not expand: {morph_open['states']}")

        direct = execute(sid, """const range=document.getElementById('direct-range'); range.value='64'; range.dispatchEvent(new Event('input',{bubbles:true})); return new DOMMatrix(getComputedStyle(document.getElementById('direct-object')).transform).m41;""")
        require(approx(direct, 64, .5), f"direct manipulation did not track input: {direct}")

        for appearance in ("light", "dark", "deep-dark"):
            execute(sid, f"document.documentElement.dataset.glzAppearance='{appearance}'; return true;")
            current = state(sid)
            assert_canonical(current)
            assert_normal_timings(current)
            screenshot(sid, appearance)

        execute(sid, "document.documentElement.dataset.glzMaterialPerformance='reduced'; return true;")
        reduced_perf = state(sid)
        expected_reduced = {"instant": 60, "fast": 120, "standard": 180, "deliberate": 270, "spatial": 360}
        for name, target in expected_reduced.items():
            require(approx(reduced_perf["effective"][name], target, .5), f"reduced performance {name} drifted: {reduced_perf['effective']}")

        execute(sid, "document.documentElement.dataset.glzMaterialPerformance='minimal'; return true;")
        minimal = state(sid)
        require(all(approx(value, 0, .1) for value in minimal["effective"].values()), f"minimal motion durations did not collapse: {minimal['effective']}")
        require(all(approx(minimal["transitionMs"][name], 0, .1) for name in ("press","selection","popover","dialog","sheet","searchPanel","searchEntry","morph","direct")), f"minimal profile retained transition duration: {minimal['transitionMs']}")

        execute(sid, "document.documentElement.dataset.glzMaterialPerformance='full'; document.documentElement.dataset.mode='reduced-motion'; return true;")
        media(sid, [{"name": "prefers-reduced-motion", "value": "reduce"}])
        execute(sid, """document.getElementById('motion-popover').dataset.open='true'; document.getElementById('motion-dialog').dataset.open='true'; document.getElementById('motion-sheet').dataset.open='true'; document.getElementById('motion-search').dataset.open='true'; document.getElementById('motion-card').setAttribute('aria-expanded','true'); const range=document.getElementById('direct-range'); range.value='72'; range.dispatchEvent(new Event('input',{bubbles:true})); return true;""")
        time.sleep(.1)
        reduced_motion = state(sid)
        for name in ("popover","dialog","sheet","searchPanel"):
            require(reduced_motion["transforms"][name] == "none", f"Reduced Motion retained nonessential spatial transform for {name}: {reduced_motion['transforms'][name]}")
        require(reduced_motion["transitionMs"]["selection"] == 0 and reduced_motion["transitionMs"]["morph"] == 0, f"Reduced Motion retained selection/Morph travel: {reduced_motion['transitionMs']}")
        require(reduced_motion["transitionMs"]["popover"] <= 80.5 and reduced_motion["transitionMs"]["dialog"] <= 80.5 and reduced_motion["transitionMs"]["sheet"] <= 80.5 and reduced_motion["transitionMs"]["searchPanel"] <= 80.5, f"Reduced Motion fade exceeded 80 ms: {reduced_motion['transitionMs']}")
        require(approx(reduced_motion["transforms"]["directX"], 72, .5), f"Reduced Motion detached direct manipulation: {reduced_motion['transforms']['directX']}")
        screenshot(sid, "reduced-motion")

        execute(sid, "delete document.documentElement.dataset.mode; return true;")
        media(sid, [{"name": "forced-colors", "value": "active"}])
        forced = state(sid)
        require(all(approx(forced["transitionMs"][name], 0, .1) for name in ("press","selection","popover","dialog","sheet","searchPanel","searchEntry","morph","direct")), f"Forced Colors retained custom transition delay: {forced['transitionMs']}")
        require(all(value == "none" for value in forced["animations"].values()), f"Forced Colors retained animation: {forced['animations']}")
        screenshot(sid, "forced-colors")

        media(sid, [])
        viewport(sid, 390, 900)
        execute(sid, """document.documentElement.dataset.glzAppearance='light'; document.documentElement.dataset.glzTextScale='200'; document.documentElement.style.fontSize='200%'; document.getElementById('motion-search').dataset.open='false'; document.getElementById('motion-popover').dataset.open='false'; document.getElementById('motion-dialog').dataset.open='false'; document.getElementById('motion-sheet').dataset.open='false'; return true;""")
        compact = state(sid)
        require_no_overflow(compact)
        require(all(float(t.get("w", 0)) >= 48 and float(t.get("h", 0)) >= 48 for t in compact.get("targets", [])), f"compact 200% target floor drifted: {compact.get('targets')}")
        screenshot(sid, "compact-200")
        print("GLAZE UI V1.2 Motion and Connected Transformation rendered validation: PASS")
        return 0
    except AcceptanceError as error:
        print(f"GLAZE UI V1.2 Motion and Connected Transformation rendered validation failed: {error}", file=sys.stderr)
        return 1
    finally:
        if sid:
            try:
                request("DELETE", f"/session/{sid}")
            except Exception:
                pass
        for process in (driver, http):
            if process:
                process.terminate()
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    process.kill()


if __name__ == "__main__":
    raise SystemExit(main())
