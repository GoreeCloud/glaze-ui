import assert from 'node:assert/strict';
import fs from 'node:fs';

const readJson = path => JSON.parse(fs.readFileSync(new URL(`../${path}`, import.meta.url), 'utf8'));

const lifecycle = readJson('registry/lifecycle.json');
const review = readJson('acceptance/v1.6-stable-qualification-review.json');
const rcReview = readJson('acceptance/v1.6-qualification-review.json');
const readiness = readJson('acceptance/v1.6-production-readiness-review.json');
const driveReconciliation = readJson('acceptance/v1.6-drive-document-reconciliation.json');
const productionApplicability = readJson('acceptance/v1.6-production-applicability.json');
const artifactPlan = readJson('acceptance/v1.6-artifact-provenance-plan.json');
const finalArtifactAcceptance = readJson('acceptance/v1.6-final-artifact-acceptance.json');
const securityReview = readJson('acceptance/v1.6-stable-security-review.json');

assert.equal(fs.readFileSync(new URL('../VERSION', import.meta.url), 'utf8').trim(), '1.5.1');
assert.equal(lifecycle.currentStable, '1.5.1');
assert.equal(lifecycle.currentOfficial, '1.5.1');
assert.equal(lifecycle.activeCandidate, '1.6.0-rc.1');

const rc = lifecycle.releases.find(item => item.version === '1.6.0-rc.1');
assert.ok(rc, 'V1.6 Release Candidate lifecycle record is missing');
assert.equal(rc.status, 'release-candidate');
assert.equal(rc.consumerEligible, false);
assert.equal(rc.stableBaseline, '1.5.1');

assert.equal(review.recordId, 'goreecloud.glaze-ui.v1.6.stable-qualification-review');
assert.equal(review.reviewedReleaseCandidate, '1.6.0-rc.1');
assert.equal(review.source.qualificationSource, 'c7509c79256b04b0aa67cb9dd0737d7588e0ae4a');
assert.equal(review.source.qualificationEvidenceIntegrationCommit, '354f5759385c28596fcfec26a3ad525e89fb1c35');
assert.equal(review.source.releaseCandidateIntegrationCommit, '3f070f6fc01bc7904e3cd8c20851db5a0c40d539');
assert.equal(review.source.repositoryDocumentationReconciliationCommit, '294e721c6fc56afcde62f7fe70c96e9d711557b1');
assert.equal(review.governance.platformContract?.version, '0.4');
assert.match(review.governance.platformContract?.scope || '', /shared[- ]library/);

assert.equal(rcReview.evidenceMatrix.verifiedCount, 24);
assert.equal(rcReview.evidenceMatrix.unverifiedCount, 0);
assert.equal(rcReview.evidenceMatrix.notApplicableCount, 0);
assert.equal(rcReview.decision, 'approved-for-release-candidate');

assert.equal(readiness.reviewFindings.nineSystemApplicabilityEvaluated, true);
assert.equal(readiness.reviewFindings.qualificationEvidenceComplete, true);
assert.equal(readiness.reviewFindings.productionReadinessGranted, false);
assert.equal(readiness.reviewFindings.productionAcceptanceGranted, false);

assert.equal(driveReconciliation.decision, 'passed');
assert.equal(driveReconciliation.taskRecord?.driveFileId, '1sluzc6yiRlRlLf71JjFqUowM6ZC4amcy');
assert.equal(driveReconciliation.taskRecord?.sha256, '96a7edef2fad27336178f322b2942be7af477aaa717637226342094784522fbe');
assert.equal(driveReconciliation.taskRecord?.pageCount, 76);
assert.equal(driveReconciliation.taskRecord?.visualVerification?.allPagesReviewed, true);
assert.equal(driveReconciliation.changeLogRecord?.driveFileId, '1p1PTyUeQ2Ht4tzibAATmrEuVctyLs8up');
assert.equal(driveReconciliation.changeLogRecord?.sha256, '166ea03adcd4008d1327233fdac2b6df2922ec452e1a3baf49f493cd0039978b');
assert.equal(driveReconciliation.changeLogRecord?.pageCount, 235);
assert.equal(driveReconciliation.changeLogRecord?.visualVerification?.allPagesReviewed, true);

const requiredBlockers = [
  'release.artifact-provenance-and-publication-boundary',
];
const blockers = new Map(review.blockers.map(item => [item.id, item]));
for (const id of requiredBlockers) {
  assert.ok(blockers.has(id), `Stable qualification blocker missing: ${id}`);
  assert.match(blockers.get(id).status, /^blocked/, `Stable blocker must remain fail-closed: ${id}`);
}

assert.equal(review.blockers.length, 1, 'V1.6 Stable review must retain only the publication/readback blocker after final security acceptance');
assert.ok(review.verifiedPasses.some(item => item.id === 'drive.documentation-and-task-reconciliation' && item.status === 'passed'), 'Drive reconciliation must be a verified pass');
assert.ok(review.verifiedPasses.some(item => item.id === 'platform-contract.current-machine-contract' && item.status === 'passed'), 'Platform Contract shared-library declaration must be a verified pass');
assert.ok(review.verifiedPasses.some(item => item.id === 'security.secret-and-history-scan' && item.status === 'passed'), 'Secret/history security scan must be a verified pass');
assert.equal(productionApplicability.decision, 'deployment-not-applicable-publication-acceptance-required');
assert.equal(productionApplicability.componentBoundary?.type, 'shared-library');
assert.equal(productionApplicability.deploymentApplicability?.directProductionDeploymentRequired, false);
assert.equal(productionApplicability.deploymentApplicability?.result, 'not-applicable-justified');
assert.equal(productionApplicability.productionAcceptanceApplicability?.releasePublicationAcceptanceRequired, true);
assert.equal(productionApplicability.productionAcceptanceApplicability?.finalArtifactAcceptanceRequired, true);
assert.equal(productionApplicability.currentDisposition?.publicationAcceptanceCompleted, false);
assert.equal(productionApplicability.currentDisposition?.stablePromotionAuthorized, false);
assert.ok(review.verifiedPasses.some(item => item.id === 'production-acceptance.applicability' && item.status === 'passed-applicability-resolved'), 'Production applicability must be a verified resolved boundary');
assert.ok(review.verifiedPasses.some(item => item.id === 'security.dependency-and-supply-chain-scan' && item.status === 'passed'), 'Dependency and supply-chain scan must be a verified pass');
assert.ok(review.verifiedPasses.some(item => item.id === 'security.release-security-acceptance' && item.status === 'passed'), 'Final Stable security acceptance must be a verified pass');
assert.equal(review.source.finalArtifactCandidateSource, 'a7180679ea851389e0f3004515f9a25f420e716d');
assert.equal(review.source.finalArtifactCandidateTree, '9ff0bf7a5f9d64f109d99bf4b76b81bd2a162268');
assert.ok(review.verifiedPasses.some(item => item.id === 'repository.main-branch-protection' && item.status === 'passed'), 'Authoritative main branch protection must be a verified pass');
assert.equal(review.repositoryProtectionEvidence?.rulesetId, 23699829, 'Verified main ruleset ID mismatch');
assert.equal(review.repositoryProtectionEvidence?.enforcement, 'active', 'Verified main ruleset must be active');
assert.equal(review.repositoryProtectionEvidence?.branchProtected, true, 'Authoritative main must be protected');
assert.deepEqual(review.repositoryProtectionEvidence?.bypassActors, [], 'Verified main ruleset bypass list must be empty');
assert.equal(review.repositoryProtectionEvidence?.currentUserCanBypass, 'never', 'Verified main ruleset must not permit silent current-user bypass');
assert.equal(review.repositoryProtectionEvidence?.strictRequiredStatusChecksPolicy, true, 'Required checks must use strict/up-to-date enforcement');
assert.deepEqual(
  [...review.repositoryProtectionEvidence.requiredStatusChecks].sort(),
  ['platform-contract-0-4', 'stable-qualification-review', 'stable-security-evidence', 'validate-v1'].sort(),
  'Verified main required-check set mismatch'
);
assert.equal(artifactPlan.status, 'final-artifact-security-accepted-awaiting-publication');
assert.equal(artifactPlan.decision, 'final-security-accepted-prerelease-publication-authorized');
assert.equal(artifactPlan.currentBoundary?.stablePromotionAuthorized, false);
assert.equal(artifactPlan.currentBoundary?.finalStableRevisionSelected, true);
assert.equal(artifactPlan.currentBoundary?.finalCandidateArtifactPrepared, true);
assert.equal(artifactPlan.currentBoundary?.finalSecurityAcceptanceGranted, true);
assert.equal(artifactPlan.currentBoundary?.publicationAuthorized, true);
assert.equal(artifactPlan.currentBoundary?.authoritativeMainRevision, 'a7180679ea851389e0f3004515f9a25f420e716d');
assert.equal(artifactPlan.rehearsal?.publishesTag, false);
assert.equal(artifactPlan.rehearsal?.publishesGithubRelease, false);
assert.equal(artifactPlan.rehearsal?.grantsStable, false);
assert.equal(artifactPlan.targetStableVersion, '1.6.0');
assert.equal(artifactPlan.finalStablePreparation?.workflow, '.github/workflows/glaze-v1.6-final-artifact-preparation.yml');
assert.equal(artifactPlan.finalStablePreparation?.builder, 'scripts/build_glaze_v1_6_final_artifact.py');
assert.equal(artifactPlan.finalStablePreparation?.targetVersion, '1.6.0');
assert.equal(artifactPlan.finalStablePreparation?.intendedImmutableTag, 'v1.6.0');
assert.equal(artifactPlan.finalStablePreparation?.outputArchive, 'glaze-ui-v1.6.0-source-runtime.tar.gz');
assert.equal(artifactPlan.finalStablePreparation?.deterministicDoubleBuildRequired, true);
assert.equal(artifactPlan.finalStablePreparation?.extractedArtifactSecretScanRequired, true);
assert.equal(artifactPlan.finalStablePreparation?.publishesTag, false);
assert.equal(artifactPlan.finalStablePreparation?.publishesGithubRelease, false);
assert.equal(artifactPlan.finalStablePreparation?.grantsStable, false);
assert.equal(artifactPlan.finalStablePreparation?.status, 'passed-exact-main');
assert.equal(artifactPlan.finalStablePreparation?.selectedSourceRevision, 'a7180679ea851389e0f3004515f9a25f420e716d');
assert.equal(artifactPlan.finalStablePreparation?.selectedSourceTree, '9ff0bf7a5f9d64f109d99bf4b76b81bd2a162268');
assert.equal(artifactPlan.finalStablePreparation?.workflowRunId, 35447623700);
assert.equal(artifactPlan.finalStablePreparation?.actionsArtifactId, 10586051196);
assert.equal(artifactPlan.finalStablePreparation?.archiveSha256, '687268b5eb76917eccae9d935ffa1bead333d5dee50b6098e996a3f44cee50af');
assert.equal(artifactPlan.finalStablePreparation?.sbomSha256, '3ffbb8bfe372d20642cd58f34fc0faaec2a74657d90e10742b75c5adf52dde82');
assert.equal(artifactPlan.finalStablePreparation?.provenanceSha256, '711b58d5854085fb104dbae8bb5e7f7cfe4e8846e2e1fb314441c5212821ddd8');
const expectedFinalizationOrder = [
  'repository-protection',
  'exact-candidate-selection',
  'final-unpublished-artifact',
  'final-security-acceptance',
  'immutable-publication',
  'post-publication-readback',
  'exact-candidate-stable-qualification',
];
assert.deepEqual(
  artifactPlan.finalizationSequence?.map(item => item.id),
  expectedFinalizationOrder,
  'V1.6 finalization sequence must remain non-circular and fail-closed'
);
assert.equal(artifactPlan.finalizationSequence?.[0]?.status, 'passed');
assert.equal(artifactPlan.finalizationSequence?.[1]?.status, 'passed');
assert.equal(artifactPlan.finalizationSequence?.[2]?.status, 'passed');
assert.equal(artifactPlan.finalizationSequence?.[3]?.status, 'passed');
assert.equal(artifactPlan.finalizationSequence?.[4]?.status, 'authorized-pending');
assert.equal(artifactPlan.finalizationSequence?.[5]?.status, 'blocked-on-immutable-publication');
assert.equal(artifactPlan.finalizationSequence?.[6]?.status, 'blocked-on-post-publication-readback');
assert.equal(securityReview.overallDecision, 'passed');
assert.equal(securityReview.stableSecurityAcceptanceGranted, true);
assert.equal(securityReview.stablePromotionAuthorized, false);
assert.deepEqual(securityReview.remainingReleaseSecurityBlockers, []);
assert.equal(securityReview.finalSecurityAcceptance?.result, 'passed');
assert.equal(securityReview.finalSecurityAcceptance?.sourceRevision, 'a7180679ea851389e0f3004515f9a25f420e716d');
assert.equal(securityReview.finalSecurityAcceptance?.finalArtifactWorkflowRunId, 35447623700);
assert.equal(securityReview.finalSecurityAcceptance?.stableSecurityWorkflowRunId, 35447623641);
assert.equal(securityReview.finalSecurityAcceptance?.publicationAuthorized, true);
assert.equal(securityReview.finalSecurityAcceptanceBoundary?.requiresProtectedSource, true);
assert.equal(securityReview.finalSecurityAcceptanceBoundary?.requiresUnpublishedFinalCandidateArtifact, true);
assert.equal(securityReview.finalSecurityAcceptanceBoundary?.requiresArtifactChecksumSbomProvenance, true);
assert.equal(securityReview.finalSecurityAcceptanceBoundary?.requiresExtractedArtifactSecretScan, true);
assert.equal(securityReview.finalSecurityAcceptanceBoundary?.requiresPublishedTagOrRelease, false);
assert.equal(securityReview.finalSecurityAcceptanceBoundary?.publicationOccursAfterSecurityAcceptance, true);
assert.equal(securityReview.finalSecurityAcceptanceBoundary?.publicationMustReuseAcceptedArtifactBytes, true);
assert.equal(securityReview.finalSecurityAcceptanceBoundary?.targetStableVersion, '1.6.0');
assert.equal(securityReview.finalSecurityAcceptanceBoundary?.intendedImmutableTag, 'v1.6.0');
assert.equal(securityReview.finalSecurityAcceptanceBoundary?.acceptanceRecord, 'acceptance/v1.6-final-artifact-acceptance.json');
assert.equal(securityReview.finalSecurityAcceptanceBoundary?.acceptedSourceRevision, 'a7180679ea851389e0f3004515f9a25f420e716d');

assert.equal(finalArtifactAcceptance.decision, 'accepted-for-controlled-candidate-publication');
assert.equal(finalArtifactAcceptance.stableStatusGranted, false);
assert.equal(finalArtifactAcceptance.stablePromotionAuthorized, false);
assert.equal(finalArtifactAcceptance.publicationAuthorized, true);
assert.equal(finalArtifactAcceptance.publicationMustRemainPrereleaseUntilStablePromotion, true);
assert.equal(finalArtifactAcceptance.candidate?.sourceRevision, 'a7180679ea851389e0f3004515f9a25f420e716d');
assert.equal(finalArtifactAcceptance.candidate?.sourceTree, '9ff0bf7a5f9d64f109d99bf4b76b81bd2a162268');
assert.equal(finalArtifactAcceptance.candidate?.postMergeWorkflowCount, 31);
assert.equal(finalArtifactAcceptance.candidate?.postMergeWorkflowFailureCount, 0);
assert.equal(finalArtifactAcceptance.artifact?.workflowRunId, 35447623700);
assert.equal(finalArtifactAcceptance.artifact?.actionsArtifactId, 10586051196);
assert.equal(finalArtifactAcceptance.artifact?.archiveSha256, '687268b5eb76917eccae9d935ffa1bead333d5dee50b6098e996a3f44cee50af');
assert.equal(finalArtifactAcceptance.artifact?.sbomSha256, '3ffbb8bfe372d20642cd58f34fc0faaec2a74657d90e10742b75c5adf52dde82');
assert.equal(finalArtifactAcceptance.artifact?.provenanceSha256, '711b58d5854085fb104dbae8bb5e7f7cfe4e8846e2e1fb314441c5212821ddd8');
assert.equal(finalArtifactAcceptance.stableSecurityEvidence?.workflowRunId, 35447623641);
assert.equal(finalArtifactAcceptance.stableSecurityEvidence?.unreviewedSecretFindingCount, 0);
assert.equal(finalArtifactAcceptance.stableSecurityEvidence?.selectedAdvisoryCount, 0);
assert.equal(finalArtifactAcceptance.stableSecurityEvidence?.cyclonedxVulnerabilityCount, 0);
assert.equal(finalArtifactAcceptance.securityAcceptance?.finalStableSecurityAcceptanceGranted, true);
assert.equal(finalArtifactAcceptance.candidate?.postMergeWorkflowCountType, 'unique-workflow-names');
assert.equal(finalArtifactAcceptance.candidate?.postMergeRunRecordCountObservedAtAcceptance, 73);
assert.equal(finalArtifactAcceptance.stableSecurityControlMatrix?.standard, 'GoreeCloud — Standard — Stable Release Security Blockers');
assert.equal(finalArtifactAcceptance.stableSecurityControlMatrix?.version, 'v1.0');
assert.equal(finalArtifactAcceptance.stableSecurityControlMatrix?.evaluatedControlCount, 39);
assert.equal(finalArtifactAcceptance.stableSecurityControlMatrix?.passedOrBoundedPassedCount, 14);
assert.equal(finalArtifactAcceptance.stableSecurityControlMatrix?.notApplicableJustifiedCount, 25);
assert.equal(finalArtifactAcceptance.stableSecurityControlMatrix?.blockedCount, 0);
assert.equal(finalArtifactAcceptance.stableSecurityControlMatrix?.unknownCount, 0);
assert.equal(finalArtifactAcceptance.stableSecurityControlMatrix?.exceptedCount, 0);
assert.deepEqual(finalArtifactAcceptance.stableSecurityControlMatrix?.exceptions, []);
assert.equal(finalArtifactAcceptance.stableSecurityControlMatrix?.controls?.length, 39);
for (const control of finalArtifactAcceptance.stableSecurityControlMatrix.controls) {
  assert.ok(['passed', 'passed-bounded', 'not-applicable-justified'].includes(control.result), `invalid final security control disposition: ${control.id}`);
  assert.ok(typeof control.justification === 'string' && control.justification.length > 0, `missing final security control justification: ${control.id}`);
}
assert.equal(finalArtifactAcceptance.releaseSecurityAcceptanceRecord?.finalSecurityGateResult, 'passed');
assert.deepEqual(finalArtifactAcceptance.releaseSecurityAcceptanceRecord?.exceptions, []);
assert.equal(securityReview.controlApplicabilitySummary?.evaluatedControlCount, 39);
assert.equal(securityReview.controlApplicabilitySummary?.blockedCount, 0);
assert.equal(securityReview.controlApplicabilitySummary?.unknownCount, 0);
assert.equal(securityReview.controlApplicabilitySummary?.exceptedCount, 0);
assert.equal(securityReview.finalSecurityAcceptance?.controlApplicabilityMatrixAccepted, true);
assert.equal(blockers.get('release.artifact-provenance-and-publication-boundary')?.status, 'blocked-security-accepted-awaiting-publication-readback');
assert.equal(review.remainingBlockerCount, 1, 'remainingBlockerCount must be one');
assert.equal(review.decision, 'blocked-remain-release-candidate');
assert.equal(review.stablePromotionAuthorized, false);
assert.equal(review.productionReadinessGranted, false);
assert.equal(review.productionAcceptanceGranted, false);
assert.equal(review.consumerEligibilityGranted, false);
assert.equal(review.requiredLifecycleState, 'Release Candidate');

console.log('GLAZE UI V1.6 Stable qualification review: BLOCKED as governed.');
console.log('Current Stable remains 1.5.1; active candidate remains 1.6.0-rc.1.');
console.log(`Recorded blockers: ${review.blockers.length}; final security acceptance: passed; Stable promotion authorization: false.`);
