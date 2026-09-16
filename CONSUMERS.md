# GLAZE UI V1.5 — Contextual + Capability Awareness Consumers

The machine-readable consumer registry authority for current consumer state is `consumers/registry.json`.

The required target for every applicable GoreeCloud user-facing consumer is **GLAZE UI V1.5 — Contextual + Capability Awareness** (`1.5.1`). Fresh repository-local V1.5 adoption and acceptance evidence is required for each consumer; prior V1.5.0, V1.4.1, V1.4.0, V1.3, V1.2, V1.1, V1.0, Candidate, Development, or pre-reset evidence does not automatically establish current conformance.

No consumer is production-eligible merely because GLAZE UI V1.5.1 is the current Stable platform target. Each application or service must independently satisfy its applicable rendered, interaction, accessibility, native/platform, product, performance, rollback, privacy/security authority, and release acceptance gates.

## Stable consumer entrypoints

- Web material baseline: `css/glaze-v1.4.1.css`
- Runtime: `js/glaze-v1.5.1.mjs`
- Contract: `GLAZE_UI_V1_5.md`
- Stable qualification scope: `contracts/v1.5.1/stable-scope.json`
- Stable acceptance: `acceptance/v1.5.1-stable.md`
- Immediate rollback baseline: `1.5.0`

V1.5.1 preserves the reviewed V1.5 Context + Capability Awareness behavior while closing the two shared qualification obligations deliberately deferred from V1.5.0. Consumers may use contextual composition, capability-aware controls/navigation/actions, runtime/connectivity/window adaptation, graceful fallbacks, and privacy-safe diagnostics only within the authority boundaries of their own systems and integrations.

## Registry status vocabulary

- `adoption-required` — the consumer has not yet supplied accepted current-Stable V1.5.1 evidence. It may retain superseded historical target/evidence fields as migration provenance, but it does not satisfy the current required target.
- `unverified` — the current consumer state has not yet been verified against the V1.5.1 Stable target.
- `accepted-v1` — the consumer has completed governed product-specific acceptance for the current Stable contract at an exact 40-character source revision with an evidence reference. This state still does not make the overall product production-eligible; product lifecycle/release authority remains independent.

An accepted current consumer must target exactly the current Stable version and identify the exact accepted source revision and evidence record.

## V1.5.1 shared qualification boundary

The shared V1.5.1 qualification contains **18 accepted obligations**. Sixteen are retained from V1.5.0 for exact reviewed implementation anchor `ee1032a0822ab8e103f8afe48e5c1859fde65cc9`. The two V1.5.1 qualification expansions are independently accepted for frozen exact Development revision `5b59d0e36950d737dba35b58ae58058684e0831b`:

- representative measurement against the approved Glaze UI Performance Budget v1.0 — PR #230 comment `5697516074`;
- representative fold/unfold/posture/rotation target-runtime acceptance under `GCU-ADR-GLAZE-V151-POSTURE-TR-001` — PR #230 comment `5705230782`.

These shared acceptances are bounded to their reviewed environments. Consumer repositories supporting relevant performance or posture claims may retain stricter local requirements and must independently validate their supported platform/runtime boundary.

Privacy Shield, Wardveil Security, application, service, platform, policy, identity, and other authoritative systems retain their own truth domains. Glaze UI presentation must not create consent, permission, authorization, operational authority, or automatic consequential/fallback execution.

Shared Stable promotion also does not establish downstream deployment, production acceptance, an immutable `v1.5.1` tag, or GitHub Release publication.