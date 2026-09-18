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
const EVIDENCE_INTEGRATION='354f5759385c28596fcfec26a3ad525e89fb1c35';
const RC='1.6.0-rc.1';
const STABLE='1.5.1';

const qualifiedPaths=[
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
  'contracts/v1.6/acceptance.dev.json'
];

function git(args){
  return spawnSync('git',args,{cwd:root,encoding:'utf8',stdio:['ignore','pipe','pipe']});
}

assert(read('VERSION').trim()===STABLE,'Current Stable VERSION must remain 1.5.1 during V1.6 RC review');

for(const revision of [SOURCE,EVIDENCE_INTEGRATION]){
  assert(git(['cat-file','-e',revision+'^{commit}']).status===0,'required V1.6 qualification revision is unavailable: '+revision);
  assert(git(['merge-base','--is-ancestor',revision,'HEAD']).status===0,'required V1.6 qualification revision is not an ancestor of RC head: '+revision);
}

assert(git(['diff','--quiet',SOURCE,'HEAD','--',...qualifiedPaths]).status===0,'V1.6 qualified implementation or section-98 acceptance contract changed after frozen qualification source');

const lifecycle=json('registry/lifecycle.json');
assert(lifecycle.currentOfficial===STABLE&&lifecycle.currentStable===STABLE,'V1.5.1 must remain current Official Stable');
assert(lifecycle.activeCandidate===RC,'V1.6.0-rc.1 must be the active candidate');
assert(lifecycle.activePatchReleaseCandidate===null,'V1.6 RC promotion must not create a patch RC');
const release=lifecycle.releases.find(x=>x.version===RC);
assert(release&&release.status==='release-candidate','Lifecycle must contain active V1.6.0-rc.1 Release Candidate');
assert(release.consumerEligible===false,'V1.6 RC must remain non-consumer-eligible');
assert(release.stableBaseline===STABLE,'V1.6 RC Stable baseline mismatch');
assert(release.sourceQualificationAnchor===SOURCE,'V1.6 RC qualification anchor mismatch');
assert(release.qualificationEvidenceIntegrationCommit===EVIDENCE_INTEGRATION,'V1.6 RC evidence integration anchor mismatch');
assert(release.contract==='contracts/v1.6/release-candidate.json','V1.6 RC contract path mismatch');
assert(release.acceptance==='acceptance/v1.6.0-rc.1.md','V1.6 RC acceptance path mismatch');
assert(release.runtimeEntrypoint==='js/glaze-v1.6.0-rc.1.mjs','V1.6 RC runtime path mismatch');

const contract=json('contracts/v1.6/release-candidate.json');
assert(contract.internalVersion===RC&&contract.externalVersion===RC,'V1.6 RC internal/external version identity mismatch');
assert(contract.releaseLifecycle==='Release Candidate','V1.6 RC lifecycle contract mismatch');
assert(contract.consumerEligible===false,'V1.6 RC contract must remain non-consumer-eligible');
assert(contract.sourceQualificationAnchor===SOURCE,'V1.6 RC contract qualification anchor mismatch');
assert(contract.qualificationEvidenceIntegrationCommit===EVIDENCE_INTEGRATION,'V1.6 RC contract evidence integration mismatch');
assert(contract.qualification.verifiedCount===24&&contract.qualification.unverifiedCount===0&&contract.qualification.notApplicableCount===0,'V1.6 RC contract must carry 24/0/0 qualification');
assert(contract.qualification.qualificationEvidenceComplete===true&&contract.qualification.readyForGovernedQualificationReview===true,'V1.6 RC contract qualification completion mismatch');
assert(contract.qualification.governedQualificationReviewDecision==='accepted-for-release-candidate','V1.6 RC governed review decision missing');
assert(contract.authority.currentOfficialRemains===STABLE&&contract.authority.currentStableRemains===STABLE,'V1.6 RC contract must preserve V1.5.1 Stable authority');
assert(contract.authority.releaseCandidateDoesNotEstablishStable===true,'V1.6 RC must not self-grant Stable');

const runtime=read('js/glaze-v1.6.0-rc.1.mjs');
assert(runtime.includes("export * from './glaze-v1.6-development.mjs'"),'V1.6 RC wrapper must inherit frozen-qualified Development aggregate');
assert(runtime.includes("internalVersion: '1.6.0-rc.1'"),'V1.6 RC internal version missing');
assert(runtime.includes("externalVersion: '1.6.0-rc.1'"),'V1.6 RC external version missing');
assert(runtime.includes("lifecycle: 'release-candidate'"),'V1.6 RC lifecycle identity missing');
assert(runtime.includes("stablePromotionAutomatic: false"),'V1.6 RC must not auto-promote Stable');
assert(!/resolveGlaze[A-Za-z0-9_]*\s*\(/.test(runtime),'V1.6 RC identity wrapper must not add qualified behavior');

const consumers=json('consumers/registry.json');
assert(consumers.officialBaseline===STABLE&&consumers.requiredConsumerVersion===STABLE,'Consumer baseline must remain V1.5.1 while V1.6 is RC');
assert(consumers.consumers.every(x=>x.productionEligible===false),'V1.6 RC promotion must not auto-certify consumers');

const evidence=spawnSync(process.execPath,[
  path.join(root,'scripts/evaluate_glaze_v1_6_qualification_evidence.mjs'),
  '--external','acceptance/v1.6-human-evidence.json',
  '--external','acceptance/v1.6-assistive-technology-evidence.json',
  '--external','acceptance/v1.6-performance-evidence.json',
  '--require-complete','--compact'
],{cwd:root,encoding:'utf8',stdio:['ignore','pipe','pipe']});
assert(evidence.status===0,'V1.6 complete qualification evidence failed governed reconciliation at RC head'+(evidence.stderr?'\n'+evidence.stderr.trim():''));
const result=JSON.parse(evidence.stdout);
assert(result.matrix.verifiedCount===24&&result.matrix.unverifiedCount===0&&result.matrix.notApplicableCount===0,'V1.6 RC reconciliation must remain 24/0/0');
assert(result.matrix.qualificationEvidenceComplete===true&&result.matrix.readyForGovernedQualificationReview===true,'V1.6 RC evidence must remain complete and review-ready');
assert(result.matrix.blockingLaneIds.length===0,'V1.6 RC evidence must have no qualification blockers');

const acceptance=read('acceptance/v1.6.0-rc.1.md');
assert(acceptance.includes('24 verified / 0 unverified / 0 not applicable'),'V1.6 RC acceptance must record complete qualification matrix');
assert(acceptance.includes(SOURCE),'V1.6 RC acceptance must name frozen qualification source');
assert(acceptance.includes(EVIDENCE_INTEGRATION),'V1.6 RC acceptance must name evidence integration commit');
assert(acceptance.includes('1.5.1'),'V1.6 RC acceptance must preserve Stable baseline');

console.log('GLAZE UI V1.6.0-rc.1 Release Candidate authority verification: PASS');
console.log('Frozen qualification source: '+SOURCE);
console.log('Qualification evidence integration: '+EVIDENCE_INTEGRATION);
console.log('Qualification matrix: 24 verified / 0 unverified / 0 not applicable');
console.log('Current Stable preserved: '+STABLE);
console.log('Consumer eligible: false');
