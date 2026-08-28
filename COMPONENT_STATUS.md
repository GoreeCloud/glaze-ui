# Glaze UI Component Lifecycle

This record defines lifecycle status for canonical Glaze UI capabilities.

## Lifecycle definitions

### Stable
Documented, validated capabilities included in the current compatibility promise.

### Candidate
Implemented capabilities still under formal promotion review.

### Experimental
Exploratory capabilities that may change substantially and cannot be mandatory Stable dependencies.

### Planned
Roadmap direction only; not implemented shipping functionality.

## Glaze UI 1.3 Stable foundations
The 1.3 semantic color, surface, typography, spacing, shape, effects/spatial motion, state-layer, focus/target, accessibility/resilience, safe-area, privacy, product-personality, core controls, Functional Glass, Clear Glass, adaptive action groups, reachability, and hero-typography contracts remain retained Stable history and compatibility regression evidence.

## Glaze UI 1.4 Stable form-factor layer
| Area | Status | Retained contract |
| --- | --- | --- |
| Mobile semantic composition | Stable | Touch/reachability-first shell and safe areas. |
| Tablet semantic composition | Stable | Pane/posture-aware touch-first layouts. |
| Desktop semantic composition | Stable | Resizable pointer/keyboard workspace. |
| TV semantic composition | Stable | Far-view, overscan-safe directional-focus behavior. |
| TV focus primitives | Stable | Focus/selection distinction and resilient static focus. |
| Form-factor token roles | Stable | Viewing distance, input, navigation, density and composition roles. |

## Glaze UI 1.5 Stable systems
| Area | Status | Retained contract |
| --- | --- | --- |
| Adaptive semantic color | Stable | Contextual semantic color with protected producer-authoritative truth. |
| Iconography, construction, and identity grammar | Stable | Shared visual language, optical sizing and deterministic construction. |
| Motion and interaction | Stable | Purpose-driven interruptible motion and reduced-motion substitution. |
| Material and depth | Stable | Historical Canvas/Solid/Raised/Functional Glass/Clear Glass/Overlay compatibility hierarchy. |
| Layout, spacing, and density | Stable | Semantic spacing, bounded measures, density, safe areas and target floors. |
| Interaction states and input modality | Stable | Focus-visible, hover, pressed, selected and mixed-input semantics. |

## Glaze UI 1.6 Stable systems
| Area | Status | Retained contract |
| --- | --- | --- |
| Evidence presentation and authority surfaces | Stable | Producer-authoritative evidence, provenance/freshness and fail-closed transport presentation. |
| Adaptive workspace and navigation | Stable | Semantic workspace regions, form-factor transformation and input-aware targets. |

## Glaze UI 2.0 Stable systems
Glaze UI **2.0.0 is the current Stable consumer target**. The following design-system capabilities were promoted after exact Candidate source/rendered acceptance:

| Area | Status | Stable contract |
| --- | --- | --- |
| Glaze Material | Stable | Canvas / Surface / Soft Glaze / Glaze / Deep Glaze / Live Glaze with Clear/Balanced/Solid clarity and readable opaque fallback. |
| Appearance and expression | Stable | Light/Dark/Deep Dark and Calm/Balanced/Expressive semantics. |
| Connected Transformation | Stable | Relationship-preserving transformation with native View Transition/shared-element use where available and state-preserving fallback. |
| Navigation Capsule and adaptive navigation | Stable | Phone floating capsule, Tablet rail, Desktop sidebar and TV focus-dock transformation without target shrinkage. |
| Live Surfaces | Stable | Cross-context identity for ongoing processes without minting producer truth. |
| Accessibility/resilience | Stable | 48px general and 56px TV floors, reduced motion/transparency, increased contrast, forced colors, large-text reflow and effects-free usability. |
| Foldable/hinge-aware layout | Stable | Representative pane/hinge exclusion and continuity semantics. |
| Wearable rotational navigation | Stable | Platform-neutral compact rotational-navigation semantics and reduced-motion reference behavior; native/real-device product acceptance remains separate. |
| Spatial floating surfaces | Stable | Platform-neutral anchored/floating surface semantics, effective target preservation under perspective and full depth-free fallback. |

The exact Candidate artifacts remain preserved for promotion provenance. Their filenames and historical Candidate status do not change the current 2.0 Stable lifecycle.

## Glaze Motion Experimental extension
Glaze Motion extends retained Glaze motion research without changing the 2.0 Stable compatibility target.

| Area | Status | Experimental contract |
| --- | --- | --- |
| Motion Core 0.2 / 0.6 evidence line | Experimental | Semantic runtime, bounded springs, direct manipulation, local performance evidence and test-only consumer evaluations. |
| Motion Studio | Planned | Rich product-site storytelling and advanced choreography. |
| Motion Spatial | Planned | Three.js/WebGL/WebGPU experimental graphics and advanced demonstrations. |

Glaze Motion is **Experimental**, is not a mandatory 2.0 consumer dependency, and is not production-conformant unless separately promoted through its own lifecycle gate.

## Candidate form-factor layer
Historical promotion boundary: these form-factor capabilities were the **Candidate form-factor layer** while Glaze UI 1.4 was under review. They are retained Stable history; no active 1.4 form-factor capability remains Candidate.

## Experimental and roadmap boundary
**Glaze Intelligence Layer** presentation grammar included in 2.0 does not create an agent runtime, model, memory, automation, or execution authority. Glaze Agents, independent memory systems, automation, ambient computing, voice, operating-experience, app-store, Motion Studio, Motion Spatial, and other unimplemented ideas remain **Planned/roadmap concepts** until separately implemented, versioned, validated, and promoted.

## Promotion requirements
Candidate capabilities become Stable only after documented semantics, implementation/native mapping guidance, accessibility/resilience behavior, fail-closed validation, applicable rendered/native acceptance, compatibility/migration review, and the `STABILITY.md` promotion gate.

Stable capabilities may not disappear silently; breaking removal requires migration guidance and an appropriate major version.
