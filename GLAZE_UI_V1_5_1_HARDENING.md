# GLAZE UI V1.5.1 — Qualification Hardening

**Lifecycle:** Development follow-up after V1.5.0 Stable  
**Planned version:** `1.5.1`  
**Stable baseline:** `1.5.0`  
**Originating reviewed V1.5.0 implementation anchor:** `ee1032a0822ab8e103f8afe48e5c1859fde65cc9`  
**Scope decision date:** 2026-09-15

## Purpose

V1.5.1 is the governed follow-up qualification release for the two review obligations intentionally moved out of the bounded V1.5.0 Stable scope by explicit project-owner direction.

This document does not mark either obligation passed. Both remain open until real evidence is collected against an exact V1.5.1 candidate revision.

## Mandatory V1.5.1 qualification work

### 1. `performance-representative-budget`

Measure representative Glaze UI interaction and rendering behavior against the active **Standard — Glaze UI Performance Budget v1.0**.

Required acceptance includes the governed numeric thresholds and sample sizes, including resolver percentiles, interaction-to-painted-update percentiles, refresh-adaptive active-frame continuity, severe-stall rate, catastrophic-stall exclusion, and preservation of task/authority boundaries.

V1.5.0 does **not** claim that this new numeric budget was measured or passed.

### 2. `platform-posture-continuity`

Verify supported fold, unfold, posture, rotation, and related form-factor transitions on a representative physical device or approved target runtime.

Evidence must preserve task state, destination/state continuity, semantic hierarchy, capability truth, authorization boundaries, and the prohibition on automatic navigation/permission/consequential/fallback execution.

V1.5.0 does **not** claim foldable/posture target-runtime acceptance.

## Carry-forward requirements

V1.5.1 must preserve the V1.5.0 Stable behavior and all previously accepted V1.5 qualification boundaries unless an intentionally versioned change is separately reviewed. In particular, V1.5.1 must preserve:

- truthful capability and provider authority;
- Privacy Shield and Wardveil Security authority boundaries;
- no inferred authorization or consent;
- no automatic permission request, consequential execution, fallback execution, or navigation;
- task and page continuity;
- stable primary-action ordering;
- accessibility presentation precedence;
- privacy-minimized diagnostics;
- graceful offline, degraded, constrained-runtime, and unsupported-effect behavior.

## Promotion boundary

V1.5.1 may not be represented as Stable solely because these tasks exist or because V1.5.0 is Stable. Stable V1.5.1 requires exact-revision implementation, validation, applicable human/target-runtime evidence, lifecycle approval, and authoritative release-state verification.
