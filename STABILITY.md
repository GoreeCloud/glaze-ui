# Glaze UI Stability Contract

Glaze UI is a shared production dependency. Stability means predictable semantics, repeatable exact-revision validation, controlled change management, documented migration, rendered evidence, explicit rollback, and mandatory alignment of GoreeCloud applications to the current Stable release.

## Current release boundary

- **Stable baseline:** Glaze UI **1.5.0** on `main` after promotion.
- Glaze UI 1.4.0 is the immediately preceding historical Stable baseline. It remains preserved for migration, rollback, and audit evidence but is not a valid current application target.
- Glaze UI 1.0.0 through 1.4.0 are historical Stable releases, not supported active consumer targets.
- Every GoreeCloud-controlled user-facing consumer must target the current Stable baseline.
- When a newer Stable release exists, controlled migration is mandatory rather than optional.
- Experimental and Planned roadmap concepts do not alter the Stable contract.

Historical compatibility means prior release evidence remains available to support controlled migration and rollback. It does not authorize a production application to remain on a superseded Stable release. No older-version compatibility record, grandfathering decision, platform limitation, or documented exception waives the current-Stable consumer requirement.

## Stability principles

1. Stable means compatible enough to support a controlled migration path.
2. Stable means fail closed.
3. Stable means evidence-bound to an exact candidate SHA.
4. Stable means product-safe: design-system promotion never implies downstream application readiness, but it establishes the mandatory application target.
5. Stable means accessible under reduced motion/transparency, increased contrast, forced colors, and solid fallbacks.
6. Stable means local and privacy-conscious.
7. Stable means reversible.
8. Stable means current: superseded Glaze UI releases do not satisfy current production conformance.

## Stable promotion gate

A candidate may become Stable only when repository validation, rendered acceptance, required accessibility/resilience/form-factor cases, compatibility/migration assessment, lifecycle records, version/status documentation, and rollback are complete on the exact final candidate. Platform-native or real-device evidence is required when the **design-system candidate itself implements platform-native behavior that the canonical web/reference harness cannot prove**. Consumer-native implementations remain subject to their own application-specific adoption and release acceptance.

If any applicable gate is incomplete, the release remains Candidate.

Promotion of a new Stable release creates a mandatory migration requirement for GoreeCloud-controlled user-facing consumers. Applications may remain temporarily on the previous release only while actively migrating in a nonconforming or migration-required state; that temporary state cannot satisfy the Glaze UI production-readiness gate.

## 1.5 promotion applicability

Glaze UI 1.5 core contains platform-neutral tokens, CSS/reference implementations, semantic form-factor contracts, and browser-rendered acceptance. It does not ship an Android, iOS/iPadOS/tvOS, Linux-native, television-hardware, smartwatch/wearable, or other native client runtime. Native consumers must prove their own platform mapping, focus/input engine, safe-area/overscan behavior, performance, accessibility, and product task flows before claiming application-level 1.4 acceptance.

Mobile, Tablet, Desktop, and TV have first-class Stable 1.5 form-factor contracts. A smartwatch/wearable or other user-facing target without an applicable Stable Glaze UI interaction contract is production-blocked until the design system implements, validates, and promotes that contract. Missing Stable platform coverage is not an exception.

## Stable maintenance rules

While 1.5.x is Stable, compatibility, accessibility, deterministic validation, accurate documentation, controlled adoption, mandatory consumer migration, and regression resistance outrank feature expansion. No speculative intelligence or roadmap concept enters Stable merely because it has been discussed.

Security, privacy, accessibility, and defect fixes are maintained on the current Stable release. Historical releases may be used temporarily for rollback or migration diagnosis, but such use does not restore current conformance or production eligibility.

## Regression blockers

Stable changes are blocked by semantic-token drift without migration, loss of visible focus, undersized actionable targets where compliant sizing is possible, loss of field/selection semantics, nonessential motion under reduced-motion, unreadable transparency fallbacks, forced-colors state loss, unapproved remote presentation dependencies, generic scaled form-factor layouts, version/status disagreement, stale/non-exact promotion evidence, or governance that permits a production consumer to remain on a superseded Glaze UI release.

## Consumer compatibility

`CONSUMERS.md` and `consumers/registry.json` distinguish current-Stable alignment, Adoption Candidate work, Migration Required consumers, and Unverified evidence.

Applications may not remain on older Stable Glaze UI versions as a conforming production state. A consumer that still targets an older release is `migration-required` and remains blocked on the Glaze UI production gate until it targets the current Stable baseline and completes application-specific acceptance.

An Adoption Candidate must target the current Stable release. Consumer migration is version-specific, intentional in execution, mandatory in outcome, and must not silently depend on Candidate or Experimental Glaze UI behavior.

Historical note: Glaze UI 1.3.0 remains preserved in release history and migration evidence.
