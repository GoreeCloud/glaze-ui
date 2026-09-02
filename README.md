# Glaze UI

Glaze UI is GoreeCloud's shared visual and interaction design system. **Beauty is a requirement, not a regression risk.** It standardizes reusable semantics, accessibility, resilience, privacy and cross-platform behavior without flattening product personality.

## Current Stable — Glaze UI 2.2

**Glaze UI 2.2.0 is the current Stable canonical baseline.** Its governing shell principle is **Solid where users read or make explicit critical decisions. Glazed where users interact with transient navigation, command, search, control, or feedback chrome.** Its defining identity remains **ergonomic spatial hierarchy + Glaze Material + connected transformation + adaptive expression**.

`GLAZE_UI_2_2_STABLE.md` is the current release contract. The 2.2 Candidate contract, Candidate acceptance records, Candidate-named CSS/runtime implementation layers and exact visual-review source remain preserved as promotion provenance; their filenames do not make the promoted 2.2 semantics non-Stable.

Stable 2.2 includes the bounded System Shell, a 32-component contract catalog across Foundation, Structure, Overlay, Signature and Intelligence, bounded Universal Search and Control Center reference behavior, migration compatibility, deterministic performance/System Glaze budgets, source-pinned screenshot pixel regression, Optical Reachability presentation, and a bounded Android handheld native reference.

Current material hierarchy remains **Canvas → Surface → Soft Glaze → Glaze → Deep Glaze → Live Glaze**. Durable readable content stays solid. Transient interaction uses bounded Glaze according to role, with at most one dominant Glaze system panel in ordinary composition and one to three small floating Glaze controls. Reduced Transparency / effective Solid and Forced Colors remain authoritative effects-free renderings.

Stable 2.2 retains Light/Dark/Deep Dark, Calm/Balanced/Expressive, Connected Transformation, adaptive density, accessibility-resolution precedence, foldable/wearable/spatial compatibility evidence, a 48px touch-oriented reference target floor, a 56px Touch Assistance/far-view floor where applicable, visible focus, non-color semantic state, and effects-free accessibility fallbacks.

Human Visual Excellence for the 2.2 Optical Reachability presentation was explicitly **Accepted** on 2026-09-01. The immutable approved visual source is `0411b0f6dd877aea30e2c5674e1acde0105fd97b`.

## Historical promotion evidence

Glaze UI **2.1.0** is the immediately preceding historical Stable baseline and the rollback reference for 2.2.0. Its release contract, acceptance, versioned CSS/runtime entrypoints, source-pinned visual baseline and bounded Android reference remain preserved for reproducible regression, migration, rollback diagnosis and audit.

Glaze UI **2.0.0** and Glaze UI 1.0.0 through 1.6.0 also remain preserved as historical release and permanent regression evidence. Their historical status does not make them active production targets.

## Design lineage

Glaze UI is informed by **Samsung One UI 8.5**, **Apple Liquid Glass** and **Google Material 3 Expressive**, reinterpreted through GoreeCloud privacy, identity, accessibility, resilience and self-hosted requirements. These are references, not templates.

## Full-spectrum enforcement

Glaze UI is mandatory identity architecture, not a theme. `ENFORCEMENT.md` and `tokens/enforcement.json` define a fail-closed, non-exhaustive contract for GoreeCloud-controlled user-visible and interaction-facing decisions.

Privacy Shield remains privacy-control authority; Wardveil Security security/protection authority; Everkeep resilience/preservation/recovery/portability/succession/digital-legacy authority; GoreeCloud Mesh coordination/governance authority; application logic application-state authority. Glaze UI presents supplied state and never invents evidence, execution authority or domain truth.

## Retained form-factor evidence

The dependency-free five-profile compatibility reference remains a permanent regression suite:

- Mobile 390×844
- Tablet 820×1180
- Desktop 1280×900
- Wide Desktop 1600×1000
- TV 1920×1080

2.x additionally retains representative foldable, wearable and spatial references. Form factor is chosen from task, window, input, viewing distance, posture/resizability and platform convention—not width/device name alone.

## Mandatory current-Stable consumer target

The current Stable consumer target is **2.2.0**, recorded by `consumers/registry.json`. It is the only Glaze UI version that may satisfy a current application conformance or production-readiness requirement.

All audited consumers remain `migration-required` or `unverified` immediately after the 2.2 design-system promotion. **No application is upgraded by declaration**, and there are no application-level production exceptions. Existing 2.1 and earlier evidence is migration input only until each repository adopts 2.2 and completes its own rendered/native/accessibility/platform acceptance.

Stable platform-neutral and bounded Android reference evidence does not certify a downstream native/hardware product. Such consumers still require application-specific native, accessibility, system-integration, performance and representative physical-device acceptance.

The canonical consumer registry retains the bounded 2.2 Candidate assessment as historical promotion provenance only; it cannot satisfy Stable consumer conformance.

## Stability priority

Glaze UI remains stabilization-first. `STABILITY.md` governs compatibility, promotion, rollback and mandatory migration; `COMPONENT_STATUS.md` governs Stable, Candidate, Experimental and Planned lifecycle states; `CONSUMERS.md` / `consumers/registry.json` govern evidence-backed alignment.

Glaze Motion remains Experimental unless separately promoted. Speculative intelligence capabilities beyond the bounded Stable 2.2 component/reference contracts, agents, automation, ambient computing, voice, or other roadmap concepts do not enter Stable merely because they are discussed.

## Repository layout

- `VERSION` — current Stable semantic version (`2.2.0`).
- `GLAZE_UI_2_2_STABLE.md` — current 2.2 Stable release contract.
- `acceptance/2.2-stable.md` — exact-revision Stable promotion acceptance and release-closure boundary.
- `css/glaze-2.2.0.css` / `js/glaze-2.2.0.mjs` — versioned 2.2 Stable consumer entrypoints.
- `GLAZE_UI_2_2_CANDIDATE.md`, `acceptance/2.2-candidate.md`, `acceptance/2.2-visual-review.md`, 2.2 Candidate-named CSS/runtime layers and 2.2 reference harnesses — preserved promotion-source/reference evidence.
- `contracts/components/2.2/` — complete 32-component 2.2 contract catalog.
- `contracts/system-shell/glaze-system-shell-2.2.json` — bounded 2.2 System Shell contract.
- `contracts/migration/glaze-2.1-to-2.2.json` / `MIGRATION_2_1_TO_2_2.md` — current Stable migration contract.
- `contracts/performance/glaze-2.2-performance-budget.json` — 2.2 performance and System Glaze-budget evidence.
- `contracts/regression/visual-baselines-2.2.json` — source-pinned 2.2 visual baseline authority.
- `reference/native/android/2.2-candidate/` and `.github/workflows/glaze-2.2-android-native.yml` — bounded Android handheld 2.2 promotion source and exact-head Stable native acceptance.
- `GLAZE_UI_2_1_STABLE.md`, `acceptance/2.1-stable.md`, `css/glaze-2.1.0.css`, `js/glaze-2.1.0.mjs` and `reference/native/android/buildable/` — retained 2.1 historical release/regression authority and rollback evidence.
- `schemas/consumer-registry.schema.json`, `consumers/registry.json` and `scripts/validate_consumer_registry.py` — mandatory current-Stable consumer migration governance.
- legacy `css/glaze*.css`, 1.5/1.6 subsystem layers and canonical reference — permanent compatibility regressions.
- `COMPONENTS.md`, `CONFORMANCE.md`, `ADOPTION.md`, `ACCEPTANCE.md`, `STABILITY.md`, `COMPONENT_STATUS.md` — governance and compatibility documentation.

## Validation

Pull-request workflows validate the **exact source revision** and remain authoritative. Current promotion/maintenance commands include:

```bash
python3 scripts/validate_release_state.py
python3 scripts/validate_glaze_2_2_stable.py
python3 scripts/validate_glaze_2_2_migration.py
python3 scripts/validate_consumer_registry.py
python3 scripts/validate_enforcement.py
node --test tests/glaze-2.2-runtime.test.mjs tests/glaze-2.2-system-interactions.test.mjs tests/glaze-2.2-performance.test.mjs
python3 scripts/validate_glaze_2_2_rendered.py
python3 scripts/validate_glaze_2_2_components_rendered.py
python3 scripts/validate_glaze_2_2_structure_rendered.py
python3 scripts/validate_glaze_2_2_overlay_rendered.py
python3 scripts/validate_glaze_2_2_advanced_rendered.py
python3 scripts/validate_glaze_2_2_system_interactions_rendered.py
python3 scripts/validate_glaze_2_2_performance_rendered.py
python3 scripts/validate_glaze_2_2_optical_reachability_rendered.py
python3 scripts/validate_glaze_2_1_historical.py
```

The 2.2 source-pinned screenshot workflow independently re-renders immutable approved source `0411b0f6dd877aea30e2c5674e1acde0105fd97b` and the current exact head on the same Chromium runner before comparison. The 2.2 Android workflow builds, installs and launches the exact-source bounded native reference and executes runtime/accessibility/resilience acceptance. Neither design-system gate substitutes for downstream physical-device acceptance.

Retained 1.x, 2.0 and 2.1 validators/rendered/native matrices remain permanent regressions appropriate to their historical lifecycle. A prior or partial run is not equivalent to exact-final-revision CI.

## Versioning

Glaze UI follows semantic versioning. Patch releases are compatible corrections; minor releases add compatible semantics; major releases may change established contracts. Glaze UI 2.2.0 is a compatible Stable refinement of the 2.x architecture with a complete bounded component contract catalog, stronger System Shell hierarchy, deterministic interaction and material budgets, accessibility-preserving Optical Reachability, and expanded exact-head acceptance infrastructure.

## License

MIT. The current license remains appropriate for the reusable Glaze UI software/design-system implementation. GoreeCloud branding and product identity remain subject to applicable project policies and are not granted merely by the software license.
