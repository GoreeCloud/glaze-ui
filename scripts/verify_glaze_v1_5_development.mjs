import assert from 'node:assert/strict';
import fs from 'node:fs';
import {
  GLAZE_CONTEXT_DOMAINS,
  GLAZE_CAPABILITY_DOMAINS,
  GLAZE_CAPABILITY_STATES,
  normalizeGlazeContext,
  normalizeGlazeCapability,
  normalizeGlazeCapabilities,
  resolveGlazeCapability,
  resolveCapabilityAwareActions,
  resolveGlazeAdaptation,
  createGlazeAdaptationStabilizer,
  mapV141OpticalCapabilities,
  glazeContextCapabilityDevelopment
} from '../js/glaze-v1.5-context-capability.dev.mjs';

const development = JSON.parse(fs.readFileSync(new URL('../registry/development/glaze-v1.5.0-dev.1.json', import.meta.url), 'utf8'));
const contract = JSON.parse(fs.readFileSync(new URL('../contracts/v1.5/context-capability.dev.json', import.meta.url), 'utf8'));

assert.equal(development.version, '1.5.0-dev.1');
assert.equal(development.lifecycle, 'development');
assert.equal(development.consumerEligible, false);
assert.equal(development.stableBaseline, '1.4.1');
assert.equal(development.stable141Preserved, true);
assert.equal(contract.version, development.version);
assert.equal(contract.lifecycle, 'development');
assert.equal(contract.acceptance.releaseCandidateAccepted, false);
assert.equal(contract.acceptance.stableAccepted, false);
assert.equal(glazeContextCapabilityDevelopment.consumerEligible, false);
assert.equal(glazeContextCapabilityDevelopment.glazeIsAuthorizationAuthority, false);

assert.deepEqual([...GLAZE_CONTEXT_DOMAINS], contract.contextDomains);
assert.deepEqual([...GLAZE_CAPABILITY_DOMAINS], contract.capabilityDomains);
assert.deepEqual([...GLAZE_CAPABILITY_STATES], contract.capabilityStates);

const context = normalizeGlazeContext({
  layout: {density: 'compact'},
  input: {primary: 'touch'},
  connectivity: {class: 'offline'}
});
assert.equal(context.contextAvailable, true);
assert.equal(context.persisted, false);
assert.equal(context.telemetryRequired, false);
assert.equal(context.remoteAnalysisRequired, false);
assert.deepEqual(context.availableDomains, ['layout', 'input', 'connectivity']);
assert.throws(() => normalizeGlazeContext({content: {rawContent: 'private'}}), /Sensitive or raw context field/);
assert.throws(() => normalizeGlazeContext({task: {sessionToken: 'secret'}}), /Sensitive or raw context field/);

const missingProvenance = normalizeGlazeCapability({id: 'service.search', domain: 'service', state: 'available'});
assert.equal(missingProvenance.state, 'unknown');
assert.equal(missingProvenance.availableForInvocation, false);
assert.ok(missingProvenance.reasonCodes.includes('missing-provenance-failed-closed'));

const capabilities = normalizeGlazeCapabilities([
  {id: 'service.search', domain: 'service', state: 'degraded', provenance: {provider: 'search-service', authority: 'service'}},
  {id: 'authorization.camera', domain: 'authorization', state: 'permission-required', provenance: {provider: 'platform-permissions', authority: 'platform'}},
  {id: 'application.admin', domain: 'application', state: 'restricted', provenance: {provider: 'policy-engine', authority: 'policy'}},
  {id: 'connectivity.network', domain: 'connectivity', state: 'offline', provenance: {provider: 'network-adapter', authority: 'platform'}}
]);
assert.equal(resolveGlazeCapability(capabilities, 'service.search').availableForInvocation, true);
assert.equal(resolveGlazeCapability(capabilities, 'missing.capability').state, 'unknown');

const actions = resolveCapabilityAwareActions([
  {id: 'search', label: 'Search', primary: true, requiredCapabilities: ['service.search']},
  {id: 'camera', label: 'Camera', requiredCapabilities: ['authorization.camera'], consequential: true},
  {id: 'admin', label: 'Admin', requiredCapabilities: ['application.admin']},
  {id: 'sync', label: 'Sync', requiredCapabilities: ['connectivity.network']},
  {id: 'unknown', label: 'Unknown', requiredCapabilities: ['missing.capability']}
], capabilities);
assert.deepEqual(actions.map(action => action.id), ['search', 'camera', 'admin', 'sync', 'unknown']);
assert.equal(actions[0].enabled, true);
assert.equal(actions[0].degraded, true);
assert.equal(actions[1].enabled, false);
assert.equal(actions[1].recovery, 'request-permission-user-initiated');
assert.equal(actions[1].permissionRequestedAutomatically, false);
assert.equal(actions[1].automaticExecutionAllowed, false);
assert.ok(actions[2].reasonCodes.includes('restricted-by-authority'));
assert.ok(actions[3].reasonCodes.includes('offline'));
assert.ok(actions[4].reasonCodes.includes('capability-unknown'));

const opticalCapabilities = mapV141OpticalCapabilities({capabilities: {backdropBlur: false, motion: true}});
assert.equal(opticalCapabilities.find(item => item.id === 'rendering.backdrop-blur').state, 'unsupported');
assert.equal(opticalCapabilities.find(item => item.id === 'rendering.motion').state, 'available');

const forcedColors = resolveGlazeAdaptation({
  context: {layout: {density: 'compact'}},
  accessibility: {forcedColors: true},
  capabilities: opticalCapabilities,
  actions: []
});
assert.equal(forcedColors.optical.mode, 'solid-forced-colors');
assert.equal(forcedColors.optical.motionAllowed, false);
assert.equal(forcedColors.authorizationInferred, false);
assert.equal(forcedColors.primaryActionOrderStable, true);
assert.equal(forcedColors.explanation.privacy.rawContextIncluded, false);
assert.equal(forcedColors.explanation.privacy.capabilityProvidersIncluded, false);
assert.equal(JSON.stringify(forcedColors.explanation).includes('compact'), false);
assert.equal(JSON.stringify(forcedColors.explanation).includes('glaze-v1.4.1-optical-engine'), false);

const stabilizer = createGlazeAdaptationStabilizer({minStableSamples: 2, minDwellMs: 100});
assert.equal(stabilizer.update('a', {mode: 'a'}, 0).accepted, true);
const pendingOne = stabilizer.update('b', {mode: 'b'}, 10);
assert.equal(pendingOne.accepted, false);
assert.equal(pendingOne.pending, true);
const pendingTwo = stabilizer.update('b', {mode: 'b'}, 50);
assert.equal(pendingTwo.accepted, false);
const accepted = stabilizer.update('b', {mode: 'b'}, 120);
assert.equal(accepted.accepted, true);
assert.equal(accepted.changed, true);
assert.equal(accepted.signature, 'b');

const lifecycle = JSON.parse(fs.readFileSync(new URL('../registry/lifecycle.json', import.meta.url), 'utf8'));
assert.equal(lifecycle.currentOfficial, '1.4.1');
assert.equal(lifecycle.currentStable, '1.4.1');
assert.equal(lifecycle.activeCandidate, null);
assert.equal(lifecycle.activePatchReleaseCandidate, null);
const stable = lifecycle.releases.find(item => item.version === '1.4.1');
assert.equal(stable?.status, 'stable');
assert.equal(stable?.consumerEligible, true);

console.log('GLAZE UI 1.5.0-dev.1 context/capability development verification: PASS');
console.log(`Context domains: ${GLAZE_CONTEXT_DOMAINS.length}`);
console.log(`Capability domains: ${GLAZE_CAPABILITY_DOMAINS.length}`);
console.log(`Capability states: ${GLAZE_CAPABILITY_STATES.length}`);
console.log('Stable baseline preserved: 1.4.1');
