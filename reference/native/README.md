# Glaze UI Wearable Native References

Status: **Development Candidate implementation evidence**

These native reference files map the Glaze UI wearable candidate contract onto representative platform-native UI frameworks:

- `wear-os/GlazeWearableReference.kt` — Compose for Wear OS reference using a vertical `TransformingLazyColumn`, native Material 3 semantics, current minimum interactive sizing, and platform rotary behavior.
- `wear-os/MainActivity.kt` plus `wear-os/buildable/` — minimal reproducible Android application harness for compiling the same reference composable against a pinned stable-platform toolchain: AGP 9.3.0, Kotlin Compose plugin 2.3.21, compileSdk/targetSdk 36 for stable Android 16, Wear Compose Material 3 1.5.0, and verified Gradle 9.5.0.
- `watchos/GlazeWearableReference.swift` — SwiftUI watchOS reference using a vertical `ScrollView`, native Button semantics, Dynamic Type-compatible text, accessibility labels/values, and system Digital Crown scrolling behavior.

These files intentionally prefer native controls and navigation behavior where the operating system provides stronger accessibility, focus, ergonomics, battery, or input behavior. They are semantic mappings, not pixel-identical cross-platform implementations.

## Build evidence boundary

The Wear OS harness is intentionally unsigned and non-production. A successful `:app:assembleDebug` CI result proves only that the reference source compiles into a debug APK against the pinned SDK/toolchain on the recorded exact repository revision. It does not prove emulator execution, visual acceptance, TalkBack behavior, rotary task completion, battery behavior, interruption restoration, signing/release readiness, or real-device acceptance.

The harness deliberately uses stable Android 16/API 36 rather than Android 17/API 37 preview because the hosted runner's SDK repository does not currently expose the API 37 preview platform. Preview-SDK availability is not allowed to masquerade as a Glaze UI source failure.

The watchOS reference remains source-only until an explicitly controlled macOS/Xcode build path is added and validated. Repository source presence must not be represented as watchOS compilation evidence.

## Evidence boundary

Repository presence and source validation prove only that representative native mappings exist and remain aligned with the Development Candidate contract. They do **not** prove runtime correctness, emulator/simulator acceptance, watch hardware acceptance, battery behavior, complication/tile/widget behavior, screen-reader behavior, or production readiness.

Stable promotion still requires platform-native build evidence for every supported platform, round/rectangular visual acceptance, touch-only task completion, rotary/crown-enhanced task completion where supported, large-text and screen-reader acceptance, reduced-motion and reduced-transparency acceptance, interruption/state-restoration validation, and real-device validation for every supported wearable platform.
