#!/usr/bin/env python3
"""Promote a fully validated GLAZE UI V1.1 release candidate to Stable source authority.

This script is intentionally deterministic and is designed to run only after the
Glaze V1.1 Release Evidence workflow has succeeded for the exact source revision.
It updates current authority coherently in one generated commit. It does not create
a Git tag or GitHub Release; those remain post-merge release-finalization steps.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RC_VERSION = "1.1.0-rc.1"
STABLE_VERSION = "1.1.0"
PRODUCT = "GLAZE UI V1.1"
TODAY = "2026-09-03"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, value: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(value.rstrip() + "\n", encoding="utf-8")


def load(path: str):
    return json.loads(read(path))


def dump(path: str, value) -> None:
    write(path, json.dumps(value, indent=2))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def replace_required(text: str, old: str, new: str, label: str) -> str:
    require(old in text, f"promotion source drift: {label}")
    return text.replace(old, new)


def stable_optical(candidate: str) -> str:
    candidate = re.sub(
        r"\A/\*.*?\*/\n",
        "/*\n * GLAZE UI V1.1 — Stable optical refinement layer.\n * Activation: html[data-glaze-version=\\\"1.1\\\"] only.\n * Inherits the GLAZE UI V1.0 structural material baseline without adding\n * nested backdrop blur, semantic-state authority, content sampling, or remote assets.\n */\n",
        candidate,
        count=1,
        flags=re.DOTALL,
    )
    candidate = candidate.replace('@import url("./glaze-v1.0.0.css");\n\n', "", 1)
    candidate = candidate.replace('html[data-glaze-version-candidate="1.1"]', 'html[data-glaze-version="1.1"]')
    return candidate


def stable_appearance(candidate: str) -> str:
    candidate = re.sub(
        r"\A/\*.*?\*/\n",
        "/*\n * GLAZE UI V1.1 — Stable explicit appearance adapter.\n * Maps Light, Dark, and Deep Dark to inherited V1 structural surface/text roles.\n * Protected semantic-state colors remain producer-authoritative and unchanged.\n */\n",
        candidate,
        count=1,
        flags=re.DOTALL,
    )
    return candidate.replace('html[data-glaze-version-candidate="1.1"]', 'html[data-glaze-version="1.1"]')


def promote_machine_contracts(rc_revision: str, evidence_run_id: str) -> None:
    candidate = load("contracts/v1.1/optical-refinement.candidate.json")
    stable = json.loads(json.dumps(candidate))
    stable["id"] = "glaze-ui-v1.1-optical-refinement"
    stable["version"] = STABLE_VERSION
    stable["lifecycle"] = "stable"
    stable["releaseBoundary"] = {
        "currentTarget": True,
        "currentTargetVersion": STABLE_VERSION,
        "productionStableDesignSystemRelease": True,
        "downstreamConsumerConformanceAutomatic": False,
        "downstreamProductionEligibilityAutomatic": False,
    }
    stable["releaseEvidence"] = {
        "humanOpticalApproval": {
            "status": "approved",
            "authority": "GoreeCloud project owner",
            "date": TODAY,
            "approvedVisualSourceRevision": "8ea1f789bbabf943c3359514dc1506b24fa3c51b",
        },
        "releaseCandidateRevision": rc_revision,
        "releaseEvidenceWorkflowRun": int(evidence_run_id) if evidence_run_id.isdigit() else evidence_run_id,
        "stableSourcePromotionRequiresExactHeadValidation": True,
        "tagAndGitHubReleaseRequiredAfterMerge": True,
    }
    dump("contracts/v1.1/optical-refinement.json", stable)

    atmosphere = load("tokens/glaze-v1.1-atmosphere.candidate.json")
    stable_atmosphere = json.loads(json.dumps(atmosphere))
    stable_atmosphere["id"] = "glaze-v1.1-atmosphere"
    stable_atmosphere["version"] = STABLE_VERSION
    stable_atmosphere["lifecycle"] = "stable"
    stable_atmosphere["currentV1Token"] = True
    dump("tokens/glaze-v1.1-atmosphere.json", stable_atmosphere)

    rc_baseline = load("contracts/v1.1/visual-regression-baseline.rc.json")
    baseline = {
        "schemaVersion": 1,
        "product": PRODUCT,
        "version": STABLE_VERSION,
        "status": "stable-human-approved-source-pinned",
        "baselineRevision": rc_baseline["approvedVisualSourceRevision"],
        "releaseCandidateEvidenceRevision": rc_revision,
        "approvedBy": rc_baseline["approvedBy"],
        "approvedOn": rc_baseline["approvedOn"],
        "cases": rc_baseline["cases"],
        "note": "Stable V1.1 preserves the project-owner-approved optical pixels. Candidate identity text in the immutable acceptance scenes is retained as provenance; Stable runtime CSS is a deterministic selector/lifecycle promotion of the approved optical implementation.",
        "newOpticalPixelsRequireNewHumanApproval": True,
    }
    dump("contracts/regression/visual-baselines-v1.json", baseline)

    release = {
        "schemaVersion": 1,
        "product": PRODUCT,
        "version": STABLE_VERSION,
        "lifecycle": "Stable source promotion",
        "releaseCandidate": RC_VERSION,
        "releaseCandidateRevision": rc_revision,
        "releaseEvidenceWorkflowRun": int(evidence_run_id) if evidence_run_id.isdigit() else evidence_run_id,
        "humanOpticalApproval": {
            "authority": "GoreeCloud project owner",
            "date": TODAY,
            "approvedVisualSourceRevision": "8ea1f789bbabf943c3359514dc1506b24fa3c51b",
        },
        "webEvidence": {
            "sourcePinnedBaseline": "contracts/regression/visual-baselines-v1.json",
            "requiredCases": 5,
        },
        "androidEvidence": {
            "scope": "framework-native Android handheld emulator reference",
            "requiredCases": ["light-48dp", "dark-reduced-transparency-48dp", "deep-dark-200-percent-text-touch-assistance-56dp"],
            "boundaries": ["not OEM-wide qualification", "not physical-device qualification", "not TalkBack certification", "not app signing/distribution acceptance", "not downstream application conformance"],
        },
        "finalization": {
            "governedMergeRequired": True,
            "postMergeMainValidationRequired": True,
            "immutableTagRequired": "v1.1.0",
            "githubReleaseRequired": "v1.1.0",
            "canonicalGoreecloudDocumentationSyncRequired": True,
        },
    }
    dump("contracts/v1.1/release.json", release)


def promote_current_authority() -> None:
    write("VERSION", STABLE_VERSION)

    lifecycle = load("registry/lifecycle.json")
    v10 = lifecycle.get("releases", [{}])[0]
    lifecycle.update({
        "updated": TODAY,
        "officialProductLabel": PRODUCT,
        "currentOfficial": STABLE_VERSION,
        "currentStable": STABLE_VERSION,
        "activeCandidate": None,
        "resetState": "stable",
    })
    lifecycle["releases"] = [
        {
            "version": "1.0.0",
            "label": "GLAZE UI V1.0",
            "status": "historical-reset-baseline",
            "consumerEligible": False,
            "contract": "GLAZE_UI_V1_0.md",
            "acceptance": "acceptance/v1.0-stable.md",
            "note": v10.get("note", "Historical V1.0 reset baseline; not a current consumer target."),
        },
        {
            "version": STABLE_VERSION,
            "label": PRODUCT,
            "status": "stable",
            "consumerEligible": True,
            "contract": "GLAZE_UI_V1_1.md",
            "acceptance": "acceptance/v1.1-stable.md",
            "note": "Current Stable shared design-system release. Consumer applications remain independently migration- and acceptance-gated.",
        },
    ]
    lifecycle["capabilities"] = {
        "system-shell": {"status": "stable-inherited", "since": "1.0.0", "implementation": "contracts/system-shell/glaze-system-shell-v1.json"},
        "component-catalog": {"status": "stable-inherited", "since": "1.0.0", "implementation": "contracts/components/v1/catalog.json"},
        "web-entrypoint": {"status": "stable", "since": STABLE_VERSION, "implementation": "css/glaze-v1.1.0.css"},
        "runtime-entrypoint": {"status": "stable", "since": STABLE_VERSION, "implementation": "js/glaze-v1.1.0.mjs"},
        "performance-budget": {"status": "stable-inherited", "since": "1.0.0", "implementation": "contracts/performance/glaze-v1-performance-budget.json"},
        "visual-regression": {"status": "stable", "since": STABLE_VERSION, "implementation": "contracts/regression/visual-baselines-v1.json"},
        "native-reference": {"status": "bounded-release-evidence", "since": STABLE_VERSION, "implementation": "reference/v1.1/native/android"},
    }
    dump("registry/lifecycle.json", lifecycle)

    consumers = load("consumers/registry.json")
    consumers["officialBaseline"] = STABLE_VERSION
    consumers["officialProductLabel"] = PRODUCT
    consumers["requiredConsumerVersion"] = STABLE_VERSION
    consumers["auditedAt"] = TODAY
    rule = consumers.get("enforcement", {}).get("unsupportedPlatformRule", "")
    consumers["enforcement"]["unsupportedPlatformRule"] = rule.replace("GLAZE UI V1.0", PRODUCT)
    for consumer in consumers.get("consumers", []):
        consumer["requiredTargetVersion"] = STABLE_VERSION
        consumer["productionEligible"] = False
        notes = consumer.get("notes", "")
        notes = notes.replace("GLAZE UI V1.0", PRODUCT).replace("V1.0", "V1.1")
        consumer["notes"] = notes or "Fresh repository-local GLAZE UI V1.1 adoption and acceptance evidence is required."
    dump("consumers/registry.json", consumers)

    schema = load("contracts/glaze.conformance-evidence.schema.json")
    schema["title"] = "GLAZE UI V1.1 Conformance Evidence Record"
    schema["properties"]["target"]["properties"]["glaze_version"]["const"] = STABLE_VERSION
    dump("contracts/glaze.conformance-evidence.schema.json", schema)

    tokens = load("tokens/glaze-v1.json")
    tokens.update({
        "product": PRODUCT,
        "version": STABLE_VERSION,
        "status": "stable",
        "sources": ["glaze.tokens.json", "materials.json", "semantic-colors.json", "glaze-v1.1-atmosphere.json"],
        "note": "Current Stable V1 token manifest. V1.1 adds the approved optical-atmosphere layer while preserving inherited V1 material, semantic, accessibility, component, and system-shell authority.",
    })
    dump("tokens/glaze-v1.json", tokens)


def promote_entrypoints() -> None:
    write("css/glaze-v1.1.css", stable_optical(read("css/glaze-v1.1-candidate.css")))
    write("css/glaze-v1.1-appearance.css", stable_appearance(read("css/glaze-v1.1-appearance.candidate.css")))
    write(
        "css/glaze-v1.1.0.css",
        '/* GLAZE UI V1.1.0 — official Stable web entrypoint. */\n'
        '@import url("./glaze-v1.0.0.css");\n'
        '@import url("./glaze-v1.1.css");\n'
        '@import url("./glaze-v1.1-appearance.css");',
    )
    write(
        "js/glaze-v1.1.0.mjs",
        '/* GLAZE UI V1.1.0 — official Stable runtime entrypoint. */\n'
        'export * from "./glaze-v1.runtime.mjs";\n'
        'export * from "./glaze-v1.system-interactions.mjs";',
    )


def promote_docs(rc_revision: str, evidence_run_id: str) -> None:
    write("GLAZE_UI_V1_1.md", f"""# GLAZE UI V1.1 — Official Stable Contract

**Official product identity:** GLAZE UI V1.1  
**Machine version:** 1.1.0  
**Lifecycle:** Stable  
**Repository:** `GoreeCloud/goreecloud-glaze-ui`

GLAZE UI V1.1 is GoreeCloud's current Stable shared visual and interaction design-system release. It preserves the structural, semantic, accessibility, component, System Shell, and performance contracts established by V1.0 while adding the human-approved Optical Refinement and Extended Atmospheric Color System.

## Stable design identity

The core presentation rule remains: **Solid where users read or make explicit critical decisions. Glazed where users interact with transient navigation, command, search, control, or feedback chrome.**

V1.1 adds a restrained environmental identity built around **Deep Teal + Soft Amber**, with neutral structure remaining dominant. Atmospheric expression resolves after protected semantic meaning and accessibility requirements and never becomes a source of security, privacy, identity, recovery, or coordination truth.

## Frozen V1.1 additions

- Unified upper-left optical light direction and restrained edge illumination.
- Deep Teal + Soft Amber atmospheric identity with deterministic Aura and material-tint caps.
- 8 / 16 / 24 / 32 px optical geometry references plus capsule geometry.
- Explicit Light, Dark, and Deep Dark structural appearance mapping.
- Comfortable, Standard, Productive, and Immersive optical density mappings while preserving interaction-target floors.
- Existing V1 signature-component optical refinement without component-catalog expansion.
- Optional Environmental Color Memory bounded to local, non-semantic derivation with a no-sampling fallback; it is not implemented in the first Stable web layer.

## Preserved authority

V1.1 does not add protected semantic colors, enable nested backdrop blur, promote Glaze Motion, require environmental sampling, or make Muted Coral canonical. Forced Colors, Reduced Motion, Reduced Transparency, Increased Contrast, 200% text, Touch Assistance, and semantic-state authority resolve before atmospheric expression.

The inherited material budget remains one dominant Glaze panel plus at most three small floating Glaze controls, with no default nested backdrop-blur stack and effects removable before semantics.

## Current entrypoints

- Web: `css/glaze-v1.1.0.css`
- Runtime: `js/glaze-v1.1.0.mjs`
- Optical contract: `contracts/v1.1/optical-refinement.json`
- Atmospheric tokens: `tokens/glaze-v1.1-atmosphere.json`
- Visual baseline authority: `contracts/regression/visual-baselines-v1.json`
- Acceptance: `acceptance/v1.1-stable.md`
- Current validator: `scripts/validate_glaze_v1.py`

## Release evidence

The project owner explicitly approved the V1.1 optical review on {TODAY}. Release-candidate revision `{rc_revision}` passed source-pinned web regression and fresh framework-native Android handheld emulator evidence in workflow run `{evidence_run_id}` before Stable source promotion.

The Android evidence is bounded design-system reference evidence, not OEM-wide, physical-device, TalkBack, signing/distribution, downstream application, or production-deployment acceptance.

## Consumer boundary

No downstream GoreeCloud application becomes V1.1-conformant by this release alone. Each consumer must explicitly migrate to 1.1.0 and produce application-specific exact-revision evidence for its supported platforms and production boundary.

Glaze Motion remains separately Experimental unless a later governed contract explicitly changes that lifecycle.
""")

    write("README.md", f"""# GLAZE UI V1.1

GLAZE UI V1.1 is GoreeCloud's current Stable shared visual and interaction design system. **Beauty is a requirement, not a regression risk.** Machine version: **1.1.0**.

## Core rule

**Solid where users read or make explicit critical decisions. Glazed where users interact with transient navigation, command, search, control, or feedback chrome.**

V1.1 preserves the V1 System Shell, 32-component catalog, semantic color, accessibility, material, performance, and native-mapping contracts while adding the approved Optical Refinement and **Deep Teal + Soft Amber** atmospheric system.

The atmosphere is intentionally subordinate: neutral structure remains dominant; protected semantic meaning, focus, accessibility, and required boundaries always resolve first. Environmental Color Memory remains optional and is not required by the first Stable implementation.

## Stable evidence

Project-owner optical approval was recorded on {TODAY}. Exact release-candidate revision `{rc_revision}` reproduced the five approved web reference PNG hashes and passed fresh Android handheld emulator acceptance for Light/48dp, Dark + Reduced Transparency/48dp, and Deep Dark + 200% text + Touch Assistance/56dp in release-evidence workflow `{evidence_run_id}`.

Current source authority:
- `VERSION` — `1.1.0`
- `GLAZE_UI_V1_1.md` — official Stable contract
- `registry/lifecycle.json` — lifecycle authority
- `css/glaze-v1.1.0.css` — Stable web entrypoint
- `js/glaze-v1.1.0.mjs` — Stable runtime entrypoint
- `contracts/v1.1/optical-refinement.json` — Stable optical contract
- `tokens/glaze-v1.1-atmosphere.json` — Stable atmosphere tokens
- `contracts/regression/visual-baselines-v1.json` — approved visual baseline authority
- `acceptance/v1.1-stable.md` — Stable acceptance boundary

The V1.0 contract and candidate/RC records remain historical audit evidence, not current consumer targets. No downstream GoreeCloud application auto-upgrades or gains production eligibility by declaration.

Glaze Motion remains separately Experimental.

## License

MIT. GoreeCloud branding and product identity remain subject to applicable project policies.
""")

    write("SPECIFICATIONS.md", f"""# GLAZE UI V1.1 — Specifications

## Product identity

- **Official product name:** GLAZE UI V1.1
- **Machine version:** `1.1.0`
- **Lifecycle:** Stable
- **Repository:** `GoreeCloud/goreecloud-glaze-ui`
- **Authoritative product contract:** `GLAZE_UI_V1_1.md`

## Runtime entrypoints

- Web CSS: `css/glaze-v1.1.0.css`
- Web JavaScript: `js/glaze-v1.1.0.mjs`
- Token manifest: `tokens/glaze-v1.json`
- V1.1 atmosphere: `tokens/glaze-v1.1-atmosphere.json`
- V1.1 optical contract: `contracts/v1.1/optical-refinement.json`
- Component catalog: `contracts/components/v1/catalog.json`
- System Shell: `contracts/system-shell/glaze-system-shell-v1.json`
- Lifecycle registry: `registry/lifecycle.json`
- Consumer registry: `consumers/registry.json`

## Stable V1.1 requirements

V1.1 preserves V1 structural materials, semantic/protected-state authority, accessibility precedence, the canonical 32-component catalog, System Shell semantics, and the governed Glaze-region performance budget. It adds deterministic optical lighting, Deep Teal + Soft Amber atmosphere, explicit Light/Dark/Deep Dark structural mapping, optical geometry and density refinements, and approved reference-scene acceptance.

Atmosphere is always lower priority than protected meaning, Forced Colors, Reduced Motion, Reduced Transparency, Increased Contrast, large text, touch assistance, platform capability, and material clarity. No feature may depend on atmosphere or color alone for meaning.

## Acceptance boundary

Stable source qualification is backed by project-owner optical approval, source-pinned web regression, current V1 contract validation, and fresh Android handheld emulator evidence from exact release-candidate revision `{rc_revision}` / workflow `{evidence_run_id}`. Platform-native evidence remains bounded to what it actually tested. Downstream applications remain independently migration-, platform-, accessibility-, and production-acceptance-gated.
""")

    write("BRANDING.md", """# GLAZE UI V1.1 — Branding

## Official identity

- **Product name:** GLAZE UI V1.1
- **Short product name:** Glaze UI
- **Machine version:** `1.1.0`
- **Lifecycle:** Stable
- **Repository:** `GoreeCloud/goreecloud-glaze-ui`

Use **GLAZE UI V1.1** where the official versioned product identity is required. Use **Glaze UI** in ordinary prose where the version is not material. Use `1.1.0` for machine-readable version fields.

The official Facet identity mark remains `assets/identity/official/facet/glaze-ui-mark.svg`.

V1.1's atmospheric identity is Deep Teal + Soft Amber over neutral structure. Branding never overrides semantic state, accessibility, or producer-authoritative security/privacy/identity/recovery/coordination truth.

V1.0 and V1.1 candidate/RC labels are historical only and must not be presented as current product identity. Branding alone does not establish downstream conformance or production acceptance.
""")

    write("ACCEPTANCE.md", """# GLAZE UI V1.1 Acceptance

GLAZE UI V1.1 / 1.1.0 is the current Stable design-system release after completion of the governed release-finalization sequence.

Stable source acceptance includes deterministic V1.1 contracts, project-owner optical approval, exact source-pinned web visual regression, inherited V1 semantic/material/accessibility validation, and fresh framework-native Android handheld emulator evidence.

The Android evidence is intentionally bounded and does not claim OEM-wide, physical-device, TalkBack, signing/distribution, or downstream application acceptance.

No downstream GoreeCloud application becomes V1.1-conformant or production-eligible automatically. Each consumer must explicitly target 1.1.0 and satisfy its own exact-revision acceptance boundary.
""")

    write("acceptance/v1.1-stable.md", f"""# GLAZE UI V1.1 — Stable Source Acceptance

**Version:** `1.1.0`  
**Product:** GLAZE UI V1.1  
**Source lifecycle represented by this promotion:** Stable  
**Human optical approval:** Approved by GoreeCloud project owner on {TODAY}

## Exact pre-promotion release evidence

- Release-candidate source revision: `{rc_revision}`
- Release-evidence workflow run: `{evidence_run_id}`
- Five human-approved web reference scenes reproduced their source-pinned SHA-256 hashes exactly.
- Fresh framework-native Android handheld reference built and executed on the exact release-candidate revision.
- Android Light preserved 48dp Primary and Secondary targets and native interaction.
- Android Dark + Reduced Transparency suppressed atmosphere and preserved the 48dp target floor.
- Android Deep Dark + 200% text + Touch Assistance preserved 56dp Primary and Secondary targets with scroll-reachable content.
- Existing semantic-color, icon, material, layout, and V1/V1.1 compatibility workflows passed on the release-candidate revision.

## Stable source authority

- [x] `VERSION` is `1.1.0`.
- [x] Lifecycle registry proposes GLAZE UI V1.1 / 1.1.0 as current Stable.
- [x] Official V1.1 contract and Stable machine contracts exist.
- [x] Stable web and runtime entrypoints exist.
- [x] Stable visual baseline authority points to the project-owner-approved V1.1 pixels.
- [x] Consumer registry requires 1.1.0 while keeping every consumer independently acceptance-gated.
- [x] Conformance-evidence schema targets 1.1.0.
- [x] Public Design Center source is synchronized to V1.1 Stable.

## Release-finalization gates

- [ ] Exact Stable-promotion PR head passes all required workflows.
- [ ] Stable-promotion PR is reviewed and merged under GoreeCloud repository governance.
- [ ] Exact post-merge `main` revision passes required validation.
- [ ] Immutable `v1.1.0` tag points to the verified release commit.
- [ ] GitHub Release `v1.1.0` is created from that exact commit with release notes and source provenance.
- [ ] Canonical GoreeCloud Policy, Project Specification, Design Language Standard, and Change Log are synchronized to released V1.1 Stable.

## Boundaries

Stable design-system release does not imply downstream application conformance, application production acceptance, OEM-wide Android qualification, physical-device qualification, TalkBack certification, app signing/distribution acceptance, or production deployment of any consumer.

Candidate and Release Candidate artifacts remain immutable audit evidence and do not become current consumer entrypoints.
""")

    rc = read("acceptance/v1.1-release-candidate.md")
    rc = rc.replace("- [ ] Exact release-candidate revision passes the existing V1 baseline validators.", "- [x] Exact release-candidate revision passes the existing V1 baseline validators.")
    rc = rc.replace("- [ ] Exact release-candidate revision passes V1.1 specification and implementation validators.", "- [x] Exact release-candidate revision passes V1.1 specification and implementation validators.")
    rc = rc.replace("- [ ] Exact release-candidate revision reproduces all five human-approved source-pinned rendered PNG hashes.", "- [x] Exact release-candidate revision reproduces all five human-approved source-pinned rendered PNG hashes.")
    rc = rc.replace("- [ ] Fresh Android handheld framework-native reference builds on the exact release-candidate revision.", "- [x] Fresh Android handheld framework-native reference builds on the exact release-candidate revision.")
    rc = rc.replace("- [ ] Android Light uses the 48dp target floor and passes native interaction acceptance.", "- [x] Android Light uses the 48dp target floor and passes native interaction acceptance.")
    rc = rc.replace("- [ ] Android Dark + Reduced Transparency suppresses atmospheric treatment while preserving hierarchy and 48dp targets.", "- [x] Android Dark + Reduced Transparency suppresses atmospheric treatment while preserving hierarchy and 48dp targets.")
    rc = rc.replace("- [ ] Android Deep Dark + 200% text + Touch Assistance preserves the 56dp target floor.", "- [x] Android Deep Dark + 200% text + Touch Assistance preserves the 56dp target floor.")
    rc = rc.replace("- [ ] Android evidence bundle contains exact source revision, emulator build identity, screenshot hashes, and APK.", "- [x] Android evidence bundle contains exact source revision, emulator build identity, screenshot hashes, and APK.")
    rc = rc.replace("- [ ] No pre-reset Stable evidence is relabeled as V1.1 evidence.", "- [x] No pre-reset Stable evidence is relabeled as V1.1 evidence.")
    rc = rc.replace("- [ ] Release-candidate documentation remains explicit that V1.0 is current until Stable promotion.", "- [x] Release-candidate documentation remained explicit that V1.0 was current until this separate Stable promotion.")
    rc = rc.replace("- [ ] A dedicated Stable promotion commit changes current source authority coherently to `1.1.0`.", "- [x] This dedicated Stable promotion commit changes current source authority coherently to `1.1.0`.")
    rc = rc.replace("- [ ] `VERSION`, lifecycle registry, official contract, current web entrypoint, visual-regression authority, acceptance boundary, validators, and current documentation agree on V1.1.", "- [x] `VERSION`, lifecycle registry, official contract, current web entrypoint, visual-regression authority, acceptance boundary, validators, and current documentation agree on V1.1.")
    rc += f"\n\nExact RC evidence anchor: `{rc_revision}` · release-evidence workflow `{evidence_run_id}`.\n"
    write("acceptance/v1.1-release-candidate.md", rc)


def promote_validators() -> None:
    old_validator = read("scripts/validate_glaze_v1.py")
    write("scripts/validate_glaze_v1_0_reset.py", old_validator)
    write(
        "scripts/validate_glaze_v1.py",
        '#!/usr/bin/env python3\n"""Current GLAZE UI product validator. Delegates to the V1.1 Stable authority gate."""\nfrom validate_glaze_v1_1_stable import main\n\nif __name__ == "__main__":\n    raise SystemExit(main())',
    )

    candidate_validator = read("scripts/validate_glaze_v1_1_candidate.py")
    candidate_validator = replace_required(
        candidate_validator,
        'require(current_version == "1.0.0", "VERSION must remain 1.0.0 until governed V1.1 promotion")',
        'require(current_version in {"1.0.0", "1.1.0"}, "candidate history may be validated only during V1.0 pre-promotion or V1.1 Stable authority")',
        "candidate current-version boundary",
    )
    write("scripts/validate_glaze_v1_1_candidate.py", candidate_validator)

    ci = read(".github/workflows/ci.yml")
    ci = ci.replace("name: GLAZE UI V1.0 CI", "name: GLAZE UI V1.1 CI")
    ci = ci.replace("Validate GLAZE UI V1.0 reset contract", "Validate current GLAZE UI V1.1 Stable contract")
    ci = ci.replace("node --check js/glaze-v1.0.0.mjs", "node --check js/glaze-v1.1.0.mjs")
    write(".github/workflows/ci.yml", ci)


def promote_website() -> None:
    index = read("website/index.html")
    replacements = {
        "official GLAZE UI V1.0 reset baseline": "current Stable GLAZE UI V1.1 release",
        "GoreeCloud Design Center — GLAZE UI V1.0": "GoreeCloud Design Center — GLAZE UI V1.1",
        "/assets/glaze-v1.0.0.css": "/assets/glaze-v1.1.0.css",
        "Official reset baseline · GLAZE UI V1.0": "Current Stable · GLAZE UI V1.1",
        "GLAZE UI V1.0 is GoreeCloud's sole current visual and interaction design-system identity. Machine version <strong>1.0.0</strong> defines the reset baseline while production acceptance is re-earned with fresh exact-revision evidence.": "GLAZE UI V1.1 is GoreeCloud's current Stable visual and interaction design-system release. Machine version <strong>1.1.0</strong> adds the human-approved Deep Teal + Soft Amber optical system while preserving V1 semantics, accessibility, structure, and material boundaries.",
        "Explore V1": "Explore V1.1",
        "V1 component catalog": "V1.1 component catalog",
        "Official V1 identity does not equal production acceptance.": "Stable V1.1 identity does not equal downstream production acceptance.",
        "Production revalidation is required after the reset. Downstream applications must target GLAZE UI V1.0 explicitly and generate fresh application-specific evidence for the exact source revision they evaluate. Prior product evidence is historical only and cannot be inherited into a V1 acceptance claim.": "Downstream applications must target GLAZE UI V1.1 / 1.1.0 explicitly and generate fresh application-specific evidence for the exact source revision they evaluate. The Stable design-system release does not auto-upgrade consumers or inherit application production acceptance.",
        "Design Center · GLAZE UI V1.0": "Design Center · GLAZE UI V1.1",
        "Official reset baseline. Production revalidation required.": "Current Stable design-system release. Downstream conformance remains application-specific.",
    }
    for old, new in replacements.items():
        index = replace_required(index, old, new, f"website index marker {old[:36]}")
    write("website/index.html", index)

    not_found = read("website/404.html")
    not_found = not_found.replace("GLAZE UI V1.0", "GLAZE UI V1.1").replace("/assets/glaze-v1.0.0.css", "/assets/glaze-v1.1.0.css")
    write("website/404.html", not_found)

    build = read("website/build.py")
    build = replace_required(build, '    "glaze-v1.0.0.css",', '    "glaze-v1.1.0.css",\n    "glaze-v1.1.css",\n    "glaze-v1.1-appearance.css",\n    "glaze-v1.0.0.css",', "Design Center stable CSS publication")
    build = build.replace("official V1 entrypoint/layers", "official V1.1 entrypoint/layers and inherited V1 structural layers")
    build = build.replace("official GLAZE UI V1.0 source", "official GLAZE UI V1.1 Stable source")
    build = build.replace("isolated V1-only public publication boundary", "isolated current V1.1 public publication boundary")
    write("website/build.py", build)

    validator = read("website/validate.py")
    validator = validator.replace('    "assets/glaze-v1.0.0.css",', '    "assets/glaze-v1.1.0.css",\n    "assets/glaze-v1.1.css",\n    "assets/glaze-v1.1-appearance.css",\n    "assets/glaze-v1.0.0.css",')
    validator = validator.replace('entrypoint = (DIST / "assets" / "glaze-v1.0.0.css").read_text(encoding="utf-8")', 'entrypoint = (DIST / "assets" / "glaze-v1.1.0.css").read_text(encoding="utf-8")\nbase_entrypoint = (DIST / "assets" / "glaze-v1.0.0.css").read_text(encoding="utf-8")')
    validator = validator.replace('"GLAZE UI V1.0",', '"GLAZE UI V1.1",', 1)
    validator = validator.replace('"Machine version <strong>1.0.0</strong>",', '"Machine version <strong>1.1.0</strong>",')
    validator = validator.replace('"Production revalidation",', '"current Stable",')
    validator = validator.replace('"GLAZE UI V1.0",\n    "404 · GLAZE UI V1.0",\n    "/assets/glaze-v1.0.0.css",', '"GLAZE UI V1.1",\n    "404 · GLAZE UI V1.1",\n    "/assets/glaze-v1.1.0.css",')
    old_markers = '''for marker in (\n    '@import url("./glaze-v1.foundation.css")',\n    '@import url("./glaze-v1.components.css")',\n    '@import url("./glaze-v1.components.adaptive.css")',\n    '@import url("./glaze-v1.components.runtime.css")',\n    '@import url("./glaze-v1.structure.css")',\n    '@import url("./glaze-v1.overlay.css")',\n    '@import url("./glaze-v1.advanced.css")',\n    '@import url("./glaze-v1.visual-refinement.css")',\n    '@import url("./glaze-v1.optical-reachability.css")',\n):\n    if marker not in entrypoint:\n        raise SystemExit(f"V1 entrypoint missing required source layer: {marker}")'''
    new_markers = '''for marker in (\n    '@import url("./glaze-v1.0.0.css")',\n    '@import url("./glaze-v1.1.css")',\n    '@import url("./glaze-v1.1-appearance.css")',\n):\n    if marker not in entrypoint:\n        raise SystemExit(f"V1.1 Stable entrypoint missing required source layer: {marker}")\n\nfor marker in (\n    '@import url("./glaze-v1.foundation.css")',\n    '@import url("./glaze-v1.components.css")',\n    '@import url("./glaze-v1.components.adaptive.css")',\n    '@import url("./glaze-v1.components.runtime.css")',\n    '@import url("./glaze-v1.structure.css")',\n    '@import url("./glaze-v1.overlay.css")',\n    '@import url("./glaze-v1.advanced.css")',\n    '@import url("./glaze-v1.visual-refinement.css")',\n    '@import url("./glaze-v1.optical-reachability.css")',\n):\n    if marker not in base_entrypoint:\n        raise SystemExit(f"inherited V1 structural entrypoint missing required layer: {marker}")'''
    validator = replace_required(validator, old_markers, new_markers, "Design Center entrypoint validation block")
    validator = validator.replace("GLAZE UI V1.0 Design Center validation passed", "GLAZE UI V1.1 Design Center validation passed")
    validator = validator.replace("isolated V1 publication", "isolated Stable V1.1 publication")
    validator = validator.replace("exact-reset production-revalidation disclosure", "current Stable identity and downstream-conformance boundary")
    write("website/validate.py", validator)


def main() -> int:
    require(read("VERSION").strip() == "1.0.0", "Stable promotion must begin from the validated V1.1 RC while V1.0 is still current")
    rc_revision = os.environ.get("GLAZE_RC_REVISION", "").strip()
    evidence_run_id = os.environ.get("GLAZE_RC_WORKFLOW_RUN_ID", "").strip()
    require(re.fullmatch(r"[0-9a-f]{40}", rc_revision) is not None, "GLAZE_RC_REVISION must be the exact successful RC head SHA")
    require(bool(evidence_run_id), "GLAZE_RC_WORKFLOW_RUN_ID is required")
    actual = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True, capture_output=True, check=True).stdout.strip()
    require(actual == rc_revision, f"promotion checkout mismatch: actual={actual} evidence={rc_revision}")

    rc_record = load("contracts/v1.1/release-candidate.rc.json")
    require(rc_record["humanOpticalApproval"]["status"] == "approved", "human optical approval is required")
    require(rc_record["intendedReleaseVersion"] == STABLE_VERSION, "RC intended release version drift")

    promote_machine_contracts(rc_revision, evidence_run_id)
    promote_entrypoints()
    promote_current_authority()
    promote_docs(rc_revision, evidence_run_id)
    promote_validators()
    promote_website()

    print(f"Prepared atomic Stable source promotion from exact RC {rc_revision} / workflow {evidence_run_id}")
    print("Boundary: merge, post-merge validation, immutable tag, GitHub Release, and canonical GoreeCloud documentation synchronization remain required before final Stable completion is claimed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
