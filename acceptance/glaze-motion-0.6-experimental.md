# Glaze Motion 0.6 Experimental Acceptance Record

## Experimental evidence/governance iteration

Glaze Motion 0.6 is an Experimental evidence and governance iteration. It adds no new Motion Core runtime primitive and does not change the current runtime implementation baseline. `js/glaze.motion.core.js` remains the **0.4.0** implementation baseline, and the retained 0.4 unit, interaction, accessibility, reference-consumer, and rendered acceptance matrix remains mandatory regression evidence.

Motion Studio and Motion Spatial remain Planned.

## First-party downstream evidence

### GoreeCloud Launcher

- Consumer state: **Glaze UI 1.5.0 Adoption Candidate**
- Evaluation: Glaze Motion 0.4, native Android test-only
- Pull request: **#22**
- Exact validated head: `3095b9320b660f5e166465990d5d2bee061d7422`
- Merged revision: `23a389b3b24db726ceab5e328f9f8157fa7655ae`
- Android CI: **#67**
- Production Experimental dependency: **no**
- Native/physical-device certification: **no**

Launcher maps Motion Core semantics into its real workspace ordering domain while retaining a fail-closed production quarantine.

### GoreeCloud Keyboard

- Consumer state: **Glaze UI 1.5.0 Adoption Candidate**
- Evaluation: Glaze Motion 0.5, native Android test-only
- Pull request: **#4**
- Exact validated head: `80de7bd2dcff6d07b06b19f8250e37d20155d7ff`
- Merged revision: `c9c0500263b40640339cf7a46f1a029d9a2ac240`
- Android CI: **#15**
- Runtime profile: Android 15 / API 35 / x86_64 emulator
- Production Experimental dependency: **no**
- Native/physical-device certification: **no**

Keyboard maps Motion Core timing, press-state, optional-settling, and reduced-motion semantics into its real first-party `KeyboardView` interaction path. The accepted emulator suite verifies that semantic input remains tied to actual key release and suggestion hit-testing while the Android animator duration scale is disabled and optional settling collapses.

## Troubleshooting retained as evidence

Keyboard Android CI #13 passed its build/governance job but failed the initial emulator reduced-motion assertion because `ValueAnimator.areAnimatorsEnabled()` did not reliably reflect the already-applied global animation-scale setting inside the instrumentation process. The emulator requirement was retained. The test was corrected to read Android's authoritative `Settings.Global.ANIMATOR_DURATION_SCALE` while preserving zero-duration, no-settling, key-release, and suggestion-selection assertions. Corrected exact head `80de7bd2dcff6d07b06b19f8250e37d20155d7ff` then passed both jobs in Android CI #15.

## What 0.6 does not prove

Two first-party native Android evaluations improve breadth but do not establish production Glaze Motion conformance. They do not prove:

- representative physical-device behavior;
- complete TalkBack, switch-access, keyboard/remote, or other assistive-technology acceptance across applicable consumers;
- representative frame pacing, input latency, power, thermal, memory, or settling-workload acceptance;
- full native/rendered Glaze UI product acceptance for Launcher or Keyboard;
- compatibility across the broader GoreeCloud consumer set;
- dependency, security, licensing, and release-governance readiness for production Motion adoption.

## Runtime compatibility boundary

Glaze Motion 0.6 keeps `runtimeCompatibilityBaseline: 0.4.0`. The 0.6 version identifies the evidence/governance state, not a new runtime API. Existing 0.4 runtime imports, semantics, and rendered regression evidence remain authoritative for implemented Motion Core behavior.

## Promotion boundary

This evidence remains insufficient for Candidate promotion. Candidate review still requires representative consumer and device evidence, applicable accessibility and performance acceptance, compatibility and migration review, dependency/security/licensing review, and normal Glaze UI governance. Experimental Motion must remain non-mandatory and non-production for downstream consumers until those gates are satisfied.
