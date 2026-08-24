# Wear OS Build Harness

Status: **Development Candidate build evidence only**

This minimal Android application compiles the canonical `../GlazeWearableReference.kt` source and `../MainActivity.kt` entry point. It exists to produce exact-revision stable-SDK compilation evidence without turning the wearable candidate into a Stable Glaze UI contract.

Pinned build inputs:

- Android Gradle Plugin 9.3.0
- Kotlin Compose plugin 2.3.21
- Gradle 9.5.0, downloaded and SHA-256 verified by CI
- compileSdk 36
- targetSdk 36
- Android 16 stable SDK
- Wear Compose Material 3 1.5.0

The GitHub Actions `wear-os-build` job runs `gradle :app:assembleDebug --no-daemon --stacktrace` on the exact pull-request head. A successful job is compilation/debug-APK evidence only. It does not provide emulator execution, visual acceptance, TalkBack acceptance, touch/rotary task acceptance, signing/release evidence, battery evidence, interruption restoration, or real-device acceptance.
