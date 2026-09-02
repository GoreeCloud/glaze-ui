# Glaze UI 2.2 — Evidence Presentation and Authority Surfaces

**Lifecycle:** Stable. Introduced in Glaze UI 1.6.0 and retained/extended in the current Glaze UI **2.2.0** Stable consumer target.

The evidence-presentation contract gives GoreeCloud products a shared way to present evidence-backed state from Wardveil Security, Privacy Shield, Everkeep, GoreeCloud Mesh, GoreeCloud Identity, and Glaze UI without allowing presentation to invent, strengthen, merge, or obscure authority.

The historical 1.6 rendered acceptance artifacts remain preserved as promotion evidence. Glaze UI 2.0 extended the source and consumer contract to GoreeCloud Identity; Glaze UI 2.1 carried that authority boundary into the color-coded Glaze Material and accessibility-resolution contract; Glaze UI 2.2 carries it forward under the current System Shell, component, material-budget, and accessibility rules. Dedicated rendered Identity Center acceptance remains application-specific evidence and is not implied by source-contract support alone.

## Core invariant

Glaze UI presents evidence; it does not create evidence.

A polished card, shield icon, account icon, color, animation, badge, material treatment, or status label must never imply that security, privacy, recovery, continuity, identity, authentication, authorization, coordination, or conformance is true unless the applicable authoritative producer supplied usable evidence under its own contract.

## Evidence inputs

An evidence surface may consume:

1. a producer-specific contract and domain status;
2. optional GoreeCloud Mesh Evidence Envelope metadata for provenance, freshness, lifecycle, and transport state; and
3. Glaze UI semantic presentation rules.

A valid Mesh envelope is not a substitute for producer acceptance. If producer-specific evidence is missing, invalid, stale, unsupported, or unavailable, Glaze UI must show an appropriately unavailable or unknown presentation rather than infer success.

## Authority identity

Evidence surfaces must preserve the system responsible for the represented truth:

- **Wardveil Security** — security/protection authority;
- **Privacy Shield** — privacy, consent, data-minimization, data-governance, and user-control authority;
- **Everkeep** — resilience, backup, recovery, preservation, portability, succession, and continuity authority;
- **GoreeCloud Mesh** — platform coordination, governance, integration, capabilities, and event-transport authority;
- **GoreeCloud Identity** — identity, authentication, authorization, accounts, devices, credentials, sessions, and delegated-authority authority;
- **Glaze UI** — presentation, interaction, accessibility, responsiveness, and design-conformance authority only.

Glaze UI must not combine these domains into a generic `safe`, `protected`, `trusted`, or equivalent aggregate state.

Producer/domain pairs are fail-closed. For example, GoreeCloud Identity evidence labeled with Wardveil's `security` authority domain is invalid presentation input; Privacy Shield evidence labeled `authentication` is likewise invalid. A producer cannot borrow another producer's authority merely because the evidence traveled through Mesh.

## GoreeCloud Identity boundary

GoreeCloud Identity has two distinct relationships with evidence presentation:

1. it may authenticate the caller that reads evidence from Mesh using a least-privilege `mesh.evidence.read` credential; and
2. it may itself produce minimized Identity evidence for identity/authentication/authorization/account/device/credential/session/delegated-authority state.

These roles must never be conflated. Successful authentication of the evidence reader does not prove that any displayed producer outcome is positive. Likewise, current Identity evidence does not independently authorize a Privacy Shield purpose, establish Wardveil protection, prove Everkeep recoverability, establish Mesh governance success, or establish Glaze UI conformance.

Bearer credentials are request credentials, not presentation data. They must not be returned in normalized presentation models or rendered into evidence surfaces.

## Presentation anatomy

A complete evidence surface can contain:

- **Primary state** — supplied by the producer contract.
- **Authority identity** — the producer responsible for the state.
- **Scope** — the resource, application, device, service, account, session, or operation represented.
- **Freshness** — current, stale, expired, or unknown producer-declared evidence freshness.
- **Transport/lifecycle** — current, stale-only, empty, unavailable, or invalid Mesh transport state where applicable.
- **Reason** — a bounded human-readable explanation or producer reason-code interpretation.
- **Source detail** — optional drill-down for contract, revision, observation time, validity window, and evidence reference.
- **Action** — producer-authorized remediation, review, refresh, recovery, privacy-control, identity-review, or details path where the producer contract authorizes it.

Compact surfaces may omit source detail visually, but provenance must remain available through an accessible details path when required by the product context.

## Freshness semantics

Freshness describes evidence timing, not domain success.

- `current` — evidence is inside the producer-declared validity window.
- `stale` — evidence was once usable but requires refresh under the producer contract.
- `expired` — the producer-declared validity window has ended.
- `unknown` — freshness cannot be established.

A `current` envelope can still contain a negative, blocked, attention, denied, degraded, failed, revoked, expired-credential, or unauthorized producer outcome. A current timestamp must never be styled as a positive domain result by itself.

## Transport semantics

Mesh transport availability is distinct from producer state.

Transport availability must not be rendered as protection, privacy compliance, recoverability, valid identity, successful authentication, authorization, or design conformance.

A successful Mesh read only establishes that a transport response was obtained and structurally accepted. Glaze UI still validates producer identity, the producer/domain pairing, evidence lifecycle, and producer-specific semantics before presentation.

## Glaze Material hierarchy

Current 2.2 evidence surfaces use **Canvas / Surface / Soft Glaze / Glaze / Deep Glaze / Live Glaze**. Content-heavy evidence remains solid; interaction and contextual chrome may use bounded color-coded Glaze Material. Readability and producer-state distinction override optical richness.

Ordinary evidence surfaces should use **Surface** or **Soft Glaze**. Contextual panels may use **Glaze**, **Deep Glaze**, or Overlay where readability and accessibility remain intact. **Live Glaze** must not reduce critical evidence readability and must always have a readable Reduced Transparency / effective Solid fallback. Forced Colors remains authoritative. Evidence surfaces also obey the 2.2 System Glaze budget; adding evidence does not authorize stacking additional dominant translucent system panels.

Historical Canvas/Solid/Raised/Functional Glass/Clear Glass behavior remains compatibility history for the retained 1.6 rendered acceptance artifacts.

## Color, iconography, and motion

Color is supplemental, never the sole carrier of state. Producer truth families remain distinct: Wardveil security meaning cannot silently reuse Privacy Shield privacy meaning; Identity authentication meaning cannot silently become a security verdict; Everkeep recovery meaning cannot be replaced by generic success semantics.

System icons identify authority or source. They do not independently prove that the represented capability is active.

Motion may communicate refresh, transition, expansion, or changed state, but it must never imply successful verification before producer evidence arrives. Reduced Motion receives the current Glaze substitution behavior. Glaze Motion remains separately Experimental and is not required for evidence presentation.

## Accessibility and resilience

Evidence surfaces must:

- expose state, authority, freshness, transport/lifecycle, and required actions to assistive technology;
- never rely on color, material, translucency, motion, or icon shape alone;
- preserve readable contrast in Light, Dark, and Deep Dark appearances and in Reduced Transparency, Increased Contrast, Forced Colors, Large Text, and effects-free modes;
- preserve appropriate keyboard, pointer, touch, TV directional-focus, wearable, and other supported input behavior;
- preserve reflow and critical information at 200% text scaling; and
- avoid forcing raw opaque identifiers or sensitive identity attributes into the primary reading order when a human-readable explanation is available.

## Privacy and minimization

Presentation must not request raw private content merely to display evidence status. Mesh envelopes and producer summaries remain minimized. Identity presentation must not expose passwords, passkeys/private keys, recovery secrets, bearer tokens, session secrets, or raw identity profile attributes. Sensitive detail stays behind explicit authorized disclosure paths governed by the authoritative producer and Privacy Shield where applicable.

## Consumer mapping examples

The shared evidence anatomy maps into the GoreeCloud platform centers without transferring authority to Glaze UI:

- **Security Center** presents Wardveil Security producer state, evidence freshness, scope, and remediation paths while Wardveil remains the security/protection authority.
- **Privacy Center** presents Privacy Shield decisions, permissions, data-use status, minimization context, and authorized controls while Privacy Shield remains the privacy/data-use authority.
- **Continuity Center** presents Everkeep backup, preservation, recovery, restore-verification, portability, succession, and continuity evidence while Everkeep remains the continuity authority.
- **Mesh Center** presents GoreeCloud Mesh coordination, provenance, transport, lifecycle, integration, and governance metadata while Mesh remains coordination/governance authority and does not replace a domain producer's verdict.
- **Identity Center** presents GoreeCloud Identity account, authentication, authorization, device, credential, session, and delegated-authority evidence while GoreeCloud Identity remains the identity authority.
- **Design Center** may present Glaze UI design-conformance evidence while Glaze UI remains presentation/design authority only.

Application-specific surfaces may consume the same grammar when they preserve producer identity, authority boundaries, freshness semantics, minimization rules, and fail-closed behavior.

## Mesh consumer requirements

`reference/mesh-evidence-consumer.mjs` is the retained current source reference consumer. It must:

- require HTTPS except loopback development for Mesh reads;
- use the GoreeCloud Identity read credential only in the `Authorization` header;
- normalize Mesh lifecycle without promoting stale history to current state;
- validate every producer/authority-domain pair;
- preserve producer outcomes verbatim;
- reject cross-authority escalation;
- allow refresh intent only for explicit producer-owned domains;
- never create an overall safety, trust, privacy, protection, recovery, or identity score/verdict; and
- return transport-only unavailable/invalid models without domain claims when the trust boundary cannot be established.

## Historical 1.6 rendered acceptance

`reference/candidate-1.6-evidence-acceptance.html` and `scripts/validate_candidate_1_6_evidence_rendered.py` remain the retained browser-rendered 1.6 acceptance matrix.

That historical matrix covers light and dark Mobile `390×844`, Tablet `820×1180`, Desktop `1280×900`, Wide Desktop `1600×1000`, and TV `1920×1080`, plus reduced motion, reduced transparency, TV forced colors, and Mobile 200% text scaling/reflow.

Those artifacts remain evidence that the original platform-neutral security/privacy/continuity/coordination presentation contract passed its 1.6 promotion gates. Their filenames and embedded historical Candidate labels are intentionally not rewritten to pretend they were originally 2.2 artifacts.

## Current 2.2 acceptance boundary

The source contract, tokens, schema, reference Mesh consumer, and automated consumer tests include GoreeCloud Identity as an explicit authority and fail closed on producer/domain mismatch. Stable 2.2 carries this contract forward under the current material, System Shell, component, and accessibility systems.

This source-level integration does **not** by itself establish downstream Identity Center acceptance, downstream application adoption, native-platform acceptance, real-device accessibility validation, or production runtime acceptance. Those require separate evidence before application claims are upgraded.
