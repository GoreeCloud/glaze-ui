# Contributing to Glaze UI

Glaze UI is GoreeCloud's shared design system. Changes should strengthen consistency, accessibility, privacy, resilience, tangible interaction and visual quality without turning GoreeCloud applications into generic clones.

## Principles

- Preserve the current Glaze UI 2.0 visual/interaction character.
- Prefer semantic tokens over literal values.
- Content remains readable; Glaze Material is selective.
- Avoid third-party browser dependencies unless explicitly justified.
- Maintain keyboard, contrast, forced-colors, reduced-motion/transparency, large-text and target-size behavior.
- Keep reference implementations dependency-free.
- Treat product personality as compatible with conformance.
- Preserve producer authority: presentation may not create Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Mesh or application truth.

## Before opening a pull request

Run the Stable source gates from the repository root:

```bash
python3 -m py_compile scripts/validate_glaze_ui.py scripts/validate_release_state.py scripts/validate_glaze_2_stable.py scripts/validate_glaze_2_candidate.py scripts/validate_wearables.py scripts/validate_consumer_registry.py website/build.py website/validate.py integrations/firefox/validate.py
python3 scripts/validate_glaze_ui.py
python3 scripts/validate_release_state.py
python3 scripts/validate_glaze_2_stable.py
python3 scripts/validate_glaze_2_candidate.py
python3 scripts/validate_wearables.py
python3 scripts/validate_consumer_registry.py
python3 integrations/firefox/validate.py
python3 website/validate.py
```

The pull-request workflow is authoritative and checks out the **exact PR head**. Do not merge or promote a Stable-maintenance/release PR until that exact revision passes the complete workflow.

## Rendered and visual acceptance

Presentation/interaction changes must preserve the canonical Stable and 2.0 regression matrices:

```bash
python3 scripts/validate_rendered_reference.py
python3 scripts/validate_candidate_2_rendered.py
python3 scripts/validate_candidate_2_resilience.py
python3 scripts/validate_candidate_2_emerging.py
node scripts/validate_candidate_2_contrast.mjs
```

Review at least:

- Mobile — 390 × 844
- Tablet — 820 × 1180
- Desktop — 1280 × 900
- Wide Desktop — 1600 × 1000
- TV — 1920 × 1080
- representative foldable/hinge posture
- compact wearable rotational-navigation surface
- spatial depth and fully flattened fallback

Review applicable Light/Dark/Deep Dark, reduced-motion/transparency, increased contrast, forced colors, large text, effects-free fallbacks and input model. Screenshots alone are insufficient; representative task flows are required.

## Token changes

Compatible additions normally belong in a minor release. Removing/redefining required semantics may require a major release. The canonical Stable token map may retain historical compatibility fields when permanent regression gates depend on them, but current 2.0 semantics must remain explicit and unambiguous.

## Component changes

Document shared behavior in `COMPONENTS.md`. Do not add a shared component solely because one product needs a specialized local pattern. Application-specific components may remain local while using current Glaze semantics.

## Accessibility changes

Accessibility fallbacks are part of intended design quality. Improvements preserve visible focus, readable contrast, programmatic state, 48px general/56px TV floors and effects-free task completion.

## Stable maintenance boundary

Glaze UI 2.0.x maintenance prioritizes compatibility, deterministic validation, accurate documentation, controlled adoption, accessibility, privacy, authority boundaries and regression resistance over speculative feature expansion. Historical 1.x regressions remain preserved; they are not active consumer targets.

Consumer applications are independently versioned and are never marked migrated merely because Glaze UI changes.

## Commit and review scope

Keep changes focused and understandable. Do not mix unrelated application code, secrets, credentials, generated build artifacts or production configuration into this repository.
