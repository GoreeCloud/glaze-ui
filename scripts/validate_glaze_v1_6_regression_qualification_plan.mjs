#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=rel=>fs.readFileSync(path.join(root,rel),'utf8');
const json=rel=>JSON.parse(read(rel));
const assert=(value,message)=>{if(!value)throw new Error(message);};
const sort=value=>[...value].sort();

const plan=json('contracts/v1.6/qualification.regression.plan.json');
const renderedPlan=json('contracts/v1.6/qualification.rendered.plan.json');
const renderedRecord=json('acceptance/v1.6-rendered-evidence.json');
const acceptance=json('contracts/v1.6/acceptance.dev.json');
const lifecycle=json('registry/lifecycle.json');

assert(read('VERSION').trim()==='1.5.1','Stable VERSION must remain 1.5.1');
assert(lifecycle.currentOfficial==='1.5.1'&&lifecycle.currentStable==='1.5.1','Stable lifecycle must remain 1.5.1');
assert(lifecycle.activeCandidate===null&&lifecycle.plannedNext===null&&lifecycle.activePatchReleaseCandidate===null,'regression qualification tooling must not promote lifecycle');

assert(plan.schemaVersion===1,'regression plan schema version drifted');
assert(plan.lifecycle==='DevelopmentQualification','regression plan lifecycle mismatch');
assert(plan.sourceRevision===renderedPlan.sourceRevision,'regression plan must target rendered plan frozen source');
assert(plan.sourceRevision===renderedRecord.sourceRevision,'regression plan must target durable rendered evidence source');
assert(plan.acceptanceModelVersion===renderedRecord.acceptanceModelVersion,'regression acceptance model mismatch');
assert(plan.stableBaseline==='1.5.1'&&plan.consumerEligible===false,'regression plan Stable/consumer boundary drifted');
assert(plan.laneId==='regression-testing','regression plan must target regression-testing lane');

assert(plan.baseline.runId===renderedRecord.qualificationRun.runId,'baseline run must match durable rendered record');
assert(plan.baseline.artifactId===renderedRecord.artifact.id,'baseline artifact ID must match durable rendered record');
assert(plan.baseline.artifactName===renderedRecord.artifact.name,'baseline artifact name must match durable rendered record');
assert(plan.baseline.artifactDigest===renderedRecord.artifact.digest,'baseline artifact digest must match durable rendered record');
assert(plan.baseline.sourceRevision===renderedRecord.sourceRevision,'baseline source revision mismatch');
assert(plan.baseline.record==='acceptance/v1.6-rendered-evidence.json','baseline record path drifted');

const renderedScenes=sort(renderedPlan.scenes.map(scene=>scene.id));
assert(JSON.stringify(sort(plan.sceneIds))===JSON.stringify(renderedScenes),'regression scene set must equal rendered qualification scene set');
assert(new Set(plan.sceneIds).size===9,'regression scene IDs must be unique');
assert(plan.comparison.kind==='screenshot-sha256-exact'&&plan.comparison.tolerance===0,'regression comparison must remain exact and zero-tolerance');
for(const key of ['allScenesRequired','baselineManifestRequired','freshManifestRequired','sourceRevisionMustMatch']){
  assert(plan.comparison[key]===true,'regression comparison requirement drifted: '+key);
}

assert(Array.isArray(acceptance.evidenceRequirements['regression-testing']),'acceptance contract missing regression-testing');
const regressionGroups=acceptance.evidenceRequirements['regression-testing'];
assert(JSON.stringify(regressionGroups)==='[["machine"],["rendered"]]','regression evidence groups drifted');

assert(plan.evidenceBoundary.renderedRegressionOnly===true,'regression rendered-only boundary missing');
for(const key of [
  'humanEvidenceClaimed','assistiveTechnologyEvidenceClaimed','physicalDeviceEvidenceClaimed',
  'nativePlatformEvidenceClaimed','representativePerformanceEvidenceClaimed','lifecyclePromotionAutomatic',
  'candidateStatusGranted','releaseCandidateStatusGranted','stableStatusGranted',
  'consumerAcceptanceAutomatic','deploymentAcceptanceAutomatic','productionAcceptanceAutomatic'
]) assert(plan.evidenceBoundary[key]===false,'regression authority boundary must remain false: '+key);

console.log('GLAZE UI V1.6 regression qualification plan: PASS');
console.log('Frozen source: '+plan.sourceRevision);
console.log('Baseline artifact: '+plan.baseline.artifactId);
console.log('Scenes: '+plan.sceneIds.length);
console.log('Stable baseline preserved: 1.5.1');
