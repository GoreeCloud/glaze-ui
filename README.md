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

## Glaze UI 1.5 Candidate — Adaptive Color, Iconography, Motion, and Materials

Glaze UI 1.5 is an isolated **Candidate** evolution. It does not replace the Stable 1.4 application target until the complete promotion gate is satisfied.

The adaptive-color layer turns the existing semantic color contract into a layered architecture with contextual color propagation, four prominence levels (`subtle`, `standard`, `prominent`, `critical`), protected semantic tonal families, adaptive accent derivation, contextual selection glazing, material/background sampling boundaries, color-motion behavior, and purpose-built accessibility modes. Canonical candidate artifacts are `COLOR_ARCHITECTURE.md`, `tokens/adaptive-colors.json`, `css/glaze.color.css`, and `scripts/validate_adaptive_colors.py`.

The iconography layer formalizes **recognizable identity within a shared visual language** across application, service, system, functional, and semantic icons. It defines application foundation/identity/detail composition, simpler service treatment, standardized functional and semantic glyph behavior, deterministic badge anchors and compact priority, presentation/standard/compact/micro optical sizes, adaptive-color boundaries, reduced-motion behavior, accessibility invariants, and third-party identity preservation. Canonical candidate artifacts are `ICONOGRAPHY.md`, `tokens/iconography.json`, and `scripts/validate_iconography.py`.

The motion and interaction layer defines purpose-driven, interruptible animation; semantic duration/easing roles; gesture continuity; focus, press, hover, navigation, progress, and state-transition behavior; reduced-motion substitutions; and truth-preserving authority boundaries. Canonical candidate artifacts are `MOTION.md`, `tokens/motion.json`, `css/glaze.motion.css`, and `scripts/validate_motion.py`.

The material and depth layer turns Canvas, Solid, Raised, Functional Glass, Clear Glass, Overlay, semantic depth, shadow, translucency, and backdrop behavior into a single governed contract. It requires bounded glass, stable Solid/Raised fallbacks, reduced-transparency support, performance-aware degradation, legibility over variable backdrops, and explicit authority boundaries. Canonical candidate artifacts are `MATERIALS.md`, `tokens/materials.json`, `css/glaze.materials.css`, and `scripts/validate_materials.py`.

Application identity, wallpaper, user accent, and content context may influence decorative color while success, warning, danger, privacy, security, protection, restriction, connectivity, synchronization, availability, backup, recovery, preservation, and coordination semantics remain protected. **Privacy Shield** is authoritative for privacy-control state and privacy claims; **Wardveil Security** for security and protection state; **Everkeep** for resilience, backup, recovery, preservation, portability, succession, and digital-legacy state; and **GoreeCloud Mesh** for cross-product coordination and governance state. Glaze UI presents supplied state and never invents or upgrades evidence.

Wear OS is explicitly **outside the Glaze UI 1.5 scope**. Existing Wear OS reference code and manual emulator validation are preserved for future work, but wearable support is not a 1.5 merge gate, Candidate-promotion gate, Stable-promotion gate, or current production-conformance requirement. A later Glaze UI upgrade will define, validate, and promote the wearable contract separately.

## Mandatory current-Stable consumer target

The current Stable consumer target is **1.4.0**, as recorded by `consumers/registry.json`. It is the only Glaze UI version that may satisfy current GoreeCloud application conformance or production-readiness requirements.

Historical Stable releases 1.0.0 through 1.3.0 remain preserved for audit, migration, rollback, and release history. They are not supported active application targets and may not be used to satisfy current production acceptance. Existing consumers are never grandfathered onto superseded Glaze UI versions.

When a newer Stable release is promoted, all GoreeCloud-controlled user-facing consumers covered by that Stable contract become required to migrate to that current Stable release. Migration remains controlled and application-specific, but migration itself is mandatory. There are no application-level production exceptions within the supported Stable scope.

The current Stable scope covers web, desktop, mobile, tablet, TV, progressive web, dashboard, administrative, maintained-fork, and other GoreeCloud-controlled user-facing interfaces for which an applicable Stable Glaze UI contract exists. Smartwatch/Wearable support is deferred to a later Glaze UI upgrade and is not part of the current Stable or 1.5 Candidate acceptance scope.

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
- `COLOR_ARCHITECTURE.md` — 1.5 Candidate adaptive color architecture.
- `tokens/adaptive-colors.json` — 1.5 Candidate color families, prominence, materials, authority, and accessibility contract.
- `css/glaze.color.css` — 1.5 Candidate adaptive color web primitives.
- `ICONOGRAPHY.md` — 1.5 Candidate application, service, system, functional, semantic, badge, optical-size, motion, and accessibility icon contract.
- `tokens/iconography.json` — machine-readable 1.5 Candidate iconography contract.
- `MOTION.md` — 1.5 Candidate motion and interaction contract.
- `tokens/motion.json` — semantic motion durations, easing, distance, scale, accessibility, and authority roles.
- `css/glaze.motion.css` — reusable 1.5 Candidate web motion primitives.
- `MATERIALS.md` — 1.5 Candidate material, depth, translucency, backdrop, elevation, and accessibility contract.
- `tokens/materials.json` — machine-readable 1.5 Candidate material and depth roles.
- `css/glaze.materials.css` — reusable 1.5 Candidate material primitives and fallbacks.
- `ENFORCEMENT.md` — full-spectrum, non-exhaustive, fail-closed Glaze UI governance.
- `tokens/enforcement.json` — machine-readable enforcement domains, authorities, and blocking gates.
- `FORM_FACTORS.md` — Mobile, Tablet, Desktop, and TV contract.
- `reference/native/wear-os/` — deferred wearable reference implementation; not part of current Stable or 1.5 acceptance.
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
- `reference/index.html` and `reference/formfactors.html` — dependency-free references.
- `scripts/validate_glaze_ui.py`, `scripts/validate_release_state.py`, `scripts/validate_enforcement.py`, `scripts/validate_form_factors.py`, `scripts/validate_consumer_registry.py`, `scripts/validate_rendered_reference.py`, `scripts/validate_adaptive_colors.py`, `scripts/validate_iconography.py`, `scripts/validate_motion.py`, and `scripts/validate_materials.py` — fail-closed validation.

## Material hierarchy

Canvas → Solid → Raised → Functional Glass → Overlay. Clear Glass is specialized for controls over visually rich media. Ordinary content defaults to Solid/Raised; glass is selective, not universal.

The 1.5 Candidate coordinates material luminosity, tonal separation, bounded background sampling, selection glazing, icon material depth, semantic foreground protection, reduced-transparency behavior, unsupported-backdrop fallback, and performance-aware degradation without turning glass into a universal content treatment.

## Form-factor model

- **Mobile** — near-view, touch/reachability-first, safe-area-aware, task-focused.
- **Tablet** — touch-capable, pane/posture-aware, optionally enhanced by pointer/keyboard/stylus.
- **Desktop** — pointer/keyboard-first, resizable workspace, persistent tools and denser multi-pane patterns where useful.
- **TV** — far-view, landscape-first, overscan-safe, remote/D-pad directional focus, large readable controls, shallow predictable focus groups.
- **Smartwatch/Wearable** — deferred to a later Glaze UI upgrade; not a current Stable or 1.5 Candidate production-conformance target.

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

For the isolated 1.5 Candidate, additionally run:

```bash
python3 scripts/validate_adaptive_colors.py
python3 scripts/validate_iconography.py
python3 scripts/validate_motion.py
python3 scripts/validate_materials.py
```

Iconography source validation currently proves contract/schema consistency. Stable promotion also requires representative rendered artwork and optical-size acceptance; the validator does not substitute for that visual evidence.

Wear OS emulator validation is manual development/reference validation only and is intentionally excluded from current Stable and 1.5 promotion gates.

The pull-request workflow remains authoritative for the active Stable and Candidate checks because it validates the exact candidate revision. Do not treat an earlier local run or a partial validation subset as equivalent to the final CI result.

## Versioning

Glaze UI follows semantic versioning. Patch releases are compatible corrections; minor releases add compatible semantics; major releases may change established contracts. Consumer migration is controlled and application-specific, and every new Stable baseline becomes mandatory for current GoreeCloud-controlled user-facing applications within that release's supported scope.

## License

MIT. GoreeCloud branding and product identity remain subject to their applicable project policies.