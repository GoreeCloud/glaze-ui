#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

import {
  resolveGlazeShellCapability,
  resolveGlazeSystemShellContext,
  resolveGlazeShellTransition,
  resolveGlazeControlCenterContinuity,
  resolveGlazeShellActivityPresentation,
  glazeV17SystemShellContinuityDevelopmentContract
} from '../js/glaze-v1.7-system-shell-continuity.dev.mjs';
import {glazeV17Development} from '../js/glaze-v1.7-development.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const read = rel => fs.readFileSync(path.join(root, rel), 'utf8');
const json = rel => JSON.parse(read(rel));
const assert = (condition, message) => { if (!condition) throw new Error(message); };

const contract = json('contracts/v1.7/system-shell-continuity.dev.json');
const schema = json('schemas/v1.7-system-shell-continuity.schema.json');
const tokens = json('tokens/glaze-v1.7-system-shell-continuity.dev.json');
const lifecycle = json('registry/lifecycle.json');
const stable = read('VERSION').trim();
const spec = read('GLAZE_UI_V1_7_PLANNED.md');

const shellRegions = [
  'workspace','navigation','universal-search','control-center',
  'notification-activity','critical-system'
];
const transitionKinds = [
  'compact-expanded-navigation','split-view','multi-window','window-restoration',
  'application-system-handoff','task-switch','shell-overlay','control-center',
  'search-continuity'
];
const platformCapabilities = [
  'multi-window','split-view','window-restoration','application-system-handoff',
  'task-switch','shell-overlay','persistent-control-center-layout','system-search',
  'notification-activity'
];
const capabilityStates = [
  'available','unavailable','unsupported','restricted','permission-required',
  'temporarily-unavailable','unknown'
];
const activityPriorities = [
  'informational','background','required-attention','warning','critical','progress',
  'recoverable-failure','security','privacy','unknown'
];
const profiles = ['mobile','tablet','desktop','foldable','tv','wearable'];
const presentations = {
  mobile:'compact-shell-stack',
  tablet:'adaptive-split-shell',
  desktop:'workspace-multi-window-shell',
  foldable:'posture-aware-shell',
  tv:'far-view-shell',
  wearable:'glanceable-shell'
};

assert(stable === '1.6.0', 'V1.7 dev.6 must preserve GLAZE UI V1.6 / 1.6.0 as current Stable');
assert(lifecycle.currentOfficial === stable && lifecycle.currentStable === stable, 'VERSION/current Stable authority must agree');
assert(lifecycle.activeCandidate === null, 'V1.7 dev.6 must not create an active Candidate');
assert(lifecycle.activePatchReleaseCandidate === null, 'V1.7 dev.6 must not create a patch RC');
assert(lifecycle.plannedNext === null, 'V1.7 dev.6 must not mutate lifecycle plannedNext');

assert(spec.includes('## 7. System Shell Continuity'), 'V1.7 specification missing System Shell Continuity section');
for (const phrase of [
  'Notification and activity presentation',
  'Control Center continuity',
  'Persistent Control Center layout where supported',
  'Multi-window behavior',
  'Split-view behavior',
  'Compact-to-expanded navigation',
  'Window restoration',
  'Application-to-system handoff',
  'Task switching',
  'Shell overlays',
  'Search continuity',
  'Contextual command surfaces'
]) {
  assert(spec.includes(phrase), `V1.7 specification missing shell requirement: ${phrase}`);
}
assert(spec.includes('A transition between shell configurations must not unnecessarily alter the active task.'), 'active-task shell continuity rule missing');
assert(spec.includes('Navigation and system-shell recomposition must remain predictable and reversible.'), 'predictable/reversible shell rule missing');

assert(fs.existsSync(path.join(root, 'IMPLEMENTED-FEATURES.md')), 'IMPLEMENTED-FEATURES.md is required');
assert(fs.existsSync(path.join(root, 'PLANNED-FEATURES.md')), 'PLANNED-FEATURES.md is required');
assert(fs.existsSync(path.join(root, 'CHANGELOGS.md')), 'CHANGELOGS.md is required');
assert(!fs.existsSync(path.join(root, 'FEATURE-ROADMAP.md')), 'FEATURE-ROADMAP.md must remain retired');
assert(!fs.existsSync(path.join(root, 'CHANGELOG.md')), 'legacy singular CHANGELOG.md must remain retired');

assert(schema.$schema === 'https://json-schema.org/draft/2020-12/schema', 'schema must use JSON Schema 2020-12');
assert(contract.$schema === '../../schemas/v1.7-system-shell-continuity.schema.json', 'contract schema binding mismatch');
assert(contract.version === '1.7.0-dev.6', 'contract version mismatch');
assert(contract.lifecycle === 'Development', 'contract must remain Development');
assert(contract.stableBaseline === '1.6.0', 'contract Stable baseline mismatch');
assert(contract.consumerEligible === false, 'contract must remain non-consumer-eligible');
assert(JSON.stringify(contract.implementedSpecificationSections) === JSON.stringify([7]), 'implemented section set mismatch');
assert(JSON.stringify(contract.shellRegions) === JSON.stringify(shellRegions), 'shell region set mismatch');
assert(JSON.stringify(contract.transitionKinds) === JSON.stringify(transitionKinds), 'shell transition set mismatch');
assert(JSON.stringify(contract.platformCapabilities) === JSON.stringify(platformCapabilities), 'platform capability set mismatch');
assert(JSON.stringify(contract.capabilityStates) === JSON.stringify(capabilityStates), 'capability state set mismatch');
assert(JSON.stringify(contract.profilePresentations) === JSON.stringify(presentations), 'profile shell presentation mismatch');
assert(contract.continuity.activeTaskPreservedUnlessAuthoritativeTaskChange === true, 'active task preservation rule missing');
assert(contract.continuity.navigationPreserved === true, 'navigation continuity missing');
assert(contract.continuity.focusPreserved === true, 'focus continuity missing');
assert(contract.continuity.selectionPreserved === true, 'selection continuity missing');
assert(contract.continuity.draftsPreserved === true, 'draft continuity missing');
assert(contract.continuity.queryAndFiltersPreserved === true, 'query/filter continuity missing');
assert(contract.continuity.paneAndWindowContextPreserved === true, 'pane/window continuity missing');
assert(contract.continuity.safePendingInteractionsPreserved === true, 'pending interaction continuity missing');
assert(contract.continuity.providerOwnedTruthPreserved === true, 'provider truth continuity missing');
assert(contract.continuity.shellReconfigurationMayResetTaskByItself === false, 'shell recomposition must not reset task');
assert(contract.continuity.transitionsPredictable === true, 'shell transitions must be predictable');
assert(contract.continuity.transitionsReversible === true, 'shell transitions must be reversible');
assert(contract.controlCenter.layoutIdentityStable === true, 'Control Center layout identity must be stable');
assert(contract.controlCenter.moduleOrderStableUnlessAuthoritativeLayoutChange === true, 'Control Center module order stability missing');
assert(contract.controlCenter.persistentLayoutOnlyWherePlatformSupportsIt === true, 'persistent Control Center layout must require support');
assert(contract.controlCenter.persistencePerformedByGlaze === false, 'Glaze must not persist Control Center layout');
assert(contract.controlCenter.crossDeviceSyncEstablished === false, 'dev.6 must not claim Control Center sync');
assert(contract.notificationActivityBoundary.shellPresentationSupported === true, 'shell activity presentation boundary missing');
assert(contract.notificationActivityBoundary.fullSection8ComponentSystemEstablished === false, 'dev.6 must not claim section 8 completion');
assert(contract.notificationActivityBoundary.truthOwnedByCallerOrProvider === true, 'activity truth authority missing');
assert(contract.notificationActivityBoundary.truthGeneratedByGlaze === false, 'Glaze must not generate activity truth');
assert(contract.notificationActivityBoundary.priorityInventedByGlaze === false, 'Glaze must not invent activity priority');
assert(contract.notificationActivityBoundary.criticalStateRequiresAuthoritativeSource === true, 'critical activity must require authority');
assert(contract.authority.boundary === 'presentation-only', 'System Shell must remain presentation-only');
assert(contract.authority.windowingSupportCreatedByGlaze === false, 'Glaze must not create windowing support');
assert(contract.authority.systemPrivilegeGrantedByGlaze === false, 'Glaze must not grant system privilege');
assert(contract.authority.notificationTruthCreatedByGlaze === false, 'Glaze must not create notification truth');
assert(contract.authority.searchAuthorityCreatedByGlaze === false, 'Glaze must not create search authority');
assert(contract.authority.navigationExecutedByGlaze === false, 'Glaze must not execute navigation');
assert(contract.authority.handoffExecutedByGlaze === false, 'Glaze must not execute handoff');
assert(contract.authority.windowRestorationExecutedByGlaze === false, 'Glaze must not execute restoration');
assert(contract.authority.taskSwitchExecutedByGlaze === false, 'Glaze must not execute task switch');
assert(contract.authority.persistencePerformedByGlaze === false, 'Glaze must not perform persistence');
assert(contract.authority.consequentialExecutionAutomatic === false, 'Glaze must not auto-execute consequential actions');

assert(tokens.version === '1.7.0-dev.6', 'token map version mismatch');
assert(tokens.lifecycle === 'Development', 'token map must remain Development');
assert(tokens.stableBaseline === '1.6.0', 'token map Stable baseline mismatch');
assert(tokens.consumerEligible === false, 'token map must remain non-consumer-eligible');
assert(Object.keys(tokens.shellRegions).length === 6, 'token map shell-region count mismatch');
assert(Object.keys(tokens.transitionKinds).length === 9, 'token map transition count mismatch');
assert(Object.keys(tokens.profilePresentations).length === 6, 'token map profile presentation count mismatch');
assert(Object.keys(tokens.capabilityRoles).length === 7, 'token map capability role count mismatch');
assert(tokens.continuity.shellReconfigurationMayResetTaskByItself === false, 'token map must prohibit shell task reset');
assert(tokens.continuity.transitionsPredictable === true && tokens.continuity.transitionsReversible === true, 'token map transition guarantees missing');
assert(tokens.controlCenter.persistencePerformedByGlaze === false, 'token map must not persist Control Center layout');
assert(tokens.notificationActivity.fullSection8ComponentSystemEstablished === false, 'token map must not claim section 8 completion');
assert(tokens.notificationActivity.truthGeneratedByGlaze === false, 'token map must not generate activity truth');
assert(tokens.boundaries.windowingSupportCreatedByGlaze === false, 'token map must not create windowing support');
assert(tokens.boundaries.consequentialExecutionAutomatic === false, 'token map must not auto-execute');

for (const source of tokens.sourceAuthorities || []) {
  assert(fs.existsSync(path.join(root, source)), `token source authority missing: ${source}`);
}

for (const capability of platformCapabilities) {
  for (const state of capabilityStates) {
    const resolved = resolveGlazeShellCapability({
      capability,
      state,
      authoritative:true
    });
    assert(resolved.capability === capability, `capability id mismatch: ${capability}`);
    assert(resolved.acceptedState === state, `authoritative capability state mismatch: ${capability}/${state}`);
    assert(resolved.available === (state === 'available'), `available flag mismatch: ${capability}/${state}`);
    assert(resolved.authority.capabilityCreatedByGlaze === false, `Glaze created capability: ${capability}`);
  }
}

const unverifiedCapability = resolveGlazeShellCapability({
  capability:'multi-window',
  state:'available',
  authoritative:false
});
assert(unverifiedCapability.acceptedState === 'unknown', 'unverified available shell capability must fail closed');
assert(unverifiedCapability.available === false, 'unverified shell capability must not be available');
assert(unverifiedCapability.requestedStateWithheldWithoutAuthority === true, 'withheld shell capability must be observable');

for (const profile of profiles) {
  const context = resolveGlazeSystemShellContext({profile});
  assert(context.profile === profile, `shell profile mismatch: ${profile}`);
  assert(context.presentation === presentations[profile], `shell presentation mismatch: ${profile}`);
  assert(context.regions.length === 6, `shell regions missing: ${profile}`);
  assert(context.continuity.shellReconfigurationMayResetTaskByItself === false, `shell task reset allowed: ${profile}`);
  assert(context.capabilities['multi-window'].acceptedState === 'unknown', `default capability must be unknown: ${profile}`);
  assert(context.authority.windowingSupportCreatedByGlaze === false, `windowing support manufactured: ${profile}`);
}

const supportedDesktop = resolveGlazeSystemShellContext({
  profile:'desktop',
  capabilities:{
    'multi-window':{state:'available',authoritative:true},
    'split-view':{state:'available',authoritative:true},
    'persistent-control-center-layout':{state:'available',authoritative:true},
    'system-search':{state:'available',authoritative:true}
  }
});
assert(supportedDesktop.capabilities['multi-window'].available === true, 'authoritative desktop multi-window capability should be presented');
assert(supportedDesktop.capabilities['split-view'].available === true, 'authoritative desktop split-view capability should be presented');
assert(supportedDesktop.composition.multiWindowRequiresAuthoritativeCapability === false, 'available multi-window capability should satisfy shell requirement');
assert(supportedDesktop.composition.contextualCommandSurfaceComponent === 'GlzCommandSurface', 'shell must delegate contextual command surface');

const previousTaskState = {
  navigationDestination:'memos/detail',
  focusId:'memo-title',
  selectionIds:['memo-42'],
  draftText:'shell continuity draft',
  activeFilters:['work'],
  query:'continuity',
  paneState:'detail',
  pendingInteractions:['save-draft'],
  workingContext:{provider:'authoritative'}
};
const stateClasses = {
  navigationDestination:'durable',
  focusId:'session-scoped',
  selectionIds:'session-scoped',
  draftText:'recoverable',
  activeFilters:'durable',
  query:'session-scoped',
  paneState:'presentation-only',
  pendingInteractions:'temporary',
  workingContext:'provider-owned'
};
const previousShellState = {
  activeWindowId:'window-a',
  windowContextKey:'workspace-a',
  splitViewId:'split-a',
  overlayIds:['overlay-a'],
  controlCenterLayoutId:'layout-a',
  searchScope:'application',
  taskSwitchContext:'task-a',
  handoffContext:'device-a'
};

for (const transitionKind of transitionKinds) {
  const resolved = resolveGlazeShellTransition({
    transitionKind,
    previousTaskId:'task-a',
    incomingTaskId:'task-b',
    taskIdentityAuthoritative:false,
    previousShellState,
    incomingShellState:{
      activeWindowId:'window-b',
      searchScope:'system'
    },
    shellStateAuthoritative:false,
    previousTaskState,
    stateClasses
  });
  assert(resolved.transitionKind === transitionKind, `transition kind mismatch: ${transitionKind}`);
  assert(resolved.task.acceptedTaskId === 'task-a', `unauthorized task change accepted: ${transitionKind}`);
  assert(resolved.task.requestedTaskChangeWithheldWithoutAuthority === true, `unauthorized task change not recorded: ${transitionKind}`);
  assert(resolved.shellState.activeWindowId === 'window-a', `unauthorized shell state changed window: ${transitionKind}`);
  assert(resolved.taskState.navigationDestination === 'memos/detail', `navigation lost: ${transitionKind}`);
  assert(resolved.taskState.focusId === 'memo-title', `focus lost: ${transitionKind}`);
  assert(resolved.taskState.selectionIds[0] === 'memo-42', `selection lost: ${transitionKind}`);
  assert(resolved.taskState.draftText === 'shell continuity draft', `draft lost: ${transitionKind}`);
  assert(resolved.taskState.query === 'continuity', `query lost: ${transitionKind}`);
  assert(resolved.taskState.workingContext.provider === 'authoritative', `provider truth lost: ${transitionKind}`);
  assert(resolved.continuity.shellReconfigurationMayResetTaskByItself === false, `shell reset allowed: ${transitionKind}`);
  assert(resolved.continuity.transitionsPredictable === true && resolved.continuity.transitionsReversible === true, `transition guarantees missing: ${transitionKind}`);
  assert(resolved.authority.consequentialExecutionAutomatic === false, `auto execution leaked: ${transitionKind}`);
}

const authoritativeTaskSwitch = resolveGlazeShellTransition({
  transitionKind:'task-switch',
  previousTaskId:'task-a',
  incomingTaskId:'task-b',
  taskIdentityAuthoritative:true,
  previousShellState,
  incomingShellState:{activeWindowId:'window-b',searchScope:'system'},
  shellStateAuthoritative:true,
  previousTaskState,
  stateClasses
});
assert(authoritativeTaskSwitch.task.acceptedTaskId === 'task-b', 'authoritative task switch should accept caller-owned task change');
assert(authoritativeTaskSwitch.task.taskIdentityChanged === true, 'authoritative task switch marker missing');
assert(authoritativeTaskSwitch.shellState.activeWindowId === 'window-b', 'authoritative shell-state update should be accepted');
assert(authoritativeTaskSwitch.shellState.searchScope === 'system', 'authoritative search scope should be accepted');
assert(authoritativeTaskSwitch.authority.taskSwitchExecutedByGlaze === false, 'Glaze must not execute task switch');

const ccUnverified = resolveGlazeControlCenterContinuity({
  previousModuleIds:['wifi','bluetooth','brightness'],
  incomingModuleIds:['brightness','wifi','bluetooth'],
  layoutAuthoritative:false,
  requestedPersistentLayout:true,
  persistenceCapabilityState:'available',
  persistenceCapabilityAuthoritative:false
});
assert(ccUnverified.moduleIds.join(',') === 'wifi,bluetooth,brightness', 'unauthorized Control Center reorder must be rejected');
assert(ccUnverified.requestedIncomingOrderWithheldWithoutAuthority === true, 'withheld Control Center order must be observable');
assert(ccUnverified.persistence.effective === 'session-only', 'unverified persistence capability must fail closed to session-only');
assert(ccUnverified.persistence.performedByGlaze === false, 'Glaze must not persist Control Center layout');

const ccPersistent = resolveGlazeControlCenterContinuity({
  previousModuleIds:['wifi','bluetooth','brightness'],
  incomingModuleIds:['brightness','wifi','bluetooth'],
  layoutAuthoritative:true,
  requestedPersistentLayout:true,
  persistenceCapabilityState:'available',
  persistenceCapabilityAuthoritative:true
});
assert(ccPersistent.moduleIds.join(',') === 'brightness,wifi,bluetooth', 'authoritative Control Center reorder should be accepted');
assert(ccPersistent.persistence.effective === 'platform-persistent', 'authoritative persistence capability should allow platform-persistent presentation');
assert(ccPersistent.persistence.performedByGlaze === false, 'platform-persistent presentation must not mean Glaze persisted data');
assert(ccPersistent.persistence.crossDeviceSyncEstablished === false, 'Control Center continuity must not claim cross-device sync');

for (const priority of activityPriorities) {
  const activity = resolveGlazeShellActivityPresentation({
    priority,
    authoritative:true,
    sourceId:'provider-a',
    eventId:`event-${priority}`
  });
  assert(activity.acceptedPriority === priority, `authoritative activity priority mismatch: ${priority}`);
  assert(activity.sourceId === 'provider-a', `authoritative activity source lost: ${priority}`);
  assert(activity.presentation.fullSection8ComponentSystemEstablished === false, `dev.6 overclaimed section 8: ${priority}`);
  assert(activity.authority.truthGeneratedByGlaze === false, `Glaze generated activity truth: ${priority}`);
}

const unverifiedCritical = resolveGlazeShellActivityPresentation({
  priority:'critical',
  authoritative:false,
  sourceId:'provider-a',
  eventId:'event-critical'
});
assert(unverifiedCritical.acceptedPriority === 'unknown', 'unverified critical activity must fail closed to unknown');
assert(unverifiedCritical.sourceId === null && unverifiedCritical.eventId === null, 'unverified activity identity must be withheld');
assert(unverifiedCritical.presentation.criticalPresentationAllowed === false, 'unverified critical activity must not receive critical treatment');

assert(glazeV17SystemShellContinuityDevelopmentContract.version === '1.7.0-dev.6', 'runtime contract version mismatch');
assert(glazeV17SystemShellContinuityDevelopmentContract.lifecycle === 'development', 'runtime contract must remain Development');
assert(glazeV17SystemShellContinuityDevelopmentContract.stableBaseline === '1.6.0', 'runtime Stable baseline mismatch');
assert(glazeV17SystemShellContinuityDevelopmentContract.consumerEligible === false, 'runtime must remain non-consumer-eligible');
assert(glazeV17SystemShellContinuityDevelopmentContract.shellRegions.length === 6, 'runtime shell region count mismatch');
assert(glazeV17SystemShellContinuityDevelopmentContract.transitionKinds.length === 9, 'runtime transition count mismatch');
assert(glazeV17SystemShellContinuityDevelopmentContract.platformCapabilities.length === 9, 'runtime capability count mismatch');
assert(glazeV17SystemShellContinuityDevelopmentContract.capabilityStates.length === 7, 'runtime capability-state count mismatch');
assert(glazeV17SystemShellContinuityDevelopmentContract.fullSection8ComponentSystemEstablished === false, 'runtime must not claim section 8 completion');
assert(glazeV17SystemShellContinuityDevelopmentContract.nativeShellParityEstablished === false, 'runtime must not claim native shell parity');
assert(glazeV17SystemShellContinuityDevelopmentContract.presentationOnly === true, 'runtime must remain presentation-only');

assert(glazeV17Development.version === '1.7.0-dev.6', 'aggregate version mismatch');
assert(glazeV17Development.lifecycle === 'development', 'aggregate must remain Development');
assert(glazeV17Development.stableBaseline === '1.6.0', 'aggregate Stable baseline mismatch');
assert(glazeV17Development.consumerEligible === false, 'aggregate must remain non-consumer-eligible');
assert(JSON.stringify(glazeV17Development.implementedSpecificationSections) === JSON.stringify([1,2,3,4,5,6,7]), 'aggregate section set mismatch');
assert(glazeV17Development.taskContinuityFoundation === 'js/glaze-v1.7-task-continuity.dev.mjs', 'aggregate lost Task Continuity');
assert(glazeV17Development.adaptiveInputFoundation === 'js/glaze-v1.7-adaptive-input.dev.mjs', 'aggregate lost Adaptive Input');
assert(glazeV17Development.formFactorProfilesFoundation === 'js/glaze-v1.7-form-factor-profiles.dev.mjs', 'aggregate lost Form-Factor Profiles');
assert(glazeV17Development.commandSurfaceFoundation === 'js/glaze-v1.7-command-surface.dev.mjs', 'aggregate lost Command Surface');
assert(glazeV17Development.personalizationFoundation === 'js/glaze-v1.7-personalization.dev.mjs', 'aggregate lost Personalization');
assert(glazeV17Development.systemShellContinuityFoundation === 'js/glaze-v1.7-system-shell-continuity.dev.mjs', 'aggregate missing System Shell Continuity');

let invalidCapability=false;
try { resolveGlazeShellCapability({capability:'teleportation',state:'available',authoritative:true}); } catch { invalidCapability=true; }
assert(invalidCapability, 'unknown shell capability must fail closed');

let invalidCapabilityState=false;
try { resolveGlazeShellCapability({capability:'multi-window',state:'maybe',authoritative:true}); } catch { invalidCapabilityState=true; }
assert(invalidCapabilityState, 'unknown shell capability state must fail closed');

let invalidTransition=false;
try { resolveGlazeShellTransition({transitionKind:'instant-teleport'}); } catch { invalidTransition=true; }
assert(invalidTransition, 'unknown shell transition must fail closed');

let invalidProfile=false;
try { resolveGlazeSystemShellContext({profile:'spatial'}); } catch { invalidProfile=true; }
assert(invalidProfile, 'non-first-class shell profile must fail closed');

let invalidPriority=false;
try { resolveGlazeShellActivityPresentation({priority:'panic',authoritative:true}); } catch { invalidPriority=true; }
assert(invalidPriority, 'unknown activity priority must fail closed');

console.log('GLAZE UI V1.7 System Shell Continuity Development foundation: PASS');
console.log('Implemented section: 7');
console.log('Shell regions: 6');
console.log('Shell transition kinds: 9');
console.log('Platform capability classes: 9');
console.log('Capability states: 7');
console.log('Activity priorities: 10');
console.log('Full section 8 component system established: false');
console.log('Native shell parity established: false');
console.log('Stable baseline preserved: 1.6.0');
console.log('Consumer eligible: false');
