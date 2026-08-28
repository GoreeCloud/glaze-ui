#!/usr/bin/env python3
"""Run Glaze UI 2.0 Candidate resilience acceptance."""

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


def run_resilience_case(
    browser: str,
    port: int,
    *,
    test_case: str,
    width: int,
    height: int,
    appearance: str,
    force_prefers_contrast: bool = False,
) -> None:
    base_params = {
        "case": test_case,
        "width": width,
        "height": height,
        "appearance": appearance,
    }
    case_name = f"candidate20-resilience {test_case} {width}x{height} {appearance}"
    last_failure = "browser did not produce a result"

    for attempt in range(1, RENDER_ATTEMPTS + 1):
        query = urllib.parse.urlencode({**base_params, "attempt": attempt})
        url = f"http://127.0.0.1:{port}/reference/candidate-2.0-resilience-acceptance.html?{query}"
        with tempfile.TemporaryDirectory(prefix="glaze-candidate20-resilience-") as profile_dir:
            command = browser_command(
                browser,
                url,
                profile_dir,
                width=width,
                height=height,
                mode="normal",
            )
            if force_prefers_contrast:
                # Chromium ignores unknown command-line switches. The rendered
                # harness therefore also requires matchMedia() and computed-style
                # evidence so this cannot create a false acceptance claim.
                command.insert(-2, "--force-prefers-contrast=more")
            try:
                completed = run_browser(command)
            except Exception as exc:
                last_failure = f"attempt {attempt} browser execution failed: {exc}"
                if attempt < RENDER_ATTEMPTS:
                    print(f"Glaze UI 2.0 resilience acceptance retrying: {case_name}")
                    continue
                break

        status, result_text = acceptance_result(completed.stdout)
        if completed.returncode != 0:
            last_failure = (
                f"attempt {attempt} browser exited {completed.returncode}\n"
                f"{completed.stderr[-2000:]}"
            )
        elif status == "pass" and result_text and result_text.startswith("PASS"):
            print(f"Glaze UI 2.0 resilience acceptance passed: {case_name}")
            return
        elif status == "fail":
            raise SystemExit(
                f"Glaze UI 2.0 resilience acceptance failed for {case_name}:\n"
                f"attempt {attempt} harness reported FAIL\n{result_text or '(no result text)'}"
            )
        else:
            marker = completed.stdout[-4000:] if completed.stdout else completed.stderr[-4000:]
            last_failure = (
                f"attempt {attempt} did not reach PASS (status={status or 'missing'})\n"
                f"{result_text or marker}"
            )

        if attempt < RENDER_ATTEMPTS:
            print(f"Glaze UI 2.0 resilience acceptance retrying: {case_name}")

    raise SystemExit(
        f"Glaze UI 2.0 resilience acceptance failed for {case_name} after {RENDER_ATTEMPTS} attempts:\n"
        f"{last_failure}"
    )


def main() -> None:
    browser = find_browser()
    with serve_root() as port:
        run_resilience_case(
            browser,
            port,
            test_case="fallback",
            width=1280,
            height=900,
            appearance="light",
        )
        run_resilience_case(
            browser,
            port,
            test_case="foldable",
            width=1114,
            height=834,
            appearance="dark",
        )
        run_resilience_case(
            browser,
            port,
            test_case="contrast",
            width=1280,
            height=900,
            appearance="light",
            force_prefers_contrast=True,
        )

    print("Glaze UI 2.0 Candidate resilience acceptance passed")


if __name__ == "__main__":
    main()
