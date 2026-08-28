#!/usr/bin/env python3
"""Run rendered acceptance for the enforced Glaze UI 2.0 Candidate contract."""

from __future__ import annotations

import tempfile
import urllib.parse

from validate_rendered_reference import (
    RENDER_ATTEMPTS,
    TV_FORCED_COLORS_ATTEMPTS,
    acceptance_result,
    browser_command,
    find_browser,
    run_browser,
    serve_root,
)


def run_candidate_case(
    browser: str,
    port: int,
    *,
    width: int,
    height: int,
    appearance: str,
    form_factor: str,
    clarity: str = "balanced",
    expression: str = "balanced",
    mode: str = "normal",
) -> None:
    base_params = {
        "width": width,
        "height": height,
        "appearance": appearance,
        "clarity": clarity,
        "expression": expression,
        "formFactor": form_factor,
        "mode": mode,
    }
    case_name = (
        f"candidate20 {form_factor} {width}x{height} {appearance} "
        f"clarity={clarity} expression={expression} mode={mode}"
    )
    attempts = (
        TV_FORCED_COLORS_ATTEMPTS
        if form_factor == "tv" and mode == "forced-colors"
        else RENDER_ATTEMPTS
    )
    last_failure = "browser did not produce a result"

    for attempt in range(1, attempts + 1):
        query = urllib.parse.urlencode({**base_params, "attempt": attempt})
        url = f"http://127.0.0.1:{port}/reference/candidate-2.0-acceptance.html?{query}"
        with tempfile.TemporaryDirectory(prefix="glaze-candidate20-render-") as profile_dir:
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
                if attempt < attempts:
                    print(f"Glaze UI 2.0 rendered acceptance retrying: {case_name}")
                    continue
                break

        status, result_text = acceptance_result(completed.stdout)
        if completed.returncode != 0:
            last_failure = (
                f"attempt {attempt} browser exited {completed.returncode}\n"
                f"{completed.stderr[-2000:]}"
            )
        elif status == "pass" and result_text and result_text.startswith("PASS"):
            print(f"Glaze UI 2.0 rendered acceptance passed: {case_name}")
            return
        elif status == "fail":
            raise SystemExit(
                f"Glaze UI 2.0 rendered acceptance failed for {case_name}:\n"
                f"attempt {attempt} harness reported FAIL\n{result_text or '(no result text)'}"
            )
        else:
            marker = completed.stdout[-4000:] if completed.stdout else completed.stderr[-4000:]
            last_failure = (
                f"attempt {attempt} did not reach PASS (status={status or 'missing'})\n"
                f"{result_text or marker}"
            )

        if attempt < attempts:
            print(f"Glaze UI 2.0 rendered acceptance retrying: {case_name}")

    raise SystemExit(
        f"Glaze UI 2.0 rendered acceptance failed for {case_name} after {attempts} attempts:\n"
        f"{last_failure}"
    )


def main() -> None:
    browser = find_browser()
    with serve_root() as port:
        representative = (
            (390, 844, "mobile"),
            (820, 1180, "tablet"),
            (1280, 900, "desktop"),
            (1600, 1000, "wide-desktop"),
            (1920, 1080, "tv"),
        )

        # Core adaptive matrix: every required Stable production form factor in Light and Dark.
        for width, height, form_factor in representative:
            for appearance in ("light", "dark"):
                run_candidate_case(
                    browser,
                    port,
                    width=width,
                    height=height,
                    appearance=appearance,
                    form_factor=form_factor,
                )

        # Deep Dark gets compact and large-surface coverage.
        for width, height, form_factor in ((390, 844, "mobile"), (1280, 900, "desktop")):
            run_candidate_case(
                browser,
                port,
                width=width,
                height=height,
                appearance="deep-dark",
                form_factor=form_factor,
            )

        # Material clarity and expression axes are independently rendered.
        for clarity in ("clear", "solid"):
            run_candidate_case(
                browser,
                port,
                width=1280,
                height=900,
                appearance="light",
                form_factor="desktop",
                clarity=clarity,
            )
        for expression in ("calm", "expressive"):
            run_candidate_case(
                browser,
                port,
                width=1280,
                height=900,
                appearance="dark",
                form_factor="desktop",
                expression=expression,
            )

        # Accessibility and rendering-resilience cases.
        run_candidate_case(
            browser,
            port,
            width=390,
            height=844,
            appearance="light",
            form_factor="mobile",
            mode="large-text",
        )
        run_candidate_case(
            browser,
            port,
            width=390,
            height=844,
            appearance="light",
            form_factor="mobile",
            mode="reduced-motion",
        )
        run_candidate_case(
            browser,
            port,
            width=390,
            height=844,
            appearance="dark",
            form_factor="mobile",
            mode="reduced-transparency",
        )
        run_candidate_case(
            browser,
            port,
            width=1280,
            height=900,
            appearance="dark",
            form_factor="desktop",
            mode="no-backdrop",
        )
        run_candidate_case(
            browser,
            port,
            width=1920,
            height=1080,
            appearance="dark",
            form_factor="tv",
            mode="forced-colors",
        )

    print("Glaze UI 2.0 Candidate rendered acceptance passed")


if __name__ == "__main__":
    main()
