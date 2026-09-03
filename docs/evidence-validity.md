# GLAZE UI V1.0 Evidence Validity

Glaze UI conformance and production-UI-acceptance evidence is useful only while it remains current, attributable, application-specific, and bound to the exact source revision actually evaluated.

The machine-readable contract in `contracts/glaze.conformance-evidence.schema.json` and the fail-closed validator in `scripts/validate_conformance_evidence.py` establish the repository-side evidence format for GLAZE UI V1.0 (`1.0.0`). Evidence schema version `2` is a record-format revision; it is not a Glaze UI product version.

## Required evidence properties

A record must identify an authoritative producer, consuming application, exact 40-character application source revision, exact current GLAZE UI V1.0 product version, supported form-factor roles, observation time, expiry time, claim kind, application-specific acceptance state, and bounded evidence references.

Producer-system and application identifiers are bounded to 160 characters. Top-level records may carry at most 50 evidence references, while each integral platform-system entry may carry at most 20; each reference is bounded to 500 characters.

Evidence is not timeless and cannot be issued from the future. Expired, future-dated, malformed, superseded, wrong-version, wrong-revision, non-authoritative, or otherwise invalid evidence cannot support a current claim.

## Integral platform-system evidence

Glaze UI is presentation and interaction authority, not security, identity, privacy, continuity, or coordination authority. A current accepted application claim therefore records the status of each applicable integral platform integration represented by this contract:

- GoreeCloud Identity
- Privacy Shield
- Wardveil Security
- Everkeep
- GoreeCloud Mesh

For an applicable system, an accepted Glaze claim requires current valid integration evidence and at least one evidence reference. This does not let Glaze UI manufacture or replace another system's acceptance evidence; it prevents a Glaze claim from silently ignoring a required integration.

A system may be marked `not_applicable` only when the consuming application's governing requirements genuinely make it inapplicable. A not-applicable entry must not carry positive integration-evidence claims.

## V1 product and production boundary

The validator is deliberately bound to repository `VERSION` **1.0.0** and the sole current product identity **GLAZE UI V1.0**. Evidence from another product-version namespace cannot satisfy a current V1 application claim. Required Git history and append-oriented changelog history remain audit records only and do not define current consumer targets.

Passing this validator proves only that an evidence record satisfies repository-side validity rules. It does not itself create visual acceptance, native-device acceptance, accessibility acceptance, application conformance, production authorization, release approval, or acceptance of another GoreeCloud platform system.

Any source change to a consuming application creates a new candidate revision and requires fresh applicable evidence. Any future V1.x product change requires an explicit contract/validator update and fresh validation rather than silently treating an older record as current.
