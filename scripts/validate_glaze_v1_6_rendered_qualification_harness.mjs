#!/usr/bin/env node
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

import {createGlazeV16AcceptanceMatrix} from '../js/glaze-v1.6-acceptance.dev.mjs';

const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const PLAN='contracts/v1.6/qualification.rendered.plan.json';
const SCHEMA='schemas/v1.6-rendered-qualification-plan.schema.json';
const HARNESS='reference/v1.6/rendered-qualification.html';
const MACHINE='acceptance/v1.6-machine-evidence.json';
const SOURCE='c7509c79256b04b0aa67cb9dd0737d7588e0ae4a';

const text=relative=>readFile(path.join(ROOT,relative),'utf8');
const json=async relative=>JSON.parse(await text(relative));
const sorted=values=>[...values].sort();

async function main(){
  const [plan,schema,html,machine]=await Promise.all([
    json(PLAN),json(SCHEMA),text(HARNESS),json(MACHINE)
  ]);

  assert.equal(plan.schemaVersion,1);
  assert.equal(plan.planId,'goreecloud.glaze-ui.v1.6.rendered-browser-qualification');
  assert.equal(plan.lifecycle,'DevelopmentQualification');
  assert.equal(plan.sourceRevision,SOURCE);
  assert.equal(plan.acceptanceModelVersion,'1.6.0-dev.12');
  assert.equal(plan.stableBaseline,'1.5.1');
  assert.equal(plan.consumerEligible,false);
  assert.equal(plan.harness,HARNESS);
  assert.equal(plan.captureScript,'scripts/capture_glaze_v1_6_rendered_qualification.py');
  assert.equal(plan.validator,'scripts/validate_glaze_v1_6_rendered_qualification_harness.mjs');
  assert.equal(plan.workflow,'.github/workflows/glaze-v1.6-rendered-qualification.yml');
  assert.equal(plan.artifactDirectory,'artifacts/v1.6-rendered');
  assert.equal(plan.networkPolicy,'repository-local-only');
  assert.equal(plan.browserClass,'chromium-headless');

  const expectedEligible=[
    'reduced-motion','reduced-transparency','increased-contrast','large-text',
    'responsive-layouts','form-factor-transitions','layout-stability','representative-rendering'
  ];
  assert.deepEqual(sorted(plan.eligibleRenderedEvidenceLaneIds),sorted(expectedEligible));
  assert.equal(plan.scenes.length,9);
  assert.equal(new Set(plan.scenes.map(scene=>scene.id)).size,9);
  for(const scene of plan.scenes){
    assert.ok(Array.isArray(scene.viewport)&&scene.viewport.length===2,'scene viewport must be two-dimensional: '+scene.id);
    assert.ok(Array.isArray(scene.laneIds)&&scene.laneIds.length>=1,'scene lane coverage missing: '+scene.id);
    for(const lane of scene.laneIds){
      assert.ok(expectedEligible.includes(lane),'scene claims an ineligible rendered lane: '+scene.id+' -> '+lane);
    }
  }
  const covered=new Set(plan.scenes.flatMap(scene=>scene.laneIds));
  assert.deepEqual(sorted(covered),sorted(expectedEligible),'scene coverage must exactly match eligible rendered lanes');

  assert.equal(plan.evidenceBoundary.renderedBrowserOnly,true);
  for(const key of [
    'humanEvidenceClaimed','assistiveTechnologyEvidenceClaimed','physicalDeviceEvidenceClaimed',
    'nativePlatformEvidenceClaimed','representativePerformanceEvidenceClaimed','regressionBaselineClaimed',
    'lifecyclePromotionAutomatic','stableStatusGranted','consumerAcceptanceAutomatic',
    'deploymentAcceptanceAutomatic','productionAcceptanceAutomatic'
  ]) assert.equal(plan.evidenceBoundary[key],false,'boundary drift: '+key);

  assert.equal(schema.properties.sourceRevision.const,SOURCE);
  assert.equal(schema.properties.acceptanceModelVersion.const,'1.6.0-dev.12');
  assert.equal(schema.properties.networkPolicy.const,'repository-local-only');
  assert.equal(schema.properties.browserClass.const,'chromium-headless');
  assert.ok(schema.properties.scenes.items.required.includes('laneIds'));

  assert.equal(machine.sourceRevision,SOURCE);
  assert.equal(machine.acceptanceModelVersion,'1.6.0-dev.12');
  const syntheticRendered=plan.eligibleRenderedEvidenceLaneIds.map(id=>({
    id,verified:true,revision:SOURCE,evidenceType:'rendered',
    reference:'STRUCTURAL-SELF-TEST rendered lane '+id
  }));
  const matrix=createGlazeV16AcceptanceMatrix({
    exactRevision:SOURCE,
    evidence:[...machine.machineEvidence,...syntheticRendered]
  });
  const expected=plan.expectedMatrixDispositionAfterAcceptedRenderedEvidence;
  assert.equal(matrix.verifiedCount,expected.verifiedLaneCount);
  assert.equal(matrix.unverifiedCount,expected.unverifiedLaneCount);
  assert.equal(matrix.notApplicableCount,expected.notApplicableLaneCount);
  assert.equal(matrix.qualificationEvidenceComplete,false);
  assert.equal(matrix.readyForGovernedQualificationReview,false);
  const newlyVerified=matrix.lanes
    .filter(lane=>lane.status==='verified'&&!machine.matrixDisposition.fullyVerifiedLaneIds.includes(lane.id))
    .map(lane=>lane.id);
  assert.deepEqual(sorted(newlyVerified),sorted(expected.fullyVerifiedByThisCheckpoint));
  assert.deepEqual(sorted(matrix.blockingLaneIds),sorted([
    ...expected.remainingPartialLaneIds,...expected.remainingUntouchedLaneIds
  ]));
  const representative=matrix.lanes.find(lane=>lane.id==='representative-rendering');
  assert.equal(representative.status,'unverified');
  assert.equal(representative.satisfiedEvidenceGroupCount,1);
  assert.ok(matrix.blockingLaneIds.includes('regression-testing'),'rendered capture without a governed baseline must not close regression testing');
  assert.ok(!plan.eligibleRenderedEvidenceLaneIds.includes('regression-testing'));

  const requiredMarkers=[
    "import {glazeV16Development} from '../../js/glaze-v1.6-development.mjs'",
    "resolveGlazeLoadingPresentation",
    "resolveGlazeAccessibilityProfiles",
    "resolveGlazeResponsiveLayout",
    "resolveGlazeConnectivityPresentation",
    "state:'fully-online'",
    "window.__glazeV16RenderedEvidence=evidence",
    "window.__glazeV16RenderedReady=true",
    "humanEvidenceClaimed:false",
    "assistiveTechnologyEvidenceClaimed:false",
    "physicalDeviceEvidenceClaimed:false",
    "representativePerformanceEvidenceClaimed:false",
    "regressionBaselineClaimed:false",
    "lifecyclePromotionAutomatic:false"
  ];
  for(const marker of requiredMarkers) assert.ok(html.includes(marker),'rendered harness missing marker: '+marker);
  assert.equal(html.includes("state:'connected'"),false,'invalid legacy connectivity state must not remain');

  const forbidden=[
    /<(?:script|link|img|iframe|video|audio|source)\b[^>]*(?:src|href)\s*=\s*["']https?:\/\//i,
    /fetch\s*\(/i,/XMLHttpRequest/i,/WebSocket\s*\(/i,/sendBeacon\s*\(/i,
    /getUserMedia\s*\(/i,/navigator\.mediaDevices/i,
    /promotionEligible\s*[:=]\s*true/i,/consumerEligible\s*[:=]\s*true/i,
    /stableStatusGranted\s*[:=]\s*true/i
  ];
  for(const pattern of forbidden) assert.equal(pattern.test(html),false,'rendered harness violates local/fail-closed boundary: '+pattern);

  console.log('GLAZE UI V1.6 rendered qualification harness structural verification: PASS');
  console.log('Expected accepted-rendered checkpoint: 16 verified / 8 unverified; qualification remains incomplete.');
  console.log('Boundary: browser rendering only; no human, assistive-technology, physical-device, native-platform, performance, regression-baseline, lifecycle, consumer, deployment, or production acceptance is created.');
}

main().catch(error=>{
  console.error('GLAZE UI V1.6 rendered qualification harness FAILED: '+(error?.stack||error));
  process.exitCode=1;
});
