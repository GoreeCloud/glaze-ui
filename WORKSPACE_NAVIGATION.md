# Glaze UI 1.6 Stable — Adaptive Workspace and Navigation

Status: **Stable in Glaze UI 1.6.0**. This contract is part of the current Stable compatibility and production-conformance baseline.

## Purpose

The Adaptive Workspace layer turns Glaze UI's window, navigation, toolbar, inspector, responsive-layout, density, and input-method principles into a reusable shell contract. It is presentation and interaction architecture only; it does not redefine application behavior or the authority of Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Mesh, or application logic.

## Workspace anatomy

A Glaze workspace may contain these semantic regions:

- **window** — the application-owned visual workspace inside the platform window or browser viewport;
- **title region** — title, document identity, drag affordance, window controls, or platform-native equivalents;
- **navigation** — primary destination structure such as a sidebar, rail, tab bar, navigation bar, or bottom navigation;
- **toolbar** — frequently used actions and contextual tools;
- **content** — the primary task and information surface;
- **inspector** — contextual properties, metadata, details, filters, or secondary tools;
- **status region** — persistent non-modal status that remains subordinate to content;
- **overlay** — menus, popovers, dialogs, sheets, transient controls, and other elevated temporary surfaces.

The content region remains visually primary. Chrome supports content rather than competing with it.

## Layer model

The workspace shell uses the existing Glaze material hierarchy instead of inventing a parallel surface system:

1. Canvas / content foundation
2. Solid or Raised content regions
3. Functional Glass navigation and toolbar chrome when appropriate
4. Overlay surfaces for transient interaction

Primary reading surfaces should normally remain Solid or Raised. Functional Glass is appropriate for navigation and interactive chrome when contrast and performance permit it. Reduced-transparency and unsupported-backdrop environments must fall back to stable opaque presentation.

## Desktop window behavior

Desktop implementations should preserve the platform's native window-management affordances. Glaze UI may style application-owned regions but must not obscure or break platform-provided moving, resizing, snapping, minimizing, maximizing, restoring, closing, focus indication, or keyboard window-management behavior.

Application-owned title regions must preserve a clear drag area where the platform supports client-side decoration. Interactive controls inside a drag region must remain individually actionable and excluded from dragging.

Secondary windows are appropriate for documents, inspectors, previews, tools, and focused workflows. Blocking modal dialogs are reserved for actions that genuinely require immediate completion or confirmation.

## Navigation transformation

Glaze UI does not force one navigation pattern across all device classes. The same destination model may transform while preserving task continuity and semantic order:

- **Desktop:** persistent sidebar or rail, toolbar, contextual menus, and optional inspector.
- **Tablet:** adaptive sidebar/rail, split view, collapsible inspector, and touch-first toolbar behavior.
- **Mobile:** single-task navigation, top or bottom navigation, sheets, progressive disclosure, and compact action surfaces.
- **TV:** a distinct far-view workspace with persistent directional-focus navigation, larger targets and chrome, shallow predictable groups, far-view labels, and no pointer/swipe dependency for primary tasks. TV must not inherit the Wide Desktop workspace merely because its viewport is large.

A persistent sidebar may become an overlay drawer, an inspector may become a sheet, and low-priority toolbar actions may move into overflow. These are semantic transformations, not arbitrary rearrangements.

## Sidebar contract

Sidebars may contain sections, expandable groups, destinations, badges, favorites, pinned items, drag-and-drop organization, and contextual commands when the product requires them.

Sidebar selection must be visually distinct from keyboard focus. Collapsing a sidebar must preserve the user's current destination and must not remove access to required actions. Icon-only collapsed navigation requires accessible names and recognizable symbols.

## Toolbar contract

Toolbars contain frequent actions, not every command. Related controls should be clustered, lower-priority actions should move into overflow before becoming cramped, and destructive actions must remain visually and spatially differentiated from safe actions.

Toolbar adaptation must preserve action semantics, accessible names, keyboard order, and state. Moving an action into overflow must not silently change its enabled, selected, destructive, or loading state.

## Inspector contract

Inspectors present contextual detail and secondary controls without displacing the primary task. They may be persistent on Desktop, collapsible on Tablet, and transformed into sheets or panels on Mobile.

Closing or collapsing an inspector must not destroy unsaved user state unless the application explicitly requires that behavior and communicates it.

## Input-aware targets

Glaze UI keeps accessibility target floors while allowing pointer-dense presentation:

- coarse-pointer / touch reference target: **48px minimum**;
- mixed-input default: **44px minimum**, expanding to the coarse-pointer floor when touch is available or active;
- precision-pointer compact presentation may visually compress padding but must preserve a **40px minimum hit region** and a visible focus target;
- TV reference target: **56px minimum**.

Products may exceed these values. Compact density must never make destructive actions difficult to distinguish or activate safely.

## Density modes

The workspace layer recognizes three explicit modes:

- `comfortable` — default general-purpose composition;
- `compact` — pointer/keyboard productivity and high-information workflows;
- `spacious` — touch-forward, accessibility-forward, presentation, or far-view contexts.

Density changes spacing, padding, and information presentation. It does not reduce text legibility, focus visibility, semantic hierarchy, or required touch/far-view targets.

## Concentric geometry

Nested workspace surfaces use coordinated geometry. Outer shells and large cards use the broader radius family; nested panels, fields, buttons, menus, and selection surfaces use proportionally smaller radii. Geometry should look related without forcing every component into the same radius.

## Scroll and sticky chrome

Navigation or toolbar chrome may remain sticky or visually float above content when this improves continuity. Sticky regions must not cover focused controls, fragment anchors, validation messages, or required content. Content may extend beneath appropriate translucent chrome only when contrast and focus remain understandable.

## Accessibility and resilience

The workspace layer requires:

- logical reading and focus order independent of visual rearrangement;
- visible `:focus-visible` treatment;
- accessible names for icon-only and collapsed controls;
- reduced-motion-safe layout transitions;
- reduced-transparency and no-backdrop-filter fallbacks;
- performance-constrained opaque material fallbacks where dynamic backdrop effects are unsuitable;
- forced-colors compatibility;
- keyboard access for Desktop and web navigation, toolbar, menu, dialog, and inspector controls;
- no hover-only primary interaction on touch-capable layouts;
- state communication that does not depend exclusively on color or motion; and
- a static, high-contrast directional-focus treatment for TV when motion or rich materials are unavailable.

## State and authority boundaries

Workspace surfaces may present privacy, security, resilience, synchronization, identity, local/cloud, loading, warning, and error state, but they do not manufacture that truth. Producer-authoritative state remains governed by the applicable GoreeCloud platform system or application logic.

## Candidate implementation

The Stable implementation consists of:

- `tokens/workspace-navigation.candidate.json` — machine-readable semantic contract;
- `css/glaze.workspace.candidate.css` — reusable workspace primitives with Desktop/Tablet/Mobile/Wide Desktop/TV composition, density, input-aware targets, and accessibility/performance fallbacks;
- `reference/candidate-1.6-workspace.html` — dependency-free configurable reference composition;
- `reference/candidate-1.6-workspace-acceptance.html` — fail-closed browser-rendered acceptance harness;
- `scripts/validate_workspace_navigation.py` — fail-closed source and promotion-evidence validation;
- `scripts/validate_candidate_1_6_rendered.py` — rendered Mobile/Tablet/Desktop/Wide Desktop/TV, density, and accessibility/resilience matrix;
- `acceptance/1.6-candidate.md` — Candidate lifecycle, scope, evidence, compatibility, and rollback record; and
- CI coverage in `.github/workflows/ci.yml`.

## Stable rendered acceptance matrix

The Stable workspace is evaluated in light and dark appearances at Mobile `390×844`, Tablet `820×1180`, Desktop `1280×900`, Wide Desktop `1600×1000`, and TV `1920×1080`.

Additional cases cover compact Desktop, spacious Mobile, reduced motion, reduced transparency, constrained-performance material fallbacks, and TV forced colors. The matrix must fail closed on root overflow, missing workspace regions, lost current-destination semantics, undersized targets, incorrect form-factor transformations, TV falling through to Wide Desktop, or missing resilience behavior.

This rendered matrix remains the platform-neutral Stable regression contract only. Platform-native consumers still require their own native/real-device and application-specific acceptance.

## Stable release boundary

Stable promotion requires exact-head CI, rendered acceptance across representative Mobile, Tablet, Desktop, Wide Desktop, and TV contexts, accessibility/resilience review, mixed-input validation, compatibility review, documentation synchronization, and explicit promotion under `STABILITY.md`.

The separate Glaze UI 1.6 Evidence Presentation Candidate must also satisfy its own applicable promotion requirements. Passing the Adaptive Workspace matrix alone does not authorize Stable 1.6 promotion.

Glaze UI 1.6.0 promotion completed the design-system gate. Downstream applications must still complete controlled 1.6 adoption and application-specific rendered/native/real-device acceptance before claiming current Stable conformance.
