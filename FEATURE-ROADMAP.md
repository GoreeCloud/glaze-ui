# Glaze UI — Feature Roadmap

**Status:** Active roadmap control  
**As of:** 2026-09-18  
**Authoritative project record:** Project Specification — Glaze UI  
**Canonical lifecycle authority:** `registry/lifecycle.json`  
**Canonical repository:** `GoreeCloud/goreecloud-glaze-ui`  
**Drive control:** `GoreeCloud/Feature Roadmap/Glaze UI/FEATURE-ROADMAP.md`

## Purpose

This file is the repository-side feature roadmap control for Glaze UI. It records current planned and recommended feature work without replacing exact-revision implementation evidence, lifecycle authority, release gates, GoreeCloud Tasks Management, or the Drive-side roadmap control.

## Current verified lifecycle

GLAZE UI V1.5.1 is the qualification-hardening successor to the V1.5.0 Stable baseline. The two V1.5.1 external qualification obligations were independently reviewed and accepted on frozen exact Development revision `5b59d0e36950d737dba35b58ae58058684e0831b`; the qualification changes were integrated at `f7ef915f0aabea6cf92748018f2220a99e3a9c92`, and Release Candidate `1.5.1-rc.1` was integrated and post-merge verified at `a9c93506dd062d29c6c894940b71d060e8c39110`.

**GLAZE UI V1.5 / `1.5.1` is the current Official Stable shared target.** Stable promotion is authoritative on `main`; the immediate known-good rollback baseline remains `1.5.0`. Release publication, downstream consumer acceptance, deployment, and production acceptance remain separate governed transitions.

The V1.5.1 qualification closure contains two independently accepted additions:

1. `performance-representative-budget` — accepted for the reviewed representative Zorin OS 17.3 / Firefox 156.0 / Lenovo IdeaPad 3 15IIL05 environment; durable review authority PR #230 comment `5697516074`.
2. `platform-posture-continuity` — accepted for the approved Pixel Fold Android Emulator target runtime under `GCU-ADR-GLAZE-V151-POSTURE-TR-001`; durable review authority PR #230 comment `5705230782`.

Together with the sixteen retained V1.5.0 obligations, V1.5.1 contains **18 accepted shared qualification obligations**. The external observations remain bound to their real exact revisions and are carried into Stable only through fail-closed source-impact continuity.

## Current verified direction

V1.5.1 preserves the accepted Context + Capability Resolution architecture, including fail-closed authority/provenance handling, capability-aware presentation, accessibility-priority composition, continuity, graceful degradation, explainable diagnostics, and presentation-only enforcement boundaries. Glaze UI presents authoritative state but does not create consent, permissions, privacy authorization, security claims, recovery claims, or consequential execution authority.

The V1.5.1 Stable patch adds qualification closure and Stable patch identity without changing the reviewed V1.5 presentation or authority implementation. Publication, deployment, production acceptance, and downstream application acceptance remain separate governed transitions.

All GoreeCloud-controlled graphical consumers remain independently responsible for application-specific adoption of the current Stable Glaze UI release and for their own rendered/native/accessibility/platform acceptance. A Stable Glaze platform release does not make downstream applications Stable by inheritance.

## Roadmap

| ID | Feature / obligation | Priority | Current state |
| --- | --- | --- | --- |
| FR-001 | Reconcile and maintain every current planned or recommended Glaze UI feature from authoritative project records and verified repository evidence in this roadmap. | High | Ongoing control. |
| FR-002 | Move actionable feature obligations into GoreeCloud Tasks Management when required, preserving priority, dependency, blocker, and lifecycle disposition. | High | Ongoing control. |
| FR-003 | Do not mark features implemented, complete, cancelled, superseded, RC, Stable, deployed, or production-accepted without authoritative evidence and synchronized repository/Drive/task records. | High | Ongoing control. |
| FR-004 | Preserve GLAZE UI V1.5 / `1.5.1` as the current Official Stable authority and `1.5.0` as the immediate rollback baseline. | P0 | Verified Stable invariant; current lifecycle authority remains `1.5.1`. |
| FR-005 | Preserve the V1.5 Context + Capability Resolution architecture and its fail-closed authority, accessibility, continuity, diagnostics, degradation, and truth-preservation invariants. | P0 | Stable invariant; regression protection remains mandatory. |
| FR-006 | Maintain presentation-only authority boundaries so Glaze never creates consent, grants permissions, invents provider precedence, executes consequential operations, or upgrades Privacy Shield, Wardveil Security, Everkeep, Mesh, or application truth. | P0 | Stable invariant; V1.5.1 promotion preserves it. |
| FR-007 | Complete V1.5.1 representative performance qualification against the approved budget using exact-revision, privacy-minimized evidence from a representative reviewed environment. | P0 | Accepted — exact revision `5b59d0e36950d737dba35b58ae58058684e0831b`; PR #230 comment `5697516074`. |
| FR-008 | Complete V1.5.1 platform/posture continuity qualification using a representative physical device or approved target runtime for every claimed applicable transition family. | P0 | Accepted — approved Pixel Fold target runtime under `GCU-ADR-GLAZE-V151-POSTURE-TR-001`; PR #230 comment `5705230782`. |
| FR-009 | Complete the governed V1.5.1 lifecycle transition through Release Candidate and separate Stable promotion with exact-head and post-merge verification. | P0 | Completed for shared source/lifecycle authority; V1.5.1 is current Stable. Publication, downstream adoption, deployment, and production remain separate. |
| FR-010 | Drive current-Stable adoption across GoreeCloud-controlled user-facing consumers without allowing platform-level Stable status to imply application-level acceptance. | P0 | Ongoing consumer migration/acceptance work; required target advances to `1.5.1` after authoritative Stable promotion. |
| FR-011 | Reconcile stale historical documentation and roadmap records that still identify older Glaze releases as current, without rewriting immutable historical evidence. | High | Active documentation-control work; repository promotion surfaces reconciled for V1.5.1. |
| FR-012 | Preserve V1.5.0 and earlier release evidence as historical rollback/audit provenance without conflating it with current V1.5.1 Stable authority. | High | Historical/rollback control. |
| FR-013 | Implement the planned V1.6 Glaze Skeleton Motion System and intelligent loading decision/escalation foundation without altering V1.5.1 Stable authority. | P0 | Development source foundation implemented for sections 1–4; lifecycle remains non-consumer-eligible Development and requires exact-revision CI/acceptance evidence. |
| FR-014 | Expand V1.6 semantic loading/skeleton tokens, accessibility fallbacks, motion-fatigue controls, and configurable thresholds through governed machine contracts. | P0 | Initial semantic map and machine contract implemented; broader V1.6 token/state expansion remains open. |
| FR-015 | Expand V1.6 beyond loading into the full semantic state grammar, accessibility profiles, focus, motion families, materials, typography, density, responsive behavior, recovery, diagnostics, and conformance metadata. | P0 | Development source representation covers planned sections 1–100 continuously through aggregate `1.6.0-dev.12`. The current hardening preserves source completeness while strengthening section 98 grouped-evidence requirements; it does not establish qualification closure, Candidate, Stable, consumer, deployment, or production acceptance. |
| FR-016 | Build the V1.6 section 98 acceptance matrix, including accessibility, representative rendering, layout stability, performance, offline/degraded behavior, privacy/authority boundaries, and regression coverage. | P0 | Grouped 24-lane matrix is implemented against frozen revision `c7509c79256b04b0aa67cb9dd0737d7588e0ae4a`. Machine run `35345027816`, rendered-browser run `35348330585`, and rendered-regression run `35352215130` establish the no-external baseline at 17 verified / 7 unverified. Accepted Human evidence verifies Accessibility, Keyboard navigation, Privacy boundaries, Authority boundaries, and Representative rendering. Accepted Orca 42.0 Assistive Technology evidence verifies the dedicated Assistive Technology lane. Representative Performance candidate evidence is durably preserved at `acceptance/v1.6-performance-candidate-evidence.json` with SHA-256 `6ba3ea31b0bdde85de842c5fcac5c6756f92794efb55ba4e1d4a4d5b331823ad`; the accepted Performance review passes every approved Glaze UI Performance Budget v1.0 threshold. Governed reconciliation with all three accepted external records produces **24 verified / 0 unverified / 0 not applicable**. Qualification evidence is complete and ready for governed qualification review, but no Candidate, Release Candidate, Stable, consumer, deployment, production, tag, or release-publication status is granted automatically. |
| FR-017 | Establish downstream V1.6 application adoption profiles only after shared V1.6 lifecycle and acceptance state make consumer migration valid. | High | Deferred until shared V1.6 implementation and lifecycle prerequisites are satisfied. |

## Qualification evidence boundary

Machine checks may prove source behavior, contract integrity, exact-revision preservation, or qualification-tool integrity only to the extent those checks exercise them. They do not substitute for representative human/device/runtime evidence, assistive-technology sessions where required, privacy/policy review, performance measurements, application-specific consumer acceptance, lifecycle approval, deployment, or production acceptance.

The V1.5.1 performance and posture qualification is accepted only for the exact reviewed environments and revision recorded above. Missing evidence, unsupported transition families, unknown authority, stale evidence, source-revision mismatch, or environment mismatch must fail closed rather than being inferred as acceptable.

## Maintenance and synchronization

This repository roadmap is the current Glaze UI feature-roadmap source of truth. The live Drive path `GoreeCloud/Feature Roadmap/Glaze UI` is a navigation index only and must point back to the canonical repository rather than carry a competing `FEATURE-ROADMAP.md`. Reconcile this roadmap with the authoritative project record, current repository state, `registry/lifecycle.json`, the Drive navigation index, and GoreeCloud Tasks Management whenever feature scope, priority, dependency, implementation status, blocker, cancellation, supersession, recommendation, or verification state materially changes.

No feature may be represented as complete or Stable solely because it appears in this roadmap. Completion and lifecycle claims require applicable authoritative implementation, validation, review, release, and production evidence.

## Reconciliation rule

At each material feature change, reconcile this roadmap against the current authoritative project record, lifecycle registry, repository implementation state, applicable Platform System requirements, consumer evidence, and GoreeCloud Tasks Management. Missing obligations, stale status, duplicated work, roadmap drift, or undocumented disposition changes are defects to correct.