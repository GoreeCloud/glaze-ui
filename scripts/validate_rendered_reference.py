#!/usr/bin/env python3
"""Run rendered acceptance checks for the canonical Glaze UI reference."""

from __future__ import annotations

import contextlib
import http.server
import shutil
import socket
import subprocess
import threading
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


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


def run_case(browser: str, port: int, *, width: int, height: int, theme: str, mode: str = "normal") -> None:
    query = urllib.parse.urlencode({"width": width, "height": height, "theme": theme, "mode": mode})
    url = f"http://127.0.0.1:{port}/reference/acceptance.html?{query}"
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
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=3000",
        f"--window-size={width},{height}",
    ]
    if mode == "reduced-motion":
        command.append("--force-prefers-reduced-motion")
    elif mode == "forced-colors":
        command.append("--force-high-contrast")
    command.extend(["--dump-dom", url])

    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    output = completed.stdout
    if completed.returncode != 0:
        raise SystemExit(
            f"Rendered acceptance failed for {width}x{height} {theme} {mode}: "
            f"browser exited {completed.returncode}\n{completed.stderr[-2000:]}"
        )
    if 'data-status="pass"' not in output or "PASS" not in output:
        marker = output[-4000:] if output else completed.stderr[-4000:]
        raise SystemExit(
            f"Rendered acceptance failed for {width}x{height} {theme} {mode}:\n{marker}"
        )
    print(f"Rendered acceptance passed: {width}x{height} {theme} {mode}")


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
