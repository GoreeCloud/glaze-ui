# Glaze UI V1.4 Performance Qualification Candidate

**Status:** Development / qualification infrastructure only  
**Lifecycle effect:** None  
**Current Stable Glaze release:** V1.3 / `1.3.0`

Glaze UI V1.4 now has a bounded source contract for performance qualification evidence. The contract exists to make later performance acceptance reproducible and exact-revision-bound; it is not performance evidence by itself and it cannot promote V1.4.

## Qualification model

A performance record binds measurements to the exact Glaze source commit and source tree, a platform family, runtime, renderer, device class, canonical measurement time, individual metrics, owner-selected budgets, sample counts, evidence references, and a reviewer disposition.

The candidate contract deliberately does **not** define universal production thresholds. Performance budgets must be selected and justified by the owning qualification authority for the target runtime and device class. A metric is accepted only when its measured value is less than or equal to its explicitly recorded budget.

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

Performance qualification is blocked when source or tree revisions do not match the revision being qualified, any metric exceeds its recorded budget, measurement evidence is missing, review is not accepted, or the record is not explicitly marked passed. Contradictory metric `accepted` flags are rejected rather than trusted.

The evaluator always returns `acceptedForLifecycleGate: false`. Even a valid performance pass proves only that the submitted measurements satisfy the submitted budgets for the recorded environment. It does not prove human visual acceptance, accessibility, native parity, consumer adoption, production approval, or Stable lifecycle status.

## Stable boundary

This capability reduces one V1.4 release-readiness gap by making performance evidence machine-checkable. Stable qualification still requires real measurements from governed target environments, accepted budgets, retained artifacts, reviewer acceptance, and the other independent Glaze lifecycle gates.
