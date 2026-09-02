# Glaze UI 2.2 Evidence Validity

Glaze UI conformance and production-UI-acceptance evidence is useful only while it remains current, attributable, application-specific, and bound to the exact source revision that was actually evaluated.

The machine-readable contract in `contracts/glaze.conformance-evidence.schema.json` and the fail-closed validator in `scripts/validate_conformance_evidence.py` establish the repository-side evidence format for current Stable Glaze UI 2.2.0.

## Required evidence properties

A record must identify an authoritative producer, the consuming application, exact 40-character application source revision, exact current Stable Glaze version, supported form-factor roles, observation time, expiry time, claim kind, application-specific acceptance state, and bounded evidence references.

Evidence is not timeless. Expired, malformed, superseded, wrong-version, wrong-revision, non-authoritative, or otherwise invalid evidence cannot support a current conformance claim.

## Integral platform-system evidence

Glaze UI is presentation and interaction authority, not security, identity, privacy, continuity, or coordination authority. A current accepted application claim therefore records the status of each applicable integral platform-system integration:

- GoreeCloud Identity
- Privacy Shield
- Wardveil Security
- Everkeep
- GoreeCloud Mesh

For an applicable system, an accepted Glaze claim requires current valid integration evidence and at least one evidence reference. This does not let Glaze UI manufacture or replace the system's own acceptance evidence; it only prevents Glaze conformance evidence from silently ignoring a required integration.

A system may be marked `not_applicable` only when the consuming application's governing requirements genuinely make it inapplicable. A not-applicable entry must not carry positive integration-evidence claims.

## Stable and production boundary

The validator is deliberately bound to repository `VERSION` 2.2.0. Historical Glaze releases remain useful for migration, rollback, and audit evidence but cannot satisfy a current-Stable application claim.

Passing this validator proves only that an evidence record satisfies the current repository-side validity rules. It does not itself create visual acceptance, native-device acceptance, accessibility acceptance, application conformance, production authorization, release approval, or acceptance of any other GoreeCloud platform system.

Any source change to a consuming application creates a new candidate revision and requires fresh applicable evidence. Any future Glaze Stable promotion requires an explicit contract/validator update and fresh validation rather than silently treating an older record as current.
