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

## Glaze UI 2.0 historical Stable systems
Glaze UI **2.0.0 is the immediately preceding historical Stable baseline**. Its promoted design-system capabilities remain permanent migration, rollback and regression evidence:

| Area | Status | Retained contract |
| --- | --- | --- |
| Glaze Material | Historical Stable | Canvas / Surface / Soft Glaze / Glaze / Deep Glaze / Live Glaze foundation with readable opaque fallback. |
| Appearance and expression | Historical Stable | Light/Dark/Deep Dark and Calm/Balanced/Expressive semantics. |
| Connected Transformation | Historical Stable | Relationship-preserving transformation with native/shared-element use where available and state-preserving fallback. |
| Navigation Capsule and adaptive navigation | Historical Stable | Phone floating capsule, Tablet rail, Desktop sidebar and TV focus-dock transformation without target shrinkage. |
| Live Surfaces | Historical Stable | Cross-context identity for ongoing processes without minting producer truth. |
| Accessibility/resilience | Historical Stable | 48px general and 56px TV floors, reduced motion/transparency, increased contrast, forced colors, large-text reflow and effects-free usability. |
| Foldable/hinge-aware layout | Historical Stable | Representative pane/hinge exclusion and continuity semantics. |
| Wearable rotational navigation | Historical Stable | Platform-neutral compact rotational-navigation semantics; product native/real-device acceptance remains separate. |
| Spatial floating surfaces | Historical Stable | Platform-neutral anchored/floating surface semantics and full depth-free fallback. |

The exact 2.0 Candidate/promotion artifacts remain preserved for provenance. Their filenames and historical Candidate status do not change the fact that 2.0 was promoted and is now superseded by 2.1.

## Glaze UI 2.1 Stable systems
Glaze UI **2.1.0 is the current Stable consumer target**.

| Area | Status | Stable contract |
| --- | --- | --- |
| Color-coded Glaze Material | Stable | Content remains solid; interaction chrome uses bounded translucent Soft Glaze / Glaze / Deep Glaze / Live Glaze while accent and semantic color remain explicit. |
| Material Clarity and performance | Stable | Clear/Balanced/Solid plus deterministic Material Budgets and Full/Balanced/Constrained/Minimal degradation. |
| Appearance and expression | Stable | Light/Dark/Deep Dark and Calm/Balanced/Expressive, with accessibility precedence over decorative richness. |
| Accessibility resolution | Stable | Reduced Transparency, Forced Colors, Reduced Motion, Increased Contrast, 200% Large Text and Touch Assistance are first-class resolved renderings. |
| Density profiles | Stable | Comfortable, Standard, Compact and Far View semantics with target floors preserved. |
| Canonical reference flows | Stable | Settings, Files, Search/Command, Communication/Live Activity, Media Playback and Resilience/Exceptional States. |
| Evidence presentation and authority | Stable | Retained producer-authoritative 1.6/2.0 contract carried into 2.1 current material/accessibility semantics. |
| Source-pinned visual regression | Stable | Immutable approved baseline revision, unchanged pixel thresholds, exact-head same-run rendering, and recorded human Visual Excellence acceptance. |
| Android handheld reference | Stable | Bounded exact-source native emulator build/install/runtime reference with 48 dp general and 56 dp Touch Assistance floors; downstream physical-device acceptance remains application-specific. |
| Foldable, wearable and spatial semantics | Stable | Retained 2.x platform-neutral semantics; downstream hardware/native certification remains separate. |

Human Visual Excellence for the refined color-coded glass presentation was explicitly approved on 2026-08-30.

## Glaze Motion Experimental extension
Glaze Motion remains separately governed under the current Glaze UI 2.1 Stable release.

| Area | Status | Experimental contract |
| --- | --- | --- |
| Motion Core 0.2 / 0.6 evidence line | Experimental | Semantic runtime, bounded springs, direct manipulation, local performance evidence and test-only consumer evaluations. |
| Motion Studio | Planned | Rich product-site storytelling and advanced choreography. |
| Motion Spatial | Planned | Three.js/WebGL/WebGPU experimental graphics and advanced demonstrations. |

Glaze Motion is **Experimental**, is not a mandatory 2.1 consumer dependency, and is not production-conformant unless separately promoted through its own lifecycle gate.

## Candidate form-factor layer
Historical promotion boundary: these form-factor capabilities were the **Candidate form-factor layer** while Glaze UI 1.4 was under review. They are retained Stable history; no active 1.4 form-factor capability remains Candidate.

## Experimental and roadmap boundary
**Glaze Intelligence Layer** presentation grammar retained from 2.0 does not create an agent runtime, model, memory, automation, or execution authority. Glaze Agents, independent memory systems, automation, ambient computing, voice, operating-experience, app-store, Motion Studio, Motion Spatial, and other unimplemented ideas remain **Planned/roadmap concepts** until separately implemented, versioned, validated, and promoted.

## Promotion requirements
Candidate capabilities become Stable only after documented semantics, implementation/native mapping guidance, accessibility/resilience behavior, fail-closed validation, applicable rendered/native acceptance, compatibility/migration review, required human Visual Excellence review, and the `STABILITY.md` promotion gate.

Stable capabilities may not disappear silently; breaking removal requires migration guidance and an appropriate major version.
