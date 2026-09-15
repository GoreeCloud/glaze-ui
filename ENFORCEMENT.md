# GLAZE UI V1.4 — Enforcement

The current Glaze UI enforcement and consumer-conformance target is **GLAZE UI V1.4** (`1.4.1`). `registry/lifecycle.json` and `VERSION` are the current lifecycle authorities. GLAZE UI V1.4.0 (`1.4.0`) remains the immediately preceding known-good Stable rollback baseline and does not override the current target.

Enforcement fails closed when required V1 evidence is absent, stale, or bound to a different revision. Consumers must not claim conformance from copied tokens, renamed assets, screenshots alone, a platform declaration, or the shared V1.4.1 Stable promotion itself. Required checks include exact-revision contract validation, accessibility, supported form factors, rendered/native evidence where applicable, performance budgets, and product-specific production acceptance.

The V1.4.1 human/manual/physical qualification is accepted for the supported shared design-system claim only. It does not automatically certify a consumer application's implementation, native integration, physical-device behavior, deployment, signing, store publication, or production lifecycle state.

Historical V1.0–V1.4.0 release, Candidate, and qualification records remain provenance and rollback evidence. They do not override live `VERSION` / lifecycle authority or manufacture current acceptance.
