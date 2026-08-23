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
- **GoreeCloud Launcher** — `adoption-candidate`, target 1.4.0, evidence `docs/glaze-ui-adoption.md`; the mapped native token/evidence subset is enforced by launcher CI while phone/tablet visual/native and physical-device acceptance remain pending.
- **GoreeCloud Notes** — `adoption-candidate`, target 1.0.0, evidence `frontend/scripts/validate-glaze-foundation.mjs`; the active native-foundation draft line vendors and validates the canonical 1.0 web foundation, while real-device/network performance and accessibility acceptance remains pending.
- **GoreeCloud Monitor** — `adoption-candidate`, target 1.0.0, evidence `static/monitoring/css/glaze.css`; the active stable-foundation draft line implements and validates a repository-local Glaze layer, while target-environment rendered/accessibility and production acceptance remain pending.

No consumer is automatically migrated to 1.4.0 by the design-system promotion. An older supported target is not itself a defect; migration should be justified by product need and must retain product-specific acceptance.

## Audit completeness

The six named repositories above form the current central audit set. Removing one from the machine-readable registry requires an explicit audit-scope change rather than silently reducing coverage. The registry validator fails closed if the audited repository set changes unexpectedly.

The central audit records evidence and acceptance state; it does not replace each consumer repository's own CI, native/runtime checks, visual review, production-readiness gates, or release decision.

## Rules for consumer claims

A repository claiming version-specific alignment identifies target version, reviewed canonical revision/release anchor, repository-local mapping, automated checks, rendered/native/real-device acceptance boundary, and explicit exceptions/unsupported contexts.

A Stable consumer **must not silently depend on Candidate or Experimental** behavior. Planned roadmap concepts are not shipping dependencies.
