# GLAZE UI V1.5 — Enforcement

The current Glaze UI enforcement and consumer-conformance target is **GLAZE UI V1.5** (`1.5.0`). `registry/lifecycle.json` and `VERSION` are the live lifecycle authorities. GLAZE UI V1.4.1 (`1.4.1`) remains the immediately preceding known-good Stable rollback baseline and historical provenance; it does not override the current target.

Enforcement fails closed when required V1 evidence is absent, stale, unsupported, or bound to a different revision. Consumers must not claim conformance from copied tokens, renamed assets, screenshots alone, a platform declaration, or the shared V1.5.0 Stable promotion itself. Required checks include exact-revision contract validation, accessibility, supported form factors, rendered/native evidence where applicable, applicable performance budgets, authority-boundary preservation, and product-specific production acceptance.

The V1.5.0 shared design-system qualification accepts the governed bounded release scope recorded in `contracts/v1.5/stable-scope.json` and `acceptance/v1.5-stable.md`. The two qualification expansions `performance-representative-budget` and `platform-posture-continuity` are deliberately assigned to V1.5.1 and are not V1.5.0 passes. Consumers that make claims within those areas retain their own applicable evidence obligations, and V1.5.1 remains Development until representative evidence is reviewed and durably accepted.

The V1.4.1 human/manual/physical qualification remains valid historical shared-design-system evidence for its exact accepted scope. It does not automatically certify a consumer application's implementation, native integration, physical-device behavior, deployment, signing, store publication, production lifecycle state, or current V1.5.0 conformance.

Historical V1.0–V1.4.1 release, Candidate, qualification, and rollback records remain provenance. They must remain auditable but may not override live `VERSION` / lifecycle authority, manufacture current acceptance, or silently upgrade downstream consumers.

Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Identity, GoreeCloud Mesh, application, service, platform, policy, and other authoritative systems retain authority over their own truth domains. Glaze UI enforcement governs presentation-system conformance only and must not create authorization, security, privacy, execution, deployment, or production truth on behalf of those systems.
