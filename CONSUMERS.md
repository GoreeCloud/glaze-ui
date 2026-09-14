# GLAZE UI V1.4 — Optical Intelligence Consumers

The machine-readable consumer registry authority for current consumer state is `consumers/registry.json`.

The required target for every applicable GoreeCloud user-facing consumer is **GLAZE UI V1.4 — Optical Intelligence** (`1.4.0`). V1.4.0 is Official, Stable, and consumer-eligible. Fresh repository-local V1.4 adoption and acceptance evidence is required for each consumer; prior V1.3, V1.2, V1.1, V1.0, Candidate, or pre-reset evidence does not automatically establish current conformance.

No consumer is production-eligible merely because GLAZE UI V1.4 is the current Stable platform target. Each application or service must independently satisfy its applicable rendered, interaction, accessibility, native/platform, product, performance, rollback, and release acceptance gates while preserving the authority of the system that owns the underlying state being presented.

## Stable consumer entrypoints

- Web: `css/glaze-v1.4.0.css`
- Runtime: `js/glaze-v1.4.0.mjs`
- Contract: `GLAZE_UI_V1_4.md`
- Migration guide: `MIGRATION_V1_3_TO_V1_4.md`

V1.4 is additive over V1.3. Consumers may opt into the Glaze Optical Engine, but they must not collect new user/environment data merely to drive visual effects. Context signals remain governed by consumer-local Wardveil Security and Privacy Shield authority.

## Registry status vocabulary

- `adoption-required` — the consumer has not yet supplied accepted current-Stable V1.4 evidence. It may retain superseded historical target/evidence fields as migration provenance, but it does not satisfy the current required target.
- `unverified` — the current consumer state has not yet been verified against the V1.4 contract.
- `accepted-v1` — the consumer has completed governed product-specific acceptance for the current Stable contract at an exact 40-character source revision with an evidence reference. This state still does not make the overall product production-eligible; product lifecycle/release authority remains independent.

An accepted current consumer must target exactly the current Stable version and identify the exact accepted source revision and evidence record.

## Mandatory current-Stable gate

GoreeCloud consumer repositories should adopt the reusable current-Stable gate defined by `.github/workflows/current-stable-consumer-gate.yml` and keep a repository-local `.goreecloud/glaze-ui-conformance.json` manifest based on `templates/downstream-current-stable-conformance.template.json`.

The complete contract is documented in `CURRENT_STABLE_ENFORCEMENT.md`.

Development validation requires the manifest to target the central current Stable Glaze UI version. Stable-claim validation is stricter: the consumer must explicitly request a Stable claim, enumerate its complete user-facing platform scope, mark every enumerated platform accepted, and bind every accepted platform to repository-local evidence by SHA-256.

A product must not be considered or marked Stable when this current-Stable Glaze gate fails. Passing the gate is necessary for a Stable claim but remains insufficient by itself for overall production or product lifecycle promotion.

When a newer Glaze UI release becomes Official Stable, older consumer acceptance becomes migration provenance. The next consumer gate run must target the newly current Stable version before a new Stable claim can pass.

## V1.4.1 relationship

Human optical review, subjective polish assessment, manual assistive-technology verification, representative physical-device/native-platform qualification, and representative real-device performance qualification are assigned to V1.4.1 by owner direction. Those checks are not represented as passed V1.4.0 evidence.

The V1.4.1 carry-forward does not weaken consumer-specific acceptance. Consumers may only claim the platforms and capabilities they independently validate, and consumer repositories may retain stricter local release requirements.
