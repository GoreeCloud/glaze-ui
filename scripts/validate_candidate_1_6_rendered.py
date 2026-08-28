#!/usr/bin/env python3
"""Run rendered acceptance for the Glaze UI 1.6 Candidate adaptive workspace."""

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
    theme: str,
    form_factor: str,
    mode: str = "normal",
    density: str = "comfortable",
) -> None:
    query = urllib.parse.urlencode(
        {
            "width": width,
            "height": height,
            "theme": theme,
            "mode": mode,
            "density": density,
            "formFactor": form_factor,
        }
    )
    url = f"http://127.0.0.1:{port}/reference/candidate-1.6-workspace-acceptance.html?{query}"
    case_name = f"candidate16-workspace {form_factor} {width}x{height} {theme} {mode} {density}"
    last_failure = "browser did not produce a result"
    attempts = TV_FORCED_COLORS_ATTEMPTS if form_factor == "tv" and mode == "forced-colors" else RENDER_ATTEMPTS

    for attempt in range(1, attempts + 1):
        with tempfile.TemporaryDirectory(prefix="glaze-candidate16-workspace-render-") as profile_dir:
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
                    print(f"Glaze UI 1.6 workspace rendered acceptance retrying: {case_name}")
                    continue
                break

        status, result_text = acceptance_result(completed.stdout)
        if completed.returncode != 0:
            last_failure = (
                f"attempt {attempt} browser exited {completed.returncode}\n"
                f"{completed.stderr[-2000:]}"
            )
        elif status == "pass" and result_text and result_text.startswith("PASS"):
            print(f"Glaze UI 1.6 workspace rendered acceptance passed: {case_name}")
            return
        elif status == "fail":
            last_failure = f"attempt {attempt} harness reported FAIL\n{result_text or '(no result text)'}"
        else:
            marker = completed.stdout[-4000:] if completed.stdout else completed.stderr[-4000:]
            last_failure = (
                f"attempt {attempt} did not reach PASS (status={status or 'missing'})\n"
                f"{result_text or marker}"
            )

        if attempt < attempts:
            print(f"Glaze UI 1.6 workspace rendered acceptance retrying: {case_name}")

    raise SystemExit(
        f"Glaze UI 1.6 Candidate workspace rendered acceptance failed for {case_name} "
        f"after {attempts} attempts:\n{last_failure}"
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
        for width, height, form_factor in representative:
            for theme in ("light", "dark"):
                run_candidate_case(
                    browser,
                    port,
                    width=width,
                    height=height,
                    theme=theme,
                    form_factor=form_factor,
                )

        run_candidate_case(
            browser,
            port,
            width=1280,
            height=900,
            theme="light",
            form_factor="desktop",
            density="compact",
        )
        run_candidate_case(
            browser,
            port,
            width=390,
            height=844,
            theme="dark",
            form_factor="mobile",
            density="spacious",
        )
        run_candidate_case(
            browser,
            port,
            width=390,
            height=844,
            theme="light",
            form_factor="mobile",
            mode="reduced-motion",
        )
        run_candidate_case(
            browser,
            port,
            width=390,
            height=844,
            theme="light",
            form_factor="mobile",
            mode="reduced-transparency",
        )
        run_candidate_case(
            browser,
            port,
            width=1280,
            height=900,
            theme="dark",
            form_factor="desktop",
            mode="reduced-transparency",
        )
        run_candidate_case(
            browser,
            port,
            width=1280,
            height=900,
            theme="dark",
            form_factor="desktop",
            mode="performance-constrained",
        )
        run_candidate_case(
            browser,
            port,
            width=1920,
            height=1080,
            theme="dark",
            form_factor="tv",
            mode="forced-colors",
        )

    print("Glaze UI 1.6 Candidate adaptive workspace rendered acceptance passed")


if __name__ == "__main__":
    main()
