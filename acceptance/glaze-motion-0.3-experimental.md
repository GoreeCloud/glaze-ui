# Glaze Motion 0.3 Experimental Acceptance Record

This record describes development evidence for Motion Core 0.3.0. It is not Stable or Candidate release evidence and does not certify downstream GoreeCloud applications.

## Scope

0.3 extends the 0.2 direct-manipulation and shared-transition foundation with accessible semantic reorder/swipe/pan/zoom helpers, directional keyboard/remote mapping, local-only frame-budget instrumentation, native mapping guidance, and a representative reference-consumer harness.

## Required source evidence

- machine-readable 0.3 Experimental contract;
- dependency-free runtime with reorder, swipe, pan/zoom, directional mapping, and frame-budget primitives;
- runtime and interaction tests;
- reference-consumer tests that preserve state without View Transitions;
- local-only performance evidence with no network reporting;
- native semantic mapping guidance;
- retained 0.2 rendered Mobile/Desktop and reduced-motion acceptance.

## Consumer boundary

The canonical Glaze UI consumer registry currently marks listed downstream consumers as migration-required to Glaze UI 1.5 Stable. Motion Core 0.3 therefore does not introduce a mandatory Experimental dependency into those applications. The reference consumer exists to validate the design-system contract until a downstream application first satisfies its Stable baseline and separately opts into Experimental evaluation.

## Promotion boundary

Motion Core remains Experimental. Motion Studio and Motion Spatial remain Planned. Candidate promotion still requires representative conformant downstream consumer evidence, native/real-device evidence as applicable, accessibility acceptance, performance evidence, compatibility/migration review, and normal Glaze UI lifecycle governance.
