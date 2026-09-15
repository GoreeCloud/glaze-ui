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
- mandatory provenance for every non-unknown capability state;
- fail-closed handling for missing or invalid capability authority;
- capability-aware action resolution without automatic permission requests or consequential execution;
- accessibility-first optical presentation decisions;
- privacy-bounded context normalization and privacy-safe explanation output;
- an explicit bridge from the V1.4.1 optical capability surface into the broader rendering-capability model;
- an in-memory anti-jitter stabilizer with minimum-sample and dwell controls;
- a provider aggregation boundary that rejects provenance impersonation and fails closed on duplicate context/capability ownership instead of inventing precedence;
- explicit provider-authority ownership rules so a provider may contribute only context/capability domains its authority class is permitted to own;
- semantic composition decisions for compact touch, desktop pointer/keyboard, remote/focus, unfolded multi-pane, reading, media, and critical-configuration contexts;
- accessibility-priority composition for Large Text, Touch Assistance, Reduced Motion, Reduced Transparency, Increased Contrast, and Forced Colors;
- runtime-pressure cost reduction that selects durable presentation without modifying capability truth;
- connectivity and constrained-window continuity behavior that avoids task-state resets and page reloads during offline/reconnecting or picture-in-picture/background-like transitions;
- capability-aware navigation that can omit truly unsupported destinations while preserving restricted/offline destinations and broader task continuity;
- capability-aware control presentation with explicit unavailable/degraded states and user-initiated recovery semantics;
- predictable adaptive action prioritization that preserves primary-action order while allowing bounded context relevance to reorder only non-primary actions;
- privacy-safe unavailable/degraded explanations plus user-initiated recovery metadata;
- explicit application-authored fallback suggestions that preserve supported local/core workflows without automatic fallback execution; and
- 39 core Development conformance scenarios plus 8 action/degradation scenarios, for 47 machine-covered Development scenarios total.

## Provider authority boundary

Provider aggregation is deterministic and fail-closed. A provider cannot declare provenance as another provider or authority. If two providers claim the same context domain or capability identifier, Glaze does not guess which one wins; the conflicting input is omitted from the accepted snapshot and recorded as a semantic conflict for diagnostics. No provider priority is inferred.

Self-consistent provenance is not sufficient. Each provider authority is constrained to the semantic domains it may own. For example, service authority cannot declare input-device context or authorization truth, application authority cannot manufacture device/platform capability, and an `unknown` authority cannot contribute accepted semantic truth. Authorization-domain capability remains restricted to appropriate policy, identity, platform permission, application permission, or security authorities. This keeps Glaze from converting technically valid records into unauthorized semantic facts.

Provider diagnostics expose counts and semantic domains/states rather than raw provider identifiers or context values.

## Composition and continuity boundary

Composition consumes semantic context rather than inferring sensitive meaning from raw dimensions or activity. The Development resolver may select single- versus multi-pane presentation, control density, command-surface style, focus navigation, material preference, motion preference, and label explicitness.

Accessibility has final presentation precedence over richer device/input choices: Large Text or Touch Assistance prevents dense control presentation, Reduced Motion suppresses motion preference, and clarity-oriented accessibility states force high-clarity material and explicit labeling. Runtime pressure may lower presentation cost to a durable mode but cannot change the truth of a capability. Connectivity loss or reconnection does not itself collapse an otherwise valid composition, and constrained window modes may reduce to single-pane without resetting the user’s task.

Primary navigation identity and task continuity remain stable. When a selected destination becomes truly unsupported and is governed to be omitted, the resolver may select an explicit or deterministic visible fallback while preserving task state and reporting the continuity transition. Restricted, offline, degraded, permission-gated, and temporarily unavailable destinations remain semantically representable instead of being silently treated as nonexistent.

## Adaptive actions and graceful degradation boundary

Adaptive action prioritization is bounded and predictable. Primary actions remain in author-defined order even when capability state changes. Context relevance may reorder only non-primary actions, and ties preserve author order. Glaze does not automatically execute a newly prominent action merely because it became more relevant.

Unavailable, restricted, offline, permission-required, unsupported, unknown, and degraded states receive semantic presentation state and an explanation without exposing provider identities or raw context. Applications may supply bounded state-specific user-facing explanation text and recovery metadata. Recovery is always user initiated; Glaze does not automatically request permission or perform consequential actions.

Fallbacks are explicit application intent rather than inferred behavior. If an unavailable action names a fallback action and that fallback is currently visible and invocable, Glaze may suggest it while preserving the original action state. The fallback is never executed automatically. This allows supported local/core workflows to remain available when cloud, network, device, or service capabilities degrade without pretending the unavailable capability succeeded.

## Compatibility boundary

`1.5.0-dev.1` inherits the `1.4.1` Stable runtime and adds the new development-only context/capability layer. The Stable `1.4.1` implementation, lifecycle, acceptance, and release identity are not modified by this development line.

Consumers must not switch their current Stable conformance target from `1.4.1` to this development entrypoint. Adoption begins only after a separately governed Release Candidate and Stable process establishes a new approved release.

## Privacy boundary

Ordinary adaptation is local-first, bounded, ephemeral by default, and does not require telemetry or remote analysis. The context normalizer rejects obviously sensitive/raw context field families such as credentials, tokens, clipboard data, raw content/activity, precise location, and biometric values. Action summaries expose semantic states and reason codes rather than raw provider identities or context values. This is a source-level guardrail, not a substitute for Privacy Shield authorization at consumer/provider boundaries.

## Current acceptance state

This development revision is eligible only for machine development validation. The conformance matrices are Development gates and explicitly do **not** establish human acceptance, target-device/runtime acceptance, consumer conformance, Release Candidate status, Stable status, deployment, or production acceptance.

Before Release Candidate/Stable qualification, the same matrix items marked for external acceptance still require exact-revision human usability, accessibility/assistive-technology, representative target-device/runtime, privacy, anti-jitter/performance, and platform/posture/input/window validation. Consumer-specific composition/navigation/action integration also remains separate from the shared design-system machine gate.
