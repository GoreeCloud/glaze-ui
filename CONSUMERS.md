# Glaze UI Consumer Enforcement

Glaze UI consumer conformance is current-Stable, evidence-based, and mandatory. The machine-readable audit is `consumers/registry.json`.

## Mandatory current Stable target

Glaze UI **2.2.0** is the current Stable baseline and the only Glaze UI version that may satisfy current GoreeCloud application conformance or production-readiness requirements. Earlier Stable releases, including 2.1.0 and 2.0.0, remain historical release, migration, rollback, and audit records only.

When a newer Glaze UI release is promoted Stable, every GoreeCloud-controlled user-facing application must migrate through controlled, evidence-backed adoption. Controlled migration governs how the upgrade is performed; it does not make migration optional.

**No production exception**, grandfathering rule, compatibility pin, platform exemption, schedule exemption, or convenience exemption permits an application to remain on a superseded Glaze UI version.

## Preserved Glaze UI 2.2 Candidate assessment

The canonical `consumers/registry.json` preserves the bounded assessment layer for **2.2.0-candidate.1** as promotion provenance. It records the Candidate boundary before 2.2.0 became Stable; it is not a current Candidate baseline, a second consumer registry, or a substitute for Stable 2.2 conformance.

A preserved 2.2 Candidate evaluation is historical readiness evidence only. It cannot make a consumer production eligible under the current Stable baseline, and it cannot rewrite the consumer's current 2.2 conformance state.

The preserved Candidate evaluation list is empty. Therefore no downstream application is represented as having completed a centrally recorded 2.2 Candidate evaluation. Absence from that historical list never implies compatibility, adoption, readiness, conformance, or approval.

## Platform scope

The current-Stable rule applies to every GoreeCloud-controlled user-facing presentation layer: web/PWA, Linux and other desktop, mobile, tablet, TV, smartwatch/wearable, dashboard, administrative, family-facing, maintained fork, spatial/hardware surface, and other controlled interface where Glaze UI applies.

A headless/protocol/infrastructure-only component with no controlled UI is outside visual scope; that is a scope classification, not an exception. If it gains a controlled UI, the current-Stable requirement applies. GoreeCloud Messenger's current repository service is headless in this audit and therefore does not claim visual Glaze UI conformance; any first-party Messenger client surface must enter the consumer registry before production qualification.

Glaze UI 2.2 contains platform-neutral system-shell, component, adaptive, accessibility, motion, contrast, transparency, and input contracts plus a bounded Android handheld native reference. A native/hardware consumer still requires application-specific native, accessibility, performance, system-integration, and representative real-device acceptance.

## Consumer states

### Aligned — current Stable
Targets 2.2.0 with reviewed revision evidence, repository-local mapping, applicable automated validation, and completed product acceptance. This is the only state eligible to satisfy the Glaze UI production gate.

### Adoption Candidate
Targets 2.2.0 with evidence-backed adoption in progress, but final product acceptance remains incomplete. Adoption Candidate is not production-accepted conformance.

### Migration Required
Still targets a historical Stable release. Historical evidence remains migration input and audit history, but the consumer is nonconforming with current Stable and production-blocked on the Glaze UI gate.

### Unverified
Current-Stable version-specific evidence has not been established. Unverified cannot satisfy the production gate.

## Current audited consumers

- **GoreeCloud Manager** — `migration-required`, recorded 1.3.0; required 2.2.0.
- **GoreeCloud Website** — `migration-required`, recorded 1.5.0; required 2.2.0.
- **GoreeCloud Tasks** — `migration-required`, recorded 1.3.0; required 2.2.0.
- **GoreeCloud Launcher** — `adoption-candidate`, targets 2.2.0 with exact repository evidence at `a87f5b1bf20ce8005ca589bd4a38efa8440e7500`; final rendered/native/accessibility/reduced-motion/contrast/transparency/phone-tablet/representative-device acceptance remains required before current-Stable alignment or production approval.
- **GoreeCloud Keyboard** — `adoption-candidate`, targets 2.2.0 with exact repository evidence at `e56ec4a01dde4024aa5ef54b3d13fd681ef8ada7`; the source evidence now includes unified viewport-bounded alternate-popup rendering/pointer hit testing, while phone/tablet native/rendered, TalkBack/switch-access, representative physical-device long-press/slide/release and compact-width ergonomics, and production acceptance remain required before current-Stable alignment.
- **GoreeCloud Notes** — `unverified`; fresh repository-local 2.2 implementation evidence is required.
- **GoreeCloud Monitor** — `migration-required`, recorded 1.0.0; required 2.2.0.
- **GoreeCloud Browser** — `migration-required`, recorded 2.0.0; required 2.2.0. Its 2.0 implementation evidence remains historical migration input.
- **GoreeCloud Security Center** — `migration-required`, recorded 2.0.0; required 2.2.0. Wardveil Security retains security-truth authority; a source migration branch or preview does not by itself satisfy current-Stable application acceptance.
- **GoreeCloud Privacy Center** — `migration-required`, recorded 2.0.0; required 2.2.0. Privacy Shield retains privacy-truth authority; a source migration branch or preview does not by itself satisfy current-Stable application acceptance.

These states are evidence-backed rather than declarative. `adoption-candidate` means the consumer now targets the current Stable release with repository-local exact-revision validation, but it remains production-ineligible until its application-specific acceptance gates are complete. No repository is promoted to `aligned-current-stable` merely because 2.2 source migration exists or a preview renders successfully. Current-Stable conformance requires the exact application-specific evidence recorded by the registry.

Launcher and Keyboard retain earlier Glaze Motion evaluations as historical development evidence. Stable Glaze UI 2.2 does not turn unrelated Experimental behavior into a production dependency by implication.

## Audit completeness

The ten named repositories above form the current central audit set. This set does not limit policy scope: the current-Stable rule applies to every GoreeCloud-controlled user-facing application whether or not it is already represented in the central registry.

Removing an audited repository requires an explicit audit-scope change rather than silently reducing coverage. Each application repository remains responsible for its own current-Stable mapping, CI, rendered/native/real-device acceptance, and production-readiness evidence.

## Rules for consumer claims

A repository claiming current-Stable alignment must identify Glaze UI 2.2.0, the reviewed canonical revision/release anchor, repository-local mapping/conformance record, applicable automated checks, product acceptance boundary, and supported platform contexts.

A Stable consumer **must not silently depend on Candidate or Experimental** behavior. New consumers should use the versioned Stable entrypoints and contracts defined by the 2.2 Stable release documentation. Retained Candidate-named implementation files are promotion provenance and controlled compatibility evidence rather than production aliases.

An older exact-version claim may be preserved only as historical evidence. It must never be represented as current conformance, current-Stable alignment, or production UI acceptance.
