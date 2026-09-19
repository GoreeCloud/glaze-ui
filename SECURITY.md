# GLAZE UI — Security and Authority Boundary

## Current lifecycle

- Current Official Stable: GLAZE UI V1.6 / `1.6.0`
- Stable runtime: `js/glaze-v1.6.0.mjs`
- Immediate known-good rollback Stable: GLAZE UI V1.5 / `1.5.1`
- Retained V1.6 Release Candidate provenance: `1.6.0-rc.1` (superseded, non-consumer-eligible)
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

## V1.6 Stable security acceptance

Final Stable security acceptance is complete for exact accepted source `a7180679ea851389e0f3004515f9a25f420e716d` and the exact published V1.6.0 artifact bytes.

Verified release-security evidence includes:

- Complete Git-history secret scanning with 0 unreviewed findings after exact-fingerprint review of 21 retained historical false positives.
- A remediated Gradle-selected Android/Wear build-tool graph containing 206 distinct selected Maven coordinates / 426 selected package entries, with 0 selected OSV advisories and a 206-component CycloneDX dependency SBOM with 0 vulnerabilities.
- Deterministic final artifact preparation, SHA-256 checksum verification, CycloneDX 1.5 runtime/source SBOM, provenance bound to exact source/tree, archive-boundary validation, and an extracted-artifact Gitleaks scan with no leaks.
- Active GitHub ruleset `23699829` on `main`, with an empty bypass list, pull-request integration, strict required checks, conversation resolution, deletion protection, and force-push protection.
- Controlled `v1.6.0` publication without rebuild and post-publication byte readback matching the security-accepted archive, SBOM, provenance, and checksum manifest.
- A complete Stable Release Security Blockers applicability matrix: 39 controls evaluated, 14 Passed/Passed-bounded, 25 Not Applicable with justification, 0 Blocked, 0 Unknown, 0 Excepted, and no security exceptions.

Security acceptance closes the security gate; it does not transfer authentication, authorization, privacy, recovery, monitoring, or production authority into Glaze UI and does not automatically grant downstream application security or production acceptance.
