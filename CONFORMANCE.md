# Glaze UI 2.0 Conformance

Glaze UI 2.0 conformance protects beauty, usability, stability, accessibility, privacy, resilience, tangible interaction, and purpose-built cross-environment behavior.

## Required gates

1. **Identity** — recognizably GoreeCloud and traceable to approved Facet identity where Glaze UI branding is used.
2. **Tokens** — current semantic colors, typography, spacing, geometry, material, motion, target, state, accessibility and adaptive-layout roles map to Glaze tokens or documented native equivalents.
3. **Glaze Material** — Canvas / Surface / Soft Glaze / Glaze / Deep Glaze / Live Glaze follow their role boundaries; content is solid/readable and interaction is glazed selectively.
4. **Clarity and appearance** — Clear/Balanced/Solid and Light/Dark/Deep Dark preserve readability and layer distinction.
5. **States and selection controls** — focus, selected, pressed, disabled, loading, checked, expanded, invalid, success/warning/error and progress meaning are programmatic and not color-only.
6. **Targets** — directly actionable 2.0 reference targets preserve at least 48px effective regions; TV preserves at least 56px; perspective/depth may not visually shrink the usable hit region below the applicable floor.
7. **Expression** — Calm/Balanced/Expressive changes intensity, not semantic meaning or accessibility.
8. **Motion** — Utility/Fluid/Expressive timing and Connected Transformation communicate relationship; **Nothing teleports.** Reduced motion removes nonessential travel/morphing without blocking state changes.
9. **Connected Transformation** — source/destination relationship and state survive native View Transition/shared-element unavailability.
10. **Accessibility** — keyboard/focus, semantic names, increased contrast, reduced motion/transparency, forced colors, large-text reflow, color independence, visible boundaries, touch assistance and effects-free usability.
11. **Adaptive layout** — components transform rather than merely resize.
12. **Form-factor fidelity** — every supported environment is purpose-built rather than a scaled shell.
13. **Phone/Mobile fidelity** — touch/reachability-first; frequent actions may use a lower Glaze Action Zone; never a shrunken tablet or desktop shell.
14. **Tablet fidelity** — rail/pane/posture-aware and touch-primary; never a stretched phone layout.
15. **Desktop fidelity** — pointer/keyboard-first, resizable and workspace-oriented; never an enlarged mobile shell.
16. **TV fidelity** — far-view, landscape-first, overscan-safe, directional-focus and remote/D-pad operable; TV is not Wide Desktop.
17. **Foldable fidelity** — hinge/fold exclusion regions remain noninteractive and pane/task continuity survives posture changes.
18. **Wearable fidelity** — compact/glance-first rotational-navigation semantics; not a shrunken phone; native input/system-surface behavior requires product-specific native acceptance.
19. **Spatial fidelity** — depth is supplemental, focusability/semantics survive flattening, and effects-free fallback preserves task completion.
20. **Live Surfaces and evidence** — ongoing-process identity may move across contexts but cannot invent freshness, completion, security, privacy, resilience or coordination truth.
21. **Privacy and dependency boundary** — no unnecessary tracking, remote presentation dependency, analytics, or third-party runtime is required by the core 2.0 reference.
22. **Authority** — Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Mesh and application logic retain their respective domain truth; Glaze UI is presentation/interaction authority only.
23. **Visual acceptance** — representative supported profiles and task flows are rendered/reviewed before application release.
24. **Stability and lifecycle** — current production consumers target only current Stable Glaze UI and satisfy `COMPONENT_STATUS.md` and `STABILITY.md`; Candidate/Experimental behavior cannot silently satisfy a Stable claim.

## Form-factor fidelity acceptance

**Phone/Mobile:** verify touch navigation, safe areas, reachable actions, Navigation Capsule behavior, practical targets, overlays/sheets and no desktop dependency.

**Tablet:** verify rail/pane/split views where useful, posture/window adaptation, touch ergonomics and task-state preservation.

**Desktop:** verify pointer/keyboard behavior, useful resizing, appropriate density, menus/shortcuts/context behavior and multi-pane workflows where useful.

**TV:** verify far-view legibility, overscan-safe essential content, larger controls/type, directional focus reachability, predictable movement, no dead-end traps, Select/Back-equivalent operation, focus/selection distinction and static high-contrast focus under reduced motion/forced colors.

**Foldable:** verify hinge/fold avoidance, pane minimums, posture/orientation continuity, focus/reading order and no interactive control crossing the excluded region.

**Smartwatch/Wearable:** verify compact hierarchy, effective target size, touch/native-equivalent completion, rotational navigation when applicable, reduced motion/transparency, large text and platform-native behavior. The design-system reference does not substitute for application-specific native or real-device acceptance.

**Spatial:** verify anchored/floating surfaces, focusability, effective targets at supported depth, full flat/no-depth fallback and no dependency on advanced graphics for basic usability. Hardware-specific spatial products require application-specific native or real-device acceptance.

## Evidence

Passing overflow or screenshot checks alone is insufficient. Evidence must identify the exact design-system/application revision and the environment that was tested. A design-system Stable promotion establishes a mandatory target, not downstream product certification.

Evidence freshness and authority remain producer-bound. Expired, stale, superseded, malformed, or otherwise invalid evidence cannot support a current conformance claim.

## Current-Stable conformance claims

Glaze UI **2.0.0** is the current Stable baseline and the only active version eligible for a current GoreeCloud application conformance or production UI acceptance claim.

A product may claim **`Glaze UI 2.0 conformant`** only when every applicable current gate is satisfied, the product targets exact current Stable 2.0.0, and product-specific acceptance is complete. A Stable claim additionally requires `STABILITY.md` and the Stable lifecycle surface in `COMPONENT_STATUS.md`.

Historical Glaze UI 1.0.0 through 1.6.0 remain release, migration, rollback and audit evidence only. They cannot satisfy current production readiness after 2.0 promotion.

No documented exception can waive current-Stable application alignment. Platform-neutral Stable semantics do not waive **application-specific native or real-device acceptance** where the consuming product is native or hardware-specific.
