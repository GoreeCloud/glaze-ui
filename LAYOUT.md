# Glaze UI Layout, Spacing, and Density

Status: Glaze UI 1.5 Stable. Glaze UI 1.5.0 remains Stable as the current production target; Glaze UI 1.4.0 is the immediately preceding historical Stable baseline.

## Purpose

Glaze UI layout is a semantic system for spatial hierarchy, readable measure, predictable adaptation, touch-safe interaction, and cross-form-factor consistency. It governs presentation only and does not redefine application behavior or platform authority.

## Core principles

1. Use semantic spacing roles rather than arbitrary per-screen values.
2. Preserve readable content measure before filling available width.
3. Adapt through container behavior and form-factor rules, not device-name branching.
4. Density may compress spacing but must not reduce accessibility targets or obscure hierarchy.
5. Safe areas, display cutouts, system bars, keyboards, and overscan boundaries are first-class layout inputs.
6. Horizontal scrolling is reserved for controls or content whose semantics require it; ordinary pages must not overflow horizontally.

## Spacing scale

The canonical primitive scale is `2, 4, 8, 12, 16, 24, 32, 48, 64, 96` CSS pixels. Semantic roles map onto this scale:

- `hairline`: 2 — optical separation and micro alignment only.
- `control-gap`: 8 — tightly related controls or icon/text pairs.
- `cluster-gap`: 12 — compact related groups.
- `component-gap`: 16 — default separation between sibling components.
- `section-gap`: 24 — separation between related subsections.
- `region-gap`: 32 — separation between major regions.
- `page-gap`: 48 — large page-level separation.
- `hero-gap`: 64 — deliberate editorial or hero separation.
- `display-gap`: 96 — large-screen/display composition only.

Spacing may interpolate responsively only when the semantic relationship remains unchanged and the result remains inside the adjacent primitive bounds.

## Responsive page gutters

Page gutters are minimum safe content insets, not targets for filling space:

- compact (<600px): 16px;
- medium (600–1023px): 24px;
- expanded (1024–1599px): 32px;
- large display (≥1600px): 48px.

Safe-area insets are additive. A display cutout, system bar, rounded viewport, or TV overscan margin may increase the effective gutter but never reduce the semantic minimum.

## Content measures

Content should stop growing when additional width harms comprehension or control locality:

- `prose`: max 72ch;
- `form`: max 720px;
- `standard`: max 1200px;
- `wide`: max 1600px.

Wide data, timelines, media strips, or intrinsically horizontal controls may use a bounded internal scrolling region. The page root must not become the horizontal scrolling surface for ordinary content.

## Density

Glaze UI defines three explicit density modes:

- `comfortable` — default general-purpose density;
- `compact` — information-dense pointer/keyboard workflows;
- `spacious` — touch-first, accessibility-forward, or far-view layouts.

Density modifies inter-element spacing and padding only. It must not reduce semantic target minimums, text legibility, focus affordances, or required separation between destructive and safe actions.

Compact density must not be selected solely because a viewport is wide or narrow. Input modality, task, platform conventions, user preference, and content structure matter. Mixed-input products must preserve safe coarse-pointer targets even when compact pointer presentation is available.

## Safe areas

Page primitives consume `env(safe-area-inset-*)` where available and accept product/platform adapters for environments where web safe-area variables are unavailable. TV products additionally apply the Stable overscan-safe contract.

Safe-area padding must not be baked into individual components. It belongs to page, shell, overlay, or platform boundary primitives so nested components do not double-apply it.

## Overflow

Root horizontal overflow is nonconforming for ordinary application pages. Components with intrinsic horizontal semantics must contain their own scroll behavior, provide keyboard access when interactive, preserve visible focus, and avoid obscuring required content.

Horizontal scrolling is reserved for intrinsically horizontal semantics such as tables, timelines, code, media strips, and comparable bounded regions. It is not a substitute for responsive layout.

## Localization and order

Layouts must tolerate longer translated strings, bidirectional text, increased text size, and platform text scaling without reordering meaning or focus. Visual order must remain compatible with semantic and focus order.

## Authority boundaries

Glaze UI governs spatial presentation and interaction geometry. It does not manufacture system truth. Privacy Shield remains authoritative for privacy state, Wardveil Security for security/protection state, Everkeep for resilience/preservation state, and GoreeCloud Mesh for coordination/governance state. Layout prominence cannot invent or upgrade any of those claims.

## Stable promotion boundary

This Stable contract is enforced by source validation and representative rendered acceptance. Consumer-specific native mapping, physical safe-area/overscan testing, localization review with production strings, accessibility review, and downstream migration evidence remain product-specific responsibilities.
