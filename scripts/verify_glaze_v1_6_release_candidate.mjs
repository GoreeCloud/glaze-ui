#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=rel=>fs.readFileSync(path.join(root,rel),'utf8');
const json=rel=>JSON.parse(read(rel));
const assert=(value,message)=>{if(!value)throw new Error(message);};

const SOURCE='c7509c79256b04b0aa67cb9dd0737d7588e0ae4a';
const QUALIFICATION_INTEGRATION='354f5759385c28596fcfec26a3ad525e89fb1c35';
const RC='1.6.0-rc.1';
const STABLE='1.5.1';

assert(read('VERSION').trim()===STABLE,'VERSION must remain current Stable 1.5.1 during V1.6 RC');

const lifecycle=json('registry/lifecycle.json');
assert(lifecycle.currentOfficial===STABLE&&lifecycle.currentStable===STABLE,'current Official/Stable must remain 1.5.1');
assert(lifecycle.activeCandidate===RC,'activeCandidate must be 1.6.0-rc.1');
assert(lifecycle.plannedNext===null,'plannedNext must remain null unless separately governed');
assert(lifecycle.activePatchReleaseCandidate===null,'no patch RC may be active during V1.6 major RC');

const release=lifecycle.releases.find(item=>item.version===RC);
assert(release,'lifecycle must register 1.6.0-rc.1');
assert(release.internal_version===RC&&release.external_version===RC,'RC internal/external versions must both be 1.6.0-rc.1');
assert(release.version_name===null,'RC version name must remain unassigned');
assert(release.status==='release-candidate','V1.6 lifecycle entry must be Release Candidate');
assert(release.consumerEligible===false,'V1.6 RC must remain non-consumer-eligible');
assert(release.stableBaseline===STABLE,'V1.6 RC Stable baseline must remain 1.5.1');
assert(release.sourceQualificationAnchor===SOURCE,'V1.6 RC qualification anchor mismatch');
assert(release.qualificationEvidenceIntegrationCommit===QUALIFICATION_INTEGRATION,'V1.6 RC qualification integration mismatch');
assert(release.contract==='contracts/v1.6/release-candidate.json','V1.6 RC contract reference mismatch');
assert(release.qualification==='acceptance/v1.6-qualification-review.json','V1.6 RC review reference mismatch');
assert(release.acceptance==='acceptance/v1.6-rc.1.json','V1.6 RC acceptance reference mismatch');
assert(release.runtimeEntrypoint==='js/glaze-v1.6.0-rc.1.mjs','V1.6 RC runtime reference mismatch');

const review=json('acceptance/v1.6-qualification-review.json');
assert(review.recordId==='goreecloud.glaze-ui.v1.6.qualification-review','qualification review recordId mismatch');
assert(review.sourceQualificationAnchor===SOURCE,'qualification review source mismatch');
assert(review.acceptanceModelVersion==='1.6.0-dev.12','qualification review acceptance model mismatch');
assert(review.qualificationEvidenceIntegrationCommit===QUALIFICATION_INTEGRATION,'qualification review integration mismatch');
assert(review.evidenceMatrix?.laneCount===24,'qualification review lane count mismatch');
assert(review.evidenceMatrix?.verifiedCount===24&&review.evidenceMatrix?.unverifiedCount===0&&review.evidenceMatrix?.notApplicableCount===0,'qualification review disposition must be 24/0/0');
assert(review.evidenceMatrix?.qualificationEvidenceComplete===true&&review.evidenceMatrix?.readyForGovernedQualificationReview===true,'qualification review must originate from complete review-ready evidence');
assert(Array.isArray(review.evidenceMatrix?.blockingLaneIds)&&review.evidenceMatrix.blockingLaneIds.length===0,'qualification review must have no blocking lanes');
assert(review.releaseCandidateTarget?.internal_version===RC&&review.releaseCandidateTarget?.external_version===RC,'qualification review RC version identity mismatch');
assert(review.releaseCandidateTarget?.version_name===null,'qualification review version name must be null');
assert(review.decision==='approved-for-release-candidate','governed qualification review must approve RC');
assert(review.authority?.releaseCandidateApproved===true,'qualification review must explicitly approve RC');
assert(review.authority?.stableStatusGranted===false,'qualification review must not grant Stable');

const contract=json('contracts/v1.6/release-candidate.json');
assert(contract.version===RC,'RC contract version mismatch');
assert(contract.internal_version===RC&&contract.external_version===RC,'RC contract internal/external version mismatch');
assert(contract.version_name===null,'RC contract version name must be null');
assert(contract.releaseLifecycle==='Release Candidate','RC contract lifecycle mismatch');
assert(contract.consumerEligible===false,'RC contract consumer boundary mismatch');
assert(contract.sourceQualificationAnchor===SOURCE,'RC contract source anchor mismatch');
assert(contract.qualificationEvidenceIntegrationCommit===QUALIFICATION_INTEGRATION,'RC contract qualification integration mismatch');
assert(contract.qualification?.laneCount===24&&contract.qualification?.verifiedCount===24&&contract.qualification?.unverifiedCount===0&&contract.qualification?.notApplicableCount===0,'RC contract must carry 24/0/0 evidence disposition');
assert(contract.qualification?.evidenceComplete===true,'RC contract qualification must be complete');
assert(contract.continuity?.qualifiedSourceMayChangeDuringRcIdentityPromotion===false,'RC promotion must not change qualified source');
assert(contract.continuity?.qualificationEvidenceReboundToRcRevision===false,'RC must not rebind qualification evidence');
assert(contract.authority?.currentOfficialRemains===STABLE&&contract.authority?.currentStableRemains===STABLE,'RC contract must preserve 1.5.1 Stable authority');
for(const key of ['downstreamConsumerAcceptanceAutomatic','deploymentAcceptanceAutomatic','productionAcceptanceAutomatic','tagPublicationAutomatic','githubReleasePublicationAutomatic']){
  assert(contract.authority?.[key]===false,'RC contract authority boundary must remain false: '+key);
}

const acceptance=json('acceptance/v1.6-rc.1.json');
assert(acceptance.version===RC&&acceptance.internal_version===RC&&acceptance.external_version===RC,'RC acceptance version identity mismatch');
assert(acceptance.version_name===null,'RC acceptance version name must be null');
assert(acceptance.releaseLifecycle==='Release Candidate','RC acceptance lifecycle mismatch');
assert(acceptance.sourceQualificationAnchor===SOURCE,'RC acceptance source mismatch');
assert(acceptance.qualificationEvidenceIntegrationCommit===QUALIFICATION_INTEGRATION,'RC acceptance qualification integration mismatch');
assert(acceptance.qualificationDisposition?.verifiedCount===24&&acceptance.qualificationDisposition?.unverifiedCount===0&&acceptance.qualificationDisposition?.notApplicableCount===0,'RC acceptance must record 24/0/0');
assert(acceptance.qualificationDisposition?.qualificationEvidenceComplete===true,'RC acceptance must record evidence complete');
assert(Array.isArray(acceptance.qualificationDisposition?.blockingLaneIds)&&acceptance.qualificationDisposition.blockingLaneIds.length===0,'RC acceptance must have no blockers');
assert(acceptance.decision==='accepted-release-candidate','RC acceptance decision mismatch');
assert(acceptance.consumerEligible===false,'RC acceptance must remain non-consumer-eligible');
assert(acceptance.authority?.releaseCandidateStatusGranted===true&&acceptance.authority?.stableStatusGranted===false,'RC acceptance lifecycle authority mismatch');

const runtime=read('js/glaze-v1.6.0-rc.1.mjs');
for(const token of [
  "export * from './glaze-v1.6-development.mjs'",
  "version: '1.6.0-rc.1'",
  "internalVersion: '1.6.0-rc.1'",
  "externalVersion: '1.6.0-rc.1'",
  "versionName: null",
  "lifecycle: 'release-candidate'",
  "stableBaseline: '1.5.1'",
  SOURCE,
  QUALIFICATION_INTEGRATION,
  'qualificationEvidenceComplete: true',
  'verifiedQualificationLanes: 24',
  'consumerEligible: false',
  'stablePromotionAutomatic: false'
]) assert(runtime.includes(token),'RC runtime identity wrapper missing token: '+token);
assert(!/resolveGlaze[A-Za-z0-9_]*\s*\(/.test(runtime),'RC identity wrapper must not add resolver behavior');

const consumers=json('consumers/registry.json');
assert(consumers.officialBaseline===STABLE&&consumers.requiredConsumerVersion===STABLE,'consumer registry must remain on Stable 1.5.1');
assert(consumers.consumers.every(item=>item.requiredTargetVersion===STABLE),'every downstream consumer must continue targeting Stable 1.5.1');
assert(consumers.consumers.every(item=>item.productionEligible===false),'V1.6 RC must not make downstream consumers production eligible');

const reconcile=spawnSync(process.execPath,[
  path.join(root,'scripts/evaluate_glaze_v1_6_qualification_evidence.mjs'),
  '--external','acceptance/v1.6-human-evidence.json',
  '--external','acceptance/v1.6-assistive-technology-evidence.json',
  '--external','acceptance/v1.6-performance-evidence.json',
  '--require-complete','--compact'
],{cwd:root,encoding:'utf8',stdio:['ignore','pipe','pipe']});
assert(reconcile.status===0,'complete V1.6 evidence reconciliation failed\n'+(reconcile.stderr||reconcile.stdout));
const result=JSON.parse(reconcile.stdout);
assert(result.matrix.verifiedCount===24&&result.matrix.unverifiedCount===0&&result.matrix.notApplicableCount===0,'governed reconciler must return 24/0/0');
assert(result.matrix.qualificationEvidenceComplete===true&&result.matrix.readyForGovernedQualificationReview===true,'governed reconciler must remain complete and review-ready');
assert(result.matrix.blockingLaneIds.length===0,'governed reconciler must have no blockers');
assert(result.authority.lifecyclePromotionAutomatic===false&&result.authority.stableStatusGranted===false,'evidence reconciliation must remain non-promoting');

const sourcePaths=[
  'GLAZE_UI_V1_6_PLANNED.md',
  'js/glaze-v1.6-development.mjs',
  'js/glaze-v1.6-loading.dev.mjs',
  'js/glaze-v1.6-state-accessibility.dev.mjs',
  'js/glaze-v1.6-focus-motion.dev.mjs',
  'js/glaze-v1.6-material-type-input.dev.mjs',
  'js/glaze-v1.6-resilience-feedback.dev.mjs',
  'js/glaze-v1.6-navigation-status.dev.mjs',
  'js/glaze-v1.6-component-systems.dev.mjs',
  'js/glaze-v1.6-experience-governance.dev.mjs',
  'js/glaze-v1.6-performance-diagnostics.dev.mjs',
  'js/glaze-v1.6-conformance-adoption.dev.mjs',
  'js/glaze-v1.6-acceptance.dev.mjs',
  'contracts/v1.6/loading-skeleton.dev.json',
  'contracts/v1.6/state-accessibility.dev.json',
  'contracts/v1.6/focus-motion.dev.json',
  'contracts/v1.6/material-type-input.dev.json',
  'contracts/v1.6/resilience-feedback.dev.json',
  'contracts/v1.6/navigation-status.dev.json',
  'contracts/v1.6/component-systems.dev.json',
  'contracts/v1.6/experience-governance.dev.json',
  'contracts/v1.6/performance-diagnostics.dev.json',
  'contracts/v1.6/conformance-adoption.dev.json',
  'contracts/v1.6/acceptance.dev.json'
];
const continuity=spawnSync('git',['diff','--quiet',SOURCE,'--',...sourcePaths],{cwd:root,encoding:'utf8'});
assert(continuity.status===0,'qualified V1.6 behavior/contract source changed after frozen qualification anchor');

console.log('GLAZE UI V1.6.0-rc.1 Release Candidate verification: PASS');
console.log('Internal version: '+RC);
console.log('External version: '+RC);
console.log('Version name: none');
console.log('Frozen qualification source: '+SOURCE);
console.log('Qualification evidence integration: '+QUALIFICATION_INTEGRATION);
console.log('Qualification evidence: 24 verified / 0 unverified / 0 not applicable');
console.log('Current Official Stable preserved: '+STABLE);
console.log('Consumer eligible: false');
console.log('Stable promotion automatic: false');
