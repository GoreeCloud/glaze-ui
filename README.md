# Glaze UI

Glaze UI is GoreeCloud's shared visual and interaction design system. **Beauty is a requirement, not a regression risk.** It standardizes reusable semantics, accessibility, resilience, privacy, and cross-platform behavior without flattening product personality.

## Design lineage

Glaze UI is informed by **Samsung One UI 8.5**, **Apple Liquid Glass**, and **Google Material 3 Expressive**, reinterpreted through GoreeCloud privacy, identity, accessibility, resilience, and self-hosted requirements. These are references, not templates.

## Full-spectrum enforcement

Glaze UI is mandatory identity architecture, not a theme or finishing layer. If GoreeCloud controls a user-visible or interaction-facing decision, the current Stable Glaze UI contract governs it unless Glaze UI explicitly delegates implementation while preserving the same semantics, accessibility, identity, and integration requirements. The enforcement scope is deliberately non-exhaustive: an unnamed component, technology, form factor, state, or future interaction is not exempt.

`ENFORCEMENT.md` and `tokens/enforcement.json` define this fail-closed governance contract. Consumers may not establish competing local design systems, arbitrary semantic vocabularies, private icon conventions, incompatible component languages, or ad hoc token systems that fragment GoreeCloud family identity. New presentation capabilities that exceed current Stable semantics must extend and promote Glaze UI before becoming production dependencies.

## Glaze UI 1.4 Stable — Form-Factor Evolution

**Glaze UI 1.4.0 is the current Stable canonical baseline.** It preserves the complete 1.3 expressive foundation and promotes Mobile, Tablet, Desktop, and TV to first-class semantic interaction environments.

1.4 adds `FORM_FACTORS.md`, form-factor tokens, `css/glaze.formfactors.css`, a dependency-free five-profile reference, TV far-view/overscan/directional-focus semantics, and expanded rendered acceptance at Mobile 390×844, Tablet 820×1180, Desktop 1280×900, Wide Desktop 1600×1000, and TV 1920×1080.

TV is explicitly **not Wide Desktop**. Form-factor selection uses app window, primary input, viewing distance, platform conventions, posture/resizability, and product task rather than width or device name alone.

## Mandatory current-Stable consumer target

The current Stable consumer target is **1.4.0**, as recorded by `consumers/registry.json`. It is the only Glaze UI version that may satisfy current GoreeCloud application conformance or production-readiness requirements.

Historical Stable releases 1.0.0 through 1.3.0 remain preserved for audit, migration, rollback, and release history. They are not supported active application targets and may not be used to satisfy current production acceptance. Existing consumers are never grandfathered onto superseded Glaze UI versions.

When a newer Stable release is promoted, all GoreeCloud-controlled user-facing consumers become required to migrate to that current Stable release. Migration remains controlled and application-specific, but migration itself is mandatory. There are no application-level production exceptions.

This requirement covers web, desktop, mobile, tablet, TV, smartwatch/wearable, progressive web, dashboard, administrative, maintained-fork, and other GoreeCloud-controlled user-facing interfaces. If a platform lacks an applicable current Stable Glaze UI contract, the application is production-blocked until Glaze UI is extended, validated, and promoted with that Stable contract.

## Stability priority

Glaze UI remains stabilization-first. `STABILITY.md` governs compatibility, promotion, and mandatory consumer migration; `COMPONENT_STATUS.md` governs Stable, Candidate, Experimental, and Planned lifecycle state; `CONSUMERS.md` and `consumers/registry.json` track evidence-backed consumer alignment and migration-required state. A Stable design-system release never substitutes for application-specific adoption, native mapping, or product acceptance.

Release-state consistency is a permanent CI contract. `scripts/validate_release_state.py` binds `VERSION`, token metadata, the README Stable declaration, current-Stable consumer requirement, stability/lifecycle records, and the changelog so a future release cannot silently leave contradictory current-version or consumer-target claims behind.

Speculative intelligence, agent, automation, ambient-computing, voice, and operating-experience concepts remain roadmap-only unless separately implemented, versioned, validated, and promoted.

## Future typography reference

Glaze Sans is **not an active or Planned font-development project**. `GLAZE_SANS.md` preserves the desired future design brief—beautiful, polished, subtly rounded, geometric-humanist, highly readable, accessible, local-first, and distinctly GoreeCloud—without making a custom font part of the current Stable contract. System/platform-native fonts remain the default today.

## Repository layout

- `VERSION` — current Stable semantic version.
- `tokens/glaze.tokens.json` — canonical semantic tokens.
- `ENFORCEMENT.md` — full-spectrum, non-exhaustive, fail-closed Glaze UI governance.
- `tokens/enforcement.json` — machine-readable enforcement domains, authorities, and blocking gates.
- `FORM_FACTORS.md` — Mobile, Tablet, Desktop, and TV contract.
- `GLAZE_SANS.md` — future-only Glaze Sans visual and quality reference; not an active implementation requirement.
- `css/glaze.css` — core web primitives.
- `css/glaze.controls.css` — form/selection/feedback primitives.
- `css/glaze.expressive.css` — 1.3 expressive layer retained by 1.4.
- `css/glaze.formfactors.css` — 1.4 form-factor primitives.
- `css/glaze.accessibility.css` — resilience and accessibility fallbacks.
- `COMPONENTS.md` — shared component semantics.
- `COMPONENT_STATUS.md` — lifecycle registry.
- `STABILITY.md` — compatibility, promotion, and current-Stable consumer contract.
- `CONFORMANCE.md` — current-Stable conformance gates.
- `ADOPTION.md` — consumer integration guidance.
- `ACCEPTANCE.md` — Stable acceptance protocol.
- `acceptance/` — version-specific design-system promotion evidence.
- `reference/index.html` and `reference/formfactors.html` — dependency-free references.
- `scripts/validate_glaze_ui.py`, `scripts/validate_release_state.py`, `scripts/validate_enforcement.py`, `scripts/validate_form_factors.py`, `scripts/validate_consumer_registry.py`, and `scripts/validate_rendered_reference.py` — fail-closed validation.

## Material hierarchy

Canvas → Solid → Raised → Functional Glass → Overlay. Clear Glass is specialized for controls over visually rich media. Ordinary content defaults to Solid/Raised; glass is selective, not universal.

## Form-factor model

- **Mobile** — near-view, touch/reachability-first, safe-area-aware, task-focused.
- **Tablet** — touch-capable, pane/posture-aware, optionally enhanced by pointer/keyboard/stylus.
- **Desktop** — pointer/keyboard-first, resizable workspace, persistent tools and denser multi-pane patterns where useful.
- **TV** — far-view, landscape-first, overscan-safe, remote/D-pad directional focus, large readable controls, shallow predictable focus groups.
- **Smartwatch/Wearable** — mandatory current-Stable Glaze UI use; production requires an applicable Stable wearable contract and application-specific native/real-device acceptance.

## Validation

Run the complete Stable source and integration gate from the repository root:

```bash
python3 scripts/validate_glaze_ui.py
python3 scripts/validate_release_state.py
python3 scripts/validate_enforcement.py
python3 scripts/validate_form_factors.py
python3 scripts/validate_typography_contract.py
python3 scripts/validate_consumer_registry.py
python3 integrations/firefox/validate.py
python3 website/validate.py
python3 scripts/validate_rendered_reference.py
```

The pull-request workflow remains authoritative because it checks out and validates the exact candidate revision. Do not treat an earlier local run or a partial validation subset as equivalent to the final CI result.

## Versioning

Glaze UI follows semantic versioning. Patch releases are compatible corrections; minor releases add compatible semantics; major releases may change established contracts. Consumer migration is controlled and application-specific, and every new Stable baseline becomes mandatory for current GoreeCloud-controlled user-facing applications.

## License

MIT. GoreeCloud branding and product identity remain subject to their applicable project policies.
