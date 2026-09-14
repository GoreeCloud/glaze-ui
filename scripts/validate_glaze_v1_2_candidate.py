#!/usr/bin/env python3
"""Validate the frozen V1.2 Candidate source layer as historical promoted-source provenance.

V1.2 Stable froze implementation that had been developed under Candidate-suffixed source
paths. The legacy validator contains useful deep assertions for those frozen sources, but it
also encoded Candidate-era global lifecycle state. Later Glaze releases must not make those
source regressions fail merely because current lifecycle authority has advanced.

This harness therefore validates the preserved V1.2 Stable release record, then runs the
legacy source validator against an in-memory historical Candidate lifecycle projection. The
projection exists only to exercise the unchanged deep V1.2 source assertions; it is never
written as repository evidence and never becomes current lifecycle authority.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY_PATH = ROOT / "scripts/validate_glaze_v1_2_candidate_legacy.py"
LIFECYCLE_PATH = ROOT / "registry/lifecycle.json"


def req(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"GLAZE UI V1.2 promoted-source validation failed: {message}")


def load_json(path: Path) -> dict:
    req(path.is_file(), f"missing required file: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    req(isinstance(data, dict), f"expected JSON object: {path.relative_to(ROOT)}")
    return data


def validate_preserved_v1_2_release(lifecycle: dict) -> None:
    """Protect V1.2 release provenance without claiming that V1.2 is still current."""
    current_version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    req(bool(current_version), "current VERSION authority must remain present")
    req(lifecycle.get("currentStable") == current_version, "currentStable must remain internally consistent with VERSION")
    req(lifecycle.get("currentOfficial") == current_version, "currentOfficial must remain internally consistent with VERSION")

    release = next(
        (
            item
            for item in lifecycle.get("releases", [])
            if isinstance(item, dict) and item.get("version") == "1.2.0"
        ),
        None,
    )
    req(release is not None, "historical Stable V1.2 lifecycle record missing")
    assert release is not None
    req(release.get("label") == "GLAZE UI V1.2 — Living Frosted", "historical V1.2 product label drifted")
    req(release.get("status") == "stable", "historical V1.2 lifecycle status must remain Stable")
    req(release.get("consumerEligible") is True, "historical V1.2 release must preserve original consumer eligibility")
    req(release.get("stableBaseline") == "1.1.0", "historical V1.2 Stable baseline must remain V1.1")
    req(release.get("contract") == "GLAZE_UI_V1_2.md", "historical V1.2 Stable contract binding drifted")
    req(release.get("webEntrypoint") == "css/glaze-v1.2.0.css", "historical V1.2 web entrypoint drifted")
    req(release.get("runtimeEntrypoint") == "js/glaze-v1.2.0.mjs", "historical V1.2 runtime entrypoint drifted")


def historical_candidate_projection(lifecycle: dict) -> dict:
    """Return the minimum historical lifecycle fixture required by the legacy validator."""
    projected = copy.deepcopy(lifecycle)
    projected["officialProductLabel"] = "GLAZE UI V1.1"
    projected["currentStable"] = "1.1.0"
    projected["currentOfficial"] = "1.1.0"
    projected["activeCandidate"] = "1.2.0-candidate"

    releases = [
        item
        for item in projected.get("releases", [])
        if not (isinstance(item, dict) and item.get("version") == "1.2.0-candidate")
    ]
    releases.append(
        {
            "version": "1.2.0-candidate",
            "label": "GLAZE UI V1.2 — Frosted Neutral Candidate",
            "status": "candidate",
            "consumerEligible": False,
            "stableBaseline": "1.1.0",
            "contract": "GLAZE_UI_V1_2_CANDIDATE.md",
        }
    )
    projected["releases"] = releases

    capabilities = projected.setdefault("capabilities", {})
    shell = copy.deepcopy(capabilities.get("frosted-neutral-system-shell", {}))
    shell["status"] = "candidate"
    shell["since"] = "1.2.0-candidate"
    shell["implementation"] = "contracts/v1.2/system-shell-materials.candidate.json"
    shell["webPreview"] = "reference/v1.2/system-shell.html"
    capabilities["frosted-neutral-system-shell"] = shell
    return projected


def run_legacy_source_validation(projected_lifecycle: dict) -> None:
    req(LEGACY_PATH.is_file(), "historical Candidate source validator is missing")
    spec = importlib.util.spec_from_file_location("glaze_v1_2_candidate_legacy", LEGACY_PATH)
    req(spec is not None and spec.loader is not None, "could not load historical Candidate source validator")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # The legacy helper deliberately rejects paths outside ROOT. Place the ephemeral
    # lifecycle fixture inside the checkout, then remove it automatically after validation.
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        suffix=".json",
        prefix=".glaze-v1.2-historical-lifecycle-",
        dir=ROOT,
    ) as handle:
        json.dump(projected_lifecycle, handle, indent=2)
        handle.flush()
        module.LIFECYCLE_PATH = Path(handle.name)
        module.main()


def main() -> int:
    lifecycle = load_json(LIFECYCLE_PATH)
    validate_preserved_v1_2_release(lifecycle)
    run_legacy_source_validation(historical_candidate_projection(lifecycle))
    current_version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    print("GLAZE UI V1.2 promoted Candidate source regression: PASS")
    print(f"Authority: V1.2 Candidate-era lifecycle is historical fixture data; current lifecycle remains {current_version}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
