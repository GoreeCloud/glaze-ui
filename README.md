# Glaze UI

Glaze UI is GoreeCloud's shared visual and interaction design system. **Beauty is a requirement, not a regression risk.** It standardizes reusable semantics, accessibility, resilience, privacy, and cross-platform behavior without flattening product personality.

## Design lineage

Glaze UI is informed by **Samsung One UI 8.5**, **Apple Liquid Glass**, and **Google Material 3 Expressive**, reinterpreted through GoreeCloud privacy, identity, accessibility, resilience, and self-hosted requirements. These are references, not templates.

## Full-spectrum enforcement

Glaze UI is mandatory identity architecture, not a theme or finishing layer. If GoreeCloud controls a user-visible or interaction-facing decision, the current Stable Glaze UI contract governs it unless Glaze UI explicitly delegates implementation while preserving the same semantics, accessibility, identity, and integration requirements. The enforcement scope is deliberately non-exhaustive: an unnamed component, technology, form factor, state, or future interaction is not exempt.

`ENFORCEMENT.md` and `tokens/enforcement.json` define this fail-closed governance contract. Consumers may not establish competing local design systems, arbitrary semantic vocabularies, private icon conventions, incompatible component languages, or ad hoc token systems that fragment GoreeCloud family identity. New presentation capabilities that exceed current Stable semantics must extend and promote Glaze UI before becoming production dependencies.

## Glaze UI 1.4 Historical Stable — Form-Factor Evolution

**Glaze UI 1.4.0 is the immediately preceding historical Stable baseline.** It preserves the complete 1.3 expressive foundation and promotes Mobile, Tablet, Desktop, and TV to first-class semantic interaction environments.

1.4 adds `FORM_FACTORS.md`, form-factor tokens, `css/glaze.formfactors.css`, a dependency-free five-profile reference, TV far-view/overscan/directional-focus semantics, and expanded rendered acceptance at Mobile 390×844, Tablet 820×1180, Desktop 1280×900, Wide Desktop 1600×1000, and TV 1920×1080.

TV is explicitly **not Wide Desktop**. Form-factor selection uses app window, primary input, viewing distance, platform conventions, posture/resizability, and product task rather than width or device name alone.

## Glaze UI 1.5 Historical Stable — Adaptive Color, Iconography, Motion, Materials, Layout, and State

**Glaze UI 1.5.0 is the immediately preceding historical Stable baseline.** It retains the complete 1.4 Mobile, Tablet, Desktop, Wide Desktop, and TV form-factor contract and promotes the validated 1.5 adaptive-color, iconography/construction/identity, motion/interaction, material/depth, layout/spacing/density, and semantic state/input-modality systems.

Canonical 1.5 Stable artifacts include `COLOR_ARCHITECTURE.md`, `ICONOGRAPHY.md`, `ICON_CONSTRUCTION.md`, `MOTION.md`, `MATERIALS.md`, `LAYOUT.md`, `STATES.md`, their machine-readable token files, reusable CSS layers, fail-closed validators, and the rendered 1.5 reference/acceptance harness. The exact Candidate evidence remains preserved under `acceptance/1.5-candidate.md`; Stable promotion evidence is recorded under `acceptance/1.5.0.md`.

Application identity, wallpaper, user accent, and content context may influence decorative presentation, but semantic truth remains producer-authoritative. Privacy Shield is authoritative for privacy-control state; Wardveil Security for security/protection state; Everkeep for resilience, backup, recovery, preservation, portability, succession, and digital legacy; GoreeCloud Mesh for coordination/governance; and application logic for availability, selection, busy, validation, and workflow truth. Glaze UI presents supplied state and never invents evidence.

Wear OS remains outside the implemented 1.5 interaction contract. This is **not an exception**: a GoreeCloud smartwatch or wearable application remains production-blocked until an applicable Stable wearable Glaze UI contract is implemented, validated, and promoted.

## Glaze UI 1.6 Stable — Evidence Presentation and Adaptive Workspace

**Glaze UI 1.6.0 is the current Stable canonical baseline.** It retains every validated 1.5 Stable subsystem and promotes the evidence-presentation/authority-surface and Adaptive Workspace/Navigation contracts that passed the complete 1.6 Candidate source and browser-rendered acceptance stack.

The 1.6 Stable evidence system formalizes evidence presentation and authority surfaces: producer-authoritative state, provenance and freshness, Mesh transport context, accessible evidence disclosure, and fail-closed unavailable/invalid handling without inventing security, privacy, recovery, or coordination truth.

The 1.6 Stable Adaptive Workspace adds a reusable semantic shell for window/title regions, navigation, toolbars, primary content, inspectors, status regions, overlays, density, input-aware target floors, and form-factor transformation. Desktop may use persistent resizable navigation and inspectors; Tablet may collapse or overlay them; Mobile may transform them into drawers/sheets; TV retains directional-focus and far-view constraints. Adaptation preserves semantic order, focus order, current destination, action state, and platform-authoritative truth.

The promoted implementation is defined by `WORKSPACE_NAVIGATION.md`, `tokens/workspace-navigation.candidate.json`, `css/glaze.workspace.candidate.css`, `reference/candidate-1.6-workspace.html`, and `scripts/validate_workspace_navigation.py`. Stable regression protection remains subject to exact-head CI, rendered/native acceptance where applicable, accessibility/resilience review, compatibility/migration review, and `STABILITY.md`.

## Mandatory current-Stable consumer target

The current Stable consumer target is **1.6.0**, as recorded by `consumers/registry.json`. It is the only Glaze UI version that may satisfy current GoreeCloud application conformance or production-readiness requirements.

Historical Stable releases 1.0.0 through 1.5.0 remain preserved for audit, migration, rollback, and release history. They are not supported active application targets and may not be used to satisfy current production acceptance. Existing consumers are never grandfathered onto superseded Glaze UI versions.

When a newer Stable release is promoted, all GoreeCloud-controlled user-facing consumers covered by that Stable contract become required to migrate to that current Stable release. Migration remains controlled and application-specific, but migration itself is mandatory. There are no application-level production exceptions within the supported Stable scope.

The current Stable scope covers web, desktop, mobile, tablet, TV, progressive web, dashboard, administrative, maintained-fork, and other GoreeCloud-controlled user-facing interfaces for which an applicable Stable Glaze UI contract exists. Smartwatch/Wearable remains outside the implemented 1.6 Stable interaction scope and is therefore production-blocked until a later Stable wearable contract is promoted.

## Stability priority

Glaze UI remains stabilization-first. `STABILITY.md` governs compatibility, promotion, and mandatory consumer migration; `COMPONENT_STATUS.md` governs Stable, Candidate, Experimental, and Planned lifecycle state; `CONSUMERS.md` and `consumers/registry.json` track evidence-backed consumer alignment and migration-required state. A Stable design-system release never substitutes for application-specific adoption, native mapping, or product acceptance.

Release-state consistency is a permanent CI contract. `scripts/validate_release_state.py` binds `VERSION`, token metadata, the README Stable declaration, current-Stable consumer requirement, stability/lifecycle records, and the changelog so a future release cannot silently leave contradictory current-version or consumer-target claims behind.

Speculative intelligence, agent, automation, ambient-computing, voice, operating-experience, and wearable-expansion concepts remain roadmap-only unless separately implemented, versioned, validated, and promoted.

## Future Wear OS upgrade

Wear OS is a deferred Glaze UI expansion target. The existing `reference/native/wear-os/` implementation and `.github/workflows/wear-os-emulator.yml` are preserved as development/reference material, but the emulator workflow is manual-only and non-gating. A future Glaze UI release must define the wearable interaction model, form-factor semantics, accessibility behavior, native mapping, rendered acceptance, emulator/real-device evidence, compatibility, and promotion rules before Wear OS becomes a supported production-conformance target.

## Future typography reference

Glaze Sans is **not an active or Planned font-development project**. `GLAZE_SANS.md` preserves the desired future design brief—beautiful, polished, subtly rounded, geometric-humanist, highly readable, accessible, local-first, and distinctly GoreeCloud—without making a custom font part of the current Stable contract. System/platform-native fonts remain the default today.

## Repository layout

- `VERSION` — current Stable semantic version.
- `tokens/glaze.tokens.json` — canonical Stable semantic tokens.
- `tokens/semantic-colors.json` — Stable semantic color meaning contract.
- `COLOR.md` — Stable semantic color contract documentation.
- `COLOR_ARCHITECTURE.md` — 1.5 Stable adaptive color architecture.
- `tokens/adaptive-colors.json` — 1.5 Stable color families, prominence, materials, authority, and accessibility contract.
- `css/glaze.color.css` — 1.5 Stable adaptive color web primitives.
- `ICONOGRAPHY.md` — 1.5 Stable application, service, system, functional, semantic, badge, optical-size, motion, and accessibility icon contract.
- `tokens/iconography.json` — machine-readable 1.5 Stable iconography contract.
- `MOTION.md` — 1.5 Stable motion and interaction contract.
- `tokens/motion.json` — semantic motion durations, easing, distance, scale, accessibility, and authority roles.
- `css/glaze.motion.css` — reusable 1.5 Stable web motion primitives.
- `MATERIALS.md` — 1.5 Stable material, depth, translucency, backdrop, elevation, and accessibility contract.
- `tokens/materials.json` — machine-readable 1.5 Stable material and depth roles.
- `css/glaze.materials.css` — reusable 1.5 Stable material primitives and fallbacks.
- `EVIDENCE_PRESENTATION.md` and its token/profile contracts — Glaze UI 1.6 Stable evidence and authority presentation.
- `WORKSPACE_NAVIGATION.md` — Glaze UI 1.6 Stable adaptive workspace and navigation contract.
- `tokens/workspace-navigation.candidate.json` — machine-readable 1.6 Stable workspace anatomy, sizing, density, targets, adaptation, accessibility, and authority rules.
- `css/glaze.workspace.candidate.css` — reusable 1.6 Stable workspace shell primitives and responsive/accessibility fallbacks.
- `reference/candidate-1.6-workspace.html` — dependency-free 1.6 Stable workspace regression surface.
- `scripts/validate_workspace_navigation.py` — fail-closed 1.6 Stable workspace validator.
- `ENFORCEMENT.md` — full-spectrum, non-exhaustive, fail-closed Glaze UI governance.
- `tokens/enforcement.json` — machine-readable enforcement domains, authorities, and blocking gates.
- `FORM_FACTORS.md` — Mobile, Tablet, Desktop, and TV contract.
- `reference/native/wear-os/` — deferred wearable reference implementation; not part of current Stable or 1.6 acceptance.
- `.github/workflows/wear-os-emulator.yml` — manual-only deferred Wear OS development validation.
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
- `reference/index.html` and `reference/formfactors.html` — dependency-free Stable references.
- `scripts/validate_glaze_ui.py`, `scripts/validate_release_state.py`, `scripts/validate_enforcement.py`, `scripts/validate_form_factors.py`, `scripts/validate_consumer_registry.py`, `scripts/validate_rendered_reference.py`, `scripts/validate_adaptive_colors.py`, `scripts/validate_iconography.py`, `scripts/validate_motion.py`, `scripts/validate_materials.py`, `scripts/validate_evidence_presentation.py`, and `scripts/validate_workspace_navigation.py` — fail-closed validation.

## Material hierarchy

Canvas → Solid → Raised → Functional Glass → Overlay. Clear Glass is specialized for controls over visually rich media. Ordinary content defaults to Solid/Raised; glass is selective, not universal.

The 1.5 Stable coordinates material luminosity, tonal separation, bounded background sampling, selection glazing, icon material depth, semantic foreground protection, reduced-transparency behavior, unsupported-backdrop fallback, and performance-aware degradation without turning glass into a universal content treatment.

## Form-factor model

- **Mobile** — near-view, touch/reachability-first, safe-area-aware, task-focused.
- **Tablet** — touch-capable, pane/posture-aware, optionally enhanced by pointer/keyboard/stylus.
- **Desktop** — pointer/keyboard-first, resizable workspace, persistent tools and denser multi-pane patterns where useful.
- **TV** — far-view, landscape-first, overscan-safe, remote/D-pad directional focus, large readable controls, shallow predictable focus groups.
- **Smartwatch/Wearable** — deferred to a later Glaze UI upgrade; not a current Stable or 1.5 Stable production-conformance target.

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

For the Glaze UI 1.5 Stable subsystem contracts, additionally run:

```bash
python3 scripts/validate_adaptive_colors.py
python3 scripts/validate_iconography.py
python3 scripts/validate_motion.py
python3 scripts/validate_materials.py
python3 scripts/validate_layout.py
python3 scripts/validate_states.py
```

For Glaze UI 1.6 Stable systems, run:

```bash
python3 scripts/validate_evidence_presentation.py
python3 scripts/validate_workspace_navigation.py
node --test tests/mesh-evidence-consumer.test.mjs tests/mesh-evidence-refresh-response.test.mjs
```

The promoted 1.5 subsystem validators remain permanent Stable regression gates. Glaze UI 1.6 additionally requires its evidence-presentation and Adaptive Workspace source/rendered validators. Future Stable promotion still requires applicable rendered/native evidence, accessibility/resilience review, compatibility and migration review, release-state synchronization, and exact-final-revision CI defined by `STABILITY.md`.

Wear OS emulator validation is manual development/reference validation only and is intentionally excluded from current Stable and 1.6 promotion gates.

The pull-request workflow remains authoritative for the active Stable and Candidate checks because it validates the exact candidate revision. Do not treat an earlier local run or a partial validation subset as equivalent to the final CI result.

## Versioning

Glaze UI follows semantic versioning. Patch releases are compatible corrections; minor releases add compatible semantics; major releases may change established contracts. Consumer migration is controlled and application-specific, and every new Stable baseline becomes mandatory for current GoreeCloud-controlled user-facing applications within that release's supported scope.

## License

MIT. GoreeCloud branding and product identity remain subject to their applicable project policies.