# Glaze Motion Native Mapping Guidance

Status: **Experimental — Motion Core 0.4.0**  
Extends: **Glaze UI 1.5.0 Stable**

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

## Performance evidence

Native adapters must collect performance evidence locally during validation. Glaze Motion 0.4 retains the local-only frame-budget probe and adds a local settling-animation budget that can reject nonessential settling under reduced motion or saturation without blocking semantic state updates. Neither mechanism uploads analytics or becomes a telemetry subsystem. Candidate promotion requires representative platform evidence for frame pacing, input latency, long-task/main-thread pressure where applicable, and settling workloads.

## Authority boundary

Native motion never becomes authoritative for privacy, security, resilience, coordination, workflow completion, or other producer-owned truth. It may render a state only after the relevant authoritative producer supplies that state.
