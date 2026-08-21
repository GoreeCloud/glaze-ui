# Glaze UI Consumer Compatibility

Glaze UI is a shared dependency, but GoreeCloud applications do not all need to track the newest Stable release at the same moment. Consumer stability is version-specific and evidence-based.

The machine-readable audit lives in `consumers/registry.json`.

## Consumer states

### Aligned — current Stable

A consumer is `aligned-current-stable` when it explicitly targets the current Stable Glaze UI version, records a reviewed canonical source revision, and has repository-local conformance evidence appropriate to that application.

This state does **not** mean the consumer must repin to every later documentation-only or governance-only commit on Glaze UI `main`. A recorded, reviewed revision from the same Stable semantic contract remains a valid consumer anchor until a material design-system change or application migration requires renewed acceptance.

### Aligned — older Stable

A consumer is `aligned-older-stable` when it intentionally targets an earlier Stable Glaze UI release with its own version-specific conformance evidence.

This is supported behavior under `STABILITY.md`. Older Stable consumers are not automatically migration failures. They should move only when the migration has a product-specific reason, compatibility review, and acceptance evidence.

### Unverified

A consumer is `unverified` when the audit has not established a version-specific Glaze UI contract from the reviewed repository evidence.

Unverified means **evidence is incomplete**. It does not mean the application violates Glaze UI, has no Glaze styling, or is unsuitable for development. An unverified consumer should gain a repository-local contract before claiming version-specific Glaze conformance or production UI acceptance.

## Initial audited consumers

### GoreeCloud Manager

- Repository: `GoreeCloud/goreecloud-manager`
- State: `aligned-current-stable`
- Target: Glaze UI 1.3.0 Stable
- Evidence: `docs/glaze-ui.md`
- Automated source-level contract: yes
- Material interface changes still require application-specific rendered/browser acceptance.

Manager records a reviewed 1.3.0 source revision rather than blindly following the latest Glaze UI `main` SHA. That is intentional and compatible with the Stable consumer policy.

### GoreeCloud Website

- Repository: `GoreeCloud/goreecloud-website`
- State: `aligned-older-stable`
- Target: Glaze UI 1.1.0 Stable
- Evidence: `docs/glaze-ui-conformance.md`
- Automated source-level contract: yes

The public website is deliberately version-pinned to 1.1.0. Its older Stable target remains valid until a controlled website-specific upgrade is justified and accepted.

### GoreeCloud Tasks

- Repository: `GoreeCloud/goreecloud-tasks`
- State: `unverified`

The reviewed README and documentation surface did not establish a dedicated version-specific Glaze UI contract. This is an audit/evidence gap, not a finding that the interface is non-conformant.

### GoreeCloud Notes

- Repository: `GoreeCloud/goreecloud-notes`
- State: `unverified`

The native Notes repository is initialized for first-party development, but the reviewed repository surface does not yet establish a version-specific Glaze UI consumer record.

### GoreeCloud Monitor

- Repository: `GoreeCloud/goreecloud-monitor`
- State: `unverified`

Monitor is under active native development, but the reviewed repository surface does not yet establish a version-specific Glaze UI consumer record.

## Rules for consumer claims

A GoreeCloud repository must not claim version-specific Glaze UI alignment unless it can identify:

1. the Glaze UI semantic version it targets;
2. a reviewed canonical source revision or release anchor;
3. the repository-local mapping or conformance record;
4. the automated source-level checks that protect the mapping when applicable;
5. the rendered, native, or real-device acceptance boundary appropriate to the product;
6. any explicit exceptions or unsupported contexts.

A consumer must not silently depend on Candidate or Experimental Glaze UI behavior while claiming Stable conformance.

## Audit behavior

The central registry is intentionally conservative:

- it records only evidence actually reviewed;
- it does not infer conformance from visual resemblance;
- it does not force older Stable consumers forward;
- it does not treat an unverified consumer as failed;
- it does not replace application-specific CI or visual acceptance;
- it must not contain credentials, private runtime details, or unrelated infrastructure information.

The registry should be expanded gradually as each GoreeCloud consumer receives an evidence-backed review.
