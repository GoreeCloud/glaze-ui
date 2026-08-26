# Glaze UI 1.5 Adaptive Color Architecture Stable

> Status: Stable design-system extension. Glaze UI 1.4.0 remains the current Stable baseline until the complete 1.5 promotion gate passes.

Glaze UI 1.5 evolves the existing semantic color contract into a complete adaptive color architecture. Color is treated as an intelligent visual-language layer spanning semantic meaning, hierarchy, materials, interaction, application identity, personalization, accessibility, and motion.

## Governing principles

1. Semantic meaning is stable even when pigment changes.
2. Important states are never communicated by color alone.
3. Application identity and user personalization may influence decoration but may not redefine system semantics.
4. Color, material, depth, and motion are one coordinated presentation system.
5. Accessibility modes select purpose-built tones instead of merely inverting a default palette.
6. Wardveil Security, Privacy Shield, Everkeep, and other authoritative producers supply truth; Glaze UI only presents evidence-backed states.

## Contextual color layers

Color may propagate across related surfaces, borders, icons, controls, typography, focus treatment, selection treatment, and local interaction regions. Contextual propagation must remain restrained and must not turn an entire interface into a single undifferentiated tint.

Selected or active regions may receive `selection.glaze`, which softly coordinates the selected surface with nearby controls and indicators while preserving readable foreground contrast.

## Semantic tonal families

Each semantic family provides four presentation tones:

- `subtle` — quiet background, surface, or low-emphasis treatment;
- `standard` — ordinary foreground, icon, control, and status treatment;
- `prominent` — elevated attention across container, border, icon, and typography;
- `critical` — strongest appropriate multi-channel treatment for urgent states.

The stable families are `accent`, `success`, `information`, `warning`, `danger`, `privacy`, `security`, `online`, `offline`, `syncing`, `protected`, `restricted`, and `unavailable`.

`critical` is a prominence level, not permission to flash, pulse continuously, or overwhelm the interface. Critical presentation remains subject to reduced-motion, contrast, readability, and distraction limits.

## Adaptive accent coloring

Decorative accent color may be influenced by the user's selected accent, wallpaper, product identity, current content, and interface context. Adaptive accent derivation is constrained by semantic protection boundaries:

- success, warning, danger, destructive, privacy, security, protection, restriction, connectivity, and availability meaning may not be recolored into ambiguity;
- identity colors may not make normal actions resemble destructive or critical actions;
- contextual color extraction must preserve minimum contrast and readable foreground separation;
- dynamic sources are decorative inputs, not authoritative state inputs.

## Materials and depth

Color participates directly in Glaze UI materials. Canvas, Solid, Raised, Functional Glass, Clear Glass, and Overlay may use coordinated changes in luminosity, tonal separation, diffusion, saturation, highlights, gradients, and material density.

Translucent surfaces may borrow a bounded amount of color from content behind them. Background sampling must never reduce foreground legibility or erase boundaries needed for comprehension. Reduced-transparency and no-backdrop-filter modes use purpose-built solid alternatives.

## Motion and color

Color transitions may communicate state changes, selection, synchronization, completion, and attention. They must use the Glaze UI motion vocabulary and remain purposeful.

- successful operations may gently resolve toward success treatment;
- synchronization may use restrained animated accent treatment;
- selection may acquire contextual glazing smoothly;
- warnings may transition deliberately without unnecessary flashing.

Reduced-motion modes replace nonessential animated color behavior with immediate or simplified state changes while preserving meaning.

## Accessibility architecture

Every semantic family and prominence level must remain understandable in light, dark, high-contrast, forced-colors, grayscale/desaturated, reduced-transparency, and common color-vision-deficiency contexts. Implementations must provide non-color companions for material states through labels, icons, shape, pattern, position, text, or equivalent programmatic indicators.

Accessibility is a token-generation and component-contract requirement, not a post-processing filter.

## Token consumption

Applications request semantic tokens rather than hard-coded colors. Stable examples include:

- `accent.surface.subtle`
- `accent.foreground.standard`
- `success.icon.standard`
- `warning.border.prominent`
- `danger.surface.critical`
- `privacy.foreground.standard`
- `security.surface.prominent`
- `selection.glaze`
- `material.sample.maxInfluence`

Platform adapters may map these semantics into native color resources, CSS custom properties, theme values, or equivalent primitives while preserving names, meanings, prominence, and accessibility boundaries.

## Promotion boundary

Glaze UI 1.5 cannot become Stable on documentation alone. Promotion requires exact-final-revision source validation, adaptive-color token validation, representative rendered acceptance, light/dark/high-contrast/reduced-transparency review, color-vision and non-color-indicator checks, compatibility assessment, rollback documentation, and current-Stable consumer migration planning. Until then, 1.4.0 remains the mandatory Stable application target.
