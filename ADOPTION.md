# Adopting Glaze UI

Glaze UI **2.1.0** is the current Stable baseline and is mandatory for every GoreeCloud-controlled user-facing application and website. Superseded Glaze UI versions may remain only as historical, migration, rollback, or evidence context; they do not satisfy current production-readiness requirements.

Stable promotion establishes the required target. It does **not** make a downstream consumer conforming or production-ready by declaration. Every consumer must implement 2.1 in its own supported scope and earn repository-local validation, rendered/product acceptance, and deployment acceptance where applicable.

## 1. Record the target version and authority

Record **2.1.0**, the reviewed canonical source/release revision, repository-local evidence, automated contract, and product-specific acceptance boundary. The canonical authority is `GoreeCloud/goreecloud-glaze-ui`.

Do not treat a 1.x or 2.0 record as current conformance. Historical records remain useful for migration and rollback evidence only.

## 2. Map semantics before visuals

Map canvas/content, text/status, spacing, geometry, focus, motion, forms, selection controls, navigation, adaptive layout, form-factor and platform context before replacing successful product composition. Do not rename producer-authoritative security, privacy, identity, continuity, or operational state into visual-only local vocabulary.

## 3. Use the current material principle

**Content is solid. Interaction is glazed.**

Durable reading and data surfaces use Canvas or Surface material. Persistent secondary interaction may use Soft Glaze; floating interaction Glaze; menus and popovers Deep Glaze; deliberately active or dynamic interaction Live Glaze. Use Clear, Balanced, or Solid clarity to preserve legibility and performance.

Glaze is a semantic interaction material, not a decorative glass effect to apply indiscriminately.

## 4. Use current geometry, density, and expression

Use the 2.1 geometry and expression system according to hierarchy and task. Preserve concentric relationships, intentional utility/expression shapes, the 4pt spacing rhythm, and semantic density behavior.

Support comfortable and compact density where the product exposes density choice. Density must not reduce required interaction floors or compromise legibility.

## 5. Adopt controls as semantic units

Prefer native platform controls when they provide stronger semantics, ergonomics, accessibility, or platform fidelity. Persistent labels, help/error relationships, selection state, switches, progress and feedback are behavioral units, not decoration.

Use Quiet, Soft, Glaze, and Emphasis button roles according to hierarchy rather than inventing competing primary/secondary component systems.

## 6. Preserve accessibility from the beginning

Current 2.1 adoption includes, at minimum:

- visible keyboard focus;
- a **48px general interaction floor**;
- a **56px Touch Assistance floor** where Touch Assistance is enabled or required;
- semantic names, roles, values, and states;
- large-text reflow without clipping or loss of content;
- reduced-motion behavior;
- reduced-transparency behavior with opaque fallbacks;
- increased-contrast and forced-colors support;
- state communication that is not color-only;
- effects-free and reduced-performance fallbacks;
- usable zoom and text resize behavior.

Accessibility is part of the component and layout contract, not a post-release polish pass.

## 7. Treat adaptation as a semantic transform

Width is one signal, not a device identity. Navigation and layout may transform across phone, tablet, desktop, TV, foldable, wearable, and spatial environments while preserving semantic order, current destination, authoritative state, focus continuity, and task continuity.

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

## 9. Preserve logical order and authoritative state

Reachability, adaptive grouping, and Connected Transformation may change visual allocation, never reading order, semantic meaning, authoritative state, keyboard/focus order, or security/privacy/identity boundaries.

## 10. Keep presentation local by default

Glaze UI 2.1 does not require analytics, trackers, remote fonts or icons, CDN UI dependencies, network calls, or browser storage in the core design-system runtime. GoreeCloud websites and applications should keep presentation assets local unless an explicit reviewed product requirement establishes otherwise.

## 11. Use approved GoreeCloud visual identity

Glaze UI governs interface design; it does not authorize product branding. GoreeCloud logos, product icons, system marks, artwork, and approved production derivatives come from `GoreeCloud/goreecloud-branding-assets`.

Do not redraw, recolor, substitute, or invent an official GoreeCloud asset when an approved canonical asset exists. When no approved asset exists, use a clearly neutral presentation until the branding authority publishes one.

## 12. Add a consumer contract test

Validate the subset consumed: exact current Stable version/revision, current material/token semantics, interaction states, accessibility and resilience fallbacks, form-factor activation, target floors, platform-specific input behavior, asset provenance where relevant, and authority boundaries. Fail closed on a superseded active version or missing required evidence.

A build-time rewrite that silently converts stale active source markup into 2.1 should not be the only conformance control. Current source, generated artifact, and deployed representation should agree on the active design-system contract.

## 13. Perform visual and product acceptance

Representative web review profiles include Mobile **390×844**, Tablet **820×1180**, Desktop **1280×900**, and Wide Desktop **1600×1000**, plus additional form factors when the product supports them. Review real task flows and all important states, not screenshots alone.

Acceptance should cover light/dark appearance where supported, keyboard navigation, touch/pointer behavior, zoom and large text, reduced motion, reduced transparency, forced colors, loading/empty/error/disabled/selected/focus states, responsive transitions, and performance/resilience fallbacks.

Native or hardware products add platform-specific native, accessibility, performance, and representative-device evidence.

## Migration from Glaze UI 2.0

`MIGRATION_2_0_TO_2_1.md` is the canonical 2.0→2.1 migration and compatibility-impact guide. Preserve successful application semantics while adopting the stricter 2.1 accessibility, material, performance, state, native-platform, rollback, and evidence requirements.

Do not treat a successful 2.0 conformance record as 2.1 evidence. Where 2.0 artifacts are retained, identify them explicitly as historical or rollback context rather than current implementation guidance.

## Current adoption rule

There are no production exceptions to the current-Stable target. Platform limitations, upstream constraints, schedule pressure, incomplete migration, or technical inconvenience require additional implementation work; they do not permit a GoreeCloud-controlled user-facing production surface to claim current Glaze UI conformance while actively using a superseded or incomplete implementation.
