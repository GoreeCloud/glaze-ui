# Glaze UI Stability Contract

Glaze UI is a shared production dependency. Stability means predictable semantics, repeatable exact-revision validation, controlled change management, documented migration, rendered evidence, explicit rollback, and mandatory alignment of GoreeCloud applications to the current Stable release.

## Current release boundary

- **Stable baseline:** Glaze UI **2.2.0**.
- Glaze UI 2.1.0 is the immediately preceding historical Stable baseline and remains preserved for migration, rollback diagnosis, permanent regression, native-reference regression, and audit evidence.
- Glaze UI 1.0.0 through 2.1.0 are historical Stable releases, not supported current application targets.
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
5. Stable means accessible under Reduced Motion, Reduced Transparency, Increased Contrast, Forced Colors, 200% text, Touch Assistance, and effects-free fallbacks.
6. Stable means local and privacy-conscious.
7. Stable means reversible.
8. Stable means current: superseded releases do not satisfy current production conformance.
9. Stable visual acceptance is human-reviewed where required and remains bound to the reviewed presentation.
10. Stable promotion preserves prior accepted releases as historical regression authorities rather than making old current-version validators silently fail.

## Stable promotion gate

A Candidate may become Stable only when repository validation, rendered acceptance, applicable accessibility/resilience/form-factor cases, compatibility/migration assessment, lifecycle records, version/status documentation, rollback, and required human Visual Excellence review are complete on exact final revisions. Platform-native or real-device evidence is required when the **design-system candidate itself** claims native behavior that the platform-neutral reference cannot prove. Consumer-native implementations remain subject to application-specific native and real-device acceptance.

**If any applicable gate is incomplete, the release remains Candidate.**

Promotion of a new Stable release creates a mandatory migration requirement for GoreeCloud-controlled user-facing consumers. Applications may remain temporarily on the previous release only while actively migrating in a nonconforming or migration-required state.

## 2.2 Stable applicability

Glaze UI 2.2 promotes the accepted contract in `GLAZE_UI_2_2_STABLE.md` from preserved 2.2 Candidate implementation provenance. Stable 2.2 includes the bounded System Shell, a 32-component machine-readable catalog across Foundation, Structure, Overlay, Signature, and Intelligence tiers, bounded Universal Search and Control Center runtime/reference behavior, migration compatibility, performance/System Glaze budgets, Optical Reachability presentation, source-pinned screenshot pixel regression, and a bounded Android handheld native reference.

The approved presentation preserves solid readable content planes while using Glaze for transient navigation, command, search, control, and feedback chrome. The one-dominant-panel System Glaze budget prevents competing translucent hierarchy. Deep Dark, Light/Dark, semantic color, focus, Reduced Motion, Reduced Transparency, Increased Contrast, Forced Colors, RTL, 200% text, touch, pointer, keyboard, and Touch Assistance remain first-class acceptance concerns.

The human-approved Optical Reachability source is immutable revision `0411b0f6dd877aea30e2c5674e1acde0105fd97b`. Stable promotion is allowed to add lifecycle, packaging, validation, and release metadata only while exact-head source-pinned regression proves presentation continuity from that reviewed source.

The design-system Android 2.2 reference establishes exact-source emulator build/install/launch/runtime/accessibility/resilience evidence for its bounded Android handheld mapping. It does not certify any downstream Android application, OEM/device behavior, TalkBack, Switch Access, production signing/distribution, or physical-device ergonomics.

Glaze UI 2.1 and earlier retained references remain historical regression evidence where 2.2 carries their semantics forward. Their preservation does not make them valid current production targets.

For lineage continuity, Glaze UI 1.3.0 remains a historical Stable foundation in the repository and release record; its presence is compatibility history, not the current Stable baseline.

## Stable maintenance rules

While 2.2.x remains Stable, compatibility, accessibility, deterministic validation, accurate documentation, controlled adoption, mandatory consumer migration, semantic color integrity, material-budget discipline, source-pinned visual continuity, native-reference integrity, and regression resistance outrank feature expansion. No speculative intelligence or roadmap concept enters Stable merely because it has been discussed.

Security, privacy, accessibility, and defect fixes are maintained on the current Stable release. Historical releases may be used temporarily for rollback or migration diagnosis, but such use does not restore current conformance.

Glaze Motion remains separately Experimental and is not promoted by Glaze UI 2.2.0.

## Regression blockers

Stable changes are blocked by current-token or contract drift without migration, loss of visible focus, effective targets below required floors, loss of field/selection semantics, nonessential motion under Reduced Motion, unreadable Reduced Transparency fallback, Forced Colors state loss, effects required for basic usability, semantic color loss through glass, Material Budget violations, nested backdrop blur, more than one unapproved dominant Glaze panel, unapproved remote presentation dependencies, generic scaled form-factor layouts, broken Connected Transformation continuity/fallback, hinge-region violations, depth-induced target shrinkage, version/status disagreement, stale/non-exact promotion evidence, source-pinned visual regression, native-reference regression where applicable, or governance that permits a production consumer to remain on a superseded release.

## Consumer compatibility

`CONSUMERS.md` and `consumers/registry.json` distinguish current-Stable alignment, Migration Required consumers, and Unverified evidence.

Applications may not remain on older Stable Glaze UI versions as a conforming production state. A consumer still targeting 2.1.0 or earlier is `migration-required` until it targets 2.2.0 and completes application-specific acceptance.

An Adoption Candidate used during migration must target the current Stable release. Consumer migration is version-specific, intentional in execution, mandatory in outcome, and must not silently depend on Candidate or Experimental behavior.

Historical note: Glaze UI 1.3.0 and every later 1.x Stable release, plus Glaze UI 2.0.0 and 2.1.0, remain preserved in release history and migration evidence.

## Glaze UI 2.2 promotion evidence

The approved visual source revision is `0411b0f6dd877aea30e2c5674e1acde0105fd97b`. The approved Candidate head is `7fb817e28a3f6e9d36f55e7af7acb281813d08f4`; Candidate integration to `main` is represented by `73043d537cfbbcda4d309df8ac7da7ae663ba9d5`. Human Visual Excellence was explicitly Accepted on 2026-09-01.

`MIGRATION_2_1_TO_2_2.md` is the controlled migration basis for downstream applications. Design-system Stable promotion authorizes migration to the Stable target but does not automatically satisfy any application's own production gate.

The rollback reference for 2.2.0 is Glaze UI 2.1.0. Merge, release/tag creation, deployment, and downstream adoption remain distinct events and must retain exact-revision evidence.
