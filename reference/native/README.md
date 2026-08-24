# Glaze UI Wearable Native References

Status: **Development Candidate implementation evidence**

These native reference files map the Glaze UI wearable candidate contract onto representative platform-native UI frameworks:

- `wear-os/buildable/app/src/main/kotlin/com/goreecloud/glazeui/reference/wearable/GlazeWearableReference.kt` — canonical Compose for Wear OS reference using a vertical `TransformingLazyColumn`, native Material 3 semantics, current minimum interactive sizing, and platform rotary behavior.
- `wear-os/buildable/app/src/main/kotlin/com/goreecloud/glazeui/reference/wearable/MainActivity.kt` plus the surrounding `wear-os/buildable/` project — minimal reproducible Android application harness against a pinned stable-platform toolchain: AGP 9.3.0, Kotlin Compose plugin 2.3.21, compileSdk/targetSdk 36 for stable Android 16, Wear Compose Material 3 1.5.0, and verified Gradle 9.5.0.
- `watchos/GlazeWearableReference.swift` — SwiftUI watchOS reference using a vertical `ScrollView`, native Button semantics, Dynamic Type-compatible text, accessibility labels/values, and system Digital Crown scrolling behavior.
- `watchos/GlazeWearableReferenceApp.swift` — minimal `@main App` entry point used by the watchOS SDK typecheck and simulator build/runtime gates.

The Wear OS reference uses the conventional Android app source tree so source inputs cannot overlap Gradle build outputs. These files intentionally prefer native controls and navigation behavior where the operating system provides stronger accessibility, focus, ergonomics, battery, or input behavior. They are semantic mappings, not pixel-identical cross-platform implementations.

## Build and SDK evidence boundary

The Wear OS harness is intentionally unsigned and non-production. A successful `:app:assembleDebug` CI result proves only that the reference source compiles into a debug APK against the pinned SDK/toolchain on the recorded exact repository revision. It does not by itself prove emulator execution, visual acceptance, TalkBack behavior, rotary task completion, battery behavior, interruption restoration, signing/release readiness, or real-device acceptance.

The separate Wear OS emulator runtime gate resolves the current stable `android-wear` x86_64 system image exposed by the hosted Android SDK, installs the emulator dependencies, creates a disposable Wear OS AVD, rebuilds the exact Development Candidate APK, boots the emulator, installs the package, launches `MainActivity`, verifies the resumed activity, captures a non-empty PNG runtime screenshot as execution evidence, and force-stops the package. A successful gate establishes basic install/launch runtime compatibility on the recorded hosted Wear OS emulator environment. It does not establish native visual acceptance, TalkBack acceptance, rotary task acceptance, interruption/state restoration, battery/performance behavior, production signing, distribution readiness, or real-device acceptance.

The harness deliberately uses stable Android 16/API 36 for compilation rather than Android 17/API 37 preview because the hosted runner's SDK repository does not currently expose the API 37 preview platform. Preview-SDK availability is not allowed to masquerade as a Glaze UI source failure. The emulator runtime gate independently resolves the newest stable Wear OS x86_64 image actually exposed by `sdkmanager`, so hosted-image lifecycle changes remain visible in CI rather than being silently treated as application source failures.

The `watchos-sdk-typecheck` CI job runs on a controlled macOS runner, records the installed Xcode and watchOS SDK versions, verifies the exact repository revision, and typechecks both SwiftUI source files against the watchOS SDK with an arm64 watchOS target. A successful typecheck proves SDK-level Swift source compatibility only. It is not an Xcode archive, signed watch application build, simulator launch, UI acceptance record, accessibility-runtime result, performance result, or real-device result.

The `watchos-simulator-build` CI job uses the watchOS Simulator SDK on the controlled macOS runner to compile and link the same SwiftUI sources for `arm64-apple-watchos10.0-simulator`, package them into a minimal `GlazeWearableReference.app`, validate its property list, and apply and verify an ad-hoc CI signature. This packaged watchOS Simulator bundle is then installed onto an available watchOS Simulator; the job boots the simulator, launches the exact bundle identifier, confirms a launch process result, and terminates it cleanly.

A successful watchOS Simulator launch gate proves simulator-target compile/link/package compatibility plus basic install/launch/terminate runtime compatibility on the recorded hosted simulator environment. It does not prove visual correctness, round/rectangular layout acceptance, Digital Crown task completion, VoiceOver behavior, Dynamic Type acceptance, reduced-motion or reduced-transparency behavior, interruption/state restoration, performance, battery behavior, production signing, App Store packaging, or real-device acceptance.

## Evidence boundary

Repository presence, source validation, successful Wear OS debug compilation, a successful Wear OS emulator runtime gate, successful watchOS SDK typechecking, and successful watchOS Simulator package/runtime gates remain Development Candidate implementation evidence. They do **not** prove full runtime correctness, UI/accessibility acceptance, watch hardware acceptance, battery behavior, complication/tile/widget behavior, or production readiness.

Stable promotion still requires native round/rectangular visual acceptance, touch-only task completion, rotary/crown-enhanced task completion where supported, large-text and screen-reader acceptance, reduced-motion and reduced-transparency acceptance, interruption/state-restoration validation, production packaging/signing evidence where applicable, and real-device validation for every supported wearable platform.
