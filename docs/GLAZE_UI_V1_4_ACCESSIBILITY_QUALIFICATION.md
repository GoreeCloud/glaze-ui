# Glaze UI V1.4 Accessibility Qualification Candidate

**Status:** Development / qualification infrastructure only  
**Lifecycle effect:** None  
**Current Stable Glaze release:** V1.3 / `1.3.0`

Glaze UI V1.4 accessibility qualification is a bounded, exact-source evidence process. It does not make V1.4 Stable, does not replace human accessibility review, and does not turn automated feature detection or repository regressions into assistive-technology qualification.

## Evidence integrity

Any non-empty environment, preference, or scenario evidence reference used by the qualification record must be immutable and content-addressed as `evidence+sha256:<64-lowercase-hex-digest>:<locator>`. Mutable references such as `artifact:latest` are not accepted as qualification evidence.

A record represented as passed and human-accepted must also include a separate `reviewProvenance` object containing immutable `authorityEvidence`, distinct immutable `reviewEvidence`, and a timezone-qualified `reviewedAt` timestamp. The authority and review evidence references must be distinct from one another and from all environment, preference, and scenario evidence. Review time cannot precede `observedAt` and cannot be future-dated relative to evaluation.

This provenance binding does **not** prove that the named reviewer is genuinely authorized by GoreeCloud governance. Genuine reviewer authorization remains an external governance determination.

## Human-review boundary

Only `human` or `combined` review can support an accepted accessibility qualification record. Automated-only review cannot grant acceptance. A prepared or captured packet starts `in-progress`, human review remains `pending`, evaluator disposition remains `blocked`, and both accessibility and lifecycle acceptance remain false.

The local observation-capture path remains a manual capture aid. It does not auto-pass preference states or scenarios, does not auto-accept human review, and does not require telemetry, analytics, persistent storage, browser identity sniffing, or network access.

## Acceptance boundary

Accessibility qualification remains blocked when exact source identity is absent or mismatched, required scenarios are missing or not tested, required preference evidence is incomplete, content-addressed evidence is invalid, unresolved high/critical issues remain, human review is pending, accepted human-review provenance is missing or collides with qualification evidence, or review timing is invalid.

Even a valid accepted accessibility record always has `acceptedForLifecycleGate: false`. It establishes only the bounded accessibility qualification slice represented by its exact evidence. It does not establish a complete browser matrix, assistive-technology matrix, physical-device matrix, consumer conformance, production performance qualification, native-renderer parity, production approval, or Stable V1.4.

## Real evidence still required

The repository contains qualification contracts, evaluators, preparation tooling, capture aids, and regressions. Real acceptance still requires current target-specific observations, retained immutable evidence bytes, genuinely authorized human/combined review, representative assistive-technology/browser/device testing where applicable, and separate lifecycle/production approval.
