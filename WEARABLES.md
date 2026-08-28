# Glaze UI Wearable Contract Record

## Current authority

- Current enforced active-development design contract: **Glaze UI 2.0.0 Candidate** in `GLAZE_UI_2.md`.
- Last validated Stable implementation baseline: **Glaze UI 1.6.0**.
- Current 2.0 wearable implementation evidence: `css/glaze-2.emerging.candidate.css`, `js/glaze-2.emerging.candidate.js`, `reference/candidate-2.0-emerging.html`, and `scripts/validate_candidate_2_emerging.py`.
- Native-device certification: **not established by the 2.0 browser reference**.

Glaze UI 2.0 defines wearable navigation as **compact rotational navigation**. Wearable UI remains glance-first, near-view, short-session, interruption-tolerant, and platform-adaptive; it is not a shrunken phone UI.

## Current 2.0 design-system boundary

The 2.0 Candidate reference establishes a compact circular composition, 48px effective target floor, one selected/roving-focus navigation target, wheel and directional-key parity, and reduced-motion behavior. The implementation is platform-neutral design-system evidence. It does not claim that a Wear OS crown, watchOS Digital Crown, native screen reader, system-hosted complication/tile, device safe area, battery policy, or interruption lifecycle has been accepted on hardware.

Consumer-native implementations must still prove the platform behaviors they actually ship, including native input mapping, touch-only task completion where applicable, safe-area/edge behavior, large text, spoken semantics, reduced motion/transparency, interruption/restoration, performance, host-managed surfaces, and real-device acceptance before product production approval.

## Historical 1.x precursor evidence

The repository also retains an earlier **1.x Wearable Development Candidate** as historical design and implementation evidence. Its token/CSS/reference/native artifacts include:

- `tokens/wearable.candidate.tokens.json`;
- `css/glaze.wearable.candidate.css`;
- `reference/wearable-candidate.html`;
- `reference/native/wear-os/`;
- `reference/native/watchos/`;
- `acceptance/wearable-native-evidence.template.json`;
- `.github/workflows/wear-os-emulator.yml`.

Those artifacts were developed against earlier Glaze UI semantics and are preserved for audit, migration research, and future native mapping work. They **must not be reinterpreted as Glaze UI 2.0 native acceptance** and do not change the current Stable baseline. The manual Wear OS emulator workflow remains a development/reference check unless a future 2.0 native acceptance record explicitly binds a tested revision and promotes that evidence.

## Durable wearable rules carried into 2.0

The following non-version-specific constraints remain valid because they are consistent with the enforced 2.0 contract:

- preserve safe regions around round edges, curved corners, bezels, and system-reserved areas;
- keep hierarchy shallow and prioritize one dominant status, task, or action;
- prefer vertically ordered flows and progressive disclosure over dense dashboards or miniature desktop/mobile layouts;
- keep essential tasks available without requiring optional rotary input unless the operating system itself defines otherwise;
- keep selected/focused state visible for non-touch input;
- use native progress, selection, back/dismiss, and host-surface semantics when a consumer platform provides them;
- do not expose sensitive state merely because a wearable is glanceable;
- do not let decorative motion, translucency, or advanced rendering become necessary for task completion;
- never strengthen Wardveil Security, Privacy Shield, Everkeep, or GoreeCloud Mesh claims beyond underlying evidence.

## Validation boundary

`scripts/validate_wearables.py` now validates this lifecycle separation and the binding between the enforced 2.0 wearable semantics and the current Candidate implementation. `scripts/validate_candidate_2_emerging.py` supplies rendered 2.0 wearable/spatial acceptance. Neither validator certifies a physical wearable device or downstream application.
