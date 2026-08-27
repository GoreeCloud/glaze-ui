# Glaze Motion Native Mapping Guidance

Status: **Experimental — Motion Core 0.6.0**  
Extends: **Glaze UI 1.5.0 Stable**  
Runtime implementation baseline: **0.4.0**

This document defines semantic mapping requirements for native Glaze Motion adapters. It does not make any downstream application conformant by itself and does not promote Glaze Motion beyond Experimental.

## Mapping rule

Native adapters preserve Glaze Motion intent rather than reproducing web implementation details. Duration roles, bounded spring character, direct-manipulation semantics, cancellation, state integrity, accessibility preferences, and truth-authority boundaries must survive the mapping even when a platform uses different animation or gesture primitives.

## Web

- Use platform animation primitives for ordinary Core motion; current Glaze Motion web runtime uses Web Animations where explicitly invoked.
- Use View Transitions only as progressive enhancement; unsupported and reduced-motion paths must apply state immediately.
- Direct manipulation tracks pointer/touch input without waiting for animation.
- Keyboard and assistive alternatives produce the same semantic reorder/navigation result.
- Accessible reorder adapters consume semantic position metadata and localize user-facing announcements in the consumer; Glaze Motion does not hard-code English announcement copy.

## Mobile and tablet native

- Map direct manipulation to the platform's native gesture/input system and preserve immediate tracking.
- Map semantic duration and spring roles to platform-native animation primitives without exceeding Glaze Motion overshoot or settling intent.
- Honor the operating system's reduced-motion or equivalent accessibility preference.
- Reorder, swipe, pan, and zoom actions that affect task state require non-gesture alternatives when the action would otherwise be inaccessible.
- Directional and edge reorder commands map to native accessibility or keyboard actions where supported, while preserving semantic position metadata for localized feedback.
- Press-state or key-state animation must not become the semantic input source; the platform interaction event remains authoritative.
- Cancellation must leave application state valid and must not depend on a completion callback from an animation.

## Desktop native

- Pointer drag and resize remain direct manipulation; keyboard equivalents are first-class where the task can be expressed directionally.
- Window, pane, dialog, and navigation transitions use semantic Glaze Motion roles rather than arbitrary per-surface timing.
- Focus order and keyboard operation remain stable during transitions.
- Reduced motion removes nonessential travel and settling without removing state changes or task completion.

## TV native

- Directional input is a primary interaction model, not a fallback.
- Focus movement must stay bounded, readable at far-view distance, and semantically distinct from selection/activation.
- Reorder or navigation models map directional commands to the same semantic result as pointer/touch manipulation where both exist.
- Reduced motion replaces spatial travel with stable focus/state cues while preserving immediate response to remote input.
- Web/reference TV viewport acceptance is not native TV, hardware-remote, or real-device certification.

## First-party native evaluation evidence

Glaze Motion 0.6 records two merged native-platform consumer evaluations while keeping both consumers production-isolated from Experimental Motion.

### GoreeCloud Launcher

Launcher PR #22 was validated at exact head `3095b9320b660f5e166465990d5d2bee061d7422`, passed Android CI #67, and merged as `23a389b3b24db726ceab5e328f9f8157fa7655ae`.

The Android evaluation is deliberately **test-only**. It maps semantic reorder commands and optional-settling decisions onto Launcher's real workspace ordering domain, verifies stable-key failure behavior and localization-neutral position metadata, and is guarded against entering production sources.

### GoreeCloud Keyboard

Keyboard PR #4 was validated at exact head `80de7bd2dcff6d07b06b19f8250e37d20155d7ff`, passed Android CI #15, and merged as `c9c0500263b40640339cf7a46f1a029d9a2ac240`.

The Android 15 / API 35 x86_64 emulator evaluation is also **test-only**. It maps 0.5 timing, press-scale, optional-settling, and reduced-motion semantics onto the real native `KeyboardView` interaction surface. It verifies that key press-down does not commit semantic input, key release commits the real key exactly once, suggestion selection uses actual hit-testing, Android's animator duration scale is disabled, and optional settling collapses under the mapped reduced-motion state.

The first Keyboard emulator run exposed a brittle `ValueAnimator.areAnimatorsEnabled()` assumption. The test was corrected to read the authoritative Android global animator-duration setting without removing the emulator gate or weakening the semantic assertions.

Both repositories target Glaze UI 1.5.0 as Adoption Candidates and remain production-ineligible while final native/rendered/accessibility/physical-device acceptance is incomplete. These evaluations are useful semantic-parity evidence but are **not** native Glaze Motion certification, physical-device acceptance, or production activation.

A native adapter intended for production must go beyond this test-only evidence and integrate the applicable operating-system motion accessibility preference, localized assistive feedback, rendered behavior, representative-device performance, and application-specific acceptance.

## Performance evidence

Native adapters must collect performance evidence locally during validation. Glaze Motion retains the local-only frame-budget probe and local settling-animation budget that can reject nonessential settling under reduced motion or saturation without blocking semantic state updates. Neither mechanism uploads analytics or becomes a telemetry subsystem.

The Launcher and Keyboard evaluations do not provide Motion-specific representative physical-device frame pacing, input latency, power, thermal, or settling-workload acceptance. Candidate promotion still requires representative platform evidence for frame pacing, input latency, long-task/main-thread pressure where applicable, power/resource behavior, and settling workloads.

## Authority boundary

Native motion never becomes authoritative for privacy, security, resilience, coordination, workflow completion, text input, workspace ordering, or other producer-owned truth. It may render a state only after the relevant authoritative producer supplies that state.
