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
  const contract = await json('contracts/v1.5.1/posture-qualification-harness.dev.json');
  const html = await text(contract.harness);

  assert.equal(qualification.contractVersion, '1.5.1-dev.1');
  assert.equal(qualification.releaseLifecycle, 'Development');
  assert.equal(qualification.promotionEligible, false);
  assert.equal(qualification.consumerEligible, false);
  assert.equal(qualification.releaseCandidate, false);
  assert.equal(qualification.stable, false);
  assert.deepEqual(
    qualification.requiredQualification.map(item => [item.id, item.status]),
    [
      ['performance-representative-budget', 'pending'],
      ['platform-posture-continuity', 'pending']
    ]
  );

  assert.equal(contract.version, '1.5.1-dev.1');
  assert.equal(contract.lifecycle, 'Development');
  assert.equal(contract.stableBaseline, '1.5.0');
  assert.equal(contract.authority, 'posture-review-capture-only');
  assert.equal(contract.qualificationId, 'platform-posture-continuity');
  assert.equal(contract.candidateRuntime, 'js/glaze-v1.5-resolution.dev.mjs');
  assert.equal(contract.networkPolicy, 'repository-local-only');
  assert.equal(contract.telemetryRequired, false);
  assert.equal(contract.remoteAnalysisRequired, false);
  assert.equal(contract.automaticAcceptance, false);
  assert.equal(contract.automaticPromotionEligibility, false);
  assert.equal(contract.exactRevisionRequired, true);
  assert.equal(contract.externalEvidenceRequired, true);
  assert.equal(contract.evidenceSource.physicalDeviceAllowed, true);
  assert.equal(contract.evidenceSource.approvedTargetRuntimeAllowed, true);
  assert.equal(contract.evidenceSource.machineSimulationAloneAllowed, false);
  assert.equal(contract.evidenceSource.trustedHumanObservationRequired, true);
  assert.equal(contract.applicability.supportedTransitionFamiliesMustBeDeclared, true);
  assert.equal(contract.applicability.everyDeclaredSupportedFamilyRequiresObservedEvidence, true);
  assert.equal(contract.applicability.rotationRequiredWhenSupported, true);
  assert.equal(contract.applicability.foldOrPostureEvidenceRequiredForThisQualification, true);
  assert.deepEqual(contract.transitionFamilies, [
    'fold-unfold',
    'posture-mode-change',
    'rotation',
    'related-form-factor-transition'
  ]);

  const expectedInvariants = {
    taskStateReset: false,
    pageReloadRequired: false,
    currentDestinationChanged: false,
    capabilityTruthModified: false,
    primaryActionOrderStable: true,
    authorizationInferred: false,
    permissionGranted: false,
    automaticNavigationAllowed: false,
    automaticPermissionRequestAllowed: false,
    automaticConsequentialExecutionAllowed: false,
    automaticFallbackExecutionAllowed: false
  };
  assert.deepEqual(contract.requiredInvariants, expectedInvariants);

  const requiredMarkers = [
    'Human-observed capture surface only — not acceptance evidence.',
    '?revision=&lt;40-hex-sha&gt;',
    "import {resolveGlazeInterface} from '../../js/glaze-v1.5-resolution.dev.mjs'",
    'Machine simulation alone is not sufficient.',
    'event.isTrusted',
    "'device-posture':{posture:observed.posture}",
    "environment:{orientation:observed.orientation}",
    "currentDestinationId:'search'",
    'currentDestinationPreserved',
    'taskStatePreserved',
    'capabilityTruthPreserved',
    'primaryHierarchyStable',
    'protectedMeaningPreserved',
    'noAutomaticAuthorityAction',
    "canonicalQualificationStatus:'PENDING_REVIEW'",
    'rawTaskContentRecorded:false',
    'rawSensorStreamRecorded:false',
    'exactObservationTimestampsRecorded:false',
    'navigator.clipboard.writeText'
  ];
  for (const marker of requiredMarkers) {
    assert.ok(html.includes(marker), `posture harness missing required marker: ${marker}`);
  }

  const forbiddenRemotePatterns = [
    /<script[^>]+src\s*=\s*["']https?:\/\//i,
    /<link[^>]+href\s*=\s*["']https?:\/\//i,
    /<img[^>]+src\s*=\s*["']https?:\/\//i,
    /fetch\s*\(/i,
    /XMLHttpRequest/i,
    /WebSocket/i,
    /sendBeacon/i,
    /getUserMedia/i,
    /navigator\.mediaDevices/i,
    /geolocation/i
  ];
  for (const pattern of forbiddenRemotePatterns) {
    assert.equal(pattern.test(html), false, `posture harness violates local-only/privacy boundary: ${pattern}`);
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
    assert.equal(pattern.test(html), false, `posture harness must not create acceptance authority: ${pattern}`);
  }

  assert.equal(contract.privacy.rawTaskContentRecorded, false);
  assert.equal(contract.privacy.credentialsRecorded, false);
  assert.equal(contract.privacy.providerSecretsRecorded, false);
  assert.equal(contract.privacy.preciseLocationRecorded, false);
  assert.equal(contract.privacy.rawSensorStreamRecorded, false);
  assert.equal(contract.privacy.exactObservationTimestampsRecorded, false);

  console.log('GLAZE UI V1.5.1 posture qualification harness structural verification: PASS');
  console.log('Boundary: external human-observed capture tooling only; platform-posture-continuity remains pending.');
  console.log('No posture acceptance, lifecycle promotion, consumer acceptance, deployment, or production acceptance is implied.');
}

main().catch(error => {
  console.error(`GLAZE UI V1.5.1 posture qualification harness FAILED: ${error?.stack || error}`);
  process.exitCode = 1;
});
