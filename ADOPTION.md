# Adopting Glaze UI

Glaze UI 1.4.0 is the current Stable baseline and is mandatory for every GoreeCloud-controlled user-facing application. Existing consumers on older releases are migration-required; controlled migration is mandatory, and superseded Glaze UI versions cannot satisfy production readiness.

## 1. Record the target version
Record the **current Stable** semantic version, reviewed canonical source revision, repository-local evidence, automated contract, and product-specific acceptance boundary. A superseded version may be recorded only as historical or migration evidence.

## 2. Map semantics before visuals
Map existing canvas/surfaces/text/status/spacing/radii/focus/motion/forms/selection/navigation and form-factor contexts to Glaze semantics before replacing successful product composition.

## 3. Use the material hierarchy intentionally
Ordinary content defaults to Solid/Raised. Functional Glass belongs primarily to functional chrome. Clear Glass is limited to controls over rich media.

## 4. Adopt expression by role
Use Compact/Standard/Expressive/Hero/Pressed shapes and effects/spatial motion according to hierarchy. Reduced motion removes nonessential scale, morphing, rebound, and spatial transformation.

## 5. Adopt controls as semantic units
Prefer **native platform controls** when they already provide stronger semantics and ergonomics. Persistent labels, help/error relationships, selection state, switches, progress, and feedback are behavioral units, not decoration.

## 6. Preserve accessibility from the beginning
Visible focus, practical targets, semantic names/states, reduced motion/transparency, increased contrast, forced colors, and solid fallbacks are first-pass requirements. TV focus is primary navigation behavior.

## 7. Use breakpoints as window signals
Compact <=599, Medium 600–1023, Expanded 1024–1439, Wide >=1440. Width does not determine the full form factor; TV requires far-view/directional-input context.

## 8. Design explicitly for phone, tablet, and desktop
Mobile must not be a **shrunken tablet or desktop** shell. Tablet must not be a **stretched phone** layout. Desktop must not be an **enlarged mobile** shell. Form-factor selection also considers input, viewing distance, posture, resizability, platform conventions, and task.

### TV
TV is a separate far-viewing, landscape-first environment. Use larger type/targets/spacing, overscan-safe essential content, shallow predictable focus groups, remote/D-pad directional navigation, clear focus/selection distinction, Select/Back-equivalent task flows, and no pointer/swipe dependency for primary navigation.

### Smartwatch and wearables
Smartwatch and wearable applications are fully subject to the current-Stable requirement. Do not approximate a wearable application by shrinking Mobile. If the current Stable Glaze UI release does not yet contain an applicable Stable wearable interaction contract, the application remains development-only and production-blocked until that contract is implemented, validated, and promoted Stable.

## 9. Preserve logical order
Reachability and adaptive grouping may change visual allocation, never reading order, semantic meaning, or keyboard/focus order.

## 10. Keep presentation local by default
Glaze UI does not require analytics, trackers, remote fonts/icons, or third-party UI runtimes.

## 11. Add an application contract test
Validate the subset actually consumed: current-Stable version/revision, semantic tokens, states, material boundaries, accessibility fallbacks, form-factor activation, and directional focus where applicable. Fail closed on a superseded version or missing required Stable platform contract.

## 12. Perform visual acceptance
Representative current 1.4 profiles: Mobile 390×844; Tablet 820×1180; Desktop 1280×900; Wide Desktop 1600×1000; TV 1920×1080. Review task flows, not screenshots alone. Add native/real-device evidence for every other supported user-facing platform, including smartwatch/wearable targets once an applicable Stable Glaze UI contract exists.

## Platform-native clients
Native Android, iOS/iPadOS/tvOS, Linux, desktop, smartwatch/wearable, or other implementations map Glaze semantics into platform-native controls, focus/input systems, density units, safe areas, windowing, and accessibility. Current-Stable design-system status never waives application-specific native or real-device acceptance.

There are no production exceptions to the current-Stable target. Platform limitations, upstream UI constraints, schedule pressure, incomplete migration, or technical inconvenience require additional implementation work or a Glaze UI platform-contract enhancement; they do not permit release on a superseded or incomplete Glaze UI implementation.
