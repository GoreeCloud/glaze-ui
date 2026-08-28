# Glaze UI 1.6 Candidate — Semantic Presentation

Status: **Candidate**. Glaze UI 1.5.0 remains the current Stable production target.

## Purpose

Semantic Presentation coordinates three existing Glaze UI foundations that must work together in real interfaces: **symbols, semantic color, and accessibility**. It does not replace the Stable 1.5 iconography or adaptive-color systems. It adds a shared presentation contract so a status remains recognizable when color, motion, transparency, or visual detail is reduced.

## Governing rule

**Meaning survives presentation changes.** A semantic state may use color, symbol form, text, position, border treatment, material, and motion together, but no required meaning may depend on only one of those channels.

## Semantic state families

The Candidate profile standardizes presentation bindings for:

- information;
- success;
- warning;
- danger;
- privacy;
- security;
- protected;
- restricted;
- online;
- offline;
- syncing;
- paused;
- unavailable.

The producer of the underlying state remains authoritative. Glaze UI controls presentation only.

## Symbol-state binding

The full System Icon Registry remains Planned. This Candidate does not claim that registry exists.

For semantic state presentation, implementations must bind each supported state to a recognizable symbol role and a visible label or equivalent accessible name. State symbols follow the Stable iconography rules:

- inactive or available states normally use outlined treatment;
- selected or persistently active states may use filled or glazed treatment;
- warning, danger, privacy, security, restricted, and unavailable states use protected semantic symbol roles rather than application-specific substitutes;
- filled presentation never changes the meaning of the symbol;
- compact presentation may simplify detail but may not remove the identity-defining state cue.

## Non-color companion requirement

Every semantic state requires at least one non-color companion. Accepted companions include:

- a standardized symbol;
- visible state text;
- a distinct border or line style;
- a stable shape treatment;
- a pattern or texture where appropriate;
- explicit position or grouping with an accessible label.

Critical, destructive, privacy, security, and unavailable states should normally use both a symbol and visible text when space permits.

## Semantic color binding

Stable 1.5 semantic color families remain authoritative. Candidate components consume them through semantic roles rather than literal pigments.

Color may communicate hierarchy and attention, but presentation must preserve the state under:

- light appearance;
- dark appearance;
- increased contrast;
- forced colors;
- monochrome or desaturated presentation;
- reduced transparency;
- reduced motion;
- user-selected accent changes.

Application identity and user accent may influence decorative context but may not recolor protected semantic families into ambiguity.

## Explicit accessibility profiles

Operating-system preferences remain primary inputs. Glaze UI 1.6 Candidate additionally defines explicit application-level presentation profiles for environments where users need stronger controls or the platform does not expose a complete preference signal.

Supported profiles are additive and may be combined:

- `enhanced-focus` — stronger focus outline and separation;
- `large-targets` — raises interactive target floors without changing logical order;
- `high-contrast` — strengthens boundaries and suppresses low-value translucency;
- `reduced-transparency` — replaces glass-dependent presentation with stable opaque surfaces;
- `reduced-motion` — removes nonessential motion and spatial scale feedback;
- `monochrome` — removes decorative chroma while preserving semantic meaning through symbols, labels, geometry, and contrast.

Explicit profiles must not override a stronger operating-system accessibility requirement in the opposite direction.

## Enhanced focus

Enhanced focus must remain visually separate from selection. It uses a stronger outline, sufficient offset, and non-color geometry so keyboard and switch users can identify the active interaction target regardless of semantic color.

Focus may not be hidden solely because an element is selected, active, or destructive.

## Large targets

`large-targets` raises the general interactive minimum to 52px for near-view interfaces while retaining the Stable TV minimum of 56px. It may increase control spacing and padding but must not reorder commands or hide information.

## High contrast

High-contrast presentation favors explicit boundaries, solid surfaces, clear text hierarchy, and reduced decorative gradients. Material depth may be simplified, but semantic hierarchy and identity must remain understandable.

## Reduced transparency

Reduced transparency disables background-dependent blur and refraction for Glaze surfaces used by participating Candidate components. Opaque replacement surfaces retain borders, elevation hierarchy, and readable foreground contrast.

## Reduced motion

Reduced-motion presentation removes nonessential transitions, transform feedback, pulsing, parallax, and decorative animation. Required state changes remain immediate and understandable through static presentation.

## Monochrome presentation

Monochrome is an accessibility and robustness profile, not a stylistic grayscale filter. Decorative chroma is suppressed, while semantic differentiation is preserved through icon form, visible labels, border styles, emphasis, position, and programmatic state.

Protected semantic state must not disappear when hue is unavailable.

## Semantic status primitive

The Candidate web layer provides `.glaze-semantic-status-candidate` as a generic labeled status surface. It requires a `data-state` value and should include a visible `.glaze-semantic-status-label-candidate` label. A decorative `.glaze-semantic-symbol-candidate` may accompany the label but does not replace accessible text.

The primitive is intentionally generic. It does not manufacture producer evidence and does not replace specialized Privacy Shield, Wardveil, Everkeep, Mesh, synchronization, or application-specific components.

## Authority boundaries

- Privacy Shield supplies privacy-control truth.
- Wardveil Security supplies security/protection truth.
- Everkeep supplies backup, recovery, preservation, portability, succession, and continuity truth.
- GoreeCloud Mesh supplies coordination/governance truth.
- Application logic supplies workflow, availability, loading, validation, and selection truth.

Glaze UI may change presentation based on supplied state but may not infer a stronger claim from color, icon, emphasis, or material.

## Candidate implementation

The Candidate implementation consists of:

- `tokens/semantic-presentation.candidate.json`;
- `css/glaze.semantic-presentation.candidate.css`;
- `reference/candidate-1.6-semantic-presentation.html`;
- `scripts/validate_semantic_presentation.py`;
- exact-head CI coverage.

## Promotion boundary

Stable promotion requires source validation, representative rendered review in light/dark/high-contrast/forced-colors/monochrome/reduced-transparency/reduced-motion modes, keyboard and visible-focus acceptance, symbol/label ambiguity review, compatibility review, consumer migration planning, and explicit promotion under `STABILITY.md`.
