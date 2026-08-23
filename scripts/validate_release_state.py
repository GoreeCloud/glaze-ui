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


def human_list(values: list[str]) -> str:
    if len(values) == 1:
        return values[0]
    if len(values) == 2:
        return f"{values[0]} and {values[1]}"
    return f"{', '.join(values[:-1])}, and {values[-1]}"


def main() -> None:
    require(re.fullmatch(r"\d+\.\d+\.\d+", VERSION) is not None, "VERSION must use semantic versioning")

    tokens = json.loads(text("tokens/glaze.tokens.json"))
    require(tokens["meta"]["version"] == VERSION, "token metadata does not match VERSION")

    registry = json.loads(text("consumers/registry.json"))
    supported_versions = registry.get("supportedStableVersions")
    require(isinstance(supported_versions, list) and supported_versions, "consumer registry supported Stable set is missing")
    require(all(isinstance(version, str) and re.fullmatch(r"\d+\.\d+\.\d+", version) for version in supported_versions), "consumer registry supported Stable set contains an invalid version")
    require(VERSION in supported_versions, "current Stable VERSION is absent from supported consumer targets")
    supported_text = human_list(supported_versions)

    readme = text("README.md")
    stability = text("STABILITY.md")
    security = text("SECURITY.md")
    identity = text("IDENTITY.md")
    component_status = text("COMPONENT_STATUS.md")
    component_contract = text("COMPONENTS.md")
    conformance = text("CONFORMANCE.md")
    acceptance = text("ACCEPTANCE.md")
    contributing = text("CONTRIBUTING.md")
    changelog = text("CHANGELOG.md")

    stable_family = VERSION.rsplit(".", 1)[0]

    require(f"Glaze UI {VERSION} is the current Stable canonical baseline" in readme, "README current-Stable declaration is missing or stale")
    require(f"**Stable baseline:** Glaze UI **{VERSION}**" in stability, "STABILITY.md Stable baseline is missing or stale")
    require(f"Glaze UI {stable_family} Stable" in component_status, "COMPONENT_STATUS.md current Stable release family is missing")
    require(component_contract.startswith(f"# Glaze UI {stable_family} Component Contract\n"), "COMPONENTS.md heading does not match the current Stable release family")
    require(
        f"Glaze UI {stable_family} retains the Stable component semantics established in Glaze UI 1.3" in component_contract,
        "COMPONENTS.md does not preserve the 1.3-to-current component compatibility boundary",
    )
    require(VERSION in changelog, "CHANGELOG.md does not mention the current VERSION")

    current_stable_pattern = re.compile(r"current Stable(?: canonical)? baseline[^\n]*?Glaze UI\s+(\d+\.\d+\.\d+)", re.IGNORECASE)
    for path in ("README.md", "STABILITY.md", "COMPONENT_STATUS.md", "CONFORMANCE.md", "ADOPTION.md", "ACCEPTANCE.md"):
        body = text(path)
        for match in current_stable_pattern.finditer(body):
            require(match.group(1) == VERSION, f"{path} declares stale current Stable version {match.group(1)}")

    stable_surface_hierarchy = "Canvas/Solid/Raised/Functional Glass/Clear Glass/Overlay hierarchy"
    require(stable_surface_hierarchy in acceptance, "ACCEPTANCE.md does not use the current Stable material hierarchy")
    require(
        "Canvas, Solid, Raised, Functional Glass, Clear Glass, and Overlay" in conformance,
        "CONFORMANCE.md does not use the current Stable material hierarchy",
    )
    require(
        "Canvas/Solid/Raised/Glaze/Overlay hierarchy" not in acceptance,
        "ACCEPTANCE.md still contains the superseded generic Glaze material hierarchy",
    )

    require("## Version-specific conformance claims" in conformance, "CONFORMANCE.md version-specific conformance section is missing")
    require(
        f"supported Stable conformance targets are **{supported_text}**" in conformance,
        "CONFORMANCE.md supported conformance target set differs from consumers/registry.json",
    )
    require(
        f"Glaze UI **{VERSION}** is the current Stable baseline" in conformance,
        "CONFORMANCE.md current Stable conformance baseline is missing or stale",
    )
    require("exact-version claim" in conformance, "CONFORMANCE.md older-Stable exact-version claim boundary is missing")
    require("Requirements introduced only by a later Stable release are not retroactively implied" in conformance, "CONFORMANCE.md must reject retroactive newer-release requirements")
    require("does not mean the consumer is aligned to the current Stable baseline" in conformance, "CONFORMANCE.md must distinguish older-version conformance from current-Stable alignment")
    require("does not trigger automatic migration" in conformance, "CONFORMANCE.md controlled migration boundary is missing")
    require("`SECURITY.md` governs maintenance applicability" in conformance, "CONFORMANCE.md maintenance boundary is missing")

    require("current Stable canonical baseline" in readme, "README must use the canonical current-Stable wording")
    require("## Supported Stable consumer targets" in readme, "README supported-consumer-target section is missing")
    require(
        f"supported Stable consumer-target set is **{supported_text}**" in readme,
        "README supported consumer-target set differs from consumers/registry.json",
    )
    require("Compatibility support means a consumer may remain intentionally pinned" in readme, "README compatibility-support meaning is missing")
    require("Existing consumers are never automatically upgraded" in readme, "README controlled consumer-migration boundary is missing")
    require("`SECURITY.md` governs active security-fix and maintenance applicability" in readme, "README security-maintenance boundary is missing")
    require("## Glaze UI 1.3 compatibility" not in readme, "README still uses the superseded single-version compatibility section")

    require("Stable consumers are never migrated automatically" in stability, "controlled consumer-migration boundary is missing")
    require("No active 1.4 form-factor capability remains Candidate" in component_status, "1.4 lifecycle reconciliation is incomplete")

    require("current Stable Glaze UI baseline" in security, "SECURITY.md must bind fixes to the current Stable baseline")
    require("explicitly supported consumer target" in security, "SECURITY.md must preserve version-specific older-Stable support")
    require("shared major-version number alone does not guarantee active maintenance" in security, "SECURITY.md must reject major-version-wide maintenance promises")
    require("current Glaze UI major version" not in security, "SECURITY.md still contains the superseded broad major-version support promise")

    require(
        f"Glaze UI {VERSION} is the current Stable GoreeCloud design-system baseline" in identity,
        "IDENTITY.md current-Stable declaration is missing or stale",
    )
    require("Status: **Pending approved canonical artwork**" in identity, "IDENTITY.md must preserve the unresolved artwork status")
    require(
        "No icon, logo, favicon, or product mark is approved as canonical Glaze UI artwork at this time" in identity,
        "IDENTITY.md must preserve the no-canonical-artwork boundary",
    )
    require(
        "Glaze UI 1.3.0 is the stable GoreeCloud design system" not in identity,
        "IDENTITY.md still advertises the superseded 1.3 Stable baseline",
    )

    required_stable_commands = (
        "python3 scripts/validate_glaze_ui.py",
        "python3 scripts/validate_release_state.py",
        "python3 scripts/validate_form_factors.py",
        "python3 scripts/validate_typography_contract.py",
        "python3 scripts/validate_consumer_registry.py",
        "python3 integrations/firefox/validate.py",
        "python3 website/validate.py",
        "python3 scripts/validate_rendered_reference.py",
    )
    for command in required_stable_commands:
        require(command in readme, f"README.md omits Stable validation command: {command}")
        require(command in contributing, f"CONTRIBUTING.md omits Stable validation command: {command}")

    require("exact candidate revision" in readme, "README.md must preserve exact-candidate validation guidance")
    for profile in ("Mobile — 390 × 844", "Tablet — 820 × 1180", "Desktop — 1280 × 900", "Wide Desktop — 1600 × 1000", "TV — 1920 × 1080"):
        require(profile in contributing, f"CONTRIBUTING.md omits Stable acceptance profile: {profile}")
    require("exact PR head" in contributing, "CONTRIBUTING.md must preserve exact-head validation guidance")

    print(f"Glaze UI release-state validation passed for {VERSION}")


if __name__ == "__main__":
    main()
