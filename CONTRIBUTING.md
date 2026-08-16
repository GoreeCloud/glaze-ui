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

Run:

```bash
python3 scripts/validate_glaze_ui.py
```

For visual changes, also review `reference/index.html` at Compact and Expanded widths in both light and dark appearances.

## Token changes

Compatible token additions normally belong in a minor release. Removing or redefining required semantics may require a major release. Fixes that do not change the public semantic contract may use a patch release.

When adding a token, update the canonical CSS or platform mapping guidance when applicable and extend the validator if the token represents a required contract.

## Component changes

Document new shared component behavior in `COMPONENTS.md`. Do not add a component solely because one application needs a highly specialized UI pattern; application-specific components may remain local while using shared Glaze semantics.

## Accessibility changes

Accessibility fallbacks are part of Glaze UI's intended design quality, not optional alternate styling. Improvements should preserve a polished appearance while maintaining clear focus, readable contrast, semantic state, and predictable interaction.

## Commit and review scope

Keep changes focused and understandable. Do not mix unrelated application code, secrets, credentials, generated build artifacts, or production configuration into this repository.
