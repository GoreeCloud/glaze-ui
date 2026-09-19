# GLAZE UI V1.6 — Enforcement

The current Glaze UI enforcement and consumer-conformance target is **GLAZE UI V1.6** (`1.6.0`). `registry/lifecycle.json` and `VERSION` are the live lifecycle authorities. GLAZE UI `1.5.1` remains the immediate known-good Stable rollback baseline.

Enforcement fails closed when required V1.6 evidence is absent, stale, unsupported, or bound to a different revision. Consumers must not claim conformance from copied tokens, renamed assets, screenshots alone, a platform declaration, or the shared V1.6.0 Stable promotion itself.

The shared V1.6.0 qualification is governed by `acceptance/v1.6-stable.json`, `acceptance/v1.6-stable-qualification-review.json`, and `contracts/v1.6/stable-release.json`. The frozen shared matrix is complete at 24 verified / 0 unverified / 0 not applicable. Final security acceptance and the controlled published artifact are separately bound to exact source revision `a7180679ea851389e0f3004515f9a25f420e716d`.

Required consumer checks include exact-revision contract validation, accessibility, supported form factors, rendered/native evidence where applicable, applicable performance budgets, authority-boundary preservation, migration/rollback evidence, and product-specific release/production acceptance. A Stable Glaze UI release never makes a consumer production-eligible by inheritance.

V1.5.1 and earlier Stable/Candidate evidence remains historical provenance. Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Identity, GoreeCloud Mesh, GoreeCloud Policy, GoreeCloud Observability, applications, services, and platforms retain authority over their own truth domains. Glaze UI enforcement governs presentation-system conformance only.
