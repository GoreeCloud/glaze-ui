# Glaze UI Wearable Contract Record

## Current authority

- Current Stable design contract: **Glaze UI 2.1.0**.
- Canonical release boundary: `GLAZE_UI_2_1_STABLE.md`.
- Preserved 2.0 Stable contract: `GLAZE_UI_2_STABLE.md`.
- Exact 2.0 pre-promotion design snapshot: `GLAZE_UI_2.md` and `tokens/glaze-2.candidate.json`.
- Current platform-neutral wearable implementation remains the promoted 2.x mapping in `css/glaze-2.emerging.candidate.css`, `js/glaze-2.emerging.candidate.js`, `reference/candidate-2.0-emerging.html`, and `scripts/validate_candidate_2_emerging.py`; 2.1 carries that behavior forward without claiming new native hardware certification.
- Native-device certification: not established by the browser reference.

Glaze UI 2.1 retains wearable navigation as **compact rotational navigation**. Wearable UI is glance-first, near-view, short-session and interruption-tolerant; it is **not a shrunken phone UI**.

## Stable design-system boundary

The current reference establishes compact circular composition, a 48px effective interaction floor, one current/roving-focus navigation target, wheel/directional-key rotational semantics, reduced-motion behavior, semantic color independence and readable Solid fallback when transparency is reduced. These are Stable design-system semantics.

This platform-neutral evidence **does not certify a Wear OS crown, watchOS Digital Crown**, device safe area, host-managed complication/tile, battery policy, native spoken accessibility API, interruption lifecycle or physical-device performance. A consumer shipping those behaviors requires **application-specific native or real-device acceptance**.

## Durable rules

- Preserve safe regions around round edges, curved corners, bezels and system-reserved areas.
- Keep hierarchy shallow and prioritize one dominant status, task or action.
- Prefer vertically ordered flows/progressive disclosure over miniature phone/desktop dashboards.
- Optional rotary input must not remove an equivalent touch/native task path when the platform permits one.
- Keep selected/focused state visible for non-touch input.
- Use platform-native progress, selection, back/dismiss and host-surface semantics when they are stronger.
- Do not expose sensitive state merely because a surface is glanceable.
- Do not let motion, translucency or advanced rendering become required for task completion.
- Never strengthen Wardveil Security, Privacy Shield, Everkeep or GoreeCloud Mesh claims beyond underlying evidence.

## Historical native evidence

The repository retains **historical 1.x native evidence** and Development Candidate artifacts in `tokens/wearable.candidate.tokens.json`, `css/glaze.wearable.candidate.css`, `reference/wearable-candidate.html`, `reference/native/wear-os/`, `reference/native/watchos/`, and `acceptance/wearable-native-evidence.template.json`.

Those artifacts remain useful for audit and future native mapping research, but they were produced against earlier Glaze UI semantics. They must not be reinterpreted as 2.1 native certification. The manual Wear OS emulator workflow remains deferred development/reference evidence unless a product-specific 2.1 acceptance record explicitly binds a tested revision and environment.

## Validation boundary

`scripts/validate_wearables.py` validates current 2.1 Stable wearable semantics, preserved 2.0 promotion provenance and isolation of historical 1.x native artifacts. `scripts/validate_candidate_2_emerging.py` supplies retained browser-rendered wearable/spatial acceptance. Neither validator certifies a downstream physical device.
