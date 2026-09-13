#!/usr/bin/env python3
"""Validate the frozen V1.2 Candidate source layer as historical Stable provenance.

V1.2 Stable intentionally froze implementation developed under Candidate-suffixed
source paths. The legacy validator still contains valuable deep source assertions,
but it encoded a global release state that no longer applies after V1.3/V1.4.
This harness protects the historical V1.2 Stable record and then runs the legacy
source validator against an in-memory historical lifecycle projection only.
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


def validate_historical_stable_lifecycle(lifecycle: dict) -> None:
    release = next(
        (
            item
            for item in lifecycle.get("releases", [])
            if isinstance(item, dict) and item.get("version") == "1.2.0"
        ),
        None,
    )
    req(release is not None, "Stable V1.2 lifecycle record missing")
    assert release is not None
    req(release.get("status") == "stable", "V1.2 lifecycle status must remain Stable")
    req(release.get("consumerEligible") is True, "V1.2 Stable must remain consumer-adoptable as a historical release")
    req(release.get("stableBaseline") == "1.1.0", "V1.2 Stable baseline must remain V1.1")
    req(release.get("contract") == "GLAZE_UI_V1_2.md", "V1.2 Stable contract binding drifted")
    req(release.get("webEntrypoint") == "css/glaze-v1.2.0.css", "V1.2 Stable web entrypoint drifted")
    req(release.get("runtimeEntrypoint") == "js/glaze-v1.2.0.mjs", "V1.2 Stable runtime entrypoint drifted")
    req(lifecycle.get("activeCandidate") != "1.2.0-candidate", "V1.2 must not return as an active Candidate")


def historical_candidate_projection(lifecycle: dict) -> dict:
    """Return the historical lifecycle fixture required by the legacy deep validator."""
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
    validate_historical_stable_lifecycle(lifecycle)
    run_legacy_source_validation(historical_candidate_projection(lifecycle))
    print("GLAZE UI V1.2 promoted Candidate source validation: PASS")
    print("Authority: V1.2 is preserved historical Stable provenance; Candidate-era lifecycle fields exist only in the in-memory test fixture.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
