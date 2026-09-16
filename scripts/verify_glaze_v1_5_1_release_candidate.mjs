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

assert(read('VERSION').trim() === '1.5.0', 'Current Official Stable VERSION must remain 1.5.0 during RC');

const lifecycle = json('registry/lifecycle.json');
assert(lifecycle.currentOfficial === '1.5.0', 'currentOfficial must remain 1.5.0 during RC');
assert(lifecycle.currentStable === '1.5.0', 'currentStable must remain 1.5.0 during RC');
assert(lifecycle.activePatchReleaseCandidate === '1.5.1-rc.1', 'activePatchReleaseCandidate must be 1.5.1-rc.1');
assert(lifecycle.plannedNext === '1.5.1', 'plannedNext must remain 1.5.1');

const candidate = lifecycle.releases.find(item => item.version === '1.5.1-rc.1');
assert(candidate, 'Lifecycle must contain 1.5.1-rc.1');
assert(candidate.status === 'release-candidate', '1.5.1-rc.1 must be release-candidate');
assert(candidate.consumerEligible === false, 'RC must not be consumer eligible');
assert(candidate.stableBaseline === '1.5.0', 'RC Stable baseline must be 1.5.0');
assert(candidate.sourceQualificationAnchor === qualifiedAnchor, 'RC qualification anchor mismatch');
assert(candidate.sourceIntegrationAnchor === integrationCommit, 'RC integration anchor mismatch');
assert(candidate.runtimeEntrypoint === 'js/glaze-v1.5.1-rc.1.mjs', 'RC runtime entrypoint mismatch');

const contract = json('contracts/v1.5.1/release-candidate.json');
assert(contract.version === '1.5.1-rc.1', 'RC contract version mismatch');
assert(contract.releaseLifecycle === 'Release Candidate', 'RC contract lifecycle mismatch');
assert(contract.consumerEligible === false, 'RC contract consumer boundary mismatch');
assert(contract.sourceQualificationAnchor === qualifiedAnchor, 'RC contract qualification anchor mismatch');
assert(contract.qualificationIntegrationCommit === integrationCommit, 'RC contract integration commit mismatch');
assert(contract.externalQualification.performanceRepresentativeBudget.status === 'accepted', 'Performance qualification must be accepted');
assert(contract.externalQualification.platformPostureContinuity.status === 'accepted', 'Posture qualification must be accepted');
assert(contract.continuity.qualificationEvidenceReboundToRcRevision === false, 'Evidence must not be silently rebound');

const candidateRuntime = read('js/glaze-v1.5.1-rc.1.mjs');
assert(candidateRuntime.includes("export * from './glaze-v1.5.0.mjs'"), 'RC runtime must inherit V1.5.0 Stable runtime');
assert(candidateRuntime.includes("version: '1.5.1-rc.1'"), 'RC runtime version identity missing');
assert(candidateRuntime.includes("lifecycle: 'release-candidate'"), 'RC runtime lifecycle identity missing');
assert(candidateRuntime.includes(qualifiedAnchor), 'RC runtime qualification anchor missing');
assert(candidateRuntime.includes('stablePromotionAutomatic: false'), 'RC runtime must not auto-promote Stable');

const consumers = json('consumers/registry.json');
assert(consumers.officialBaseline === '1.5.0', 'Consumer official baseline must remain 1.5.0 during RC');
assert(consumers.requiredConsumerVersion === '1.5.0', 'Consumer required target must remain 1.5.0 during RC');
assert(consumers.consumers.every(item => item.productionEligible === false), 'RC must not auto-certify consumers');

const acceptance = read('acceptance/v1.5.1-rc.1.md');
assert(acceptance.includes(qualifiedAnchor), 'RC acceptance must name qualification anchor');
assert(acceptance.includes('5697516074'), 'RC acceptance must reference performance review record');
assert(acceptance.includes('5705230782'), 'RC acceptance must reference posture review record');
assert(acceptance.includes('GCU-ADR-GLAZE-V151-POSTURE-TR-001'), 'RC acceptance must preserve posture approval reference');

console.log('GLAZE UI V1.5.1-rc.1 Release Candidate authority verification: PASS');
console.log(`Qualified Development anchor: ${qualifiedAnchor}`);
console.log(`Qualification integration commit: ${integrationCommit}`);
console.log('Current Official Stable remains: 1.5.0');
console.log('Downstream consumer acceptance automatic: false');
