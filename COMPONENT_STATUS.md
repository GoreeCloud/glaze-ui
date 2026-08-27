# Glaze UI Component Lifecycle

This record defines lifecycle status for canonical Glaze UI capabilities.

## Lifecycle definitions

### Stable
Documented, validated capabilities included in the compatibility promise.

### Candidate
Implemented capabilities still under formal promotion review.

### Experimental
Exploratory capabilities that may change substantially and cannot be mandatory Stable dependencies.

### Planned
Roadmap direction only; not implemented shipping functionality.

## Glaze UI 1.3 Stable foundations
The 1.3 semantic color, surface, typography, spacing, shape, effects/spatial motion, state-layer, focus/target, accessibility/resilience, safe-area, privacy, product-personality, core controls, Functional Glass, Clear Glass, adaptive action groups, reachability, and hero-typography contracts remain Stable and are retained by 1.4.

## Glaze UI 1.4 Stable form-factor layer
| Area | Status | Stable contract |
| --- | --- | --- |
| Mobile semantic composition | Stable | Touch/reachability-first shell, safe areas, mobile navigation, dense-data transformation. |
| Tablet semantic composition | Stable | Pane/posture-aware layouts with touch primary and optional pointer/keyboard/stylus enhancement. |
| Desktop semantic composition | Stable | Resizable workspace, pointer/keyboard behavior, persistent navigation/toolbars and multi-pane patterns where useful. |
| TV semantic composition | Stable | Far-view, landscape-first, overscan-safe, directional-focus, remote/D-pad operation. |
| TV focus primitives | Stable | Focus/selection distinction, predictable directional movement, bounded focus motion, reduced-motion/forced-colors fallback. |
| Form-factor token roles | Stable | Viewing distance, input, navigation, density, composition, anti-pattern metadata. |

## Glaze UI 1.5 Stable systems
| Area | Status | Stable contract |
| --- | --- | --- |
| Adaptive semantic color | Stable | Contextual semantic color, protected truth families, prominence, accessibility and reduced-transparency behavior. |
| Iconography, construction, and identity grammar | Stable | Shared visual language with stable recognition, optical sizing, protected semantics, deterministic construction and badge rules. |
| Motion and interaction | Stable | Purpose-driven interruptible motion, reduced-motion substitution, truthful state transitions and input-aware feedback. |
| Material and depth | Stable | Canvas/Solid/Raised/Functional Glass/Clear Glass/Overlay hierarchy with bounded translucency and fallbacks. |
| Layout, spacing, and density | Stable | Semantic spacing, gutters, bounded measures, density modes, safe-area behavior, target floors and overflow containment. |
| Interaction states and input modality | Stable | Focus-visible, hover, pressed, selected, expanded, disabled, read-only, loading, invalid, success and mixed-input semantics. |

## Glaze UI 1.6 Candidate systems
| Area | Status | Candidate contract |
| --- | --- | --- |
| Evidence presentation and authority surfaces | Candidate | Producer-authoritative state presentation, explicit authority identity, evidence freshness, Mesh transport state, provenance detail, accessibility, and fail-closed unavailable/invalid handling without inventing security, privacy, recovery, or coordination truth. |

The 1.6 evidence-presentation candidate is defined by `EVIDENCE_PRESENTATION.md`, `tokens/evidence-presentation.json`, and `tokens/mesh-evidence-profile.json`. It is implemented source material under formal promotion review and is **not** part of the 1.5.0 Stable compatibility promise or current Stable consumer target.

## Glaze Motion Experimental extension
Glaze Motion extends the Stable Glaze UI motion baseline without changing the current Stable compatibility target.

| Area | Status | Experimental contract |
| --- | --- | --- |
| Motion Core 0.2 | Experimental | Semantic motion runtime, bounded springs, direct-manipulation gesture sessions, snap resolution, shared-element/View Transition fallback, component adapters, reduced-motion invariants, source tests, and rendered acceptance. |
| Motion Studio | Planned | Rich product-site storytelling, scroll choreography, Rive/SVG/Canvas animation, bounded particles/parallax, cinematic transitions, and interactive hero experiences. |
| Motion Spatial | Planned | Three.js/WebGL2/WebGPU, interactive 3D, real-time visualization, mesh/simulation, and advanced product demonstrations with progressive fallback. |

Motion Core 0.2 is implemented development source but is **not** part of Glaze UI 1.5.0 Stable, is not a mandatory consumer dependency, and must not be represented as production-conformant until normal Candidate/Stable promotion requirements are satisfied.

## Candidate form-factor layer
Historical promotion boundary: these form-factor capabilities were the **Candidate form-factor layer** while Glaze UI 1.4 was under review. They are now Stable in 1.4.0. No active 1.4 form-factor capability remains Candidate after promotion.

## Experimental and roadmap boundary
Glaze Intelligence Layer, Glaze Agents, Glaze Memory, automation, ambient computing, voice, operating-experience, app-store, and other speculative 1.7/1.8/2.0 ideas remain **Planned/roadmap concepts** and are not shipping Stable behavior.

## Promotion requirements
Candidate capabilities become Stable only after documented semantics, implementation/native mapping guidance, accessibility/resilience behavior, fail-closed validation, rendered/native acceptance applicable to the design-system scope, compatibility/migration review, and the `STABILITY.md` promotion gate.

Experimental Glaze Motion capabilities must first establish promotion-ready APIs/tokens, representative consumer evidence, accessibility and performance evidence, and an explicit Candidate boundary before Stable promotion is considered.

Stable capabilities may not disappear silently; breaking removal requires migration guidance and an appropriate major version.
