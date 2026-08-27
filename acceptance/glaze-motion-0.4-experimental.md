# Glaze Motion 0.4 Experimental Acceptance Record

This record describes development evidence for Motion Core 0.4.0. It is not Stable or Candidate release evidence and does not certify downstream GoreeCloud applications.

## Scope

0.4 retains the 0.3 direct-manipulation, semantic gesture, shared-transition, native-mapping, local performance, and reference-consumer foundation. It adds an aggregate Motion Core entry point, accessible reorder command/result semantics, a bounded local settling-animation budget, and an expanded rendered web/reference matrix.

## Required source evidence

- machine-readable 0.4 Experimental contract;
- compatibility-preserving 0.4 aggregate entry point over the retained 0.3 primitive module;
- accessible reorder controller with directional plus Home/End commands and localization-neutral position metadata;
- local-only settling budget that rejects optional settling under reduced motion or saturation without blocking semantic state updates;
- runtime, interaction, accessibility, and reference-consumer tests;
- local-only frame-budget evidence with no network reporting;
- native semantic mapping guidance;
- rendered Mobile, Desktop, and TV reference acceptance in normal and reduced-motion modes.

## Rendered boundary

The TV rendered profile validates web/reference behavior at a TV-sized viewport plus directional input semantics exercised by the runtime. It is not native TV, remote-hardware, or real-device certification.

## Consumer boundary

The canonical Glaze UI consumer registry currently marks listed downstream consumers as migration-required to Glaze UI 1.5 Stable. Motion Core 0.4 therefore does not introduce a mandatory Experimental dependency into those applications. The reference consumers validate the design-system contract until a downstream application first satisfies its Stable baseline and separately opts into Experimental evaluation.

## Promotion boundary

Motion Core remains Experimental. Motion Studio and Motion Spatial remain Planned. Candidate promotion still requires representative conformant downstream consumer evidence, native/real-device evidence as applicable, accessibility acceptance, performance evidence, compatibility/migration review, dependency/security/licensing review, and normal Glaze UI lifecycle governance.
