# Buildable Android Handheld Reference

This project is the minimal buildable harness for the Glaze UI 2.1 Android handheld Candidate reference.

Toolchain contract:

- Android Gradle Plugin: 9.3.0
- compileSdk / targetSdk: 36
- minSdk: 28
- Java: 17
- CI Gradle distribution: verified 9.5.0
- application ID: `com.goreecloud.glazeui.reference.android`

The implementation uses Android framework UI primitives only. It does not use WebView and does not require an application UI framework dependency.

Test-only Intent extras are accepted by `MainActivity` so CI can render deterministic Candidate states:

- `appearance`: `light`, `dark`, or `deep-dark`
- `reducedTransparency`: boolean
- `touchAssistance`: boolean

These extras are a reference-harness control surface, not a GoreeCloud preference-storage or device-policy implementation.
