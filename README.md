# Glaze UI

Glaze UI is GoreeCloud's shared visual and interaction design system. **Beauty is a requirement, not a regression risk.** It standardizes reusable semantics, accessibility, resilience, privacy, and cross-platform behavior without flattening product personality.

## Design lineage

Glaze UI is informed by **Samsung One UI 8.5**, **Apple Liquid Glass**, and **Google Material 3 Expressive**, reinterpreted through GoreeCloud privacy, identity, accessibility, resilience, and self-hosted requirements. These are references, not templates.

## Glaze UI 1.4 Stable — Form-Factor Evolution

**Glaze UI 1.4.0 is the current Stable canonical baseline.** It preserves the complete 1.3 expressive foundation and promotes Mobile, Tablet, Desktop, and TV to first-class semantic interaction environments.

1.4 adds `FORM_FACTORS.md`, form-factor tokens, `css/glaze.formfactors.css`, a dependency-free five-profile reference, TV far-view/overscan/directional-focus semantics, and expanded rendered acceptance at Mobile 390×844, Tablet 820×1180, Desktop 1280×900, Wide Desktop 1600×1000, and TV 1920×1080.

TV is explicitly **not Wide Desktop**. Form-factor selection uses app window, primary input, viewing distance, platform conventions, posture/resizability, and product task rather than width or device name alone.

## Glaze UI 1.5 Candidate — Adaptive Color and Iconography

Glaze UI 1.5 is an isolated **Candidate** evolution. It does not replace the Stable 1.4 application target until the complete promotion gate is satisfied.

The adaptive-color layer turns the existing semantic color contract into a layered architecture with contextual color propagation, four prominence levels (`subtle`, `standard`, `prominent`, `critical`), protected semantic tonal families, adaptive accent derivation, contextual selection glazing, material/background sampling boundaries, color-motion behavior, and purpose-built accessibility modes. Canonical candidate artifacts are `COLOR_ARCHITECTURE.md`, `tokens/adaptive-colors.json`, `css/glaze.color.css`, and `scripts/validate_adaptive_colors.py`.

The iconography layer formalizes **recognizable identity within a shared visual language** across application, service, system, functional, and semantic icons. It defines application foundation/identity/detail composition, simpler non-launchable service treatment, standardized functional and semantic glyph behavior, badge anchors and priority, presentation/standard/compact/micro optical sizes, adaptive-color boundaries, reduced-motion behavior, accessibility invariants, and third-party identity preservation. Canonical candidate artifacts are `ICONOGRAPHY.md`, `tokens/iconography.json`, and `scripts/validate_iconography.py`.

Application identity, wallpaper, user accent, and content context may influence decorative color while success, warning, danger, privacy, security, protection, restriction, connectivity, synchronization, and availability semantics remain protected. Privacy Shield and Wardveil Security remain authoritative for privacy/security truth; Glaze UI presents supplied state and never invents or upgrades evidence.

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
- `tokens/glaze.tokens.json` — canonical Stable semantic tokens.
- `tokens/semantic-colors.json` — Stable semantic color meaning contract.
- `COLOR.md` — Stable semantic color contract documentation.
- `COLOR_ARCHITECTURE.md` — 1.5 Candidate adaptive color architecture.
- `tokens/adaptive-colors.json` — 1.5 Candidate color families, prominence, materials, authority, and accessibility contract.
- `css/glaze.color.css` — 1.5 Candidate adaptive color web primitives.
- `ICONOGRAPHY.md` — 1.5 Candidate application, service, system, functional, semantic, badge, optical-size, motion, and accessibility icon contract.
- `tokens/iconography.json` — machine-readable 1.5 Candidate iconography contract.
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
- `scripts/validate_glaze_ui.py`, `scripts/validate_release_state.py`, `scripts/validate_form_factors.py`, `scripts/validate_consumer_registry.py`, `scripts/validate_rendered_reference.py`, `scripts/validate_adaptive_colors.py`, and `scripts/validate_iconography.py` — fail-closed validation.

## Material hierarchy

Canvas → Solid → Raised → Functional Glass → Overlay. Clear Glass is specialized for controls over visually rich media. Ordinary content defaults to Solid/Raised; glass is selective, not universal.

The 1.5 Candidate additionally coordinates material luminosity, tonal separation, bounded background sampling, selection glazing, icon material depth, and semantic foreground protection without turning glass into a universal content treatment.

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
python3 scripts/validate_form_factors.py
python3 scripts/validate_typography_contract.py
python3 scripts/validate_consumer_registry.py
python3 integrations/firefox/validate.py
python3 website/validate.py
python3 scripts/validate_rendered_reference.py
```

For the isolated 1.5 Candidate, additionally run:

```bash
python3 scripts/validate_adaptive_colors.py
python3 scripts/validate_iconography.py
```

The pull-request workflow remains authoritative because it checks out and validates the exact candidate revision. Do not treat an earlier local run or a partial validation subset as equivalent to the final CI result.

## Versioning

Glaze UI follows semantic versioning. Patch releases are compatible corrections; minor releases add compatible semantics; major releases may change established contracts. Consumer migration is controlled and application-specific, and every new Stable baseline becomes mandatory for current GoreeCloud-controlled user-facing applications.

## License

MIT. GoreeCloud branding and product identity remain subject to their applicable project policies.