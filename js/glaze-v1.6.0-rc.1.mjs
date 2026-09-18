/* GLAZE UI V1.6.0-rc.1 — Release Candidate identity wrapper.
 *
 * Identity-only wrapper over the frozen-qualified V1.6 Development aggregate.
 * The qualified implementation remains bound to source
 * c7509c79256b04b0aa67cb9dd0737d7588e0ae4a.
 */

export * from './glaze-v1.6-development.mjs';

export const glazeV160ReleaseCandidate = Object.freeze({
  internalVersion: '1.6.0-rc.1',
  externalVersion: '1.6.0-rc.1',
  lifecycle: 'release-candidate',
  stableBaseline: '1.5.1',
  sourceQualificationAnchor: 'c7509c79256b04b0aa67cb9dd0737d7588e0ae4a',
  qualificationEvidenceIntegrationCommit: '354f5759385c28596fcfec26a3ad525e89fb1c35',
  consumerEligible: false,
  qualificationEvidenceComplete: true,
  readyForGovernedQualificationReview: true,
  stablePromotionAutomatic: false,
  consumerAcceptanceAutomatic: false,
  deploymentAcceptanceAutomatic: false,
  productionAcceptanceAutomatic: false
});
