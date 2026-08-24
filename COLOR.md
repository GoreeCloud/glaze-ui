# Glaze UI Semantic Color Contract

Color coding in Glaze UI is important because color serves as a functional visual language across the operating system and application ecosystem. It helps users recognize actions, states, hierarchy, security conditions, navigation, and system feedback without relying solely on text.

## Governing principle

Glaze UI uses color semantically, not decoratively. The same semantic meaning must be presented consistently across GoreeCloud surfaces regardless of application identity, theme, form factor, or platform.

Color complements typography, icons, shape, spacing, elevation, and motion. Material information must never be communicated by color alone.

## Core semantic roles

The canonical semantic roles are:

- `accent` — primary interactive emphasis that is not itself a status or warning;
- `surface` — base application or system surface;
- `selected` — currently selected item, destination, or control state;
- `focus` — keyboard, accessibility, or explicit input focus;
- `success` — successful completion or healthy positive outcome;
- `information` — neutral informational state requiring user awareness but not warning;
- `warning` — caution, elevated attention, or possible intervention;
- `danger` — error, destructive action, critical failure, or high-severity condition;
- `protected` — current, positively evidenced protection state;
- `restricted` — access is constrained, denied, policy-limited, or intentionally unavailable to the current actor;
- `online` — reachable, connected, or currently available network/service state;
- `offline` — disconnected or intentionally offline state;
- `syncing` — active synchronization or reconciliation work is in progress;
- `unavailable` — capability or state cannot currently be provided, verified, or reached.

These names define meaning rather than fixed pigments. Their rendered colors may adapt for light, dark, high-contrast, grayscale, color-vision accommodation, display characteristics, and future theme systems while preserving the semantic role.

## Accessibility requirements

Every material semantic state must have a non-color companion. Depending on context this may be a label, icon, shape, pattern, text treatment, position, status description, or another programmatically exposed indicator.

Glaze UI consumers must preserve distinguishability in:

- light appearance;
- dark appearance;
- high-contrast modes;
- grayscale or desaturated presentation;
- common color-vision-deficiency conditions;
- user-customized themes;
- reduced-transparency or reduced-effects modes where applicable.

A consumer fails conformance if loss or alteration of color alone removes the user's ability to understand a material state.

## Branding and semantic separation

Application identity colors are not semantic status colors. Branding must not redefine the meaning of success, information, warning, danger, protected, restricted, online, offline, syncing, unavailable, selection, or focus.

For example, an application whose identity color is red must not cause ordinary controls or accents to resemble destructive actions, errors, or critical warnings. Where an identity color conflicts with a system semantic role, the system semantic treatment takes precedence for the affected control or state.

Decorative colors may be expressive, but they must not create false system meaning.

## Centralized token rule

Applications must consume centralized Glaze UI semantic color tokens rather than hard-code independent status colors. Platform adapters may map the canonical tokens to native color resources, CSS custom properties, theme values, or equivalent primitives, but the semantic names and meanings remain stable.

Consumers may introduce application-specific semantic roles only when the role is genuinely domain-specific and does not duplicate or override a canonical Glaze UI role. Such roles should be mapped back to canonical system roles whenever the meaning is equivalent.

## Security, privacy, and resilience states

Wardveil Security, Privacy Shield, and Everkeep surfaces must use these semantic roles without transferring authority to Glaze UI. A `protected` presentation, for example, may only represent a protection state supplied by an authoritative producer under the relevant Wardveil contract; Glaze UI supplies presentation semantics, not security truth.

Unknown, stale, unavailable, or unverified evidence must not be visually upgraded into a positive state merely because a positive brand or accent color is available.

## Theme adaptation

Themes may change pigment, luminance, saturation, contrast, material treatment, translucency, and surrounding surface relationships. They must not reverse or collapse semantic meaning. A warning must remain distinguishishable from information and success; danger must remain distinguishable from accent; restricted must remain distinguishable from protected; offline and unavailable must not become visually equivalent to online.

## Conformance boundary

Conforming implementations must:

1. use canonical semantic roles for equivalent meanings;
2. avoid hard-coded application-specific replacements for canonical status colors;
3. preserve a non-color indicator for every material state;
4. keep branding/decorative color separate from system semantic meaning;
5. adapt tokens through theme/accessibility layers without changing their semantics;
6. preserve evidence and authority boundaries for security, privacy, resilience, synchronization, and connectivity states.
