# Glaze UI Release Acceptance Protocol

Stable promotion requires exact-revision source validation plus representative rendered/accessibility acceptance. `STABILITY.md` governs compatibility/promotion; `COMPONENT_STATUS.md` governs lifecycle.

## Required evidence

Record exact candidate/promotion SHA, CI run, rendering environment, proposed status, compatibility/migration impact, lifecycle changes, unresolved/unsupported cases and rollback boundary. A prior or partial run cannot substitute for the exact final revision.

## Representative form-factor matrix

| Profile | Required reference |
| --- | --- |
| Phone / Mobile | 390 × 844 |
| Tablet | 820 × 1180 |
| Desktop | 1280 × 900 |
| Wide Desktop | 1600 × 1000 |
| TV | 1920 × 1080 |

The retained design-system suite also includes representative foldable/hinge-aware, compact wearable and spatial surfaces. Appearance: Light/Dark where applicable plus Deep Dark representative cases. Input: touch/pointer/keyboard/directional/rotational semantics as applicable. Motion: normal and reduced motion. Transparency: normal and reduced transparency. Contrast: normal/increased; `forced-colors: active` or equivalent. Near-view profiles retain 200% browser zoom/reflow coverage.

Each supported form factor requires a **representative task flow**, not merely a static screenshot. Unsupported or consumer-native cases must be recorded explicitly rather than silently treated as accepted.

## Core 2.0 acceptance checks

- no unintended horizontal overflow;
- current **Canvas / Surface / Soft Glaze / Glaze / Deep Glaze / Live Glaze** hierarchy with content/interaction role separation;
- Clear / Balanced / Solid clarity preserves readability;
- practical targets: 48px general, 56px TV, with spatial perspective unable to reduce the rendered target below the applicable floor;
- visible focus and non-color state meaning;
- persistent field labels, textarea behavior, checkbox and radio choices, switches, segmented controls/tabs and progress indicators remain accessible;
- Connected Transformation preserves state when native View Transition/shared-element support is unavailable;
- Navigation Capsule compression preserves reachability;
- reduced-motion and reduced-transparency fallbacks;
- increased contrast and forced-colors distinction;
- no unapproved remote presentation dependencies;
- purpose-built Phone/Mobile, Tablet, Desktop, TV, foldable, wearable and spatial behavior rather than scaled shells;
- adaptive transitions preserve task continuity, reading order, keyboard/focus order and critical actions;
- advanced effects are never required for basic usability.

## Form-factor fidelity acceptance

### Phone / Mobile
Touch/reachability-first; safe-area-aware; Navigation Capsule/mobile overlays; frequent actions remain reachable; never a shrunken Tablet/Desktop interface.

### Tablet
Intentional rails/panes/split/master-detail where useful; touch remains primary; posture/orientation/window changes preserve state; never a stretched Mobile interface.

### Desktop
Pointer/keyboard workflows, resizable windows, appropriate density, menus/toolbars/shortcuts/context behavior where useful; never an enlarged Mobile interface.

### TV
Far-view legibility; landscape-first; overscan-safe essential content; larger type/targets/spacing; directional focus plus Select/Back-equivalent task flow; no pointer/swipe dependency; focus remains distinct from selection; no unreachable controls or focus traps; reduced-motion/forced-colors preserve a strong static focus indicator.

### Foldable
Representative book posture reserves a physical hinge exclusion region; panes remain outside the hinge, preserve minimum usable widths and maintain state/focus/read order through posture changes.

### Wearable
Compact circular/near-view reference preserves one current rotational-navigation target, 48px effective targets, keyboard/wheel-equivalent rotational semantics and reduced-motion operation. Design-system browser evidence is not native-device certification.

### Spatial
Anchored/floating surfaces preserve semantic focusability and the 48px effective floor at supported depth; a fully flattened no-Z mode remains equivalent and usable. Hardware-specific spatial products require native/real-device acceptance.

## Retained 1.x regression acceptance

The old **Functional Glass** and **Clear Glass** terminology, adaptive button-group emphasis, compact reachability, form controls and Mobile/Tablet/Desktop/Wide Desktop/TV references are retained only as compatibility regression evidence. The dependency-free Mobile/Tablet/Desktop/Wide Desktop/TV references remain permanent historical gates protecting semantics still required by migrated products. They do not supersede the current 2.0 material vocabulary.

The 1.5/1.6 source and rendered suites remain permanent regressions for adaptive color, iconography, interaction state, legacy material compatibility, layout/density, evidence presentation and Adaptive Workspace behavior. Glaze Motion remains separately Experimental.

## 2.0 Stable promotion acceptance

Before 2.0 Candidate becomes Stable:

- the exact frozen Candidate feature/evidence revision passes all 2.0 and retained Stable gates;
- the release-state migration changes VERSION, Stable token metadata, enforcement and consumer-required target without manufacturing consumer conformance;
- 1.6.0 is preserved as the immediately preceding historical Stable baseline;
- the exact final promotion revision passes the complete suite again;
- release documentation, Design Center output, changelog and rollback boundary agree;
- downstream native/hardware consumers remain separately gated.

Candidate evidence accepted before release includes the five-profile Light/Dark matrix, Deep Dark representative cases, Clear/Balanced/Solid, Calm/Balanced/Expressive, large text, reduced motion/transparency, forced colors, no-backdrop, independent `prefers-contrast: more`, no-View-Transition fallback, 1114×834 hinge-aware foldable composition, 360×360 wearable rotational navigation and spatial depth/flat fallback.

## Stability promotion acceptance

Before any Candidate becomes Stable: lifecycle classification is accurate; Experimental/Planned capability is not required; promoted capability has semantics/accessibility/validation/migration guidance; exact final candidate passes source and rendered/native acceptance applicable to its scope; failed cases are fixed without weakening gates; Stable docs/status/version agree; rollback is identified.

For platform-neutral design-system references, native/real-device execution is not automatically applicable. Native consumers still require product-specific native/real-device acceptance.

**If any required check cannot be executed, the release remains a candidate.**
