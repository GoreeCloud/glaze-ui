# Glaze UI 1.5 Conformance

Glaze UI 1.5 conformance protects beauty, usability, stability, accessibility, privacy, resilience, and purpose-built form-factor behavior while retaining the full 1.3 expressive foundation.

## Twenty-one required gates

1. **Identity** — recognizably GoreeCloud.
2. **Tokens** — semantic colors, spacing, radii, typography, material, motion, targets, safe areas, and form-factor roles map to Glaze tokens or documented native equivalents.
3. **Surface hierarchy** — Canvas, Solid, Raised, Functional Glass, Clear Glass, and Overlay follow their documented roles.
4. **States** — default/hover/pressed/focus/selected/disabled/loading/status states are defined where relevant; focus and selection remain distinct where the platform separates them.
5. **Forms and selection** — persistent labels, help/error relationships, checked/selected state, binary switch semantics, and determinate progress remain accessible.
6. **Expressive hierarchy** — stronger geometry/motion/type is concentrated in important moments.
7. **Motion separation** — effects and spatial motion use their semantic families; reduced motion removes nonessential transformations.
8. **Accessibility** — keyboard/focus, semantic names, target sizing, contrast, reduced motion/transparency, forced colors, and solid fallbacks.
9. **Adaptive window behavior** — Compact/Medium/Expanded/Wide are window signals, not device identities.
10. **Form-factor fidelity** — every supported user-facing platform is purpose-built rather than a scaled shell.
11. **Mobile fidelity** — touch/reachability-first, safe-area-aware, task-focused; never a shrunken tablet or desktop shell.
12. **Tablet fidelity** — pane/posture/window-aware and touch-primary; never a stretched phone layout.
13. **Desktop fidelity** — pointer/keyboard-first, resizable, workspace-oriented; never an enlarged mobile shell.
14. **TV fidelity** — far-view, landscape-first, overscan-safe, directional-focus, remote/D-pad operable, with clear focus/selection distinction; TV is not Wide Desktop.
15. **Adaptive action grouping** — emphasis may change allocation but never semantic/focus order.
16. **Privacy** — no unnecessary tracking or remote presentation dependencies.
17. **Resilience** — critical content/actions survive missing blur, animation, hover, pointer, or nonessential JavaScript; TV retains static focus under reduced motion/forced colors.
18. **Product personality and visual character** — recognizable Glaze family resemblance without cloned product composition.
19. **Cross-platform mapping** — web, Linux and other desktop platforms, Android, iOS/iPadOS/tvOS, smartwatch/wearable platforms, and other clients preserve semantic roles using appropriate native primitives.
20. **Visual acceptance** — representative supported profiles and task flows are rendered/reviewed before Stable application release.
21. **Stability and lifecycle** — current production consumers target only the current Stable Glaze UI release, depend only on Stable capabilities, and satisfy `COMPONENT_STATUS.md` and `STABILITY.md`; there are no application-level production exceptions to current-Stable conformance.

## Form-factor acceptance expectations

Phone/Mobile: verify touch navigation, safe areas, reachable actions, practical targets, mobile overlays, and no desktop dependency.

Tablet: verify rails/panes/split views where useful, orientation/posture/window adaptation, touch ergonomics, and task-state preservation.

Desktop: verify pointer/keyboard behavior, useful resizing, appropriate density, menus/shortcuts/context behavior, and multi-pane workflows where useful.

TV: verify far-view legibility, overscan-safe essential content, larger controls/type, directional focus reachability, predictable movement, no dead-end traps, Select/Back-equivalent operation, clear focus versus selection, and static high-contrast focus under reduced motion/forced colors.

Smartwatch/Wearable: the current Stable shared Glaze semantics remain mandatory. A GoreeCloud smartwatch or wearable application may not be production-approved until the current Stable Glaze UI release contains an applicable Stable wearable interaction contract and the application completes representative native and real-device acceptance against it. Missing wearable support is a release blocker, not an exception.

## Evidence

Passing overflow checks alone is insufficient. Multi-form-factor products require representative task-flow evidence and application-specific rendered/native acceptance. A design-system Stable promotion does not automatically certify downstream consumers, but once promoted it becomes the mandatory consumer target for all GoreeCloud-controlled user-facing applications.

Evidence used to support a current Glaze UI conformance or production UI acceptance claim must identify when it was observed and the producer- or applicable-policy-defined time through which that evidence remains valid. Evidence whose validity deadline is missing when required, has expired, or is no longer supported by the authoritative producer cannot support a current passing claim. GoreeCloud Mesh and other consumers may evaluate the producer-declared deadline but may not extend, replace, or override it.

## Current-Stable conformance claims

Glaze UI **1.5.0** is the current Stable baseline and the only active version eligible for a current GoreeCloud application conformance or production UI acceptance claim.

A product may claim **`Glaze UI 1.5 conformant`** only when every applicable current 1.5 gate is satisfied, the product targets the exact current Stable release, and product-specific acceptance is complete. A Stable claim additionally requires compliance with `STABILITY.md` and the Stable lifecycle surface in `COMPONENT_STATUS.md`.

Historical Glaze UI releases 1.0.0 through 1.4.0 remain preserved for release history, migration analysis, rollback, and audit evidence. A historical exact-version statement may describe a previous implementation, but it does not mean the consumer is aligned to the current Stable baseline, cannot satisfy current production readiness, and must not be used as a current conformance claim.

When a newer Glaze UI release becomes Stable, requirements introduced by that Stable release become mandatory for GoreeCloud-controlled user-facing applications. Migration must be controlled and validated, but the existence of an older successful conformance record does not permit the application to remain on the superseded release.

No documented exception can waive the current-Stable application requirement. If a platform or interaction environment is not yet covered by an applicable Stable Glaze UI contract, production is blocked until the design system itself gains and promotes the required Stable contract.
