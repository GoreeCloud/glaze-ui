# Glaze UI Interaction States and Input Modality

Status: Glaze UI 1.5 Candidate. Glaze UI 1.4.0 remains Stable.

## Purpose

Glaze UI defines how component state is presented across keyboard, pointer, touch, remote/gamepad, assistive technology, and mixed-input environments. The contract governs presentation and interaction feedback; application business logic and underlying platform truth remain outside Glaze UI authority.

## State model

Interactive components may expose these semantic states where applicable:

- `default` — available and not actively engaged.
- `hover` — pointer proximity preview only; never the sole carrier of required information or action.
- `focus-visible` — keyboard, remote/gamepad, or other non-pointer navigation focus requiring an unmistakable focus indicator.
- `pressed` — transient physical/virtual activation feedback.
- `selected` — persistent choice within a selectable set.
- `expanded` — disclosure/open state, distinct from selected and pressed.
- `disabled` — unavailable for interaction and semantically disabled to assistive technology.
- `read-only` — content may be reviewed/copied but not edited; must remain distinguishable from disabled.
- `loading` — work is in progress; state must be truthful and expose busy semantics when appropriate.
- `invalid` — user input requires correction; explanation must not rely on color alone.
- `success` — confirmed successful state where explicit confirmation is useful; must not be inferred from decorative color alone.

State combinations must remain semantically coherent. For example, loading may coexist with selected or expanded, but disabled must not masquerade as read-only.

## Input modality

Glaze UI supports mixed-input use. Components must not permanently infer modality from viewport size or device category.

- Keyboard: focus-visible treatment is required for navigable controls.
- Pointer: hover may supplement but never replace focus, labels, help, or activation pathways.
- Touch/coarse pointer: no interaction may require hover.
- TV remote/gamepad: directional focus is a primary navigation signal; focused targets must remain visually distinct at viewing distance.
- Assistive technology: semantic HTML/ARIA/native accessibility state is authoritative over purely visual state.

A surface may transition between modalities during the same session without losing operability or state clarity.

## Focus-visible

Focus indication must:

1. remain visible against Solid, Raised, Functional Glass, Clear Glass, Overlay, and media-backed surfaces;
2. avoid relying on color alone when contrast may vary;
3. not be clipped by ordinary component overflow;
4. track the semantic focus target rather than an unrelated parent;
5. remain available under reduced motion, reduced transparency, high contrast, and constrained performance modes.

Pointer click focus may use platform `:focus-visible` heuristics; never globally suppress outlines without an equivalent replacement.

## Hover and pressed

Hover is anticipatory, not authoritative. Pressed state is short-lived activation feedback and must not be confused with selected state. Motion may reinforce these states but the state must remain understandable when motion is reduced.

## Selected and expanded

Selected state represents a persistent chosen item and should map to native or ARIA selection semantics where applicable. Expanded state represents disclosure visibility and should map to `aria-expanded` or equivalent native semantics. Visual treatment must keep these concepts distinct.

## Disabled and read-only

Disabled controls must expose native `disabled` or `aria-disabled="true"` as appropriate. Visual dimming alone is insufficient.

Read-only content must remain legible and navigable where useful. Use native `readonly` or equivalent semantics. Do not apply disabled styling to read-only fields when that would imply the content is unavailable.

When an unavailable action needs explanation, preserve a discoverable explanation path rather than relying on hover over a disabled control.

## Loading and progress

Loading state must expose truthful busy semantics (`aria-busy="true"` or native equivalent) when the affected region is temporarily updating. Determinate progress must reflect actual progress; indeterminate treatment must not imply a fabricated percentage.

Loading presentation should preserve layout dimensions where practical to prevent unnecessary movement. Cancellation or escape behavior belongs to the application workflow and must remain available when the underlying operation supports it.

## Validation and status

Invalid state must pair visual emphasis with semantic invalid state and an accessible explanation. Error, warning, success, and informational status must not depend on color, material, iconography, or motion alone.

## TV and distance interaction

TV/remote navigation uses focus, not hover, as the primary affordance. Focus targets must be large enough for distance viewing, remain inside safe/overscan-aware regions, and preserve predictable directional order. Press/activation feedback must not shift layout or move the target away from focus.

## Accessibility and preference fallbacks

Reduced motion removes nonessential state travel while preserving state distinction. Reduced transparency and constrained-performance modes must preserve focus, selection, validation, loading, and disabled/read-only distinction on stable surfaces. Forced-colors/high-contrast environments may replace decorative state colors; native/system focus and semantic state remain valid.

## Authority boundaries

Glaze UI governs presentation and interaction feedback for semantic state. Application logic determines whether an action is actually available, selected, busy, invalid, successful, or expanded. Privacy Shield, Wardveil Security, Everkeep, and GoreeCloud Mesh remain authoritative for their underlying privacy, security, resilience, and coordination state; Glaze UI must not visually invent those states.

## Candidate boundary

This contract is isolated to Glaze UI 1.5 Candidate. It does not alter 1.4.0 Stable semantics, migrate consumers, or authorize production conformance until explicit promotion.
