# GLAZE UI V1.4 Adoption

The current Glaze UI adoption target is **GLAZE UI V1.4 — Optical Material & Chromatic Depth** (`1.4.0`). GLAZE UI V1.3 (`1.3.0`) remains available as the immediate Stable rollback baseline.

Adoption requires repository-local implementation evidence, exact-revision validation, rendered or native acceptance as applicable, accessibility acceptance, supported-form-factor validation, performance/fallback validation, and product-specific production approval. Importing tokens, copying styles, wrapping the Stable runtime, or changing a version label does not establish consumer conformance by itself.

All consumers remain fail-closed in `consumers/registry.json` until V1.4-specific evidence is recorded for the exact consumer revision. The shared V1.4 Stable promotion does not grant downstream conformance or production eligibility automatically.

Human/manual/subjective/assistive-technology/physical-device qualification deferred from the shared V1.4.0 release is tracked under V1.4.1. That deferral is not passed V1.4.0 evidence and does not substitute for consumer-specific acceptance.

Consumers should migrate through `css/glaze-v1.4.0.css` and `js/glaze-v1.4.0.mjs` rather than importing implementation-stage `.candidate` modules directly unless a governed integration explicitly requires a lower-level contract.
