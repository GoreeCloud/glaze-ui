# GLAZE UI — User Manual

## Audience

This manual is for GoreeCloud developers, designers, maintainers, reviewers, and downstream application teams that consume or evaluate Glaze UI.

Glaze UI is a shared design-system and interaction runtime, not an end-user application.

## Current lifecycle

- **Current Official Stable:** GLAZE UI V1.6 / `1.6.0`
- **Stable runtime:** `js/glaze-v1.6.0.mjs`
- **Stable web/material baseline:** `css/glaze-v1.4.1.css` where not superseded by V1.6 semantic contracts
- **Immediate rollback Stable:** GLAZE UI V1.5 / `1.5.1`
- **Retained Release Candidate provenance:** `1.6.0-rc.1` (superseded, non-consumer-eligible)
- **Current consumer target:** `1.6.0`
- **Lifecycle authority:** `VERSION` and `registry/lifecycle.json`

Do not infer lifecycle state from a filename, branch name, screenshot, historical changelog entry, or retained Candidate/Development record.

## Using the current Stable release

Downstream production or Stable consumer work must use the current Stable target unless a separately governed migration or test explicitly authorizes another lifecycle state.

For V1.5.1:

1. Use the Stable contract and runtime identified by the repository front-door documentation.
2. Preserve semantic tokens and authority boundaries rather than copying raw appearance values into an application-local design system.
3. Implement application-specific states, flows, and native mappings using Glaze semantics appropriate to the supported platform.
4. Run the consumer's own rendered/native/accessibility/platform validation.
5. Record exact source revision and evidence in the consumer repository.
6. Do not claim consumer conformance merely because Glaze UI itself is Stable.

## Evaluating V1.6 Release Candidate

V1.6 `1.6.0-rc.1` is available for governed qualification, migration planning, and controlled evaluation. It is not the current consumer target.

Use the RC only when the task explicitly requires Release Candidate evaluation. Preserve these boundaries:

- Do not automatically migrate production consumers.
- Do not treat RC status as Stable.
- Do not publish or deploy the RC as production by implication.
- Keep qualification evidence bound to the exact source and evidence records that produced it.
- Re-run applicable validation if the exact candidate source changes materially.

## Authority boundaries

Glaze UI controls presentation and interaction semantics. It does not authenticate users, grant permissions, decide policy, establish privacy/security/recovery truth, perform backup, register Mesh capability, or declare production health.

When presenting authoritative state:

- Preserve producer provenance.
- Fail closed on conflict or unknown state.
- Never convert unavailable evidence into a positive state.
- Never let color alone communicate protected meaning.
- Do not execute consequential fallback or permission actions automatically.

## Accessibility

Consumers must preserve applicable Glaze accessibility requirements, including:

- Keyboard and focus behavior.
- Minimum interaction targets.
- Contrast.
- Reduced Motion.
- Reduced Transparency.
- Forced Colors.
- Large-text and reflow behavior.
- Screen-reader and semantic-label behavior.
- Touch, pointer, remote, and supported input adaptation.
- State communication that does not depend on color alone.

Shared design-system qualification does not replace consumer-specific accessibility acceptance.

## Loading, degraded, and recovery states

Use semantic loading, progress, empty, offline, stale, degraded, denied, error, and recovery states according to the active Glaze contract. Do not present fabricated progress, invented recovery capability, or successful state before the authoritative operation has succeeded.

## Version and release changes

Lifecycle changes are controlled work. Do not change `VERSION`, `registry/lifecycle.json`, current Stable entrypoints, consumer eligibility, tags, or release records as an incidental side effect of ordinary feature or documentation work.

## Reporting problems

For security-sensitive findings, follow `SECURITY.md` and applicable GoreeCloud security governance. For implementation, contract, accessibility, rendering, or conformance defects, use the repository's governed issue and pull-request workflow with exact revision identity and reproducible evidence.
