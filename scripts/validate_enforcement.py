#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / "tokens" / "enforcement.json"
DOC = ROOT / "ENFORCEMENT.md"
README = ROOT / "README.md"


def fail(message: str) -> None:
    raise SystemExit(f"Glaze UI enforcement validation failed: {message}")


def main() -> None:
    for path in (TOKENS, DOC, README):
        if not path.is_file():
            fail(f"missing {path.relative_to(ROOT)}")

    data = json.loads(TOKENS.read_text(encoding="utf-8"))
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if data.get("meta", {}).get("currentStable") != version:
        fail("enforcement current Stable baseline must match VERSION")
    scope = data.get("scope", {})
    if scope.get("nonExhaustive") is not True:
        fail("enforcement scope must remain non-exhaustive")
    if scope.get("failClosed") is not True:
        fail("material uncertainty must fail closed")
    if scope.get("productionExceptions") is not False:
        fail("production exceptions are prohibited")
    if data.get("prohibitedParallelSystems") is not True:
        fail("parallel local design systems must remain prohibited")

    required_domains = {
        "visualIdentity", "applicationIdentity", "serviceIdentity", "typography",
        "iconography", "color", "semanticColor", "materials", "surfaceHierarchy",
        "spacing", "geometry", "elevationDepth", "motion", "components",
        "interactionStates", "navigation", "forms", "feedback",
        "responsiveAdaptiveLayout", "formFactors", "inputMethods", "focus",
        "accessibility", "loadingEmptyErrorOfflineDegraded", "privacyPresentation",
        "securityProtectionPresentation", "resilienceRecoveryPresentation",
        "thirdPartyPresentation"
    }
    if set(data.get("domains", [])) != required_domains:
        fail("full-spectrum domain registry is incomplete")

    authority = data.get("integralAuthority", {})
    if authority.get("privacy") != "Privacy Shield":
        fail("Privacy Shield authority changed")
    if authority.get("securityProtection") != "Wardveil Security":
        fail("Wardveil Security authority changed")
    if authority.get("resiliencePreservationRecoveryPortabilitySuccessionLegacy") != "Everkeep":
        fail("Everkeep authority changed")

    doc = DOC.read_text(encoding="utf-8")
    for phrase in (
        "illustrative and non-exhaustive",
        "fails closed",
        "competing local design system",
        "Platform convention is an implementation mapping, not an exemption",
        "extended, validated, versioned, and promoted",
    ):
        if phrase not in doc:
            fail(f"missing enforcement documentation invariant: {phrase}")

    readme = README.read_text(encoding="utf-8")
    if "Full-spectrum enforcement" not in readme:
        fail("README must expose the full-spectrum enforcement contract")

    print("Glaze UI full-spectrum enforcement validation passed")


if __name__ == "__main__":
    main()
