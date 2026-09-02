# Glaze UI 2.2 Conformance

Glaze UI 2.2 conformance protects beauty, usability, stability, accessibility, privacy, resilience, tangible interaction, semantic color through Glaze, bounded system hierarchy, and purpose-built cross-environment behavior.

## Required gates

1. **Identity** — recognizably GoreeCloud and traceable to approved identity.
2. **Tokens and contracts** — current semantic colors, typography, spacing, geometry, material, motion, targets, states, accessibility, adaptive-layout roles, component contracts and System Shell roles map to Glaze UI 2.2 contracts or documented native equivalents.
3. **System surface hierarchy** — Workspace → Application → System Overlay → System Panel → Critical System is respected; higher-priority system surfaces become progressively more explicit and solid.
4. **Glaze Material** — durable readable content is solid by default; transient navigation, command, search, control and feedback chrome may use bounded Glaze according to role.
5. **System Glaze budget** — ordinary composition contains at most one dominant Glaze panel plus one to three small floating Glaze controls; nested backdrop blur is prohibited.
6. **Appearance and expression** — Light/Dark/Deep Dark and Calm/Balanced/Expressive preserve readability and layer distinction; decorative richness never outranks access.
7. **Semantic color through Glaze** — selection, live/protected, warning, failure, offline and other state meaning remains explicit and color is never the only carrier.
8. **States and controls** — focus, selected, pressed, disabled, loading, checked, expanded, invalid, success/warning/error and progress meaning are programmatic and deterministic.
9. **Targets** — touch-oriented shell/control targets preserve at least 48 px/dp where governed by 2.2; Touch Assistance and far-view contexts preserve at least 56 px/dp where applicable.
10. **Expression and motion** — Connected Transformation and spatial continuity explain relationships; Reduced Motion removes nonessential travel/morphing without blocking state changes or focus movement.
11. **Accessibility precedence** — Reduced Transparency, Forced Colors, Increased Contrast, Reduced Motion, 200% text and Touch Assistance override decorative optical treatment where required.
12. **Adaptive layout** — components transform rather than merely resize.
13. **Form-factor fidelity** — phone/mobile, tablet, desktop, TV, foldable, wearable and spatial mappings are purpose-built where supported rather than scaled shells.
14. **Universal Search** — immediate query focus, deterministic results before generated interpretation, keyboard traversal, generated-source provenance when available, explicit destructive confirmation, Escape cancellation semantics and focus restoration are preserved when the system-level contract is used.
15. **Control Center** — programmatic toggle/range values, one-dominant-panel exclusivity and focus restoration are preserved when the system-level contract is used.
16. **Intelligence presentation** — generated/AI identity is explicit, generated interpretation remains distinct from retrieved source content, provenance is shown when available, and presentation does not create execution or evidence authority.
17. **Live Surfaces and evidence** — ongoing-process identity may move across contexts but cannot invent freshness, completion, security, privacy, resilience or coordination truth.
18. **Privacy and dependency boundary** — no unnecessary tracking, remote presentation dependency, analytics, or third-party runtime is required by the core reference.
19. **Authority** — Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Mesh and application logic retain domain truth; Glaze UI is presentation/interaction authority only.
20. **Visual acceptance** — representative supported profiles and task flows are rendered/reviewed; the 2.2 design-system Human Visual Excellence gate is bound to immutable approved source `0411b0f6dd877aea30e2c5674e1acde0105fd97b`.
21. **Native evidence boundary** — the bounded Android handheld reference must pass its exact-source build/emulator/runtime/accessibility/resilience gate; downstream native products require their own native/physical-device/OEM/assistive-technology acceptance.
22. **Stability and lifecycle** — production consumers target only current Stable Glaze UI. Candidate/Experimental behavior cannot silently satisfy a Stable claim. `COMPONENT_STATUS.md` and `STABILITY.md` are mandatory lifecycle references.

## Form-factor fidelity acceptance

**Phone/Mobile:** verify touch navigation, safe areas, reachable actions, practical targets, overlays/sheets and no desktop dependency.

**Tablet:** verify rail/pane/split views where useful, posture/window adaptation, touch ergonomics and task-state preservation.

**Desktop:** verify pointer/keyboard behavior, useful resizing, appropriate density, menus/shortcuts/context behavior and multi-pane workflows where useful.

**TV:** verify far-view legibility, overscan-safe essential content, larger controls/type, directional focus reachability, predictable movement, no dead-end traps, Select/Back-equivalent operation, focus/selection distinction and static high-contrast focus under Reduced Motion/Forced Colors.

**Foldable:** verify hinge/fold avoidance, pane minimums, posture/orientation continuity, focus/reading order and no interactive control crossing an excluded hinge region.

**Smartwatch/Wearable:** verify compact hierarchy, effective target size, touch/native-equivalent completion, rotational navigation when applicable, Reduced Motion/Transparency, large text and platform-native behavior. Design-system compatibility references do not substitute for application-specific native or real-device acceptance.

**Spatial:** verify anchored/floating surfaces, focusability, effective targets at supported depth, full flat/no-depth fallback and no dependency on advanced graphics for basic usability. Hardware-specific spatial products require application-specific native or real-device acceptance.

## Evidence

Passing overflow or screenshot checks alone is insufficient. Evidence must identify the exact design-system/application revision and environment tested. A design-system Stable promotion establishes a mandatory target, not downstream product certification.

Evidence freshness and authority remain producer-bound. Expired, stale, superseded, malformed, or otherwise invalid evidence cannot support a current conformance claim.

Source-pinned visual regression must render both the immutable approved 2.2 source and the current exact head independently on the controlled runner. Self-blessing the current head as its own baseline is not conformance evidence.

## Current-Stable conformance claims

Glaze UI **2.2.0** is the current Stable baseline and the only active version eligible for a current GoreeCloud application conformance or production UI acceptance claim.

A product may claim **`Glaze UI 2.2 conformant`** only when every applicable current gate is satisfied, the product targets exact current Stable 2.2.0, and product-specific acceptance is complete. A Stable claim additionally requires the Stable lifecycle surfaces in `COMPONENT_STATUS.md` and `STABILITY.md`.

Historical Glaze UI 1.0.0 through 2.1.0 remain release, migration, rollback and audit evidence only. They cannot satisfy current production readiness after 2.2 promotion.

No documented exception can waive current-Stable application alignment. Platform-neutral or bounded design-system native evidence does not waive **application-specific native or real-device acceptance** where the consuming product is native or hardware-specific.

## Candidate and Experimental boundary

`2.2.0-candidate.1` is historical promotion provenance only and cannot be a production consumer target. Candidate-named implementation files are not production aliases; current consumers use 2.2.0 Stable entrypoints or documented native equivalents.

Glaze Motion remains separately Experimental. The bounded Stable Intelligence component tier does not create an agent runtime, model authority, independent memory, automation authority, or background execution authority.
