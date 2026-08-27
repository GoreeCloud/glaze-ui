# Glaze Motion

Status: **Experimental foundation (0.1.0)**  
Extends: **Glaze UI 1.5.0 Stable**

Glaze Motion is GoreeCloud's formal motion, animation, transition, spatial-interaction, and interactive-graphics extension of Glaze UI. It does not replace the existing Glaze UI 1.5 Stable motion contract in `MOTION.md`; it builds a richer, separately governed capability layer on top of that Stable baseline.

The architectural relationship is:

`Glaze UI -> Glaze Motion -> Motion Core / Motion Studio / Motion Spatial`

Only **Motion Core** has source implementation in 0.1.0. Motion Studio and Motion Spatial remain Planned and cannot be represented as implemented or Stable capabilities.

## Design rule

Motion must communicate hierarchy, causality, state, continuity, spatial relationship, focus, progress, or identity. It must not exist merely because an interface can be animated.

Application interfaces remain restrained and task-oriented. Product websites may be more expressive. Expensive 3D, simulation, shader, or real-time rendering is reserved for experiences where it adds meaningful value.

## Motion Core — Experimental

Motion Core is the dependency-free baseline for ordinary GoreeCloud application and website interfaces.

0.1.0 introduces:

- semantic duration and easing roles inherited from the Glaze UI 1.5 Stable motion vocabulary;
- reusable restrained, standard, expressive, and spatial spring presets;
- CSS primitives for entrance, exit, state transition, press, lift, progress, and shared-element continuity hooks;
- a dependency-free JavaScript runtime for reduced-motion detection, duration resolution, Web Animations delegation, deterministic spring keyframe generation, capability detection, and spatial-backend fallback selection;
- centralized reduced-motion behavior through `prefers-reduced-motion` and injectable runtime preference resolution;
- a fail-closed validator and Node test suite.

Motion Core must remain interruptible by default. Application state must never depend on an animation finishing. The final semantic state must be valid even when animation is disabled, cancelled, unsupported, or interrupted.

## Motion Studio — Planned

Motion Studio is the intended richer storytelling tier for GoreeCloud product websites, launch pages, onboarding, interactive diagrams, and expressive brand experiences.

Planned capabilities include:

- scroll-driven choreography;
- animated illustrations;
- Rive or equivalent locally controlled vector animation;
- SVG and Canvas animation;
- particle systems;
- bounded parallax and layered depth;
- dimensional responsive cards;
- cinematic page transitions;
- interactive hero sections;
- advanced entrance, reveal, and continuity choreography.

Motion Studio is not implemented by 0.1.0 and is not part of any Stable compatibility promise.

## Motion Spatial — Planned

Motion Spatial is the intended highest-complexity tier for flagship experiences, specialized visualization, simulation, and deliberately immersive interfaces.

Planned capabilities include:

- Three.js experiences;
- WebGL2 rendering;
- WebGPU rendering;
- interactive 3D environments;
- advanced data and mesh visualization;
- interactive product demonstrations;
- real-time graphics and visual effects;
- spatial and simulation-based interfaces.

Motion Spatial must use progressive enhancement. The intended fallback direction is:

`WebGPU -> WebGL2 -> Canvas/SVG/CSS -> static accessible representation`

A lower rendering tier may reduce visual richness, but it must preserve the task, message, critical content, semantic state, and essential relationships.

## Motion tokens

`tokens/glaze-motion.json` is the machine-readable Experimental contract for Glaze Motion 0.1.0.

The initial token groups cover:

- duration roles;
- easing roles;
- spring physics presets;
- movement distances;
- scale feedback;
- runtime invariants;
- reduced-motion behavior;
- performance expectations;
- advanced-rendering fallback order;
- platform truth-authority mapping.

Consumers must use semantic intent rather than inventing arbitrary timing and spring values per component.

## Spring system

The initial spring vocabulary is intentionally bounded:

- `restrained` — compact feedback and calm utility interactions;
- `standard` — ordinary direct manipulation and component transitions;
- `expressive` — higher-value moments where additional physical character improves continuity;
- `spatial` — larger spatial relationships where movement communicates position or depth.

Spring character must never be the sole carrier of success, warning, danger, privacy, security, protection, or recovery meaning. Those truths remain producer-authoritative and must remain perceivable without motion.

## Runtime primitives

`js/glaze.motion.js` provides the initial dependency-free Motion Core runtime.

The 0.1.0 API includes:

- `prefersReducedMotion()`;
- `resolveDuration()`;
- `createSpringKeyframes()`;
- `animate()`;
- `detectCapabilities()`;
- `selectSpatialBackend()`.

The runtime is deliberately small. It does not create a component framework, global animation scheduler, analytics surface, remote dependency, or hidden state system.

## CSS primitives

`css/glaze.motion.core.css` provides reusable web primitives for:

- standard state transitions;
- entrance and exit motion;
- press feedback;
- bounded hover/focus lift;
- shared-element/View Transition naming hooks;
- determinate progress interpolation;
- reduced-motion collapse.

The CSS layer prefers transform and opacity for movement and avoids making animation a prerequisite for layout or semantics.

## Accessibility and reduced motion

Accessibility is part of the architecture, not optional polish.

When `prefers-reduced-motion: reduce` or an equivalent runtime preference is active:

- nonessential translation is removed;
- decorative scaling is removed;
- parallax and large camera-like movement are disabled;
- decorative loops are disabled;
- Motion Core duration roles collapse to zero;
- entrance and exit animation collapse to static final state;
- focus, selection, progress, loading, success, warning, error, privacy, security, and other semantic states remain perceivable without movement;
- removing motion must never delay task completion.

Native adapters must honor equivalent platform accessibility settings.

## Performance and resilience

The lightest technique that communicates the intended relationship should be preferred.

Motion Core targets smooth interaction on representative supported devices and establishes these initial rules:

- prefer compositor-friendly transform and opacity work where appropriate;
- avoid unnecessary layout and paint churn;
- avoid autonomous render loops for ordinary application UI;
- suspend or reduce off-screen work where the platform permits it;
- lazy-load future advanced graphics assets;
- preserve essential content and actions if animation JavaScript or an advanced graphics subsystem fails.

Motion Studio and Motion Spatial will require explicit performance budgets and representative device acceptance before promotion.

## Privacy, security, and authority

Glaze Motion is presentation infrastructure. It does not become authoritative for underlying platform truth.

- Privacy Shield supplies privacy-control truth.
- Wardveil Security supplies security and protection truth.
- Everkeep supplies resilience, preservation, backup, recovery, portability, succession, and digital-legacy truth.
- GoreeCloud Mesh supplies coordination and governance truth when implemented and evidenced.
- Product/application logic supplies domain-specific workflow, progress, availability, and validation truth.

Motion may present those states only after the authoritative producer supplies them. It must never animate success, protection, synchronization, recovery, or completion prematurely.

Glaze Motion must not introduce analytics, tracking, advertising technology, third-party runtime font/icon delivery, or unnecessary remote animation dependencies.

## Lifecycle and promotion

Glaze Motion 0.1.0 is **Experimental**. It is intentionally outside the Glaze UI 1.5.0 Stable compatibility promise and must not become a mandatory production dependency.

Promotion requires, as applicable:

- documented semantic contracts;
- stable token/API design;
- accessibility and reduced-motion acceptance;
- resilience and fallback validation;
- representative rendered acceptance;
- performance evidence;
- compatibility and migration review;
- dependency/security/licensing review for future Studio/Spatial libraries;
- explicit lifecycle promotion under normal Glaze UI governance.

Development must proceed from Motion Core outward. Motion Studio should be implemented only after the Core contract is useful and stable enough to support it. Motion Spatial should be introduced selectively and must never become a universal rendering requirement for GoreeCloud applications.
