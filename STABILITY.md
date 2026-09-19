# GLAZE UI Stability Contract

**Current Stable authority:** GLAZE UI V1.5 — Contextual + Capability Awareness / `1.5.1`  
**Immediate rollback baseline:** GLAZE UI V1.5 / `1.5.0`  
**Current lifecycle source:** `registry/lifecycle.json`

## Stability principles

1. Stable behavior fails closed when required evidence is absent.
2. Accessibility and semantic clarity outrank decorative effects.
3. Exact-revision evidence is required for qualification claims that depend on human, runtime, device, or platform observations.
4. Lifecycle scope decisions must never manufacture missing evidence.
5. Presentation adaptation must preserve capability truth, authorization boundaries, task continuity, and understandable state.
6. Glaze UI must not infer authorization, grant permission or consent, or automatically execute navigation, consequential actions, or fallbacks.
7. Platform-native claims require representative platform-native evidence.
8. Downstream product readiness remains product-specific and repository-local.
9. Recovery preserves previous known-good Stable releases and exact source history.

## Current V1.5.1 boundary

V1.5.1 is the qualification-hardening Stable patch for the reviewed Context + Capability Awareness presentation layer. The reviewed V1.5 implementation remains anchored to exact revision `ee1032a0822ab8e103f8afe48e5c1859fde65cc9`; V1.5.1 does not change its presentation or operational-authority behavior.

The governed V1.5.1 Stable scope contains **18 accepted shared qualification obligations**: the sixteen V1.5.0 obligations plus two independently reviewed V1.5.1 expansions bound to exact Development revision `5b59d0e36950d737dba35b58ae58058684e0831b`:

- `performance-representative-budget` — review authority PR #230 comment `5697516074`;
- `platform-posture-continuity` — review authority PR #230 comment `5705230782`, using approved target-runtime authority `GCU-ADR-GLAZE-V151-POSTURE-TR-001`.

The exact Stable boundary is recorded in `contracts/v1.5.1/stable-scope.json` and `acceptance/v1.5.1-stable.md`.

## Evidence continuity

The V1.5.1 performance and posture observations remain bound to the exact revision on which they were performed. Stable promotion carries those observations only through fail-closed source-impact continuity proving that qualification-sensitive sources remain byte-identical to `5b59d0e36950d737dba35b58ae58058684e0831b`.

The V1.5.1 public Stable runtime entrypoint wraps the unchanged V1.5.0 Stable runtime and promotes patch identity only. It does not create new operational authority or silently rebind evidence.

## Rollback and historical releases

GLAZE UI V1.5 / `1.5.0` is the immediate known-good Stable rollback baseline. V1.5.1-rc.1 is retained as superseded Release Candidate provenance. V1.4.1, V1.4.0, V1.3.0, earlier Stable releases, and the V1.0 reset-era contract remain retained as historical provenance according to repository lifecycle records.

## Consumer boundary

No downstream application or website becomes `1.5.1`-conformant merely because the shared design system is Stable. Each consumer must adopt the current Stable target and complete fresh repository-local V1.5 adoption and acceptance evidence appropriate to its supported platforms, runtime, accessibility, integrations, and production boundary.

## Publication and deployment boundary

Stable design-system authority does not automatically establish an immutable `v1.5.1` tag, GitHub Release, deployment, production acceptance, or downstream application acceptance. Those remain separate governed transitions.

Glaze Motion remains separately governed unless a later Stable Glaze UI contract explicitly incorporates it.

## Active V1.6 Stable qualification review

GLAZE UI V1.6 / `1.6.0-rc.1` is the active governed Release Candidate. Its shared qualification matrix is complete at 24 verified / 0 unverified / 0 not applicable, but that qualification completeness does not by itself satisfy the higher Stable gate.

The current fail-closed Stable review is recorded in `acceptance/v1.6-stable-qualification-review.json` and its machine gate is `scripts/verify_glaze_v1_6_stable_qualification_review.mjs`.

**Current decision: blocked — remain Release Candidate.**

Verified shared passes include candidate identity, 24/24 qualification evidence, the nine-system Release Candidate readiness review, rendered/human/assistive-technology evidence, bounded representative performance, rollback to V1.5.1, immutable GitHub Action pin enforcement, current repository-front-door documentation, canonical Drive task/changelog reconciliation, the Contract 0.4 shared-library machine declaration, the exact-candidate secret/Git-history scan, remediated selected dependency/supply-chain evidence, and the shared-library production-applicability disposition.

Authoritative default-branch protection is now verified complete through active GitHub ruleset `23699829` (**GoreeCloud Main Branch Production**) targeting the default branch with no bypass actors, pull-request integration, strict/up-to-date required checks, conversation resolution, deletion protection, non-fast-forward/force-push protection, and merge-only integration.

Final Stable security acceptance is now verified complete for exact protected source `a7180679ea851389e0f3004515f9a25f420e716d` and its exact unpublished 1.6.0 artifact bytes. The accepted release archive SHA-256 is `687268b5eb76917eccae9d935ffa1bead333d5dee50b6098e996a3f44cee50af`; the CycloneDX 1.5 SBOM SHA-256 is `3ffbb8bfe372d20642cd58f34fc0faaec2a74657d90e10742b75c5adf52dde82`; and the provenance SHA-256 is `711b58d5854085fb104dbae8bb5e7f7cfe4e8846e2e1fb314441c5212821ddd8`. The full Git-history/selected-dependency security run and all 31 post-merge workflows on that exact source passed.

Stable remains blocked by one recorded release boundary: immutable publication/readback followed by final exact-candidate Stable qualification and lifecycle promotion. Controlled publication of **only** the accepted bytes is authorized under `v1.6.0`, but the GitHub Release must remain explicitly prerelease / Release Candidate until the final Stable gate passes.

The governed next sequence is fail-closed: publish the accepted bytes without rebuilding; verify the annotated tag, prerelease record, archive/checksum/SBOM/provenance downloads and digests; then perform the final exact-candidate Stable qualification and lifecycle transition. Until that transition is verified, current Official/Stable remains 1.5.1, V1.6 remains 1.6.0-rc.1, and downstream consumer migration remains unauthorized.
