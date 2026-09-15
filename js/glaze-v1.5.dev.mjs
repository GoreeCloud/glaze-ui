/* GLAZE UI 1.5.0-dev.1 — Contextual + Capability Awareness development entrypoint. */
export * from './glaze-v1.4.1.mjs';
export * from './glaze-v1.5-context-capability.dev.mjs';

export const glazeV15Development = Object.freeze({
  version: '1.5.0-dev.1',
  lifecycle: 'development',
  stableBaseline: '1.4.1',
  consumerEligible: false,
  authorityBoundary: 'presentation-only',
  stablePromotionAutomatic: false
});
