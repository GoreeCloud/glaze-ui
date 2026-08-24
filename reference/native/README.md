# Glaze UI Wearable Native References

Status: **Development Candidate implementation evidence**

These native reference files map the Glaze UI wearable candidate contract onto representative platform-native UI frameworks:

- `wear-os/buildable/app/src/main/kotlin/com/goreecloud/glazeui/reference/wearable/GlazeWearableReference.kt` — canonical Compose for Wear OS reference using a vertical `TransformingLazyColumn`, native Material 3 semantics, current minimum interactive sizing, and platform rotary behavior.
- `wear-os/buildable/app/src/main/kotlin/com/goreecloud/glazeui/reference/wearable/MainActivity.kt` plus the surrounding `wear-os/buildable/` project — minimal reproducible Android application harness against a pinned stable-platform toolchain: AGP 9.3.0, Kotlin Compose plugin 2.3.21, compileSdk/targetSdk 36 for stable Android 16, Wear Compose Material 3 1.5.0, and verified Gradle 9.5.0.
- `watchos/GlazeWearableReference.swift` — SwiftUI watchOS reference using a vertical `ScrollView`, native Button semantics, Dynamic Type-compatible text, accessibility labels/values, and system Digital Crown scrolling behavior.
- `watchos/GlazeWearableReferenceApp.swift` — minimal `@main App` entry point used by the watchOS SDK typecheck gate.

The Wear OS reference uses the conventional Android app source tree so source inputs cannot overlap Gradle build outputs. These files intentionally prefer native controls and navigation behavior where the operating system provides stronger accessibility, focus, ergonomics, battery, or input behavior. They are semantic mappings, not pixel-identical cross-platform implementations.

## Build and SDK evidence boundary

The Wear OS harness is intentionally unsigned and non-production. A successful `:app:assembleDebug` CI result proves only that the reference source compiles into a debug APK against the pinned SDK/toolchain on the recorded exact repository revision. It does not prove emulator execution, visual acceptance, TalkBack behavior, rotary task completion, battery behavior, interruption restoration, signing/release readiness, or real-device acceptance.

The harness deliberately uses stable Android 16/API 36 rather than Android 17/API 37 preview because the hosted runner's SDK repository does not currently expose the API 37 preview platform. Preview-SDK availability is not allowed to masquerade as a Glaze UI source failure.

The `watchos-sdk-typecheck` CI job runs on a controlled macOS runner, records the installed Xcode and watchOS SDK versions, verifies the exact repository revision, and typechecks both SwiftUI source files against the watchOS SDK with an arm64 watchOS target. Exact-head CI #240 on commit `45d289b46e312846c01f9a210dfbe0244daec80f` completed this gate successfully. That result proves SDK-level Swift source compatibility only. It is not an Xcode archive, signed watch application build, simulator launch, UI acceptance record, accessibility-runtime result, performance result, or real-device result.

## Evidence boundary

Repository presence, source validation, successful Wear OS debug compilation, and successful watchOS SDK typechecking remain Development Candidate implementation evidence. They do **not** prove runtime correctness, emulator/simulator acceptance, watch hardware acceptance, battery behavior, complication/tile/widget behavior, screen-reader behavior, or production readiness.

Stable promotion still requires packaged platform build evidence where applicable, round/rectangular visual acceptance, touch-only task completion, rotary/crown-enhanced task completion where supported, large-text and screen-reader acceptance, reduced-motion and reduced-transparency acceptance, interruption/state-restoration validation, and real-device validation for every supported wearable platform.
