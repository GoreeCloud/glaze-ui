# Glaze UI

Glaze UI is GoreeCloud's shared visual and interaction design system. **Beauty is a requirement, not a regression risk.** It standardizes reusable semantics, accessibility, resilience, and cross-platform behavior without flattening product personality.

## Design lineage

Glaze UI is informed by **Samsung One UI 8.5**, **Apple Liquid Glass**, and **Google Material 3 Expressive**, reinterpreted through GoreeCloud privacy, identity, accessibility, resilience, and self-hosted requirements. These are references, not templates.

## Glaze UI 1.4 Stable — Form-Factor Evolution

**Glaze UI 1.4.0 is the current Stable canonical baseline.** It preserves the complete 1.3 expressive foundation and promotes Mobile, Tablet, Desktop, and TV to first-class semantic interaction environments.

1.4 adds `FORM_FACTORS.md`, form-factor tokens, `css/glaze.formfactors.css`, a dependency-free four-profile reference, TV far-view/overscan/directional-focus semantics, and expanded rendered acceptance at Mobile 390×844, Tablet 820×1180, Desktop 1280×900, Wide Desktop 1600×1000, and TV 1920×1080.

TV is explicitly **not Wide Desktop**. Form-factor selection uses app window, primary input, viewing distance, platform conventions, posture/resizability, and product task rather than width or device name alone.

## Glaze UI 1.3 compatibility

Glaze UI 1.3.0 remains a supported older Stable release for consumers that have not intentionally migrated. 1.4 is a compatible minor evolution; existing consumers are not automatically upgraded.

## Stability priority

Glaze UI remains stabilization-first. `STABILITY.md` governs compatibility and promotion; `COMPONENT_STATUS.md` governs Stable, Candidate, Experimental, and Planned lifecycle state; `CONSUMERS.md` and `consumers/registry.json` track evidence-backed consumer alignment. A Stable design-system release never substitutes for application-specific adoption, native mapping, or product acceptance.

Speculative intelligence, agent, automation, ambient-computing, voice, and operating-experience concepts remain roadmap-only unless separately implemented, versioned, validated, and promoted.

## Future typography reference

Glaze Sans is **not an active or Planned font-development project**. `GLAZE_SANS.md` preserves the desired future design brief—beautiful, polished, subtly rounded, geometric-humanist, highly readable, accessible, local-first, and distinctly GoreeCloud—without making a custom font part of the current Stable contract. System/platform-native fonts remain the default today.

## Repository layout

- `VERSION` — current Stable semantic version.
- `tokens/glaze.tokens.json` — canonical semantic tokens.
- `FORM_FACTORS.md` — Mobile, Tablet, Desktop, and TV contract.
- `GLAZE_SANS.md` — future-only Glaze Sans visual and quality reference; not an active implementation requirement.
- `css/glaze.css` — core web primitives.
- `css/glaze.controls.css` — form/selection/feedback primitives.
- `css/glaze.expressive.css` — 1.3 expressive layer retained by 1.4.
- `css/glaze.formfactors.css` — 1.4 form-factor primitives.
- `css/glaze.accessibility.css` — resilience and accessibility fallbacks.
- `COMPONENTS.md` — shared component semantics.
- `COMPONENT_STATUS.md` — lifecycle registry.
- `STABILITY.md` — compatibility and promotion contract.
- `CONFORMANCE.md` — version-specific conformance gates.
- `ADOPTION.md` — consumer integration guidance.
- `ACCEPTANCE.md` — Stable acceptance protocol.
- `acceptance/` — version-specific promotion evidence.
- `reference/index.html` and `reference/formfactors.html` — dependency-free references.
- `scripts/validate_glaze_ui.py`, `scripts/validate_form_factors.py`, `scripts/validate_consumer_registry.py`, and `scripts/validate_rendered_reference.py` — fail-closed validation.

## Material hierarchy

Canvas → Solid → Raised → Functional Glass → Overlay. Clear Glass is specialized for controls over visually rich media. Ordinary content defaults to Solid/Raised; glass is selective, not universal.

## Form-factor model

- **Mobile** — near-view, touch/reachability-first, safe-area-aware, task-focused.
- **Tablet** — touch-capable, pane/posture-aware, optionally enhanced by pointer/keyboard/stylus.
- **Desktop** — pointer/keyboard-first, resizable workspace, persistent tools and denser multi-pane patterns where useful.
- **TV** — far-view, landscape-first, overscan-safe, remote/D-pad directional focus, large readable controls, shallow predictable focus groups.

## Validation

```bash
python3 scripts/validate_glaze_ui.py
python3 scripts/validate_form_factors.py
python3 scripts/validate_consumer_registry.py
python3 scripts/validate_rendered_reference.py
```

## Versioning

Glaze UI follows semantic versioning. Patch releases are compatible corrections; minor releases add compatible semantics; major releases may change established contracts. Consumer migration is always controlled and application-specific.

## License

MIT. GoreeCloud branding and product identity remain subject to their applicable project policies.
