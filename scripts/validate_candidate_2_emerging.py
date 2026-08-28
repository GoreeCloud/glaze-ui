#!/usr/bin/env python3
"""Validate Glaze UI 2.0 Candidate wearable and spatial implementation acceptance."""

from __future__ import annotations

import tempfile
import urllib.parse
from pathlib import Path

from validate_rendered_reference import (
    RENDER_ATTEMPTS,
    acceptance_result,
    browser_command,
    find_browser,
    run_browser,
    serve_root,
)

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / "tokens" / "glaze-2.candidate.json"
CSS = ROOT / "css" / "glaze-2.emerging.candidate.css"
RUNTIME = ROOT / "js" / "glaze-2.emerging.candidate.js"
REFERENCE = ROOT / "reference" / "candidate-2.0-emerging.html"
HARNESS = ROOT / "reference" / "candidate-2.0-emerging-acceptance.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Glaze UI 2.0 wearable/spatial acceptance failed: {message}")


def validate_source() -> None:
    import json

    for path in (TOKENS, CSS, RUNTIME, REFERENCE, HARNESS):
        require(path.is_file(), f"missing required artifact: {path.relative_to(ROOT)}")

    data = json.loads(TOKENS.read_text(encoding="utf-8"))
    css = CSS.read_text(encoding="utf-8")
    runtime = RUNTIME.read_text(encoding="utf-8")
    reference = REFERENCE.read_text(encoding="utf-8")
    harness = HARNESS.read_text(encoding="utf-8")

    navigation = data.get("layout", {}).get("navigationTransform", {})
    require(navigation.get("wearable") == "compact-rotational-navigation", "wearable navigation transform drifted")
    require(navigation.get("spatial") == "floating-control-surface", "spatial navigation transform drifted")
    require(data.get("accessibility", {}).get("usableWithoutAdvancedEffects") is True, "advanced-effects fallback invariant missing")

    for marker in (
        ".glaze-wearable-frame",
        ".glaze-wearable-rotary-nav",
        "--glaze-wearable-target: 48px",
        ".glaze-spatial-stage",
        ".glaze-spatial-anchor",
        ".glaze-spatial-control-surface",
        "data-glaze-spatial-flat",
        "prefers-reduced-motion",
        "prefers-contrast",
        "forced-colors",
        "@supports not (transform-style: preserve-3d)",
    ):
        require(marker in css, f"emerging-environment CSS missing: {marker}")

    for marker in (
        "bindRotaryNavigation",
        "setRotarySelection",
        "moveRotarySelection",
        "setSpatialDepth",
        "setSpatialFlat",
        "aria-current",
        "tabIndex",
        "wheel",
        "ArrowDown",
    ):
        require(marker in runtime, f"emerging-environment runtime missing: {marker}")

    lowered_runtime = runtime.lower()
    for forbidden in (
        "fetch(",
        "xmlhttprequest",
        "websocket",
        "eventsource",
        "webtransport",
        "navigator.sendbeacon",
        "localstorage",
        "sessionstorage",
        "indexeddb",
        "document.cookie",
        "caches.open",
        "analytics",
        "sentry",
        "amplitude",
        "mixpanel",
        "eval(",
        "new function(",
        ".innerhtml",
        "document.write(",
    ):
        require(forbidden not in lowered_runtime, f"runtime contains forbidden dependency/storage/unsafe marker: {forbidden}")

    for label, source in (
        ("emerging CSS", css),
        ("emerging runtime", runtime),
        ("emerging reference", reference),
        ("emerging harness", harness),
    ):
        lowered = source.lower()
        for forbidden in ("http://", "https://", "@import ", "url(//", "src=\"//", "href=\"//"):
            require(forbidden not in lowered, f"{label} contains forbidden remote dependency marker: {forbidden}")

    require('href="../css/glaze-2.candidate.css"' in reference, "reference must include core Candidate CSS")
    require('href="../css/glaze-2.emerging.candidate.css"' in reference, "reference must include emerging Candidate CSS")
    require("from '../js/glaze-2.candidate.js'" in reference, "reference must include core Candidate runtime")
    require("from '../js/glaze-2.emerging.candidate.js'" in reference, "reference must include emerging Candidate runtime")


def run_case(
    browser: str,
    port: int,
    *,
    test_case: str,
    width: int,
    height: int,
    appearance: str,
    mode: str = "normal",
    flat: bool = False,
) -> None:
    base_params = {
        "case": test_case,
        "width": width,
        "height": height,
        "appearance": appearance,
        "mode": mode,
        "flat": "1" if flat else "0",
    }
    case_name = f"candidate20-emerging {test_case} {width}x{height} {appearance} {mode}{' flat' if flat else ''}"
    last_failure = "browser did not produce a result"

    for attempt in range(1, RENDER_ATTEMPTS + 1):
        query = urllib.parse.urlencode({**base_params, "attempt": attempt})
        url = f"http://127.0.0.1:{port}/reference/candidate-2.0-emerging-acceptance.html?{query}"
        with tempfile.TemporaryDirectory(prefix="glaze-candidate20-emerging-") as profile_dir:
            command = browser_command(
                browser,
                url,
                profile_dir,
                width=width,
                height=height,
                mode=mode,
            )
            try:
                completed = run_browser(command)
            except Exception as exc:
                last_failure = f"attempt {attempt} browser execution failed: {exc}"
                if attempt < RENDER_ATTEMPTS:
                    print(f"Glaze UI 2.0 wearable/spatial acceptance retrying: {case_name}")
                    continue
                break

        status, result_text = acceptance_result(completed.stdout)
        if completed.returncode != 0:
            last_failure = f"attempt {attempt} browser exited {completed.returncode}\n{completed.stderr[-2000:]}"
        elif status == "pass" and result_text and result_text.startswith("PASS"):
            print(f"Glaze UI 2.0 wearable/spatial acceptance passed: {case_name}")
            return
        elif status == "fail":
            raise SystemExit(
                f"Glaze UI 2.0 wearable/spatial acceptance failed for {case_name}:\n"
                f"attempt {attempt} harness reported FAIL\n{result_text or '(no result text)'}"
            )
        else:
            marker = completed.stdout[-4000:] if completed.stdout else completed.stderr[-4000:]
            last_failure = f"attempt {attempt} did not reach PASS (status={status or 'missing'})\n{result_text or marker}"

        if attempt < RENDER_ATTEMPTS:
            print(f"Glaze UI 2.0 wearable/spatial acceptance retrying: {case_name}")

    raise SystemExit(
        f"Glaze UI 2.0 wearable/spatial acceptance failed for {case_name} after {RENDER_ATTEMPTS} attempts:\n{last_failure}"
    )


def main() -> None:
    validate_source()
    browser = find_browser()
    with serve_root() as port:
        run_case(browser, port, test_case="wearable", width=360, height=360, appearance="light")
        run_case(browser, port, test_case="wearable", width=360, height=360, appearance="dark", mode="reduced-motion")
        run_case(browser, port, test_case="spatial", width=1280, height=800, appearance="dark")
        run_case(browser, port, test_case="spatial", width=1024, height=768, appearance="light", flat=True)

    print("Glaze UI 2.0 Candidate wearable and spatial implementation acceptance passed; native-device certification remains separate")


if __name__ == "__main__":
    main()
