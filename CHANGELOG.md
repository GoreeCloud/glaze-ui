# Changelog

All notable changes to the Glaze UI reference implementation are recorded here.

## Unreleased

### Added

- Purpose-built phone, tablet, and desktop UI requirements as distinct form-factor experiences rather than scaled variants of one responsive shell.
- Form-factor fidelity as a Stable conformance gate covering navigation, density, pane structure, interaction patterns, resizable windows, foldables, and desktop-mode mobile environments.
- Representative Stable acceptance coverage for Phone/Compact 390 × 844, Tablet/Medium 820 × 1180, Desktop/Expanded 1280 × 900, and Wide 1600 × 1000 layouts.
- Representative task-flow acceptance for each supported form factor, including explicit rejection of shrunken desktop/tablet phone UIs, stretched phone tablet UIs, and enlarged mobile desktop shells.
- A canonical visual-character contract defining Glaze UI as a coordinated system of layered depth, selective blur and reflection cues, rounded/circular/pill geometry, background-aware color, bold information hierarchy, deliberate whitespace and grouping, and tactile bounded interaction motion.

### Improved

- Acceptance now treats unsupported form factors as an explicit recorded state rather than allowing untested targets to be silently treated as passed.
- Form-factor transitions must preserve task continuity, reading order, keyboard/focus order, and critical-action access.
- The canonical repository validator now fails closed if phone/tablet/desktop guidance or the expanded acceptance matrix is removed.
- Component and conformance guidance now distinguish recognizable Glaze visual character from superficial use of blur or rounded cards, while preserving selective-glass boundaries, readability, semantic contrast, accessibility, reduced-motion behavior, privacy, and product-specific purpose.

### Validation and integration

- Exact visual-character contract head `03d10b98df0805b618d6c6614e4b4d58460385ec` passed Glaze UI CI `#104`, run ID `32528873999`, including exact-source checkout, repository validation, Firefox integration validation, deterministic public design-site validation, and Chromium-rendered Glaze UI reference acceptance.
- Pull request #26, `Clarify canonical Glaze UI visual character`, was promoted from draft only after the complete exact-head gate passed and was squash-merged with expected-head protection as canonical main commit `f3b7da7bb302116cf09d793236a6fc4264037fb9`.
- This work clarified the existing Stable Glaze UI 1.3.0 visual contract without changing the version, accepted material hierarchy, accessibility/privacy boundaries, downstream consumer state, or production infrastructure.

## 1.3.0 — 2026-08-20

Stable expressive-hierarchy release based on the documented Glaze UI lineage of One UI 8.5, Liquid Glass, and Material 3 Expressive while preserving GoreeCloud's original identity and accessibility/privacy requirements.

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
- 1.3-specific source, public-site, and rendered-acceptance gates.
- `acceptance/1.3.0.md` as the Stable release evidence record.

### Improved

- Material guidance now explicitly treats glass as a functional hierarchy layer rather than a universal content-card treatment.
- Component and conformance contracts now distinguish calm utility interactions from high-value expressive moments.
- Mobile ergonomics now include one-handed reachability as a first-class composition consideration.
- Motion guidance now separates effect changes from spatial/geometry changes so interaction feedback can stay quick while larger transitions feel fluid.
- Adaptive action groups can communicate priority through space allocation without changing order or semantics.
- The public design site, reference implementation, release protocol, and fail-closed validator describe and test the Stable 1.3 contract while retaining 1.2.0 as a historical baseline.

### Validation and Stable promotion

- Exact candidate head `e206c3da3f5c0df1f1d0e73d7339f9b45b0e1f16` passed Glaze UI CI run `#29`, run ID `32345605986`.
- The validate job passed exact-source checkout, validator compilation, canonical repository validation, deterministic public design-site build validation, and Chromium-rendered reference acceptance.
- PR #6 was moved from draft to ready for review only after that exact-head evidence was available.
- PR #6 was squash-merged with expected-head protection as Stable merge commit `2ac8d0cd444c8234e908e31b05b2cb4dc7d3e5a9` with release title `Glaze UI 1.3.0`.
- Glaze UI 1.3.0 is now the Stable canonical baseline. Glaze UI 1.2.0 remains part of historical and compatibility records.

### Preserved

- Canvas, Solid, Raised, Glaze, and Overlay hierarchy.
- Compact, Medium, Expanded, and Wide adaptive model.
- Complete Glaze UI 1.2 application-interface semantics and rendered-acceptance coverage.
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
- The rendered harness verified absence of horizontal overflow, interactive target geometry, persistent labels, field-error relationships, selection state, determinate progress, banners, five-level surface presence, appearance-control focusability, and activation of requested accessibility media modes.
- The full acceptance record is maintained at `acceptance/1.2.0.md`.

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
