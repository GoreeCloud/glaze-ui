# Glaze UI Layout, Spacing, and Density

Status: Glaze UI 1.5 Candidate. Glaze UI 1.4.0 remains Stable.

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
- `content-gap`: 16 — default sibling content spacing.
- `section-gap`: 32 — major section separation.
- `region-gap`: 48 — independent page regions.
- `page-gap`: 64 — large structural separation.

Do not use `hairline` as a touch target or text clearance substitute.

## Page gutters

Minimum page gutters are semantic and responsive:

- compact: 16px
- medium: 24px
- expanded: 32px
- large-screen/TV: 48px

Applications may grow gutters when composition benefits, but must not shrink below the active semantic minimum except for edge-to-edge media or platform-native immersive surfaces.

## Content measure

- prose: maximum 72ch
- forms and settings: maximum 720px
- standard application content: maximum 1200px
- wide data or media workspace: maximum 1600px where the task genuinely benefits

A component should choose the narrowest measure appropriate to its task. Maximum measure is not a required width.

## Containers and grids

Use fluid containers with semantic maximum measures. Grid columns are content-driven; Glaze UI does not require a fixed 12-column implementation. Responsive composition must prefer reflow, wrapping, stacking, and progressive disclosure over shrinking interactive content below accessible limits.

## Density modes

Glaze UI defines three presentation densities:

- `comfortable` — default for general-purpose surfaces.
- `compact` — information-dense desktop/tablet workflows.
- `spacious` — TV, touch-at-distance, presentation, and low-clutter contexts.

Density modifies inter-element spacing and padding only. It must not reduce minimum pointer/touch targets, text legibility, focus indication, or semantic separation required for comprehension.

Compact density must never be automatically inferred solely from viewport width. The application or platform adapter selects density according to input modality and task.

## Minimum interactive geometry

- coarse/touch target: at least 44×44 CSS px
- pointer-focused compact target: at least 32×32 CSS px when an equivalent accessible activation area is preserved
- adjacent destructive and primary actions require enough separation to avoid accidental activation

Platform-native guidance may require larger targets and takes precedence where stricter.

## Safe areas and transient UI

Root page containers must support `env(safe-area-inset-*)` where available. Bottom actions, sheets, media controls, and navigation must remain reachable above transient system UI and virtual keyboards. Fixed positioning must not assume all viewport pixels are usable.

## Responsive behavior

Glaze UI uses four representative presentation classes aligned with the Stable form-factor contract:

- compact/mobile
- medium/tablet
- expanded/desktop
- large-screen/TV

These are behavioral classes, not hardware identities. Foldables, resizable windows, desktop web views, and embedded surfaces may cross classes dynamically.

Layouts must remain valid during resizing and orientation changes without requiring a full application restart.

## Overflow

Ordinary page shells must not create horizontal viewport overflow. Long text must wrap or truncate according to component semantics. Code, tables, timelines, media strips, and other intrinsically wide content may use bounded internal scrolling without forcing the root viewport to scroll horizontally.

## Accessibility and localization

Layout must tolerate text enlargement, longer translations, bidirectional text, and user font substitutions. Fixed heights around text are discouraged unless the component contract explicitly guarantees clipping-safe content. Spatial ordering must not contradict semantic or focus order.

## Performance

Layout primitives must prefer normal flow, grid, flexbox, container queries, and bounded sticky/fixed regions. Avoid JavaScript measurement loops for behavior expressible in CSS. Performance degradation must not collapse content hierarchy or accessibility geometry.

## Authority boundaries

Glaze UI governs visual spacing, layout, density, and responsive presentation. Privacy Shield, Wardveil Security, Everkeep, and GoreeCloud Mesh remain authoritative for their underlying privacy, security, resilience, and coordination state. Layout must never imply capabilities those systems have not established.

## Candidate boundary

This contract is isolated to Glaze UI 1.5 Candidate. It does not alter the 1.4.0 Stable contract, migrate consumers, or authorize production conformance until explicit promotion.
