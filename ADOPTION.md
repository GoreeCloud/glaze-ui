# Adopting Glaze UI

Glaze UI **2.2.0** is the current Stable baseline and is mandatory for every GoreeCloud-controlled user-facing application and website where Glaze UI applies. Superseded Glaze UI versions may remain only as historical, migration, rollback, or evidence context; they do not satisfy current production-readiness requirements.

Stable promotion establishes the required target. It does **not** make a downstream consumer conforming or production-ready by declaration. Every consumer must implement 2.2 in its own supported scope and earn repository-local validation, rendered/native/product acceptance, and deployment acceptance where applicable.

## 1. Record the target version and authority

Record **2.2.0**, the reviewed canonical source/release revision, repository-local evidence, automated contract, and product-specific acceptance boundary. The canonical authority is `GoreeCloud/goreecloud-glaze-ui`.

Do not treat a 2.1 or earlier record as current conformance. Historical records remain useful for migration, rollback and regression evidence only.

## 2. Map semantics before visuals

Map Workspace/Application/System Overlay/System Panel/Critical System ownership, canvas/content, text/status, spacing, geometry, focus, motion, forms, selection controls, navigation, adaptive layout, component tier, form-factor and platform context before replacing successful product composition. Do not rename producer-authoritative security, privacy, identity, continuity, or operational state into visual-only local vocabulary.

## 3. Use the current material principle

**Solid where users read or make explicit critical decisions. Glazed where users interact with transient navigation, command, search, control, or feedback chrome.**

Durable reading and data surfaces use Canvas or Surface material. Persistent secondary interaction may use Soft Glaze; floating interaction Glaze; menus/popovers Deep Glaze; deliberately active/dynamic interaction Live Glaze. Critical System presentation is certainty-first and increasingly solid.

Glaze is a semantic interaction material, not a decorative effect to apply indiscriminately.

## 4. Respect the System Glaze budget

Ordinary shell composition allows at most **one dominant Glaze panel** plus **one to three small floating Glaze controls**. Nested backdrop blur is prohibited. More visual layering requires an explicitly justified exceptional context rather than a disabled validator.

Universal Search and Control Center must not appear simultaneously as competing dominant Glaze panels.

## 5. Use current geometry, density, and expression

Use the 2.2 geometry and expression system according to hierarchy and task. Preserve concentric relationships, intentional utility/expression shapes, semantic density behavior, reachable action placement, and optical depth only where it explains interaction.

Density must not reduce required interaction floors or compromise legibility. Depth/transformation must never reduce effective target size below the applicable floor.

## 6. Adopt controls as semantic units

Prefer native platform controls when they provide stronger semantics, ergonomics, accessibility, or platform fidelity. Persistent labels, help/error relationships, selection state, switches, sliders, progress and feedback are behavioral units, not decoration.

Map locally consumed controls to the applicable 2.2 Foundation, Structure, Overlay, Signature, or Intelligence component contract rather than matching appearance alone.

## 7. Preserve accessibility from the beginning

Current 2.2 adoption includes, at minimum:

- visible keyboard focus;
- a **48px/dp touch-oriented interaction floor** where governed by the 2.2 shell/component contract;
- a **56px/dp Touch Assistance / far-view floor** where applicable;
- semantic names, roles, values, and states;
- 200% text/reflow without clipping or loss of content;
- Reduced Motion behavior;
- Reduced Transparency behavior with solid fallbacks;
- Increased Contrast and Forced Colors support;
- state communication that is not color-only;
- effects-free and reduced-performance fallbacks;
- usable zoom and text resize behavior;
- RTL/localization expansion; and
- focus restoration after transient system surfaces close.

Accessibility is part of the component and layout contract, not a post-release polish pass.

## 8. Design explicitly for phone, tablet, and desktop

### Phone
Phone layouts prioritize reachability, touch, safe areas, compact task focus, and intentional bottom/edge action placement. Mobile must not be a shrunken tablet or desktop shell.

### Tablet
Tablet is a first-class composition with intentional pane use, spacing, density, navigation, and input behavior. It must not be a stretched phone layout.

### Desktop
Desktop uses available space for clearer hierarchy, denser information where appropriate, keyboard/pointer efficiency, and persistent navigation when useful. It must not be an enlarged mobile shell.

### TV
TV is a far-viewing, landscape-first environment. Use larger type, targets, and spacing; predictable focus groups; remote/D-pad directional navigation; clear focus/selection distinction; Select/Back-equivalent task flows; and no pointer/swipe dependency for primary navigation.

### Foldables
Reserve physical hinges/folds as exclusion regions where required. Prefer pane-aware task composition, preserve continuity across posture/orientation changes, and never route an essential target through an unusable hinge region.

### Wearables
Wearable UI is glance-first and purpose-built. Do not shrink Mobile. Rotational or crown input may enhance interaction where supported while preserving the platform's required native interaction and accessibility paths.

### Spatial
Use depth as supplemental hierarchy only. Anchored and floating controls remain semantic and usable when flattened; advanced graphics are never required for basic task completion.

## 9. Treat adaptation as a semantic transform

Width is one signal, not a device identity. Navigation and layout may transform across phone, tablet, desktop, TV, foldable, wearable, and spatial environments while preserving semantic order, current destination, authoritative state, focus continuity, and task continuity.

Reachability, adaptive grouping, and Connected Transformation may change visual allocation, never reading order, semantic meaning, authoritative state, keyboard/focus order, or security/privacy/identity boundaries.

## 10. Integrate Universal Search deliberately

Do not relabel ordinary local search as Universal Search. A system-level implementation preserves immediate query focus, deterministic source/results ordering before generated interpretation, keyboard traversal, generated-source provenance when available, explicit second activation for destructive actions, Escape cancellation semantics, and meaningful focus restoration.

Generated interpretation must remain visually and semantically distinct from retrieved source content.

## 11. Integrate Control Center deliberately

Use semantic system controls rather than simulated cards. Toggle state must be programmatically available, range controls expose real values, and closing the panel restores meaningful invoker focus. Control Center cannot coexist with another dominant Glaze system panel without an approved exceptional context.

## 12. Use Intelligence components without inventing authority

AI Action, AI Suggestion, AI Answer, Smart Summary and Source Chip are presentation contracts. They require explicit generated/AI identity, source provenance when available, calibrated language, nonblocking behavior and dismissibility where appropriate.

They do not create model authority, independent memory, automation permission, background execution authority, or evidence truth.

## 13. Keep presentation local by default

Glaze UI 2.2 does not require analytics, trackers, remote fonts or icons, CDN UI dependencies, network calls, or browser storage in the core design-system runtime. GoreeCloud websites and applications should keep presentation assets local unless an explicit reviewed product requirement establishes otherwise.

## 14. Use approved GoreeCloud visual identity

Glaze UI governs interface design; it does not authorize product branding. GoreeCloud logos, product icons, system marks, artwork, and approved production derivatives come from the canonical branding authority.

Do not redraw, recolor, substitute, or invent an official GoreeCloud asset when an approved canonical asset exists. When no approved asset exists, use a clearly neutral presentation until the branding authority publishes one.

## 15. Add a consumer contract test

Validate the subset consumed: exact current Stable version/revision, component/System Shell mapping, material/token semantics, interaction states, accessibility and resilience fallbacks, form-factor activation, target floors, System Glaze budget, platform-specific input behavior, asset provenance where relevant, and authority boundaries. Fail closed on a superseded active version or missing required evidence.

A build-time rewrite that silently converts stale active source markup into 2.2 should not be the only conformance control. Current source, generated artifact, and deployed representation should agree on the active design-system contract.

## 16. Perform visual and product acceptance

Representative web review profiles include Mobile **390×844**, Tablet **820×1180**, Desktop **1280×900**, and Wide Desktop **1600×1000**, plus additional form factors when the product supports them. Review real task flows and all important states, not screenshots alone.

Acceptance should cover Light/Dark/Deep Dark where supported, keyboard navigation, touch/pointer behavior, 200% text, RTL/localization, Reduced Motion, Reduced Transparency, Increased Contrast, Forced Colors, Touch Assistance, loading/empty/error/disabled/selected/focus states, responsive transitions, and performance/resilience fallbacks.

Native or hardware products add platform-specific native, accessibility, performance, OEM/system-integration, assistive-technology, and representative physical-device evidence.

## Migration from Glaze UI 2.1

`MIGRATION_2_1_TO_2_2.md` is the canonical 2.1→2.2 migration and compatibility-impact guide. Preserve successful application semantics while adopting the stricter 2.2 System Shell hierarchy, complete component catalog, accessibility, System Glaze budget, Universal Search/Control Center, Intelligence provenance, performance, native-reference, rollback, and evidence requirements.

Do not treat a successful 2.1 conformance record as 2.2 evidence. Where 2.1 artifacts are retained, identify them explicitly as historical or rollback context rather than current implementation guidance.

## Current adoption rule

There are no production exceptions to the current-Stable target. Platform limitations, upstream constraints, schedule pressure, incomplete migration, or technical inconvenience require additional implementation work; they do not permit a GoreeCloud-controlled user-facing production surface to claim current Glaze UI conformance while actively using a superseded or incomplete implementation.

Candidate-named 2.2 implementation files are promotion provenance, not production aliases. Production consumers use the 2.2.0 Stable entrypoints or documented native equivalents.
