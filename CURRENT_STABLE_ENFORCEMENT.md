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

An `accepted` platform must reference repository-local evidence by path, SHA-256 digest, and exact 40-character consumer `sourceRevision`. `sourceRevision` identifies the implementation commit that was actually reviewed; it does not need to equal the later governance commit that records the evidence.

To prevent stale evidence replay, the gate fetches consumer Git history and proves that the reviewed revision is an ancestor of the current revision. Any files changed after review must be limited to the conformance manifest itself and the evidence files declared by the manifest. If application source, UI resources, build files, or any other undeclared path changes after review, that platform evidence is rejected as stale and must be refreshed.

This evidence-only transition avoids a self-referential commit problem: the act of committing a review record naturally creates a later Git revision, but that later revision cannot smuggle product changes past the review.

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
- Every accepted evidence record names an exact reviewed implementation revision available in Git history.
- Every reviewed implementation revision is an ancestor of the consumer revision under test.
- Every post-review change is limited to the manifest and declared evidence files; any product/source drift blocks the claim.
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

The reusable workflow checks out complete consumer Git history so it can prove review continuity, and it checks out the current `main` policy authority from `GoreeCloud/goreecloud-glaze-ui`. This is intentional: consumer validation must follow the latest Official Stable Glaze UI authority instead of silently remaining pinned to an obsolete design-system release. The exact policy commit checked out at runtime is captured in the generated gate report.

A release or Stable-promotion workflow must invoke the same reusable workflow with:

```yaml
with:
  manifest-path: .goreecloud/glaze-ui-conformance.json
  stable-claim: true
```

The Stable-claim invocation should be a required release check wherever repository policy supports required status checks.

## Recommended review sequence

The recommended flow is:

1. Land the implementation revision to be reviewed with the Glaze gate workflow and fail-closed manifest already present.
2. Perform product/platform review against that exact implementation commit.
3. Commit the resulting acceptance evidence and update the manifest in a follow-up governance-only commit.
4. Run the Stable-claim gate. It accepts the later governance commit only when Git proves no undeclared source/product file changed after the reviewed implementation revision.

Any product change after step 2 requires fresh evidence for every affected platform.

## Exact-decision report

Each successful reusable-workflow run writes and uploads `glaze-ui-current-stable-gate-report.json`.

The report binds the validation result to both sides of the authorization decision and records:

- exact current consumer source revision,
- exact reviewed implementation revision for each accepted platform,
- files changed between review and the current governance revision,
- exact Glaze UI policy revision,
- current central Stable version,
- consumer target version,
- Stable-claim mode,
- platform coverage counts,
- accepted platform state,
- verified evidence paths and SHA-256 values,
- the authority boundary stating that overall product Stable/production eligibility remains independently governed.

The report is CI evidence for the exact workflow decision. It does not replace the underlying repository-local acceptance records.

## Release transition behavior

Glaze UI release promotion should update `VERSION`, lifecycle authority, consumer registry authority, and the fail-closed downstream template target atomically. Because downstream validation reads those central authorities at runtime, a newly promoted Stable release immediately becomes the required target for subsequent consumer gate runs.

Existing historical acceptance remains useful as migration provenance but does not satisfy a new current-Stable claim. Evidence from an older reviewed revision also cannot be replayed after product/source changes.

## No global visual pass

Glaze UI conformance is intentionally scoped by consumer and platform. The enforcement system must not collapse web, Android, desktop, TV, watch, tablet, foldable, or other surfaces into a single misleading global "uses Glaze UI" state.

Each consumer must prove the platforms it actually claims.
