#!/usr/bin/env python3
"""One-use deterministic Glaze UI 1.6.0 Stable release-state conversion.

This script changes lifecycle/version/governance metadata only after the 1.6
Candidate implementation and rendered matrices have already passed exact-head
validation. It intentionally does not promote Glaze Motion or wearable support.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.6.0"
PREVIOUS = "1.5.0"
DATE = "2026-08-28"
CANDIDATE_HEAD = "9a632e8df5ddd3a66c19ef2bb90efb7e65678048"
CANDIDATE_MERGE = "cc50ad8debce49b254da424399768741b0a5a96e"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, value: str) -> None:
    (ROOT / path).write_text(value, encoding="utf-8")


def replace(path: str, old: str, new: str, *, required: bool = True) -> None:
    body = read(path)
    if old not in body:
        if required:
            raise SystemExit(f"promotion replacement missing in {path}: {old!r}")
        return
    write(path, body.replace(old, new))


def update_json(path: str, mutate) -> None:
    data = json.loads(read(path))
    mutate(data)
    write(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


# Canonical release identity.
write("VERSION", VERSION + "\n")


def tokens(data: dict) -> None:
    data["meta"]["version"] = VERSION
    data["meta"]["status"] = "Stable"
    data["meta"]["stableBaseline"] = VERSION
update_json("tokens/glaze.tokens.json", tokens)


def enforcement(data: dict) -> None:
    data["meta"]["currentStable"] = VERSION
update_json("tokens/enforcement.json", enforcement)


def evidence(data: dict) -> None:
    meta = data["glaze_ui"]
    meta["release"] = VERSION
    meta["lifecycle"] = "stable"
    meta["stable_consumer_target"] = VERSION
    # Preserve the Candidate family marker as provenance for the promoted 1.6 contract.
    meta["candidate"] = "1.6"
update_json("tokens/evidence-presentation.json", evidence)


def workspace(data: dict) -> None:
    meta = data["meta"]
    meta["releaseVersion"] = VERSION
    meta["candidateVersion"] = VERSION
    meta["status"] = "Stable"
    meta["stableBaseline"] = VERSION
update_json("tokens/workspace-navigation.candidate.json", workspace)


def mesh_profile(data: dict) -> None:
    data["status"] = "stable-source-profile"
    rules = data.get("authority_rules", [])
    rules = [
        "The Glaze UI 1.6 evidence-presentation contract is Stable; producer authority remains external to Glaze UI."
        if "evidence-presentation contract remains Candidate" in rule else rule
        for rule in rules
    ]
    data["authority_rules"] = rules
update_json("tokens/mesh-evidence-profile.json", mesh_profile)


def registry(data: dict) -> None:
    data["stableBaseline"] = VERSION
    data["requiredConsumerVersion"] = VERSION
    history = list(data.get("historicalStableVersions", []))
    if PREVIOUS not in history:
        history.append(PREVIOUS)
    data["historicalStableVersions"] = history
    data["auditedAt"] = DATE
    for consumer in data.get("consumers", []):
        consumer["requiredTargetVersion"] = VERSION
        if consumer.get("targetVersion") != VERSION:
            consumer["status"] = "migration-required"
            consumer["productionEligible"] = False
            consumer["visualAcceptance"] = (
                "Current-Stable 1.6 migration and application-specific rendered/native/accessibility acceptance are required before production approval."
            )
            consumer["notes"] = (
                f"Existing {consumer.get('targetVersion', 'unknown')} evidence is historical migration input only after Glaze UI 1.6.0 promotion."
            )
update_json("consumers/registry.json", registry)

# Core lifecycle documentation.
replace("README.md", "## Glaze UI 1.5 Stable — Adaptive Color, Iconography, Motion, Materials, Layout, and State",
        "## Glaze UI 1.5 Historical Stable — Adaptive Color, Iconography, Motion, Materials, Layout, and State")
replace("README.md", "**Glaze UI 1.5.0 is the current Stable canonical baseline.**",
        "**Glaze UI 1.5.0 is the immediately preceding historical Stable baseline.**")
replace("README.md", "## Glaze UI 1.6 Candidate — Evidence Presentation and Adaptive Workspace",
        "## Glaze UI 1.6 Stable — Evidence Presentation and Adaptive Workspace")
old_16_intro = "Glaze UI 1.6 is active **Candidate** development on top of the 1.5.0 Stable baseline. Candidate source may be evaluated and validated on `main`, but it is not part of the Stable compatibility promise, does not change the current production target, and does not trigger consumer migration until separately promoted."
new_16_intro = "**Glaze UI 1.6.0 is the current Stable canonical baseline.** It retains every validated 1.5 Stable subsystem and promotes the evidence-presentation/authority-surface and Adaptive Workspace/Navigation contracts that passed the complete 1.6 Candidate source and browser-rendered acceptance stack."
replace("README.md", old_16_intro, new_16_intro)
replace("README.md", "The first 1.6 Candidate system formalizes", "The 1.6 Stable evidence system formalizes")
replace("README.md", "The Adaptive Workspace Candidate adds", "The 1.6 Stable Adaptive Workspace adds")
replace("README.md", "The Candidate implementation is defined by", "The promoted implementation is defined by")
replace("README.md", "Stable promotion remains subject to exact-head CI, rendered/native acceptance where applicable, accessibility/resilience review, compatibility/migration review, and `STABILITY.md`.",
        "Stable regression protection remains subject to exact-head CI, rendered/native acceptance where applicable, accessibility/resilience review, compatibility/migration review, and `STABILITY.md`.")
replace("README.md", "The current Stable consumer target is **1.5.0**", "The current Stable consumer target is **1.6.0**")
replace("README.md", "Historical Stable releases 1.0.0 through 1.4.0", "Historical Stable releases 1.0.0 through 1.5.0")
replace("README.md", "outside the implemented 1.5 Stable interaction scope", "outside the implemented 1.6 Stable interaction scope")
replace("README.md", "current Stable or 1.5 acceptance", "current Stable or 1.6 acceptance")
replace("README.md", "Glaze UI 1.6 Candidate evidence and authority presentation", "Glaze UI 1.6 Stable evidence and authority presentation")
replace("README.md", "Glaze UI 1.6 Candidate adaptive workspace and navigation contract", "Glaze UI 1.6 Stable adaptive workspace and navigation contract")
replace("README.md", "machine-readable 1.6 Candidate workspace", "machine-readable 1.6 Stable workspace")
replace("README.md", "reusable 1.6 Candidate workspace shell", "reusable 1.6 Stable workspace shell")
replace("README.md", "dependency-free 1.6 Candidate workspace evaluation surface", "dependency-free 1.6 Stable workspace regression surface")
replace("README.md", "fail-closed 1.6 Candidate workspace validator", "fail-closed 1.6 Stable workspace validator")
replace("README.md", "not part of current Stable or 1.5 acceptance", "not part of current Stable or 1.6 acceptance")
replace("README.md", "For implemented Glaze UI 1.6 Candidate systems, run:", "For Glaze UI 1.6 Stable systems, run:")
replace("README.md", "The promoted 1.5 subsystem validators remain permanent Stable regression gates. Candidate validation proves source-contract consistency only; it does not promote 1.6. Stable promotion also requires the applicable rendered/native evidence, accessibility/resilience review, compatibility and migration review, release-state synchronization, and exact-final-revision CI defined by `STABILITY.md`.",
        "The promoted 1.5 subsystem validators remain permanent Stable regression gates. Glaze UI 1.6 additionally requires its evidence-presentation and Adaptive Workspace source/rendered validators. Future Stable promotion still requires applicable rendered/native evidence, accessibility/resilience review, compatibility and migration review, release-state synchronization, and exact-final-revision CI defined by `STABILITY.md`.")
replace("README.md", "current Stable and 1.5 promotion gates", "current Stable and 1.6 promotion gates")

# Stability governance: preserve the policy, move the active baseline.
replace("STABILITY.md", "**Stable baseline:** Glaze UI **1.5.0**", "**Stable baseline:** Glaze UI **1.6.0**")
replace("STABILITY.md", "Glaze UI 1.4.0 remains the immediately preceding historical Stable baseline.",
        "Glaze UI 1.5.0 remains the immediately preceding historical Stable baseline.")
replace("STABILITY.md", "The 1.5 Stable baseline promotes adaptive color, iconography/construction/identity, motion/interaction, material/depth, layout/spacing/density, and semantic interaction-state/input-modality contracts on top of retained 1.4 form-factor semantics.",
        "The 1.6 Stable baseline retains the complete 1.5 adaptive-color, iconography, motion, material, layout, state, and form-factor foundation and promotes evidence presentation/authority surfaces plus Adaptive Workspace/Navigation.")
replace("STABILITY.md", "While 1.5.x remains Stable", "While 1.6.x remains Stable")
replace("STABILITY.md", "Glaze UI 1.0.0 through 1.4.0 are historical Stable releases", "Glaze UI 1.0.0 through 1.5.0 are historical Stable releases")
replace("STABILITY.md", "the current Stable 1.5.0 release", "the current Stable 1.6.0 release")
replace("STABILITY.md", "application-level 1.4 acceptance", "application-level 1.6 acceptance")

# Conformance and acceptance protocols.
replace("CONFORMANCE.md", "# Glaze UI 1.5 Conformance", "# Glaze UI 1.6 Conformance")
replace("CONFORMANCE.md", "Glaze UI 1.5 conformance", "Glaze UI 1.6 conformance")
replace("CONFORMANCE.md", "Glaze UI **1.5.0** is the current Stable baseline", "Glaze UI **1.6.0** is the current Stable baseline")
replace("CONFORMANCE.md", "`Glaze UI 1.5 conformant`", "`Glaze UI 1.6 conformant`")
replace("CONFORMANCE.md", "current 1.5 gate", "current 1.6 gate")
replace("CONFORMANCE.md", "Historical Glaze UI releases 1.0.0 through 1.4.0", "Historical Glaze UI releases 1.0.0 through 1.5.0")

replace("ACCEPTANCE.md", "## 1.2 application-interface acceptance retained by 1.5", "## 1.2 application-interface acceptance retained by 1.6")
replace("ACCEPTANCE.md", "## 1.3 expressive acceptance retained by 1.5", "## 1.3 expressive acceptance retained by 1.6")
replace("ACCEPTANCE.md", "## 1.4 form-factor acceptance retained by 1.5", "## 1.4 form-factor acceptance retained by 1.6")
replace("ACCEPTANCE.md", "## 1.5-specific Stable acceptance", "## 1.5 Stable subsystem acceptance retained by 1.6")
replace("ACCEPTANCE.md", "For 1.5 design-system core, native/real-device execution is not applicable", "For the 1.6 platform-neutral design-system core, native/real-device execution is not applicable")
acceptance = read("ACCEPTANCE.md")
marker = "## Stability promotion acceptance\n"
insert = "## 1.6-specific Stable acceptance\n\nEvidence Presentation and Authority Surfaces must preserve producer authority, neutral freshness/transport semantics, current negative outcomes, 200% text reflow, reduced-motion/transparency behavior, forced-colors distinction, and Mobile/Tablet/Desktop/Wide Desktop/TV rendering. Adaptive Workspace and Navigation must preserve semantic/focus order, current destination/action state, input-aware target floors, purpose-built Mobile/Tablet/Desktop/Wide Desktop/TV transformation, distinct TV far-view composition, reduced-transparency/performance fallbacks, and no unintended root overflow. The retained Candidate harnesses are permanent Stable regression gates for these promoted contracts.\n\n"
if insert not in acceptance:
    if marker not in acceptance: raise SystemExit("ACCEPTANCE.md promotion marker missing")
    acceptance = acceptance.replace(marker, insert + marker)
write("ACCEPTANCE.md", acceptance)

# Component contract/status.
replace("COMPONENTS.md", "# Glaze UI 1.5 Component Contract", "# Glaze UI 1.6 Component Contract")
replace("COMPONENTS.md", "Glaze UI 1.5 retains the Stable component semantics established in Glaze UI 1.3", "Glaze UI 1.6 retains the Stable component semantics established in Glaze UI 1.3")
replace("COMPONENT_STATUS.md", "# Glaze UI Component Lifecycle Registry", "# Glaze UI Component Lifecycle Registry")
replace("COMPONENT_STATUS.md", "## Glaze UI 1.6 Candidate systems", "## Glaze UI 1.6 Stable systems")
replace("COMPONENT_STATUS.md", "| Evidence presentation and authority surfaces | Candidate |", "| Evidence presentation and authority surfaces | Stable |")
replace("COMPONENT_STATUS.md", "| Adaptive workspace and navigation | Candidate |", "| Adaptive workspace and navigation | Stable |")
replace("COMPONENT_STATUS.md", "No Glaze UI 1.6 Candidate capability changes the current 1.5.0 Stable consumer target until separately promoted.",
        "Glaze UI 1.6.0 is the current Stable consumer target. The promoted evidence-presentation and Adaptive Workspace capabilities are now Stable; Glaze Motion and wearable expansion retain their separate non-Stable lifecycle states.")
replace("COMPONENT_STATUS.md", "Glaze Motion is not part of the Glaze UI 1.5.0 Stable compatibility promise", "Glaze Motion is not part of the Glaze UI 1.6.0 Stable compatibility promise")

# Promoted subsystem docs/tokens remain in their audited historical filenames.
replace("EVIDENCE_PRESENTATION.md", "# Glaze UI 1.6 Candidate — Evidence Presentation and Authority Surfaces", "# Glaze UI 1.6 Stable — Evidence Presentation and Authority Surfaces")
replace("EVIDENCE_PRESENTATION.md", "**Lifecycle:** Candidate. This contract is not part of the current Glaze UI 1.5.0 Stable baseline and must not be used to satisfy current Stable conformance until separately validated and promoted.",
        "**Lifecycle:** Stable in Glaze UI 1.6.0. This contract is part of the current Stable compatibility and conformance baseline.")
replace("EVIDENCE_PRESENTATION.md", "## Candidate rendered acceptance", "## Stable rendered acceptance")
replace("EVIDENCE_PRESENTATION.md", "## Candidate acceptance requirements", "## Stable regression requirements")
replace("EVIDENCE_PRESENTATION.md", "Until those gates pass and the release is explicitly promoted, this remains Candidate and the current Stable consumer target stays Glaze UI 1.5.0.",
        "These gates passed during the 1.6 Candidate promotion cycle and remain permanent Stable regression requirements. Glaze UI 1.6.0 is the current Stable consumer target.")

replace("WORKSPACE_NAVIGATION.md", "# Glaze UI 1.6 Candidate — Adaptive Workspace and Navigation", "# Glaze UI 1.6 Stable — Adaptive Workspace and Navigation")
replace("WORKSPACE_NAVIGATION.md", "Status: **Candidate**. Glaze UI 1.5.0 remains the current Stable production target. This contract is implemented for review but is not part of the Stable compatibility promise until promoted through `STABILITY.md`.",
        "Status: **Stable in Glaze UI 1.6.0**. This contract is part of the current Stable compatibility and production-conformance baseline.")
replace("WORKSPACE_NAVIGATION.md", "The Candidate implementation consists of:", "The Stable implementation consists of:")
replace("WORKSPACE_NAVIGATION.md", "## Rendered acceptance matrix", "## Stable rendered acceptance matrix")
replace("WORKSPACE_NAVIGATION.md", "The Candidate workspace is evaluated", "The Stable workspace is evaluated")
replace("WORKSPACE_NAVIGATION.md", "This rendered matrix proves the platform-neutral reference contract only.", "This rendered matrix remains the platform-neutral Stable regression contract only.")
replace("WORKSPACE_NAVIGATION.md", "## Promotion boundary", "## Stable release boundary")
replace("WORKSPACE_NAVIGATION.md", "Until the complete 1.6 promotion gate is satisfied, downstream applications may evaluate this layer only as Candidate behavior and must not claim Stable 1.6 conformance.",
        "Glaze UI 1.6.0 promotion completed the design-system gate. Downstream applications must still complete controlled 1.6 adoption and application-specific rendered/native/real-device acceptance before claiming current Stable conformance.")

# Consumer-facing governance docs.
for path in ("ADOPTION.md", "CONSUMERS.md", "IDENTITY.md"):
    body = read(path)
    body = body.replace("1.5.0", "1.6.0")
    body = body.replace("Glaze UI 1.5 ", "Glaze UI 1.6 ")
    write(path, body)

# Canonical reference and public Design Center release identity.
replace("reference/index.html", "Glaze UI 1.5", "Glaze UI 1.6")
replace("website/index.html", "Glaze UI 1.5 Stable", "Glaze UI 1.6 Stable")
replace("website/index.html", "Glaze UI 1.6 Candidate", "Glaze UI 1.6 Stable")
replace("website/index.html", "Candidate · production baseline remains 1.5.0", "Stable · current production baseline 1.6.0")
replace("website/index.html", "1.5 is Stable and is the production target.", "1.6 is Stable and is the production target.")
replace("website/index.html", "1.5.0", "1.6.0")

replace("website/build.py", "'glaze.workspace.candidate.css',", "'glaze.workspace.candidate.css',")
replace("website/validate.py", "'Glaze UI 1.5 Stable'", "'Glaze UI 1.6 Stable'")
replace("website/validate.py", "'Glaze UI 1.6 Candidate'", "'Glaze UI 1.6 Stable'")
replace("website/validate.py", "'Candidate · production baseline remains 1.5.0'", "'Stable · current production baseline 1.6.0'")
replace("website/validate.py", "'1.5 is Stable and is the production target.'", "'1.6 is Stable and is the production target.'")
replace("website/validate.py", "print('Glaze UI Design Center validation passed: 1.5 Stable with bounded 1.6 Candidate preview and synchronized Facet identity')",
        "print('Glaze UI Design Center validation passed: 1.6 Stable with evidence/workspace contracts and synchronized Facet identity')")

# Changelog and Stable acceptance record.
changelog = read("CHANGELOG.md")
release_entry = f"""## 1.6.0 — Stable — {DATE}\n\n- Promoted Evidence Presentation and Authority Surfaces to Stable with producer-authority separation across Wardveil Security, Privacy Shield, Everkeep, GoreeCloud Mesh, and Glaze UI presentation authority.\n- Promoted Adaptive Workspace and Navigation to Stable across Mobile, Tablet, Desktop, Wide Desktop, and distinct far-view TV composition.\n- Retained fail-closed rendered matrices for light/dark, reduced motion, reduced transparency, forced colors, constrained-performance fallbacks, density, target floors, and 200% text reflow.\n- Fixed the Candidate 200% Mobile evidence reflow defect before promotion; the acceptance gate was not weakened.\n- Candidate promotion evidence head `{CANDIDATE_HEAD}` passed Glaze UI CI #460, Icon Construction #145, Icon Identity #137, and Semantic Color #180 before merge as `{CANDIDATE_MERGE}`.\n- Glaze Motion remains Experimental and wearable production support remains deferred/production-blocked.\n- `1.6.0` becomes the mandatory current Stable consumer target; existing 1.5 and older application evidence becomes migration input only until each consumer completes 1.6 adoption and application-specific acceptance.\n\n"""
if "## 1.6.0 — Stable" not in changelog:
    first_release = changelog.find("## ")
    if first_release < 0: raise SystemExit("CHANGELOG.md has no release heading")
    changelog = changelog[:first_release] + release_entry + changelog[first_release:]
write("CHANGELOG.md", changelog)

stable_record = f"""# Glaze UI 1.6.0 Stable Acceptance Record\n\n## Release identity\n\n- Stable version: `1.6.0`\n- Previous Stable baseline: `1.5.0`\n- Scope: retained 1.5 Stable foundation plus Evidence Presentation and Authority Surfaces and Adaptive Workspace and Navigation.\n- Excluded from promotion: Glaze Motion remains Experimental; smartwatch/wearable production support remains deferred and production-blocked.\n\n## Candidate evidence\n\nThe exact validated Candidate hardening head was `{CANDIDATE_HEAD}`. It passed Glaze UI CI #460, Icon Construction #145, Icon Identity #137, and Semantic Color #180, including both 1.6 browser-rendered matrices. That work was squash-merged to `main` as `{CANDIDATE_MERGE}` before release-state conversion.\n\nThe evidence matrix caught a real Mobile 200% text-reflow overflow before promotion. The implementation was corrected and the unchanged fail-closed test passed on the final Candidate head.\n\n## Promotion conversion\n\nThe release-state conversion changes the canonical version, lifecycle metadata, current-Stable consumer requirement, governance documents, Design Center release identity, and Stable regression labels without weakening semantic, accessibility, rendering, authority, or subsystem validation. The final promotion PR head must pass the complete exact-head workflow stack before merge.\n\n## Authority boundaries\n\nGlaze UI governs presentation and interaction. Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Mesh, and application logic remain authoritative for their respective underlying truth. Freshness and transport availability do not become positive domain truth through Glaze UI presentation.\n\n## Consumer effect\n\nPromotion makes `1.6.0` the mandatory current Stable target. Existing consumers with 1.5.0 or older evidence are `migration-required` until they complete controlled 1.6 adoption and application-specific rendered/native/accessibility acceptance. Design-system promotion does not certify downstream application readiness.\n\n## Rollback\n\nBefore merge, rollback is branch/PR-level. After merge, rollback uses a documented revert or successor patch while preserving 1.5.0, Candidate 1.6, and 1.6.0 release evidence for audit and controlled migration.\n"""
write("acceptance/1.6.0.md", stable_record)

# Release validators switch from Candidate lifecycle assertions to Stable 1.6 assertions.
replace("scripts/validate_enforcement.py", 'if data.get("meta", {}).get("currentStable") != "1.4.0":\n        fail("current Stable baseline must remain 1.4.0")',
        'version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()\n    if data.get("meta", {}).get("currentStable") != version:\n        fail("enforcement current Stable baseline must match VERSION")')

replace("scripts/validate_evidence_presentation.py", 'if data.get("glaze_ui", {}).get("lifecycle") != "candidate":\n    fail("evidence presentation must remain Candidate until promotion")',
        'if data.get("glaze_ui", {}).get("lifecycle") != "stable":\n    fail("evidence presentation must be Stable after 1.6.0 promotion")')
replace("scripts/validate_evidence_presentation.py", 'if data.get("glaze_ui", {}).get("stable_consumer_target") != "1.5.0":\n    fail("current Stable consumer target must remain 1.5.0")',
        'if data.get("glaze_ui", {}).get("stable_consumer_target") != "1.6.0":\n    fail("evidence presentation Stable consumer target must be 1.6.0")')
replace("scripts/validate_evidence_presentation.py", 'if "Evidence presentation and authority surfaces | Candidate" not in status:\n    fail("component lifecycle registry must keep evidence presentation Candidate")',
        'if "Evidence presentation and authority surfaces | Stable" not in status:\n    fail("component lifecycle registry must mark evidence presentation Stable")')
replace("scripts/validate_evidence_presentation.py", '"The release remains **Candidate**",', '"Stable version: `1.6.0`",')
replace("scripts/validate_evidence_presentation.py", 'ACCEPTANCE_RECORD = ROOT / "acceptance" / "1.6-candidate.md"', 'ACCEPTANCE_RECORD = ROOT / "acceptance" / "1.6.0.md"')
replace("scripts/validate_evidence_presentation.py", '"Candidate version: `1.6.0-candidate`",\n    "Stable baseline preserved: `1.5.0`",', '"Stable version: `1.6.0`",\n    "Previous Stable baseline: `1.5.0`",')

replace("scripts/validate_workspace_navigation.py", 'if meta.get("status") != "Candidate":\n        fail("workspace layer must remain Candidate before promotion")',
        'if meta.get("status") != "Stable":\n        fail("workspace layer must be Stable after 1.6.0 promotion")')
replace("scripts/validate_workspace_navigation.py", 'if meta.get("stableBaseline") != "1.5.0":\n        fail("workspace Candidate must retain 1.5.0 Stable baseline")',
        'if meta.get("stableBaseline") != "1.6.0":\n        fail("workspace Stable baseline must be 1.6.0")')
replace("scripts/validate_workspace_navigation.py", '"Status: **Candidate**",\n            "Glaze UI 1.5.0 remains the current Stable production target",',
        '"Status: **Stable in Glaze UI 1.6.0**",\n            "current Stable compatibility and production-conformance baseline",')
replace("scripts/validate_workspace_navigation.py", 'ACCEPTANCE_RECORD = ROOT / "acceptance" / "1.6-candidate.md"', 'ACCEPTANCE_RECORD = ROOT / "acceptance" / "1.6.0.md"')
replace("scripts/validate_workspace_navigation.py", '"Candidate version: `1.6.0-candidate`",\n            "Stable baseline preserved: `1.5.0`",\n            "The release remains **Candidate**",',
        '"Stable version: `1.6.0`",\n            "Previous Stable baseline: `1.5.0`",\n            "mandatory current Stable target",')

# Release-state validator now also requires promoted 1.6 subsystem lifecycle truth.
validator = read("scripts/validate_release_state.py")
needle = "require('No active 1.4 form-factor capability remains Candidate' in component_status,'1.4 lifecycle reconciliation is incomplete')"
addition = needle + "\n    require('Evidence presentation and authority surfaces | Stable' in component_status,'1.6 evidence-presentation lifecycle reconciliation is incomplete')\n    require('Adaptive workspace and navigation | Stable' in component_status,'1.6 workspace lifecycle reconciliation is incomplete')\n    require('Glaze Motion 0.6 | Experimental' in component_status,'Glaze Motion must remain Experimental during 1.6 promotion')"
if addition not in validator:
    if needle not in validator: raise SystemExit("release-state lifecycle marker missing")
    validator = validator.replace(needle, addition)
write("scripts/validate_release_state.py", validator)

# CI labels reflect Stable 1.6 while retaining historical Candidate harness filenames.
replace(".github/workflows/ci.yml", "Validate Glaze UI 1.6 evidence presentation Candidate", "Validate Glaze UI 1.6 evidence presentation Stable")
replace(".github/workflows/ci.yml", "Validate Glaze UI 1.6 adaptive workspace Candidate", "Validate Glaze UI 1.6 adaptive workspace Stable")
replace(".github/workflows/ci.yml", "Validate rendered Glaze UI 1.6 Candidate adaptive workspace", "Validate rendered Glaze UI 1.6 Stable adaptive workspace")
replace(".github/workflows/ci.yml", "Validate rendered Glaze UI 1.6 Candidate evidence presentation", "Validate rendered Glaze UI 1.6 Stable evidence presentation")

# Styling headers become truthful while selectors/filenames remain audit-stable.
replace("css/glaze.workspace.candidate.css", "/* Glaze UI 1.6 Candidate — Adaptive Workspace and Navigation\n   Stable baseline remains Glaze UI 1.5.0. Do not treat these primitives as Stable. */",
        "/* Glaze UI 1.6.0 Stable — Adaptive Workspace and Navigation.\n   Historical Candidate filename/selectors are retained for compatibility and release-evidence continuity. */")
replace("css/glaze.evidence.css", "/* Glaze UI 1.6 Candidate — evidence presentation primitives.\n * Candidate only: current Stable consumer target remains Glaze UI 1.5.0.\n */",
        "/* Glaze UI 1.6.0 Stable — evidence presentation primitives. */")

print("Glaze UI 1.6.0 Stable release-state conversion applied")
