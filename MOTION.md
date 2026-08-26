# Glaze UI Motion and Interaction Contract

Status: **Glaze UI 1.5 Stable**

Glaze UI motion exists to explain change, preserve spatial context, confirm interaction, and communicate system state. Motion is never required to understand content, never overrides user accessibility preferences, and never fabricates product, privacy, security, synchronization, or availability truth.

## Principles

1. **Purpose before decoration.** Every animation must support continuity, causality, hierarchy, orientation, confirmation, or state communication.
2. **Interruptible by default.** User-driven transitions must yield immediately to new input. Long blocking sequences are prohibited.
3. **Reduced motion is first-class.** `prefers-reduced-motion`, native reduced-motion settings, and equivalent platform accessibility controls must remove nonessential displacement, scaling, parallax, blur travel, and looping motion.
4. **State remains truthful.** Motion may visualize a supplied state transition but may not imply success, security, privacy, completion, synchronization, or protection before authoritative state exists.
5. **Input-aware behavior.** Touch, pointer, keyboard, remote/D-pad, stylus, and assistive input may use different feedback while preserving the same semantic result.
6. **Performance is part of quality.** Prefer compositor-friendly opacity and transform changes. Avoid motion that causes unnecessary layout, paint, battery, or thermal cost.

## Duration roles

Glaze UI uses semantic duration roles rather than arbitrary milliseconds:

- `instant` — 0 ms. Immediate state changes and reduced-motion substitutions.
- `micro` — 90 ms. Press, hover, focus-ring refinement, icon-state acknowledgement.
- `short` — 160 ms. Small control transitions, disclosure affordances, selection changes.
- `medium` — 240 ms. Standard surface entrance/exit, pane transitions, contextual overlays.
- `long` — 360 ms. Larger spatial transitions where continuity benefits from additional time.
- `ambient` — 700 ms. Rare nonblocking background emphasis only; never required for task comprehension.

Durations are maximum defaults, not minimum waits. Consumers should shorten or eliminate motion when platform conventions, user settings, performance, or interruption require it.

## Easing roles

- `standard` — balanced acceleration/deceleration for ordinary state transitions.
- `enter` — decelerating arrival emphasizing destination stability.
- `exit` — accelerating departure that clears the path quickly.
- `emphasized` — stronger but bounded easing for major spatial continuity.
- `linear` — reserved for continuous progress, timelines, and value movement where constant rate carries meaning.

Spring motion may be used only when platform-native, interruptible, nonessential, and bounded against excessive overshoot. Success, warning, danger, privacy, security, and protection semantics must never be communicated by spring character alone.

## Interaction feedback

### Press and activation

Press feedback should use small opacity, tonal, or scale changes. Scale feedback must remain subtle and must not cause layout movement. Activation feedback must never delay the command itself.

### Hover

Hover is an enhancement, never a requirement. Hover states must not reveal the only path to critical information or controls.

### Keyboard and directional focus

Focus movement must remain visually trackable. TV and remote/D-pad focus may use stronger scale/elevation emphasis than desktop keyboard focus, but motion must stay short, deterministic, and reduced-motion aware.

### Drag and direct manipulation

Dragged content should track input directly. Release animations may settle to a valid destination, but must be interruptible and must not conceal a rejected or invalid drop state.

### Loading and progress

Indeterminate motion is allowed only when the duration is genuinely unknown. Determinate progress must prefer actual progress. Infinite decorative spinners are prohibited when meaningful progress or a static waiting state is available.

### Gesture navigation

Gesture-driven transitions should be progress-linked to the gesture rather than replaying a fixed animation after release. Cancellation must return predictably to the prior state.

## Spatial continuity

Transitions should preserve the perceived origin and destination of surfaces where doing so helps orientation. Shared-axis and container-transform patterns may be used when they remain performant and accessible. Large parallax, forced perspective, simulated depth travel, and camera-like motion are prohibited for routine navigation.

## Material and glass behavior

Glaze UI material motion may animate opacity, bounded blur intensity, tonal separation, and elevation where supported. Blur radius must not sweep aggressively across large surfaces. Clear Glass and Functional Glass must not create continuous shimmering, refraction, or autonomous lens motion.

## Icon motion

Functional and semantic icons may animate between closely related states when the meaning remains recognizable at every frame. Application and service identity marks must not continuously animate in ordinary navigation. Badges may appear/disappear with `micro` or `short` transitions but must not pulse indefinitely for attention.

## Reduced-motion contract

When reduced motion is active:

- spatial translation is removed or reduced to near-zero;
- scale changes used only for decoration are removed;
- parallax and simulated depth are disabled;
- looping decorative animation is stopped;
- blur travel is replaced by immediate or opacity-based state change;
- focus, selection, pressed, loading, and progress states remain perceptible through static visual treatment;
- task completion must never take longer because animation was removed.

Consumers must not invent a separate reduced-motion visual language. The same semantic states remain authoritative.

## Haptics and sound

Haptics and sound are optional platform adapters, not substitutes for visual or accessible state. Haptic feedback should be concise, user-triggered, and aligned with platform conventions. Repetitive, ambient, or attention-demanding haptics are prohibited unless required by a separately governed safety-critical product behavior.

## Motion authority and evidence

Glaze UI owns presentation semantics for motion. Domain systems remain authoritative for their underlying truth:

- Privacy Shield supplies privacy state.
- Wardveil Security supplies security/protection state.
- Everkeep supplies resilience, preservation, backup, and recovery state.
- GoreeCloud Mesh supplies coordination/governance state when implemented and evidenced.

Motion may represent these states only after the authoritative system has supplied them.

## Conformance

A Glaze UI 1.5 Stable consumer satisfies this contract only when it:

- uses semantic duration/easing roles or documented native equivalents;
- honors platform reduced-motion settings;
- keeps required state legible without animation;
- avoids autonomous decorative loops for core UI;
- preserves interruptibility for user-driven transitions;
- avoids false progress or premature success/security/privacy implications;
- validates web implementations against `tokens/motion.json` and `css/glaze.motion.css` where applicable.

This Candidate contract does not change the current Stable target of 1.4.0 until Glaze UI 1.5 is promoted through the existing release process.
