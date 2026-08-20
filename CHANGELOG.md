# Changelog

All notable changes to the Glaze UI reference implementation are recorded here.

## 1.3.0 — 2026-08-20

Expressive-hierarchy evolution based on the documented Glaze UI lineage of One UI 8.5, Liquid Glass, and Material 3 Expressive while preserving GoreeCloud's original identity and accessibility/privacy requirements.

### Added

- Explicit Glaze UI design-lineage metadata and documentation.
- `css/glaze.expressive.css` as the canonical 1.3 expressive layer.
- Functional Glass for navigation, controls, toolbars, floating actions, and transient chrome.
- Clear Glass for controls over visually rich media, with a stricter usage boundary than ordinary Glaze surfaces.
- Compact, Standard, Expressive, Hero, and Pressed shape semantics.
- Separate effects-motion and spatial-motion duration/easing semantics.
- Expressive action and tile primitives with bounded shape morphing.
- Adaptive button groups with visual emphasis that preserves logical/action order.
- Compact reachability composition helpers that support lower action zones without DOM or keyboard reordering.
- Hero and supporting typography primitives for more intentional expressive hierarchy.
- Reduced-motion, reduced-transparency, forced-colors, and no-backdrop-filter fallbacks for the new expressive layer.

### Improved

- Material guidance now explicitly treats glass as a functional hierarchy layer rather than a universal content-card treatment.
- Component and conformance contracts now distinguish calm utility interactions from high-value expressive moments.
- Mobile ergonomics now include one-handed reachability as a first-class composition consideration.
- Motion guidance now separates effect changes from spatial/geometry changes so interaction feedback can stay quick while larger transitions feel fluid.
- Adaptive action groups can communicate priority through space allocation without changing order or semantics.

### Preserved

- Canvas, Solid, Raised, Glaze, and Overlay hierarchy.
- Compact, Medium, Expanded, and Wide adaptive model.
- 44px minimum actionable targets, visible focus, semantic state layers, form/selection semantics, safe-area handling, privacy boundaries, and resilience fallbacks.
- Product personality and the rule that visual quality must not regress for the sake of standardization.

## 1.2.0 — 2026-08-20

Stable application-interface expansion focused on form semantics, selection controls, explicit focus treatment, feedback completeness, rendered acceptance, and stronger adoption safety.

### Added

- Dedicated semantic `focusRing` and text-selection color roles for light and dark appearances.
- Placeholder opacity and field/group/message spacing semantics.
- `css/glaze.controls.css` as the canonical 1.2 control-primitives layer.
- Reusable field, field-label, help/error message, textarea, checkbox/radio choice, switch, segmented-control/tab, progress, and banner primitives.
- Explicit form and selection conformance requirements covering persistent labels, programmatic help/error relationships, checked/selected state, binary switch semantics, and determinate progress values.
- Stronger adoption guidance favoring platform-native control semantics before custom visual replacement.
- `ACCEPTANCE.md`, defining the exact representative web matrix, 1.2-specific visual/accessibility checks, required evidence, and the rule that an unexecuted required gate cannot be silently treated as passed.
- `reference/acceptance.html` and `scripts/validate_rendered_reference.py` for browser-rendered Stable-release acceptance without adding a JavaScript package dependency.
- A permanent rendered-reference CI gate for pull requests and main pushes.

### Improved

- Focus treatment is now governed by a dedicated semantic color role rather than being derived only from accent/current color mixing.
- Consumer contract testing guidance now includes form relationships, selection semantics, and presentation dependency boundaries.
- Visual acceptance guidance now explicitly covers form errors, selection controls, progress, banners, overlays, 200% zoom/reflow, and exact Compact 390 × 844 and Expanded 1280 × 900 viewports.
- Increased-contrast and forced-colors coverage now includes textarea, switch, segmented selection, progress, banners, selected/checked states, and focus treatment.
- Repository validation now fails closed if the 1.2 accessibility fallbacks or release-acceptance protocol disappear.

### Validation and acceptance

- Exact candidate head `43a9b4a8e2f8bf0c515b554aa60dd0309bd12ea6` passed Glaze UI CI run `32341099002` after forced-colors hardening.
- Exact candidate head `4f4b00396a1e70bf2ba911f6236ea1192ead2698` passed Glaze UI CI run `32341496773` after acceptance-protocol enforcement.
- Presentation-bearing candidate head `987b33247eb399934196a6d9bcf812f6b26210e3` passed Glaze UI CI run `32341673211` (run #20), including Chromium-rendered Compact 390 × 844 and Expanded 1280 × 900 light/dark acceptance plus reduced-motion and forced-colors cases.
- The full acceptance record is maintained at `acceptance/1.2.0.md`.

## 1.1.0 — 2026-08-18

Compatible design-system expansion focused on richer reusable semantics and cross-platform application ergonomics.

### Added

- `info`, `onAccent`, and semantic modal-scrim color roles for light and dark appearances.
- Shared hover, pressed, focus, and selected state-layer opacity tokens.
- Standard 16/20/24/32 icon sizing roles.
- Compact and comfortable density guidance that preserves 44px minimum actionable targets.
- Expanded typography roles, adaptive gutter tokens, and safe-area support.
- Reusable web primitives for navigation items, toolbars, badges, dialogs, menus, toasts, scrims, and icons.
- Stronger cross-platform and exact-version consumer conformance requirements.

## 1.0.0 — 2026-08-16

Initial canonical Glaze UI design-system foundation.

### Added

- Platform-neutral semantic design tokens for light and dark appearances.
- Canvas, Solid, Raised, Glaze, and Overlay surface hierarchy.
- Shared web CSS primitives and signature GoreeCloud gradient treatment.
- Component interaction and state contract.
- Compact, Medium, Expanded, and Wide adaptive layout ranges.
- Instant, Fast, Standard, and Emphasized motion vocabulary.
- Reduced-motion, increased-contrast, forced-colors, and no-backdrop-filter fallbacks.
- Dependency-free visual reference implementation.
- Zero-dependency repository validator.
- Stable-release conformance gates and application adoption guidance.
- MIT license, contribution guidance, security policy, and GitHub Actions validation.
