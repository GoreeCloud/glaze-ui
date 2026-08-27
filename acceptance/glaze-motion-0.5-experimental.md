# Glaze Motion 0.5 Experimental Acceptance

Status: **Experimental evidence/governance iteration**  
Extends: **Glaze UI 1.5.0 Stable**  
Runtime compatibility baseline: **Motion Core 0.4.0**

## Purpose

Glaze Motion 0.5 advances Motion Core evidence from design-system-only reference validation to a merged first-party downstream evaluation. It does not add a new runtime primitive, activate Experimental Motion in production, or promote Motion Core to Candidate or Stable.

The 0.4 runtime and rendered matrix remain the implementation baseline. 0.5 adds governed consumer evidence and reconciles the current-Stable Glaze UI consumer registry with that downstream repository state.

## First-party downstream evidence

Consumer: **GoreeCloud Launcher**  
Repository: `GoreeCloud/goreecloud-launcher`  
Pull request: **#22 — Advance Launcher to Glaze UI 1.5 and add Motion evaluation**  
Exact validated head: `3095b9320b660f5e166465990d5d2bee061d7422`  
Squash merge revision: `23a389b3b24db726ceab5e328f9f8157fa7655ae`  
Merged: **2026-08-27 08:28:48 CDT**  
Android CI: **#67**

The exact pull-request head passed:

- repository privacy and manifest guards;
- the Glaze UI 1.5 Adoption Candidate contract;
- the test-only Glaze Motion evaluation quarantine contract;
- Room cutover and schema guards;
- Android lint, unit tests, and debug assembly;
- the retained Android 16 emulator runtime suite.

## Evaluated consumer behavior

Launcher evaluates Motion Core 0.4 semantics against its real workspace ordering domain while keeping all Experimental Motion mapping under `app/src/test`.

The downstream evidence demonstrates:

- Previous/Next semantic reorder commands map to Launcher's existing EARLIER/LATER domain operations.
- First/Last semantic reorder commands map to the existing stable-key target operation.
- Reorder results expose localization-neutral position metadata rather than design-system-owned English announcement copy.
- Missing stable keys fail closed and cannot invent a workspace state transition.
- Optional settling is rejected under reduced motion or local saturation without blocking semantic ordering state.
- The production surface retains explicit non-drag ordering and direct-manipulation cancellation paths.
- A repository guard rejects the `GlazeMotionExperimental` marker if it escapes into production Kotlin sources.

This is representative first-party consumer evidence because the tests exercise real Launcher domain primitives rather than a standalone design-system mock.

## Glaze UI consumer state

Launcher also migrated its bounded native Glaze UI mapping from historical 1.4 evidence to the exact Glaze UI 1.5.0 Stable release anchor `2e1618397f6ebcdd254a76bfdd7e98846f2c5aa3`.

Its central consumer state is therefore **Adoption Candidate**, not `aligned-current-stable`:

- target Glaze UI: 1.5.0;
- automated repository contract: present;
- production eligible on the Glaze UI gate: no;
- phone/tablet native, rendered, accessibility, reduced-motion, and physical-device acceptance: incomplete.

The test-only Glaze Motion evaluation does not satisfy those missing production gates.

## What 0.5 does not prove

This evidence does **not** establish:

- production activation of Glaze Motion in Launcher;
- native Android reduced-motion integration with the applicable operating-system accessibility preference;
- rendered Launcher Motion acceptance;
- physical-device Motion acceptance;
- assistive-technology or localized announcement acceptance;
- representative-device frame pacing, input latency, power, or settling-workload acceptance;
- full Launcher Glaze UI 1.5 product acceptance;
- Motion Core Candidate or Stable readiness.

The Android 16 emulator run is valid downstream application/runtime regression evidence, but it is not a Motion-specific rendered, accessibility, performance, or physical-device certification.

## Runtime compatibility boundary

0.5 is an evidence/governance iteration. The aggregate Motion Core runtime remains the 0.4 implementation in `js/glaze.motion.core.js`, with the 0.3 compatibility module and 0.4 accessibility/settling extensions unchanged.

Existing 0.4 runtime tests and the six-case Mobile/Desktop/TV normal/reduced-motion web/reference matrix remain required regression evidence for 0.5. No 0.5 claim depends on an unimplemented runtime API.

## Promotion boundary

Motion Core remains **Experimental** and outside the Glaze UI 1.5.0 Stable compatibility promise. Motion Studio and Motion Spatial remain Planned.

Before any Candidate proposal, Glaze Motion still requires additional representative consumer acceptance, applicable native and real-device evidence, accessibility and performance acceptance, compatibility/migration review, dependency/security/licensing review, and normal Glaze UI promotion governance. One merged test-only first-party evaluation is meaningful evidence but is not sufficient for Candidate promotion.
