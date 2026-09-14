# GLAZE UI V1.4 Adoption

The current Glaze UI adoption target is **GLAZE UI V1.4 — Optical Intelligence** (`1.4.0`). GLAZE UI V1.3 (`1.3.0`) remains the immediate known-good Stable rollback baseline.

Adoption requires repository-local implementation evidence, exact-revision validation, rendered or native acceptance as applicable, accessibility acceptance, supported-form-factor validation, and product-specific release approval. Importing tokens, copying styles, changing a version label, or matching screenshots does not establish conformance.

Consumers remain fail-closed in `consumers/registry.json` until current-Stable evidence is recorded for the relevant consumer scope. The shared V1.4 Stable promotion does not grant downstream conformance automatically, and a single accepted platform does not authorize another platform by implication.

V1.4 adoption should use `css/glaze-v1.4.0.css` and `js/glaze-v1.4.0.mjs` where applicable. Consumers that use the Optical Engine must preserve its bounded accessibility behavior and may only supply contextual signals through consumer-local adapters accepted by their own Privacy Shield and Wardveil Security boundaries.

Human/manual/physical-device qualification assigned to V1.4.1 remains separate from V1.4.0 machine-verifiable Stable evidence and separate from each consumer's own product acceptance. A consumer must not mark itself Stable merely because the shared Glaze UI release is Stable.
