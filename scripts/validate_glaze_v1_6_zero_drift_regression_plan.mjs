#!/usr/bin/env node
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

import {createGlazeV16AcceptanceMatrix} from '../js/glaze-v1.6-acceptance.dev.mjs';

const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const json=async rel=>JSON.parse(await readFile(path.join(ROOT,rel),'utf8'));
const text=rel=>readFile(path.join(ROOT,rel),'utf8');
const sorted=values=>[...values].sort();

const SOURCE='c7509c79256b04b0aa67cb9dd0737d7588e0ae4a';

async function main(){
  const [plan,schema,renderPlan,machine,rendered,lifecycle,version]=await Promise.all([
    json('contracts/v1.6/regression.rendered.plan.json'),
    json('schemas/v1.6-rendered-regression-plan.schema.json'),
    json('contracts/v1.6/qualification.rendered.plan.json'),
    json('acceptance/v1.6-machine-evidence.json'),
    json('acceptance/v1.6-rendered-evidence.json'),
    json('registry/lifecycle.json'),
    text('VERSION')
  ]);

  assert.equal(plan.schemaVersion,1);
  assert.equal(plan.lifecycle,'DevelopmentQualification');
  assert.equal(plan.sourceRevision,SOURCE);
  assert.equal(plan.acceptanceModelVersion,'1.6.0-dev.12');
  assert.equal(plan.stableBaseline,'1.5.1');
  assert.equal(plan.specificationSection,83);
  assert.equal(plan.acceptanceLaneId,'regression-testing');
  assert.equal(plan.renderedQualificationPlan,'contracts/v1.6/qualification.rendered.plan.json');
  assert.equal(plan.captureScript,'scripts/capture_glaze_v1_6_rendered_qualification.py');
  assert.equal(plan.qualifier,'scripts/qualify_glaze_v1_6_zero_drift_regression.py');
  assert.equal(plan.comparison.mode,'independent-browser-session-zero-decoded-pixel-drift');
  assert.equal(plan.comparison.changedPixelTolerance,0);
  assert.equal(plan.comparison.maximumChannelDeltaTolerance,0);
  assert.equal(plan.comparison.compareDecodedRgba,true);
  assert.equal(plan.comparison.sceneSetMustMatch,true);
  assert.equal(plan.comparison.browserProductMustMatch,true);
  assert.equal(plan.comparison.browserRevisionMustMatch,true);
  assert.equal(plan.comparison.sameRunnerRequired,true);
  assert.equal(plan.requiredSceneCount,9);
  assert.equal(new Set(plan.requiredSceneIds).size,9);
  assert.deepEqual(sorted(plan.requiredSceneIds),sorted(renderPlan.scenes.map(scene=>scene.id)));
  assert.equal(plan.evidence.type,'rendered');
  assert.equal(plan.evidence.machineGroupAlreadySatisfied,true);
  assert.equal(plan.evidence.renderedGroupSatisfiedOnlyOnZeroDriftPass,true);
  assert.equal(plan.evidence.baselineAndRepeatBoundToSameFrozenSource,true);
  assert.equal(plan.evidence.referenceMayBePromotedToDurableRecordOnlyAfterSuccessfulExactHeadRun,true);

  assert.equal(schema.properties.sourceRevision.const,SOURCE);
  assert.equal(schema.properties.acceptanceLaneId.const,'regression-testing');
  assert.equal(schema.properties.comparison.properties.changedPixelTolerance.const,0);
  assert.equal(schema.properties.comparison.properties.maximumChannelDeltaTolerance.const,0);

  for(const key of [
    'humanEvidenceClaimed','assistiveTechnologyEvidenceClaimed','physicalDeviceEvidenceClaimed',
    'nativePlatformEvidenceClaimed','representativePerformanceEvidenceClaimed',
    'candidateStatusGranted','releaseCandidateStatusGranted','stableStatusGranted',
    'consumerAcceptanceAutomatic','deploymentAcceptanceAutomatic','productionAcceptanceAutomatic'
  ]) assert.equal(plan.authority[key],false,'authority drift: '+key);

  assert.equal(machine.sourceRevision,SOURCE);
  assert.equal(rendered.sourceRevision,SOURCE);
  const current=createGlazeV16AcceptanceMatrix({
    exactRevision:SOURCE,
    evidence:[...machine.machineEvidence,...rendered.renderedEvidence]
  });
  assert.equal(current.verifiedCount,16);
  assert.equal(current.unverifiedCount,8);
  const currentRegression=current.lanes.find(lane=>lane.id==='regression-testing');
  assert.equal(currentRegression.status,'unverified');
  assert.equal(currentRegression.satisfiedEvidenceGroupCount,1);

  const synthetic={
    id:'regression-testing',verified:true,revision:SOURCE,evidenceType:'rendered',
    reference:'STRUCTURAL-SELF-TEST zero-drift rendered regression'
  };
  const projected=createGlazeV16AcceptanceMatrix({
    exactRevision:SOURCE,
    evidence:[...machine.machineEvidence,...rendered.renderedEvidence,synthetic]
  });
  assert.equal(projected.verifiedCount,17);
  assert.equal(projected.unverifiedCount,7);
  assert.equal(projected.notApplicableCount,0);
  assert.equal(projected.qualificationEvidenceComplete,false);
  assert.equal(projected.readyForGovernedQualificationReview,false);
  const projectedRegression=projected.lanes.find(lane=>lane.id==='regression-testing');
  assert.equal(projectedRegression.status,'verified');
  const representative=projected.lanes.find(lane=>lane.id==='representative-rendering');
  assert.equal(representative.status,'unverified');
  assert.equal(representative.satisfiedEvidenceGroupCount,1);
  for(const id of ['assistive-technology','performance']){
    const lane=projected.lanes.find(item=>item.id===id);
    assert.equal(lane.status,'unverified');
    assert.equal(lane.satisfiedEvidenceGroupCount,0);
  }

  assert.equal(version.trim(),'1.5.1');
  assert.equal(lifecycle.currentOfficial,'1.5.1');
  assert.equal(lifecycle.currentStable,'1.5.1');
  assert.equal(lifecycle.plannedNext,null);
  assert.equal(lifecycle.activeCandidate,null);
  assert.equal(lifecycle.activePatchReleaseCandidate,null);

  console.log('GLAZE UI V1.6 zero-drift regression plan verification: PASS');
  console.log('Comparison rule: 0 changed decoded pixels / 0 maximum channel delta.');
  console.log('Projected accepted-regression checkpoint: 17 verified / 7 unverified; qualification remains incomplete.');
  console.log('Boundary: structural projection only; no rendered regression evidence is recorded until an exact-head zero-drift run succeeds.');
}

main().catch(error=>{
  console.error('GLAZE UI V1.6 zero-drift regression plan FAILED: '+(error?.stack||error));
  process.exitCode=1;
});
