#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createGlazeV16AcceptanceMatrix} from '../js/glaze-v1.6-acceptance.dev.mjs';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=rel=>fs.readFileSync(path.join(root,rel),'utf8');
const json=rel=>JSON.parse(read(rel));
const assert=(value,message)=>{if(!value)throw new Error(message);};
const sort=value=>[...value].sort();

const record=json('acceptance/v1.6-regression-evidence.json');
const machine=json('acceptance/v1.6-machine-evidence.json');
const rendered=json('acceptance/v1.6-rendered-evidence.json');
const plan=json('contracts/v1.6/qualification.regression.plan.json');
const lifecycle=json('registry/lifecycle.json');
const acceptance=read('acceptance/v1.6-development.md');

assert(read('VERSION').trim()==='1.5.1','Stable VERSION must remain 1.5.1');
assert(lifecycle.currentOfficial==='1.5.1'&&lifecycle.currentStable==='1.5.1','Stable lifecycle must remain 1.5.1');
assert(lifecycle.activeCandidate===null&&lifecycle.plannedNext===null&&lifecycle.activePatchReleaseCandidate===null,'regression evidence must not promote lifecycle');

assert(record.schemaVersion===1,'regression evidence schema version drifted');
assert(record.lifecycle==='DevelopmentQualification','regression evidence lifecycle mismatch');
assert(record.sourceRevision===plan.sourceRevision,'regression evidence source must match regression plan');
assert(record.sourceRevision===machine.sourceRevision&&record.sourceRevision===rendered.sourceRevision,'all V1.6 evidence must bind same frozen source');
assert(record.acceptanceModelVersion===machine.acceptanceModelVersion&&record.acceptanceModelVersion===rendered.acceptanceModelVersion,'acceptance model version mismatch');
assert(record.stableBaseline==='1.5.1','regression Stable baseline mismatch');

assert(record.tooling.pullRequest===258,'regression tooling PR mismatch');
assert(record.tooling.toolingHeadRevision==='fe471447d37ea800d03be438e1126f0840f89000','regression tooling head mismatch');
assert(record.tooling.mergeRevision==='b1f8575d6ed9199a7eb130f919680376c2e74d14','regression tooling merge mismatch');
assert(record.qualificationRun.runId===35352215130,'regression run mismatch');
assert(record.qualificationRun.verificationJobId===105622807547,'regression verification job mismatch');
assert(record.qualificationRun.comparisonJobId===105622931820,'regression comparison job mismatch');
assert(record.qualificationRun.conclusion==='success','regression run must be successful');
assert(record.qualificationRun.observedAt==='2026-09-18T13:47:36Z','regression observation timestamp drifted');

assert(record.artifact.id===10550685472,'regression artifact ID mismatch');
assert(record.artifact.name==='glaze-v1.6-rendered-regression-35352215130','regression artifact name mismatch');
assert(record.artifact.sizeBytes===3808954,'regression artifact size mismatch');
assert(record.artifact.digest==='sha256:5c4058fba12969fe1c95c523f5f9cd4fc1fb846cc2b3aaab4b2ba84c9034839d','regression artifact digest mismatch');
assert(record.artifact.createdAt==='2026-09-18T13:47:36Z','regression artifact creation timestamp mismatch');
assert(record.artifact.expiresAt==='2026-12-17T13:46:44Z','regression artifact expiry mismatch');
assert(record.artifact.sceneCount===9&&record.artifact.expiredAtObservation===false,'regression artifact state mismatch');
assert(Date.parse(record.artifact.expiresAt)>Date.parse(record.qualificationRun.observedAt),'regression artifact expiry must be after observation');

assert(record.priorRenderedEvidence.runId===rendered.qualificationRun.runId,'prior rendered run mismatch');
assert(record.priorRenderedEvidence.artifactId===rendered.artifact.id,'prior rendered artifact mismatch');
assert(record.priorRenderedEvidence.artifactDigest===rendered.artifact.digest,'prior rendered digest mismatch');
assert(record.priorRenderedEvidence.pixelBaselineClaimed===false,'prior artifact must not be retroactively declared a pixel baseline');

assert(record.comparison.kind===plan.comparison.kind,'comparison kind must match plan');
assert(record.comparison.semanticBaselineMatched===true&&record.comparison.freshVisualRepeatabilityMatched===true,'regression comparison must have passed');
assert(record.comparison.pixelTolerance===0,'regression pixel tolerance must remain zero');
assert(record.comparison.semanticMismatches.length===0&&record.comparison.freshVisualMismatches.length===0,'regression mismatch arrays must remain empty');

const expectedSceneIds=sort(plan.sceneIds);
const actualSceneIds=sort(record.baselineScenes.map(item=>item.id));
assert(JSON.stringify(actualSceneIds)===JSON.stringify(expectedSceneIds),'regression baseline scene set mismatch');
assert(new Set(actualSceneIds).size===9,'regression baseline scene IDs must be unique');
for(const item of record.baselineScenes){
  for(const key of ['evidenceSha256','pixelSha256','screenshotSha256']) assert(/^[0-9a-f]{64}$/.test(item[key]),'invalid scene hash: '+item.id+' '+key);
}

assert(record.renderedEvidence.length===1,'regression record must contain one rendered evidence item');
const evidence=record.renderedEvidence[0];
assert(evidence.id==='regression-testing'&&evidence.verified===true&&evidence.revision===record.sourceRevision&&evidence.evidenceType==='rendered','regression evidence item mismatch');
const expectedReference='GitHub Actions run 35352215130 / comparison job 105622931820 / artifact 10550685472 / sha256:5c4058fba12969fe1c95c523f5f9cd4fc1fb846cc2b3aaab4b2ba84c9034839d';
assert(evidence.reference===expectedReference,'regression evidence reference mismatch');

const matrix=createGlazeV16AcceptanceMatrix({
  exactRevision:record.sourceRevision,
  evidence:[...machine.machineEvidence,...rendered.renderedEvidence,...record.renderedEvidence]
});
const disposition=record.matrixDisposition;
assert(matrix.verifiedCount===17&&matrix.unverifiedCount===7&&matrix.notApplicableCount===0,'expected 17 verified / 7 unverified / 0 N/A after regression evidence');
assert(matrix.qualificationEvidenceComplete===false&&matrix.readyForGovernedQualificationReview===false,'regression evidence must not complete qualification');
assert(JSON.stringify(sort(disposition.fullyVerifiedLaneIds))===JSON.stringify(sort(matrix.lanes.filter(l=>l.status==='verified').map(l=>l.id))),'fully verified lane disposition mismatch');
assert(JSON.stringify(sort(disposition.partialLaneIds))===JSON.stringify(sort(matrix.lanes.filter(l=>l.status==='unverified'&&l.evidenceGroups.some(g=>g.satisfied)).map(l=>l.id))),'partial lane disposition mismatch');
assert(JSON.stringify(sort(disposition.untouchedLaneIds))===JSON.stringify(sort(matrix.lanes.filter(l=>l.status==='unverified'&&!l.evidenceGroups.some(g=>g.satisfied)).map(l=>l.id))),'untouched lane disposition mismatch');
assert(disposition.verifiedCount===17&&disposition.unverifiedCount===7&&disposition.notApplicableCount===0,'recorded matrix counts mismatch');
assert(disposition.qualificationEvidenceComplete===false&&disposition.readyForGovernedQualificationReview===false,'recorded qualification disposition must remain incomplete');

assert(record.authority.renderedRegressionEvidenceClaimed===true&&record.authority.regressionBaselineClaimed===true,'bounded regression evidence must be claimed');
for(const key of ['humanEvidenceClaimed','assistiveTechnologyEvidenceClaimed','deviceEvidenceClaimed','nativePlatformEvidenceClaimed','performanceEvidenceClaimed','candidateStatusGranted','releaseCandidateStatusGranted','stableStatusGranted','consumerAcceptanceAutomatic','deploymentAcceptanceAutomatic','productionAcceptanceAutomatic']) assert(record.authority[key]===false,'authority boundary must remain false: '+key);

for(const fragment of ['**17 fully verified lanes.**','**7 lanes remain unverified overall.**','Regression testing | **Verified — machine + rendered regression**']){
  assert(acceptance.includes(fragment),'acceptance matrix documentation missing: '+fragment);
}
console.log('GLAZE UI V1.6 regression evidence record: PASS');
console.log('Frozen source: '+record.sourceRevision);
console.log('Regression artifact: '+record.artifact.id);
console.log('Matrix: 17 verified / 7 unverified');
console.log('Stable baseline preserved: 1.5.1');
