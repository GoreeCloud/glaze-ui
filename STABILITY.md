# GLAZE UI Stability Contract

**Current Stable authority:** GLAZE UI V1.6 / `1.6.0`  
**Immediate rollback baseline:** GLAZE UI V1.5 / `1.5.1`  
**Current lifecycle source:** `registry/lifecycle.json`

## Stability principles

1. Stable behavior fails closed when required evidence is absent.
2. Accessibility and semantic clarity outrank decorative effects.
3. Exact-revision evidence is required for qualification claims that depend on human, runtime, device, platform, security, or release observations.
4. Lifecycle scope decisions must never manufacture missing evidence.
5. Presentation adaptation preserves capability truth, authorization boundaries, task continuity, and understandable state.
6. Glaze UI does not infer authorization, grant permission or consent, or automatically execute navigation, consequential actions, or fallbacks.
7. Downstream product readiness remains product-specific and repository-local.
8. Recovery preserves previous known-good Stable releases and exact source/release history.

## Current V1.6.0 boundary

GLAZE UI V1.6.0 is the current Official Stable shared presentation-system release. Its governed qualification matrix is **24 verified / 0 unverified / 0 not applicable**. Final Stable security acceptance passed for exact released source `a7180679ea851389e0f3004515f9a25f420e716d` and tree `9ff0bf7a5f9d64f109d99bf4b76b81bd2a162268`.

Authoritative `main` is protected by active ruleset `23699829` with no bypass actors, pull-request promotion, strict/up-to-date required checks, conversation resolution, deletion protection, force-push protection, and merge-only integration.

The accepted V1.6.0 source/runtime artifact was built deterministically, passed checksum/SBOM/provenance validation and extracted-artifact secret scanning, was published without rebuild under immutable tag `v1.6.0` and GitHub Release `392095913`, and passed byte-for-byte publication readback.

## Rollback and historical releases

GLAZE UI `1.5.1` is the immediate known-good Stable rollback target using `js/glaze-v1.5.1.mjs`. V1.6.0-rc.1 is retained as superseded Release Candidate provenance. V1.5.1, V1.5.0, V1.4.1, and earlier accepted releases remain preserved historical evidence for their exact scopes.

## Consumer boundary

No downstream application or website becomes `1.6.0`-conformant merely because the shared design system is Stable. Each consumer must adopt the current Stable target and complete fresh repository-local V1.6 acceptance appropriate to its supported platforms, runtime, accessibility, integrations, privacy/security authority, rollback, and production boundary.

## Deployment and production boundary

GLAZE UI is a source-distributed shared library and has no independently deployed service/backend. Its applicable release-acceptance boundary is immutable publication and readback, which passed. Application deployment and production acceptance remain downstream product responsibilities.

Glaze Motion remains separately governed unless a later Stable Glaze UI contract explicitly incorporates it.
