#!/usr/bin/env node
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {resolveGlazeOptics, glazeOpticalEngineV14} from '../js/glaze-v1.4-optical-engine.mjs';

function read(path) {
  return readFileSync(new URL(`../${path}`, import.meta.url), 'utf8');
}

function json(path) {
  return JSON.parse(read(path));
}

const VERSION = '1.4.0';

assert.equal(read('VERSION').trim(), VERSION, 'VERSION must be 1.4.0');

const lifecycle = json('registry/lifecycle.json');
assert.equal(lifecycle.currentOfficial, VERSION, 'currentOfficial must be 1.4.0');
assert.equal(lifecycle.currentStable, VERSION, 'currentStable must be 1.4.0');
assert.equal(lifecycle.activeCandidate, null, 'Stable release must not leave an active candidate');
const release = lifecycle.releases.find(item => item.version === VERSION);
assert.ok(release, 'lifecycle must contain the 1.4.0 release record');
assert.equal(release.status, 'stable');
assert.equal(release.consumerEligible, true);
assert.equal(release.webEntrypoint, 'css/glaze-v1.4.0.css');
assert.equal(release.runtimeEntrypoint, 'js/glaze-v1.4.0.mjs');
assert.equal(release.deferredFollowUp, 'GLAZE_UI_V1_4_1_HARDENING.md');

const consumers = json('consumers/registry.json');
assert.equal(consumers.officialBaseline, VERSION);
assert.equal(consumers.requiredConsumerVersion, VERSION);
for (const consumer of consumers.consumers) {
  assert.equal(consumer.requiredTargetVersion, VERSION, `${consumer.name} must require ${VERSION}`);
}

assert.equal(glazeOpticalEngineV14.version, VERSION);
assert.equal(glazeOpticalEngineV14.lifecycle, 'stable');
assert.equal(glazeOpticalEngineV14.telemetryRequired, false);
assert.equal(glazeOpticalEngineV14.remoteContextRequired, false);
assert.equal(glazeOpticalEngineV14.preservesTokenSystem, true);
assert.equal(glazeOpticalEngineV14.additiveComponentApi, true);
assert.equal(glazeOpticalEngineV14.maxMemoryTintInfluence, 0.08);

const calm = resolveGlazeOptics({backgroundComplexity: 'simple', backgroundLuminance: 'mid'});
const busy = resolveGlazeOptics({backgroundComplexity: 'complex', backgroundLuminance: 'bright'});
assert.ok(busy.frostStrength > calm.frostStrength, 'busy/bright backgrounds must increase frost');
assert.ok(calm.frostStrength >= 0.20 && calm.frostStrength <= 0.88);
assert.ok(busy.frostStrength >= 0.20 && busy.frostStrength <= 0.88);

const lowSemantic = resolveGlazeOptics({semanticImportance: 0});
const highSemantic = resolveGlazeOptics({semanticImportance: 1});
assert.ok(highSemantic.semanticProtection > lowSemantic.semanticProtection, 'semantic importance must increase protection');
assert.ok(highSemantic.blurScale < lowSemantic.blurScale, 'semantic protection must reduce blur scale');

const tint = resolveGlazeOptics({memoryTint: {css: 'rgb(12 120 220)', influence: 1}});
assert.equal(tint.memoryTint.influence, 0.08, 'memory tint influence must be clamped to 8%');

for (const accessibility of [
  {forcedColors: true},
  {reducedTransparency: true}
]) {
  const result = resolveGlazeOptics({
    backgroundComplexity: 'complex',
    memoryTint: {css: 'red', influence: 0.08},
    accessibility
  });
  assert.equal(result.mode, 'solid-accessible');
  assert.equal(result.blurScale, 0);
  assert.equal(result.memoryTint, null);
  assert.equal(result.decorativeTintAllowed, false);
}

const contrast = resolveGlazeOptics({
  daypart: 'dusk',
  memoryTint: {css: 'red', influence: 0.08},
  accessibility: {increasedContrast: true}
});
assert.equal(contrast.memoryTint, null);
assert.equal(contrast.warmth, 0);
assert.equal(contrast.decorativeTintAllowed, false);

const stableCss = read('css/glaze-v1.4.0.css');
assert.match(stableCss, /glaze-v1\.3\.0\.css/);
assert.match(stableCss, /solid-accessible/);
assert.match(stableCss, /forced-colors/);
assert.match(stableCss, /prefers-reduced-transparency/);

const stableRuntime = read('js/glaze-v1.4.0.mjs');
assert.match(stableRuntime, /glaze-v1\.3\.0\.mjs/);
assert.match(stableRuntime, /glaze-v1\.4-optical-engine\.mjs/);

const contract = read('GLAZE_UI_V1_4.md');
const followUp = read('GLAZE_UI_V1_4_1_HARDENING.md');
const acceptance = read('acceptance/v1.4-stable.md');
assert.match(contract, /Official Stable/);
assert.match(contract, /human validation and human verification are assigned to GLAZE UI V1\.4\.1/i);
assert.match(followUp, /Human Validation & Optical Hardening/);
assert.match(acceptance, /not represented as passed evidence/i);

console.log('GLAZE UI V1.4.0 Stable verification passed.');
