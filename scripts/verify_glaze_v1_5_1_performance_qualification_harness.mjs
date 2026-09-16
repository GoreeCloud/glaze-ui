#!/usr/bin/env node
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const text = relative => readFile(path.join(ROOT, relative), 'utf8');
const json = async relative => JSON.parse(await text(relative));

async function main() {
  const qualification = await json('contracts/v1.5.1/qualification.dev.json');
  const harnessContract = await json('contracts/v1.5.1/performance-qualification-harness.dev.json');
  const html = await text(harnessContract.harness);

  assert.equal(qualification.contractVersion, '1.5.1-dev.1');
  assert.equal(qualification.releaseLifecycle, 'Development');
  assert.equal(qualification.promotionEligible, false);
  assert.equal(qualification.consumerEligible, false);
  assert.equal(qualification.releaseCandidate, false);
  assert.equal(qualification.stable, false);
  assert.equal(qualification.requiredQualificationCount, 2);
  assert.deepEqual(
    qualification.requiredQualification.map(item => [item.id, item.status]),
    [
      ['performance-representative-budget', 'pending'],
      ['platform-posture-continuity', 'pending']
    ],
    'V1.5.1 qualification obligations must remain pending until external evidence is reviewed'
  );

  assert.equal(harnessContract.version, '1.5.1-dev.1');
  assert.equal(harnessContract.lifecycle, 'Development');
  assert.equal(harnessContract.stableBaseline, '1.5.0');
  assert.equal(harnessContract.authority, 'performance-measurement-surface-only');
  assert.equal(harnessContract.qualificationId, 'performance-representative-budget');
  assert.equal(harnessContract.governingBudget, 'Standard — Glaze UI Performance Budget v1.0');
  assert.equal(harnessContract.candidateRuntime, 'js/glaze-v1.5-resolution.dev.mjs');
  assert.equal(harnessContract.networkPolicy, 'repository-local-only');
  assert.equal(harnessContract.telemetryRequired, false);
  assert.equal(harnessContract.remoteAnalysisRequired, false);
  assert.equal(harnessContract.automaticAcceptance, false);
  assert.equal(harnessContract.automaticPromotionEligibility, false);
  assert.equal(harnessContract.exactRevisionRequired, true);

  assert.ok(harnessContract.minimumSamples.resolverWarmup >= 20);
  assert.ok(harnessContract.minimumSamples.resolverMeasured >= 200);
  assert.ok(harnessContract.minimumSamples.interactionToPaint >= 30);
  assert.ok(harnessContract.minimumSamples.idleFrameIntervals >= 120);
  assert.ok(harnessContract.minimumSamples.activeFrameIntervals >= 240);
  assert.equal(harnessContract.thresholds.resolverP95MsMax, 10.0);
  assert.equal(harnessContract.thresholds.resolverP99MsMax, 16.7);
  assert.equal(harnessContract.thresholds.interactionPaintP95MsMax, 100);
  assert.equal(harnessContract.thresholds.interactionPaintP99MsMax, 200);
  assert.equal(harnessContract.thresholds.severeFrameStallRatePercentMax, 1.0);
  assert.equal(harnessContract.thresholds.catastrophicForegroundStallCountMax, 0);
  assert.deepEqual(harnessContract.requiredTransitionCoverage, [
    'connectivity',
    'capability-or-authorization',
    'layout-or-window',
    'input-or-presentation',
    'constrained-or-low-power'
  ]);

  const requiredMarkers = [
    'Local measurement surface only — not acceptance evidence.',
    '?revision=&lt;40-hex-sha&gt;',
    "import {resolveGlazeInterface} from '../../js/glaze-v1.5-resolution.dev.mjs'",
    'resolverDurations.length>=200',
    'interactionDurations.length>=30',
    'idleIntervals.length>=120',
    'activeIntervals.length>=240',
    'event.isTrusted',
    'requestAnimationFrame(()=>requestAnimationFrame(',
    "document.visibilityState !== 'visible'",
    'invalidatedByBackgrounding',
    'capabilityTruthModified',
    'taskStateReset',
    'pageReloadRequired',
    'authorizationInferred',
    'automaticNavigationAllowed',
    'automaticPermissionRequestAllowed',
    'automaticConsequentialExecutionAllowed',
    'automaticFallbackExecutionAllowed',
    'withinApprovedBudget',
    "canonicalQualificationStatus:'PENDING_REVIEW'",
    'not platform-posture-continuity evidence',
    'navigator.clipboard.writeText'
  ];
  for (const marker of requiredMarkers) {
    assert.ok(html.includes(marker), `performance harness missing required marker: ${marker}`);
  }

  const thresholdMarkers = [
    'resolverP95<=10.0',
    'resolverP99<=16.7',
    'interactionP95<=100',
    'interactionP99<=200',
    'Math.max(20,1.25*idleMedian)',
    'severeRate<=1.0',
    'catastrophicCount===0'
  ];
  for (const marker of thresholdMarkers) assert.ok(html.includes(marker), `performance harness threshold drift: ${marker}`);

  const forbiddenRemotePatterns = [
    /<script[^>]+src\s*=\s*["']https?:\/\//i,
    /<link[^>]+href\s*=\s*["']https?:\/\//i,
    /<img[^>]+src\s*=\s*["']https?:\/\//i,
    /fetch\s*\(/i,
    /XMLHttpRequest/i,
    /WebSocket/i,
    /sendBeacon/i,
    /getUserMedia/i,
    /navigator\.mediaDevices/i
  ];
  for (const pattern of forbiddenRemotePatterns) {
    assert.equal(pattern.test(html), false, `performance harness violates local-only boundary: ${pattern}`);
  }

  const forbiddenAuthorityClaims = [
    /canonicalQualificationStatus\s*:\s*['"]PASS['"]/i,
    /promotionEligible\s*[:=]\s*true/i,
    /releaseCandidate\s*[:=]\s*true/i,
    /stable\s*[:=]\s*true/i,
    /consumerEligible\s*[:=]\s*true/i,
    /automaticAcceptance\s*[:=]\s*true/i
  ];
  for (const pattern of forbiddenAuthorityClaims) {
    assert.equal(pattern.test(html), false, `performance harness must not create acceptance authority: ${pattern}`);
  }

  assert.equal(harnessContract.privacy.aggregateTimingOnly, true);
  assert.equal(harnessContract.privacy.rawUserContentRecorded, false);
  assert.equal(harnessContract.privacy.credentialsRecorded, false);
  assert.equal(harnessContract.privacy.providerSecretsRecorded, false);
  assert.equal(harnessContract.privacy.rawActivityRecorded, false);

  console.log('GLAZE UI V1.5.1 performance qualification harness structural verification: PASS');
  console.log('Boundary: local measurement tooling only; both V1.5.1 qualifications remain pending.');
  console.log('No representative performance result, posture result, lifecycle promotion, consumer acceptance, deployment, or production acceptance is implied.');
}

main().catch(error => {
  console.error(`GLAZE UI V1.5.1 performance qualification harness FAILED: ${error?.stack || error}`);
  process.exitCode = 1;
});
