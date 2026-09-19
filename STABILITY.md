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

Verified shared passes include candidate identity, 24/24 qualification evidence, the nine-system Release Candidate readiness review, rendered/human/assistive-technology evidence, bounded representative performance, rollback to V1.5.1, immutable GitHub Action pin enforcement, and current repository-front-door documentation.

Stable remains blocked while the recorded unresolved controls remain open, including authoritative default-branch protection, current machine Platform Contract applicability/schema alignment, exact-candidate secret/history scanning, dependency/supply-chain security evidence, final release-security acceptance, final artifact/provenance/publication boundary, and applicable production-acceptance disposition. Canonical Drive task/changelog reconciliation is verified complete.

No Stable tag, GitHub Release, consumer migration, deployment, production-readiness claim, or production-acceptance claim is authorized by this review.
