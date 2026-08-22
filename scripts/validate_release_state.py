#!/usr/bin/env python3
"""Fail closed when Glaze UI release-state records drift from VERSION."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Glaze UI release-state validation failed: {message}")


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> None:
    require(re.fullmatch(r"\d+\.\d+\.\d+", VERSION) is not None, "VERSION must use semantic versioning")

    tokens = json.loads(text("tokens/glaze.tokens.json"))
    require(tokens["meta"]["version"] == VERSION, "token metadata does not match VERSION")

    readme = text("README.md")
    stability = text("STABILITY.md")
    components = text("COMPONENT_STATUS.md")
    changelog = text("CHANGELOG.md")

    require(f"Glaze UI {VERSION} is the current Stable canonical baseline" in readme, "README current-Stable declaration is missing or stale")
    require(f"**Stable baseline:** Glaze UI **{VERSION}**" in stability, "STABILITY.md Stable baseline is missing or stale")
    require(f"Glaze UI {VERSION.rsplit('.', 1)[0]} Stable" in components, "COMPONENT_STATUS.md current Stable release family is missing")
    require(VERSION in changelog, "CHANGELOG.md does not mention the current VERSION")

    current_stable_pattern = re.compile(r"current Stable(?: canonical)? baseline[^\n]*?Glaze UI\s+(\d+\.\d+\.\d+)", re.IGNORECASE)
    for path in ("README.md", "STABILITY.md", "COMPONENT_STATUS.md", "CONFORMANCE.md", "ADOPTION.md", "ACCEPTANCE.md"):
        body = text(path)
        for match in current_stable_pattern.finditer(body):
            require(match.group(1) == VERSION, f"{path} declares stale current Stable version {match.group(1)}")

    require("current Stable canonical baseline" in readme, "README must use the canonical current-Stable wording")
    require("Stable consumers are never migrated automatically" in stability, "controlled consumer-migration boundary is missing")
    require("No active 1.4 form-factor capability remains Candidate" in components, "1.4 lifecycle reconciliation is incomplete")

    print(f"Glaze UI release-state validation passed for {VERSION}")


if __name__ == "__main__":
    main()
