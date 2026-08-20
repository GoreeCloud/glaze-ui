# Changelog

All notable changes to the Glaze UI reference implementation are recorded here.

## 1.2.0 — Candidate — 2026-08-20

Compatible application-interface expansion focused on form semantics, selection controls, explicit focus treatment, feedback completeness, and stronger adoption safety.

### Added

- Dedicated semantic `focusRing` and text-selection color roles for light and dark appearances.
- Placeholder opacity and field/group/message spacing semantics.
- `css/glaze.controls.css` as the canonical 1.2 control-primitives layer.
- Reusable field, field-label, help/error message, textarea, checkbox/radio choice, switch, segmented-control/tab, progress, and banner primitives.
- Explicit form and selection conformance requirements covering persistent labels, programmatic help/error relationships, checked/selected state, binary switch semantics, and determinate progress values.
- Stronger adoption guidance favoring platform-native control semantics before custom visual replacement.
- `ACCEPTANCE.md`, defining the exact representative web matrix, 1.2-specific visual/accessibility checks, required evidence, and the rule that an unexecuted required gate cannot be silently treated as passed.

### Improved

- Focus treatment is now governed by a dedicated semantic color role rather than being derived only from accent/current color mixing.
- Consumer contract testing guidance now includes form relationships, selection semantics, and presentation dependency boundaries.
- Visual acceptance guidance now explicitly covers form errors, selection controls, progress, banners, overlays, 200% zoom/reflow, and exact Compact 390 × 844 and Expanded 1280 × 900 viewports.
- Increased-contrast and forced-colors coverage now includes textarea, switch, segmented selection, progress, banners, selected/checked states, and focus treatment.
- Repository validation now fails closed if the 1.2 accessibility fallbacks or release-acceptance protocol disappear.

### Validation

- Exact candidate head `43a9b4a8e2f8bf0c515b554aa60dd0309bd12ea6` passed Glaze UI CI run `32341099002` after forced-colors hardening.
- Exact candidate head `4f4b00396a1e70bf2ba911f6236ea1192ead2698` passed Glaze UI CI run `32341496773` after acceptance-protocol enforcement.
- Stable promotion remains blocked until the representative rendered visual/accessibility matrix is executed and recorded for the final exact candidate revision.

### Preserved

- Canvas, Solid, Raised, Glaze, and Overlay hierarchy.
- Compact, Medium, Expanded, and Wide adaptive model.
- Shared state-layer, motion, safe-area, privacy, and resilience contracts.
- Product personality and the rule that visual quality must not regress for the sake of standardization.

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

### Preserved

- Canvas, Solid, Raised, Glaze, and Overlay hierarchy.
- Compact, Medium, Expanded, and Wide adaptive model.
- Existing motion vocabulary and accessibility/resilience requirements.
- Local-first privacy boundary and dependency-free reference direction.
- Product personality and the rule that visual quality must not regress for the sake of standardization.

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

### Design intent

Glaze UI 1.0 formalizes the GoreeCloud interface language without replacing its established beauty. Selective translucency, softened depth, rounded geometry, purposeful gradients, polished controls, spacious composition, strong light and dark themes, and product-specific personality remain protected characteristics.
