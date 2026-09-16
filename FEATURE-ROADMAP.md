# Glaze UI — Feature Roadmap

**Status:** Active roadmap control  
**As of:** 2026-09-15  
**Authoritative project record:** Project Specification — Glaze UI  
**Canonical lifecycle authority:** `registry/lifecycle.json`  
**Canonical repository:** `GoreeCloud/goreecloud-glaze-ui`  
**Drive control:** `GoreeCloud/Feature Roadmap/Glaze UI/FEATURE-ROADMAP.docx`

## Purpose

This file is the repository-side feature roadmap control for Glaze UI. It records current planned and recommended feature work without replacing exact-revision implementation evidence, lifecycle authority, release gates, GoreeCloud Tasks Management, or the Drive-side roadmap control.

## Current verified lifecycle

The current Official Stable release is **GLAZE UI V1.5 / `1.5.0`**. The accepted Stable integration commit is `b7fa8164bfdeaa1dc0acb21b770e7601120da04e`, and `1.4.1` remains the documented rollback baseline.

The active successor stabilization stream is **GLAZE UI V1.5.1 / `1.5.1-dev.1`**, which remains **Development**, **Draft**, **non-RC**, **non-Stable**, and **non-consumer-authorizing**. Draft PR #230 (`feature/glaze-v1.5.1-hardening`) adds bounded qualification tooling while preserving the exact `1.5.0` Stable baseline.

V1.5.1 has exactly two remaining external qualification obligations:

1. `performance-representative-budget` — requires representative measurements against the approved GoreeCloud Glaze UI Performance Budget and exact reviewed revision;
2. `platform-posture-continuity` — requires representative physical-device or approved target-runtime evidence for applicable posture/rotation/form-factor transitions.

Neither obligation may be satisfied by machine simulation, generated review artifacts, repository-local harness success, or implication. Missing or mismatched evidence must remain pending.

## Current verified direction

V1.5.0 Stable provides the accepted Context + Capability Resolution baseline, including fail-closed authority/provenance handling, capability-aware presentation, accessibility-priority composition, continuity, graceful degradation, explainable diagnostics, and presentation-only enforcement boundaries. Glaze UI presents authoritative state but does not create consent, permissions, privacy authorization, security claims, recovery claims, or consequential execution authority.

V1.5.1 hardening now provides repository-local qualification harnesses for representative performance measurement and posture-continuity evidence capture. Those harnesses are evidence-collection and boundary-verification tools only; they cannot promote lifecycle state, accept downstream consumers, or manufacture representative evidence.

All GoreeCloud-controlled graphical consumers remain independently responsible for application-specific adoption of the current Stable Glaze UI release and for their own rendered/native/accessibility/platform acceptance. A Stable Glaze platform release does not make downstream applications Stable by inheritance.

## Roadmap

| ID | Feature / obligation | Priority | Current state |
| --- | --- | --- | --- |
| FR-001 | Reconcile and maintain every current planned or recommended Glaze UI feature from authoritative project records and verified repository evidence in this roadmap. | High | Ongoing control. |
| FR-002 | Move actionable feature obligations into GoreeCloud Tasks Management when required, preserving priority, dependency, blocker, and lifecycle disposition. | High | Ongoing control. |
| FR-003 | Do not mark features implemented, complete, cancelled, superseded, RC, Stable, deployed, or production-accepted without authoritative evidence and synchronized repository/Drive/task records. | High | Ongoing control. |
| FR-004 | Preserve GLAZE UI V1.5 / `1.5.0` as the current Official Stable authority and `1.4.1` as the rollback baseline while successor work remains isolated. | P0 | Active control — Stable authority verified in `registry/lifecycle.json`. |
| FR-005 | Preserve the V1.5 Context + Capability Resolution architecture and its fail-closed authority, accessibility, continuity, diagnostics, degradation, and truth-preservation invariants. | P0 | Stable baseline; regression protection remains mandatory. |
| FR-006 | Maintain presentation-only authority boundaries so Glaze never creates consent, grants permissions, invents provider precedence, executes consequential operations, or upgrades Privacy Shield, Wardveil Security, Everkeep, Mesh, or application truth. | P0 | Stable invariant; V1.5.1 qualification tooling explicitly preserves it. |
| FR-007 | Complete V1.5.1 representative performance qualification against the approved budget using exact-revision, privacy-minimized evidence from a representative reviewed environment. | P0 | Pending external evidence. Harness implemented in Draft PR #230; no acceptance inferred. |
| FR-008 | Complete V1.5.1 platform/posture continuity qualification using a representative physical device or approved target runtime for every claimed applicable transition family. | P0 | Pending external evidence. Harness implemented in Draft PR #230; machine simulation alone is insufficient. |
| FR-009 | Keep V1.5.1 Development until FR-007 and FR-008 are independently reviewed and durably recorded; only then evaluate any later RC or Stable transition under lifecycle governance. | P0 | Blocked on FR-007 and FR-008. No RC/Stable claim. |
| FR-010 | Drive current-Stable adoption across GoreeCloud-controlled user-facing consumers without allowing platform-level Stable status to imply application-level acceptance. | P0 | Ongoing consumer migration/acceptance work. |
| FR-011 | Reconcile stale historical documentation and roadmap records that still identify older Glaze releases as current, without rewriting immutable historical evidence. | High | Active documentation-control work. |
| FR-012 | Preserve the separately governed V1.4.1 publication/rollback evidence as historical release provenance without conflating it with current V1.5.0 Stable authority or V1.5.1 qualification. | High | Historical/rollback control. |

## Qualification evidence boundary

Machine checks may prove source behavior, contract integrity, exact-revision preservation, or qualification-tool integrity only to the extent those checks exercise them. They do not substitute for representative human/device/runtime evidence, assistive-technology sessions where required, privacy/policy review, performance measurements, application-specific consumer acceptance, lifecycle approval, deployment, or production acceptance.

A V1.5.1 qualification artifact must remain pending until real evidence is produced and reviewed against the exact source revision and applicable environment. Missing evidence, unsupported transition families, unknown authority, stale evidence, source-revision mismatch, or environment mismatch must fail closed rather than being inferred as acceptable.

## Maintenance and synchronization

This roadmap and the corresponding Drive `FEATURE-ROADMAP.docx` must remain materially synchronized with one another and with the authoritative project record, current repository state, `registry/lifecycle.json`, and GoreeCloud Tasks Management. Update both copies whenever feature scope, priority, dependency, implementation status, blocker, cancellation, supersession, recommendation, or verification state materially changes.

No feature may be represented as complete or Stable solely because it appears in this roadmap. Completion and lifecycle claims require applicable authoritative implementation, validation, review, release, and production evidence.

## Reconciliation rule

At each material feature change, reconcile this roadmap against the current authoritative project record, lifecycle registry, repository implementation state, applicable Platform System requirements, consumer evidence, and GoreeCloud Tasks Management. Missing obligations, stale status, duplicated work, roadmap drift, or undocumented disposition changes are defects to correct.
