#!/usr/bin/env python3
"""Fail-closed Glaze UI 2.1 -> 2.2 migration compatibility validation.

Passing proves that the Candidate migration assessment is internally aligned
with the current 2.1 Stable boundary and implemented 2.2 Candidate contracts.
It does not make 2.2 consumer eligible or establish Stable promotion.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / "contracts" / "migration" / "glaze-2.1-to-2.2.json"
DOC = ROOT / "MIGRATION_2_1_TO_2_2.md"
TOKENS = ROOT / "tokens" / "glaze-2.2.candidate.json"
COMPONENTS = ROOT / "contracts" / "components" / "2.2"
ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        fail(f"top-level JSON must be an object: {path.relative_to(ROOT)}")
        return {}
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> None:
    version_file = ROOT / "VERSION"
    require(version_file.is_file(), "VERSION is missing")
    if version_file.is_file():
        require(version_file.read_text(encoding="utf-8").strip() == "2.1.0", "Candidate migration must keep VERSION at Stable 2.1.0")

    migration = read_json(MIGRATION)
    tokens = read_json(TOKENS)
    require(DOC.is_file(), "MIGRATION_2_1_TO_2_2.md is missing")
    doc = DOC.read_text(encoding="utf-8") if DOC.is_file() else ""

    require(migration.get("schemaVersion") == 1, "migration schemaVersion must be 1")
    require(migration.get("sourceVersion") == "2.1.0", "migration sourceVersion must be 2.1.0")
    require(migration.get("targetVersion") == "2.2.0-candidate.1", "migration targetVersion must be 2.2.0-candidate.1")
    require(migration.get("targetLifecycle") == "candidate", "migration targetLifecycle must remain Candidate")
    require(migration.get("targetConsumerEligible") is False, "2.2 Candidate migration target must not be consumer eligible")
    require(migration.get("productionMigrationAuthorized") is False, "production migration must remain unauthorized while 2.2 is Candidate")
    require(migration.get("stableRollbackVersion") == "2.1.0", "Stable rollback version must remain 2.1.0")
    require(migration.get("classification") == "additive-semantic-refinement-with-explicit-adoption-work", "migration compatibility classification drifted")
    require(migration.get("stableWebEntrypointDuringCandidate") == "css/glaze-2.1.0.css", "Stable web entrypoint must remain 2.1.0 during Candidate")
    require(migration.get("candidateImplementationEntrypointsAreProductionAliases") is False, "Candidate implementation filenames must not become production aliases")

    catalog = migration.get("componentCatalog", {})
    require(catalog == {"foundation": 8, "structure": 8, "overlay": 6, "signature": 5, "intelligence": 5, "total": 32}, "migration component catalog counts drifted")
    actual_contracts = sorted(COMPONENTS.glob("glz-*.json")) if COMPONENTS.is_dir() else []
    require(len(actual_contracts) == 32, f"2.2 component catalog must contain exactly 32 contracts, found {len(actual_contracts)}")

    expected_hierarchy = ["workspace", "application", "system-overlay", "system-panel", "critical-system"]
    require(migration.get("systemSurfaceHierarchy") == expected_hierarchy, "migration System Shell hierarchy drifted")
    require(tokens.get("surface", {}).get("systemHierarchy") == expected_hierarchy, "2.2 tokens disagree with migration System Shell hierarchy")

    expected_priority = ["disabled", "error", "pressed", "focus", "selected", "hover", "rest"]
    require(migration.get("statePriority") == expected_priority, "migration state priority drifted")
    require(tokens.get("interaction", {}).get("statePriority") == expected_priority, "2.2 tokens disagree with migration state priority")

    budget = migration.get("systemGlazeBudget", {})
    token_budget = tokens.get("system", {}).get("shellGlazeBudget", {})
    require(budget.get("dominantPanelsMax") == 1, "migration must preserve one dominant Glaze panel maximum")
    require(budget.get("smallFloatingControlsMax") == 3, "migration must preserve three small floating Glaze control maximum")
    require(budget.get("exceptionRequiresExplicitContext") is True, "migration Glaze budget exceptions must require explicit context")
    require(budget.get("nestedBackdropBlurAllowed") is False, "migration must prohibit nested backdrop blur")
    require(token_budget.get("dominantPanelsMax") == 1 and token_budget.get("smallFloatingControlsMax") == 3, "2.2 token Glaze budget disagrees with migration contract")

    search = migration.get("universalSearch", {})
    for key in (
        "immediateQueryFocus",
        "deterministicResultsBeforeGeneratedInterpretation",
        "keyboardTraversal",
        "generatedSourceProvenanceRequiredWhenAvailable",
        "destructiveActionRequiresSecondExplicitActivation",
        "escapeCancelsConfirmationBeforeClose",
        "focusRestoration",
    ):
        require(search.get(key) is True, f"Universal Search migration requirement missing: {key}")

    control = migration.get("controlCenter", {})
    for key in ("programmaticToggleState", "nativeRangeValues", "exclusiveDominantPanelWithSearch", "focusRestoration"):
        require(control.get(key) is True, f"Control Center migration requirement missing: {key}")

    required_revalidation = {
        "keyboard",
        "pointer",
        "touch",
        "large-text-200-percent",
        "rtl-and-localization-expansion",
        "reduced-motion",
        "reduced-transparency",
        "increased-contrast",
        "forced-colors",
        "touch-assistance",
        "performance-and-effect-fallbacks",
        "native-platform-acceptance-where-applicable",
        "human-visual-excellence",
    }
    require(required_revalidation.issubset(set(migration.get("requiredConsumerRevalidation", []))), "consumer revalidation matrix is incomplete")

    for marker in (
        "Current Stable: **2.1.0**",
        "Target under review: **2.2.0-candidate.1**",
        "Production migration authorized: **No**",
        "32-component Candidate catalog",
        "one dominant Glaze panel",
        "Universal Search",
        "Control Center",
        "Generated interpretation must remain distinct from retrieved source content.",
        "remain on Glaze UI 2.1.0 Stable",
        "does not establish that:\n\n- Glaze UI 2.2 is Stable",
    ):
        require(marker in doc, f"migration documentation missing required marker: {marker}")

    if ERRORS:
        print("Glaze UI 2.1 -> 2.2 migration validation failed:")
        for error in ERRORS:
            print(f"- {error}")
        raise SystemExit(1)

    print("Glaze UI 2.1 -> 2.2 migration compatibility validation passed (Candidate remains non-consumer-eligible)")


if __name__ == "__main__":
    main()
