/*
 * GLAZE UI V1.4.0 — official Stable runtime entrypoint.
 *
 * The imported .candidate modules are promoted implementation sources whose
 * filenames/metadata preserve qualification provenance. Stable lifecycle and
 * consumer eligibility are established by this public facade plus VERSION,
 * GLAZE_UI_V1_4.md, and registry/lifecycle.json.
 */
export * from "./glaze-v1.3.0.mjs";
export * from "./glaze-v1.4-optical-runtime.candidate.mjs";
export * from "./glaze-v1.4-accessibility-runtime.candidate.mjs";
export * from "./glaze-v1.4-browser-capabilities.candidate.mjs";
export * from "./glaze-v1.4-optical-web.candidate.mjs";

export const glazeV14Stable = Object.freeze({
  version: '1.4.0',
  lifecycle: 'stable',
  official: true,
  consumerEligible: true,
  predecessor: '1.3.0',
  publicRuntimeEntrypoint: 'js/glaze-v1.4.0.mjs',
  publicWebEntrypoint: 'css/glaze-v1.4.0.css',
  humanQualificationDeferredTo: '1.4.1',
  deferredHumanEvidenceIsPassed: false,
  telemetryRequired: false,
  analyticsRequired: false
});
