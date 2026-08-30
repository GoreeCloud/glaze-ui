# Glaze UI Stability Contract

Glaze UI is a shared production dependency. Stability means predictable semantics, repeatable exact-revision validation, controlled change management, documented migration, rendered evidence, explicit rollback, and mandatory alignment of GoreeCloud applications to the current Stable release.

## Current release boundary

- **Stable baseline:** Glaze UI **2.1.0**.
- Glaze UI 2.0.0 is the immediately preceding historical Stable baseline and remains preserved for migration, rollback diagnosis, permanent regression and audit evidence.
- Glaze UI 1.0.0 through 2.0.0 are historical Stable releases, not supported active application targets.
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
5. Stable means accessible under reduced motion/transparency, increased contrast, forced colors, large text, Touch Assistance, and effects-free fallbacks.
6. Stable means local and privacy-conscious.
7. Stable means reversible.
8. Stable means current: superseded releases do not satisfy current production conformance.
9. Stable visual acceptance is human-reviewed where required and remains bound to the reviewed presentation.

## Stable promotion gate

A Candidate may become Stable only when repository validation, rendered acceptance, applicable accessibility/resilience/form-factor cases, compatibility/migration assessment, lifecycle records, version/status documentation, rollback, and required human Visual Excellence review are complete on exact final revisions. Platform-native or real-device evidence is required when the **design-system candidate itself** claims native behavior that the platform-neutral reference cannot prove. Consumer-native implementations remain subject to application-specific native and real-device acceptance.

**If any applicable gate is incomplete, the release remains Candidate.**

Promotion of a new Stable release creates a mandatory migration requirement for GoreeCloud-controlled user-facing consumers. Applications may remain temporarily on the previous release only while actively migrating in a nonconforming or migration-required state.

## 2.1 Stable applicability

Glaze UI 2.1 promotes the contract in `GLAZE_UI_2_1_STABLE.md` from the preserved 2.1 Candidate source. Stable 2.1 includes deterministic Material Budgets and performance degradation, machine-readable component/material/accessibility-resolution contracts, Clear/Balanced/Solid Material Clarity, density profiles, six canonical reference flows, exceptional-state acceptance, source-pinned screenshot pixel regression, a bounded native Android handheld reference, and the human-approved color-coded glass refinement.

The approved presentation keeps durable content planes solid while making navigation, controls, action islands, command surfaces and Live Glaze more visibly translucent. Accent and semantic colors remain explicit. Reduced Transparency / effective Solid and Forced Colors remove the optical material effects when required.

The design-system Android reference establishes exact-source emulator build/install/launch/runtime evidence for its bounded mapping. It does not certify any downstream Android application, OEM/device behavior, TalkBack, Switch Access, production signing/distribution or physical-device ergonomics.

Glaze UI 2.0's Mobile, Tablet, Desktop, Wide Desktop, TV, foldable/hinge-aware, compact wearable rotational-navigation, and spatial floating-surface semantics remain retained compatibility/regression evidence where 2.1 carries them forward.

## Stable maintenance rules

While 2.1.x remains Stable, compatibility, accessibility, deterministic validation, accurate documentation, controlled adoption, mandatory consumer migration, semantic color integrity, material-budget discipline and regression resistance outrank feature expansion. No speculative intelligence or roadmap concept enters Stable merely because it has been discussed.

Security, privacy, accessibility, and defect fixes are maintained on the current Stable release. Historical releases may be used temporarily for rollback or migration diagnosis, but such use does not restore current conformance.

## Regression blockers

Stable changes are blocked by current-token drift without migration, loss of visible focus, effective targets below required floors, loss of field/selection semantics, nonessential motion under Reduced Motion, unreadable Reduced Transparency fallback, Forced Colors state loss, effects required for basic usability, semantic color loss through glass, Material Budget violations, unapproved remote presentation dependencies, generic scaled form-factor layouts, broken Connected Transformation continuity/fallback, hinge-region violations, depth-induced target shrinkage, version/status disagreement, stale/non-exact promotion evidence, or governance that permits a production consumer to remain on a superseded release.

## Consumer compatibility

`CONSUMERS.md` and `consumers/registry.json` distinguish current-Stable alignment, Migration Required consumers, and Unverified evidence.

Applications may not remain on older Stable Glaze UI versions as a conforming production state. A consumer still targeting 2.0.0 or earlier is `migration-required` until it targets 2.1.0 and completes application-specific acceptance.

An Adoption Candidate, when used during future migrations, must target the current Stable release. Consumer migration is version-specific, intentional in execution, mandatory in outcome, and must not silently depend on Candidate or Experimental behavior.

Historical note: Glaze UI 1.3.0 and every later 1.x Stable release, plus Glaze UI 2.0.0, remain preserved in release history and migration evidence.

## Glaze UI 2.1 promotion evidence

The approved visual baseline source revision is `5b46903c18660ae78e7f1aaea39a93136efacda7`. The reviewed exact-head Candidate revision is `a21601691dc412baa6a889533d6fa5b3a7996dc2`. Human Visual Excellence was explicitly approved on 2026-08-30.

`MIGRATION_2_0_TO_2_1.md` is now the controlled migration basis for downstream applications. Design-system Stable promotion does not automatically satisfy any application's own production gate.
