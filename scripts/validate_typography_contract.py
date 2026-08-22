#!/usr/bin/env python3
"""Validate the Glaze UI Stable typography source contract."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / "tokens" / "glaze.tokens.json"
TOKEN_README = ROOT / "tokens" / "README.md"


def fail(message: str) -> None:
    raise SystemExit(f"typography contract validation failed: {message}")


def main() -> None:
    data = json.loads(TOKENS.read_text(encoding="utf-8"))
    typography = data.get("typography")
    if not isinstance(typography, dict):
        fail("missing typography token group")

    family = typography.get("family")
    if not isinstance(family, str) or not family.strip():
        fail("typography.family must be a non-empty string")

    first_family = family.split(",", 1)[0].strip().strip("'\"").lower()
    if first_family not in {"system-ui", "ui-sans-serif"}:
        fail("canonical typography.family must be system/platform-native first")

    source_policy = typography.get("sourcePolicy")
    if not isinstance(source_policy, str):
        fail("typography.sourcePolicy is required")

    policy_lower = source_policy.lower()
    for phrase in ("system/platform-native", "locally bundled", "third-party runtime"):
        if phrase not in policy_lower:
            fail(f"typography.sourcePolicy must state {phrase!r}")

    forbidden_runtime_hosts = (
        "fonts.googleapis.com",
        "fonts.gstatic.com",
        "use.typekit.net",
        "fonts.adobe.com",
    )
    tracked_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and path.suffix.lower() in {".css", ".html", ".js", ".json", ".md", ".py", ".yml", ".yaml"}
    ).lower()
    for host in forbidden_runtime_hosts:
        if host in tracked_text:
            fail(f"forbidden third-party runtime font host referenced: {host}")

    readme = TOKEN_README.read_text(encoding="utf-8").lower()
    for phrase in ("system/platform-native first", "third-party runtime font-delivery service", "locally bundled open-source font"):
        if phrase not in readme:
            fail(f"tokens/README.md must document {phrase!r}")

    print("Glaze UI typography contract validation passed.")


if __name__ == "__main__":
    main()
