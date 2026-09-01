#!/usr/bin/env python3
"""Rendered acceptance for Glaze UI 2.2 Foundation components.

This validates bounded web/reference behavior only. It does not establish
native-device acceptance, complete component-library coverage, human Visual
Excellence approval, downstream consumer readiness, or Stable promotion.
"""
from __future__ import annotations

import subprocess
import tempfile
import urllib.parse

from validate_rendered_reference import (
    RENDER_ATTEMPTS,
    acceptance_result,
    browser_command,
    find_browser,
    run_browser,
    serve_root,
)


def run_case(
    browser: str,
    port: int,
    *,
    page: str = "candidate-2.2-components.html",
    width: int,
    height: int,
    appearance: str = "light",
    mode: str = "normal",
    direction: str = "ltr",
    input_mode: str = "pointer",
) -> None:
    params = {
        "appearance": appearance,
        "mode": mode,
        "direction": direction,
        "input": input_mode,
    }
    name = f"2.2 components {page} {width}x{height} {appearance} mode={mode} dir={direction} input={input_mode}"
    last = "browser did not produce a result"
    for attempt in range(1, RENDER_ATTEMPTS + 1):
        query = urllib.parse.urlencode({**params, "attempt": attempt})
        url = f"http://127.0.0.1:{port}/reference/{page}?{query}"
        with tempfile.TemporaryDirectory(prefix="glaze-22-components-") as profile:
            command = browser_command(browser, url, profile, width=width, height=height, mode=mode)
            try:
                completed = run_browser(command)
            except subprocess.TimeoutExpired as exc:
                stdout = exc.stdout.decode(errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
                stderr = exc.stderr.decode(errors="replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
                last = f"attempt {attempt} timed out\n{(stdout or stderr)[-2000:]}"
                if attempt < RENDER_ATTEMPTS:
                    print(f"Glaze UI 2.2 component acceptance retrying: {name}")
                    continue
                break

        status, text = acceptance_result(completed.stdout)
        if completed.returncode != 0:
            last = f"attempt {attempt} browser exited {completed.returncode}\n{completed.stderr[-2000:]}"
        elif status == "pass" and text and text.startswith("PASS"):
            print(f"Glaze UI 2.2 component rendered acceptance passed: {name}")
            return
        elif status == "fail":
            raise SystemExit(
                f"Glaze UI 2.2 component rendered acceptance failed for {name}:\n{text or '(no result text)'}"
            )
        else:
            last = f"attempt {attempt} did not reach PASS (status={status or 'missing'})\n{text or completed.stdout[-3000:]}"
        if attempt < RENDER_ATTEMPTS:
            print(f"Glaze UI 2.2 component acceptance retrying: {name}")

    raise SystemExit(
        f"Glaze UI 2.2 component rendered acceptance failed for {name} after {RENDER_ATTEMPTS} attempts:\n{last}"
    )


def main() -> None:
    browser = find_browser()
    cases = (
        dict(width=390, height=844, appearance="light", mode="normal", input_mode="touch"),
        dict(width=390, height=844, appearance="dark", mode="reduced-transparency", input_mode="touch"),
        dict(width=390, height=844, appearance="light", mode="large-text", input_mode="touch"),
        dict(width=390, height=844, appearance="light", mode="touch-assistance", input_mode="touch"),
        dict(width=820, height=1180, appearance="dark", mode="normal", input_mode="touch"),
        dict(width=1280, height=900, appearance="light", mode="normal"),
        dict(width=1280, height=900, appearance="dark", mode="reduced-motion"),
        dict(width=1280, height=900, appearance="deep-dark", mode="normal"),
        dict(width=1280, height=900, appearance="light", mode="increased-contrast"),
        dict(width=1280, height=900, appearance="light", mode="forced-colors"),
        dict(width=1280, height=900, appearance="dark", mode="normal", direction="rtl"),
        dict(page="candidate-2.2-components-adaptive.html", width=390, height=844, appearance="light", mode="touch", input_mode="touch"),
        dict(page="candidate-2.2-components-adaptive.html", width=390, height=844, appearance="light", mode="touch-assistance", input_mode="touch"),
        dict(page="candidate-2.2-components-adaptive.html", width=1280, height=900, appearance="light", mode="increased-contrast"),
        dict(page="candidate-2.2-components-adaptive.html", width=1280, height=900, appearance="dark", mode="reduced-transparency"),
    )
    with serve_root() as port:
        for case in cases:
            run_case(browser, port, **case)
    print("Glaze UI 2.2 Foundation component rendered acceptance passed")


if __name__ == "__main__":
    main()
