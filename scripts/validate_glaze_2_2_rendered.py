#!/usr/bin/env python3
"""Rendered acceptance for the bounded Glaze UI 2.2 Candidate system shell.

This validator exercises the dependency-free web reference in a real Chromium
renderer. It proves only the cases enumerated here and does not manufacture
native, physical-device, downstream-consumer, or human Visual Excellence evidence.
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
    flow: str,
    width: int,
    height: int,
    appearance: str,
    form_factor: str,
    mode: str = "normal",
    performance: str = "balanced",
) -> None:
    params = {
        "flow": flow,
        "width": width,
        "height": height,
        "appearance": appearance,
        "formFactor": form_factor,
        "mode": mode,
        "performance": performance,
    }
    name = (
        f"2.2 {flow} {form_factor} {width}x{height} "
        f"appearance={appearance} mode={mode} performance={performance}"
    )
    last = "browser did not produce a result"

    for attempt in range(1, RENDER_ATTEMPTS + 1):
        query = urllib.parse.urlencode({**params, "attempt": attempt})
        url = (
            f"http://127.0.0.1:{port}/reference/"
            f"candidate-2.2-system-shell.html?{query}"
        )
        with tempfile.TemporaryDirectory(prefix="glaze-22-render-") as profile:
            command = browser_command(
                browser,
                url,
                profile,
                width=width,
                height=height,
                mode=mode,
            )
            try:
                completed = run_browser(command)
            except subprocess.TimeoutExpired as exc:
                stdout = (
                    exc.stdout.decode(errors="replace")
                    if isinstance(exc.stdout, bytes)
                    else (exc.stdout or "")
                )
                stderr = (
                    exc.stderr.decode(errors="replace")
                    if isinstance(exc.stderr, bytes)
                    else (exc.stderr or "")
                )
                last = (
                    f"attempt {attempt} timed out\n"
                    f"{(stdout or stderr)[-2500:]}"
                )
                if attempt < RENDER_ATTEMPTS:
                    print(f"Glaze UI 2.2 rendered acceptance retrying: {name}")
                    continue
                break

        status, text = acceptance_result(completed.stdout)
        if completed.returncode != 0:
            last = (
                f"attempt {attempt} browser exited {completed.returncode}\n"
                f"{completed.stderr[-2500:]}"
            )
        elif status == "pass" and text and text.startswith("PASS"):
            print(f"Glaze UI 2.2 rendered acceptance passed: {name}")
            return
        elif status == "fail":
            raise SystemExit(
                f"Glaze UI 2.2 rendered acceptance failed for {name}:\n"
                f"{text or '(no result text)'}"
            )
        else:
            marker = completed.stdout[-3500:] if completed.stdout else completed.stderr[-3500:]
            last = (
                f"attempt {attempt} did not reach PASS "
                f"(status={status or 'missing'})\n{text or marker}"
            )

        if attempt < RENDER_ATTEMPTS:
            print(f"Glaze UI 2.2 rendered acceptance retrying: {name}")

    raise SystemExit(
        f"Glaze UI 2.2 rendered acceptance failed for {name} "
        f"after {RENDER_ATTEMPTS} attempts:\n{last}"
    )


def main() -> None:
    browser = find_browser()
    with serve_root() as port:
        cases = (
            dict(flow="workspace", width=390, height=844, appearance="light", form_factor="mobile"),
            dict(flow="workspace", width=820, height=1180, appearance="dark", form_factor="tablet"),
            dict(flow="workspace", width=1280, height=900, appearance="light", form_factor="desktop"),
            dict(flow="workspace", width=1280, height=900, appearance="deep-dark", form_factor="desktop"),
            dict(flow="search", width=1280, height=900, appearance="light", form_factor="desktop"),
            dict(flow="search", width=1280, height=900, appearance="deep-dark", form_factor="desktop"),
            dict(flow="control-center", width=820, height=1180, appearance="dark", form_factor="tablet"),
            dict(flow="control-center", width=1280, height=900, appearance="dark", form_factor="desktop", mode="reduced-transparency"),
            dict(flow="critical", width=1280, height=900, appearance="dark", form_factor="desktop"),
            dict(flow="workspace", width=1280, height=900, appearance="light", form_factor="desktop", mode="reduced-motion"),
            dict(flow="workspace", width=390, height=844, appearance="light", form_factor="mobile", mode="large-text"),
            dict(flow="workspace", width=390, height=844, appearance="light", form_factor="mobile", mode="touch-assistance"),
            dict(flow="workspace", width=1280, height=900, appearance="light", form_factor="desktop", mode="increased-contrast"),
            dict(flow="workspace", width=1280, height=900, appearance="light", form_factor="desktop", mode="forced-colors"),
            dict(flow="workspace", width=1280, height=900, appearance="dark", form_factor="desktop", performance="minimal"),
        )
        for case in cases:
            run_case(browser, port, **case)

    print("Glaze UI 2.2 Candidate rendered System Shell acceptance passed")


if __name__ == "__main__":
    main()
