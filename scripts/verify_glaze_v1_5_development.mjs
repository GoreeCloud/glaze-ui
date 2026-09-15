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
import {
  createGlazeProviderSnapshot,
  providerSnapshotSummary,
  glazeProviderDevelopmentContract
} from '../js/glaze-v1.5-provider-registry.dev.mjs';
import {
  resolveGlazeComposition,
  resolveGlazeNavigation,
  resolveGlazeControlPresentation,
  glazeCompositionDevelopmentContract
} from '../js/glaze-v1.5-composition.dev.mjs';

const development = JSON.parse(fs.readFileSync(new URL('../registry/development/glaze-v1.5.0-dev.1.json', import.meta.url), 'utf8'));
const contract = JSON.parse(fs.readFileSync(new URL('../contracts/v1.5/context-capability.dev.json', import.meta.url), 'utf8'));
const conformance = JSON.parse(fs.readFileSync(new URL('../conformance/v1.5-development-matrix.json', import.meta.url), 'utf8'));

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
assert.equal(glazeProviderDevelopmentContract.providerPrecedenceInferred, false);
assert.equal(glazeCompositionDevelopmentContract.automaticNavigationAllowed, false);

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

const expectedInvocation = new Map([
  ['supported', false],
  ['available', true],
  ['degraded', true],
  ['temporarily-unavailable', false],
  ['offline', false],
  ['permission-required', false],
  ['restricted', false],
  ['unsupported', false],
  ['disabled', false],
  ['unknown', false]
]);
for (const state of GLAZE_CAPABILITY_STATES) {
  const record = normalizeGlazeCapability({
    id: `state.${state}`,
    domain: 'application',
    state,
    provenance: state === 'unknown' ? undefined : {provider: 'state-verifier', authority: 'application'}
  });
  assert.equal(record.state, state);
  assert.equal(record.availableForInvocation, expectedInvocation.get(state));
}

const missingProvenance = normalizeGlazeCapability({id: 'service.search', domain: 'service', state: 'available'});
assert.equal(missingProvenance.state, 'unknown');
assert.equal(missingProvenance.availableForInvocation, false);
assert.ok(missingProvenance.reasonCodes.includes('missing-provenance-failed-closed'));

const capabilities = normalizeGlazeCapabilities([
  {id: 'service.search', domain: 'service', state: 'degraded', provenance: {provider: 'search-service', authority: 'service'}},
  {id: 'authorization.camera', domain: 'authorization', state: 'permission-required', provenance: {provider: 'platform-permissions', authority: 'platform'}},
  {id: 'application.admin', domain: 'application', state: 'restricted', provenance: {provider: 'policy-engine', authority: 'policy'}},
  {id: 'connectivity.network', domain: 'connectivity', state: 'offline', provenance: {provider: 'network-adapter', authority: 'platform'}},
  {id: 'device.cast', domain: 'device', state: 'unsupported', provenance: {provider: 'device-adapter', authority: 'platform'}},
  {id: 'service.export', domain: 'service', state: 'temporarily-unavailable', provenance: {provider: 'export-service', authority: 'service'}},
  {id: 'application.experimental', domain: 'application', state: 'disabled', provenance: {provider: 'app-runtime', authority: 'application'}}
]);
assert.equal(resolveGlazeCapability(capabilities, 'service.search').availableForInvocation, true);
assert.equal(resolveGlazeCapability(capabilities, 'missing.capability').state, 'unknown');

const actions = resolveCapabilityAwareActions([
  {id: 'search', label: 'Search', primary: true, requiredCapabilities: ['service.search']},
  {id: 'camera', label: 'Camera', requiredCapabilities: ['authorization.camera'], consequential: true},
  {id: 'admin', label: 'Admin', requiredCapabilities: ['application.admin']},
  {id: 'sync', label: 'Sync', requiredCapabilities: ['connectivity.network']},
  {id: 'cast', label: 'Cast', requiredCapabilities: ['device.cast']},
  {id: 'export', label: 'Export', requiredCapabilities: ['service.export']},
  {id: 'experimental', label: 'Experimental', requiredCapabilities: ['application.experimental']},
  {id: 'unknown', label: 'Unknown', requiredCapabilities: ['missing.capability']}
], capabilities);
assert.deepEqual(actions.map(action => action.id), ['search', 'camera', 'admin', 'sync', 'cast', 'export', 'experimental', 'unknown']);
assert.equal(actions[0].enabled, true);
assert.equal(actions[0].degraded, true);
assert.equal(actions[1].enabled, false);
assert.equal(actions[1].recovery, 'request-permission-user-initiated');
assert.equal(actions[1].permissionRequestedAutomatically, false);
assert.equal(actions[1].automaticExecutionAllowed, false);
assert.ok(actions[2].reasonCodes.includes('restricted-by-authority'));
assert.ok(actions[3].reasonCodes.includes('offline'));
assert.ok(actions[4].reasonCodes.includes('unsupported'));
assert.ok(actions[5].reasonCodes.includes('temporarily-unavailable'));
assert.ok(actions[6].reasonCodes.includes('disabled'));
assert.ok(actions[7].reasonCodes.includes('capability-unknown'));

const providerSnapshot = createGlazeProviderSnapshot([
  {
    id: 'platform-context',
    authority: 'platform',
    context: {input: {primary: 'touch'}, 'device-posture': {posture: 'folded'}},
    capabilities: [
      {id: 'device.cast', domain: 'device', state: 'unsupported'},
      {id: 'connectivity.network', domain: 'connectivity', state: 'available'}
    ]
  },
  {
    id: 'search-service',
    authority: 'service',
    context: {connectivity: {class: 'online'}},
    capabilities: [{id: 'service.search', domain: 'service', state: 'available'}]
  }
]);
assert.deepEqual([...providerSnapshot.context.availableDomains].sort(), ['connectivity', 'device-posture', 'input']);
assert.equal(providerSnapshot.capabilities.byId['service.search'].state, 'available');
assert.equal(providerSnapshot.providerPrecedenceInferred, false);
const providerSummary = providerSnapshotSummary(providerSnapshot);
assert.equal(providerSummary.providerIdsIncluded, false);
assert.equal(JSON.stringify(providerSummary).includes('search-service'), false);

assert.throws(() => createGlazeProviderSnapshot([{
  id: 'app',
  authority: 'application',
  capabilities: [{id: 'application.edit', domain: 'application', state: 'available', provenance: {provider: 'other'}}]
}]), /cannot impersonate/);

const contextConflict = createGlazeProviderSnapshot([
  {id: 'one', authority: 'application', context: {task: {kind: 'reading'}}},
  {id: 'two', authority: 'application', context: {task: {kind: 'composing'}}}
]);
assert.deepEqual(contextConflict.conflicts.contextDomains, ['task']);
assert.equal(contextConflict.context.domains.task, undefined);

const capabilityConflict = createGlazeProviderSnapshot([
  {id: 'one', authority: 'service', capabilities: [{id: 'service.shared', domain: 'service', state: 'available'}]},
  {id: 'two', authority: 'service', capabilities: [{id: 'service.shared', domain: 'service', state: 'degraded'}]}
]);
assert.deepEqual(capabilityConflict.conflicts.capabilityIds, ['service.shared']);
assert.equal(resolveGlazeCapability(capabilityConflict.capabilities, 'service.shared').state, 'unknown');

const compactTouch = resolveGlazeComposition({context: {layout: {category: 'compact'}, input: {primary: 'touch'}}, intent: {supportsMultiPane: true}});
assert.equal(compactTouch.paneMode, 'single-pane');
assert.equal(compactTouch.controlDensity, 'comfortable');
assert.equal(compactTouch.commandSurface, 'direct-controls');
assert.equal(compactTouch.actionOrderingPolicy, 'preserve-author-order');

const desktop = resolveGlazeComposition({context: {layout: {category: 'expanded'}, input: {primary: 'pointer'}}, intent: {supportsMultiPane: true}});
assert.equal(desktop.paneMode, 'multi-pane');
assert.equal(desktop.controlDensity, 'dense');
assert.equal(desktop.commandSurface, 'toolbar-and-shortcuts');

const remote = resolveGlazeComposition({context: {layout: {category: 'expanded'}, input: {primary: 'remote'}}});
assert.equal(remote.navigationMode, 'focus-navigation');
assert.equal(remote.controlDensity, 'spacious');

const unfolded = resolveGlazeComposition({context: {'device-posture': {posture: 'unfolded'}}, intent: {supportsMultiPane: true}});
assert.equal(unfolded.paneMode, 'multi-pane');
assert.equal(unfolded.taskStateReset, false);

const navigation = resolveGlazeNavigation({
  currentId: 'cast',
  capabilities,
  destinations: [
    {id: 'home', label: 'Home'},
    {id: 'cast', label: 'Cast', capabilityId: 'device.cast', visibilityPolicy: 'omit-unsupported', fallbackId: 'home'},
    {id: 'admin', label: 'Admin', capabilityId: 'application.admin'},
    {id: 'sync', label: 'Sync', capabilityId: 'connectivity.network'}
  ]
});
assert.deepEqual(navigation.visibleDestinationIds, ['home', 'admin', 'sync']);
assert.equal(navigation.destinations.find(item => item.id === 'admin').visible, true);
assert.equal(navigation.destinations.find(item => item.id === 'admin').enabled, false);
assert.equal(navigation.destinations.find(item => item.id === 'sync').visible, true);
assert.equal(navigation.acceptedCurrentId, 'home');
assert.equal(navigation.currentDestinationChanged, true);
assert.equal(navigation.taskStateReset, false);
assert.equal(navigation.automaticNavigationAllowed, false);

const controls = resolveGlazeControlPresentation([
  {id: 'camera', requiredCapabilities: ['authorization.camera'], consequential: true},
  {id: 'search', requiredCapabilities: ['service.search']}
], capabilities);
assert.equal(controls[0].presentationState, 'permission-required');
assert.equal(controls[0].enabled, false);
assert.equal(controls[0].permissionRequestedAutomatically, false);
assert.equal(controls[1].presentationState, 'degraded');
assert.equal(controls[1].explanationRequired, true);

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

const reducedTransparency = resolveGlazeAdaptation({
  accessibility: {reducedTransparency: true, reducedMotion: true},
  capabilities: mapV141OpticalCapabilities({capabilities: {backdropBlur: true, motion: true}}),
  actions: []
});
assert.equal(reducedTransparency.optical.mode, 'solid-reduced-transparency');
assert.equal(reducedTransparency.optical.motionAllowed, false);

const runtimeDowngrade = resolveGlazeAdaptation({capabilities: opticalCapabilities, actions: []});
assert.equal(runtimeDowngrade.optical.mode, 'solid-fallback');

const touchComposition = resolveGlazeComposition({context: {input: {primary: 'touch'}}});
const pointerComposition = resolveGlazeComposition({context: {input: {primary: 'pointer'}, layout: {category: 'expanded'}}});
assert.notEqual(touchComposition.commandSurface, pointerComposition.commandSurface);
assert.equal(touchComposition.pageReloadRequired, false);
assert.equal(pointerComposition.pageReloadRequired, false);

const foldedComposition = resolveGlazeComposition({context: {'device-posture': {posture: 'folded'}}, intent: {supportsMultiPane: true}});
const unfoldedComposition = resolveGlazeComposition({context: {'device-posture': {posture: 'unfolded'}}, intent: {supportsMultiPane: true}});
assert.equal(foldedComposition.paneMode, 'single-pane');
assert.equal(unfoldedComposition.paneMode, 'multi-pane');
assert.equal(unfoldedComposition.taskStateReset, false);

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

assert.equal(conformance.version, '1.5.0-dev.1');
assert.equal(conformance.lifecycle, 'development');
assert.equal(conformance.humanOrTargetRuntimeAcceptanceEstablished, false);
assert.equal(conformance.promotionBoundary.machineCoverageAloneQualifiesReleaseCandidate, false);
assert.equal(conformance.promotionBoundary.machineCoverageAloneQualifiesStable, false);
const scenarioIds = new Set(conformance.scenarios.map(scenario => scenario.id));
const requiredScenarioIds = [
  ...GLAZE_CAPABILITY_STATES.map(state => `capability.${state}`),
  'provenance.missing-fails-closed',
  'provenance.impersonation-rejected',
  'provider.duplicate-capability-fails-closed',
  'provider.duplicate-context-fails-closed',
  'composition.compact-touch',
  'composition.desktop-pointer-keyboard',
  'composition.remote-focus',
  'composition.unfolded-multipane',
  'navigation.unsupported-omit',
  'navigation.restricted-visible',
  'navigation.offline-visible',
  'navigation.continuity-on-removal',
  'accessibility.forced-colors-authority',
  'accessibility.reduced-transparency-authority',
  'adaptation.anti-jitter',
  'privacy.sensitive-context-rejected',
  'privacy.diagnostics-minimized',
  'runtime.optical-downgrade',
  'input.method-transition',
  'posture.fold-transition'
];
for (const scenarioId of requiredScenarioIds) assert.ok(scenarioIds.has(scenarioId), `Missing conformance scenario: ${scenarioId}`);
assert.ok(conformance.scenarios.every(scenario => scenario.machineCovered === true));
assert.ok(conformance.scenarios.some(scenario => scenario.externalAcceptanceRequired === true));

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
console.log(`Development conformance scenarios: ${conformance.scenarios.length}`);
console.log('Provider collisions: fail closed');
console.log('Composition/navigation continuity: verified');
console.log('Stable baseline preserved: 1.4.1');
