#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const read = rel => fs.readFileSync(path.join(root, rel), 'utf8');
const json = rel => JSON.parse(read(rel));
const assert = (condition, message) => { if (!condition) throw new Error(message); };

const qualifiedAnchor = '5b59d0e36950d737dba35b58ae58058684e0831b';
const integrationCommit = 'f7ef915f0aabea6cf92748018f2220a99e3a9c92';
const version = read('VERSION').trim();
const lifecycle = json('registry/lifecycle.json');

const candidate = lifecycle.releases.find(item => item.version === '1.5.1-rc.1');
assert(candidate, 'Lifecycle must retain 1.5.1-rc.1 history');
assert(candidate.consumerEligible === false, 'RC must remain non-consumer-eligible');
assert(candidate.stableBaseline === '1.5.0', 'RC Stable baseline must remain 1.5.0');
assert(candidate.sourceQualificationAnchor === qualifiedAnchor, 'RC qualification anchor mismatch');
assert(candidate.sourceIntegrationAnchor === integrationCommit, 'RC qualification integration anchor mismatch');
assert(candidate.runtimeEntrypoint === 'js/glaze-v1.5.1-rc.1.mjs', 'RC runtime entrypoint mismatch');

if (version === '1.5.0') {
  assert(lifecycle.currentOfficial === '1.5.0', 'currentOfficial must remain 1.5.0 while RC is active');
  assert(lifecycle.currentStable === '1.5.0', 'currentStable must remain 1.5.0 while RC is active');
  assert(lifecycle.activePatchReleaseCandidate === '1.5.1-rc.1', 'activePatchReleaseCandidate must be 1.5.1-rc.1 while RC is active');
  assert(candidate.status === 'release-candidate', 'Active 1.5.1-rc.1 must be release-candidate');
} else {
  const tuple = version.split('.').slice(0, 3).map(Number);
  assert(tuple.length === 3 && tuple.every(Number.isInteger), 'Current Stable must use major.minor.patch versioning');
  assert(
    tuple[0] > 1 || (tuple[0] === 1 && (tuple[1] > 5 || (tuple[1] === 5 && tuple[2] >= 1))),
    `Unsupported lifecycle state for retained V1.5.1 RC verification: ${version}`
  );
  assert(lifecycle.currentOfficial === version, 'currentOfficial must match VERSION after V1.5.1 Stable promotion');
  assert(lifecycle.currentStable === version, 'currentStable must match VERSION after V1.5.1 Stable promotion');
  const liveRelease = lifecycle.releases.find(item => item.version === version);
  assert(liveRelease && liveRelease.status === 'stable' && liveRelease.consumerEligible === true, 'current lifecycle release must remain consumer-eligible Stable');
  assert(lifecycle.activePatchReleaseCandidate === null, 'No V1.5.1 patch RC may remain active after Stable promotion');
  assert(candidate.status === 'superseded-release-candidate', '1.5.1-rc.1 must remain superseded Release Candidate history after Stable promotion');
}

const contract = json('contracts/v1.5.1/release-candidate.json');
assert(contract.version === '1.5.1-rc.1', 'RC contract version mismatch');
assert(contract.releaseLifecycle === 'Release Candidate', 'RC contract lifecycle mismatch');
assert(contract.consumerEligible === false, 'RC contract consumer boundary mismatch');
assert(contract.sourceQualificationAnchor === qualifiedAnchor, 'RC contract qualification anchor mismatch');
assert(contract.qualificationIntegrationCommit === integrationCommit, 'RC contract integration commit mismatch');
assert(contract.externalQualification.performanceRepresentativeBudget.status === 'accepted', 'Performance qualification must remain accepted in RC provenance');
assert(contract.externalQualification.platformPostureContinuity.status === 'accepted', 'Posture qualification must remain accepted in RC provenance');
assert(contract.continuity.qualificationEvidenceReboundToRcRevision === false, 'RC evidence must not be silently rebound');

const candidateRuntime = read('js/glaze-v1.5.1-rc.1.mjs');
assert(candidateRuntime.includes("export * from './glaze-v1.5.0.mjs'"), 'RC runtime must inherit V1.5.0 Stable runtime');
assert(candidateRuntime.includes("version: '1.5.1-rc.1'"), 'RC runtime version identity missing');
assert(candidateRuntime.includes("lifecycle: 'release-candidate'"), 'RC runtime lifecycle identity missing');
assert(candidateRuntime.includes(qualifiedAnchor), 'RC runtime qualification anchor missing');
assert(candidateRuntime.includes('stablePromotionAutomatic: false'), 'RC runtime must not auto-promote Stable');

const consumers = json('consumers/registry.json');
assert(consumers.consumers.every(item => item.productionEligible === false), 'RC or shared Stable promotion must not auto-certify consumers');
if (version === '1.5.0') {
  assert(consumers.officialBaseline === '1.5.0', 'Consumer official baseline must remain 1.5.0 while RC is active');
  assert(consumers.requiredConsumerVersion === '1.5.0', 'Consumer required target must remain 1.5.0 while RC is active');
} else {
  assert(consumers.officialBaseline === version, 'Consumer official baseline must match the governed current Stable');
  assert(consumers.requiredConsumerVersion === version, 'Consumer required target must match the governed current Stable');
}

const acceptance = read('acceptance/v1.5.1-rc.1.md');
assert(acceptance.includes(qualifiedAnchor), 'RC acceptance must name qualification anchor');
assert(acceptance.includes('5697516074'), 'RC acceptance must preserve performance review record');
assert(acceptance.includes('5705230782'), 'RC acceptance must preserve posture review record');
assert(acceptance.includes('GCU-ADR-GLAZE-V151-POSTURE-TR-001'), 'RC acceptance must preserve posture approval reference');

console.log(version === '1.5.0'
  ? 'GLAZE UI V1.5.1-rc.1 active Release Candidate authority verification: PASS'
  : 'GLAZE UI V1.5.1-rc.1 historical Release Candidate integrity verification: PASS');
console.log(`Qualified Development anchor: ${qualifiedAnchor}`);
console.log(`Qualification integration commit: ${integrationCommit}`);
console.log('Downstream consumer acceptance automatic: false');
