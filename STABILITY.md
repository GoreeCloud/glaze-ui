# Glaze UI Stability Contract

Glaze UI is a shared production dependency. Stability means predictable semantics, repeatable exact-revision validation, controlled change management, documented migration, rendered evidence, explicit rollback, and mandatory alignment of GoreeCloud applications to the current Stable release.

## Current release boundary

- **Stable baseline:** Glaze UI **2.0.0**.
- Glaze UI 1.6.0 is the immediately preceding historical Stable baseline and remains preserved for migration, rollback diagnosis, and audit evidence.
- Glaze UI 1.0.0 through 1.6.0 are historical Stable releases, not supported active application targets.
- Every GoreeCloud-controlled user-facing consumer must target the current Stable baseline.
- Controlled migration is mandatory when a newer Stable release exists.
- **No downstream application is promoted by declaration.** A design-system release establishes the mandatory target; each product still completes its own adoption and acceptance.
- Experimental and Planned roadmap concepts do not alter the Stable contract.

Historical compatibility means prior release evidence remains available to support controlled migration and rollback. It does not authorize a production application to remain on a superseded Stable release.

## Stability principles

1. Stable means compatible enough to support a controlled migration path.
2. Stable means fail closed.
3. Stable means evidence-bound to exact promotion revisions.
4. Stable means product-safe: design-system promotion never implies downstream application readiness.
5. Stable means accessible under reduced motion/transparency, increased contrast, forced colors, large text, and effects-free fallbacks.
6. Stable means local and privacy-conscious.
7. Stable means reversible.
8. Stable means current: superseded releases do not satisfy current production conformance.

## Stable promotion gate

A Candidate may become Stable only when repository validation, rendered acceptance, applicable accessibility/resilience/form-factor cases, compatibility/migration assessment, lifecycle records, version/status documentation, and rollback are complete on exact final revisions. Platform-native or real-device evidence is required when the **design-system candidate itself** claims native behavior that the platform-neutral reference cannot prove. Consumer-native implementations remain subject to application-specific native and real-device acceptance.

**If any applicable gate is incomplete, the release remains Candidate.**

Promotion of a new Stable release creates a mandatory migration requirement for GoreeCloud-controlled user-facing consumers. Applications may remain temporarily on the previous release only while actively migrating in a nonconforming or migration-required state.

## 2.0 Stable applicability

Glaze UI 2.0 promotes the administrator-enforced platform-neutral contract in `GLAZE_UI_2_STABLE.md`. Its exact pre-promotion Candidate source and browser-rendered evidence remain preserved. Stable 2.0 includes Mobile, Tablet, Desktop, Wide Desktop, TV, foldable/hinge-aware, compact wearable rotational-navigation, and spatial floating-surface semantics at the design-system layer.

The wearable/spatial references prove Glaze UI composition, input semantics, effective target floors, reduced-motion behavior, depth fallback, and effects-free operation. They do not certify Wear OS, watchOS, XR hardware, physical crowns, host-managed surfaces, battery behavior, platform accessibility APIs, device safe areas, or hardware performance. Those remain application-specific native or real-device acceptance requirements.

The previous 1.x material vocabulary remains in repository compatibility/regression assets, but 2.0's current normative hierarchy is Canvas / Surface / Soft Glaze / Glaze / Deep Glaze / Live Glaze.

## Stable maintenance rules

While 2.0.x remains Stable, compatibility, accessibility, deterministic validation, accurate documentation, controlled adoption, mandatory consumer migration, and regression resistance outrank feature expansion. No speculative intelligence or roadmap concept enters Stable merely because it has been discussed.

Security, privacy, accessibility, and defect fixes are maintained on the current Stable release. Historical releases may be used temporarily for rollback or migration diagnosis, but such use does not restore current conformance.

## Regression blockers

Stable changes are blocked by current-token drift without migration, loss of visible focus, effective targets below required floors, loss of field/selection semantics, nonessential motion under reduced-motion, unreadable transparency fallback, forced-colors state loss, effects required for basic usability, unapproved remote presentation dependencies, generic scaled form-factor layouts, broken Connected Transformation continuity/fallback, hinge-region violations, depth-induced target shrinkage, version/status disagreement, stale/non-exact promotion evidence, or governance that permits a production consumer to remain on a superseded release.

## Consumer compatibility

`CONSUMERS.md` and `consumers/registry.json` distinguish current-Stable alignment, Adoption Candidate work, Migration Required consumers, and Unverified evidence.

Applications may not remain on older Stable Glaze UI versions as a conforming production state. A consumer still targeting 1.x is `migration-required` until it targets 2.0.0 and completes application-specific acceptance.

An Adoption Candidate must target the current Stable release. Consumer migration is version-specific, intentional in execution, mandatory in outcome, and must not silently depend on Candidate or Experimental behavior.

Historical note: Glaze UI 1.3.0 and every later 1.x Stable release remain preserved in release history and migration evidence.
