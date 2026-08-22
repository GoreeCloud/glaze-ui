# Glaze UI Consumer Compatibility

Glaze UI consumer stability is version-specific and evidence-based. The machine-readable audit is `consumers/registry.json`.

## Consumer states

### Aligned — current Stable
Targets the current Stable version with reviewed revision, repository-local evidence, automated contract where applicable, and completed product acceptance.

### Aligned — older Stable
Intentionally remains on an earlier Stable version with version-specific evidence. Older Stable is supported and is not automatic migration debt.

### Adoption Candidate
Evidence-backed adoption of a supported Stable Glaze version where final application-specific acceptance remains incomplete. An Adoption Candidate may target the current or an older supported Stable release; the status describes the **consumer's** acceptance state, not the design-system lifecycle.

### Unverified
Version-specific evidence has not yet been established. Unverified is an evidence gap, not an automatic non-conformance finding.

## Audited consumers after Glaze UI 1.4 promotion

- **GoreeCloud Manager** — `aligned-older-stable`, target 1.3.0, evidence `docs/glaze-ui.md`.
- **GoreeCloud Website** — `aligned-older-stable`, target 1.1.0, evidence `docs/glaze-ui-conformance.md`.
- **GoreeCloud Tasks** — `adoption-candidate`, target 1.3.0, evidence `docs/glaze-ui.md`; automated representative acceptance passed but final native/manual production acceptance remains pending.
- **GoreeCloud Notes** — `unverified`.
- **GoreeCloud Monitor** — `unverified`.

No consumer is automatically migrated to 1.4.0 by the design-system promotion.

## Rules for consumer claims

A repository claiming version-specific alignment identifies target version, reviewed canonical revision/release anchor, repository-local mapping, automated checks, rendered/native/real-device acceptance boundary, and explicit exceptions/unsupported contexts.

A Stable consumer **must not silently depend on Candidate or Experimental** behavior. Planned roadmap concepts are not shipping dependencies.
