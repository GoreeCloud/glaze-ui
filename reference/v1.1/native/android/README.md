# GLAZE UI V1.1 — Android Handheld Release-Candidate Reference

This directory contains the bounded framework-native Android handheld reference used to generate fresh V1.1 platform-native evidence.

It is intentionally a reference harness, not a downstream GoreeCloud application and not a declaration that every Android consumer conforms to V1.1.

## Toolchain

- Android Gradle Plugin: 9.3.0
- compileSdk / targetSdk: 36
- minSdk: 28
- Java: 17
- CI Gradle distribution: verified 9.5.0
- application ID: `com.goreecloud.glazeui.reference.v11`
- UI implementation: Android framework primitives only; no WebView and no application UI-framework dependency

## Deterministic acceptance controls

The reference accepts test-only Intent extras so CI can render governed states:

- `appearance`: `light`, `dark`, or `deep-dark`
- `reducedTransparency`: boolean
- `touchAssistance`: boolean

These extras are test-harness controls only. They do not implement GoreeCloud preference storage, device policy, Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Identity, or GoreeCloud Mesh truth.

## Evidence boundary

The emulator gate proves a bounded Android framework-native mapping for the V1.1 optical contract, target geometry, appearance roles, and Reduced Transparency fallback. It does not by itself establish OEM-wide behavior, physical-device qualification, TalkBack certification, app signing/distribution, downstream consumer conformance, or production deployment.
