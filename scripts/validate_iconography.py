#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / "tokens" / "iconography.json"
DOC = ROOT / "ICONOGRAPHY.md"


def fail(message: str) -> None:
    raise SystemExit(f"iconography validation failed: {message}")


def main() -> None:
    if not TOKENS.is_file():
        fail("tokens/iconography.json is missing")
    if not DOC.is_file():
        fail("ICONOGRAPHY.md is missing")

    data = json.loads(TOKENS.read_text(encoding="utf-8"))
    if data.get("meta", {}).get("status") != "candidate":
        fail("iconography contract must remain Candidate until promotion")
    if data.get("meta", {}).get("stableBaseline") != "1.4.0":
        fail("Stable baseline must remain 1.4.0")
    if data.get("principle") != "recognizable identity within a shared visual language":
        fail("canonical iconography principle changed unexpectedly")

    required_classes = {"application", "service", "system", "functional", "semantic"}
    if set(data.get("classes", {})) != required_classes:
        fail("icon classes are incomplete or unexpected")
    if data["classes"]["application"].get("layers") != ["foundation", "identity", "detail"]:
        fail("application three-layer composition is required")
    if data["classes"]["service"].get("launchable") is not False:
        fail("service visual category must remain non-launchable")

    optical = data.get("opticalSizes", {})
    if list(optical) != ["presentation", "standard", "compact", "micro"]:
        fail("optical-size roles must be presentation, standard, compact, micro")
    sizes = [optical[k].get("minPx") for k in optical]
    if sizes != sorted(sizes, reverse=True):
        fail("optical-size minimums must descend from presentation to micro")

    required_semantics = {"success", "information", "warning", "danger", "privacy", "security", "protected", "restricted", "online", "offline", "syncing", "paused", "unavailable"}
    if set(data.get("semanticRoles", [])) != required_semantics:
        fail("semantic icon roles are incomplete")
    if data.get("authority", {}).get("privacy") != "Privacy Shield":
        fail("Privacy Shield must remain authoritative for privacy truth")
    if data.get("authority", {}).get("security") != "Wardveil Security":
        fail("Wardveil Security must remain authoritative for security truth")

    access = data.get("accessibility", {})
    for key in ["nonColorMeaningRequired", "accessibleNamesForInteractiveIcons", "grayscale", "highContrast", "reducedTransparency", "forcedColors", "reducedMotion"]:
        if access.get(key) is not True:
            fail(f"accessibility invariant {key} must be true")

    badges = data.get("badges", {})
    if badges.get("maxVisibleCompact") != 1:
        fail("compact badge stacking must remain bounded to one visible priority badge")
    if badges.get("overflowTreatment") != "expanded-labeled-status":
        fail("badge overflow must use an expanded labeled status treatment")
    if data.get("motion", {}).get("continuousDecorativeAnimation") is not False:
        fail("continuous decorative animation must remain prohibited")
    if data.get("thirdParty", {}).get("mustNotFalselyRebrand") is not True:
        fail("third-party identity protection is required")

    doc = DOC.read_text(encoding="utf-8")
    for phrase in [
        "recognizable identity within a shared visual language",
        "Privacy Shield is authoritative for privacy truth",
        "Wardveil Security is authoritative for security truth",
        "Responsive iconography is not simple asset scaling",
        "Candidate promotion boundary",
    ]:
        if phrase not in doc:
            fail(f"documentation invariant missing: {phrase}")

    print("Glaze UI iconography Candidate validation passed")


if __name__ == "__main__":
    main()
