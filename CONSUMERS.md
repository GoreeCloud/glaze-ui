# GLAZE UI V1.5 — Contextual + Capability Awareness Consumers

The machine-readable consumer registry authority for current consumer state is `consumers/registry.json`.

The required target for every applicable GoreeCloud user-facing consumer is **GLAZE UI V1.5 — Contextual + Capability Awareness** (`1.5.0`). Fresh repository-local V1.5 adoption and acceptance evidence is required for each consumer; prior V1.4.1, V1.4.0, V1.3, V1.2, V1.1, V1.0, Candidate, Development, or pre-reset evidence does not automatically establish current conformance.

No consumer is production-eligible merely because GLAZE UI V1.5 is the current Stable platform target. Each application or service must independently satisfy its applicable rendered, interaction, accessibility, native/platform, product, performance, rollback, privacy/security authority, and release acceptance gates.

## Stable consumer entrypoints

- Web material baseline: `css/glaze-v1.4.1.css`
- Runtime: `js/glaze-v1.5.0.mjs`
- Contract: `GLAZE_UI_V1_5.md`
- Stable qualification scope: `contracts/v1.5/stable-scope.json`
- Stable acceptance: `acceptance/v1.5-stable.md`
- Immediate rollback baseline: `1.4.1`

V1.5.0 inherits the V1.4.1 optical foundation and adds the Stable Context + Capability Awareness presentation layer. Consumers may use contextual composition, capability-aware controls/navigation/actions, runtime/connectivity/window adaptation, graceful fallbacks, and privacy-safe diagnostics only within the authority boundaries of their own systems and integrations.

## Registry status vocabulary

- `adoption-required` — the consumer has not yet supplied accepted current-Stable V1.5.0 evidence. It may retain superseded historical target/evidence fields as migration provenance, but it does not satisfy the current required target.
- `unverified` — the current consumer state has not yet been verified against the V1.5.0 contract.
- `accepted-v1` — the consumer has completed governed product-specific acceptance for the current Stable contract at an exact 40-character source revision with an evidence reference. This state still does not make the overall product production-eligible; product lifecycle/release authority remains independent.

An accepted current consumer must target exactly the current Stable version and identify the exact accepted source revision and evidence record.

## V1.5.0 shared qualification boundary

The shared V1.5.0 qualification accepts the 16 reviewed obligations recorded in `contracts/v1.5/stable-scope.json` for exact reviewed implementation anchor `ee1032a0822ab8e103f8afe48e5c1859fde65cc9`.

Two further shared qualification expansions are versioned into V1.5.1 rather than claimed by V1.5.0:

- representative measurement against the Glaze UI Performance Budget v1.0;
- representative fold/unfold/posture/rotation target-runtime acceptance.

Consumers must not infer either claim from V1.5.0 Stable status. Consumer repositories supporting relevant performance or posture claims may retain stricter local requirements and must independently validate their supported platform/runtime boundary.

Privacy Shield, Wardveil Security, application, service, platform, policy, identity, and other authoritative systems retain their own truth domains. Glaze UI presentation must not create consent, permission, authorization, operational authority, or automatic consequential/fallback execution.
