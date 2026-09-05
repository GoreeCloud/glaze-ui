#!/usr/bin/env python3
"""Validate bounded GLAZE UI V1.2 core token ownership without creating a competing value source."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts/v1.2/core-tokens.candidate.json"
MANIFEST = ROOT / "tokens/glaze-v1.2-core.candidate.json"
README = ROOT / "tokens/README.md"
LIFECYCLE = ROOT / "registry/lifecycle.json"
VERSION = ROOT / "VERSION"
ARTIFACTS = ROOT / "artifacts"
REPORT = ARTIFACTS / "glaze-v1.2-core-tokens-report.json"

EXPECTED = {
    "color": ("color.opticalPalette", "tokens/glaze-v1.2-optical-foundation.candidate.json", "/opticalPalette", "candidate-owned"),
    "atmosphere": ("atmosphere.auraFamilies", "tokens/glaze-v1.2-optical-foundation.candidate.json", "/auraFamilies", "candidate-owned"),
    "material": ("material.appearance", "tokens/glaze-v1.2-frosted-neutral.candidate.json", "/materials", "candidate-owned"),
    "frost": ("frost.levels", "tokens/glaze-v1.2-optical-foundation.candidate.json", "/frostLevels", "candidate-owned"),
    "blur": ("blur.material", "tokens/glaze-v1.2-frosted-neutral.candidate.json", "/effects/blur", "candidate-owned"),
    "opacity": ("opacity.material", "tokens/glaze-v1.2-frosted-neutral.candidate.json", "/materials", "candidate-owned"),
    "spacing": ("spacing.scale", "tokens/glaze-v1.2-spatial-foundation.candidate.json", "/spacePx", "candidate-owned"),
    "density": ("density.profiles", "tokens/glaze-v1.2-spatial-foundation.candidate.json", "/density", "candidate-owned"),
    "radius": ("radius.roles", "tokens/glaze-v1.2-geometry.candidate.json", "/radiusPx", "candidate-owned"),
    "shadow": ("shadow.roles", "tokens/glaze-v1.2-depth.candidate.json", "/depth", "candidate-owned"),
    "elevation": ("elevation.roles", "tokens/glaze-v1.2-depth.candidate.json", "/depth", "candidate-owned"),
    "typography": ("typography.roles", "tokens/glaze-v1.2-typography.candidate.json", "/roles", "candidate-owned"),
    "iconSize": ("icon.sizes", "tokens/glaze-v1.2-crystal-icons.candidate.json", "/sizes", "candidate-owned"),
    "stroke": ("icon.strokes", "tokens/glaze-v1.2-crystal-icons.candidate.json", "/strokeViewBox", "candidate-owned"),
    "motion": ("motion.durations", "tokens/glaze-v1.2-motion.candidate.json", "/durationsMs", "candidate-owned"),
    "semanticColor": ("semanticColor.roles", "tokens/semantic-colors.json", "/roles", "inherited-semantic-contract"),
}
UNESTABLISHED = {"state", "formFactor"}
RAW_VALUE = re.compile(r"#[0-9a-fA-F]{3,8}|rgba?\(|\b\d+(?:\.\d+)?(?:px|rem|em|ms)\b")


class ValidationError(RuntimeError):
    pass


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValidationError(message)


def load(path: Path) -> dict:
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"expected object in {path.relative_to(ROOT)}")
    return value


def resolve_pointer(document: object, pointer: str) -> object:
    require(pointer.startswith("/"), f"invalid JSON pointer {pointer!r}")
    current = document
    for raw in pointer[1:].split("/"):
        key = raw.replace("~1", "/").replace("~0", "~")
        require(isinstance(current, dict) and key in current, f"unresolved JSON pointer {pointer!r} at {key!r}")
        current = current[key]
    return current


def validate_candidate_source(path: Path, document: dict) -> None:
    require(document.get("version") == "1.2.0-candidate", f"Candidate version drifted in {path.relative_to(ROOT)}")
    require(document.get("lifecycle") == "candidate", f"Candidate lifecycle drifted in {path.relative_to(ROOT)}")
    require(document.get("stableBaseline") == "1.1.0", f"Stable baseline drifted in {path.relative_to(ROOT)}")
    if "consumerEligible" in document:
        require(document.get("consumerEligible") is False, f"Candidate consumer eligibility drifted in {path.relative_to(ROOT)}")
    if "currentStableToken" in document:
        require(document.get("currentStableToken") is False, f"Candidate was presented as current Stable in {path.relative_to(ROOT)}")


def main() -> int:
    contract = load(CONTRACT)
    manifest = load(MANIFEST)
    lifecycle = load(LIFECYCLE)

    require(VERSION.read_text(encoding="utf-8").strip() == "1.1.0", "VERSION no longer preserves V1.1 Stable")
    require(lifecycle.get("currentStable") == "1.1.0" and lifecycle.get("currentOfficial") == "1.1.0", "lifecycle no longer preserves V1.1 Stable/Official")
    v12 = next((item for item in lifecycle.get("releases", []) if item.get("version") == "1.2.0-candidate"), None)
    require(isinstance(v12, dict) and v12.get("status") == "candidate" and v12.get("consumerEligible") is False, "V1.2 lifecycle boundary drifted")

    for document, name in ((contract, "contract"), (manifest, "manifest")):
        require(document.get("version") == "1.2.0-candidate", f"core token {name} version drifted")
        require(document.get("lifecycle") == "candidate", f"core token {name} lifecycle drifted")
        require(document.get("consumerEligible") is False, f"core token {name} consumer eligibility drifted")
        require(document.get("stableBaseline") == "1.1.0", f"core token {name} Stable baseline drifted")

    principles = contract.get("principles", {})
    for key in ("semanticRolesBeforeRawValues", "singleOwnerPerFamily", "compositionManifestDoesNotDuplicateRawValues", "candidateDoesNotReplaceStable", "unimplementedFamiliesRemainExplicitlyUnestablished", "platformAdaptersMayMapButNotRedefineSemanticAuthority"):
        require(principles.get(key) is True, f"core token principle missing: {key}")

    aliases = manifest.get("aliases", {})
    families = contract.get("families", {})
    require(set(families) == set(EXPECTED) | UNESTABLISHED, f"core token family set drifted: {sorted(families)}")
    require(set(aliases) == {item[0] for item in EXPECTED.values()}, f"core token alias set drifted: {sorted(aliases)}")
    require(not RAW_VALUE.search(json.dumps(aliases, sort_keys=True)), "core composition manifest copied raw token values")

    loaded_sources: dict[str, dict] = {}
    resolved: dict[str, str] = {}
    for family, (alias_name, source, pointer, status) in EXPECTED.items():
        item = families.get(family, {})
        alias = aliases.get(alias_name, {})
        require(item.get("status") == status and item.get("owner") == source and item.get("pointer") == pointer, f"ownership drifted for {family}")
        require(alias == {"source": source, "pointer": pointer}, f"alias drifted for {family}")
        path = ROOT / source
        if source not in loaded_sources:
            loaded_sources[source] = load(path)
            if source.startswith("tokens/glaze-v1.2-"):
                validate_candidate_source(path, loaded_sources[source])
        value = resolve_pointer(loaded_sources[source], pointer)
        require(value not in ({}, [], None, ""), f"alias resolved to empty authority for {family}")
        resolved[family] = f"{source}#{pointer}"

    semantic = loaded_sources["tokens/semantic-colors.json"]
    require(semantic.get("color_only_communication_allowed") is False, "semantic color contract permits color-only meaning")
    require(semantic.get("branding_may_override_semantics") is False, "semantic color contract permits branding to redefine meaning")

    for family in UNESTABLISHED:
        item = families.get(family, {})
        mirror = manifest.get("unestablished", {}).get(family, {})
        require(item.get("owner") is None and item.get("pointer") is None and item.get("consumerClaimBlocked") is True, f"unestablished family incorrectly claims ownership: {family}")
        require(mirror.get("consumerClaimBlocked") is True, f"manifest unestablished boundary drifted: {family}")
    require(all(spec.get("source") != "tokens/states.json" for spec in aliases.values()), "unrelated lifecycle state tokens were imported as V1.2 authority")

    rules = manifest.get("rules", {})
    require(all(rules.get(key) is True for key in ("aliasesResolveToExistingSources", "aliasesContainNoCopiedRawValues", "oneFamilyOneOwner", "unestablishedFamiliesCannotBePresentedAsImplemented", "semanticColorMeaningDoesNotAuthorizeHardCodedPigment", "candidateCannotBecomeConsumerTargetByManifestPresence")), "core token manifest rules drifted")

    readme = README.read_text(encoding="utf-8")
    for marker in ("V1.1 / `1.1.0`", "glaze-v1.2-core.candidate.json", "non-consumer-eligible", "does not duplicate raw token values"):
        require(marker in readme, f"token authority documentation missing marker: {marker}")

    ARTIFACTS.mkdir(exist_ok=True)
    report = {
        "id": contract["id"],
        "version": contract["version"],
        "lifecycle": contract["lifecycle"],
        "stableBaseline": contract["stableBaseline"],
        "consumerEligible": contract["consumerEligible"],
        "resolvedFamilies": resolved,
        "unestablishedFamilies": sorted(UNESTABLISHED),
        "result": "pass"
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"GLAZE UI V1.2 core token authority validated: {len(resolved)} resolved families; {len(UNESTABLISHED)} explicitly unestablished")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as error:
        print(f"GLAZE UI V1.2 core token authority validation failed: {error}")
        raise SystemExit(1)
