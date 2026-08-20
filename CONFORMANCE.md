# Glaze UI 1.3 Conformance

Glaze UI conformance protects both beauty and usability. An application is conformant when it uses the shared semantic contract without flattening its product personality.

## Required gates

1. **Identity** — recognizably GoreeCloud; no accidental upstream/default-framework identity.
2. **Tokens** — semantic colors, spacing, radii, expressive shapes, typography, icon sizing, density, material, motion, focus, state layers, target sizes, layout gutters, field composition, and safe-area behavior map to Glaze tokens or documented platform-native equivalents.
3. **Surface hierarchy** — Canvas, Solid, Raised, Glaze, and Overlay roles are intentional; ordinary content defaults to Solid/Raised, Functional Glass is primarily functional chrome, Clear Glass is limited to controls over visually rich media, and modal backdrops use a semantic scrim.
4. **States** — default, hover where applicable, pressed, focus, selected, disabled, loading, info, success, warning, error, and destructive behavior are defined when relevant. Interactive state feedback uses the shared state-layer contract or a documented native equivalent.
5. **Forms and selection** — editable fields have persistent labels, help/error relationships are programmatic when supported, selection controls expose checked/selected state, switches represent true binary settings, and progress exposes value semantics when determinate.
6. **Expressive hierarchy** — stronger shape, motion, typography, and adaptive emphasis are concentrated in important actions, selected containers, hero moments, or product identity. Repeated utility controls remain calm and predictable.
7. **Motion separation** — effects motion and spatial motion use the appropriate semantic family. Expressive spatial motion is not used indiscriminately, and reduced-motion mode removes nonessential shape/scale/spatial transformations.
8. **Accessibility** — keyboard access where applicable, visible focus using the semantic focus role, semantic labels, target sizing, reduced motion, reduced transparency, increased contrast, forced colors, and solid glass fallback.
9. **Adaptive layout and reachability** — Compact, Medium, Expanded, and Wide layouts transform navigation and information density rather than merely shrinking. Mobile clients account for safe areas, viewport-bounded overlays, and may use lower action zones without changing logical/keyboard order.
10. **Adaptive action grouping** — group emphasis may change visual allocation but not action order, semantic meaning, focus order, or access to sibling actions.
11. **Privacy** — no tracking UI dependencies; remote fonts/scripts/icons are prohibited unless explicitly justified and documented; appearance preference remains local unless a product requirement needs synchronization.
12. **Resilience** — core content and critical actions remain understandable when blur, animation, remote assets, or nonessential JavaScript features are unavailable.
13. **Product personality** — applications may vary composition, accent emphasis, imagery, information architecture, visualization, and specialized components while retaining the Glaze contract.
14. **Cross-platform mapping** — web, Linux, Android, iOS, and other clients use the same semantic roles even when platform-native implementation primitives differ.
15. **Visual acceptance** — light and dark modes are reviewed visually at representative Compact and Expanded widths before stable release; products with additional native clients also require representative real-client acceptance.

## Evidence

Each stable GoreeCloud application should expose a small automated Glaze contract test and record any exception with the affected rule, reason, user impact, approved fallback, and review condition. Consumer records should identify the exact Glaze UI version and, when practical, the canonical source revision used for validation.

Automated evidence should verify the durable semantics the product actually consumes. For web clients using the 1.3 expressive layer, this includes functional/clear glass usage boundaries, solid fallbacks, expressive shape semantics, reduced-motion behavior, reachability without document-order mutation, adaptive group semantics, persistent labels, focus visibility, error/help relationships, checked or selected state, target sizing, and the absence of unapproved remote presentation dependencies.

## Conformance statement

A product may claim `Glaze UI 1.3 conformant` only when all applicable gates above are satisfied or every deviation is covered by an explicit, documented GoreeCloud exception. Conformance is version-specific and should be re-evaluated when a product changes its presentation architecture or adopts a new major or minor Glaze UI version that expands applicable semantics.
