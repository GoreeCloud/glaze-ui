# Glaze UI 1.6 Candidate — Evidence Presentation and Authority Surfaces

**Lifecycle:** Candidate. This contract is not part of the current Glaze UI 1.5.0 Stable baseline and must not be used to satisfy current Stable conformance until separately validated and promoted.

Glaze UI 1.6 Candidate introduces a shared presentation contract for evidence-backed platform state from Wardveil Security, Privacy Shield, Everkeep, and GoreeCloud Mesh.

The goal is to make system truth understandable without allowing presentation to invent, strengthen, merge, or obscure authority.

## Core invariant

Glaze UI presents evidence; it does not create evidence.

A polished card, shield icon, color, animation, badge, or status label must never imply that a security, privacy, recovery, continuity, or coordination claim is true unless the applicable producer supplied current evidence under its own contract.

## Evidence inputs

An evidence surface may consume:

1. a producer-specific contract and domain status;
2. optional GoreeCloud Mesh Evidence Envelope metadata for provenance, freshness, and transport state;
3. Glaze UI semantic presentation rules.

A valid Mesh envelope is not a substitute for producer acceptance. If the producer-specific evidence is missing, invalid, stale, unsupported, or unavailable, Glaze UI must show an appropriately unavailable/unknown presentation rather than infer success.

## Authority identity

Evidence surfaces must identify the system responsible for the represented truth when that identity is relevant to user understanding or administrative review:

- Wardveil Security — security/protection authority;
- Privacy Shield — privacy/data-use authority;
- Everkeep — resilience/recovery/preservation/continuity authority;
- GoreeCloud Mesh — coordination/governance transport authority;
- Glaze UI — presentation/design-conformance authority only.

Glaze UI must not combine these into a generic "safe" or "protected" state when the underlying evidence domains differ.

## Presentation anatomy

A complete evidence surface can contain:

- **Primary state** — supplied by the producer contract.
- **Authority identity** — the producer responsible for the state.
- **Scope** — the resource, application, device, service, or operation represented.
- **Freshness** — current, stale, expired, or unknown transport/evidence freshness when available.
- **Reason** — a bounded human-readable explanation or reason-code interpretation.
- **Source detail** — optional drill-down for contract, revision, observation time, validity window, and evidence reference.
- **Action** — producer-authorized remediation, review, refresh, recovery, or privacy-control action when available.

The compact surface may omit source detail visually, but it must remain available through an accessible details path when provenance is needed for the product context.

## Freshness semantics

Freshness describes evidence timing, not domain success.

- `current` — evidence is within the producer-declared validity window.
- `stale` — evidence was once usable but requires refresh under the producer contract.
- `expired` — the producer-declared validity window has ended.
- `unknown` — freshness cannot be established.

A `current` envelope can still contain a negative, blocked, attention, denied, degraded, or failed producer outcome. A current timestamp must never be styled as a positive domain result by itself.

## Transport semantics

Mesh transport availability is distinct from producer state:

- `available` — the envelope/transport metadata is available and structurally usable.
- `unavailable` — the transport or source cannot currently be reached.
- `invalid` — provenance, authority-domain, minimization, or envelope validation failed.

Transport availability must not be rendered as protection, privacy compliance, recoverability, or design conformance.

## Visual hierarchy

Evidence surfaces should use the existing Glaze material hierarchy:

Canvas → Solid → Raised → Functional Glass → Overlay.

Ordinary evidence cards default to Solid or Raised. Functional Glass may be used for transient overlays, compact system panels, or contextual surfaces when contrast and reduced-transparency fallbacks are preserved. Clear Glass must not be used for dense evidence text or critical status summaries.

## Color and iconography

Color is supplemental, never the sole carrier of state.

The producer's protected semantic truth family must remain intact. Wardveil security state must not silently reuse Privacy Shield privacy meaning; Everkeep recovery state must not reuse generic success semantics if its producer contract requires a distinct recoverability state.

System icons identify authority or source. They do not independently prove that the represented capability is active.

## Motion

Motion may communicate refresh, transition, expansion, or changed state, but it must never imply successful verification before evidence arrives.

Loading/refresh motion must resolve to the producer-supplied state or to unknown/unavailable. Reduced-motion preferences must receive the existing Glaze substitution behavior.

## Accessibility

Evidence surfaces must:

- expose state, authority, freshness, and required actions to assistive technology;
- never rely on color, translucency, motion, or icon shape alone;
- preserve readable contrast under light/dark appearances and reduced transparency;
- provide keyboard, pointer, touch, TV directional-focus, and other current Stable input behavior appropriate to the form factor;
- avoid forcing raw opaque identifiers into the primary reading order when a human-readable explanation exists.

## Privacy and minimization

Presentation must not request raw private content merely to display evidence status. Mesh envelopes and producer summaries should remain minimized. Sensitive detail must stay behind explicit authorized disclosure paths governed by the producer and Privacy Shield where applicable.

## Candidate acceptance requirements

Promotion requires:

1. machine-readable evidence-presentation tokens;
2. reference implementations for compact status, detailed status, stale/expired, unavailable, and conflicting-domain examples;
3. rendered acceptance across Mobile, Tablet, Desktop, Wide Desktop, and TV;
4. light/dark, reduced-motion, reduced-transparency, forced-colors, and zoom/text-scaling validation;
5. consumer mapping examples for Wardveil Security Center, Privacy Shield settings/status, Everkeep Recovery Center, and Mesh Console;
6. validation that transport freshness cannot be mistaken for positive domain truth;
7. validation that Glaze UI does not create security, privacy, or recovery claims.

Until those gates pass, this remains Candidate and the current Stable consumer target stays Glaze UI 1.5.0.
