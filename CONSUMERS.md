# Glaze UI Consumer Enforcement

Glaze UI consumer conformance is current-Stable, evidence-based, and mandatory. The machine-readable audit is `consumers/registry.json`.

## Mandatory current Stable target

Glaze UI **2.0.0** is the current Stable baseline and the only Glaze UI version that may satisfy current GoreeCloud application conformance or production-readiness requirements. Earlier Stable releases remain historical release, migration, rollback and audit records only.

When a newer Glaze UI release is promoted Stable, every GoreeCloud-controlled user-facing application must migrate through controlled, evidence-backed adoption. Controlled migration governs how the upgrade is performed; it does not make migration optional.

**No production exception**, grandfathering rule, compatibility pin, platform exemption, schedule exemption or convenience exemption permits an application to remain on a superseded Glaze UI version.

## Platform scope

The current-Stable rule applies to every GoreeCloud-controlled user-facing presentation layer: web/PWA, Linux and other desktop, mobile, tablet, TV, smartwatch/wearable, dashboard, administrative, family-facing, maintained fork, spatial/hardware surface and other controlled interface where Glaze UI applies.

A headless/protocol/infrastructure-only component with no controlled UI is outside visual scope; that is a scope classification, not an exception. If it gains a controlled UI, the current-Stable requirement applies.

Glaze UI 2.0 contains platform-neutral wearable and spatial contracts. A native/hardware consumer still requires application-specific native, accessibility, performance, system-integration and representative real-device acceptance.

## Consumer states

### Aligned — current Stable
Targets 2.0.0 with reviewed revision evidence, repository-local mapping, applicable automated validation and completed product acceptance. This is the only state eligible to satisfy the Glaze UI production gate.

### Adoption Candidate
Targets 2.0.0 with evidence-backed adoption in progress, but final product acceptance remains incomplete. Adoption Candidate is not production-accepted conformance.

### Migration Required
Still targets a historical 1.x release. Historical evidence remains migration input/audit history, but the consumer is nonconforming with current Stable and production-blocked on the Glaze UI gate.

### Unverified
Current-Stable version-specific evidence has not been established. Unverified cannot satisfy the production gate.

## Current audited consumers

- **GoreeCloud Manager** — `migration-required`, recorded 1.3.0; required 2.0.0.
- **GoreeCloud Website** — `migration-required`, recorded 1.5.0; required 2.0.0.
- **GoreeCloud Tasks** — `migration-required`, recorded 1.3.0; required 2.0.0.
- **GoreeCloud Launcher** — `adoption-candidate`, targets 2.0.0 at consumer merge `88e7007013ac096a39f04ff4a3993591ef2ed5f2`; final application acceptance remains pending and production eligibility remains false.
- **GoreeCloud Keyboard** — `migration-required`, recorded 1.6.0 Adoption Candidate evidence is now historical migration input; required 2.0.0.
- **GoreeCloud Notes** — `unverified`; fresh repository-local 2.0 implementation evidence is required.
- **GoreeCloud Monitor** — `migration-required`, recorded 1.0.0; required 2.0.0.

The Launcher state change is evidence-backed rather than declarative: Launcher main now contains repository-local 2.0 mapping and automated validation. Its central `referenceRevision` is the consumer adoption merge anchor; the Launcher adoption document separately records canonical Glaze UI Stable revision `ff3fff4306bd53ea9c0715a7c0d64265bb038617`.

No other downstream application is upgraded to 2.0 by this registry reconciliation. Exact prior revisions/evidence paths remain preserved so migration work starts from verified history rather than a declaration.

Launcher and Keyboard retain test-only Glaze Motion evaluations as historical development evidence. Glaze Motion remains Experimental and must not become a production dependency by implication of the 2.0 design-system release or Launcher adoption.

## Audit completeness

The seven named repositories above form the current central audit set. This set does not limit policy scope: the current-Stable rule applies to every GoreeCloud-controlled user-facing application whether or not it is already represented in the central registry.

Removing an audited repository requires an explicit audit-scope change rather than silently reducing coverage. Each application repository remains responsible for its own current-Stable mapping, CI, rendered/native/real-device acceptance and production-readiness evidence.

## Rules for consumer claims

A repository claiming current-Stable alignment must identify Glaze UI 2.0.0, the reviewed canonical revision/release anchor, repository-local mapping/conformance record, applicable automated checks, product acceptance boundary and supported platform contexts.

A Stable consumer **must not silently depend on Candidate or Experimental** behavior. The promoted 2.0 implementation retains some Candidate-named files only to preserve exact promotion provenance; their current lifecycle is governed by `GLAZE_UI_2_STABLE.md` and the release state, not by the filename.

An older exact-version claim may be preserved only as historical evidence. It must never be represented as current conformance, current-Stable alignment or production UI acceptance.
