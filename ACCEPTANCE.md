# Glaze UI Release Acceptance Protocol

Glaze UI Stable promotion requires both exact-revision source validation and representative rendered visual/accessibility acceptance. Automated repository conformance is necessary but does not replace rendered acceptance.

`STABILITY.md` is the governing compatibility and promotion contract. `COMPONENT_STATUS.md` identifies which foundations and components are Stable, Candidate, Experimental, or Planned. Acceptance evidence must be consistent with both records before a Stable claim is permitted.

## Required evidence

Acceptance must identify the exact candidate commit SHA and record the browser or native rendering environment used. Evidence is valid only for that exact revision unless a later change is proven presentation-neutral.

The release record must also identify:

- current Stable baseline;
- proposed release status;
- component lifecycle changes, if any;
- compatibility and migration impact;
- unresolved or explicitly deferred acceptance cases;
- rollback commit or branch boundary.

## Representative web matrix

The canonical web reference and public design-site source must be reviewed at minimum in these conditions:

| Dimension | Required coverage |
| --- | --- |
| Viewport | Phone/Compact: 390 × 844; Tablet/Medium: 820 × 1180; Desktop/Expanded: 1280 × 900; Wide: 1600 × 1000 |
| Appearance | Light and Dark |
| Input | Keyboard navigation and pointer/touch-target geometry |
| Motion | Normal and `prefers-reduced-motion: reduce` |
| Transparency | Normal and `prefers-reduced-transparency: reduce` where supported |
| Contrast | Normal and increased-contrast/high-contrast behavior |
| Forced colors | `forced-colors: active` or equivalent platform High Contrast mode |
| Zoom/reflow | 200% browser zoom or an equivalent narrow/reflow check |

For products that do not support one of the form-factor classes above, the omission must be explicitly recorded. Unsupported is acceptable; silently untested is not.

## Core acceptance checks

The review must confirm all of the following:

1. No horizontal overflow occurs at representative phone, tablet, desktop, or Wide widths.
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
17. Phone, tablet, and desktop layouts use purpose-built navigation, density, pane structure, and interaction patterns rather than scaled variants of one shell.
18. Form-factor transitions preserve task continuity, reading order, keyboard order, focus order, and access to critical actions.
19. Foldable, resizable-window, and desktop-mode mobile environments select composition from the effective window/input context rather than a fixed device-name assumption.
20. Stable release documentation does not claim Candidate, Experimental, or Planned capabilities as part of the Stable compatibility surface.
21. Version metadata, lifecycle status, conformance, changelog, and release status agree on the exact final candidate revision.

## Form-factor fidelity acceptance

For every supported form factor, acceptance must include a representative task flow—not just a static screenshot—and confirm the following.

### Phone

- Navigation and action placement are reachable and touch-first.
- Primary tasks do not depend on desktop-style multi-column density.
- Sheets, dialogs, menus, and overlays remain viewport-bounded and safe-area aware.
- The result does not look or behave like a shrunken tablet or desktop interface.

### Tablet

- Additional space is used intentionally through panes, rails, split views, master-detail structure, richer previews, or equivalent tablet-appropriate composition where useful.
- Controls remain touch-appropriate even when information density increases.
- Orientation or window-size changes preserve task state and hierarchy.
- The result does not look like a stretched phone interface.

### Desktop

- Pointer and keyboard workflows are complete where applicable, including visible hover/focus treatment and discoverable shortcuts or menus when the product supports them.
- Larger work areas may use persistent navigation, toolbars, contextual regions, multi-pane workflows, denser tables, or drag-and-drop where useful.
- Resizable windows remain usable across the supported desktop range.
- The result does not look like an enlarged mobile shell.

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

## Stability promotion acceptance

Before a Candidate becomes Stable, acceptance must additionally confirm:

1. `COMPONENT_STATUS.md` accurately classifies every capability introduced or materially changed by the candidate.
2. No Experimental or Planned capability is required by the Stable reference, validator, or consumer contract.
3. Any Candidate capability being promoted has documented semantics, accessibility/resilience behavior, validation coverage, compatibility impact, and migration guidance.
4. The exact final candidate passes source validation and rendered/native acceptance after the last presentation-affecting change.
5. A failed acceptance case is corrected without removing, bypassing, or weakening the affected assertion unless a separately reviewed governance change justifies the new requirement.
6. Stable documentation does not contain transient statements that become false immediately after merge.
7. Rollback is possible through an identified Git revision without unrelated production-infrastructure changes.

If a candidate introduces platform-native behavior that the browser reference cannot prove, representative native/real-device evidence remains mandatory before Stable promotion for that capability.

## Acceptance record

A Stable promotion record should include:

- exact candidate SHA;
- CI run ID and conclusion;
- renderer/browser and operating system;
- phone, tablet, desktop, and Wide viewport/appearance matrix completed for supported targets;
- representative task flows exercised per supported form factor;
- accessibility modes exercised;
- defects discovered during acceptance;
- commits that corrected those defects;
- final exact SHA accepted;
- component lifecycle changes;
- compatibility/migration assessment;
- any unsupported form-factor class or approved exception with reason, impact, fallback, and review condition;
- final Stable merge commit and rollback point.

If any required check cannot be executed, the release remains a candidate. The missing check must be recorded rather than silently treated as passed.
