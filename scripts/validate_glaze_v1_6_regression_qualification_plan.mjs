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
const capture=read('scripts/capture_glaze_v1_6_rendered_qualification.py');

assert(read('VERSION').trim()==='1.5.1','Stable VERSION must remain 1.5.1');
assert(lifecycle.currentOfficial==='1.5.1'&&lifecycle.currentStable==='1.5.1','Stable lifecycle must remain 1.5.1');
assert(lifecycle.activeCandidate===null&&lifecycle.plannedNext===null&&lifecycle.activePatchReleaseCandidate===null,'regression qualification tooling must not promote lifecycle');

assert(plan.schemaVersion===2,'regression plan schema version drifted');
assert(plan.lifecycle==='DevelopmentQualification','regression plan lifecycle mismatch');
assert(plan.sourceRevision===renderedPlan.sourceRevision,'regression plan must target rendered plan frozen source');
assert(plan.sourceRevision===renderedRecord.sourceRevision,'regression plan must target durable rendered evidence source');
assert(plan.acceptanceModelVersion===renderedRecord.acceptanceModelVersion,'regression acceptance model mismatch');
assert(plan.stableBaseline==='1.5.1'&&plan.consumerEligible===false,'regression Stable/consumer boundary drifted');
assert(plan.laneId==='regression-testing','regression plan must target regression-testing lane');

const prior=plan.priorRenderedEvidence;
assert(prior.runId===renderedRecord.qualificationRun.runId,'prior rendered run mismatch');
assert(prior.artifactId===renderedRecord.artifact.id,'prior rendered artifact ID mismatch');
assert(prior.artifactName===renderedRecord.artifact.name,'prior rendered artifact name mismatch');
assert(prior.artifactDigest===renderedRecord.artifact.digest,'prior rendered artifact digest mismatch');
assert(prior.sourceRevision===renderedRecord.sourceRevision,'prior rendered source revision mismatch');
assert(prior.record==='acceptance/v1.6-rendered-evidence.json','prior rendered record path drifted');
assert(prior.pixelBaselineClaimed===false,'prior rendered artifact must not be retroactively declared a pixel baseline');

const renderedScenes=sort(renderedPlan.scenes.map(scene=>scene.id));
assert(JSON.stringify(sort(plan.sceneIds))===JSON.stringify(renderedScenes),'regression scene set must equal rendered qualification scene set');
assert(new Set(plan.sceneIds).size===9,'regression scene IDs must be unique');
const comparison=plan.comparison;
assert(comparison.kind==='semantic-baseline-plus-double-render-sha256-exact','regression comparison kind drifted');
assert(comparison.pixelTolerance===0,'pixel comparison tolerance must remain zero');
for(const key of ['allScenesRequired','priorManifestRequired','sourceRevisionMustMatch','semanticEvidenceSha256MustMatchPrior','freshScreenshotSha256MustMatchEachOther']){
  assert(comparison[key]===true,'regression comparison requirement drifted: '+key);
}
assert(comparison.freshManifestCount===2,'regression qualification must require two fresh manifests');

assert(capture.includes("background-position:50% 0!important"),'capture must normalize skeleton background position before screenshot');
assert(capture.includes("line.style.backgroundPosition='50% 0'"),'capture must explicitly normalize skeleton inline background position');
assert(capture.includes(".glass{backdrop-filter:none!important;-webkit-backdrop-filter:none!important;background:var(--surface-solid)!important}"),'capture must normalize composited material after semantic measurement');

assert(Array.isArray(acceptance.evidenceRequirements['regression-testing']),'acceptance contract missing regression-testing');
assert(JSON.stringify(acceptance.evidenceRequirements['regression-testing'])==='[["machine"],["rendered"]]','regression evidence groups drifted');

assert(plan.evidenceBoundary.renderedRegressionOnly===true,'regression rendered-only boundary missing');
assert(plan.evidenceBoundary.priorArtifactReclassifiedAsPixelBaseline===false,'prior artifact must not be reclassified');
for(const key of [
  'humanEvidenceClaimed','assistiveTechnologyEvidenceClaimed','physicalDeviceEvidenceClaimed',
  'nativePlatformEvidenceClaimed','representativePerformanceEvidenceClaimed','lifecyclePromotionAutomatic',
  'candidateStatusGranted','releaseCandidateStatusGranted','stableStatusGranted',
  'consumerAcceptanceAutomatic','deploymentAcceptanceAutomatic','productionAcceptanceAutomatic'
]) assert(plan.evidenceBoundary[key]===false,'regression authority boundary must remain false: '+key);

console.log('GLAZE UI V1.6 regression qualification plan: PASS');
console.log('Frozen source: '+plan.sourceRevision);
console.log('Prior rendered evidence artifact: '+prior.artifactId);
console.log('Fresh normalized captures required: 2');
console.log('Pixel tolerance: 0');
console.log('Stable baseline preserved: 1.5.1');
