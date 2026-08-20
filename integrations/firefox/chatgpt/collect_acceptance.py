#!/usr/bin/env python3
"""Generate a privacy-preserving runtime acceptance record for the ChatGPT Firefox extension."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "manifest.json"
CHECKS = [
    "Extension loads without extension-attributable manifest, CSP, or console errors.",
    "Toolbar popup opens and reflects stored state.",
    "Enable/disable behavior and local persistence work as documented.",
    "Comfortable/compact density stays synchronized between popup and preferences.",
    "Functional Glass and expressive-motion preferences stay synchronized.",
    "New-chat creation behaves normally.",
    "Existing conversation navigation behaves normally.",
    "Message composition, editing, submission, stop-generation, retry/regenerate, and edit workflows remain functional where available.",
    "File upload and attachment controls remain functional where available.",
    "Available tool, model, project, and workspace controls remain functional.",
    "Menus, dialogs, popovers, settings, code blocks, tables, citations, and copy controls remain usable.",
    "Disabling/removing the extension restores the original presentation without data loss.",
    "Light appearance is readable and preserves ChatGPT functionality.",
    "Dark appearance is readable and preserves ChatGPT functionality.",
    "No extension-introduced horizontal overflow appears at representative compact and expanded widths.",
    "Keyboard-only navigation and visible focus remain usable.",
    "Browser zoom/reflow remains usable at 200 percent.",
    "Reduced motion removes non-essential extension-authored motion.",
    "Increased contrast / forced colors remain legible where supported.",
    "Functional Glass disabled and no-backdrop-filter fallbacks remain readable.",
    "ChatGPT-provided accessible names and semantics remain intact.",
    "Extension permissions remain limited to storage and ChatGPT-only host access.",
    "No extension-authored network request is observed during normal operation.",
    "No ChatGPT conversation/account/session data is persisted by the extension.",
    "No analytics, telemetry, advertising, remote fonts, remote icons, or remote presentation dependency is loaded.",
    "Authentication and session handling are not modified by the extension.",
    "Current live ChatGPT interface was reviewed for selector/DOM drift.",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xpi", required=True, type=Path, help="Path to the exact XPI tested")
    parser.add_argument("--revision", required=True, help="Exact GoreeCloud/glaze-ui commit SHA")
    parser.add_argument("--firefox-version", required=True, help="Firefox version used for acceptance")
    parser.add_argument("--firefox-channel", required=True, choices=("release", "esr", "beta", "developer", "nightly"))
    parser.add_argument("--desktop", default="", help="Desktop environment, if applicable")
    parser.add_argument("--tester", default="", help="Tester name or local role; do not use an account identifier")
    parser.add_argument("--functional-glass", choices=("on", "off"), default="on")
    parser.add_argument("--expressive-motion", choices=("on", "off"), default="on")
    parser.add_argument("--output", required=True, type=Path, help="Markdown evidence output path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.xpi.is_file():
        raise SystemExit(f"XPI does not exist: {args.xpi}")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    now = datetime.now(timezone.utc).astimezone()
    lines = [
        "# Firefox ChatGPT Glaze UI Runtime Acceptance",
        "",
        "> Privacy boundary: this record intentionally excludes conversation text, prompts, responses, account identifiers, authentication material, cookies, session tokens, uploaded-file contents, URLs, browsing history, bookmarks, and Firefox profile databases.",
        "",
        "## Environment",
        "",
        f"- Repository revision: `{args.revision}`",
        f"- Extension version: `{manifest['version']}`",
        f"- Tested XPI: `{args.xpi.name}`",
        f"- XPI SHA-256: `{sha256(args.xpi)}`",
        f"- Firefox: `{args.firefox_version}` ({args.firefox_channel})",
        f"- Operating system: `{platform.system()} {platform.release()}`",
        f"- Machine architecture: `{platform.machine()}`",
        f"- Desktop environment: `{args.desktop or 'not recorded'}`",
        f"- Test date: `{now.isoformat(timespec='minutes')}`",
        f"- Tester: `{args.tester or 'not recorded'}`",
        f"- Functional Glass preference: `{args.functional_glass}`",
        f"- Expressive motion preference: `{args.expressive_motion}`",
        "",
        "## Required scenarios",
        "",
    ]
    lines.extend(f"- [ ] {check}" for check in CHECKS)
    lines.extend([
        "",
        "## DOM-drift notes",
        "",
        "Record only affected UI surface names and selector/compatibility observations. Do not paste conversation or account content.",
        "",
        "- None recorded.",
        "",
        "## Decision",
        "",
        "- [ ] PASS — all blocking scenarios passed.",
        "- [ ] FAIL — one or more blocking scenarios failed.",
        "",
        "Notes:",
        "",
        "- Add non-sensitive acceptance notes here.",
        "",
    ])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote privacy-preserving acceptance record: {args.output}")


if __name__ == "__main__":
    main()
