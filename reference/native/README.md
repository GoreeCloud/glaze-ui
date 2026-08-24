# Glaze UI Wearable Native References

Status: **Development Candidate implementation evidence**

These native reference files map the Glaze UI wearable candidate contract onto representative platform-native UI frameworks:

- `wear-os/GlazeWearableReference.kt` — Compose for Wear OS reference using a vertical `TransformingLazyColumn`, native Material 3 semantics, current minimum interactive sizing, and platform rotary behavior.
- `watchos/GlazeWearableReference.swift` — SwiftUI watchOS reference using a vertical `ScrollView`, native Button semantics, Dynamic Type-compatible text, accessibility labels/values, and system Digital Crown scrolling behavior.

These files intentionally prefer native controls and navigation behavior where the operating system provides stronger accessibility, focus, ergonomics, battery, or input behavior. They are semantic mappings, not pixel-identical cross-platform implementations.

## Evidence boundary

Repository presence and source validation prove only that representative native mappings exist and remain aligned with the Development Candidate contract. They do **not** prove compilation against every current SDK, runtime correctness, emulator acceptance, watch hardware acceptance, battery behavior, complication/tile/widget behavior, screen-reader behavior, or production readiness.

Stable promotion still requires platform-native build evidence, round/rectangular visual acceptance, touch-only task completion, rotary/crown-enhanced task completion where supported, large-text and screen-reader acceptance, reduced-motion and reduced-transparency acceptance, interruption/state-restoration validation, and real-device validation for every supported wearable platform.
