# GLAZE UI V1.6 — Enforcement

The current Glaze UI enforcement and consumer-conformance target is **GLAZE UI V1.6** (`1.6.0`). `registry/lifecycle.json` and `VERSION` are the live lifecycle authorities. GLAZE UI `1.5.1` remains the immediate known-good Stable rollback baseline and historical provenance; it does not override the current target.

Enforcement fails closed when required V1.6 evidence is absent, stale, unsupported, or bound to a different revision. Consumers must not claim conformance from copied tokens, renamed assets, screenshots alone, a platform declaration, or the shared V1.6.0 Stable promotion itself. Required checks include exact-revision contract validation, accessibility, supported form factors, rendered/native evidence where applicable, applicable performance budgets, authority-boundary preservation, and product-specific production acceptance.

The shared design-system qualification is governed by `acceptance/v1.6-stable.json`, `acceptance/v1.6-stable-qualification-review.json`, and the immutable `v1.6.0` publication/readback evidence. The shared matrix is 24 verified / 0 unverified / 0 not applicable. These passes do not automatically establish consumer-specific performance, platform, physical-device, deployment, or production acceptance.

Historical V1.5.1 and earlier release/qualification records remain auditable provenance. Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Identity, GoreeCloud Mesh, GoreeCloud Policy, applications, services, and other authoritative systems retain authority over their own truth domains. Glaze UI enforcement governs presentation-system conformance only.
