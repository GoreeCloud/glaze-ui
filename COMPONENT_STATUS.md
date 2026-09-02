# Glaze UI Component Lifecycle

This record defines lifecycle status for canonical Glaze UI capabilities. Machine authority is `registry/lifecycle.json`.

## Lifecycle definitions

### Stable
Documented, validated capabilities included in the current compatibility promise.

### Candidate
Implemented capabilities still under formal promotion review.

### Experimental
Exploratory capabilities that may change substantially and cannot be mandatory Stable dependencies.

### Planned
Roadmap direction only; not implemented shipping functionality.

### Historical
Preserved release/capability evidence that is no longer a current production target but remains available for migration, rollback, regression and audit.

## Glaze UI 1.3 Stable foundations
The 1.3 semantic color, surface, typography, spacing, shape, effects/spatial motion, state-layer, focus/target, accessibility/resilience, safe-area, privacy, product-personality, core controls, Functional Glass, Clear Glass, adaptive action groups, reachability, and hero-typography contracts remain retained Stable history and compatibility regression evidence.

## Glaze UI 1.4 Stable form-factor layer
| Area | Status | Retained contract |
| --- | --- | --- |
| Mobile semantic composition | Historical Stable | Touch/reachability-first shell and safe areas. |
| Tablet semantic composition | Historical Stable | Pane/posture-aware touch-first layouts. |
| Desktop semantic composition | Historical Stable | Resizable pointer/keyboard workspace. |
| TV semantic composition | Historical Stable | Far-view, overscan-safe directional-focus behavior. |
| TV focus primitives | Historical Stable | Focus/selection distinction and resilient static focus. |
| Form-factor token roles | Historical Stable | Viewing distance, input, navigation, density and composition roles. |

## Glaze UI 1.5 Stable systems
| Area | Status | Retained contract |
| --- | --- | --- |
| Adaptive semantic color | Historical Stable | Contextual semantic color with protected producer-authoritative truth. |
| Iconography, construction, and identity grammar | Historical Stable | Shared visual language, optical sizing and deterministic construction. |
| Motion and interaction | Historical Stable | Purpose-driven interruptible motion and reduced-motion substitution. |
| Material and depth | Historical Stable | Historical Canvas/Solid/Raised/Functional Glass/Clear Glass/Overlay compatibility hierarchy. |
| Layout, spacing, and density | Historical Stable | Semantic spacing, bounded measures, density, safe areas and target floors. |
| Interaction states and input modality | Historical Stable | Focus-visible, hover, pressed, selected and mixed-input semantics. |

## Glaze UI 1.6 Stable systems
| Area | Status | Retained contract |
| --- | --- | --- |
| Evidence presentation and authority surfaces | Historical Stable | Producer-authoritative evidence, provenance/freshness and fail-closed transport presentation. |
| Adaptive workspace and navigation | Historical Stable | Semantic workspace regions, form-factor transformation and input-aware targets. |

## Glaze UI 2.0 historical Stable systems
Glaze UI **2.0.0 is a historical Stable baseline**. Its promoted capabilities remain permanent migration, rollback and regression evidence.

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

## Glaze UI 2.1 historical Stable systems
Glaze UI **2.1.0 is the immediately preceding historical Stable baseline and the rollback reference for 2.2.0**.

| Area | Status | Retained contract |
| --- | --- | --- |
| Color-coded Glaze Material | Historical Stable | Content remains solid; interaction chrome uses bounded translucent material while accent and semantic color remain explicit. |
| Material Clarity and performance | Historical Stable | Clear/Balanced/Solid plus deterministic Material Budgets and Full/Balanced/Constrained/Minimal degradation. |
| Accessibility resolution | Historical Stable | Reduced Transparency, Forced Colors, Reduced Motion, Increased Contrast, 200% text and Touch Assistance resolved renderings. |
| Density profiles | Historical Stable | Comfortable, Standard, Compact and Far View semantics with target floors preserved. |
| Canonical reference flows | Historical Stable | Settings, Files, Search/Command, Communication/Live Activity, Media Playback and Resilience/Exceptional States. |
| Source-pinned visual regression | Historical Stable | Immutable approved baseline revision and exact-head same-run rendering. |
| Android handheld reference | Historical Stable | Retained bounded exact-source emulator build/install/runtime regression evidence. |
| Foldable, wearable and spatial semantics | Historical Stable | Retained 2.x platform-neutral semantics; downstream hardware/native certification remains separate. |

Human Visual Excellence for the 2.1 refined color-coded glass presentation was approved on 2026-08-30. Its evidence remains immutable historical regression authority.

## Glaze UI 2.2 Stable systems
Glaze UI **2.2.0 is the current Stable consumer target**.

| Area | Status | Stable contract |
| --- | --- | --- |
| System Shell hierarchy | Stable | Workspace → Application → System Overlay → System Panel → Critical System, with increasingly explicit/solid presentation as system priority rises. |
| Foundation components | Stable | 8 machine-readable component contracts with rendered acceptance. |
| Structure components | Stable | 8 machine-readable component contracts with rendered acceptance. |
| Overlay components | Stable | 6 machine-readable component contracts with rendered acceptance. |
| Signature components | Stable | 5 bounded components, including Capsule, Morph Card, Smart Rail, Aurora Surface and Universal Search. |
| Intelligence components | Stable | 5 presentation components with explicit generated/AI identity and provenance requirements where available. |
| Evidence presentation and authority surfaces | Stable | Producer-authoritative evidence, provenance/freshness, fail-closed transport presentation, and cross-domain authority separation carried forward under 2.2 material/System Shell rules. |
| Complete component contract catalog | Stable | 32 total component contracts across the five tiers; catalog stability does not auto-implement them in products. |
| Universal Search reference runtime | Stable | Bounded keyboard traversal, deterministic results-before-generation, destructive confirmation and focus restoration. |
| Control Center reference runtime | Stable | Programmatic toggle/range state, dominant-panel exclusivity and focus restoration. |
| System Glaze budget | Stable | At most one dominant Glaze panel and one to three small floating Glaze controls in ordinary composition; nested backdrop blur prohibited. |
| Optical Reachability | Stable | Human-approved presentation with sculpted reachable controls, contained selection, readable solid content and accessibility-precedence fallbacks. |
| Accessibility and input | Stable | Keyboard, pointer, touch, RTL, 200% text, Reduced Motion, Reduced Transparency, Increased Contrast, Forced Colors and Touch Assistance acceptance. |
| Target geometry | Stable | 48 px/dp touch-oriented shell/control floor and 56 px/dp Touch Assistance/far-view floor where applicable. |
| Performance and degradation | Stable | Deterministic performance/System Glaze-budget evidence; effects simplify before semantics or target geometry. |
| Source-pinned visual regression | Stable | Six-case same-run rendering against immutable human-approved source `0411b0f6dd877aea30e2c5674e1acde0105fd97b`. |
| Android handheld reference | Stable | Bounded 2.2 exact-source build/emulator/runtime/accessibility/resilience design-system evidence; downstream physical-device/OEM/AT acceptance remains product-specific. |
| Consumer migration governance | Stable | 2.2.0 is mandatory current target; downstream consumers remain separately evidence-gated and are never auto-promoted. |

Human Visual Excellence for the 2.2 Optical Reachability presentation was explicitly **Accepted** on 2026-09-01.

## Glaze Motion Experimental extension
Glaze Motion remains separately governed under the current Glaze UI 2.2 Stable release.

| Area | Status | Experimental contract |
| --- | --- | --- |
| Motion Core 0.2 / 0.6 evidence line | Experimental | Semantic runtime, bounded springs, direct manipulation, local performance evidence and test-only consumer evaluations. |
| Motion Studio | Planned | Rich product-site storytelling and advanced choreography. |
| Motion Spatial | Planned | Three.js/WebGL/WebGPU experimental graphics and advanced demonstrations. |

Glaze Motion is **Experimental**, is not a mandatory 2.2 consumer dependency, and is not production-conformant unless separately promoted through its own lifecycle gate.

## Candidate form-factor layer
Historical promotion boundary: these form-factor capabilities were the **Candidate form-factor layer** while Glaze UI 1.4 was under review. They are retained Stable history; no active 1.4 form-factor capability remains Candidate.

There is no active Glaze UI 2.2 Candidate after Stable promotion. `2.2.0-candidate.1` is historical promotion provenance only.

## Experimental and roadmap boundary
**Glaze Intelligence Layer** presentation grammar and the bounded Stable 2.2 Intelligence component tier do not create an agent runtime, model, memory, automation, or execution authority. Glaze Agents, independent memory systems, automation, ambient computing, voice, operating-experience, app-store, Motion Studio, Motion Spatial, and other unimplemented ideas remain **Planned/roadmap concepts** until separately implemented, versioned, validated, and promoted.

## Promotion requirements
Candidate capabilities become Stable only after documented semantics, implementation/native mapping guidance, accessibility/resilience behavior, fail-closed validation, applicable rendered/native acceptance, compatibility/migration review, required human Visual Excellence review, and the `STABILITY.md` promotion gate.

Stable capabilities may not disappear silently; breaking removal requires migration guidance and an appropriate major version.
