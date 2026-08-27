# Glaze Motion 0.2 Experimental Acceptance Record

Status: **Experimental development evidence — not Stable promotion evidence**

## Scope
This record covers the Glaze Motion Motion Core 0.2 development layer only. It does not promote Glaze Motion, Motion Studio, or Motion Spatial into the Glaze UI Stable compatibility promise.

## Implemented evidence
- Direct-manipulation drag sessions with activation slop, axis locking, velocity calculation, completion, and cancellation.
- Deterministic velocity-projected snap-point selection against declared destinations.
- Shared-element naming and View Transition delegation with state-preserving fallback.
- Semantic component adapters for button, disclosure, dialog, navigation, reorder, and shared-element roles.
- Reduced-motion separation between direct input tracking and post-gesture settling travel.
- Bounded spring output enforced in runtime generation.
- Source validation, runtime tests, interaction tests, and a dedicated rendered harness.

## Required development checks
- `python3 scripts/validate_glaze_motion.py`
- `node --test tests/glaze-motion-runtime.test.mjs tests/glaze-motion-interaction.test.mjs`
- `python3 scripts/validate_glaze_motion_rendered.py`
- Full Glaze UI CI for the exact proposed revision.

## Acceptance boundary
Passing these checks demonstrates that the 0.2 Experimental source is internally consistent and suitable for continued development. It does not certify downstream GoreeCloud applications, native platform mappings, real-device performance, battery impact, or a Stable release.

Motion Studio and Motion Spatial remain Planned. Candidate promotion for Motion Core requires broader representative consumer evidence, accessibility review, performance evidence, compatibility/migration review, and normal Glaze UI lifecycle promotion.
