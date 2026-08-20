# Glaze UI Release Acceptance Protocol

Glaze UI Stable promotion requires both exact-revision source validation and representative rendered visual/accessibility acceptance. Automated repository conformance is necessary but does not replace rendered acceptance.

## Required evidence

Acceptance must identify the exact candidate commit SHA and record the browser or native rendering environment used. Evidence is valid only for that exact revision unless a later change is proven presentation-neutral.

## Representative web matrix

The canonical web reference and public design-site source must be reviewed at minimum in these conditions:

| Dimension | Required coverage |
| --- | --- |
| Viewport | Compact: 390 × 844; Expanded: 1280 × 900 |
| Appearance | Light and Dark |
| Input | Keyboard navigation and pointer/touch-target geometry |
| Motion | Normal and `prefers-reduced-motion: reduce` |
| Transparency | Normal and `prefers-reduced-transparency: reduce` where supported |
| Contrast | Normal and increased-contrast/high-contrast behavior |
| Forced colors | `forced-colors: active` or equivalent platform High Contrast mode |
| Zoom/reflow | 200% browser zoom or an equivalent narrow/reflow check |

## Core acceptance checks

The review must confirm all of the following:

1. No horizontal overflow occurs at Compact or Expanded representative widths.
2. The Canvas, Solid, Raised, Glaze, and Overlay hierarchy remains visually understandable.
3. Primary, secondary, destructive, icon, navigation, and appearance controls preserve visible focus and practical 44-pixel minimum targets.
4. Field labels remain visible independently of placeholder text.
5. Help and error messages remain programmatically associated with their fields where the platform supports that relationship.
6. Error state remains understandable without relying on color alone.
7. Native checkbox/radio controls retain native semantics and visible checked state.
8. Switch controls communicate checked/unchecked state, preserve keyboard focus, and are used only for binary settings.
9. Segmented controls or tabs preserve selected state, focus visibility, and readable labels.
10. Determinate progress exposes an accessible value and remains understandable when animation is removed.
11. Banners remain readable in normal, increased-contrast, and forced-colors modes.
12. Reduced motion removes nonessential movement rather than merely accelerating it.
13. Reduced transparency and unsupported backdrop-filter conditions produce readable solid fallbacks.
14. Forced-colors mode preserves visible focus, selection, checked state, progress state, destructive distinction, and usable expressive controls.
15. Light and Dark appearances both remain recognizably Glaze UI rather than generic or visually flattened.
16. The reference remains free of remote fonts, remote icons, analytics, tracking, and UI runtime dependencies.

## 1.2 application-interface acceptance retained by 1.3

Glaze UI 1.3 preserves the complete 1.2 application-interface contract. Stable promotion therefore continues to require representative acceptance of:

- persistent field labels;
- help and error relationships;
- textarea behavior;
- checkbox and radio choices;
- switches;
- segmented controls/tabs;
- progress indicators;
- informational, success, warning, error, and destructive banners where demonstrated;
- dedicated semantic focus-ring and text-selection treatment.

## 1.3-specific expressive acceptance

Glaze UI 1.3 additionally requires representative acceptance of:

- **Functional Glass** on navigation, controls, toolbars, floating actions, or transient chrome without converting ordinary content surfaces into universal glass;
- **Clear Glass** only when demonstrated over visually rich media, with foreground controls remaining readable in both appearances;
- readable Solid/Raised fallbacks for all new glass roles when transparency is reduced or backdrop filtering is unavailable;
- the Compact, Standard, Expressive, Hero, and Pressed shape hierarchy without uncontrolled shape noise;
- expressive press/shape response without layout instability, accidental activation, or loss of focus visibility;
- distinct effects-motion and spatial-motion behavior, with expressive spatial motion concentrated in prominent interactions;
- reduced-motion removal of nonessential scaling, shape morphing, and spatial transformation;
- adaptive button-group emphasis that preserves DOM order, focus order, accessible names, and equivalent access to sibling actions;
- compact reachability composition that can place frequent actions lower in the visual layout without changing reading or keyboard order;
- hero typography that remains readable under reflow, localization pressure, and user text scaling;
- visual confirmation that stronger expression still feels recognizably Glaze UI rather than like a Samsung, Apple, or Google skin.

## Acceptance record

A Stable promotion record should include:

- exact candidate SHA;
- CI run ID and conclusion;
- renderer/browser and operating system;
- viewport and appearance matrix completed;
- accessibility modes exercised;
- defects discovered during acceptance;
- commits that corrected those defects;
- final exact SHA accepted;
- any approved exception with reason, impact, fallback, and review condition.

If any required check cannot be executed, the release remains a candidate. The missing check must be recorded rather than silently treated as passed.
