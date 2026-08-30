# Glaze UI 2.1 Android Handheld Native Reference

Status: **Candidate native implementation evidence**

This directory contains a bounded, original GoreeCloud-owned Android handheld reference for Glaze UI 2.1. It maps Candidate semantics onto Android-native framework controls rather than embedding the web reference or adopting a third-party application implementation.

The buildable reference demonstrates:

- solid Canvas/Surface content composition;
- a bounded Glaze interaction zone;
- the 48 dp general interaction-target floor;
- a 56 dp Touch Assistance floor;
- Light, Dark and Deep Dark appearance mappings;
- true-black Deep Dark canvas behavior;
- Reduced Transparency resolving the interaction treatment to Solid;
- native `sp` text scaling inside a scrollable/reflowing layout;
- explicit, text-labeled Protected, Offline and Conflict reference states that do not rely on hue alone; and
- a native button state transition that can be exercised by the emulator acceptance harness.

All displayed platform states are explicitly simulated reference content. The reference does not query, infer or claim live Wardveil Security, Privacy Shield, Everkeep, GoreeCloud Identity, GoreeCloud Sync or GoreeCloud Mesh state.

## Evidence boundary

The reference is intentionally small and unsigned. A successful Android Gradle build proves source/toolchain compatibility for the exact tested repository revision. A successful emulator gate additionally proves install, launch, deterministic preference-harness input, minimum-target inspection, explicit action-state transition, large-text reflow reachability and screenshot capture on the recorded hosted Android emulator environment.

Neither result is physical-device acceptance. Emulator automation does not prove TalkBack, Switch Access, touch ergonomics, OEM rendering, battery/performance behavior, interruption/state restoration, production signing, store packaging, or representative Moto G 2026 behavior. Those remain separate evidence.
