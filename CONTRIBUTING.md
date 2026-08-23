# Contributing to Glaze UI

Glaze UI is the shared GoreeCloud design system. Changes should strengthen consistency, accessibility, privacy, resilience, and visual quality without turning GoreeCloud applications into generic clones.

## Principles

- Preserve the established Glaze UI visual character.
- Prefer semantic tokens over new literal values.
- Keep translucency selective and always provide readable fallbacks.
- Avoid new third-party browser dependencies unless they are clearly justified.
- Maintain keyboard, contrast, forced-colors, reduced-motion, and target-size behavior.
- Keep the reference implementation dependency-free.
- Treat product personality as compatible with conformance.

## Before opening a pull request

Run the Stable source gate locally from the repository root:

```bash
python3 -m py_compile scripts/validate_glaze_ui.py scripts/validate_release_state.py scripts/validate_form_factors.py scripts/validate_consumer_registry.py scripts/validate_typography_contract.py scripts/validate_rendered_reference.py website/build.py website/validate.py integrations/firefox/validate.py
python3 scripts/validate_glaze_ui.py
python3 scripts/validate_release_state.py
python3 scripts/validate_form_factors.py
python3 scripts/validate_typography_contract.py
python3 scripts/validate_consumer_registry.py
python3 integrations/firefox/validate.py
python3 website/validate.py
```

The pull-request workflow is authoritative and checks out the exact PR head before running the permanent Glaze UI CI gate. Do not promote or merge a Stable-maintenance PR until that exact candidate passes the complete workflow.

## Rendered and visual acceptance

For changes that can affect presentation, interaction, accessibility, form-factor behavior, or reference output, also run:

```bash
python3 scripts/validate_rendered_reference.py
```

Review the canonical five-profile acceptance matrix rather than only generic breakpoints:

- Mobile — 390 × 844
- Tablet — 820 × 1180
- Desktop — 1280 × 900
- Wide Desktop — 1600 × 1000
- TV — 1920 × 1080

Review light/dark appearance where applicable, reduced-motion and forced-colors resilience, and the relevant input model. TV changes require directional-focus and far-viewing acceptance. A passing screenshot at one width is not sufficient evidence for a cross-form-factor change.

## Token changes

Compatible token additions normally belong in a minor release. Removing or redefining required semantics may require a major release. Fixes that do not change the public semantic contract may use a patch release.

When adding a token, update the canonical CSS or platform mapping guidance when applicable and extend the validator if the token represents a required contract.

## Component changes

Document new shared component behavior in `COMPONENTS.md`. Do not add a component solely because one application needs a highly specialized UI pattern; application-specific components may remain local while using shared Glaze semantics.

## Accessibility changes

Accessibility fallbacks are part of Glaze UI's intended design quality, not optional alternate styling. Improvements should preserve a polished appearance while maintaining clear focus, readable contrast, semantic state, and predictable interaction.

## Stable maintenance boundary

Glaze UI 1.4.x maintenance prioritizes compatibility, deterministic validation, accurate documentation, controlled adoption, accessibility, privacy, and regression resistance over speculative feature expansion. Consumer applications are independently versioned and are never migrated merely because Glaze UI changes.

## Commit and review scope

Keep changes focused and understandable. Do not mix unrelated application code, secrets, credentials, generated build artifacts, or production configuration into this repository.
