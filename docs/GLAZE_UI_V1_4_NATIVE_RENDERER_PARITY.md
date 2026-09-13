# Glaze UI V1.4 Native Renderer Parity Qualification

Glaze UI V1.4 remains a non-Stable candidate. Native renderer parity is a separate qualification gate and is not implied by web/runtime tests, token compatibility, accessibility checks, or performance evidence.

The V1.4 native-renderer parity evidence contract binds a review record to an exact candidate commit, exact source-tree revision, native platform/runtime/renderer environment, reference renderer, capture time, owner-defined comparison method, owner-defined acceptance criteria, and per-scene content-addressed reference/native evidence.

The evaluator deliberately does **not** define a universal pixel-difference threshold, perceptual score, device set, evidence lifetime, or target-specific pass criterion. Those authorities belong to the applicable Glaze qualification owner for the target platform and renderer. The caller must provide an explicit maximum evidence age when evaluating a record.

Evidence references use `evidence+sha256:<digest>:<locator>` so reviewed bytes cannot silently be replaced by a mutable artifact. Scene evidence alone is not sufficient to establish a review. The reviewer must also provide a distinct content-addressed authority-evidence reference, a separate content-addressed review-attestation reference, and a canonical `reviewedAt` timestamp. Review evidence cannot reuse scene evidence or the authority-evidence reference. The review timestamp cannot predate the governed capture and cannot be future-dated relative to evaluation.

For a record to qualify, every listed scene must have an accepted disposition, the overall reviewer must accept the record, the reviewer attestation must satisfy those provenance and timing rules, the record must be marked `passed`, exact source expectations must match, and the captured evidence must satisfy the caller-selected freshness ceiling.

These review fields prove only that the parity record carries immutable review provenance under the supplied qualification policy; they do not independently establish that the named human or organization is genuinely authorized. The applicable qualification owner remains responsible for the authority model and target-specific acceptance criteria.

Even a valid record can only set `acceptedForNativeRendererParityQualification` for the exact bound target evidence. `acceptedForLifecycleGate` is always false. Native renderer parity qualification cannot by itself make V1.4 Stable, consumer-eligible, production-approved, or accepted on another platform, renderer, device class, or source revision.
