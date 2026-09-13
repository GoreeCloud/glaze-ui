# GLAZE UI V1.4 — Enforcement

The current Glaze UI enforcement and consumer-conformance target is **GLAZE UI V1.4 — Optical Material & Chromatic Depth** (`1.4.0`). `registry/lifecycle.json` and `VERSION` are the current lifecycle authorities. GLAZE UI V1.3 (`1.3.0`) remains the immediate Stable rollback baseline and does not override the current target.

Enforcement fails closed when required V1 evidence is absent, stale, or bound to a different revision. Consumers must not claim conformance from copied tokens, renamed assets, screenshots alone, a platform declaration, implementation-stage `.candidate` imports, or the shared V1.4 Stable promotion itself. Required checks include exact-revision contract validation, deterministic fallback behavior, accessibility, supported form factors, rendered/native evidence where applicable, performance budgets, and product-specific production acceptance.

The V1.0 reset established the V1 namespace and remains historical baseline evidence. V1.2 and V1.3 Stable releases, along with Candidate/promoted-source lineage, remain historical provenance and rollback evidence. Live lifecycle authority is V1.4 Stable `1.4.0`.

Human optical/material review, manual interaction and assistive-technology verification, representative workflows, physical-device/OEM/compositor qualification, native-renderer observation, and physical-device performance/power verification are explicitly transferred to V1.4.1. They remain deferred/unverified and must not be represented as passed V1.4.0 evidence.
