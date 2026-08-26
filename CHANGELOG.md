# Changelog

All notable changes to the Glaze UI reference implementation are recorded here.

## Unreleased

### Added

- `MOTION.md`, `tokens/motion.json`, `css/glaze.motion.css`, and `scripts/validate_motion.py` establish the Glaze UI 1.5 Candidate motion and interaction contract with semantic timing/easing, interruptible user-driven transitions, reduced-motion behavior, gesture and focus feedback, truthful progress/state communication, and platform authority boundaries.
- `MATERIALS.md`, `tokens/materials.json`, `css/glaze.materials.css`, and `scripts/validate_materials.py` establish the Glaze UI 1.5 Candidate material/depth system across Canvas, Solid, Raised, Functional Glass, Clear Glass, Overlay, semantic z-depth, shadow, bounded backdrop sampling, reduced-transparency fallback, and constrained-performance degradation.
- CI now compiles and runs the dedicated motion and material Candidate validators against the exact pull-request revision.

### Improved

- `COMPONENTS.md` now identifies itself as the Glaze UI 1.4 component contract while explicitly preserving the Stable component semantics established in 1.3.
- `scripts/validate_release_state.py` now fails closed when the canonical component-contract heading drifts from the current Stable release family or when the retained 1.3 compatibility boundary disappears.
- Candidate glass behavior is now explicitly selective rather than universal: ordinary content defaults to Solid/Raised, Clear Glass is media-overlay-specialized, and unsupported or accessibility-constrained translucency falls back without losing hierarchy or information.
- Material presentation cannot manufacture privacy, security, resilience, or coordination truth; those states remain authoritative to Privacy Shield, Wardveil Security, Everkeep, and GoreeCloud Mesh respectively.

### Release boundary

- Glaze UI 1.4.0 remains the current Stable production baseline.
- The 1.5 motion and materials work remains Candidate until exact-revision CI and representative rendered acceptance satisfy promotion requirements.

## 1.4.0 — 2026-08-21

Stable form-factor evolution release preserving the complete Glaze UI 1.3 expressive foundation while making Mobile, Tablet, Desktop, and TV first-class semantic interaction environments.

### Added

- `FORM_FACTORS.md` as the canonical form-factor contract based on app window, primary input, viewing distance, platform conventions, posture/resizability, and product task rather than width or device name alone.
- Platform-neutral Mobile, Tablet, Desktop, and TV semantic token roles.
- `css/glaze.formfactors.css` reusable composition primitives.
- Dependency-free Mobile, Tablet, Desktop, and TV reference experiences.
- TV far-view typography, 56px reference minimum targets, larger icon roles, directional-focus semantics, bounded focus scale/lift, overscan-safe references, and focus/selection distinction.
- A dedicated fail-closed `scripts/validate_form_factors.py` Stable contract validator.
- `acceptance/1.4.0.md` as the release acceptance record.
- A consumer-registry migration model that moves current Stable baseline metadata to 1.4 without automatically migrating downstream applications.

### Improved

- Purpose-built Phone/Mobile, Tablet, Desktop, Wide Desktop, and TV acceptance replaces generic scaled-shell assumptions.
- Form-factor fidelity now covers navigation, density, pane structure, resizable windows, touch/reachability, pointer/keyboard behavior, viewing distance, and directional focus.
- Form-factor transitions preserve task continuity, reading order, keyboard/focus order, and critical-action access.
- TV is explicitly a far-viewing, directional-input environment and must never be treated as Wide Desktop.
- The public design-site source and canonical reference now describe 1.4 as Stable while retaining the 1.3 material, expressive, accessibility, privacy, and resilience contracts.
- Stability and component-lifecycle governance from later 1.3 hardening work were reconciled into the 1.4 promotion rather than overwritten by the older candidate branch.

### Validation and Stable promotion

- Earlier candidate head `b076e10d71cb1576ab1904cce71392f4a4b636ca` passed Glaze UI CI #109 / run `32530794651`, including the full Candidate form-factor matrix.
- The stale candidate branch was reconciled onto hardened Stable main `1120f576eeeb2f5725896f85847b5470907f91cf` before promotion.
- Promotion gating caught and corrected missing historical Phone terminology, missing representative-task-flow wording, accidental removal of the retained 1.3 expressive rendered assertion, a validator wording mismatch for the stronger TV/Wide-Desktop rule, and lost live 1.3 reference examples/44px appearance targets. No gate was removed or weakened.
- Exact reconciled content-bearing head `777844030f365c3ce45205633ef05135e4df5067` passed Glaze UI CI #125 / run `32541270573`: canonical repository validation, dedicated 1.4 form-factor validation, consumer-registry validation, Firefox integration, deterministic public design-site validation, and the complete Chromium-rendered reference/form-factor matrix.
- Final exact promotion head `a8dfb979e85b2636130880bfd11cdfd4c7679b60` passed the entire promotion stack again in Glaze UI CI #128 / run `32541459970`, including the retained 1.2/1.3 rendered assertions and the complete Mobile, Tablet, Desktop, Wide Desktop, TV, reduced-motion, and TV forced-colors matrix.
- PR #28 was promoted from draft only after CI #128 passed and was squash-merged with expected-head protection as canonical Stable commit `01c86323f8b747373d308026adc8b0881855cdc5`.

### Compatibility

- Glaze UI 1.3.0 remains a supported older Stable consumer target.
- Manager remains intentionally pinned to 1.3.0, the public website consumer remains pinned to 1.1.0, Tasks remains an Adoption Candidate against 1.3.0, and unverified consumers remain unverified until separately audited.
- Native applications still require application-specific native/real-device acceptance; design-system-core Stable status does not certify downstream products.
- Speculative intelligence, agents, automation, ambient computing, voice, and operating-experience concepts remain Planned/roadmap-only.

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
- PR #6 was moved from draft to ready for review only after the exact-head workflow succeeded.
- PR #6 was squash-merged with expected-head protection as Stable merge commit `2ac8d0cd444c8234e908e31b05b2cb4dc7d3e5a9` with release title `Glaze UI 1.3.0`.
- Glaze UI 1.3.0 is now the supported older Stable baseline. Glaze UI 1.2.0 remains part of historical and compatibility records.

### Preserved

- Canvas, Solid, Raised, Glaze, and Overlay hierarchy.
- Compact, Medium, Expanded, and Wide adaptive model.
- Complete Glaze UI 1.2 application-interface semantics and rendered-acceptance coverage.
- 44px minimum actionable targets, visible focus, semantic state layers, form/selection semantics, safe-area handling, privacy boundaries, and resilience fallbacks.
- Product personality and the rule that visual quality must not regress for the sake of standardization.

## 1.2.0 — 2026-08-20

Stable application-interface expansion focused on form semantics, selection controls, explicit focus treatment, feedback completeness, and stronger adoption safety.

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