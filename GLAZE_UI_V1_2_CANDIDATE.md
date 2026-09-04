# GLAZE UI V1.2 — Frosted Neutral Material Candidate

**Lifecycle:** Planned Candidate / next-upgrade track  
**Stable baseline:** GLAZE UI V1.1 / 1.1.0  
**Promotion status:** Not Stable; not a consumer migration target  
**Primary intent:** Move the default Glaze material from teal/amber atmospheric tinting toward frosty, white, blurred, translucent neutral glass.

GLAZE UI V1.2 preserves the V1.1 structural, semantic, accessibility, hierarchy, component, System Shell, and performance contracts while changing the default optical character of glazed surfaces.

## Governing visual rule

**Neutral glass is the material. Color is an accent.**

Ordinary glazed surfaces must read first as frosted white, pearl, clear-neutral, soft gray, or neutral dark glass. Blue, teal, green, aqua, amber, or other chromatic pigments must not become the default base tint of windows, panels, cards, menus, toolbars, sheets, dialogs, popovers, search surfaces, sidebars, quick settings, or shell chrome.

Semantic and brand colors remain available for active controls, focus, selection, progress, status, badges, icons, and product identity. They do not define the underlying glass substrate.

## Light appearance

The target character is milky, translucent, softly reflective glass with visible backdrop diffusion.

Reference material values:

- Base glass: `rgba(255, 255, 255, 0.58)`
- Raised glass: `rgba(255, 255, 255, 0.72)`
- Overlay glass: `rgba(250, 250, 250, 0.82)`
- Specular border: `rgba(255, 255, 255, 0.52)`
- Structural border: `rgba(80, 80, 80, 0.10)`
- Standard blur: `28px`
- Heavy blur: `44px`
- Backdrop saturation target: approximately `1.08–1.15`

The values are reference targets, not permission to weaken contrast or hierarchy.

## Dark and Deep Dark appearance

Dark Glaze remains translucent but becomes neutral graphite/smoke rather than blue-green.

Reference material values:

- Dark base: `rgba(25, 25, 27, 0.62)`
- Dark raised: `rgba(38, 38, 41, 0.72)`
- Dark overlay: `rgba(42, 42, 45, 0.82)`
- Dark specular border: `rgba(255, 255, 255, 0.12)`
- Deep Dark base: `rgba(14, 14, 16, 0.72)`
- Deep Dark overlay: `rgba(24, 24, 27, 0.86)`

A cool or warm environmental cast may appear indirectly through the backdrop, but the material itself remains neutral.

## Material hierarchy

The inherited material hierarchy remains **Canvas → Surface → Soft Glaze → Glaze → Deep Glaze → Live Glaze**.

V1.2 changes how glazed levels are optically differentiated:

- **Soft Glaze:** light diffusion, low-opacity neutral fill, subtle white edge.
- **Glaze:** stronger diffusion and a slightly more opaque neutral substrate.
- **Deep Glaze:** greater depth, broader shadow, stronger edge separation, still chromatically neutral.
- **Live Glaze:** may expose more environmental color from the backdrop or content, but must not paint a permanent teal/green base tint onto the material.

Depth should come from blur, opacity, luminance, border reflection, geometry, and shadow before hue.

## Frosted edge and depth language

Glaze surfaces should use:

- soft white or neutral specular highlights along upper/light-facing edges;
- faint inner edge illumination rather than hard outlines;
- broad low-opacity shadows rather than dense black strokes;
- rounded geometry and capsule treatments where appropriate;
- visual separation through opacity and depth before chromatic tint.

No glossy effect may obscure text, state, target boundaries, or focus.

## Color and atmosphere policy

The V1.1 Deep Teal + Soft Amber atmosphere becomes **optional accent atmosphere**, not the default material substrate.

For V1.2 Candidate:

- neutral material contribution is the dominant optical source;
- default material tint from teal, aqua, green, or amber is `0`;
- atmospheric aura may remain outside a surface or pass through the backdrop at low strength;
- selected, focused, active, semantic, or branded controls may use color intentionally;
- quick-settings and shell panels must be neutral glass with colored active states, not colored glass panels with brighter colored controls.

## Wallpaper and backdrop interaction

The material should allow bounded background color and form to diffuse through the surface. Background-derived color is an optical consequence of translucency, not a hard-coded panel pigment.

Environmental sampling remains local-only and optional. It must not infer protected semantics or transmit source imagery for derivation.

## Accessibility and resilience

Reduced Transparency removes backdrop-dependent effects and falls back toward solid neutral surfaces while preserving hierarchy, contrast, boundaries, and state.

Forced Colors disables custom material pigmentation and custom optical edge treatment where required by the platform.

Increased Contrast strengthens boundaries before adding chroma.

Reduced Motion is independent of transparency and does not alter semantic state.

Critical reading and consequential-decision surfaces remain eligible for Solid/Raised treatment under the inherited material contract.

## Performance

V1 material budgets remain inherited: one dominant Glaze region plus up to three small floating Glaze controls by default, with no default nested backdrop blur.

When performance degrades, reduce environmental effects and blur before degrading text, target size, state, focus, or semantic truth.

## Candidate implementation

- Candidate tokens: `tokens/glaze-v1.2-frosted-neutral.candidate.json`
- Candidate web layer: `css/glaze-v1.2-frosted-neutral.candidate.css`
- Candidate preview entrypoint: `css/glaze-v1.2.0-candidate.css`
- Candidate reference: `reference/v1.2/frosted-neutral.html`
- Candidate validator: `scripts/validate_glaze_v1_2_candidate.py`

Until V1.2 is formally promoted, the preview layer is activated on the V1.1 Stable baseline with `data-glaze-upgrade="v1.2-frosted-neutral"`. This does not change `VERSION`, `currentStable`, or downstream consumer eligibility.
