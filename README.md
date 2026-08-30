# Glaze UI

Glaze UI is GoreeCloud's shared visual and interaction design system. **Beauty is a requirement, not a regression risk.** It standardizes reusable semantics, accessibility, resilience, privacy and cross-platform behavior without flattening product personality.

## Current Stable — Glaze UI 2.0

**Glaze UI 2.0.0 is the current Stable canonical baseline.** Its governing sentence is **Make interaction feel tangible.** Its defining identity is **ergonomic spatial hierarchy + Glaze Material + connected transformation + adaptive expression**.

`GLAZE_UI_2_STABLE.md` is the current release contract. The exact 37-section pre-promotion Candidate remains preserved in `GLAZE_UI_2.md`, `tokens/glaze-2.candidate.json` and `acceptance/2.0-candidate.md`; its Candidate lifecycle labels are historical evidence, not the current release status.

Current material hierarchy: **Canvas → Surface → Soft Glaze → Glaze → Deep Glaze → Live Glaze**. Content defaults to Canvas/Surface; interaction uses Glaze Material according to role. Stable 2.0 also includes Clear/Balanced/Solid clarity, Light/Dark/Deep Dark, Calm/Balanced/Expressive, Connected Transformation, Navigation Capsule, Live Surfaces, foldable hinge awareness, compact wearable rotational navigation, spatial floating surfaces, a 48px general target floor, a 56px TV floor and effects-free accessibility fallbacks.

The promoted implementation retains Candidate-named source paths for reproducible promotion evidence: `css/glaze-2.candidate.css`, `js/glaze-2.candidate.js`, foldable/emerging Candidate layers and their rendered harnesses. Their filenames do not make the promoted semantics non-Stable.

## Active Candidate — Glaze UI 2.1

Glaze UI **2.1.0-candidate.1** is the active refinement line. It is not consumer-eligible and does not change repository `VERSION`, the current Stable target, or any consumer's Stable conformance state.

The bounded Candidate implementation currently includes machine-readable component/material/accessibility contracts, executable preference/material resolution, six canonical web reference flows, interaction and computed visual-invariant regression, resilience/exception-state acceptance, source-pinned same-run screenshot pixel regression, a native Android handheld reference with a dedicated emulator acceptance gate, and a fail-closed 2.1 assessment layer in the existing canonical `consumers/registry.json`.

The Android reference uses Android-native framework controls, not WebView, and exercises content-first Surface composition, bounded Glaze interaction, 48/56 dp target floors, Light/Dark/Deep Dark, Solid Reduced-Transparency fallback, 200% system text scaling reachability, and explicit simulated semantic-state labels. Emulator success remains different from TalkBack, OEM/physical-device, signing/distribution and human Visual Excellence acceptance.

No downstream 2.1 consumer evaluation is currently recorded. Candidate assessment machinery is migration/readiness infrastructure only; **2.0.0 remains the only version that may satisfy the production consumer gate** until formal 2.1 promotion.

## Design lineage

Glaze UI is informed by **Samsung One UI 8.5**, **Apple Liquid Glass** and **Google Material 3 Expressive**, reinterpreted through GoreeCloud privacy, identity, accessibility, resilience and self-hosted requirements. These are references, not templates.

## Full-spectrum enforcement

Glaze UI is mandatory identity architecture, not a theme. `ENFORCEMENT.md` and `tokens/enforcement.json` define a fail-closed, non-exhaustive contract for GoreeCloud-controlled user-visible and interaction-facing decisions.

Privacy Shield remains privacy-control authority; Wardveil Security security/protection authority; Everkeep resilience/preservation/recovery/portability/succession/digital-legacy authority; GoreeCloud Mesh coordination/governance authority; application logic application-state authority. Glaze UI presents supplied state and never invents evidence, execution authority or domain truth.

## Historical Stable compatibility

Glaze UI **1.6.0** is the immediately preceding historical Stable baseline. Releases 1.0.0 through 1.6.0 remain preserved for audit, migration, rollback diagnosis and permanent regression evidence. Their Canvas/Solid/Raised/Functional Glass/Clear Glass/Overlay vocabulary is legacy 1.x compatibility semantics only.

The retained 1.3 expressive foundation, 1.4 form-factor layer, 1.5 color/iconography/motion/material/layout/state systems and 1.6 evidence-presentation/adaptive-workspace systems remain permanent compatibility regressions. Historical stability does not make 1.x an active production target.

## Retained Stable form-factor evidence

The **dependency-free five-profile reference** remains a permanent regression suite:

- Mobile 390×844
- Tablet 820×1180
- Desktop 1280×900
- Wide Desktop 1600×1000
- TV 1920×1080

2.0 additionally retains representative foldable, wearable and spatial references. Form factor is chosen from task, window, input, viewing distance, posture/resizability and platform convention—not width/device name alone.

## Mandatory current-Stable consumer target

The current Stable consumer target is **2.0.0**, recorded by `consumers/registry.json`. It is the only version that may satisfy current application conformance or production-readiness requirements.

Every evidenced 1.x consumer is migration-required after 2.0 promotion. Launcher and Keyboard's former 1.6 Adoption Candidate records remain historical migration evidence, not 2.0 evidence. Notes remains Unverified. No application is upgraded by declaration, and there are no application-level production exceptions.

Stable platform-neutral wearable/spatial semantics do not certify a downstream native/hardware product. Such consumers still require application-specific native, accessibility, system-integration, performance and representative physical-device acceptance.

The canonical consumer registry also carries the bounded 2.1 Candidate assessment layer. A Candidate evaluation cannot make an application production eligible or replace its recorded Stable state.

## Stability priority

Glaze UI remains stabilization-first. `STABILITY.md` governs compatibility, promotion, rollback and mandatory migration; `COMPONENT_STATUS.md` governs Stable, Candidate, Experimental and Planned lifecycle states; `CONSUMERS.md` / `consumers/registry.json` govern evidence-backed alignment.

Glaze Motion remains Experimental unless separately promoted. Speculative intelligence capabilities, agents, automation, ambient computing, voice, operating-experience or other roadmap concepts do not enter Stable merely because they are discussed.

## Repository layout

- `VERSION` — current Stable semantic version.
- `GLAZE_UI_2_STABLE.md` — current 2.0 Stable release contract.
- `GLAZE_UI_2.md` / `tokens/glaze-2.candidate.json` — immutable 2.0 Candidate promotion-source evidence.
- `GLAZE_UI_2_1_CANDIDATE.md` / `registry/lifecycle.json` — active 2.1 Candidate contract and lifecycle authority.
- `tokens/glaze.tokens.json` — canonical Stable token map with current 2.0 summary and legacy 1.x compatibility fields.
- `css/glaze-2.candidate.css` / `js/glaze-2.candidate.js` — promoted 2.0 web implementation retained at evidence paths.
- `css/glaze-2.foldable.candidate.css` — promoted foldable primitives.
- `css/glaze-2.emerging.candidate.css` / `js/glaze-2.emerging.candidate.js` — promoted platform-neutral wearable/spatial primitives.
- `reference/candidate-2.0*.html` and `scripts/validate_candidate_2_*` — permanent 2.0 rendered/resilience regression evidence.
- `reference/candidate-2.1-*.html`, `js/glaze-2.1.candidate.mjs` and `scripts/validate_glaze_2_1_*` — active 2.1 web Candidate runtime/reference/acceptance evidence.
- `reference/native/android/buildable/` and `.github/workflows/glaze-2.1-android-native.yml` — bounded Android handheld Candidate source/build/emulator evidence.
- `schemas/consumer-registry.schema.json`, `consumers/registry.json` and `scripts/validate_consumer_registry.py` — Stable consumer audit plus non-production 2.1 Candidate assessment machinery.
- legacy `css/glaze*.css`, 1.5/1.6 subsystem layers and canonical reference — permanent compatibility regressions.
- `COMPONENTS.md`, `CONFORMANCE.md`, `ADOPTION.md`, `ACCEPTANCE.md`, `STABILITY.md`, `COMPONENT_STATUS.md` — current governance.

## Validation

The pull-request workflows validate the **exact candidate revision** and remain authoritative. Core commands include:

```bash
python3 scripts/validate_glaze_ui.py
python3 scripts/validate_release_state.py
python3 scripts/validate_glaze_2_stable.py
python3 scripts/validate_glaze_2_candidate.py
python3 scripts/validate_enforcement.py
python3 scripts/validate_form_factors.py
python3 scripts/validate_typography_contract.py
python3 scripts/validate_consumer_registry.py
python3 integrations/firefox/validate.py
python3 website/validate.py
python3 scripts/validate_rendered_reference.py
python3 scripts/validate_candidate_2_rendered.py
python3 scripts/validate_candidate_2_resilience.py
python3 scripts/validate_candidate_2_emerging.py
node scripts/validate_candidate_2_contrast.mjs
python3 scripts/validate_glaze_2_1_candidate.py
python3 scripts/validate_glaze_2_1_regression.py
python3 scripts/validate_glaze_2_1_native.py
```

The 2.1 Android emulator runtime validator is executed by `.github/workflows/glaze-2.1-android-native.yml` after the exact-source debug APK is built, installed and launched. It is not a substitute for physical-device acceptance.

Retained 1.3–1.6 validators/rendered matrices remain permanent Stable regressions. A prior or partial run is not equivalent to exact-final-revision CI.

## Versioning

Glaze UI follows semantic versioning. Patch releases are compatible corrections; minor releases add compatible semantics; major releases may change established contracts. Glaze UI 2.0 is a major migration because its material hierarchy, geometry, motion timing, personalization, adaptive interaction, component grammar, foldable/wearable/spatial semantics and Connected Transformation contract supersede established 1.x design semantics.

## License

MIT. GoreeCloud branding and product identity remain subject to applicable project policies.
