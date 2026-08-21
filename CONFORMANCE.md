# Glaze UI 1.3 Conformance

Glaze UI conformance protects both beauty and usability. An application is conformant when it uses the shared semantic contract without flattening its product personality.

## Seventeen required gates

1. **Identity** — recognizably GoreeCloud; no accidental upstream/default-framework identity.
2. **Tokens** — semantic colors, spacing, radii, expressive shapes, typography, icon sizing, density, material, motion, focus, state layers, target sizes, layout gutters, field composition, and safe-area behavior map to Glaze tokens or documented platform-native equivalents.
3. **Surface hierarchy** — Canvas, Solid, Raised, Glaze, and Overlay roles are intentional; ordinary content defaults to Solid/Raised, Functional Glass is primarily functional chrome, Clear Glass is limited to controls over visually rich media, and modal backdrops use a semantic scrim.
4. **States** — default, hover where applicable, pressed, focus, selected, disabled, loading, info, success, warning, error, and destructive behavior are defined when relevant. Interactive state feedback uses the shared state-layer contract or a documented native equivalent.
5. **Forms and selection** — editable fields have persistent labels, help/error relationships are programmatic when supported, selection controls expose checked/selected state, switches represent true binary settings, and progress exposes value semantics when determinate.
6. **Expressive hierarchy** — stronger shape, motion, typography, and adaptive emphasis are concentrated in important actions, selected containers, hero moments, or product identity. Repeated utility controls remain calm and predictable.
7. **Motion separation** — effects motion and spatial motion use the appropriate semantic family. Expressive spatial motion is not used indiscriminately, physical stretch/shift/rebound/shape-morph feedback remains bounded and purposeful, and reduced-motion mode removes nonessential shape/scale/spring/spatial transformations.
8. **Accessibility** — keyboard access where applicable, visible focus using the semantic focus role, semantic labels, target sizing, reduced motion, reduced transparency, increased contrast, forced colors, and solid glass fallback.
9. **Adaptive layout and reachability** — Compact, Medium, Expanded, and Wide layouts transform navigation and information density rather than merely shrinking. Mobile clients account for safe areas, viewport-bounded overlays, and may use lower action zones without changing logical/keyboard order.
10. **Form-factor fidelity** — supported phone, tablet, and desktop experiences are deliberately composed for their effective form factor and input model. Phone UI must not be a shrunken tablet or desktop layout; tablet UI must not be a stretched phone layout; desktop UI must not be an enlarged mobile shell. Representative acceptance verifies navigation, density, pane structure, interaction model, and primary workflows for each supported form factor.
11. **Adaptive action grouping** — group emphasis may change visual allocation but not action order, semantic meaning, focus order, or access to sibling actions.
12. **Privacy** — no tracking UI dependencies; remote fonts/scripts/icons are prohibited unless explicitly justified and documented; appearance preference remains local unless a product requirement needs synchronization.
13. **Resilience** — core content and critical actions remain understandable when blur, animation, remote assets, or nonessential JavaScript features are unavailable.
14. **Product personality and visual character** — applications may vary composition, accent emphasis, imagery, information architecture, visualization, and specialized components while retaining a recognizable Glaze family resemblance. Where appropriate to the product and platform, that resemblance includes layered depth, selective translucency and blur, restrained reflection/highlight cues, soft elevation, rounded/circular/pill geometry, coordinated adaptive tints and accents, deliberate whitespace and grouping, bold information hierarchy, and tactile but bounded motion. No single effect is mandatory everywhere, and beauty must not override readability, semantic contrast, accessibility, performance, or the application's Role and Purpose.
15. **Cross-platform mapping** — web, Linux, Android, iOS, and other clients use the same semantic roles even when platform-native implementation primitives differ. Platform-native clients may diverge in navigation and composition when required to provide the correct phone, tablet, or desktop experience.
16. **Visual acceptance** — light and dark modes are reviewed visually at representative phone/Compact, tablet/Medium, desktop/Expanded, and Wide layouts for every supported target before stable release; products with native clients also require representative real-client acceptance. Review must consider the complete visual character—material depth, coordinated color, geometry, spacing, hierarchy, grouping, and motion quality—rather than treating the presence of rounded cards or blur as sufficient Glaze UI evidence.
17. **Stability and lifecycle** — Stable consumers target only Glaze UI capabilities classified Stable in `COMPONENT_STATUS.md` unless a documented application-specific exception explicitly adopts Candidate behavior. Stable releases follow `STABILITY.md`: exact-revision evidence, compatibility assessment, fail-closed validation, documented rollback, no silent Candidate/Experimental dependency, and no speculative roadmap concept represented as shipping functionality.

## Form-factor acceptance expectations

Phone acceptance should verify touch-first navigation, safe areas, reachable primary actions, readable single-column or intentionally stacked content, mobile-appropriate sheets/dialogs, and the absence of desktop/tablet composition merely reduced in scale.

Tablet acceptance should verify intentional use of the larger canvas through suitable rails, side panels, split views, master-detail relationships, previews, contextual panes, or other tablet-appropriate structures when they benefit the product. Simply increasing margins around a phone composition is not sufficient.

Desktop acceptance should verify pointer and keyboard affordances, useful window resizing, desktop-appropriate information density, persistent navigation or toolbars when beneficial, keyboard shortcuts where applicable, hover/context behavior, multi-pane workflows where useful, and the absence of a phone-first shell enlarged to fill the window.

Breakpoint values guide responsive implementation but do not replace form-factor judgment. Variable-window devices such as foldables, desktop-mode mobile environments, and resizable application windows may transition between form-factor compositions dynamically.

## Evidence

Each stable GoreeCloud application should expose a small automated Glaze contract test and record any exception with the affected rule, reason, user impact, approved fallback, and review condition. Consumer records should identify the exact Glaze UI version and, when practical, the canonical source revision used for validation.

Automated evidence should verify the durable semantics the product actually consumes. For web clients using the 1.3 expressive layer, this includes functional/clear glass usage boundaries, solid fallbacks, expressive shape semantics, reduced-motion behavior, reachability without document-order mutation, adaptive group semantics, persistent labels, focus visibility, error/help relationships, checked or selected state, target sizing, form-factor transitions, and the absence of unapproved remote presentation dependencies.

For multi-form-factor products, evidence should include representative phone, tablet, and desktop checks that assert the intended navigation and layout mode is active. Passing overflow or screenshot-size checks alone does not establish form-factor conformance.

Visual evidence should also demonstrate that the application feels compositionally connected rather than assembled from unrelated widgets. When the target supports the relevant effects, reviewers should check coordinated surface depth, background-aware color relationships, recognizable geometry, readable hierarchy, deliberate grouping, and responsive interaction feedback while confirming that accessibility and solid-surface fallbacks remain intact.

Stability evidence should identify the lifecycle status of any Glaze capability the product consumes. A Stable product must not silently depend on a Candidate, Experimental, or merely Planned capability. When a Candidate is intentionally adopted for evaluation, that state must be explicit and must not be described as Stable conformance.

## Conformance statement

A product may claim `Glaze UI 1.3 conformant` only when all applicable gates above are satisfied or every deviation is covered by an explicit, documented GoreeCloud exception. Conformance is version-specific and should be re-evaluated when a product changes its presentation architecture or adopts a new major or minor Glaze UI version that expands applicable semantics.

A Stable claim additionally requires compliance with `STABILITY.md` and may use only the Stable lifecycle surface recorded in `COMPONENT_STATUS.md`, except where a separately documented exception explicitly states otherwise.
