# Glaze UI Wearable Form-Factor Candidate Contract

Status: **Development Candidate**  
Tracking issue: #58  
Current Stable remains: **Glaze UI 1.4.0**

This contract develops first-class smartwatch and wearable support without changing the current Stable Glaze UI release. It cannot satisfy a production conformance claim until a later release explicitly promotes a wearable contract to Stable and each consuming application completes native and real-device acceptance.

## Role

Wearable UI is glance-first, near-view, short-session, touch-capable, interruption-tolerant, and platform-native. It is not a shrunken phone UI.

## Composition

- Present one dominant status, task, or action at a time.
- Keep hierarchy shallow and labels concise.
- Prefer vertically ordered flows and progressive disclosure.
- Avoid dense dashboards, multi-pane layouts, desktop tables, persistent sidebars, and phone navigation shells.
- Preserve safe regions around round edges, curved corners, bezels, system indicators, and platform-reserved areas.
- Support round and rectangular displays where the target platform exposes both.
- Keep critical controls reachable without precision pointing.

## Candidate semantic tokens

Wearable-specific candidate tokens live in `tokens/wearable.candidate.tokens.json`. They are additive candidate semantics and do not modify Stable `tokens/glaze.tokens.json`.

The candidate defines:

- a 48 dp Wear OS minimum actionable target baseline;
- compact content-edge and control-gap spacing;
- short-session motion limits;
- safe-edge inset roles for constrained displays;
- glance, task, complication/tile/widget, and ambient surface roles;
- rotary/crown focus and selection semantics;
- reduced-motion and reduced-transparency requirements.

Native platform requirements override candidate numeric values when the platform requires a larger or otherwise safer value.

## Navigation and input

- Vertical scrolling is the default information-flow model.
- Navigation depth must remain low for routine tasks.
- Use platform-native back, dismiss, edge-swipe, crown, bezel, or system navigation behavior where applicable.
- Preserve task state across interruption, dismissal, screen sleep, and foreground/background transitions when supported.
- Rotary/crown input is a first-class enhancement, not a mandatory dependency.
- Essential tasks must remain available through touch or another native equivalent unless the operating system itself defines a rotary-only interaction.

## Glanceable surfaces

Complications, tiles, widgets, live activities, always-on surfaces, and similar system-hosted surfaces are constrained presentation surfaces, not miniature copies of the application.

They must:

- show only the most important current value, state, progress, or action;
- follow host refresh, privacy, battery, and interaction limits;
- avoid overstating freshness;
- deep-link into a focused task when the platform permits it;
- avoid exposing sensitive content when lock/privacy context does not support it.

## Accessibility and resilience

Candidate acceptance must cover, where applicable:

- larger text without clipping or overlap;
- screen-reader/spoken semantics;
- sufficient target size and spacing;
- visible non-touch focus/selection;
- increased/high contrast equivalents;
- reduced motion;
- reduced transparency and solid-surface fallback;
- round and rectangular display stress cases;
- equivalent task completion without optional rotary input.

## Motion and materials

Wearable motion must be brief, purposeful, and subordinate to task completion. System transitions are preferred over decorative choreography. Functional Glass may be used only when it improves hierarchy and retains legibility; Solid or Raised fallback remains mandatory. Ambient/always-on presentation must reduce nonessential motion, luminance demand, and decoration.

## Privacy, Wardveil Security, Privacy Shield, and Everkeep

Wearables are often visible in shared physical environments. Glaze UI presentation must not expose sensitive state unnecessarily and must never strengthen security, privacy, backup, recovery, or resilience claims beyond evidence available from the underlying platform capability.

## Prohibited wearable patterns

- Scaling a Mobile composition down to watch dimensions.
- Tiny adjacent controls.
- Essential hover, pointer, or drag-only interaction.
- Phone drawer/hamburger navigation copied onto a watch.
- Edge-to-edge critical controls that ignore round displays.
- Decorative motion that delays task completion.
- Long text-entry workflows where a platform-native or companion-device alternative is appropriate.
- Assuming every wearable has a crown or rotary input.
- Treating complications, widgets, tiles, or ambient surfaces as unrestricted canvases.

## Candidate acceptance matrix

A future Stable wearable contract must record representative acceptance for:

1. Compact round display.
2. Compact rectangular display where supported.
3. Touch-only task completion.
4. Rotary/crown-enhanced navigation where supported.
5. Large-text accessibility.
6. Reduced-motion behavior.
7. Reduced-transparency/solid fallback.
8. Glanceable system-hosted surfaces where exposed.
9. Interruption and task-state restoration.
10. Platform-native back/dismiss behavior.
11. Native platform rendering.
12. Real-device validation before application production approval.

## Validation boundary

`scripts/validate_wearables.py` validates the candidate source contract, token file, lifecycle boundary, and required acceptance language. Passing this validator proves repository consistency only. It is not native acceptance, real-device acceptance, Stable promotion, or production approval.
