# Glaze Motion

Status: **Experimental foundation (0.3.0)**  
Extends: **Glaze UI 1.5.0 Stable**

Glaze Motion is GoreeCloud's formal motion, animation, transition, spatial-interaction, and interactive-graphics extension of Glaze UI. It does not replace the existing Glaze UI 1.5 Stable motion contract in `MOTION.md`; it builds a richer, separately governed capability layer on top of that Stable baseline.

`Glaze UI -> Glaze Motion -> Motion Core / Motion Studio / Motion Spatial`

Only **Motion Core** has source implementation in 0.3.0. Motion Studio and Motion Spatial remain Planned and cannot be represented as implemented, Stable, or mandatory production dependencies.

## Design rule
Motion must communicate hierarchy, causality, state, continuity, spatial relationship, focus, progress, or identity. It must not exist merely because an interface can be animated.

## Motion Core — Experimental
0.3.0 retains the 0.2 semantic timing, bounded springs, direct-manipulation sessions, velocity-projected snapping, shared-element/View Transition fallback, component adapters, reduced-motion behavior, rendered acceptance, and capability fallbacks. It adds accessible reorder/swipe/pan/zoom state primitives, directional keyboard/remote mapping, local-only performance instrumentation, native mapping guidance, and a representative reference-consumer evidence harness.

Motion Core remains interruptible by default. Application state must never depend on an animation finishing.

## Direct manipulation and accessible gestures
Direct manipulation is input tracking, not decorative animation. Reduced-motion mode must not detach drag, resize, pan, reorder, or similar controls from active input. Tracking remains immediate while nonessential post-gesture inertia and settling collapse.

`createReorderModel()` requires stable unique item keys and exposes deterministic move operations independent of pointer animation. `resolveDirectionalMove()` maps keyboard or directional-remote input into the same semantic move result. `resolveSwipeAction()` returns semantic start/end/none results based on bounded distance/velocity thresholds. `createPanZoomState()` provides clamped pan/zoom state while leaving application commands and permissions authoritative.

Task-critical gesture actions require non-gesture alternatives when the platform supports them. Cancellation must always leave valid application state.

## Shared-element transitions
`createSharedElementName()`, `setSharedElementName()`, and `startSharedTransition()` preserve identity and continuity. Stable keys are required. When View Transitions are unsupported or reduced motion is active, the state update still executes immediately.

## Component adapters
Button, disclosure, dialog, navigation, reorder, and shared-element roles map to semantic duration/easing/spring values through `createMotionAdapter()`. Reduced motion collapses timing without removing state changes.

## Performance instrumentation
`createFrameBudgetProbe()` records frame intervals and long-task durations for local validation. It has no network reporting, analytics, persistence, or authority role. Its output is evidence for development and acceptance only; it does not itself prove that an application meets a performance target.

## Native mappings
`NATIVE_MOTION_MAPPINGS.md` defines semantic parity requirements for web, mobile/tablet native, desktop native, and TV native adapters. Native implementations may use platform-specific primitives but must preserve duration/spring intent, direct manipulation, cancellation, reduced-motion behavior, focus/input semantics, and producer truth boundaries.

## Reference consumer evidence
`reference/glaze-motion-consumer.mjs` is a dependency-free representative consumer harness for reorder, shared-transition fallback, and local performance evidence. It is design-system evidence only. It does not certify any GoreeCloud production application.

The current consumer registry marks listed downstream apps as migration-required to Glaze UI 1.5 Stable, so 0.3 does not introduce Experimental Motion as a mandatory dependency in those consumers.

## Motion Studio — Planned
Motion Studio remains the planned richer storytelling tier for product websites, onboarding, interactive diagrams, Rive/SVG/Canvas animation, bounded particles/parallax, dimensional cards, cinematic transitions, interactive heroes, and advanced reveal choreography. It is not implemented by 0.3.0.

## Motion Spatial — Planned
Motion Spatial remains the planned advanced tier for Three.js, WebGL2, WebGPU, interactive 3D, data/mesh visualization, product demonstrations, real-time graphics, and simulation. Progressive fallback remains `WebGPU -> WebGL2 -> Canvas/SVG/CSS -> static accessible representation`.

## Motion tokens
`tokens/glaze-motion.json` is the machine-readable Experimental 0.3 contract covering timing, springs, gestures, accessible interaction, shared elements, component adapters, reduced motion, performance instrumentation, native mappings, consumer evidence, rendered acceptance, fallbacks, and truth-authority mapping.

## Runtime API
`js/glaze.motion.js` includes the 0.2 APIs plus `resolveSwipeAction()`, `resolveDirectionalMove()`, `createReorderModel()`, `createPanZoomState()`, and `createFrameBudgetProbe()`.

## Accessibility and reduced motion
Reduced motion removes decorative translation/scaling, parallax, loops, camera-like travel, and post-gesture settling; durations collapse to zero; direct manipulation still tracks input; semantic state remains perceivable; keyboard/remote alternatives remain available; task completion must not be delayed.

## Performance and resilience
Motion Core targets 60 fps with a nominal 16.67 ms frame budget and 50 ms long-task boundary. It prefers transform/opacity, avoids persistent `will-change` and autonomous loops, bounds concurrent settling work, and preserves essential content/actions when animation support fails. Performance probes are local-only and never introduce telemetry.

## Privacy, security, and authority
Glaze Motion is presentation infrastructure. Privacy Shield supplies privacy truth; Wardveil Security supplies security/protection truth; Everkeep supplies resilience/backup/recovery/preservation truth; GoreeCloud Mesh supplies coordination/governance truth; product logic supplies workflow/ordering/progress truth. Motion must never invent or prematurely animate those states.

## Validation and promotion
Glaze Motion 0.3.0 remains **Experimental** and outside Glaze UI 1.5.0 Stable. Source validation, runtime/interaction/reference-consumer tests, native mapping documentation, local performance instrumentation, and retained rendered acceptance provide development evidence only. Candidate or Stable promotion still requires conformant representative downstream consumer evidence, applicable native/real-device evidence, accessibility and performance acceptance, compatibility/migration review, dependency/security/licensing review, and normal Glaze UI promotion governance.
