# Changelog

All notable changes to the Glaze UI reference implementation are recorded here.

## 2.2.0 — Stable — 2026-09-01

- Promoted the accepted Glaze UI 2.2 Candidate design-system surface to `2.2.0` Stable without rewriting the human-reviewed Candidate presentation or its immutable provenance.
- Adds versioned Stable entrypoints `css/glaze-2.2.0.css` and `js/glaze-2.2.0.mjs` over preserved Candidate implementation layers.
- Promoted the bounded System Shell, 32-component contract catalog, Foundation/Structure/Overlay/Signature/Intelligence reference presentation, Universal Search and Control Center reference interactions, performance/System Glaze budget, Optical Reachability presentation, source-pinned visual regression and bounded Android handheld reference into the Stable contract.
- Preserves the Human Visual Excellence decision **Accepted** for source revision `0411b0f6dd877aea30e2c5674e1acde0105fd97b` and requires source-pinned regression to prove presentation continuity on the exact promotion head.
- Moved lifecycle, canonical token, enforcement, consumer-target, migration and Design Center authorities to the `2.2.0` Stable boundary while preserving `2.1.0` as the documented rollback and historical regression baseline.
- Keeps every downstream GoreeCloud application separately migration-gated and non-production-eligible until its own repository-local 2.2 adoption, accessibility, rendered/native and product acceptance gates pass.
- Retains compact platform-neutral wearable/spatial semantics while keeping historical native wearable evidence isolated; neither browser references nor the bounded Android handheld reference certify Wear OS, watchOS or downstream physical devices.
- Keeps Glaze Motion Experimental and prevents Candidate/Experimental capability from becoming a Stable consumer dependency by implication.
- Corrects lifecycle-transition drift discovered by fail-closed validation, including Candidate-only migration language, superseded 2.1 current-Stable assumptions, public Design Center 2.1 publication, canonical token authority, wearable lifecycle authority and the system-interaction rendered-validator path. No acceptance threshold or semantic requirement is weakened.
- Stable release completed after exact-head and post-merge GitHub/Cloudflare validation, expected-head-protected PR #115 merge as `6731098b28dd0393faa878c70d989a221d714a20`, annotated `v2.2.0` tag creation, GitHub Release `380971405`, and recorded release-closure evidence.

## 2.0.0 — Stable — 2026-08-28

- Promoted the administrator-enforced Glaze UI 2.0 design contract to the current Stable GoreeCloud design-system baseline under the governing sentence **Make interaction feel tangible.**
- Established the current Glaze Material hierarchy as Canvas / Surface / Soft Glaze / Glaze / Deep Glaze / Live Glaze, with Clear / Balanced / Solid clarity, Light / Dark / Deep Dark appearance, Calm / Balanced / Expressive expression, Connected Transformation, Navigation Capsule, Live Surfaces, foldable hinge awareness, wearable rotational navigation, and spatial floating surfaces.
- Preserved the exact 2.0 Candidate contract, token snapshot, implementation filenames, and acceptance record as immutable pre-promotion provenance rather than rewriting historical Candidate evidence.
- Promoted 48px general and 56px TV interaction floors, state-preserving no-View-Transition fallback, 1114×834 hinge-aware foldable acceptance, representative wearable rotational navigation, spatial flat fallback, increased-contrast emulation, reduced-motion/transparency, forced-colors, and no-backdrop resilience as Stable design-system evidence.
- Kept native or real-device wearable/spatial certification application-specific; the platform-neutral design-system release does not certify Wear OS, watchOS, XR hardware, crown input, native accessibility APIs, host-managed surfaces, or physical-device performance.
- Migrated canonical release-state governance, enforcement metadata, component/lifecycle/conformance/adoption records, Design Center publication, and the mandatory consumer target from 1.6.0 to 2.0.0.
- Reclassified every evidenced 1.x consumer as migration-required under the 2.0 current-Stable rule without manufacturing downstream 2.0 conformance; GoreeCloud Notes remains Unverified.
- Retained Glaze UI 1.x source/rendered suites and Glaze Motion 0.6 Experimental evidence as permanent compatibility/regression gates; Glaze Motion remains Experimental and is not promoted by the 2.0 release.
- Release-state migration exposed two wording-only validator mismatches (`View Transitions are unavailable` provenance wording and the explicit `Wearable rotational navigation` Stable boundary). Both were corrected without weakening product or rendered acceptance assertions.
- Exact promotion head `5478407bf6fbc013f28fd5100d6674dfd20c92d4` passed Glaze UI CI #505 / run `33164360997`, Semantic Color #225 / run `33164361128`, Icon Construction #190 / run `33164360987`, and Icon Identity #182 / run `33164361019`.
- Cloudflare Pages successfully deployed the exact promotion head to the PR/branch preview before merge; production promotion remains bound to the controlled `main` merge.

## 1.6.0 — Stable — 2026-08-28

- Promoted Evidence Presentation and Authority Surfaces to Stable with producer-authority separation across Wardveil Security, Privacy Shield, Everkeep, GoreeCloud Mesh, and Glaze UI presentation authority.
- Promoted Adaptive Workspace and Navigation to Stable across Mobile, Tablet, Desktop, Wide Desktop, and distinct far-view TV composition.
- Retained fail-closed rendered matrices for light/dark, reduced motion, reduced transparency, forced colors, constrained-performance fallbacks, density, target floors, and 200% text reflow.
- Fixed the Candidate 200% Mobile evidence reflow defect before promotion; the acceptance gate was not weakened.
- Candidate promotion evidence head `9a632e8df5ddd3a66c19ef2bb90efb7e65678048` passed Glaze UI CI #460, Icon Construction #145, Icon Identity #137, and Semantic Color #180 before merge as `cc50ad8debce49b254da424399768741b0a5a96e`.
- Glaze Motion remains Experimental and wearable production support remains deferred/production-blocked.
- `1.6.0` becomes the mandatory current Stable consumer target; existing 1.5 and older application evidence becomes migration input only until each consumer completes 1.6 adoption and application-specific acceptance.

## Unreleased

### Glaze UI 1.6 — Adaptive Workspace Candidate

- Added `WORKSPACE_NAVIGATION.md` as the Candidate contract for semantic window/workspace regions, title areas, navigation, toolbars, primary content, inspectors, status regions, overlays, density, input-aware targets, responsive transformation, accessibility/resilience, and platform-authority boundaries.
- Added `tokens/workspace-navigation.candidate.json` so the workspace anatomy, dimensions, target floors, geometry, navigation transformations, adaptation invariants, accessibility requirements, and authority bindings are machine-readable.
- Added `css/glaze.workspace.candidate.css` with reusable Desktop/Tablet/Mobile workspace composition, sidebar and inspector transformation, pointer/touch target adaptation, reduced-motion, reduced-transparency, no-backdrop-filter, and forced-colors behavior.
- Added `reference/candidate-1.6-workspace.html` as a dependency-free evaluation surface and `scripts/validate_workspace_navigation.py` as a fail-closed Candidate validator.
- Wired the Candidate validator into the exact-head Glaze UI CI workflow and surfaced a bounded workspace preview in the Design Center without changing the Stable production target.
- Corrected Design Center Facet authority wording: the authoritative identity source is `GoreeCloud/goreecloud-branding-assets` at `systems/glaze-ui/glaze-ui-mark.svg`; this repository publishes a synchronized byte-equivalent consumer copy.
- Glaze UI 1.5.0 remains the current Stable baseline. The Adaptive Workspace layer does not trigger consumer migration or permit Stable 1.6 conformance claims until the normal promotion gate is completed.

### Glaze Motion — Experimental

- Motion Core 0.3 was merged as `f1f42eab087b9b49623b8db63d8ecbe399fccdf6`, adding semantic reorder/swipe/pan/zoom state, directional keyboard/remote parity, local-only frame-budget instrumentation, native mapping guidance, and reference-consumer evidence while remaining outside the Glaze UI 1.5 Stable compatibility promise.
- Motion Core 0.4 adds a compatibility-preserving aggregate runtime entry point, localization-neutral accessible reorder commands and position metadata, and a bounded local settling-animation budget that can refuse optional settling under reduced motion or saturation without blocking semantic state updates.
- Rendered Glaze Motion acceptance is expanded to Mobile, Desktop, and TV web/reference profiles in both normal and reduced-motion modes; this is development evidence and not native or real-device certification.
- Motion Core 0.5 records the first merged first-party downstream evaluation from GoreeCloud Launcher PR #22 (`23a389b3b24db726ceab5e328f9f8157fa7655ae`) after Android CI #67 passed the repository, build, unit, Room, and Android 16 emulator gates. The evaluation remains test-only and does not activate Experimental Motion in production.
- Motion Core 0.6 adds the second merged first-party native evaluation from GoreeCloud Keyboard PR #4 (`c9c0500263b40640339cf7a46f1a029d9a2ac240`). Exact head `80de7bd2dcff6d07b06b19f8250e37d20155d7ff` passed Android CI #15, including the repository quarantine/build gate and an Android 15 / API 35 x86_64 emulator reduced-motion interaction test against the real `KeyboardView` key-release and suggestion-selection paths.
- The first Keyboard emulator attempt in Android CI #13 exposed a brittle process-level animation-state assertion. The emulator gate was retained and corrected to read Android's authoritative global animator-duration setting; semantic and reduced-motion assertions were not weakened.
- The central consumer registry now records both Launcher and Keyboard as Glaze UI 1.5.0 `adoption-candidate` consumers with `productionEligible: false`; their final native/rendered/accessibility/physical-device acceptance remains pending.
- Motion Core 0.6 is an evidence/governance iteration with the 0.4.0 runtime implementation retained as its compatibility baseline; no new runtime primitive is claimed and two test-only native Android evaluations remain insufficient for Candidate promotion.
- Earlier 0.1/0.2 experimental foundation work remains superseded lineage rather than Stable product capability. Motion Studio and Motion Spatial remain Planned.

## 1.5.0 — 2026-08-25

Stable adaptive-expression and interaction-architecture release. Promotes the validated 1.5 adaptive color, iconography/construction/identity, motion/interaction, material/depth, layout/spacing/density, and semantic state/input-modality systems while retaining the complete 1.4 form-factor layer.

### Added

- Layered adaptive semantic color with protected truth families and accessibility modes.
- Governed iconography, icon construction, optical sizing, identity-lock, semantic badge, and adaptive-presentation contracts.
- Purpose-driven interruptible motion with reduced-motion substitutions and truthful progress/state rules.
- Canvas/Solid/Raised/Functional Glass/Clear Glass/Overlay material and depth architecture with reduced-transparency and constrained-performance fallbacks.
- Semantic spacing, responsive gutters, bounded measures, density modes, safe-area behavior, target floors, localization/order rules, and bounded intrinsic overflow.
- Focus-visible, hover, pressed, selected, expanded, disabled, read-only, loading, invalid, success, and mixed keyboard/pointer/touch/remote/assistive-input semantics.
- `acceptance/1.5.0.md` as the Stable release acceptance record.

### Validation and promotion

- Exact pre-promotion Candidate head `3613fe3b47827e29b23b2606db68f2ec6e7a9434` passed Glaze UI CI #375 / run `32925596296`, Icon Construction #60, Icon Identity #52, and Semantic Color #95.
- Stable release conversion preserves all subsystem/source/rendered gates; the exact final promotion head must pass the full stack before merge.
- Earlier forced-colors TV `PENDING` browser-harness attempts were treated as incomplete, not as passes; no assertion or acceptance threshold was weakened.

### Compatibility and consumer boundary

- Glaze UI 1.4.0 becomes the immediately preceding historical Stable baseline.
- All GoreeCloud-controlled user-facing consumers must migrate to 1.5.0 through evidence-backed application-specific adoption.
- Wearable applications remain production-blocked until an applicable Stable wearable contract exists.
- Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Mesh, and application logic retain authority for underlying truth; Glaze UI remains presentation authority.

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
