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
| FR-018 | Design and implement GLAZE UI V1.7 around Interaction Continuity + Personal Expression, including Task Continuity, Adaptive Input 2.0, first-class form-factor profiles, adaptive composition, GlzCommandSurface, Advanced Theme Manager 2.0, layered theme architecture, Semantic Color System 2.0, protected semantic colors, semantic prominence/layering, intelligent palette generation, color-coded navigation/system/connectivity/data visualization, theme accessibility and safety, declarative theme packages, local-first theme generation, shell continuity, notification/activity surfaces, native Glaze kits, expanded adaptive/personalization components, Glaze Inspector/Studio, continuity-aware motion, accessibility continuity, cross-device consistency, privacy/authority boundaries, performance/energy awareness, and evidence-driven V1.7 acceptance. | P0 | In progress — `1.7.0-dev.11` is the latest bounded Development aggregate. `1.7.0-dev.10` remains the verified v1.1 Section 25 Expanded Component System foundation; `1.7.0-dev.9` remains the verified Section 24 Native Glaze Kits source-mapping foundation; `1.7.0-dev.8` remains the verified Theme and Semantic Color Reconciliation foundation; the historical dev tranche numbers from dev.1–dev.7 remain verified Development provenance against the earlier v1.0 plan, with `1.7.0-dev.7` retained as the last pre-v1.1-reconciliation aggregate. `1.7.0-dev.11` adds a bounded v1.1 Section 26 Glaze Inspector foundation that evolves existing conformance and diagnostics into explainable component-state, token-provenance, semantic-color/theme-resolution, material/accessibility/focus/input/adaptive-layout/form-factor/target-size/authority/migration inspection. It remains advisory and privacy-minimized, does not mutate source or create provider truth, and does not establish Section 26 completion, rendered/native/assistive-technology/performance acceptance, lifecycle promotion, consumer eligibility, deployment, or production acceptance. |

## V1.7 Planning Boundary

GLAZE UI V1.6 / `1.6.0` remains the current Official Stable shared target. V1.7 planning must not change `VERSION`, `registry/lifecycle.json`, current Stable runtime entrypoints, published V1.6 release evidence, or downstream consumer eligibility.

Any V1.7 implementation must remain presentation-focused, preserve provider authority, and fail closed rather than inventing authentication, authorization, privacy, security, consent, permission, capability, connectivity, data-integrity, recovery, identity, backup, availability, trust, or acceptance truth.

## Qualification Boundary

Automated validation alone must not establish V1.7 acceptance. Claimed V1.7 support requires applicable exact-revision evidence for source behavior, semantic correctness, theme safety, custom-theme accessibility, protected semantic color enforcement, palette generation, contrast, grayscale and color-vision differentiation, Forced Colors, Increased Contrast, Reduced Transparency, appearance modes, inputs, task continuity, adaptive composition, Mobile/Tablet/Desktop/Foldable/TV/Wearable support where claimed, representative rendering, performance and energy behavior, native-platform behavior, regression, human review, assistive technology, security/privacy/authority boundaries, and artifact provenance.

## Maintenance

Keep this file synchronized with verified repository implementation state, `registry/lifecycle.json`, the canonical Drive navigation index `GoreeCloud/Sources/Glaze-UI-Index`, and applicable GoreeCloud task records. Planned work must remain planned until authoritative implementation and acceptance evidence establishes another state.
