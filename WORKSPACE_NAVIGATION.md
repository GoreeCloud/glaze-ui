# Glaze UI 1.6 Stable — Adaptive Workspace and Navigation

Status: **Stable in Glaze UI 1.6.0** and retained in the current **Glaze UI 2.2.0** compatibility and production-conformance baseline.

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

Workspace regions map to existing Glaze UI material roles rather than inventing a second material system:

- content defaults to **Solid** or **Raised**;
- persistent navigation and tool chrome may use **Functional Glass** when contrast, performance, and platform capability permit;
- overlays use the established **Overlay** hierarchy;
- Clear Glass remains specialized for controls over visually rich media and is not a default workspace panel material;
- reduced-transparency, unsupported-backdrop, and performance-constrained contexts fall back to opaque Stable surfaces.

These names record the original 1.6 compatibility mapping. Current 2.2 consumers map the same semantic regions through the current Canvas / Surface / Soft Glaze / Glaze / Deep Glaze / Live Glaze hierarchy and System Glaze budget. Material treatment never upgrades producer-authoritative status or evidence.

## Navigation transformation

Glaze UI does not force one navigation pattern across all device classes. The same semantic destinations transform according to form factor, input, available space, viewing distance, and platform convention:

- **Desktop:** persistent sidebar or rail, toolbar, contextual menus, and optional inspector.
- **Tablet:** adaptive sidebar/rail, split view, collapsible inspector, and touch-first toolbar behavior.
- **Mobile:** single-task navigation, top or bottom navigation, sheets, progressive disclosure, and compact action surfaces.
- **TV:** a distinct far-view workspace with persistent directional-focus navigation, larger targets and chrome, shallow predictable groups, far-view labels, and no pointer/swipe dependency for primary tasks. TV must not inherit the Wide Desktop workspace merely because its viewport is large.

A persistent sidebar may become an overlay drawer, an inspector may become a sheet, and low-priority toolbar actions may move into overflow. These are semantic transformations, not arbitrary rearrangements.

## Responsive workspace behavior

Window width is a layout signal, not a device identity. Form-factor selection also considers primary input, viewing distance, posture, platform convention, resizability, and product task.

Near-view layouts may use Compact, Medium, Expanded, or Wide window behavior while retaining their selected Mobile, Tablet, or Desktop interaction environment. TV remains a separately selected far-view interaction environment.

The workspace must preserve:

- semantic reading order;
- keyboard/focus order;
- current destination;
- action state;
- selection state;
- producer-authoritative system state; and
- meaningful task continuity through layout transformation.

## Input-aware targets

Glaze UI workspace controls use interaction floors appropriate to the active input environment:

- precision pointer: **40 px** minimum when compact density is intentionally selected;
- mixed input: **44 px** minimum;
- coarse pointer/touch: **48 px** minimum;
- TV directional focus: **56 px** minimum.

Visual density may tighten spacing without shrinking the interactive hit region below the applicable floor. Hover is enhancement only and may not be required for primary task completion on touch-capable layouts.

## Density

Workspace density is semantic rather than a global scale transform:

- **comfortable** — default balanced spacing;
- **compact** — denser information and tool presentation where pointer/keyboard use and task complexity justify it;
- **spacious** — increased separation for touch, focus, presentation, or low-density contexts.

Density may alter gaps and padding but must not reduce accessibility, change information meaning, or hide required state.

## Geometry

Window, region, panel, and control geometry follows the Glaze UI nested-radius principle. Child surfaces normally use proportionally smaller radii than their parent workspace region. Expressive geometry remains concentrated in high-value moments rather than applied uniformly.

## Accessibility and resilience

The workspace layer requires:

- visible focus;
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

## Stable implementation

The Stable implementation consists of:

- `tokens/workspace-navigation.candidate.json` — machine-readable semantic contract retained at its historical Candidate-era path for compatibility and audit continuity;
- `css/glaze.workspace.candidate.css` — reusable workspace primitives with Desktop/Tablet/Mobile/Wide Desktop/TV composition, density, input-aware targets, and accessibility/performance fallbacks, retained at its historical path;
- `reference/candidate-1.6-workspace.html` — dependency-free reference composition retained as promotion evidence;
- `reference/candidate-1.6-workspace-acceptance.html` — fail-closed browser-rendered acceptance harness retained as a Stable regression gate;
- `scripts/validate_workspace_navigation.py` — fail-closed Stable source and lifecycle validation;
- `scripts/validate_candidate_1_6_rendered.py` — historical Candidate-named rendered matrix retained as a Stable regression gate;
- `acceptance/1.6-candidate.md` — preserved Candidate lifecycle, scope, evidence, compatibility, and rollback record;
- `acceptance/1.6.0.md` — canonical Stable promotion record; and
- CI coverage in `.github/workflows/ci.yml`.

## Stable rendered acceptance matrix

The Stable workspace is evaluated in light and dark appearances at Mobile `390×844`, Tablet `820×1180`, Desktop `1280×900`, Wide Desktop `1600×1000`, and TV `1920×1080`.

Additional cases cover compact Desktop, spacious Mobile, reduced motion, reduced transparency, constrained-performance material fallbacks, and TV forced colors. The matrix must fail closed on root overflow, missing workspace regions, lost current-destination semantics, undersized targets, incorrect form-factor transformations, TV falling through to Wide Desktop, or missing resilience behavior.

This rendered matrix remains the platform-neutral Stable regression contract only. Platform-native consumers still require their own native/real-device and application-specific acceptance.

## Stable release boundary

Glaze UI 1.6.0 promotion required exact-head CI, rendered acceptance across representative Mobile, Tablet, Desktop, Wide Desktop, and TV contexts, accessibility/resilience review, mixed-input validation, compatibility review, documentation synchronization, and explicit promotion under `STABILITY.md`.

The Glaze UI 1.6 Evidence Presentation and Authority Surfaces contract is also Stable. During promotion, passing the Adaptive Workspace matrix alone did not authorize Stable 1.6 promotion; both 1.6 systems and the retained Stable regression stack were required to pass.

Glaze UI 1.6.0 promotion history remains immutable. Under the current 2.2 release, this workspace contract is retained compatibility semantics and regression evidence; downstream applications must adopt **Glaze UI 2.2.0** and complete their own current rendered/native/real-device acceptance before claiming current Stable conformance.
