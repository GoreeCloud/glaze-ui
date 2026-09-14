# Current Stable Consumer Gate — Acceptance Boundary

**Lifecycle:** Enforcement infrastructure  
**Central Stable authority:** `VERSION`, `registry/lifecycle.json`, `consumers/registry.json`  
**Product lifecycle authority:** Remains consumer-local and independent

## Machine-verifiable acceptance

The current-Stable consumer gate may be treated as structurally accepted when repository CI proves all of the following on the exact proposed Glaze UI source revision:

- the downstream validator compiles,
- the conformance schema and fail-closed template parse as JSON,
- schema vocabulary remains in parity with validator vocabulary,
- the fail-closed downstream template targets the current central Stable version,
- central Stable and consumer-registry authorities agree,
- stale Glaze targets are rejected,
- forced Stable claims against incomplete adoption are rejected,
- incomplete platform coverage is rejected for Stable claims,
- accepted platforms without repository-local evidence are rejected,
- unavailable or non-ancestor reviewed implementation revisions are rejected,
- mutated evidence hashes are rejected,
- post-review product/source changes are rejected while manifest/evidence-only governance transitions are permitted,
- Stable claims without an exact Glaze UI policy revision are rejected,
- duplicate platform declarations are rejected,
- manifest and evidence path traversal are rejected,
- repository-identity mismatches are rejected,
- the existing central consumer-registry validator continues to pass.

## Evidence continuity boundary

A platform's `sourceRevision` identifies the exact implementation commit that was reviewed. The evidence and manifest may be committed in a later revision because committing the evidence necessarily changes Git history.

The gate must prove that the reviewed revision is an ancestor of the current consumer revision and that every path changed after review is limited to the repository-local conformance manifest and evidence files explicitly declared by that manifest. Any undeclared source or product change invalidates continuity and requires fresh review evidence.

This rule prevents both circular exact-HEAD requirements and stale evidence replay.

## Non-claims

This acceptance boundary does not certify any downstream application as Glaze-conformant and does not promote any GoreeCloud application to Stable.

The reusable workflow is enforcement infrastructure only. Each consumer must still create its own repository-local manifest and evidence and pass the gate against its own exact reviewed implementation provenance. Each accepted platform evidence declaration must remain SHA-256-bound to its evidence file.

A successful current-Stable gate proves only the Glaze UI prerequisite represented by the gate. It does not replace consumer product, security, privacy, accessibility, native-platform, performance, rollback, release, or production acceptance.
