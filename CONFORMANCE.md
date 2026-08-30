# Glaze UI 2.1 Conformance

Glaze UI 2.1 conformance protects beauty, usability, stability, accessibility, privacy, resilience, tangible interaction, semantic color through glass, and purpose-built cross-environment behavior.

## Required gates

1. **Identity** — recognizably GoreeCloud and traceable to approved identity.
2. **Tokens** — current semantic colors, typography, spacing, geometry, material, motion, target, state, accessibility and adaptive-layout roles map to Glaze tokens or documented native equivalents.
3. **Glaze Material** — Canvas / Surface / Soft Glaze / Glaze / Deep Glaze / Live Glaze follow role boundaries; **content is solid and interaction is glazed** selectively.
4. **Material Budgets** — visible Glaze Material remains within the recipe/performance budget and degrades deterministically.
5. **Clarity and appearance** — Clear/Balanced/Solid and Light/Dark/Deep Dark preserve readability and layer distinction.
6. **Semantic color through glass** — selection, live/protected, warning, failure, offline and other state meaning remains explicit and color is never the only carrier.
7. **States and controls** — focus, selected, pressed, disabled, loading, checked, expanded, invalid, success/warning/error and progress meaning are programmatic.
8. **Targets** — general interactive targets preserve at least 48px/dp where governed by the 2.x reference; Touch Assistance and TV preserve at least 56px/dp.
9. **Expression and motion** — Calm/Balanced/Expressive changes intensity, not meaning; **Nothing teleports.** Reduced Motion removes nonessential travel/morphing without blocking state changes.
10. **Accessibility precedence** — Reduced Transparency, Forced Colors, Increased Contrast, Reduced Motion, Large Text and Touch Assistance override decorative optical treatment where required.
11. **Adaptive layout** — components transform rather than merely resize.
12. **Form-factor fidelity** — phone/mobile, tablet, desktop, TV, foldable, wearable and spatial mappings are purpose-built where supported rather than scaled shells.
13. **Live Surfaces and evidence** — ongoing-process identity may move across contexts but cannot invent freshness, completion, security, privacy, resilience or coordination truth.
14. **Privacy and dependency boundary** — no unnecessary tracking, remote presentation dependency, analytics, or third-party runtime is required by the core reference.
15. **Authority** — Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Mesh and application logic retain domain truth; Glaze UI is presentation/interaction authority only.
16. **Visual acceptance** — representative supported profiles and task flows are rendered/reviewed; the 2.1 Stable system-level Visual Excellence gate was explicitly approved.
17. **Stability and lifecycle** — production consumers target only current Stable Glaze UI. Candidate/Experimental behavior cannot silently satisfy a Stable claim.

## Form-factor fidelity acceptance

**Phone/Mobile:** verify touch navigation, safe areas, reachable actions, practical targets, overlays/sheets and no desktop dependency.

**Tablet:** verify rail/pane/split views where useful, posture/window adaptation, touch ergonomics and task-state preservation.

**Desktop:** verify pointer/keyboard behavior, useful resizing, appropriate density, menus/shortcuts/context behavior and multi-pane workflows where useful.

**TV:** verify far-view legibility, overscan-safe essential content, larger controls/type, directional focus reachability, predictable movement, no dead-end traps, Select/Back-equivalent operation, focus/selection distinction and static high-contrast focus under reduced motion/forced colors.

**Foldable:** verify hinge/fold avoidance, pane minimums, posture/orientation continuity, focus/reading order and no interactive control crossing the excluded region.

**Smartwatch/Wearable:** verify compact hierarchy, effective target size, touch/native-equivalent completion, rotational navigation when applicable, reduced motion/transparency, large text and platform-native behavior. The design-system reference does not substitute for application-specific native or real-device acceptance.

**Spatial:** verify anchored/floating surfaces, focusability, effective targets at supported depth, full flat/no-depth fallback and no dependency on advanced graphics for basic usability. Hardware-specific spatial products require application-specific native or real-device acceptance.

## Evidence

Passing overflow or screenshot checks alone is insufficient. Evidence must identify the exact design-system/application revision and environment tested. A design-system Stable promotion establishes a mandatory target, not downstream product certification.

Evidence freshness and authority remain producer-bound. Expired, stale, superseded, malformed, or otherwise invalid evidence cannot support a current conformance claim.

## Current-Stable conformance claims

Glaze UI **2.1.0** is the current Stable baseline and the only active version eligible for a current GoreeCloud application conformance or production UI acceptance claim.

A product may claim **`Glaze UI 2.1 conformant`** only when every applicable current gate is satisfied, the product targets exact current Stable 2.1.0, and product-specific acceptance is complete. A Stable claim additionally requires `STABILITY.md` and the Stable lifecycle surface in `COMPONENT_STATUS.md`.

Historical Glaze UI 1.0.0 through 2.0.0 remain release, migration, rollback and audit evidence only. They cannot satisfy current production readiness after 2.1 promotion.

No documented exception can waive current-Stable application alignment. Platform-neutral Stable semantics do not waive **application-specific native or real-device acceptance** where the consuming product is native or hardware-specific.
