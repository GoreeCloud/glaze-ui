# Migrating from Glaze UI 2.0 to 2.1

Status: **Candidate migration guidance**  
Current Stable: **2.0.0**  
Target after formal promotion: **2.1.0**

This document defines the compatibility impact and controlled migration path from Glaze UI 2.0 to the active 2.1 Candidate. It does not make 2.1 consumer-eligible before formal Stable promotion.

## Compatibility position

Glaze UI 2.1 is a compatible refinement of the 2.0 design identity rather than a replacement for it. The core material hierarchy remains **Canvas → Surface → Soft Glaze → Glaze → Deep Glaze → Live Glaze**. Light, Dark and Deep Dark; Clear, Balanced and Solid Material Clarity; Calm, Balanced and Expressive expression; Connected Transformation; the 48 px/dp general target floor; the 56 px/dp TV/Touch-Assistance floor; content-first composition; and platform-authoritative state boundaries all carry forward.

2.1 strengthens determinism and conformance around those semantics. A 2.0 application therefore should not be visually rewritten merely to adopt 2.1. Migration should preserve successful task structure and product personality while updating the parts affected by the new contracts and acceptance rules.

## Material changes consumers must evaluate

A consumer migrating to 2.1 must evaluate the following implemented Candidate refinements:

- machine-readable lifecycle, component, material and accessibility-resolution contracts;
- deterministic Accessibility Resolution Matrix precedence;
- deterministic performance profiles and material fallback behavior;
- Material Budgets for Productivity, Communication, Media, Administration and Creative recipes;
- formal Comfortable, Standard, Compact and Far View density behavior;
- deterministic Reduced Transparency → Solid behavior where required;
- Large Text reflow behavior, including Compact density yielding to readable effective density when necessary;
- Touch Assistance enlargement to the 56 px/dp effective target floor;
- forced-colors/system-semantic authority and protected semantic-color precedence;
- stronger state-completeness, resilience and exceptional-state expectations;
- source-pinned screenshot regression and expanded rendered/interaction evidence expectations where applicable; and
- native platform mapping requirements when browser/source evidence cannot establish native behavior.

These refinements can expose pre-existing visual or accessibility defects in a 2.0 consumer even when its ordinary/default presentation appears unchanged. A stricter 2.1 validation failure is not automatically a design-system incompatibility; it may identify a consumer behavior that 2.0 did not validate as precisely.

## Behavior that must not be inherited by accident

2.1 Stable consumers must not depend on Candidate-only filenames, active Candidate lifecycle labels, experimental Glaze Motion behavior, planned System Icon Registry behavior, planned development-inspector behavior, or other Planned/Experimental capabilities unless those capabilities are separately promoted.

Glaze Motion remains Experimental. Motion may align with Glaze Motion semantics without making the Experimental package a Stable dependency.

## Consumer migration sequence

1. Keep the application on Glaze UI 2.0.0 until 2.1 is formally promoted Stable.
2. Record the exact 2.1 Stable release revision when promotion occurs.
3. Change the application target from 2.0.0 to 2.1.0 through a repository-local adoption change; do not infer adoption from the central registry.
4. Map the application’s consumed components, material roles, appearance modes, density profiles, state vocabulary and platform-state presentation to the 2.1 Stable contract.
5. Apply the Accessibility Resolution Matrix rather than maintaining incompatible application-local precedence rules.
6. Validate Material Budgets and performance fallbacks in representative task flows.
7. Re-run application-specific keyboard, pointer, touch, large-text, reduced-motion, reduced-transparency, increased-contrast, forced-colors and applicable native/platform acceptance.
8. Perform application-specific human Visual Excellence review against the application’s exact adoption revision.
9. Update repository-local conformance evidence and the canonical GoreeCloud consumer registry only from verified application evidence.
10. Keep production eligibility false until the application’s own adoption and product acceptance are complete.

## Compatibility impact by area

### Materials and composition

No wholesale material rename is required from 2.0. Consumers should keep content on Canvas/Surface and interaction on bounded Glaze roles. The principal migration impact is stricter deterministic material behavior and recipe-specific budget enforcement.

### Accessibility

This is the most important behavioral tightening. Applications with custom preference-resolution logic must reconcile it with the 2.1 Accessibility Resolution Matrix. Protected semantic meaning and platform forced-color authority outrank cosmetic personalization. Reduced Motion, Reduced Transparency, Increased Contrast, Large Text and Touch Assistance are first-class renderings, not optional embellishments.

### Responsive layout and density

Existing 2.0 form-factor mappings remain valid when they satisfy 2.1 evidence. Consumers should re-check Compact density under Large Text, Far View behavior on TV, touch/pointer transitions, reachability and pane transformations rather than assuming width-only breakpoints are sufficient.

### Motion and interaction

Connected Transformation remains the interaction grammar. 2.1 adds stronger expectations around interruption, reversal, focus transfer and reduced-motion alternatives. No consumer should add motion merely to demonstrate 2.1 adoption.

### Platform-state presentation

Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Sync, GoreeCloud Identity and GoreeCloud Mesh remain the authorities for their own state. Glaze UI standardizes presentation only. Migration must not turn simulated, cached or visual state into a claim that a platform capability actually executed.

### Native applications

Native consumers should preserve native platform semantics and ergonomics while mapping the shared 2.1 contract. The design-system Android reference and hosted emulator evidence do not certify a downstream Android application, OEM behavior, physical-device ergonomics, TalkBack, signing, distribution or battery/performance behavior.

## Rollback

Until 2.1 is promoted, rollback means remaining on the current Stable 2.0.0 release. After a future 2.1 Stable promotion, 2.0.0 becomes a historical Stable migration/rollback reference rather than a conforming current production target. A temporary rollback may support diagnosis or recovery, but it does not restore current-Stable conformance.

Consumers must preserve repository-local migration history and exact prior evidence so a failed adoption can be diagnosed without rewriting history.

## Central consumer-registry effect at promotion

Formal 2.1 Stable promotion changes the mandatory target; it does not promote applications by declaration. The canonical consumer audit must then require 2.1.0. Existing applications that still target 2.0.0 or earlier remain non-production-eligible under the Glaze UI gate until their own 2.1 adoption and acceptance evidence is complete.

A repository absent from 2.1 adoption evidence is unassessed for 2.1, not implicitly compatible.

## Promotion boundary

This migration guidance satisfies the documentation requirement only when the implementation and compatibility statements remain consistent with the exact release candidate. Stable promotion still requires the complete 2.1 gate: exact-final-revision CI, rendered/interaction/accessibility/resilience evidence, applicable native/platform evidence, normal GoreeCloud release governance and recorded human Visual Excellence acceptance.