# Glaze UI Current Stable Consumer Enforcement

**Status:** Active enforcement contract  
**Authority:** `GoreeCloud/goreecloud-glaze-ui`  
**Current Stable source:** `VERSION` + `registry/lifecycle.json` + `consumers/registry.json`

## Policy

Every applicable GoreeCloud user-facing application, website, client, and interface must target the current Official Stable Glaze UI release.

A GoreeCloud product must not be considered, labeled, published, or promoted as Stable merely because it visually resembles Glaze UI or because it passed an older Glaze UI release. A Stable claim requires current-Stable Glaze UI verification for the consumer's complete declared user-facing platform scope.

When Glaze UI promotes a new Official Stable release, a consumer that still targets an older release becomes out of policy for new Stable claims until it migrates and supplies fresh repository-local acceptance evidence.

This enforcement does not transfer product lifecycle authority to Glaze UI. Passing the Glaze gate is necessary for a Stable claim, but it is not sufficient for production eligibility. Product-specific accessibility, security, privacy, native-platform, performance, rollback, release, and other acceptance obligations remain independently governed.

## Repository-local conformance manifest

Consumers should keep a manifest at:

```text
.goreecloud/glaze-ui-conformance.json
```

The canonical structure is defined by:

- `schemas/downstream-current-stable-conformance.schema.json`
- `templates/downstream-current-stable-conformance.template.json`

The manifest identifies the consumer, repository, Glaze UI target, adoption state, Stable-claim intent, complete user-facing platform coverage assertion, and per-platform acceptance state.

An `accepted` platform must reference repository-local evidence by path, SHA-256 digest, and exact 40-character consumer `sourceRevision`. The gate recomputes the digest and compares the evidence revision to the consumer revision under test. Replacing or mutating evidence, or attempting to reuse evidence from an older consumer revision, causes validation to fail.

The fail-closed template is itself tied to the current central Stable version. Central source validation fails if Glaze UI promotes a new Stable release without updating the downstream template target.

## Development mode

Development mode verifies that the consumer targets the current Glaze UI Stable version and that its manifest/evidence relationships are internally valid. A consumer may remain `adoption-required` or `unverified` while migration work is incomplete.

Development mode does not authorize a Stable claim.

## Stable-claim mode

Stable-claim mode is fail-closed. It requires all of the following:

- `stableClaim` is explicitly `true`.
- `targetVersion` exactly equals the central current Stable `VERSION`.
- `status` is `accepted-v1`.
- `coverage.allUserFacingPlatformsEnumerated` is `true`.
- Every enumerated user-facing platform is `accepted`.
- Every accepted platform has repository-local evidence.
- Every evidence SHA-256 digest matches the exact referenced file.
- Every accepted evidence record is bound to the exact consumer source revision under test.
- The manifest repository identity matches the repository executing the workflow.
- The exact Glaze UI policy revision used to evaluate the consumer is recorded.
- The current consumer source revision is recorded in the generated gate report.

A single accepted platform never implies acceptance of another platform.

## Reusable GitHub Actions gate

Consumer repositories can call the central gate without copying validator logic:

```yaml
name: Glaze UI Current Stable

on:
  pull_request:
  push:
    branches: [main]

jobs:
  glaze-ui:
    uses: GoreeCloud/goreecloud-glaze-ui/.github/workflows/current-stable-consumer-gate.yml@main
    with:
      manifest-path: .goreecloud/glaze-ui-conformance.json
      stable-claim: false
```

The reusable workflow always checks out the current `main` policy authority from `GoreeCloud/goreecloud-glaze-ui`. This is intentional: consumer validation must follow the latest Official Stable Glaze UI authority instead of silently remaining pinned to an obsolete design-system release. The exact policy commit checked out at runtime is captured in the generated gate report.

A release or Stable-promotion workflow must invoke the same reusable workflow with:

```yaml
with:
  manifest-path: .goreecloud/glaze-ui-conformance.json
  stable-claim: true
```

The Stable-claim invocation should be a required release check wherever repository policy supports required status checks.

## Exact-revision report

Each successful reusable-workflow run writes and uploads `glaze-ui-current-stable-gate-report.json`.

The report binds the validation result to both sides of the authorization decision and records:

- exact consumer source revision,
- exact Glaze UI policy revision,
- current central Stable version,
- consumer target version,
- Stable-claim mode,
- platform coverage counts,
- accepted platform state,
- verified evidence paths, SHA-256 values, and evidence source revisions,
- the authority boundary stating that overall product Stable/production eligibility remains independently governed.

The report is CI evidence for the exact workflow decision. It does not replace the underlying repository-local acceptance records.

## Release transition behavior

Glaze UI release promotion should update `VERSION`, lifecycle authority, consumer registry authority, and the fail-closed downstream template target atomically. Because downstream validation reads those central authorities at runtime, a newly promoted Stable release immediately becomes the required target for subsequent consumer gate runs.

Existing historical acceptance remains useful as migration provenance but does not satisfy a new current-Stable claim. Evidence from an older source revision also cannot be replayed against a changed consumer revision.

## No global visual pass

Glaze UI conformance is intentionally scoped by consumer and platform. The enforcement system must not collapse web, Android, desktop, TV, watch, tablet, foldable, or other surfaces into a single misleading global "uses Glaze UI" state.

Each consumer must prove the platforms it actually claims.
