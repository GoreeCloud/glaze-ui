# GLAZE UI — Security and Authority Boundary

## Current lifecycle

- Current Official Stable: GLAZE UI V1.5 / `1.5.1`
- Active governed successor: GLAZE UI V1.6 / `1.6.0-rc.1`
- V1.6 consumer eligible: No
- Lifecycle authority: `VERSION` and `registry/lifecycle.json`

## Security role

Glaze UI is a shared presentation and interaction design system. It does not establish authentication, authorization, encryption, malware protection, privacy authorization, policy decisions, backup, recovery, network trust, service health, or operational security state.

Glaze UI may present authoritative state supplied by the responsible system, but it must not create, upgrade, infer, or silently substitute that state.

## Authoritative producers

Depending on the consuming product and capability, authoritative truth may come from:

- GoreeCloud Identity for identity and authentication state.
- Wardveil Security for security/protection state.
- GoreeCloud Privacy Shield for privacy and data-use state.
- Everkeep for backup, restore, recovery, and preservation state.
- GoreeCloud Mesh for registered capability and coordination state.
- GoreeCloud Policy for policy decisions and enforcement state.
- GoreeCloud Observability for operational-health and monitoring evidence.
- GoreeCloud Manager for authorized administrative visibility and control-plane state.
- The consuming application, operating system, runtime, or other documented producer for domains it legitimately owns.

Glaze UI remains the presentation authority for its own design-system semantics only.

## Required behavior

Glaze UI source and consumers must:

- Fail closed when required authority or provenance is conflicting, stale, malformed, unavailable, or unknown.
- Distinguish unknown, unavailable, restricted, denied, unsupported, degraded, and unverified states rather than coercing them into favorable state.
- Avoid UI-only controls that imply backend security enforcement that does not exist.
- Avoid automatic permission grants, automatic authorization, or consequential execution based only on presentation state.
- Minimize diagnostic context and avoid raw private content, credentials, session material, provider secrets, and unnecessary identifiers.
- Keep public client and reference assets free of privileged secrets.
- Preserve accessibility and protected semantic meaning during security, privacy, denial, recovery, or degraded-state presentation.
- Treat downstream application security acceptance as separate from shared Glaze UI qualification.

## V1.6 Release Candidate boundary

The V1.6 governed qualification review records explicit Release Candidate evaluation against the nine Integral Platform Systems. That review verifies the design system's applicable authority boundaries; it does not grant Stable security qualification, production readiness, deployment acceptance, or downstream consumer security acceptance.

Stable promotion remains subject to the current Stable Release Security Blockers standard and exact-candidate security evidence.
