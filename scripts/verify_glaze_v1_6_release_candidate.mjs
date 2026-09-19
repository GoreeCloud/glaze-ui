#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';

const read = path => fs.readFileSync(new URL(`../${path}`, import.meta.url), 'utf8');
const json = path => JSON.parse(read(path));
const SOURCE='c7509c79256b04b0aa67cb9dd0737d7588e0ae4a';
const QI='354f5759385c28596fcfec26a3ad525e89fb1c35';

const lifecycle=json('registry/lifecycle.json');
assert.equal(read('VERSION').trim(), '1.6.0');
assert.equal(lifecycle.currentOfficial, '1.6.0');
assert.equal(lifecycle.currentStable, '1.6.0');
assert.equal(lifecycle.activeCandidate, null);

const rc=lifecycle.releases.find(item=>item.version==='1.6.0-rc.1');
assert.ok(rc);
assert.equal(rc.status,'superseded-release-candidate');
assert.equal(rc.consumerEligible,false);
assert.equal(rc.stableBaseline,'1.5.1');
assert.equal(rc.sourceQualificationAnchor,SOURCE);
assert.equal(rc.qualificationEvidenceIntegrationCommit,QI);
assert.equal(rc.contract,'contracts/v1.6/release-candidate.json');
assert.equal(rc.acceptance,'acceptance/v1.6-rc.1.json');
assert.equal(rc.runtimeEntrypoint,'js/glaze-v1.6.0-rc.1.mjs');

const review=json('acceptance/v1.6-qualification-review.json');
assert.equal(review.sourceQualificationAnchor,SOURCE);
assert.equal(review.qualificationEvidenceIntegrationCommit,QI);
assert.equal(review.evidenceMatrix.laneCount,24);
assert.equal(review.evidenceMatrix.verifiedCount,24);
assert.equal(review.evidenceMatrix.unverifiedCount,0);
assert.equal(review.evidenceMatrix.notApplicableCount,0);
assert.equal(review.decision,'approved-for-release-candidate');

const rcAcceptance=json('acceptance/v1.6-rc.1.json');
assert.equal(rcAcceptance.version,'1.6.0-rc.1');
const wrapper=read('js/glaze-v1.6.0-rc.1.mjs');
assert.ok(wrapper.includes("export * from './glaze-v1.6-development.mjs'"));
assert.ok(wrapper.includes("version: '1.6.0-rc.1'"));
assert.ok(wrapper.includes("lifecycle: 'release-candidate'"));

console.log('GLAZE UI V1.6.0-rc.1 retained historical integrity: PASS');
console.log('Current Stable is 1.6.0; RC remains non-consumer-eligible provenance.');
