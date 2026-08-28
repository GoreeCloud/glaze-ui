# Adopting Glaze UI

Glaze UI 2.0.0 is the current Stable baseline and is mandatory for every GoreeCloud-controlled user-facing application. Existing 1.x consumers are migration-required; controlled migration is mandatory, and superseded Glaze UI versions cannot satisfy production readiness.

## 1. Record the target version
Record **2.0.0**, the reviewed canonical source/release revision, repository-local evidence, automated contract, and product-specific acceptance boundary. A 1.x version may be recorded only as historical or migration evidence.

## 2. Map semantics before visuals
Map canvas/content, text/status, spacing, geometry, focus, motion, forms, selection controls, navigation, adaptive layout, form-factor and platform context before replacing successful product composition. Do not rename producer-authoritative security/privacy/resilience state into visual-only local vocabulary.

## 3. Adopt the 2.0 material hierarchy intentionally
Content uses Canvas/Surface. Persistent secondary controls may use Soft Glaze; floating interaction Glaze; menus/popovers Deep Glaze; active/dynamic interaction Live Glaze. Use Clear/Balanced/Solid clarity to preserve readability. The legacy 1.x Functional Glass/Clear Glass hierarchy is migration evidence, not the target vocabulary.

## 4. Adopt expression by role
Use 2.0 utility/expression geometry and Calm/Balanced/Expressive personalization according to hierarchy. Reduced motion removes nonessential scale, morphing, rebound and travel while preserving direct manipulation and immediate state changes.

## 5. Adopt controls as semantic units
Prefer **native platform controls** when they already provide stronger semantics and ergonomics. Persistent labels, help/error relationships, selection state, switches, progress and feedback are behavioral units, not decoration. Quiet/Soft/Glaze/Emphasis button roles replace arbitrary primary/secondary styling decisions for new 2.0 work.

## 6. Preserve accessibility from the beginning
Visible focus, a 48px general effective target floor, 56px TV floor, semantic names/states, large-text reflow, reduced motion/transparency, increased contrast, forced colors, color independence and effects-free fallbacks are first-pass requirements.

## 7. Use adaptation as a semantic transform
Width is one signal, not a device identity. Navigation may transform from phone Navigation Capsule to Tablet rail, Desktop sidebar, TV focus dock, wearable compact rotational navigation or spatial floating surface. Preserve semantic/focus order, current destination, state and task continuity.

## 8. Design explicitly for phone, tablet, and desktop
Mobile must not be a **shrunken tablet or desktop** shell. Tablet must not be a **stretched phone** layout. Desktop must not be an **enlarged mobile** shell. Form-factor selection also considers input, viewing distance, posture, resizability, platform conventions and task.

### TV
TV is a separate far-viewing, landscape-first environment. Use larger type/targets/spacing, overscan-safe essential content, shallow predictable focus groups, remote/D-pad directional navigation, clear focus/selection distinction, Select/Back-equivalent task flows and no pointer/swipe dependency for primary navigation.

### Foldables
Reserve physical hinges/folds as exclusion regions when required. Prefer pane-aware task composition, preserve continuity across posture/orientation changes, and never route an essential interactive target through an unusable hinge region.

### Smartwatch and wearables
Wearable UI is glance-first, compact and purpose-built. Do not shrink Mobile. Map rotational/crown input as an enhancement where supported while preserving touch or another native equivalent when the platform permits it. Product acceptance must cover native safe areas, accessibility, host-managed surfaces, interruption/restoration and representative hardware when shipped.

### Spatial
Use depth as supplemental hierarchy only. Anchored/floating controls remain semantic and usable when flattened; advanced graphics are never required for basic task completion. Hardware-specific spatial products require native/hardware acceptance.

## 9. Preserve logical order
Reachability, adaptive grouping and Connected Transformation may change visual allocation, never reading order, semantic meaning, authoritative state or keyboard/focus order.

## 10. Keep presentation local by default
Glaze UI 2.0 does not require analytics, trackers, remote fonts/icons, CDN UI dependencies, network calls or browser storage in the core design-system runtime.

## 11. Add an application contract test
Validate the subset consumed: exact current Stable version/revision, current material/token semantics, state/accessibility fallbacks, form-factor activation, Connected Transformation fallback, target floors, platform-specific input behavior and authority boundaries. Fail closed on a superseded version or missing required evidence.

## 12. Perform visual and product acceptance
Representative design-system browser profiles include Mobile 390×844; Tablet 820×1180; Desktop 1280×900; Wide Desktop 1600×1000; TV 1920×1080, plus representative foldable, wearable and spatial references. Review task flows, not screenshots alone. Native or hardware products add platform-specific native, accessibility, performance and real-device evidence.

## Migration from 1.6

Glaze UI 1.6.0 is the immediately preceding historical Stable baseline. Preserve working application semantics while replacing old material names, 44px legacy minima, navigation assumptions and motion/geometry choices with the 2.0 contract. Do not treat a successful 1.6 Adoption Candidate or historical conformance record as 2.0 evidence.

There are no production exceptions to the current-Stable target. Platform limitations, upstream constraints, schedule pressure, incomplete migration or technical inconvenience require additional implementation work; they do not permit release on a superseded or incomplete Glaze UI implementation.
