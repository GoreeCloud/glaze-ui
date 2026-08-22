# Glaze UI Release Acceptance Protocol

Stable promotion requires exact-revision source validation plus representative rendered visual/accessibility acceptance. `STABILITY.md` governs compatibility/promotion; `COMPONENT_STATUS.md` governs lifecycle.

## Required evidence

Record exact candidate SHA, CI run, rendering environment, proposed status, compatibility/migration impact, lifecycle changes, unresolved/unsupported cases, and rollback boundary.

## Representative form-factor matrix

| Profile | Required reference |
| --- | --- |
| Phone / Mobile | 390 × 844 |
| Tablet | 820 × 1180 |
| Desktop | 1280 × 900 |
| Wide Desktop | 1600 × 1000 |
| TV | 1920 × 1080 |

Appearance: Light/Dark where applicable. Input: touch/pointer/keyboard/directional focus as applicable. Motion: normal and reduced motion. Transparency: normal and reduced transparency where supported. Contrast: normal/increased. Forced colors: `forced-colors: active` or equivalent. Near-view profiles retain 200% browser zoom/reflow coverage.

## Core acceptance checks

- no unintended horizontal overflow;
- recognizable Canvas/Solid/Raised/Glaze/Overlay hierarchy;
- practical targets and visible focus;
- persistent field labels and accessible help/error relationships;
- checked/selected/progress/status meaning independent of color alone;
- reduced-motion and transparency fallbacks;
- forced-colors focus/selection/checked/progress/destructive distinction;
- no unapproved remote presentation dependencies;
- purpose-built Phone/Mobile, Tablet, Desktop, and TV layouts rather than scaled shells;
- adaptive transitions preserve task continuity, reading order, keyboard/focus order, and critical actions.

## Form-factor fidelity acceptance

### Phone / Mobile
Touch/reachability-first; safe-area-aware; mobile navigation/overlays; dense content transforms appropriately; never a shrunken Tablet/Desktop interface.

### Tablet
Intentional rails/panes/split/master-detail where useful; touch remains primary; posture/orientation/window changes preserve state; never a stretched Mobile interface.

### Desktop
Pointer/keyboard workflows, resizable windows, appropriate density, menus/toolbars/shortcuts/context behavior where useful; never an enlarged Mobile interface.

### TV
Far-view legibility; landscape-first; overscan-safe essential content; larger type/targets/spacing; directional focus plus Select/Back-equivalent task flow; no pointer/swipe dependency; focus remains obvious and distinct from selection; no unreachable controls or focus traps; bounded focus scale/lift; reduced-motion/forced-colors preserve a strong static focus indicator; TV never resembles Wide Desktop with a remote added afterward.

## 1.2 application-interface acceptance retained by 1.4

Persistent field labels, textarea behavior, checkbox and radio choices, switches, segmented controls/tabs, progress indicators, banners, focus-ring, and selection semantics remain required.

## 1.3 expressive acceptance retained by 1.4

Functional Glass, Clear Glass boundaries, expressive shape hierarchy, effects/spatial motion separation, adaptive button-group emphasis, compact reachability, hero typography, solid fallbacks, and reduced-motion behavior remain required.

## 1.4-specific form-factor acceptance

`FORM_FACTORS.md`, form-factor tokens, `css/glaze.formfactors.css`, dependency-free Mobile/Tablet/Desktop/TV references, TV safe-region semantics, far-view type/targets, directional focus, focus/selection distinction, reduced-motion/forced-colors focus fallback, width-independent TV selection, and window/input-aware near-view selection are mandatory.

## Stability promotion acceptance

Before Candidate becomes Stable: lifecycle classification is accurate; Experimental/Planned capability is not required; promoted capability has semantics/accessibility/validation/migration guidance; exact final candidate passes source and rendered/native acceptance applicable to its scope; failed cases are fixed without weakening gates; Stable docs/status/version agree; rollback is identified.

For 1.4 design-system core, native/real-device execution is not applicable because this repository ships no native runtime. Native consumers still require product-specific native/real-device acceptance.

If any required check cannot be executed, the release remains a candidate. Unsupported must be explicit; untested is not accepted.
