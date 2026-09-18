# GLAZE UI V1.5 — Enforcement

The current Glaze UI enforcement and consumer-conformance target is **GLAZE UI V1.5** (`1.5.1`). `registry/lifecycle.json` and `VERSION` are the live lifecycle authorities. GLAZE UI V1.5.0 (`1.5.0`) remains the immediate known-good Stable rollback baseline and historical provenance; it does not override the current target.

Enforcement fails closed when required V1 evidence is absent, stale, unsupported, or bound to a different revision. Consumers must not claim conformance from copied tokens, renamed assets, screenshots alone, a platform declaration, or the shared V1.5.1 Stable promotion itself. Required checks include exact-revision contract validation, accessibility, supported form factors, rendered/native evidence where applicable, applicable performance budgets, authority-boundary preservation, and product-specific production acceptance.

The V1.5.1 shared design-system qualification is governed by `contracts/v1.5.1/stable-scope.json` and `acceptance/v1.5.1-stable.md`. The two qualification expansions `performance-representative-budget` and `platform-posture-continuity` are accepted for their reviewed shared environments and evidence anchors. Those bounded shared passes do not automatically establish consumer-specific performance, platform, physical-device, deployment, or production acceptance.

The V1.5.0, V1.4.1, and earlier Stable qualification remains valid historical shared-design-system evidence for each exact accepted scope. It does not automatically certify a consumer application's implementation, native integration, physical-device behavior, deployment, signing, store publication, production lifecycle state, or current V1.5.1 conformance.

Historical V1.0–V1.5.0 release, Candidate, qualification, and rollback records remain provenance. They must remain auditable but may not override live `VERSION` / lifecycle authority, manufacture current acceptance, or silently upgrade downstream consumers.

Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Identity, GoreeCloud Mesh, application, service, platform, policy, and other authoritative systems retain authority over their own truth domains. Glaze UI enforcement governs presentation-system conformance only and must not create authorization, security, privacy, execution, deployment, or production truth on behalf of those systems.
