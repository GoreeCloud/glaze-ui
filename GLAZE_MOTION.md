# Glaze Motion

Status: **Experimental foundation (0.2.0)**  
Extends: **Glaze UI 1.5.0 Stable**

Glaze Motion is GoreeCloud's formal motion, animation, transition, spatial-interaction, and interactive-graphics extension of Glaze UI. It does not replace the existing Glaze UI 1.5 Stable motion contract in `MOTION.md`; it builds a richer, separately governed capability layer on top of that Stable baseline.

`Glaze UI -> Glaze Motion -> Motion Core / Motion Studio / Motion Spatial`

Only **Motion Core** has source implementation in 0.2.0. Motion Studio and Motion Spatial remain Planned and cannot be represented as implemented, Stable, or mandatory production dependencies.

## Design rule
Motion must communicate hierarchy, causality, state, continuity, spatial relationship, focus, progress, or identity. It must not exist merely because an interface can be animated.

## Motion Core — Experimental
0.2.0 retains the 0.1 semantic durations, easing, bounded springs, entrance/exit primitives, reduced-motion behavior, capability detection, and rendering fallbacks, and adds direct-manipulation gesture sessions, deterministic velocity-projected snapping, CSS drag hooks, shared-element/View Transition fallback, semantic component adapters, runtime-bounded spring output, dedicated interaction tests, and dependency-free rendered acceptance.

Motion Core remains interruptible by default. Application state must never depend on an animation finishing.

## Direct manipulation
Direct manipulation is input tracking, not decorative animation. Reduced-motion mode must not make drag, resize, pan, reorder, or similar controls detach from active input. Tracking remains immediate; nonessential post-gesture inertia, spring travel, and settling collapse under reduced motion.

The runtime provides `createDragSession()`, `resolveSnapPoint()`, and `applyDragPosition()` while application logic remains authoritative for ordering, commands, permissions, and domain state.

## Shared-element transitions
Shared-element transitions preserve identity and spatial continuity. 0.2 provides `createSharedElementName()`, `setSharedElementName()`, and `startSharedTransition()`. Stable shared keys are required. When View Transitions are unsupported or reduced motion is active, the state update still executes immediately.

## Component adapters
Component adapters translate common GoreeCloud roles into semantic motion without creating a component framework. Initial roles are button, disclosure, dialog, navigation, reorder, and shared. `createMotionAdapter()` resolves semantic duration/easing/spring values and collapses timing under reduced motion; CSS hooks use `data-glaze-motion-role`.

## Motion Studio — Planned
Motion Studio remains the planned richer storytelling tier for product websites, onboarding, interactive diagrams, Rive/SVG/Canvas animation, bounded particles/parallax, dimensional cards, cinematic transitions, interactive heroes, and advanced reveal choreography. It is not implemented by 0.2.0.

## Motion Spatial — Planned
Motion Spatial remains the planned advanced tier for Three.js, WebGL2, WebGPU, interactive 3D, data/mesh visualization, product demonstrations, real-time graphics, and simulation. Progressive fallback remains `WebGPU -> WebGL2 -> Canvas/SVG/CSS -> static accessible representation`.

## Motion tokens
`tokens/glaze-motion.json` is the machine-readable Experimental 0.2 contract covering durations/easing, bounded springs, gestures, shared elements, component adapters, reduced motion, performance, rendered acceptance, fallbacks, and truth-authority mapping.

## Runtime API
`js/glaze.motion.js` includes `prefersReducedMotion()`, `resolveDuration()`, `createSpringKeyframes()`, `animate()`, `createDragSession()`, `resolveSnapPoint()`, `createMotionAdapter()`, `createSharedElementName()`, `setSharedElementName()`, `startSharedTransition()`, `applyDragPosition()`, `detectCapabilities()`, and `selectSpatialBackend()`.

## Accessibility and reduced motion
Reduced motion removes decorative translation/scaling, parallax, loops, camera-like travel, and post-gesture settling; durations collapse to zero; direct manipulation still tracks input; semantic state remains perceivable; task completion must not be delayed.

## Performance and resilience
Motion Core targets 60 fps with a nominal 16.67 ms frame budget and 50 ms long-task boundary. It prefers transform/opacity, avoids persistent `will-change` and autonomous loops, bounds concurrent settling work, and preserves essential content/actions when animation support fails.

## Privacy, security, and authority
Glaze Motion is presentation infrastructure. Privacy Shield supplies privacy truth; Wardveil Security supplies security/protection truth; Everkeep supplies resilience/backup/recovery/preservation truth; GoreeCloud Mesh supplies coordination/governance truth; product logic supplies workflow/ordering/progress truth. Motion must never invent or prematurely animate those states.

## Validation and promotion
Glaze Motion 0.2.0 remains **Experimental** and outside Glaze UI 1.5.0 Stable. Source validation, 14 runtime/interaction tests, and a dedicated rendered harness provide development evidence only. Candidate or Stable promotion still requires representative consumer, accessibility, performance, compatibility/migration, dependency/security/licensing, and normal Glaze UI promotion evidence.
