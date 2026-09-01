#!/usr/bin/env python3
"""Capture exact-head Glaze UI 2.2 Optical Reachability component review images.

These screenshots are human-review evidence only. They do not establish an
approved baseline or Human Visual Excellence on their own.
"""
from __future__ import annotations

import shutil
import tempfile
import urllib.parse
from pathlib import Path

from validate_rendered_reference import (
    FORCED_COLORS_VIRTUAL_TIME_BUDGET_MS,
    RENDER_ATTEMPTS,
    VIRTUAL_TIME_BUDGET_MS,
    find_browser,
    run_browser,
    serve_root,
)

ROOT = Path(__file__).resolve().parents[1]
PAGE = "candidate-2.2-optical-reachability-acceptance.html"

CASES = (
    dict(id="optical-components-desktop-light", width=1280, height=900, appearance="light", mode="normal", direction="ltr", input="pointer"),
    dict(id="optical-components-mobile-dark", width=390, height=844, appearance="dark", mode="normal", direction="ltr", input="touch"),
    dict(id="optical-components-tablet-reduced-transparency", width=820, height=1180, appearance="dark", mode="reduced-transparency", direction="ltr", input="touch"),
    dict(id="optical-components-mobile-large-text", width=390, height=844, appearance="light", mode="large-text", direction="ltr", input="touch"),
    dict(id="optical-components-mobile-touch-assisted", width=390, height=844, appearance="light", mode="touch-assistance", direction="ltr", input="touch"),
    dict(id="optical-components-desktop-deep-dark", width=1280, height=900, appearance="deep-dark", mode="normal", direction="ltr", input="pointer"),
)


def case_url(port: int, case: dict) -> str:
    query = urllib.parse.urlencode({
        "appearance": case["appearance"],
        "mode": case["mode"],
        "direction": case["direction"],
        "input": case["input"],
    })
    return f"http://127.0.0.1:{port}/reference/{PAGE}?{query}"


def screenshot_command(browser: str, url: str, profile: str, output: Path, case: dict) -> list[str]:
    virtual_time = FORCED_COLORS_VIRTUAL_TIME_BUDGET_MS if case["mode"] == "forced-colors" else VIRTUAL_TIME_BUDGET_MS
    command = [
        browser,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--disable-background-networking",
        "--disable-background-timer-throttling",
        "--disable-backgrounding-occluded-windows",
        "--disable-renderer-backgrounding",
        "--disable-default-apps",
        "--disable-extensions",
        "--disable-sync",
        "--hide-scrollbars",
        "--mute-audio",
        "--no-first-run",
        "--run-all-compositor-stages-before-draw",
        "--force-device-scale-factor=1",
        f"--virtual-time-budget={virtual_time}",
        f"--user-data-dir={profile}",
        f"--window-size={case['width']},{case['height']}",
        f"--screenshot={output}",
    ]
    if case["appearance"] == "dark":
        command.append("--force-dark-mode")
    if case["mode"] == "reduced-motion":
        command.append("--force-prefers-reduced-motion")
    elif case["mode"] == "forced-colors":
        command.append("--force-high-contrast")
    command.append(url)
    return command


def capture_case(browser: str, port: int, case: dict, output: Path) -> None:
    last = "browser did not create a PNG"
    for attempt in range(1, RENDER_ATTEMPTS + 1):
        output.unlink(missing_ok=True)
        with tempfile.TemporaryDirectory(prefix="glaze-22-optical-review-") as profile:
            completed = run_browser(screenshot_command(browser, case_url(port, case), profile, output, case))
        if completed.returncode == 0 and output.is_file() and output.stat().st_size >= 256:
            print(f"Captured Glaze UI 2.2 Optical Reachability review case: {case['id']} -> {output}")
            return
        if completed.returncode != 0:
            last = f"attempt {attempt}: browser exited {completed.returncode}\n{completed.stderr[-2000:]}"
        elif not output.is_file():
            last = f"attempt {attempt}: PNG was not created"
        else:
            last = f"attempt {attempt}: PNG was only {output.stat().st_size} bytes"
        if attempt < RENDER_ATTEMPTS:
            print(f"Optical Reachability review capture retrying: {case['id']} ({attempt + 1}/{RENDER_ATTEMPTS})")
    raise SystemExit(f"Optical Reachability review capture failed for {case['id']}:\n{last}")


def main() -> None:
    output_dir = ROOT / ".artifacts" / "glaze-2.2-optical-component-review"
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)
    browser = find_browser()
    with serve_root() as port:
        for case in CASES:
            capture_case(browser, port, case, output_dir / f"{case['id']}.png")
    count = len(tuple(output_dir.glob("*.png")))
    if count != len(CASES):
        raise SystemExit(f"expected {len(CASES)} Optical Reachability review images, found {count}")
    print("Glaze UI 2.2 Optical Reachability component review capture completed. Evidence only; human approval remains required.")


if __name__ == "__main__":
    main()
