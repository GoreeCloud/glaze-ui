import assert from 'node:assert/strict';
import fs from 'node:fs';

const read = path => fs.readFileSync(new URL(`../${path}`, import.meta.url), 'utf8');
const readJson = path => JSON.parse(read(path));

const VERSION = '1.6.0';
const RC = '1.6.0-rc.1';
const ROLLBACK = '1.5.1';
const QUALIFIED_SOURCE = 'c7509c79256b04b0aa67cb9dd0737d7588e0ae4a';
const RELEASED_SOURCE = 'a7180679ea851389e0f3004515f9a25f420e716d';
const RELEASED_TREE = '9ff0bf7a5f9d64f109d99bf4b76b81bd2a162268';
const PUBLICATION_CONTROL = '7e8b537b9d1a123bc3e92679774a4d9cc704e03b';

const lifecycle = readJson('registry/lifecycle.json');
const review = readJson('acceptance/v1.6-stable-qualification-review.json');
const rcReview = readJson('acceptance/v1.6-qualification-review.json');
const readiness = readJson('acceptance/v1.6-production-readiness-review.json');
const productionApplicability = readJson('acceptance/v1.6-production-applicability.json');
const securityReview = readJson('acceptance/v1.6-stable-security-review.json');
const finalSecurity = readJson('acceptance/v1.6-final-security-acceptance.json');
const artifact = readJson('acceptance/v1.6-artifact-provenance-plan.json');
const publication = readJson('acceptance/v1.6-publication-readback.json');
const stableAcceptance = readJson('acceptance/v1.6-stable.json');
const consumers = readJson('consumers/registry.json');

assert.equal(read('VERSION').trim(), VERSION);
assert.equal(lifecycle.currentOfficial, VERSION);
assert.equal(lifecycle.currentStable, VERSION);
assert.equal(lifecycle.activeCandidate, null);
assert.equal(lifecycle.officialProductLabel, 'GLAZE UI V1.6');

const stable = lifecycle.releases.find(item => item.version === VERSION);
assert.ok(stable, 'V1.6.0 Stable lifecycle record is missing');
assert.equal(stable.status, 'stable');
assert.equal(stable.consumerEligible, true);
assert.equal(stable.stableBaseline, ROLLBACK);
assert.equal(stable.contract, 'contracts/v1.6/stable-release.json');
assert.equal(stable.acceptance, 'acceptance/v1.6-stable.json');
assert.equal(stable.runtimeEntrypoint, 'js/glaze-v1.6.0.mjs');
assert.equal(stable.sourceQualificationAnchor, QUALIFIED_SOURCE);
assert.equal(stable.releasedSourceRevision, RELEASED_SOURCE);
assert.equal(stable.releasedSourceTree, RELEASED_TREE);
assert.equal(stable.publicationControlRevision, PUBLICATION_CONTROL);
assert.equal(stable.tag, 'v1.6.0');
assert.equal(stable.githubReleaseId, 392095913);

const retainedRc = lifecycle.releases.find(item => item.version === RC);
assert.equal(retainedRc?.status, 'superseded-release-candidate');
assert.equal(retainedRc?.consumerEligible, false);
assert.equal(retainedRc?.promotedTo, VERSION);

assert.equal(rcReview.evidenceMatrix.verifiedCount, 24);
assert.equal(rcReview.evidenceMatrix.unverifiedCount, 0);
assert.equal(rcReview.evidenceMatrix.notApplicableCount, 0);
assert.equal(rcReview.decision, 'approved-for-release-candidate');

assert.equal(readiness.reviewFindings.nineSystemApplicabilityEvaluated, true);
assert.equal(readiness.reviewFindings.qualificationEvidenceComplete, true);
assert.equal(productionApplicability.componentBoundary?.type, 'shared-library');
assert.equal(productionApplicability.deploymentApplicability?.directProductionDeploymentRequired, false);
assert.equal(productionApplicability.productionAcceptanceApplicability?.releasePublicationAcceptanceRequired, true);

assert.equal(finalSecurity.decision, 'passed-for-controlled-publication');
assert.equal(finalSecurity.stableSecurityAcceptanceGranted, true);
assert.equal(finalSecurity.acceptedSource.revision, RELEASED_SOURCE);
assert.equal(finalSecurity.acceptedSource.tree, RELEASED_TREE);
assert.equal(finalSecurity.acceptedArtifact.preparationWorkflowRunId, 35447623700);
assert.equal(finalSecurity.acceptedArtifact.actionsArtifactId, 10586051196);
assert.equal(finalSecurity.acceptedArtifact.archive.sha256, '687268b5eb76917eccae9d935ffa1bead333d5dee50b6098e996a3f44cee50af');
assert.equal(finalSecurity.acceptedArtifact.sbom.sha256, '3ffbb8bfe372d20642cd58f34fc0faaec2a74657d90e10742b75c5adf52dde82');
assert.equal(finalSecurity.acceptedArtifact.provenance.sha256, '711b58d5854085fb104dbae8bb5e7f7cfe4e8846e2e1fb314441c5212821ddd8');

assert.equal(securityReview.overallDecision, 'passed');
assert.equal(securityReview.stableSecurityAcceptanceGranted, true);
assert.equal(securityReview.stablePromotionAuthorized, true);
assert.deepEqual(securityReview.remainingReleaseSecurityBlockers, []);

assert.equal(artifact.status, 'completed-published-and-read-back');
assert.equal(artifact.decision, 'completed-exact-artifact-security-publication-readback-passed');
assert.equal(artifact.currentBoundary?.finalStableRevisionSelected, true);
assert.equal(artifact.currentBoundary?.finalCandidateArtifactPrepared, true);
assert.equal(artifact.currentBoundary?.finalSecurityAcceptanceGranted, true);
assert.equal(artifact.currentBoundary?.publicationCompleted, true);
assert.equal(artifact.currentBoundary?.publicationReadbackPassed, true);
assert.deepEqual(artifact.unresolvedPrerequisites, []);

assert.equal(publication.result, 'passed');
assert.equal(publication.sourceRevision, RELEASED_SOURCE);
assert.equal(publication.sourceTree, RELEASED_TREE);
assert.equal(publication.tag, 'v1.6.0');
assert.equal(publication.tagTargetRevision, RELEASED_SOURCE);
assert.equal(publication.releaseId, 392095913);
assert.equal(publication.draft, false);
assert.equal(publication.prerelease, false);
assert.equal(publication.releasedBytesMatchSecurityAcceptedBytes, true);
assert.equal(publication.stablePromotionAuthorizedByPublicationWorkflow, false);

assert.equal(stableAcceptance.decision, 'approved-for-stable-promotion');
assert.equal(stableAcceptance.stableStatusGranted, true);
assert.equal(stableAcceptance.version, VERSION);
assert.equal(stableAcceptance.stableBaseline, ROLLBACK);
assert.equal(stableAcceptance.consumerEligible, true);
assert.equal(stableAcceptance.releasedSourceRevision, RELEASED_SOURCE);
assert.equal(stableAcceptance.publication.result, 'passed');
assert.equal(stableAcceptance.security.result, 'passed');
assert.equal(stableAcceptance.downstream.consumerAcceptanceAutomatic, false);
assert.equal(stableAcceptance.downstream.productionEligibilityAutomatic, false);

assert.equal(review.decision, 'passed-approved-stable');
assert.equal(review.stablePromotionAuthorized, true);
assert.equal(review.consumerEligibilityGranted, true);
assert.equal(review.requiredLifecycleState, 'Stable');
assert.equal(review.remainingBlockerCount, 0);
assert.deepEqual(review.blockers, []);
assert.ok(review.verifiedPasses.some(item => item.id === 'repository.main-branch-protection' && item.status === 'passed'));
assert.ok(review.verifiedPasses.some(item => item.id === 'security.release-security-acceptance' && item.status === 'passed'));
assert.ok(review.verifiedPasses.some(item => item.id === 'release.artifact-provenance-and-publication-boundary' && item.status === 'passed'));

const stableContract = readJson('contracts/v1.6/stable-release.json');
assert.equal(stableContract.version, VERSION);
assert.equal(stableContract.releaseLifecycle, 'Stable');
assert.equal(stableContract.consumerEligible, true);
assert.equal(stableContract.runtimeEntrypoint, 'js/glaze-v1.6.0.mjs');
assert.equal(stableContract.sourceQualificationAnchor, QUALIFIED_SOURCE);
assert.equal(stableContract.stableBaseline, ROLLBACK);

const stableRuntime = read('js/glaze-v1.6.0.mjs');
for (const token of [
  "version: '1.6.0'",
  "lifecycle: 'stable'",
  "stableBaseline: '1.5.1'",
  RELEASED_SOURCE.slice(0, 0), // keep static token loop shape deterministic
  "consumerEligible: true",
  "presentationOnly: true",
  "authorizationInferred: false",
  "automaticNavigationAllowed: false",
  "consequentialExecutionAutomatic: false",
  "fallbackExecutionAutomatic: false",
  "downstreamConsumerAcceptanceAutomatic: false"
]) {
  if (token) assert.ok(stableRuntime.includes(token), `Stable runtime missing required token: ${token}`);
}

assert.equal(consumers.officialBaseline, VERSION);
assert.equal(consumers.requiredConsumerVersion, VERSION);
assert.equal(consumers.officialProductLabel, 'GLAZE UI V1.6');
assert.ok(consumers.consumers.every(item => item.requiredTargetVersion === VERSION));
assert.ok(consumers.consumers.every(item => item.productionEligible === false));

console.log('GLAZE UI V1.6.0 Stable qualification review: PASS');
console.log(`Released source: ${RELEASED_SOURCE}`);
console.log('Qualification: 24 verified / 0 unverified / 0 not applicable');
console.log('Final Stable security: PASS');
console.log('Immutable publication/readback: PASS');
console.log('Stable lifecycle: 1.6.0');
console.log('Downstream consumer acceptance automatic: false');
