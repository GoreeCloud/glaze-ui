# Glaze UI 2.1 Android Handheld Native Reference

Status: **Candidate**  
Scope: **bounded native Android handheld design-system mapping**

`buildable/` is an original GoreeCloud-owned Android reference application for Glaze UI 2.1. It uses Android framework controls and layout primitives rather than WebView and requests no network permission.

The reference maps the 2.1 Candidate contract onto native Android behavior while keeping evidence boundaries explicit. It demonstrates solid Canvas/Surface content, a bounded Glaze interaction zone, 48 dp general and 56 dp Touch Assistance target floors, Light/Dark/Deep Dark appearance, true-black Deep Dark Canvas, Reduced Transparency → Solid interaction treatment, native `sp` text scaling and scroll/reflow, and text-labeled simulated Protected/Offline/Conflict states without asserting live GoreeCloud platform state.

## Toolchain

- Android Gradle Plugin 9.3.0
- Gradle 9.5.0 in CI with verified distribution checksum
- Java 17 source/target compatibility
- compileSdk 36
- targetSdk 36
- minSdk 28

## Android 16 edge-to-edge handling

Android 16 enforces edge-to-edge presentation for modern target SDKs. The reference therefore treats system-bar insets as a fixed scroll viewport boundary: the root `ScrollView` applies system window insets as clipping padding while the content itself retains its own Glaze spacing. This prevents content, including 200% text, from scrolling underneath status-bar or navigation-bar content while preserving the native edge-to-edge window model.

The action controls also remove framework elevation/state-list animation that would compete with the explicit Glaze surface treatment. The custom control backgrounds retain target floors and native Button semantics while keeping visual hierarchy deliberate.

## Exact-source emulator acceptance

`.github/workflows/glaze-2.1-android-native.yml` checks out the exact pull-request head, validates structure, resolves a stable Android Google APIs x86_64 image, installs the Android SDK/emulator and verified Gradle distribution, builds the debug APK, creates a deterministic handheld AVD without interactive `avdmanager` prompts, boots and installs the APK, then runs `scripts/validate_glaze_2_1_android_runtime.py`.

The runtime validator binds evidence to `git rev-parse HEAD` from the checked-out repository so a synthetic pull-request merge SHA cannot masquerade as the tested source revision. It validates three bounded native cases:

1. Light + Balanced — verifies 48 dp target behavior and the Ready → Completed native action transition.
2. Deep Dark + Reduced Transparency — verifies true-black Canvas, Solid interaction treatment and the 48 dp target floor.
3. Dark + 200% system text + Touch Assistance — captures the initial large-text rendering with system-bar inset protection, validates reachability after scroll, and verifies the 56 dp target floor.

A successful run publishes the debug APK, the three exact-run PNGs and `android-native-evidence.json` only after runtime acceptance succeeds.

## Evidence boundary

A green hosted emulator run is native Android **Candidate implementation/runtime evidence only**. It does not establish TalkBack or Switch Access acceptance, OEM-specific behavior, Moto G 2026 physical-device acceptance, real touch ergonomics, battery/performance behavior, interruption restoration, production signing or distribution, downstream application conformance, or human Visual Excellence acceptance.

Those evidence classes must remain separate and must not be inferred from source presence, APK build success, emulator execution or screenshots.