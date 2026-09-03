# GLAZE UI V1.0 — Semantic Color Contract

**Status:** Official V1 baseline; production revalidation required.

GLAZE UI V1.0 uses color semantically rather than decoratively. Semantic meaning must remain consistent across GoreeCloud surfaces regardless of application identity, theme, form factor, or platform, and material information must never be communicated by **color alone**.

## Core semantic roles

The canonical machine-readable roles in `tokens/semantic-colors.json` are `accent`, `surface`, `selected`, `focus`, `success`, `information`, `warning`, `danger`, `protected`, `restricted`, `online`, `offline`, `syncing`, and `unavailable`.

These names define meaning rather than fixed pigments. Rendered values may adapt for light, dark, **high-contrast**, **grayscale**, **color-vision** accommodation, custom themes, display characteristics, and reduced-effects environments while preserving the semantic role.

## Accessibility requirements

Every material semantic state requires a non-color companion such as a label, icon, shape, pattern, position, status description, or another programmatically exposed indicator. A consumer is nonconforming if loss or alteration of color alone removes the user's ability to understand a material state.

Focus and selection must remain distinguishable when both can occur. Consequential warning, danger, security, privacy, protection, connectivity, and availability states must remain understandable under accessibility adaptations.

## Branding and semantic separation

Application identity colors are not semantic status colors. Branding must not redefine success, information, warning, danger, protected, restricted, online, offline, syncing, unavailable, selection, or focus.

Where product identity conflicts with a system semantic role, the system semantic treatment takes precedence. Decorative or adaptive colors may be expressive, but they must not create false system meaning.

## Centralized token rule

Applications must consume centralized GLAZE UI V1.0 semantic color tokens rather than hard-code independent replacements for canonical state meanings. Platform adapters may map the tokens to native resources, CSS custom properties, theme values, or equivalent primitives, but the semantic names and meanings remain stable.

Consumers may introduce domain-specific roles only when they do not duplicate or override a canonical role. Equivalent meanings should map back to canonical system semantics.

## Truth and authority boundaries

Wardveil Security, Privacy Shield, Everkeep, GoreeCloud Identity, GoreeCloud Mesh, and other authoritative systems retain authority over their own truth domains. Glaze UI supplies presentation semantics only.

A `protected`, `restricted`, privacy, security, recovery, synchronization, availability, or similar presentation must be backed by the applicable **authoritative producer**. Unknown, stale, unavailable, or unverified evidence must never be visually upgraded into a positive state merely because a positive brand or accent color is available.

## Theme and adaptive color

Themes may change pigment, luminance, saturation, contrast, material treatment, translucency, and surrounding surface relationships. They must not reverse or collapse semantic meaning. Wallpaper or content-derived adaptation may influence non-protected presentation, but it must not override semantic truth.

## Conformance boundary

Conforming implementations must use canonical roles for equivalent meanings, preserve non-color indicators, keep branding separate from semantic state, adapt tokens without changing their meaning, and preserve authority boundaries for security, privacy, resilience, synchronization, and connectivity.

Machine-readable color contracts remain subject to fresh exact-revision V1 acceptance. Passing the semantic-color validator proves contract consistency; it does not by itself establish rendered accessibility or production Stable acceptance.
