# Glaze UI Wearable Form-Factor Candidate Contract

Status: **Development Candidate**

Tracking issue: #58

This document defines the initial smartwatch and wearable interaction contract being developed after Glaze UI 1.4.0 Stable. It does **not** modify the current Stable Glaze UI contract and does not authorize any wearable production-conformance claim. A wearable application remains production-blocked until a later Glaze UI release explicitly promotes an applicable wearable contract to Stable and the consuming application completes native and real-device acceptance.

## Role

Wearable UI is **glance-first, near-view, short-session, touch-capable, and platform-native**. It is not a small Mobile composition.

The primary job of a wearable surface is to reveal the most relevant state or action quickly, let the user complete a bounded task with minimal navigation, and return control to the operating system without requiring prolonged attention.

## Shared Glaze UI semantics

A wearable implementation must preserve the applicable Glaze UI semantic roles for color, material, shape, typography, state, motion, accessibility, privacy-conscious presentation, resilience, product identity, and truthful Wardveil Security, Privacy Shield, and Everkeep status presentation.

Native controls and platform interaction systems may map these semantics where native behavior provides stronger ergonomics, accessibility, battery behavior, or operating-system integration. Native mapping is not an exception to Glaze UI.

## Composition

- Prefer one dominant status, task, or action at a time.
- Keep information hierarchy shallow and immediately scannable.
- Favor short labels, concise values, symbols with accessible names, and progressive disclosure.
- Avoid dense dashboards, multi-pane layouts, desktop tables, persistent sidebars, and phone-style navigation shells.
- Preserve safe spacing around round-screen edges, curved corners, system indicators, bezels, and platform reserved regions.
- Design layouts to remain valid on both round and rectangular watch displays where the target platform permits both.
- Keep critical actions reachable without requiring precision pointing.

## Navigation and information flow

- Prefer vertical scrolling and vertically ordered task flows as the default model.
- Keep navigation depth low; a user should not need to traverse long nested hierarchies for routine tasks.
- Use platform-native back, dismiss, edge-swipe, crown, bezel, or system navigation behavior where applicable.
- Preserve task state across interruption, dismissal, screen sleep, and foreground/background transitions when the platform supports restoration.
- Do not require horizontal paging for essential actions unless the target platform convention makes the relationship explicit and accessible.

## Touch targets

Wearable controls must use platform-appropriate touch targets. For Wear OS, Glaze UI adopts a **48 × 48 dp minimum actionable target** as the candidate baseline. Other platforms must meet or exceed their native accessibility and interaction requirements rather than forcing a single physical-size assumption across ecosystems.

Visual glyphs may be smaller than the interactive target, but hit regions must remain separated enough to avoid accidental activation.

## Rotary and crown input

Rotary input is a first-class enhancement where the device exposes a crown, rotating side button, physical bezel, or touch bezel.

- Essential interactions must remain available through touch or another native equivalent unless the operating system itself defines a rotary-only interaction.
- Rotary input should primarily scroll vertical content, move through bounded selections, or adjust values.
- Scrolling or selection changes should provide clear visual feedback and use native haptics where the platform provides them automatically.
- Do not overload rotary input with surprising app-specific commands that conflict with platform navigation expectations.

## Glanceable surfaces

Complications, widgets, tiles, always-on surfaces, and similar system-hosted wearable surfaces are **constrained presentation surfaces**, not miniature copies of the full app.

- Show only the most important current value, state, progress, or action supported by the host surface.
- Follow host-platform template, refresh, privacy, battery, and interaction limits.
- Keep data accurate enough that the surface does not overstate freshness or security state.
- Treat tap-through behavior as an entry into a focused app task rather than a generic app launch when the platform supports deep linking.

## Always-on and ambient presentation

Where the operating system provides always-on or ambient modes:

- reduce visual complexity, motion, brightness demand, and nonessential decoration;
- preserve the information the user most needs at a glance;
- avoid implying live or continuously refreshed data when the platform has reduced update frequency;
- remain readable with reduced color or luminance when the platform applies power-saving presentation changes.

## Accessibility and resilience

Wearable acceptance must include, where applicable:

- user-selected larger text without clipping or overlapping controls;
- screen-reader or spoken accessibility semantics;
- sufficient touch-target size and spacing;
- visible focus/selection for non-touch input;
- increased-contrast and forced/high-contrast equivalents;
- reduced-motion behavior;
- reduced-transparency or solid-surface fallback;
- orientation, round/rectangular display, and text-scaling stress cases;
- equivalent task completion when optional rotary input is unavailable.

## Motion and materials

- Use motion sparingly because wearable sessions are short and the display is small.
- Prefer system navigation and transition motion over custom decorative choreography.
- Functional Glass may be used only when it improves hierarchy and remains readable; Solid or Raised fallbacks remain mandatory.
- Clear Glass must not reduce text or control legibility on small or always-on displays.
- Reduced-motion mode removes nonessential transforms while preserving clear state changes.

## Privacy, security, and resilience presentation

Wearable surfaces are frequently visible in public or shared physical environments.

- Avoid exposing sensitive content on glanceable or always-on surfaces unless the user and platform context explicitly allow it.
- Respect platform notification/privacy redaction behavior.
- Do not display detailed security, privacy, backup, recovery, or credential state merely because space is available; show only task-relevant, evidence-backed state.
- Wardveil Security, Privacy Shield, and Everkeep presentation must never strengthen claims beyond available evidence.

## Anti-patterns

Reject:

- a Mobile screen scaled down to watch dimensions;
- dense cards or tables requiring prolonged reading;
- tiny adjacent controls;
- essential hover, pointer, or drag-only interactions;
- nested hamburger/drawer navigation copied from phones;
- edge-to-edge critical controls that ignore round screens or curved corners;
- decorative animation that delays task completion;
- long text-entry workflows when a companion-device or system-native alternative exists;
- assuming every watch has a crown or rotary input;
- treating complications, widgets, tiles, or always-on surfaces as unrestricted app canvases.

## Candidate acceptance direction

A future Stable wearable contract must include representative native and real-device acceptance for every supported wearable target. Source inspection or browser rendering alone is insufficient.

At minimum, promotion evidence should cover:

- compact round watch display;
- compact rectangular watch display where supported;
- touch-only task completion;
- rotary/crown-enhanced navigation where supported;
- large-text accessibility;
- reduced-motion behavior;
- reduced-transparency/solid fallback;
- glanceable system-hosted surface behavior where the product exposes one;
- representative interruption and state-restoration behavior;
- platform-native back/dismiss behavior;
- real-device validation for target platforms before application production approval.

## Current boundary

Glaze UI 1.4.0 remains the current Stable baseline. This candidate document is development work toward a later release and must not be consumed as Stable behavior. GoreeCloud applications targeting smartwatch or wearable platforms remain development-only unless and until an applicable wearable Glaze UI contract is promoted to Stable and the application itself completes current-version conformance and native acceptance.
