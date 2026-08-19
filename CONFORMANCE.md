# Glaze UI 1.1 Conformance

Glaze UI conformance protects both beauty and usability. An application is conformant when it uses the shared semantic contract without flattening its product personality.

## Required gates

1. **Identity** — recognizably GoreeCloud; no accidental upstream/default-framework identity.
2. **Tokens** — semantic colors, spacing, radii, typography, icon sizing, density, motion, focus, state layers, target sizes, layout gutters, and safe-area behavior map to Glaze tokens or documented platform-native equivalents.
3. **Surface hierarchy** — Canvas, Solid, Raised, Glaze, and Overlay roles are intentional; translucency is selective and modal backdrops use a semantic scrim.
4. **States** — default, hover where applicable, pressed, focus, selected, disabled, loading, info, success, warning, error, and destructive behavior are defined when relevant. Interactive state feedback uses the shared state-layer contract or a documented native equivalent.
5. **Accessibility** — keyboard access where applicable, visible focus, semantic labels, target sizing, reduced motion, increased contrast, forced colors, and solid glass fallback.
6. **Adaptive layout** — Compact, Medium, Expanded, and Wide layouts transform navigation and information density rather than merely shrinking. Mobile clients account for safe areas and viewport-bounded overlays.
7. **Privacy** — no tracking UI dependencies; remote fonts/scripts/icons are prohibited unless explicitly justified and documented; appearance preference remains local unless a product requirement needs synchronization.
8. **Resilience** — core content and critical actions remain understandable when blur, animation, remote assets, or nonessential JavaScript features are unavailable.
9. **Product personality** — applications may vary composition, accent emphasis, imagery, information architecture, visualization, and specialized components while retaining the Glaze contract.
10. **Cross-platform mapping** — native web, Linux, Android, iOS, and other clients use the same semantic roles even when platform-native implementation primitives differ.
11. **Visual acceptance** — light and dark modes are reviewed visually at representative Compact and Expanded widths before stable release; products with additional native clients also require representative real-client acceptance.

## Evidence

Each stable GoreeCloud application should expose a small automated Glaze contract test and record any exception with the affected rule, reason, user impact, approved fallback, and review condition. Consumer records should identify the exact Glaze UI version and, when practical, the canonical source revision used for validation.

## Conformance statement

A product may claim `Glaze UI 1.1 conformant` only when all applicable gates above are satisfied or every deviation is covered by an explicit, documented GoreeCloud exception. Conformance is version-specific and should be re-evaluated when a product changes its presentation architecture or adopts a new major or minor Glaze UI version that expands applicable semantics.
