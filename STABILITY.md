# Glaze UI Stability Contract

Glaze UI is a shared production dependency. Stability means predictable semantics, repeatable exact-revision validation, controlled change management, documented compatibility, rendered evidence, and explicit rollback.

## Current release boundary

- **Stable baseline:** Glaze UI **1.4.0** on `main` after promotion.
- Glaze UI 1.3.0 is the immediately preceding Stable baseline and remains a valid older consumer target.
- The current supported Stable consumer-target set is 1.0.0, 1.1.0, 1.2.0, 1.3.0, and 1.4.0, as recorded by `consumers/registry.json`.
- Stable consumers are never migrated automatically when a newer Stable release exists.
- Experimental and Planned roadmap concepts do not alter the Stable contract.

Compatibility support for an older Stable target means a consumer may remain pinned to that exact contract with version-specific evidence and product acceptance. It does not promise identical active maintenance across every historical Stable line; `SECURITY.md` governs active security-fix and maintenance applicability. Retiring a supported consumer target requires an explicit lifecycle decision and consumer-impact review.

## Stability principles

1. Stable means compatible.
2. Stable means fail closed.
3. Stable means evidence-bound to an exact candidate SHA.
4. Stable means product-safe: design-system promotion never implies downstream application readiness.
5. Stable means accessible under reduced motion/transparency, increased contrast, forced colors, and solid fallbacks.
6. Stable means local and privacy-conscious.
7. Stable means reversible.

## Stable promotion gate

A candidate may become Stable only when repository validation, rendered acceptance, required accessibility/resilience/form-factor cases, compatibility/migration assessment, lifecycle records, version/status documentation, and rollback are complete on the exact final candidate. Platform-native or real-device evidence is required when the **design-system candidate itself implements platform-native behavior that the canonical web/reference harness cannot prove**. Consumer-native implementations remain subject to their own application-specific adoption and release acceptance.

If any applicable gate is incomplete, the release remains Candidate.

## 1.4 promotion applicability

Glaze UI 1.4 core contains platform-neutral tokens, CSS/reference implementations, semantic form-factor contracts, and browser-rendered acceptance. It does not ship an Android, iOS/iPadOS/tvOS, Linux-native, television-hardware, or other native client runtime. Therefore native-device execution is not an applicable design-system-core promotion gate for 1.4 itself. Native consumers must still prove their own platform mapping, focus engine, safe-area/overscan behavior, performance, input behavior, and product task flows before claiming application-level 1.4 acceptance.

## Stable maintenance rules

While 1.4.x is Stable, compatibility, accessibility, deterministic validation, accurate documentation, controlled adoption, and regression resistance outrank feature expansion. No speculative intelligence or roadmap concept enters Stable merely because it has been discussed.

## Regression blockers

Stable changes are blocked by semantic-token drift without migration, loss of visible focus, undersized actionable targets where compliant sizing is possible, loss of field/selection semantics, nonessential motion under reduced-motion, unreadable transparency fallbacks, forced-colors state loss, unapproved remote presentation dependencies, generic scaled form-factor layouts, version/status disagreement, or stale/non-exact promotion evidence.

## Consumer compatibility

Applications may remain on older Stable Glaze UI versions. `CONSUMERS.md` and `consumers/registry.json` distinguish current-Stable alignment, older-Stable alignment, Adoption Candidate work, and Unverified evidence. Adoption Candidate may target a supported Stable release older than the current baseline when final application-specific acceptance is still incomplete.

Consumer migration is version-specific and intentional. The registry must not silently depend on Candidate or Experimental behavior when recording Stable alignment.
