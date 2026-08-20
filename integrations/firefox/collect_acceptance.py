#!/usr/bin/env python3
"""Create a privacy-preserving Firefox Glaze UI runtime acceptance record."""

from __future__ import annotations

import argparse
import hashlib
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
USERCHROME = ROOT / "userchrome" / "userChrome.css"
SCENARIOS = (
    "Light appearance",
    "Dark appearance",
    "Active and inactive tabs",
    "URL/search focus, typing, selection, and suggestions",
    "Identity and security indicators",
    "Navigation and toolbar actions",
    "Bookmarks toolbar",
    "Application menu and transient panels",
    "Sidebar",
    "Downloads",
    "Private browsing",
    "Certificate, permission, download, update, and warning indicators",
    "Keyboard-only navigation and visible focus",
    "Increased contrast / forced colors where exposed by the platform",
    "Reduced motion",
    "200% zoom/reflow where applicable",
    "Theme removal rollback without profile-data loss",
    "userChrome.css removal rollback without profile-data loss",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_text(command: list[str]) -> str:
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError) as exc:
        return f"unavailable ({exc})"
    return (result.stdout or result.stderr).strip() or "unavailable"


def git_revision() -> str:
    return run_text(["git", "-C", str(ROOT), "rev-parse", "HEAD"])


def render(args: argparse.Namespace) -> str:
    package = args.theme_package.expanduser().resolve()
    if not package.is_file():
        raise SystemExit(f"Theme package not found: {package}")

    firefox_version = run_text([args.firefox_bin, "--version"])
    userchrome_digest = sha256(USERCHROME) if args.userchrome == "enabled" else "not enabled"
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    lines = [
        "# Firefox Glaze UI Runtime Acceptance Record",
        "",
        f"- Track: {args.track}",
        f"- Captured (UTC): {now}",
        f"- Firefox: {firefox_version}",
        f"- Operating system: {platform.platform()}",
        f"- Desktop/session: {args.desktop}",
        f"- Glaze UI repository revision: {git_revision()}",
        f"- Theme package: {package.name}",
        f"- Theme package SHA-256: {sha256(package)}",
        f"- userChrome.css: {args.userchrome}",
        f"- Canonical userChrome.css SHA-256: {userchrome_digest}",
        "",
        "## Scenario Results",
        "",
    ]
    lines.extend(f"- [ ] {scenario} — PASS / FAIL / N/A — Notes:" for scenario in SCENARIOS)
    lines.extend(
        [
            "",
            "## Failures and Corrections",
            "",
            "Record any defect, source correction, Firefox-version-specific exception, or fallback to the supported theme layer.",
            "",
            "## Final Decision",
            "",
            "- [ ] Accepted",
            "- [ ] Rejected",
            "- [ ] Accepted with documented material exception",
            "",
            "This record intentionally captures environment and package metadata only. It does not collect browsing history, bookmarks, credentials, cookies, open tabs, URLs, or Firefox profile contents.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--track", required=True, choices=("release", "esr"))
    parser.add_argument("--firefox-bin", default="firefox")
    parser.add_argument("--theme-package", required=True, type=Path)
    parser.add_argument("--userchrome", required=True, choices=("enabled", "disabled"))
    parser.add_argument("--desktop", default="unspecified", help="Desktop environment/session, for example KDE Plasma or GNOME")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    output = args.output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(args), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
