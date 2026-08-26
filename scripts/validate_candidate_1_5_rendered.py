#!/usr/bin/env python3
"""Run rendered acceptance for Glaze UI 1.5 Candidate motion and materials."""

from __future__ import annotations

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


def run_candidate_case(
    browser: str,
    port: int,
    *,
    width: int,
    height: int,
    theme: str,
    mode: str = "normal",
) -> None:
    query = urllib.parse.urlencode(
        {"width": width, "height": height, "theme": theme, "mode": mode}
    )
    url = f"http://127.0.0.1:{port}/reference/candidate-1.5-acceptance.html?{query}"
    case_name = f"candidate15 {width}x{height} {theme} {mode}"
    last_failure = "browser did not produce a result"

    for attempt in range(1, RENDER_ATTEMPTS + 1):
        with tempfile.TemporaryDirectory(prefix="glaze-candidate15-render-") as profile_dir:
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
                    print(f"Candidate rendered acceptance retrying: {case_name}")
                    continue
                break

        status, result_text = acceptance_result(completed.stdout)
        if completed.returncode != 0:
            last_failure = (
                f"attempt {attempt} browser exited {completed.returncode}\n"
                f"{completed.stderr[-2000:]}"
            )
        elif status == "pass" and result_text and result_text.startswith("PASS"):
            print(f"Candidate rendered acceptance passed: {case_name}")
            return
        elif status == "fail":
            last_failure = f"attempt {attempt} harness reported FAIL\n{result_text or '(no result text)'}"
        else:
            marker = completed.stdout[-4000:] if completed.stdout else completed.stderr[-4000:]
            last_failure = (
                f"attempt {attempt} did not reach PASS (status={status or 'missing'})\n"
                f"{result_text or marker}"
            )

        if attempt < RENDER_ATTEMPTS:
            print(f"Candidate rendered acceptance retrying: {case_name}")

    raise SystemExit(
        f"Glaze UI 1.5 Candidate rendered acceptance failed for {case_name} "
        f"after {RENDER_ATTEMPTS} attempts:\n{last_failure}"
    )


def main() -> None:
    browser = find_browser()
    with serve_root() as port:
        # Representative supported form-factor evidence in both appearances.
        for width, height in (
            (390, 844),
            (820, 1180),
            (1280, 900),
            (1920, 1080),
        ):
            for theme in ("light", "dark"):
                run_candidate_case(
                    browser,
                    port,
                    width=width,
                    height=height,
                    theme=theme,
                )

        # Accessibility and performance degradation are independent gates.
        run_candidate_case(
            browser,
            port,
            width=390,
            height=844,
            theme="light",
            mode="reduced-motion",
        )
        run_candidate_case(
            browser,
            port,
            width=390,
            height=844,
            theme="light",
            mode="reduced-transparency",
        )
        run_candidate_case(
            browser,
            port,
            width=1280,
            height=900,
            theme="dark",
            mode="reduced-transparency",
        )
        run_candidate_case(
            browser,
            port,
            width=1280,
            height=900,
            theme="dark",
            mode="performance-constrained",
        )

    print("Glaze UI 1.5 Candidate rendered motion/material acceptance passed")


if __name__ == "__main__":
    main()
