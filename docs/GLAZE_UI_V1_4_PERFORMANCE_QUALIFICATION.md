# Glaze UI V1.4 Performance Qualification Candidate

**Status:** Development / qualification infrastructure only  
**Lifecycle effect:** None  
**Current Stable Glaze release:** V1.3 / `1.3.0`

Glaze UI V1.4 now has a bounded source contract for performance qualification evidence. The contract exists to make later performance acceptance reproducible, exact-revision-bound, time-bounded, content-addressed, and review-provenance-bound; it is not performance evidence by itself and it cannot promote V1.4.

## Qualification model

A performance record binds measurements to the exact Glaze source commit and source tree, a platform family, runtime, renderer, device class, canonical measurement time, individual metrics, owner-selected budgets, sample counts, content-addressed measurement evidence references, and an attributable reviewer disposition.

The evaluator independently requires the caller to provide the exact expected source commit, exact expected source-tree revision, and a positive maximum measurement age. This prevents a record from self-asserting its own source binding or remaining acceptable indefinitely after the target environment has moved on.

Measurement evidence references must use the governed `evidence+sha256:<digest>:<locator>` form. Mutable names such as `artifact:latest` and malformed/non-SHA-256 references fail closed, preventing a later artifact from silently replacing the bytes that were measured for a performance qualification result.

Reviewer provenance uses the same immutable evidence form. The reviewer record must include content-addressed review authority evidence, separate content-addressed review attestation evidence, and a canonical `reviewedAt` timestamp. The review authority evidence and review attestation evidence must be distinct from one another and distinct from measurement evidence. Review cannot predate the measurements it accepts and cannot be future-dated relative to evaluation.

These reviewer-evidence bindings prove only which immutable authority/review artifacts were supplied to the qualification record. Repository validation does not prove that the named reviewer is genuinely authorized by GoreeCloud governance, and it does not create review authority. Real reviewer authority remains an independent governance fact that must be established by the applicable release process.

The candidate contract deliberately does **not** define universal production thresholds or a universal evidence lifetime. Performance budgets and the maximum acceptable measurement age must be selected and justified by the owning qualification authority for the target runtime and device class. A metric is accepted only when its measured value is less than or equal to its explicitly recorded budget.

The initial governed metric vocabulary is:

- startup time;
- runtime initialization time;
- stylesheet parse time;
- first interaction time;
- p95 interaction latency;
- p95 and p99 frame time; and
- peak memory usage.

Metric names are unique within one record. Units are bound to the metric definition, numeric values must be finite and non-negative, budgets must be positive, and sample counts are bounded.

## Fail-closed behavior

Performance qualification is blocked when the independently supplied source or tree expectations are missing, source or tree revisions do not match the revision being qualified, the caller does not supply a measurement-age policy, the measurements are older than that caller-selected maximum age, any metric exceeds its recorded budget, measurement evidence is missing, measurement references are not content-addressed, review is not accepted, or the record is not explicitly marked passed.

Malformed or mutable reviewer authority/review evidence is rejected. Reusing one reference for authority and review evidence, reusing measurement evidence as reviewer provenance, review before measurement, future-dated review, future-dated measurement, and contradictory metric `accepted` flags also fail closed rather than being trusted.

The evaluator always returns `acceptedForLifecycleGate: false`. Even a valid performance pass proves only that the submitted current measurements satisfy the submitted budgets for the recorded environment and that the record carries the required immutable review provenance. It does not prove human visual acceptance, accessibility, native parity, genuine reviewer authorization, consumer adoption, production approval, or Stable lifecycle status.

## Stable boundary

This capability reduces one V1.4 release-readiness gap by making performance evidence machine-checkable, freshness-bounded, content-addressed, and review-provenance-bound. Stable qualification still requires real current measurements from governed target environments, accepted budgets and freshness policy, retained measurement and review evidence bytes, genuine reviewer authority, reviewer acceptance, and the other independent Glaze lifecycle gates.
