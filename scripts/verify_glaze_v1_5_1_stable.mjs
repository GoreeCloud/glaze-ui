#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const read = rel => fs.readFileSync(path.join(root, rel), 'utf8');
const json = rel => JSON.parse(read(rel));
const assert = (condition, message) => { if (!condition) throw new Error(message); };

const reviewedImplementationAnchor = 'ee1032a0822ab8e103f8afe48e5c1859fde65cc9';
const qualifiedAnchor = '5b59d0e36950d737dba35b58ae58058684e0831b';
const qualificationIntegrationCommit = 'f7ef915f0aabea6cf92748018f2220a99e3a9c92';
const rcIntegrationCommit = 'a9c93506dd062d29c6c894940b71d060e8c39110';

assert(read('VERSION').trim() === '1.5.1', 'VERSION must identify GLAZE UI 1.5.1 Stable');

const lifecycle = json('registry/lifecycle.json');
assert(lifecycle.currentOfficial === '1.5.1', 'lifecycle currentOfficial must be 1.5.1');
assert(lifecycle.currentStable === '1.5.1', 'lifecycle currentStable must be 1.5.1');
assert(lifecycle.activeCandidate === null, 'Stable lifecycle must not retain an active Candidate');
assert(lifecycle.activePatchReleaseCandidate === null, 'Stable lifecycle must not retain an active patch RC');

const stable = lifecycle.releases.find(item => item.version === '1.5.1');
assert(stable, 'lifecycle must contain 1.5.1');
assert(stable.status === 'stable', '1.5.1 lifecycle status must be stable');
assert(stable.consumerEligible === true, '1.5.1 must be consumer eligible as a shared Stable release');
assert(stable.stableBaseline === '1.5.0', '1.5.1 Stable baseline must be 1.5.0');
assert(stable.contract === 'GLAZE_UI_V1_5.md', '1.5.1 must retain the V1.5 family contract');
assert(stable.qualification === 'contracts/v1.5.1/stable-scope.json', '1.5.1 qualification authority mismatch');
assert(stable.acceptance === 'acceptance/v1.5.1-stable.md', '1.5.1 acceptance authority mismatch');
assert(stable.runtimeEntrypoint === 'js/glaze-v1.5.1.mjs', '1.5.1 runtime entrypoint mismatch');
assert(stable.sourceQualificationAnchor === qualifiedAnchor, '1.5.1 qualification anchor mismatch');

const priorStable = lifecycle.releases.find(item => item.version === '1.5.0');
assert(priorStable?.status === 'stable', '1.5.0 must remain retained Stable rollback provenance');
assert(priorStable?.consumerEligible === true, '1.5.0 historical Stable record must remain consumer-eligible history');
assert(priorStable?.sourceQualificationAnchor === reviewedImplementationAnchor, '1.5.0 reviewed implementation anchor drift');

const rc = lifecycle.releases.find(item => item.version === '1.5.1-rc.1');
assert(rc?.status === 'superseded-release-candidate', '1.5.1-rc.1 must be retained as superseded Release Candidate history');
assert(rc?.consumerEligible === false, 'historical RC must remain non-consumer-eligible');
assert(rc?.sourceQualificationAnchor === qualifiedAnchor, 'historical RC qualification anchor drift');

const scope = json('contracts/v1.5.1/stable-scope.json');
assert(scope.version === '1.5.1', 'Stable scope version mismatch');
assert(scope.releaseLifecycle === 'Stable', 'Stable scope lifecycle mismatch');
assert(scope.stableBaseline === '1.5.0', 'Stable scope rollback baseline mismatch');
assert(scope.consumerEligible === true, 'Stable scope consumer eligibility mismatch');
assert(scope.reviewedImplementationAnchor === reviewedImplementationAnchor, 'Stable scope reviewed implementation anchor mismatch');
assert(scope.sourceQualificationAnchor === qualifiedAnchor, 'Stable scope qualification anchor mismatch');
assert(scope.qualificationIntegrationCommit === qualificationIntegrationCommit, 'Stable scope qualification integration mismatch');
assert(scope.releaseCandidateIntegrationCommit === rcIntegrationCommit, 'Stable scope RC integration mismatch');
assert(scope.runtimeEntrypoint === 'js/glaze-v1.5.1.mjs', 'Stable scope runtime mismatch');
assert(scope.qualification?.inheritedV150ObligationCount === 16, 'Stable scope must retain 16 inherited V1.5.0 obligations');
assert(scope.qualification?.v151AcceptedObligationCount === 2, 'Stable scope must contain two accepted V1.5.1 obligations');
assert(scope.qualification?.totalAcceptedObligationCount === 18, 'Stable scope must contain 18 total accepted obligations');
const accepted = scope.qualification?.v151AcceptedObligations;
assert(Array.isArray(accepted) && accepted.length === 2, 'Stable scope must enumerate exactly two V1.5.1 obligations');
for (const id of ['performance-representative-budget', 'platform-posture-continuity']) {
  const item = accepted.find(entry => entry.id === id);
  assert(item?.status === 'accepted', `${id} must be accepted in Stable scope`);
  assert(item?.boundRevision === qualifiedAnchor, `${id} exact revision mismatch`);
}
assert(accepted.find(item => item.id === 'performance-representative-budget')?.reviewRecord === 'PR #230 comment 5697516074', 'Performance review provenance mismatch');
const posture = accepted.find(item => item.id === 'platform-posture-continuity');
assert(posture?.reviewRecord === 'PR #230 comment 5705230782', 'Posture review provenance mismatch');
assert(posture?.approvalReference === 'GCU-ADR-GLAZE-V151-POSTURE-TR-001', 'Posture target-runtime approval mismatch');
assert(scope.continuity?.qualifiedV151SourceChangedByStablePromotion === false, 'Stable promotion must not claim qualified source change');
assert(scope.continuity?.v150PresentationBehaviorChanged === false, 'Stable promotion must not change reviewed V1.5 presentation behavior');
assert(scope.continuity?.authorizationBehaviorChanged === false, 'Stable promotion must not change authorization behavior');
assert(scope.continuity?.qualificationEvidenceReboundToStableRevision === false, 'Qualification evidence must remain bound to its real source revision');
assert(scope.stableClaims?.downstreamConsumerAcceptanceAutomatic === false, 'Stable must not auto-accept downstream consumers');
assert(scope.stableClaims?.tagPublicationAutomatic === false, 'Stable must not auto-publish a tag');
assert(scope.stableClaims?.githubReleasePublicationAutomatic === false, 'Stable must not auto-publish a GitHub Release');
assert(scope.stableClaims?.deploymentAcceptanceAutomatic === false, 'Stable must not auto-accept deployment');
assert(scope.stableClaims?.productionAcceptanceAutomatic === false, 'Stable must not auto-accept production');

const consumers = json('consumers/registry.json');
assert(consumers.officialBaseline === '1.5.1', 'Consumer registry officialBaseline must be 1.5.1');
assert(consumers.requiredConsumerVersion === '1.5.1', 'Consumer registry requiredConsumerVersion must be 1.5.1');
assert(consumers.consumers.every(item => item.requiredTargetVersion === '1.5.1'), 'Every consumer must require current Stable 1.5.1');
assert(consumers.consumers.every(item => item.productionEligible === false), 'Shared Stable promotion must not make any consumer production eligible');

const acceptance = read('acceptance/v1.5.1-stable.md');
for (const token of [reviewedImplementationAnchor, qualifiedAnchor, qualificationIntegrationCommit, rcIntegrationCommit, '5697516074', '5705230782', 'GCU-ADR-GLAZE-V151-POSTURE-TR-001']) {
  assert(acceptance.includes(token), `Stable acceptance missing provenance ${token}`);
}
assert(acceptance.includes('does not establish an immutable `v1.5.1` tag'), 'Stable acceptance must preserve publication boundary');

const hardening = read('GLAZE_UI_V1_5_1_HARDENING.md');
assert(hardening.includes('**Lifecycle:** Stable qualification record'), 'V1.5.1 hardening record must reflect Stable qualification state');
assert(hardening.includes(qualifiedAnchor), 'V1.5.1 hardening record must preserve qualification anchor');
assert(hardening.includes('5697516074') && hardening.includes('5705230782'), 'V1.5.1 hardening record must preserve review provenance');

const readme = read('README.md');
assert(readme.includes('Machine version: **1.5.1**'), 'README must identify 1.5.1');
assert(readme.includes('js/glaze-v1.5.1.mjs'), 'README must identify current Stable runtime');
assert(readme.includes('1.5.0') && readme.includes('rollback'), 'README must preserve 1.5.0 rollback boundary');

const stability = read('STABILITY.md');
assert(stability.includes('`1.5.1`'), 'STABILITY.md must identify current Stable 1.5.1');
assert(stability.includes('`1.5.0`'), 'STABILITY.md must identify 1.5.0 rollback baseline');

const conformance = read('CONFORMANCE.md');
assert(conformance.includes('`1.5.1`'), 'CONFORMANCE.md must identify current 1.5.1 target');
assert(conformance.includes('eighteen') || conformance.includes('18'), 'CONFORMANCE.md must identify complete shared qualification count');

const consumersGuide = read('CONSUMERS.md');
assert(consumersGuide.includes('(`1.5.1`)'), 'CONSUMERS.md must identify current 1.5.1 target');
assert(consumersGuide.includes('Fresh repository-local V1.5 adoption and acceptance evidence is required'), 'CONSUMERS.md must preserve repository-local acceptance boundary');

const runtimeModule = await import(pathToFileURL(path.join(root, 'js/glaze-v1.5.1.mjs')).href);
assert(runtimeModule.glazeV151?.version === '1.5.1', 'Stable runtime metadata version mismatch');
assert(runtimeModule.glazeV151?.lifecycle === 'stable', 'Stable runtime metadata lifecycle mismatch');
assert(runtimeModule.glazeV151?.stableBaseline === '1.5.0', 'Stable runtime metadata rollback mismatch');
assert(runtimeModule.glazeV151?.qualifiedStabilizationObligations === 18, 'Stable runtime qualification count mismatch');
assert(runtimeModule.glazeV151?.authorizationInferred === false, 'Stable runtime must not infer authorization');
assert(runtimeModule.glazeV151?.permissionRequestAutomatic === false, 'Stable runtime must not automatically request permission');
assert(runtimeModule.glazeV151?.automaticNavigationAllowed === false, 'Stable runtime must not automatically navigate');
assert(runtimeModule.glazeV151?.consequentialExecutionAutomatic === false, 'Stable runtime must not automatically execute consequential actions');
assert(runtimeModule.glazeV151?.fallbackExecutionAutomatic === false, 'Stable runtime must not automatically execute fallbacks');
assert(runtimeModule.glazeV151?.downstreamConsumerAcceptanceAutomatic === false, 'Stable runtime must not auto-accept consumers');

const resolved = runtimeModule.resolveGlazeInterface({});
assert(resolved && typeof resolved === 'object', 'Stable runtime must resolve a Glaze interface');
if (Object.prototype.hasOwnProperty.call(resolved, 'version')) {
  assert(resolved.version === '1.5.1', 'Resolved Stable interface must expose 1.5.1 identity');
}
if (Object.prototype.hasOwnProperty.call(resolved, 'lifecycle')) {
  assert(resolved.lifecycle === 'stable', 'Resolved Stable interface must remain Stable');
}

console.log('GLAZE UI V1.5.1 Stable authority verification: PASS');
console.log(`Reviewed V1.5 implementation anchor: ${reviewedImplementationAnchor}`);
console.log(`V1.5.1 qualification anchor: ${qualifiedAnchor}`);
console.log('Accepted shared qualification obligations: 18');
console.log('Immediate rollback baseline: 1.5.0');
console.log('Downstream consumer acceptance automatic: false');
console.log('Tag/GitHub Release publication automatic: false');
