# GLAZE UI V1.4 — Optical Material & Chromatic Depth Consumers

The machine-readable consumer registry authority for current consumer state is `consumers/registry.json`.

The required target for every applicable GoreeCloud user-facing consumer is **GLAZE UI V1.4 — Optical Material & Chromatic Depth** (`1.4.0`). Fresh repository-local V1.4 adoption and acceptance evidence is required for each consumer; prior V1.3, V1.2, V1.1, V1.0, Candidate, or pre-reset evidence remains useful migration/history evidence but does not automatically establish current conformance.

No consumer is production-eligible merely because GLAZE UI V1.4 is the current Stable platform target. Each application or service must independently satisfy its applicable rendered, interaction, accessibility, native/platform, product, performance, rollback, and release acceptance gates while preserving the authority of the system that owns the underlying state being presented.

## Stable consumer entrypoints

- Web: `css/glaze-v1.4.0.css`
- Runtime: `js/glaze-v1.4.0.mjs`
- Contract: `GLAZE_UI_V1_4.md`
- Acceptance: `acceptance/1.4.0.md`
- Deferred human qualification boundary: `acceptance/v1.4-deferred-qualification.md`

Historical `.candidate` filenames imported by the Stable runtime are preserved source-stage provenance. They do not make the aggregate V1.4.0 release a Candidate.

## Registry status vocabulary

- `adoption-required` — the consumer has not yet supplied accepted current-Stable V1.4 evidence. It may retain historical target/evidence fields as migration provenance, but it does not satisfy the current required target.
- `unverified` — the current consumer state has not yet been verified against the V1.4 contract.
- `accepted-v1` — the consumer has completed governed product-specific acceptance for the current Stable contract at an exact 40-character source revision with an evidence reference. This state still does not make the overall product production-eligible; product lifecycle/release authority remains independent.

An accepted current consumer must target exactly the current Stable version and identify the exact accepted source revision and evidence record.

## V1.4.1 relationship

Human optical/material review, manual keyboard/focus review, human-operated assistive-technology qualification, subjective presentation review, representative human workflows, physical-device/OEM/compositor qualification, actual native-renderer observation, physical-device production performance/power observation, and other shared design-system human verification have been moved to V1.4.1 by owner directive.

Those items remain deferred/unverified rather than passed V1.4.0 evidence. This shared design-system deferral does not weaken consumer-specific acceptance: a consumer may claim only the platforms and capabilities it independently validates.

GLAZE UI V1.3 / `1.3.0` remains the immediately preceding Stable rollback baseline for consumers that have not intentionally migrated to V1.4.0.
