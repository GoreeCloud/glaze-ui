# Glaze UI 1.4 Conformance

Glaze UI 1.4 conformance protects beauty, usability, stability, and purpose-built form-factor behavior while retaining the full 1.3 expressive foundation.

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
10. **Form-factor fidelity** — supported phone, tablet, desktop, and TV experiences are purpose-built rather than scaled shells.
11. **Mobile fidelity** — touch/reachability-first, safe-area-aware, task-focused; never a shrunken tablet or desktop shell.
12. **Tablet fidelity** — pane/posture/window-aware and touch-primary; never a stretched phone layout.
13. **Desktop fidelity** — pointer/keyboard-first, resizable, workspace-oriented; never an enlarged mobile shell.
14. **TV fidelity** — far-view, landscape-first, overscan-safe, directional-focus, remote/D-pad operable, with clear focus/selection distinction; TV is not Wide Desktop.
15. **Adaptive action grouping** — emphasis may change allocation but never semantic/focus order.
16. **Privacy** — no unnecessary tracking or remote presentation dependencies.
17. **Resilience** — critical content/actions survive missing blur, animation, hover, pointer, or nonessential JavaScript; TV retains static focus under reduced motion/forced colors.
18. **Product personality and visual character** — recognizable Glaze family resemblance without cloned product composition.
19. **Cross-platform mapping** — web, Linux, Android, iOS/iPadOS/tvOS, and other clients preserve semantic roles using appropriate native primitives.
20. **Visual acceptance** — representative supported profiles and task flows are rendered/reviewed before Stable release.
21. **Stability and lifecycle** — Stable consumers depend only on Stable capabilities unless an explicit application-specific exception says otherwise; `COMPONENT_STATUS.md` and `STABILITY.md` govern lifecycle and promotion.

## Form-factor acceptance expectations

Phone/Mobile: verify touch navigation, safe areas, reachable actions, practical targets, mobile overlays, and no desktop dependency.

Tablet: verify rails/panes/split views where useful, orientation/posture/window adaptation, touch ergonomics, and task-state preservation.

Desktop: verify pointer/keyboard behavior, useful resizing, appropriate density, menus/shortcuts/context behavior, and multi-pane workflows where useful.

TV: verify far-view legibility, overscan-safe essential content, larger controls/type, directional focus reachability, predictable movement, no dead-end traps, Select/Back-equivalent operation, clear focus versus selection, and static high-contrast focus under reduced motion/forced colors.

## Evidence

Passing overflow checks alone is insufficient. Multi-form-factor products require representative task-flow evidence and application-specific rendered/native acceptance. A design-system Stable promotion does not automatically certify downstream consumers.

## Conformance statement

A product may claim **`Glaze UI 1.4 conformant`** only when every applicable gate is satisfied or each deviation has a documented GoreeCloud exception. A Stable claim additionally requires compliance with `STABILITY.md` and the Stable lifecycle surface in `COMPONENT_STATUS.md`.
