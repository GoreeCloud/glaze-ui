#!/usr/bin/env python3
"""Validate the bounded GLAZE UI V1.1.1 import-closure patch candidate."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from validate_css_import_closure import CSS_ROOT, ENTRYPOINT, validate_import_closure

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts/v1.1/patch-1.1.1-candidate.json"
COMPONENTS = ROOT / "css/glaze-v1.components.css"
V1_ENTRY = ROOT / "css/glaze-v1.0.0.css"
LIFECYCLE = ROOT / "registry/lifecycle.json"


def main() -> int:
    errors: list[str] = []

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    lifecycle = json.loads(LIFECYCLE.read_text(encoding="utf-8"))
    components = COMPONENTS.read_text(encoding="utf-8")
    entry = V1_ENTRY.read_text(encoding="utf-8")

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    require(contract.get("candidateVersion") == "1.1.1-rc.1", "patch candidate must be 1.1.1-rc.1")
    require(contract.get("intendedStableVersion") == "1.1.1", "intended patch Stable version must be 1.1.1")
    require(contract.get("baseStableVersion") == "1.1.0", "patch must remain based on Stable 1.1.0")
    require(contract.get("baseStableRevision") == "15cc76d2bcd4065552dc31c77145b63f34d9e7b2", "base Stable revision drifted")
    require(contract.get("currentAuthorityUnchanged") is True, "patch preparation must not claim current authority changed")
    require(lifecycle.get("currentStable") == "1.1.0", "current Stable must remain 1.1.0 during patch preparation")
    require(lifecycle.get("currentOfficial") == "1.1.0", "current official version must remain 1.1.0 during patch preparation")
    require('@import url("./glaze-v1.candidate.css")' not in components, "stale Candidate dependency remains")

    foundation = '@import url("./glaze-v1.foundation.css");'
    component = '@import url("./glaze-v1.components.css");'
    require(foundation in entry and component in entry, "official V1 entrypoint must load foundation and components")
    if foundation in entry and component in entry:
        require(entry.index(foundation) < entry.index(component), "foundation must load before components")

    closure_errors, visited = validate_import_closure(ENTRYPOINT, CSS_ROOT)
    errors.extend(closure_errors)
    require(len(visited) >= 3, "Stable web graph closure unexpectedly small")

    if errors:
        print("GLAZE UI V1.1.1 patch-candidate validation FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("GLAZE UI V1.1.1 patch candidate: PASS")
    print("Boundary: current Stable authority remains immutable 1.1.0 until separate patch release finalization.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
