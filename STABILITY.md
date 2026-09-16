# GLAZE UI Stability Contract

**Current Stable authority:** GLAZE UI V1.5 — Contextual + Capability Awareness / `1.5.0`  
**Immediate rollback baseline:** GLAZE UI V1.4.1 / `1.4.1`  
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

## Current V1.5.0 boundary

V1.5.0 stabilizes the reviewed Context + Capability Awareness presentation layer against exact implementation anchor `ee1032a0822ab8e103f8afe48e5c1859fde65cc9`.

The governed V1.5.0 Stable scope contains 16 completed review obligations. The project owner explicitly moved two further qualification expansions into V1.5.1:

- `performance-representative-budget`;
- `platform-posture-continuity`.

This is a versioned scope decision, not a PASS or waiver. V1.5.0 does not claim measurement against the new Glaze UI Performance Budget v1.0 and does not claim representative foldable/posture target-runtime acceptance.

The exact boundary is recorded in `contracts/v1.5/stable-scope.json` and `acceptance/v1.5-stable.md`.

## Evidence continuity

The accepted V1.5 human and runtime observations remain bound to the exact revision on which they were performed. Stable promotion may carry those observations through a reviewed source-impact continuity assessment only when the behavior and authority implementation they cover remains unchanged.

The V1.5.0 public Stable runtime entrypoint wraps the unchanged reviewed V1.5 implementation and promotes version/lifecycle identity. It does not create new operational authority or silently rebind missing evidence.

## Rollback and historical releases

GLAZE UI V1.4.1 / `1.4.1` remains the immediate known-good Stable rollback baseline. V1.4.0, V1.3.0, earlier Stable releases, and the V1.0 reset-era contract remain retained as historical provenance according to repository lifecycle records.

## Consumer boundary

No downstream application or website becomes V1.5.0-conformant merely because the shared design system is Stable. Each consumer must adopt the current Stable target and complete repository-local acceptance appropriate to its supported platforms, runtime, accessibility, integrations, and production boundary.

## Planned V1.5.1 hardening

`GLAZE_UI_V1_5_1_HARDENING.md` governs the remaining representative numeric performance-budget measurement and posture/fold target-runtime qualification. Neither is considered completed until real exact-revision evidence exists for a V1.5.1 candidate.

Glaze Motion remains separately governed unless a later Stable Glaze UI contract explicitly incorporates it.
