import assert from 'node:assert/strict';
import fs from 'node:fs';

const readJson = path => JSON.parse(fs.readFileSync(new URL(`../${path}`, import.meta.url), 'utf8'));

const lifecycle = readJson('registry/lifecycle.json');
const review = readJson('acceptance/v1.6-stable-qualification-review.json');
const rcReview = readJson('acceptance/v1.6-qualification-review.json');
const readiness = readJson('acceptance/v1.6-production-readiness-review.json');
const driveReconciliation = readJson('acceptance/v1.6-drive-document-reconciliation.json');

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
assert.equal(driveReconciliation.taskRecord?.sha256, '711bff33f5f3b479babe228efcde7571197cde82854105cc4f662ebe89074e0f');
assert.equal(driveReconciliation.taskRecord?.pageCount, 75);
assert.equal(driveReconciliation.taskRecord?.visualVerification?.allPagesReviewed, true);
assert.equal(driveReconciliation.changeLogRecord?.driveFileId, '1p1PTyUeQ2Ht4tzibAATmrEuVctyLs8up');
assert.equal(driveReconciliation.changeLogRecord?.sha256, '166ea03adcd4008d1327233fdac2b6df2922ec452e1a3baf49f493cd0039978b');
assert.equal(driveReconciliation.changeLogRecord?.pageCount, 235);
assert.equal(driveReconciliation.changeLogRecord?.visualVerification?.allPagesReviewed, true);

const requiredBlockers = [
  'repository.main-branch-protection',
  'security.secret-and-history-scan',
  'security.dependency-and-supply-chain-scan',
  'security.release-security-acceptance',
  'release.artifact-provenance-and-publication-boundary',
  'production-acceptance.applicability'
];
const blockers = new Map(review.blockers.map(item => [item.id, item]));
for (const id of requiredBlockers) {
  assert.ok(blockers.has(id), `Stable qualification blocker missing: ${id}`);
  assert.match(blockers.get(id).status, /^blocked/, `Stable blocker must remain fail-closed: ${id}`);
}

assert.equal(review.blockers.length, 6, 'V1.6 Stable review must retain the six unresolved blockers after Platform Contract and Drive reconciliation');
assert.ok(review.verifiedPasses.some(item => item.id === 'drive.documentation-and-task-reconciliation' && item.status === 'passed'), 'Drive reconciliation must be a verified pass');
assert.ok(review.verifiedPasses.some(item => item.id === 'platform-contract.current-machine-contract' && item.status === 'passed'), 'Platform Contract shared-library declaration must be a verified pass');
assert.equal(review.remainingBlockerCount, 6, 'remainingBlockerCount must be six');
assert.equal(review.decision, 'blocked-remain-release-candidate');
assert.equal(review.stablePromotionAuthorized, false);
assert.equal(review.productionReadinessGranted, false);
assert.equal(review.productionAcceptanceGranted, false);
assert.equal(review.consumerEligibilityGranted, false);
assert.equal(review.requiredLifecycleState, 'Release Candidate');

console.log('GLAZE UI V1.6 Stable qualification review: BLOCKED as governed.');
console.log('Current Stable remains 1.5.1; active candidate remains 1.6.0-rc.1.');
console.log(`Recorded blockers: ${review.blockers.length}; Stable promotion authorization: false.`);
