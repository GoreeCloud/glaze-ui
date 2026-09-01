#!/usr/bin/env python3
"""Rendered Glaze UI 2.2 performance / Glaze-budget acceptance."""
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

PAGE = "candidate-2.2-performance-acceptance.html"


def run_case(browser: str, port: int, *, width: int, height: int, profile: str,
             appearance: str = "light", mode: str = "normal") -> None:
    name = f"2.2 Performance {profile} {width}x{height} {appearance} mode={mode}"
    params = {"profile": profile, "appearance": appearance, "mode": mode}
    last = "browser did not produce a result"
    for attempt in range(1, RENDER_ATTEMPTS + 1):
        query = urllib.parse.urlencode({**params, "attempt": attempt})
        url = f"http://127.0.0.1:{port}/reference/{PAGE}?{query}"
        with tempfile.TemporaryDirectory(prefix="glaze-22-performance-") as temp:
            command = browser_command(browser, url, temp, width=width, height=height, mode=mode)
            try:
                completed = run_browser(command)
            except subprocess.TimeoutExpired as exc:
                stdout = exc.stdout.decode(errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
                stderr = exc.stderr.decode(errors="replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
                last = f"attempt {attempt} timed out\n{(stdout or stderr)[-2000:]}"
                if attempt < RENDER_ATTEMPTS:
                    print(f"Glaze UI 2.2 performance acceptance retrying: {name}")
                    continue
                break
        status, text = acceptance_result(completed.stdout)
        if completed.returncode != 0:
            last = f"attempt {attempt} browser exited {completed.returncode}\n{completed.stderr[-2000:]}"
        elif status == "pass" and text and text.startswith("PASS"):
            print(f"Glaze UI 2.2 performance rendered acceptance passed: {name}")
            return
        elif status == "fail":
            raise SystemExit(f"Glaze UI 2.2 performance rendered acceptance failed for {name}:\n{text or '(no result text)'}")
        else:
            last = f"attempt {attempt} did not reach PASS (status={status or 'missing'})\n{text or completed.stdout[-3000:]}"
        if attempt < RENDER_ATTEMPTS:
            print(f"Glaze UI 2.2 performance acceptance retrying: {name}")
    raise SystemExit(f"Glaze UI 2.2 performance rendered acceptance failed for {name} after {RENDER_ATTEMPTS} attempts:\n{last}")


def main() -> None:
    browser = find_browser()
    cases = (
        dict(width=390, height=844, profile="full", appearance="light"),
        dict(width=390, height=844, profile="balanced", appearance="dark"),
        dict(width=390, height=844, profile="constrained", appearance="light"),
        dict(width=390, height=844, profile="minimal", appearance="dark"),
        dict(width=820, height=1180, profile="full", appearance="dark"),
        dict(width=820, height=1180, profile="constrained", appearance="light"),
        dict(width=1280, height=900, profile="full", appearance="light"),
        dict(width=1280, height=900, profile="balanced", appearance="deep-dark"),
        dict(width=1280, height=900, profile="constrained", appearance="dark"),
        dict(width=1280, height=900, profile="minimal", appearance="light"),
        dict(width=1280, height=900, profile="full", appearance="dark", mode="reduced-transparency"),
        dict(width=1280, height=900, profile="full", appearance="light", mode="forced-colors"),
        dict(width=1600, height=1000, profile="balanced", appearance="light"),
    )
    with serve_root() as port:
        for case in cases:
            run_case(browser, port, **case)
    print("Glaze UI 2.2 performance / Glaze-budget rendered acceptance passed")


if __name__ == "__main__":
    main()
