# Glaze UI Component Lifecycle

This record defines the lifecycle status of canonical Glaze UI foundations and components. The status is release-governance metadata, not a visual-quality score.

## Lifecycle definitions

### Stable

A Stable foundation or component has a documented semantic contract, representative canonical implementation or native mapping guidance, accessibility and resilience requirements, and validation coverage appropriate to its role. Stable items may be used by production GoreeCloud applications subject to application-specific acceptance.

### Candidate

A Candidate item is implemented and under formal validation but is not yet part of the Stable compatibility promise. Candidate items must not be treated as required Stable consumer behavior unless the consuming application explicitly adopts the candidate and records that boundary.

### Experimental

An Experimental item is exploratory. Its API, semantics, appearance, or implementation may change substantially. Experimental items are not permitted as mandatory dependencies for Stable GoreeCloud application releases.

### Planned

A Planned item is documented direction only. It is not an implemented Glaze UI capability and must not be represented as available.

## Glaze UI 1.3 Stable foundations

| Area | Status | Stable contract |
| --- | --- | --- |
| Semantic color system | Stable | Light/dark Canvas, surface, text, line, accent, status, focus, selection, scrim, and on-accent roles. |
| Surface hierarchy | Stable | Canvas, Solid, Raised, Glaze/Functional Glass, Overlay, with Clear Glass restricted to rich-media control contexts. |
| Typography hierarchy | Stable | Readable body/supporting roles plus bounded hero/display emphasis. |
| Spacing and adaptive gutters | Stable | Semantic spacing and Compact/Medium/Expanded/Wide gutter behavior. |
| Shape system | Stable | Compact, Standard, Expressive, Hero, and Pressed roles. |
| Motion system | Stable | Effects/spatial motion separation with bounded expressive motion and reduced-motion removal. |
| Interaction state layers | Stable | Hover, pressed, focus, and selected semantic feedback. |
| Focus and target sizing | Stable | Visible semantic focus and 44px minimum actionable target where platform behavior permits. |
| Accessibility/resilience layer | Stable | Reduced motion, reduced transparency where supported, increased contrast, forced colors, and no-backdrop-filter solid fallbacks. |
| Safe-area semantics | Stable | Additive safe-area handling for web and platform-native equivalents. |
| Privacy presentation boundary | Stable | No unnecessary remote presentation dependencies, analytics, or tracking. |
| Product personality contract | Stable | Shared family resemblance without forcing identical product composition. |

## Glaze UI 1.3 Stable components and patterns

| Component or pattern | Status | Notes |
| --- | --- | --- |
| Primary/secondary/destructive buttons | Stable | Includes loading, focus, state-layer, and target-size requirements. |
| Icon buttons | Stable | Accessible name required; compact geometry with practical target sizing. |
| Text fields, search, textarea, select | Stable | Persistent labels and programmatic help/error relationships where supported. |
| Checkbox and radio mapping | Stable | Native controls preferred when they satisfy the product need. |
| Switch | Stable | Immediate binary settings only; checked state must be programmatic. |
| Segmented controls and tabs | Stable | Selected state and appropriate keyboard semantics required. |
| Progress | Stable | Determinate value semantics where applicable. |
| Banners and in-context feedback | Stable | Textual meaning cannot rely on color alone. |
| Toasts, badges, status indicators | Stable | Accessible announcements required when state changes warrant them. |
| Cards and panels | Stable | Material role must be intentional; glass is not the default card style. |
| Expressive tiles | Stable | Stronger geometry reserved for meaningful emphasis. |
| Navigation and toolbars | Stable | Current location semantics, adaptive transformation, and target sizing required. |
| Dialogs, menus, sheets, overlays, scrims | Stable | Programmatic name, focus lifecycle, viewport bounds, safe-area and solid-fallback requirements. |
| Tables and dense-data adaptation | Stable | Scanability and accessible headers; Compact may transform to list/card presentation. |
| Adaptive action groups | Stable | Visual emphasis may change allocation but not semantic or focus order. |
| Compact reachability composition | Stable | Visual placement may improve one-handed access without document-order mutation. |
| Hero typography | Stable | Must remain readable under reflow, scaling, and localization pressure. |

## Candidate form-factor layer

The following belong to Glaze UI 1.4.0 Candidate and are not part of the 1.3 Stable compatibility promise:

| Area | Status | Candidate scope |
| --- | --- | --- |
| Mobile semantic composition | Candidate | Touch/reachability-first shell and navigation rules. |
| Tablet semantic composition | Candidate | Pane/posture-aware layouts and optional pointer/keyboard/stylus enhancement. |
| Desktop semantic composition | Candidate | Workspace-first resizable layout and pointer/keyboard semantics. |
| TV semantic composition | Candidate | Far-viewing, directional-focus, overscan-safe, remote/D-pad experience. |
| TV focus primitives | Candidate | Focus/selection distinction, directional navigation, reduced-motion and forced-colors fallback. |
| Form-factor token roles | Candidate | Viewing distance, input, navigation model, density, composition, and anti-pattern metadata. |

Candidate source may be reviewed and tested without changing the Stable status of 1.3 consumers.

## Experimental and roadmap boundary

The following are not part of the current Stable or Candidate source contract unless separately implemented and versioned in the future:

- Glaze Intelligence Layer;
- Glaze Agents;
- Glaze Memory;
- Glaze Automation Engine;
- ambient-computing/device-continuity concepts;
- Glaze Voice;
- Glaze operating-experience or app-store concepts;
- other speculative 1.7, 1.8, or 2.0 roadmap ideas.

These are **Planned/roadmap concepts**, not shipping components.

## Promotion requirements

A Candidate component or foundation becomes Stable only when:

1. its semantics are documented;
2. its implementation or platform mapping is present;
3. accessibility/resilience requirements are defined;
4. source validation covers durable invariants;
5. rendered/native acceptance covers the behavior required by its scope;
6. compatibility and migration impact are recorded;
7. the release containing it passes the Stable promotion gate in `STABILITY.md`.

## Deprecation requirements

A Stable component or semantic role may not disappear silently. Deprecation requires:

- a documented reason;
- a replacement or approved removal path;
- affected consumer guidance;
- a minimum compatibility period appropriate to the impact;
- validator and documentation updates;
- a major version when removal is breaking.
