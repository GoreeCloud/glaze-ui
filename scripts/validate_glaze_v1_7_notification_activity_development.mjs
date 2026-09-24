import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {
  resolveGlazeNotificationActivitySurface,
  glazeV17NotificationActivityDevelopmentContract
} from '../js/glaze-v1.7-notification-activity.dev.mjs';
import {glazeV17Development} from '../js/glaze-v1.7-development.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const contract = JSON.parse(fs.readFileSync(
  path.join(root, 'contracts/v1.7/notification-activity.dev.json'),
  'utf8'
));
const tokens = JSON.parse(fs.readFileSync(
  path.join(root, 'tokens/glaze-v1.7-notification-activity.dev.json'),
  'utf8'
));

const components = [
  'GlzNotificationSurface',
  'GlzActivityItem',
  'GlzActivityGroup',
  'GlzStatusFeed',
  'GlzBackgroundTask',
  'GlzProgressSurface'
];
const states = [
  'informational-activity',
  'background-work',
  'required-attention',
  'warning',
  'critical-state',
  'user-requested-progress',
  'recoverable-failure',
  'security-state',
  'privacy-state'
];
const profiles = ['mobile','tablet','desktop','foldable','tv','wearable'];

assert.equal(contract.version, '1.7.0-dev.7');
assert.equal(contract.lifecycle, 'Development');
assert.equal(contract.stableBaseline, '1.6.0');
assert.equal(contract.consumerEligible, false);
assert.deepEqual(contract.implementedSpecificationSections, [8]);
assert.deepEqual(contract.components, components);
assert.deepEqual(contract.semanticStates, states);
assert.deepEqual(
  contract.protectedSemanticStates,
  ['warning','critical-state','security-state','privacy-state']
);
assert.equal(contract.truthRequirements.providerTruthRequired, true);
assert.equal(contract.truthRequirements.sourceIdentityRequired, true);
assert.equal(contract.truthRequirements.securityStateMustBeSupplied, true);
assert.equal(contract.truthRequirements.privacyStateMustBeSupplied, true);
assert.equal(contract.presentationRules.colorAloneSufficient, false);
assert.equal(contract.presentationRules.readableTextRequired, true);
assert.equal(contract.presentationRules.groupingMayChangeProviderTruth, false);
assert.equal(contract.authority.boundary, 'presentation-only');

for (const denied of [
  'notificationPostedByGlaze',
  'activityGeneratedByGlaze',
  'backgroundWorkStartedByGlaze',
  'backgroundWorkStoppedByGlaze',
  'progressGeneratedByGlaze',
  'securityStateInferredByGlaze',
  'privacyStateInferredByGlaze',
  'dismissalExecutedByGlaze',
  'actionExecutedByGlaze',
  'persistencePerformedByGlaze',
  'crossDeviceSyncEstablished',
  'consequentialExecutionAutomatic'
]) {
  assert.equal(contract.authority[denied], false, `authority boundary weakened: ${denied}`);
}

for (const source of Object.values(contract.integrationFoundations)) {
  assert.equal(fs.existsSync(path.join(root, source)), true, `missing integration foundation: ${source}`);
}

assert.equal(tokens.version, '1.7.0-dev.7');
assert.equal(tokens.lifecycle, 'Development');
assert.equal(tokens.stableBaseline, '1.6.0');
assert.equal(tokens.consumerEligible, false);
assert.equal(Object.keys(tokens.components).length, 6);
assert.equal(Object.keys(tokens.semanticStates).length, 9);
assert.equal(Object.keys(tokens.presentationByProfile).length, 6);
assert.equal(tokens.accessibility.colorAloneSufficient, false);
assert.equal(tokens.accessibility.readableTextRequired, true);
assert.equal(tokens.boundaries.presentationOnly, true);
assert.equal(tokens.boundaries.securityPrivacyTruthInferredByGlaze, false);

const previousTaskState = {
  navigationDestination: 'activity',
  focusId: 'activity-row-2',
  selectionIds: ['task-7'],
  draftText: 'note draft',
  activeFilters: ['running'],
  query: 'backup',
  paneState: {mode: 'split', activePane: 'detail'},
  pendingInteractions: [{id: 'open-task', safe: true}],
  workingContext: {task: 'status'}
};

const trustedProgress = resolveGlazeNotificationActivitySurface({
  component: 'GlzProgressSurface',
  itemId: 'backup-7',
  sourceId: 'everkeep',
  semanticState: 'user-requested-progress',
  truthAuthoritative: true,
  title: 'Backup',
  body: 'Copying selected data',
  progress: 0.42,
  progressAuthoritative: true,
  actions: [{id: 'cancel', label: 'Cancel', available: true}],
  actionAvailabilityAuthoritative: true,
  dismissible: false,
  profile: 'mobile',
  previousTaskState
});
assert.equal(trustedProgress.presentation.presentable, true);
assert.equal(trustedProgress.providerTruth.acceptedState, 'user-requested-progress');
assert.equal(trustedProgress.progress.value, 0.42);
assert.equal(trustedProgress.progress.generatedByGlaze, false);
assert.equal(trustedProgress.actions[0].available, true);
assert.equal(trustedProgress.actions[0].executionPerformedByGlaze, false);
assert.equal(trustedProgress.taskState.draftText, 'note draft');
assert.equal(trustedProgress.continuity.itemIdentityPreserved, true);
assert.equal(trustedProgress.authority.backgroundWorkStartedByGlaze, false);

const untrustedSecurity = resolveGlazeNotificationActivitySurface({
  component: 'GlzNotificationSurface',
  itemId: 'security-1',
  sourceId: 'wardveil',
  semanticState: 'security-state',
  truthAuthoritative: false,
  title: 'Protected',
  profile: 'desktop'
});
assert.equal(untrustedSecurity.presentation.presentable, false);
assert.equal(untrustedSecurity.providerTruth.acceptedState, null);
assert.equal(untrustedSecurity.providerTruth.title, null);
assert.equal(untrustedSecurity.providerTruth.securityStateInferredByGlaze, false);
assert.equal(untrustedSecurity.presentation.unavailableTruthExplanationRequired, true);

const untrustedAction = resolveGlazeNotificationActivitySurface({
  component: 'GlzActivityItem',
  itemId: 'task-1',
  sourceId: 'service',
  semanticState: 'recoverable-failure',
  truthAuthoritative: true,
  title: 'Retry available',
  actions: [{id: 'retry', label: 'Retry', available: true}],
  actionAvailabilityAuthoritative: false,
  profile: 'tablet'
});
assert.equal(untrustedAction.actions[0].available, false);
assert.equal(untrustedAction.actions[0].requestedAvailabilityWithheldWithoutAuthority, true);
assert.equal(untrustedAction.authority.actionExecutedByGlaze, false);

const untrustedProgress = resolveGlazeNotificationActivitySurface({
  component: 'GlzBackgroundTask',
  itemId: 'task-2',
  sourceId: 'worker',
  semanticState: 'background-work',
  truthAuthoritative: true,
  title: 'Working',
  progress: 0.7,
  progressAuthoritative: false,
  profile: 'wearable'
});
assert.equal(untrustedProgress.progress.value, null);
assert.equal(untrustedProgress.progress.withheldWithoutAuthority, true);

for (const state of states) {
  const resolved = resolveGlazeNotificationActivitySurface({
    component: 'GlzStatusFeed',
    itemId: `state-${state}`,
    sourceId: 'test-provider',
    semanticState: state,
    truthAuthoritative: true,
    title: state,
    profile: 'mobile'
  });
  assert.equal(resolved.providerTruth.acceptedState, state);
  assert.equal(resolved.presentation.colorAloneSufficient, false);
  assert.equal(resolved.authority.presentationOnly, true);
}

for (const profile of profiles) {
  const resolved = resolveGlazeNotificationActivitySurface({
    component: 'GlzActivityItem',
    itemId: `profile-${profile}`,
    sourceId: 'test-provider',
    semanticState: 'informational-activity',
    truthAuthoritative: true,
    title: 'Information',
    profile
  });
  assert.equal(resolved.profile, profile);
  assert.equal(resolved.presentation.semanticIdentityPreserved, true);
}

for (const [field,value] of [
  ['component','GlzInventedSurface'],
  ['semanticState','success-ish'],
  ['profile','spatial']
]) {
  let failed = false;
  try {
    resolveGlazeNotificationActivitySurface({
      component: 'GlzActivityItem',
      itemId: 'invalid',
      sourceId: 'provider',
      semanticState: 'informational-activity',
      truthAuthoritative: true,
      title: 'Invalid',
      profile: 'mobile',
      [field]: value
    });
  } catch {
    failed = true;
  }
  assert.equal(failed, true, `unknown value must fail closed: ${field}=${value}`);
}

let invalidProgress = false;
try {
  resolveGlazeNotificationActivitySurface({
    component: 'GlzProgressSurface',
    itemId: 'bad-progress',
    sourceId: 'provider',
    semanticState: 'user-requested-progress',
    truthAuthoritative: true,
    title: 'Invalid progress',
    progress: 1.5,
    progressAuthoritative: true,
    profile: 'mobile'
  });
} catch {
  invalidProgress = true;
}
assert.equal(invalidProgress, true, 'out-of-range progress must fail closed');

assert.equal(glazeV17NotificationActivityDevelopmentContract.version, '1.7.0-dev.7');
assert.equal(glazeV17NotificationActivityDevelopmentContract.components.length, 6);
assert.equal(glazeV17NotificationActivityDevelopmentContract.semanticStates.length, 9);
assert.equal(glazeV17NotificationActivityDevelopmentContract.presentationOnly, true);
assert.equal(glazeV17NotificationActivityDevelopmentContract.notificationPostedByGlaze, false);

assert.equal(glazeV17Development.version, '1.7.0-dev.7');
assert.equal(glazeV17Development.lifecycle, 'development');
assert.equal(glazeV17Development.stableBaseline, '1.6.0');
assert.equal(glazeV17Development.consumerEligible, false);
assert.deepEqual(glazeV17Development.implementedSpecificationSections, [1,2,3,4,5,6,7,8]);
assert.equal(
  glazeV17Development.notificationActivityFoundation,
  'js/glaze-v1.7-notification-activity.dev.mjs'
);

console.log('GLAZE UI V1.7 Notification and Activity Surfaces Development foundation: PASS');
console.log('Implemented section: 8');
console.log('Components: 6');
console.log('Semantic states: 9');
console.log('Stable baseline preserved: 1.6.0');
console.log('Consumer eligible: false');
