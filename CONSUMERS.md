# Glaze UI Consumer Enforcement

Glaze UI consumer conformance is current-Stable, evidence-based, and mandatory. The machine-readable audit is `consumers/registry.json`.

## Mandatory current Stable target

Glaze UI **1.6.0** is the current Stable baseline and the only Glaze UI version that may satisfy current GoreeCloud application conformance or production-readiness requirements. Earlier Stable releases remain historical release, migration, rollback, and audit records only. They are not valid long-term application targets and do not satisfy the current production gate.

When a newer Glaze UI release is promoted to Stable, every GoreeCloud-controlled user-facing application must migrate to that new current Stable release through controlled, evidence-backed adoption. Controlled migration governs how the upgrade is performed; it does not make migration optional.

No production exception, grandfathering rule, compatibility pin, upstream styling allowance, schedule exemption, platform exemption, or convenience exemption permits a GoreeCloud application to remain on an older Glaze UI version.

## Platform scope

This rule applies to every GoreeCloud-controlled user-facing presentation layer, including web applications, progressive web applications, Linux and other desktop applications, mobile applications, tablet applications, TV applications, smartwatch and wearable applications, dashboards, administrative interfaces, family-facing interfaces, maintained forks, and other controlled user-facing software.

A headless, protocol-only, infrastructure-only, or library component with no controlled user interface is outside visual Glaze UI scope; that is a scope classification, not an exception. If that component later gains a controlled user interface, the current-Stable requirement applies immediately.

If the current Stable Glaze UI release does not yet provide an applicable Stable contract for a required user-facing platform or interaction environment, the application is production-blocked until the design system is extended, validated, and promoted with the required Stable contract. Missing platform support never creates an application exception.

## Consumer states

### Aligned — current Stable
Targets the current Stable version with reviewed revision evidence, repository-local mapping, applicable automated contract validation, and completed product acceptance. This is the only consumer state eligible to satisfy the Glaze UI production gate.

### Adoption Candidate
Targets the current Stable version with evidence-backed adoption in progress, but final application-specific rendered, native, real-device, accessibility, or production acceptance remains incomplete. Adoption Candidate is not production-accepted Glaze UI conformance.

### Migration Required
Still targets a historical Glaze UI release. Historical evidence remains useful as migration input and audit history, but the consumer is nonconforming with the current-Stable requirement and is production-blocked on the Glaze UI gate until migration and acceptance are complete.

### Unverified
Current-Stable version-specific evidence has not been established. Unverified is an evidence gap and cannot satisfy the production gate.

## Current audited consumers

- **GoreeCloud Manager** — `migration-required`, current recorded target 1.3.0; required target 1.6.0.
- **GoreeCloud Website** — `migration-required`, current recorded target 1.5.0; required target 1.6.0. The repository-local conformance record now supersedes the older 1.1 central snapshot, but 1.5 remains historical rather than current-Stable.
- **GoreeCloud Tasks** — `migration-required`, current recorded target 1.3.0; required target 1.6.0.
- **GoreeCloud Launcher** — `adoption-candidate`, target 1.6.0; required target 1.6.0; native/rendered/accessibility/reduced-motion/physical-device acceptance remains pending and production eligibility remains false. Its local record now points to the canonical 1.6 Stable promotion revision.
- **GoreeCloud Keyboard** — `adoption-candidate`, target 1.6.0; required target 1.6.0; phone/tablet native and rendered Glaze UI, TalkBack/switch-access, representative physical-device, and production acceptance remain pending and production eligibility remains false. Its local record now points to the canonical 1.6 Stable promotion revision.
- **GoreeCloud Notes** — `unverified`; the previously registered versioned evidence path is absent on current main. The repository's platform-conformance policy remains governance evidence, not proof of a specific Glaze implementation version.
- **GoreeCloud Monitor** — `migration-required`, current recorded target 1.0.0; required target 1.6.0.

Launcher contains a test-only Glaze Motion 0.4 Experimental evaluation against its real workspace ordering domain. Keyboard contains a test-only Glaze Motion 0.5 Experimental evaluation against its real native `KeyboardView` key-release and suggestion-selection paths, including an Android 15 emulator reduced-motion check. These evaluations strengthen Glaze Motion development governance but do not make Experimental Motion a production dependency and do not satisfy either application's incomplete Glaze UI product-acceptance gates.

## Audit completeness

The seven named repositories above form the current central audit set. The central audit does not limit the policy scope: the mandatory current-Stable rule applies to every GoreeCloud-controlled user-facing application whether or not it is already represented in this central registry.

Removing an audited repository from the machine-readable registry requires an explicit audit-scope change rather than silently reducing coverage. Every application repository remains responsible for its own current-Stable mapping, CI, rendered/native/real-device acceptance, and production-readiness evidence.

The August 28, 2026 reconciliation corrected stale central metadata without upgrading consumers by declaration: Website is recorded at its evidenced 1.5 historical contract, Launcher and Keyboard use their current 1.6 reviewed promotion revision, and Notes is fail-closed to Unverified because its former evidence path is no longer present.

## Rules for consumer claims

A repository claiming current-Stable alignment must identify the current Glaze UI version, reviewed canonical revision or release anchor, repository-local mapping or conformance record, applicable automated checks, rendered/native/real-device acceptance boundary, and supported platform contexts.

A Stable consumer **must not silently depend on Candidate or Experimental** behavior. Planned roadmap concepts are not shipping dependencies.

An older-version exact claim may be preserved only as historical evidence, for example to describe what a previous release implemented. It must never be represented as current conformance, current-Stable alignment, or production UI acceptance.
