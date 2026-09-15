# GLAZE UI V1.5 — Contextual + Capability Awareness

**Machine version:** `1.5.0-dev.1`  
**Release lifecycle:** Development  
**Stable baseline:** GLAZE UI V1.4.1 / `1.4.1`  
**Consumer eligible:** No  
**Stable:** No

## Purpose

This development line implements the architecture proposed by **Glaze UI V1.4.1 Extended Upgrade — Contextual Awareness and Capability Awareness** without redefining the already-published `1.4.1` Stable identity.

GLAZE UI V1.5 makes context and capability awareness first-class presentation inputs while preserving the core authority boundary:

> Context describes the situation. Capabilities describe what is possible. Authoritative providers describe what is permitted and true. Glaze determines how that verified reality is presented.

Glaze UI does not grant permissions, invent service health, manufacture security/privacy state, or treat a displayed affordance as authorization.

## Development surface

The current `1.5.0-dev.1` source introduces:

- the eleven governed context domains from the Extended proposal;
- the eight governed capability domains;
- the ten-state capability grammar, including explicit `unknown`, `permission-required`, `restricted`, `offline`, and degraded states;
- mandatory provenance for every non-unknown capability state and fail-closed handling for missing or invalid authority;
- provider aggregation that rejects provenance impersonation, duplicate ownership, inappropriate authority/domain ownership, and invented precedence;
- semantic composition for compact touch, desktop pointer/keyboard, remote/focus, unfolded multi-pane, reading, media, critical configuration, accessibility, runtime pressure, connectivity, and constrained-window states;
- capability-aware navigation and controls with explicit unavailable/degraded semantics and task continuity;
- predictable adaptive action prioritization that preserves primary-action order and limits contextual reordering to non-primary actions;
- privacy-safe unavailable/degraded explanations, user-initiated recovery metadata, and explicit application-authored fallback suggestions without automatic fallback execution;
- privacy-safe explainable adaptation diagnostics spanning composition, navigation, action, optical, capability-provenance, and continuity decisions without exposing raw context or provider identity;
- an explicit bridge from V1.4.1 optical capabilities into the broader capability model plus anti-jitter stabilization; and
- a unified developer-facing Context + Capability Resolution Layer that combines authoritative provider state with application intent and resolves accepted composition, navigation, actions, controls, optics, continuity, and diagnostics through one bounded pipeline.

Machine coverage currently consists of 39 core scenarios, 8 action/degradation scenarios, 7 diagnostics scenarios, and 10 unified-resolution scenarios, for **64 machine-covered Development scenarios total**.

## Provider authority boundary

Provider aggregation is deterministic and fail-closed. A provider cannot declare provenance as another provider or authority. If two providers claim the same context domain or capability identifier, Glaze does not guess which one wins; the conflicting input is omitted from the accepted snapshot and recorded as a semantic conflict. No provider priority is inferred.

Self-consistent provenance is not sufficient. Each provider authority is constrained to the semantic domains it may own. Service authority cannot manufacture authorization truth; application authority cannot manufacture device/platform capability; unknown authority cannot contribute accepted semantic truth. Glaze renders authoritative conclusions but does not independently create them.

## Unified resolution boundary

`resolveGlazeInterface(...)` is the Development-level unified resolution entrypoint. It accepts authoritative semantic providers together with application-defined intent, actions, navigation destinations, and current navigation identity. The resolver constructs a fail-closed provider snapshot and then derives the accepted interface presentation through the existing composition, navigation, action, control, optical, and diagnostics layers.

The unified resolver does not grant new authority. It cannot infer authorization, invent provider precedence, automatically navigate, request permission automatically, execute consequential actions automatically, or execute fallback actions automatically. Provider conflicts remain explicit and fail closed; a conflicted capability becomes unavailable/unknown to dependent presentation logic rather than being optimistically selected.

The accepted presentation is a presentation decision only. It records pane mode, density, command surface, navigation mode, material/motion preference, current accepted destination, ordered action identifiers, and optical mode while preserving task state and avoiding page reloads.

## Composition and continuity boundary

Composition consumes semantic context rather than inferring sensitive meaning from raw dimensions or activity. Accessibility has final presentation precedence over richer device/input choices. Runtime pressure may lower presentation cost but cannot change capability truth. Connectivity loss or reconnection does not itself collapse a valid composition, and constrained window modes may reduce to single-pane without resetting the user's task.

Navigation preserves broader task continuity when a destination becomes unavailable. Truly unsupported destinations may be omitted under an explicit policy; restricted, offline, degraded, permission-gated, and temporarily unavailable destinations remain semantically representable where useful.

## Adaptive actions and graceful degradation boundary

Primary actions remain in author-defined order even when capability state changes. Context relevance may reorder only non-primary actions, with ties preserving author order. Unavailable, restricted, offline, permission-required, unsupported, unknown, and degraded states receive semantic presentation and explanation without exposing raw provider identity or context.

Fallbacks are explicit application intent, not inferred behavior. When an unavailable action names a currently invocable fallback, Glaze may suggest it while preserving the original action state. Recovery and fallback execution remain user initiated.

## Explainable diagnostics boundary

The Development diagnostics layer explains accepted presentation decisions through semantic state rather than raw underlying data. It can expose composition reason codes, navigation continuity changes, omitted/blocked destinations, action states and fallback availability, optical downgrade reasons, and the authority class behind capability provenance.

Diagnostics deliberately omit raw context values, application-provided explanation text, provider identifiers, provenance scope, exact observation timestamps, credentials, and private content. Diagnostics remain presentation-only and require neither telemetry nor remote analysis for ordinary operation.

## Compatibility boundary

`1.5.0-dev.1` inherits the `1.4.1` Stable runtime and adds the new Development-only context/capability layer. The Stable `1.4.1` implementation, lifecycle, acceptance, and release identity are not modified by this Development line.

Consumers must not switch their current Stable conformance target from `1.4.1` to this Development entrypoint. Adoption begins only after a separately governed Release Candidate and Stable process establishes a new approved release.

## Privacy boundary

Ordinary adaptation is local-first, bounded, ephemeral by default, and does not require telemetry or remote analysis. The context normalizer rejects obviously sensitive/raw context field families such as credentials, tokens, clipboard data, raw content/activity, precise location, and biometric values. Action summaries, diagnostics, and unified resolution summaries expose semantic states, reason codes, authority classes, and accepted presentation outcomes rather than raw provider identities or context values.

These controls are source-level privacy guardrails and do not replace Privacy Shield authorization at consumer/provider boundaries.

## Current acceptance state

This Development revision is eligible only for machine development validation. The four conformance matrices cover 64 machine scenarios and explicitly do **not** establish human acceptance, target-device/runtime acceptance, consumer conformance, Release Candidate status, Stable status, deployment, or production acceptance.

Before Release Candidate/Stable qualification, externally marked matrix items still require exact-revision human usability, accessibility/assistive-technology, representative target-device/runtime, privacy, anti-jitter/performance, and platform/posture/input/window validation. Representative consumer integration of the unified resolution layer also remains a separate acceptance requirement.
