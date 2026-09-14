# GLAZE UI V1.4 — Enforcement

The current Glaze UI enforcement and consumer-conformance target is **GLAZE UI V1.4 — Optical Intelligence** (`1.4.0`). `registry/lifecycle.json` and `VERSION` are the current lifecycle authorities. GLAZE UI V1.3 (`1.3.0`) remains the immediate known-good Stable rollback baseline and does not override the current target.

Enforcement fails closed when required evidence is absent, stale, scoped to a different platform, or bound to incompatible source state. Consumers must not claim conformance from copied tokens, renamed assets, screenshots alone, a platform declaration, or the shared V1.4 Stable promotion itself. Required checks include current-target validation, accessibility, supported form factors, rendered/native evidence where applicable, performance budgets, and product-specific release acceptance.

The V1.0 reset and V1.1/V1.2/V1.3 releases remain historical audit and rollback provenance. Candidate-suffixed source files retained under promoted releases are implementation provenance, not current lifecycle authority. Current lifecycle truth comes from `VERSION`, `registry/lifecycle.json`, the current release contract, Stable entrypoints, and current acceptance record.

V1.4.0 machine-verifiable Stable behavior includes the bounded local Optical Engine and its accessibility fallbacks. Human optical review, manual assistive-technology verification, representative physical-device/native-platform qualification, real-device performance validation, and subjective polish are explicitly assigned to V1.4.1 and must not be represented as passed V1.4.0 evidence.

No global "uses Glaze UI" state is sufficient for a product Stable claim. Every consumer and every claimed user-facing platform must establish its own accepted current-Stable evidence, while overall product lifecycle authority remains independent of Glaze UI conformance.
