# Glaze UI

Glaze UI is GoreeCloud's shared visual and interaction design system. **Beauty is a requirement, not a regression risk.** It standardizes reusable semantics, accessibility, resilience, privacy and cross-platform behavior without flattening product personality.

## Current Stable — Glaze UI 2.1

**Glaze UI 2.1.0 is the current Stable canonical baseline.** Its governing sentence is **Make interaction feel tangible.** Its defining identity is **ergonomic spatial hierarchy + Glaze Material + connected transformation + adaptive expression**.

`GLAZE_UI_2_1_STABLE.md` is the current release contract. `GLAZE_UI_2_1_CANDIDATE.md`, `acceptance/2.1-candidate.md`, `css/glaze-2.1.reference.css`, `css/glaze-2.1.visual-excellence.css` and `js/glaze-2.1.candidate.mjs` remain preserved as promotion-source evidence; their Candidate naming does not make the promoted 2.1 semantics non-Stable.

Current material hierarchy: **Canvas → Surface → Soft Glaze → Glaze → Deep Glaze → Live Glaze**. Content defaults to Canvas/Surface. Interaction uses Glaze Material according to role, with the approved 2.1 presentation making translucency more perceptible while retaining accent and semantic color coding. Reduced Transparency / Solid and Forced Colors remain authoritative effects-free renderings.

Stable 2.1 includes Clear/Balanced/Solid clarity, Light/Dark/Deep Dark, Calm/Balanced/Expressive, Connected Transformation, Navigation Capsule, Live Surfaces, deterministic Material Budgets, performance profiles, density profiles, accessibility-resolution precedence, six canonical reference flows, source-pinned pixel regression, foldable hinge awareness, compact wearable rotational navigation, spatial floating surfaces, a 48px general reference target floor, a 56px Touch Assistance/TV floor where applicable, and effects-free accessibility fallbacks.

Human Visual Excellence for the refined color-coded glass presentation was explicitly approved on 2026-08-30. The approved source-pinned visual baseline is `5b46903c18660ae78e7f1aaea39a93136efacda7`.

## Historical promotion evidence

Glaze UI **2.0.0** is the immediately preceding historical Stable baseline. The exact 2.0 pre-promotion Candidate remains preserved in `GLAZE_UI_2.md`, `tokens/glaze-2.candidate.json` and `acceptance/2.0-candidate.md`. The promoted 2.0 implementation remains at its Candidate-named evidence paths such as `css/glaze-2.candidate.css` and `js/glaze-2.candidate.js` for reproducible regression and rollback analysis.

Glaze UI 1.0.0 through 1.6.0 and 2.0.0 remain preserved for audit, migration, rollback diagnosis and permanent regression evidence. Their historical status does not make them active production targets.

## Design lineage

Glaze UI is informed by **Samsung One UI 8.5**, **Apple Liquid Glass** and **Google Material 3 Expressive**, reinterpreted through GoreeCloud privacy, identity, accessibility, resilience and self-hosted requirements. These are references, not templates.

## Full-spectrum enforcement

Glaze UI is mandatory identity architecture, not a theme. `ENFORCEMENT.md` and `tokens/enforcement.json` define a fail-closed, non-exhaustive contract for GoreeCloud-controlled user-visible and interaction-facing decisions.

Privacy Shield remains privacy-control authority; Wardveil Security security/protection authority; Everkeep resilience/preservation/recovery/portability/succession/digital-legacy authority; GoreeCloud Mesh coordination/governance authority; application logic application-state authority. Glaze UI presents supplied state and never invents evidence, execution authority or domain truth.

## Retained Stable form-factor evidence

The **dependency-free five-profile reference** remains a permanent regression suite:

- Mobile 390×844
- Tablet 820×1180
- Desktop 1280×900
- Wide Desktop 1600×1000
- TV 1920×1080

2.x additionally retains representative foldable, wearable and spatial references. Form factor is chosen from task, window, input, viewing distance, posture/resizability and platform convention—not width/device name alone.

## Mandatory current-Stable consumer target

The current Stable consumer target is **2.1.0**, recorded by `consumers/registry.json`. It is the only version that may satisfy a current application conformance or production-readiness requirement.

All audited consumers remain `migration-required` or `unverified` immediately after the 2.1 design-system promotion. **No application is upgraded by declaration**, and there are no application-level production exceptions. Existing 2.0 and earlier evidence is migration input only until each repository adopts 2.1 and completes its own rendered/native/accessibility/platform acceptance.

Stable platform-neutral wearable/spatial semantics do not certify a downstream native/hardware product. Such consumers still require application-specific native, accessibility, system-integration, performance and representative physical-device acceptance.

The canonical consumer registry retains the bounded 2.1 Candidate assessment as historical promotion provenance only; it cannot satisfy Stable consumer conformance.

## Stability priority

Glaze UI remains stabilization-first. `STABILITY.md` governs compatibility, promotion, rollback and mandatory migration; `COMPONENT_STATUS.md` governs Stable, Candidate, Experimental and Planned lifecycle states; `CONSUMERS.md` / `consumers/registry.json` govern evidence-backed alignment.

Glaze Motion remains Experimental unless separately promoted. Speculative intelligence capabilities, agents, automation, ambient computing, voice, operating-experience or other roadmap concepts do not enter Stable merely because they are discussed.

## Repository layout

- `VERSION` — current Stable semantic version (`2.1.0`).
- `GLAZE_UI_2_1_STABLE.md` — current 2.1 Stable release contract.
- `css/glaze-2.1.0.css` / `js/glaze-2.1.0.mjs` — versioned 2.1 Stable web/runtime entrypoints.
- `GLAZE_UI_2_1_CANDIDATE.md`, `acceptance/2.1-candidate.md`, `reference/candidate-2.1-*.html`, `css/glaze-2.1.reference.css`, `css/glaze-2.1.visual-excellence.css`, and `js/glaze-2.1.candidate.mjs` — immutable 2.1 promotion-source/reference evidence.
- `GLAZE_UI_2_STABLE.md` — historical 2.0 Stable release contract.
- `GLAZE_UI_2.md` / `tokens/glaze-2.candidate.json` — immutable 2.0 Candidate promotion-source evidence.
- `tokens/glaze.tokens.json` — canonical Stable token map with current 2.1 summary and retained compatibility fields.
- `css/glaze-2.candidate.css` / `js/glaze-2.candidate.js` — promoted 2.0 web implementation retained at evidence paths.
- `css/glaze-2.foldable.candidate.css` — retained foldable primitives.
- `css/glaze-2.emerging.candidate.css` / `js/glaze-2.emerging.candidate.js` — retained platform-neutral wearable/spatial primitives.
- `reference/candidate-2.0*.html` and `scripts/validate_candidate_2_*` — permanent 2.0 rendered/resilience regression evidence.
- `reference/native/android/buildable/` and `.github/workflows/glaze-2.1-android-native.yml` — bounded Android handheld source/build/emulator evidence for the 2.1 design-system reference.
- `schemas/consumer-registry.schema.json`, `consumers/registry.json` and `scripts/validate_consumer_registry.py` — mandatory current-Stable consumer migration governance.
- legacy `css/glaze*.css`, 1.5/1.6 subsystem layers and canonical reference — permanent compatibility regressions.
- `COMPONENTS.md`, `CONFORMANCE.md`, `ADOPTION.md`, `ACCEPTANCE.md`, `STABILITY.md`, `COMPONENT_STATUS.md` — current governance.

## Validation

Pull-request workflows validate the **exact source revision** and remain authoritative. Core commands include:

```bash
python3 scripts/validate_glaze_ui.py
python3 scripts/validate_release_state.py
python3 scripts/validate_glaze_2_stable.py
python3 scripts/validate_glaze_2_1_stable.py
python3 scripts/validate_enforcement.py
python3 scripts/validate_form_factors.py
python3 scripts/validate_consumer_registry.py
python3 scripts/validate_wearables.py
node --test tests/glaze-2.1-runtime.test.mjs
python3 scripts/validate_glaze_2_1_rendered.py
python3 scripts/validate_glaze_2_1_expanded_rendered.py
python3 scripts/validate_glaze_2_1_resilience_rendered.py
```

The 2.1 source-pinned screenshot workflow re-renders the immutable approved baseline source and current exact head on the same Chromium runner before comparison. The Android workflow builds, installs and launches the exact-source native reference and executes the bounded runtime acceptance. Neither design-system gate substitutes for downstream physical-device acceptance.

Retained 1.3–2.0 validators and rendered matrices remain permanent regressions. A prior or partial run is not equivalent to exact-final-revision CI.

## Versioning

Glaze UI follows semantic versioning. Patch releases are compatible corrections; minor releases add compatible semantics; major releases may change established contracts. Glaze UI 2.1 is a compatible Stable refinement of the 2.x architecture, with a stronger bounded glass presentation, deterministic material/accessibility contracts, and expanded acceptance infrastructure.

## License

MIT. GoreeCloud branding and product identity remain subject to applicable project policies.
