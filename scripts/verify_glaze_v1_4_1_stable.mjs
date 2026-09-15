#!/usr/bin/env node
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {
  createGlazeOpticalEngineV141,
  deriveGlazeOpticalPerformanceLevel,
  glazeOpticalEngineV141
} from '../js/glaze-v1.4.1.mjs';

function read(path) {
  return readFileSync(new URL(`../${path}`, import.meta.url), 'utf8');
}

function json(path) {
  return JSON.parse(read(path));
}

const VERSION = '1.4.1';
const BASELINE = '1.4.0';
const QUALIFIED_ANCHOR = '66478aed461b83c49b2ed027c3e4afc26520e98c';

assert.equal(read('VERSION').trim(), VERSION, 'VERSION must identify 1.4.1');

const lifecycle = json('registry/lifecycle.json');
assert.equal(lifecycle.currentOfficial, VERSION, 'currentOfficial must be 1.4.1');
assert.equal(lifecycle.currentStable, VERSION, 'currentStable must be 1.4.1');
assert.equal(lifecycle.activeCandidate, null, 'Stable release must not leave an active candidate');
assert.equal(lifecycle.activePatchReleaseCandidate, null, 'Stable release must not leave an active patch RC');

const release = lifecycle.releases.find(item => item.version === VERSION);
assert.ok(release, 'lifecycle must contain the 1.4.1 release record');
assert.equal(release.status, 'stable');
assert.equal(release.consumerEligible, true);
assert.equal(release.stableBaseline, BASELINE);
assert.equal(release.contract, 'GLAZE_UI_V1_4_1.md');
assert.equal(release.qualification, 'GLAZE_UI_V1_4_1_HARDENING.md');
assert.equal(release.acceptance, 'acceptance/v1.4.1-stable.md');
assert.equal(release.webEntrypoint, 'css/glaze-v1.4.1.css');
assert.equal(release.runtimeEntrypoint, 'js/glaze-v1.4.1.mjs');
assert.equal(release.opticalEngine, 'js/glaze-v1.4.1-optical-engine.mjs');
assert.equal(release.sourceQualificationAnchor, QUALIFIED_ANCHOR);

const baseline = lifecycle.releases.find(item => item.version === BASELINE);
assert.ok(baseline, 'lifecycle must retain the 1.4.0 rollback release');
assert.equal(baseline.status, 'stable');
assert.equal(baseline.consumerEligible, true);
assert.equal(baseline.webEntrypoint, 'css/glaze-v1.4.0.css');
assert.equal(baseline.runtimeEntrypoint, 'js/glaze-v1.4.0.mjs');

const consumers = json('consumers/registry.json');
assert.equal(consumers.officialBaseline, VERSION);
assert.equal(consumers.requiredConsumerVersion, VERSION);
assert.equal(consumers.officialProductLabel, lifecycle.officialProductLabel);
for (const consumer of consumers.consumers) {
  assert.equal(consumer.requiredTargetVersion, VERSION, `${consumer.name} must require ${VERSION}`);
  assert.equal(consumer.productionEligible, false, `${consumer.name} must not be auto-certified by the shared Stable promotion`);
}

assert.equal(
  read('css/glaze-v1.4.1.css'),
  read('css/glaze-v1.4.1.candidate.css'),
  'Stable V1.4.1 CSS must be byte-identical to the reviewed Candidate CSS'
);
assert.equal(
  read('js/glaze-v1.4.1-optical-engine.mjs'),
  read('js/glaze-v1.4.1-optical-engine.candidate.mjs'),
  'Stable V1.4.1 optical engine must be byte-identical to the reviewed Candidate engine'
);

const runtime = read('js/glaze-v1.4.1.mjs');
assert.match(runtime, /glaze-v1\.4\.0\.mjs/);
assert.match(runtime, /glaze-v1\.4\.1-optical-engine\.mjs/);
assert.equal(glazeOpticalEngineV141.version, VERSION);
assert.equal(glazeOpticalEngineV141.lifecycle, 'stable');
assert.equal(glazeOpticalEngineV141.stableBaseline, BASELINE);
assert.equal(glazeOpticalEngineV141.qualifiedImplementationAnchor, QUALIFIED_ANCHOR);
assert.equal(glazeOpticalEngineV141.telemetryRequired, false);
assert.equal(glazeOpticalEngineV141.remoteContextRequired, false);
assert.equal(glazeOpticalEngineV141.deviceIdentityRequired, false);
assert.equal(glazeOpticalEngineV141.humanAcceptanceAutomatic, false);
assert.equal(glazeOpticalEngineV141.patchPromotionAutomatic, false);

const adapterFailure = createGlazeOpticalEngineV141({
  signalAdapter: {resolve() { throw new Error('synthetic local adapter failure'); }}
}).resolve();
assert.equal(adapterFailure.mode, 'solid-accessible');
assert.equal(adapterFailure.adapterStatus, 'failed-safe');
assert.equal(adapterFailure.blurScale, 0);
assert.equal(adapterFailure.memoryTint, null);

const full = createGlazeOpticalEngineV141().resolve({
  performance: {requestedLevel: 'full-optical', capabilityLevel: 'full-optical'}
});
assert.equal(full.performance.acceptedLevel, 'full-optical');

const constrained = createGlazeOpticalEngineV141().resolve({
  performance: {
    requestedLevel: 'full-optical',
    capabilityLevel: 'full-optical',
    thermalConstrained: true
  }
});
assert.equal(constrained.performance.acceptedLevel, 'efficient-optical');
assert.ok(constrained.performance.downgradeReasons.includes('thermal-budget'));

const measured = deriveGlazeOpticalPerformanceLevel({
  targetFrameMs: 11.12,
  p95FrameMs: 33.28,
  slowFrameShare: 0.21,
  degradation: 0,
  longTasks: 0
});
assert.equal(measured.capabilityLevel, 'efficient-optical');

const contract = read('GLAZE_UI_V1_4_1.md');
const acceptance = read('acceptance/v1.4.1-stable.md');
const qualification = read('GLAZE_UI_V1_4_1_HARDENING.md');
assert.match(contract, /Stable patch release/);
assert.match(contract, /qualified implementation anchor/i);
assert.match(acceptance, /Accepted as Official Stable/i);
assert.match(acceptance, /exact-head release and promotion gates/i);
assert.match(qualification, /Human Validation & Optical Hardening/);

console.log('GLAZE UI V1.4.1 Stable verification passed.');
