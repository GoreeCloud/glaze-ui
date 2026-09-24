# Glaze UI — Planned Features

**Status:** Active planned-feature control  
**As of:** 2026-09-24  
**Canonical lifecycle authority:** `registry/lifecycle.json`  
**Canonical repository:** `GoreeCloud/glaze-ui`  
**Current Official Stable:** GLAZE UI V1.6 / `1.6.0`

## Purpose

This file is the repository-native authority for planned, active, recommended, and otherwise not-yet-complete Glaze UI feature obligations. It does not establish implementation, qualification, lifecycle promotion, consumer eligibility, deployment, or production acceptance.

The detailed planned successor specification for V1.7 is `GLAZE_UI_V1_7_PLANNED.md`.

## Planned and Active Obligations

| ID | Feature / obligation | Priority | Current state |
| --- | --- | --- | --- |
| FR-001 | Reconcile and maintain every current planned or recommended Glaze UI feature from authoritative project records and verified repository evidence in this roadmap. | High | Ongoing control. |
| FR-002 | Move actionable feature obligations into GoreeCloud Tasks Management when required, preserving priority, dependency, blocker, and lifecycle disposition. | High | Ongoing control. |
| FR-003 | Do not mark features implemented, complete, cancelled, superseded, RC, Stable, deployed, or production-accepted without authoritative evidence and synchronized repository/Drive/task records. | High | Ongoing control. |
| FR-010 | Drive current-Stable adoption across GoreeCloud-controlled user-facing consumers without allowing platform-level Stable status to imply application-level acceptance. | P0 | Ongoing consumer migration/acceptance work; required target is `1.6.0`, while consumers remain separately evidence-gated. |
| FR-011 | Reconcile stale historical documentation and roadmap records that still identify older Glaze releases as current, without rewriting immutable historical evidence. | High | Active documentation-control work; current repository authority surfaces are reconciled for V1.6.0 while older records remain historical provenance. |
| FR-017 | Establish downstream V1.6 application adoption profiles only after shared V1.6 lifecycle and acceptance state make consumer migration valid. | High | Active — shared V1.6.0 is Stable; every consumer now requires fresh repository-local adoption and acceptance evidence. |
| FR-018 | Design and implement GLAZE UI V1.7 around the planned Interaction Continuity contract, including task continuity, Adaptive Input 2.0, first-class form-factor profiles, adaptive composition, command surfaces, Personalization 2.0, shell continuity, notification/activity surfaces, native Glaze kits, expanded adaptive components, Glaze Inspector/Studio, continuity-aware motion, accessibility continuity, native cross-device consistency, performance/energy awareness, and evidence-driven V1.7 acceptance. | P0 | In progress — `1.7.0-dev.8` retains the bounded Development foundations for Task Continuity, Adaptive Input 2.0, First-Class Form-Factor Profiles, Adaptive Composition, GlzCommandSurface, Personalization 2.0, System Shell Continuity, and Notification and Activity Surfaces, and adds Native Glaze Kits for section 9, bringing implemented Development sections to 1–9. The source mapping covers Android / Jetpack Compose, Apple / SwiftUI, Web, and supported Linux native UI environments while keeping native controls, capabilities, accessibility, privacy/security truth, permissions, consent, availability, and execution authority external and fail-closed. The overall V1.7 obligation remains open; broader adaptive component expansion, Inspector/Studio, continuity-aware motion, accessibility continuity, cross-device consistency, representative/native-device qualification, performance/energy qualification, Candidate/RC/Stable promotion, consumer eligibility, deployment, and production acceptance remain separate. |

## V1.7 Planning Boundary

GLAZE UI V1.6 / `1.6.0` remains the current Official Stable shared target. V1.7 planning must not change `VERSION`, `registry/lifecycle.json`, current Stable runtime entrypoints, published V1.6 release evidence, or downstream consumer eligibility.

Any V1.7 implementation must remain presentation-focused, preserve provider authority, and fail closed rather than inventing authentication, authorization, privacy, security, consent, permission, capability, connectivity, data-integrity, recovery, or acceptance truth.

## Qualification Boundary

Automated validation alone must not establish V1.7 acceptance. Claimed V1.7 support requires applicable exact-revision evidence for source behavior, semantics, accessibility, inputs, adaptive composition, form factors, continuity, representative rendering, performance, native-platform behavior, regression, human review, assistive technology, security/privacy boundaries, and artifact provenance.

## Maintenance

Keep this file synchronized with verified repository implementation state, `registry/lifecycle.json`, the canonical Drive navigation index `GoreeCloud/Sources/Glaze-UI-Index`, and applicable GoreeCloud task records. Planned work must remain planned until authoritative implementation and acceptance evidence establishes another state.
