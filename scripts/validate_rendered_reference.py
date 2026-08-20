#!/usr/bin/env python3
"""Run rendered acceptance checks for the canonical Glaze UI reference."""

from __future__ import annotations

import contextlib
import http.server
import shutil
import socket
import subprocess
import tempfile
import threading
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RENDER_ATTEMPTS = 2
RENDER_TIMEOUT_SECONDS = 40


def find_browser() -> str:
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        path = shutil.which(name)
        if path:
            return path
    raise SystemExit("Rendered acceptance failed: no supported Chromium-family browser found")


@contextlib.contextmanager
def serve_root():
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *_args):
            pass

    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]

    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), QuietHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    old_cwd = Path.cwd()
    try:
        # SimpleHTTPRequestHandler serves from the process working directory.
        import os

        os.chdir(ROOT)
        thread.start()
        yield port
    finally:
        server.shutdown()
        thread.join(timeout=5)
        os.chdir(old_cwd)


def browser_command(
    browser: str,
    url: str,
    profile_dir: str,
    *,
    width: int,
    height: int,
    mode: str,
) -> list[str]:
    command = [
        browser,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--disable-background-networking",
        "--disable-default-apps",
        "--disable-extensions",
        "--disable-sync",
        "--hide-scrollbars",
        "--mute-audio",
        "--no-first-run",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=3000",
        f"--user-data-dir={profile_dir}",
        f"--window-size={width},{height}",
    ]
    if mode == "reduced-motion":
        command.append("--force-prefers-reduced-motion")
    elif mode == "forced-colors":
        command.append("--force-high-contrast")
    command.extend(["--dump-dom", url])
    return command


def run_case(browser: str, port: int, *, width: int, height: int, theme: str, mode: str = "normal") -> None:
    query = urllib.parse.urlencode({"width": width, "height": height, "theme": theme, "mode": mode})
    url = f"http://127.0.0.1:{port}/reference/acceptance.html?{query}"
    case_name = f"{width}x{height} {theme} {mode}"
    last_failure = "browser did not produce a result"

    for attempt in range(1, RENDER_ATTEMPTS + 1):
        with tempfile.TemporaryDirectory(prefix="glaze-render-") as profile_dir:
            command = browser_command(
                browser,
                url,
                profile_dir,
                width=width,
                height=height,
                mode=mode,
            )
            try:
                completed = subprocess.run(
                    command,
                    cwd=ROOT,
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=RENDER_TIMEOUT_SECONDS,
                )
            except subprocess.TimeoutExpired as exc:
                stdout = exc.stdout.decode(errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
                stderr = exc.stderr.decode(errors="replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
                last_failure = (
                    f"attempt {attempt} timed out after {RENDER_TIMEOUT_SECONDS}s\n"
                    f"{(stdout or stderr)[-2000:]}"
                )
                if attempt < RENDER_ATTEMPTS:
                    print(f"Rendered acceptance retrying after transient timeout: {case_name}")
                    continue
                break

        output = completed.stdout
        if completed.returncode != 0:
            last_failure = (
                f"attempt {attempt} browser exited {completed.returncode}\n"
                f"{completed.stderr[-2000:]}"
            )
        elif 'data-status="pass"' in output and "PASS" in output:
            print(f"Rendered acceptance passed: {case_name}")
            return
        else:
            marker = output[-4000:] if output else completed.stderr[-4000:]
            last_failure = f"attempt {attempt} did not reach the PASS state\n{marker}"

        if attempt < RENDER_ATTEMPTS:
            print(f"Rendered acceptance retrying after incomplete browser result: {case_name}")

    raise SystemExit(f"Rendered acceptance failed for {case_name} after {RENDER_ATTEMPTS} attempts:\n{last_failure}")


def main() -> None:
    browser = find_browser()
    with serve_root() as port:
        for width, height in ((390, 844), (1280, 900)):
            for theme in ("light", "dark"):
                run_case(browser, port, width=width, height=height, theme=theme)
        run_case(browser, port, width=390, height=844, theme="light", mode="reduced-motion")
        run_case(browser, port, width=390, height=844, theme="light", mode="forced-colors")
    print("Glaze UI rendered reference acceptance passed")


if __name__ == "__main__":
    main()
