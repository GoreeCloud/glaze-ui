#!/usr/bin/env python3
"""Run Glaze UI 2.1 visual regression with bounded incomplete-render retries.

The target visual-regression implementation, manifest, reference pages, and pixel
thresholds all come from ``--source-root``. This runner only retries Chromium
captures that did not reach the target's explicit snapshot-ready state; it does
not retry or reinterpret pixel-comparison failures and cannot bless current
output as a baseline.
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_target(source_root: Path):
    scripts_dir = source_root / "scripts"
    target_path = scripts_dir / "glaze_2_1_visual_regression.py"
    if not target_path.is_file():
        raise SystemExit(f"visual regression target is missing: {target_path}")

    # The target imports its own rendered-reference helpers. Put that exact
    # source tree first so a pinned baseline is executed with its own harness.
    sys.path.insert(0, str(scripts_dir))
    spec = importlib.util.spec_from_file_location("glaze_2_1_visual_regression_target", target_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"unable to load visual regression target: {target_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("capture", "compare"))
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--baseline-dir")
    args = parser.parse_args()

    if args.mode == "compare" and not args.baseline_dir:
        raise SystemExit("compare mode requires --baseline-dir")

    source_root = (ROOT / args.source_root).resolve()
    target = load_target(source_root)
    support = sys.modules.get("validate_rendered_reference")
    attempts = int(getattr(support, "RENDER_ATTEMPTS", 5))
    attempts = max(1, attempts)

    original_capture_case = target.capture_case

    def capture_case_with_retry(browser, port, case, output):
        for attempt in range(1, attempts + 1):
            try:
                return original_capture_case(browser, port, case, output)
            except SystemExit as exc:
                message = str(exc)
                incomplete = "visual snapshot did not reach ready state" in message
                if not incomplete or attempt >= attempts:
                    raise
                print(
                    "Glaze UI 2.1 visual capture retrying after incomplete "
                    f"Chromium result: {case['id']} attempt {attempt}/{attempts}"
                )
        raise AssertionError("unreachable visual capture retry state")

    target.capture_case = capture_case_with_retry

    target_argv = [
        str(source_root / "scripts" / "glaze_2_1_visual_regression.py"),
        args.mode,
        "--output-dir",
        args.output_dir,
    ]
    if args.baseline_dir:
        target_argv.extend(["--baseline-dir", args.baseline_dir])

    previous_argv = sys.argv
    try:
        sys.argv = target_argv
        target.main()
    finally:
        sys.argv = previous_argv


if __name__ == "__main__":
    main()
