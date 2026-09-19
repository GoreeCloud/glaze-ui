# GLAZE UI V1.6 Consumers

The machine-readable consumer registry authority is `consumers/registry.json`.

The required target for every applicable GoreeCloud user-facing consumer is **GLAZE UI V1.6** (`1.6.0`). Fresh repository-local V1.6 adoption and acceptance evidence is required for each consumer. Prior V1.5.1, V1.5.0, V1.4.x, earlier Stable, Candidate, Development, or pre-reset evidence does not automatically establish current conformance.

No consumer is production-eligible merely because GLAZE UI V1.6.0 is the current Stable platform target. Each application or service must independently satisfy its own lifecycle, supported-platform, accessibility, security, privacy, integration, deployment, signing/package, and production acceptance requirements.

Current shared authority:

- Version: `1.6.0`
- Runtime: `js/glaze-v1.6.0.mjs`
- Stable contract: `contracts/v1.6/stable-release.json`
- Stable acceptance: `acceptance/v1.6-stable.json`
- Stable qualification: `acceptance/v1.6-stable-qualification-review.json`
- Immediate rollback baseline: `1.5.1`

## Registry status vocabulary

- `adoption-required` — the consumer has not supplied accepted V1.6.0 evidence. Historical target/evidence fields may remain as migration provenance but do not satisfy the current target.
- `unverified` — the current consumer state has not yet been verified against V1.6.0.
- `accepted-v1` — the consumer has completed governed product-specific acceptance for the current Stable contract at an exact 40-character source revision with an evidence reference. This state still does not make the overall product production-eligible; product lifecycle/release authority remains independent.

An accepted current consumer must target exactly the current Stable version and identify its exact accepted source revision and evidence record.

## Shared qualification boundary

V1.6.0 has 24 verified shared qualification lanes with no unverified or not-applicable lanes. These shared acceptances are bounded to their reviewed scopes. Consumer repositories must independently validate their supported platform/runtime, accessibility, performance, privacy/security, deployment, and production boundary.

Privacy Shield, Wardveil Security, Everkeep, application, service, platform, policy, identity, observability, and other authoritative systems retain their own truth domains. Glaze UI presentation must not create consent, permission, authorization, operational authority, or automatic consequential/fallback execution.
