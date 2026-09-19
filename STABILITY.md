# GLAZE UI Stability Contract

**Current Stable authority:** GLAZE UI V1.6 / `1.6.0`  
**Immediate rollback baseline:** GLAZE UI V1.5 / `1.5.1`  
**Current lifecycle source:** `registry/lifecycle.json`

## Stability principles

1. Stable behavior fails closed when required evidence is absent.
2. Accessibility and semantic clarity outrank decorative effects.
3. Exact-revision evidence is required for qualification claims that depend on human, runtime, device, artifact, or platform observations.
4. Lifecycle scope decisions must never manufacture missing evidence.
5. Presentation adaptation must preserve capability truth, authorization boundaries, task continuity, and understandable state.
6. Glaze UI must not infer authorization, grant permission or consent, or automatically execute navigation, consequential actions, or fallbacks.
7. Platform-native claims require representative platform-native evidence.
8. Downstream product readiness remains product-specific and repository-local.
9. Recovery preserves previous known-good Stable releases and exact source history.

## Current V1.6.0 boundary

V1.6.0 is the current shared Stable release. The frozen qualification source `c7509c79256b04b0aa67cb9dd0737d7588e0ae4a` completed the governed matrix at **24 verified / 0 unverified / 0 not applicable**. Qualification evidence integration is `354f5759385c28596fcfec26a3ad525e89fb1c35`.

Final security and release evidence is bound to accepted release source `a7180679ea851389e0f3004515f9a25f420e716d` / tree `9ff0bf7a5f9d64f109d99bf4b76b81bd2a162268`. The exact published source/runtime archive SHA-256 is `687268b5eb76917eccae9d935ffa1bead333d5dee50b6098e996a3f44cee50af`.

Controlled tag `v1.6.0` resolves to the accepted release source and GitHub Release `392095913` contains only the accepted archive, checksum manifest, CycloneDX 1.5 SBOM, and provenance. Post-publication readback verified that released bytes match the security-accepted bytes. GitHub reports its optional release `immutable` flag as false; GoreeCloud control is provided by exact tag/source binding, protected no-rebuild publication, fixed digests, byte readback, and no-rewrite governance.

## Rollback and historical releases

V1.5.1 is the immediate known-good Stable rollback baseline using `js/glaze-v1.5.1.mjs`. Its exact qualification and Stable acceptance remain historical provenance. V1.6.0-rc.1 is retained as superseded Release Candidate provenance. Earlier releases remain retained according to lifecycle records.

## Consumer boundary

No downstream application or website becomes `1.6.0`-conformant merely because the shared design system is Stable. Every consumer must complete fresh repository-local V1.6 adoption and acceptance evidence for its supported platforms, runtime, accessibility, integrations, and production boundary.

## Production boundary

GLAZE UI is a source-distributed shared library and owns no independent service/backend deployment. Its applicable Stable production/release boundary is controlled publication and artifact acceptance, which is complete. Downstream application deployment and production acceptance remain separate.

Glaze Motion remains separately governed unless a later Stable Glaze UI contract explicitly incorporates it.
