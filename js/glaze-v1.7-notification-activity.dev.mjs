/* GLAZE UI V1.7 — Notification and Activity Surfaces Development foundation.
 *
 * Development-only presentation resolver. GLAZE UI V1.6 / 1.6.0 remains
 * the current Official Stable consumer target.
 */

import {resolveGlazeTaskContinuity} from './glaze-v1.7-task-continuity.dev.mjs';
import {
  resolveGlazeFormFactorProfile,
  glazeV17FormFactorProfilesDevelopmentContract
} from './glaze-v1.7-form-factor-profiles.dev.mjs';

const COMPONENTS = Object.freeze([
  'GlzNotificationSurface',
  'GlzActivityItem',
  'GlzActivityGroup',
  'GlzStatusFeed',
  'GlzBackgroundTask',
  'GlzProgressSurface'
]);

const SEMANTIC_STATES = Object.freeze([
  'informational-activity',
  'background-work',
  'required-attention',
  'warning',
  'critical-state',
  'user-requested-progress',
  'recoverable-failure',
  'security-state',
  'privacy-state'
]);

const PROTECTED_STATES = Object.freeze([
  'warning',
  'critical-state',
  'security-state',
  'privacy-state'
]);

const ATTENTION_BY_STATE = Object.freeze({
  'informational-activity': 'passive',
  'background-work': 'ongoing',
  'required-attention': 'attention',
  warning: 'warning',
  'critical-state': 'critical',
  'user-requested-progress': 'ongoing',
  'recoverable-failure': 'attention',
  'security-state': 'attention',
  'privacy-state': 'attention'
});

const PROFILE_PRESENTATION = Object.freeze({
  mobile: 'compact-notification-activity',
  tablet: 'adaptive-notification-activity',
  desktop: 'windowed-notification-activity',
  foldable: 'posture-aware-notification-activity',
  tv: 'far-view-notification-activity',
  wearable: 'glanceable-notification-activity'
});

function plainObject(value) {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) return false;
  const proto = Object.getPrototypeOf(value);
  return proto === Object.prototype || proto === null;
}

function requiredText(value, label, max = 200) {
  const normalized = String(value ?? '').trim();
  if (!normalized) throw new TypeError(`${label} is required`);
  if (normalized.length > max) throw new RangeError(`${label} exceeds ${max} characters`);
  return normalized;
}

function optionalText(value, max = 1000) {
  if (value == null) return null;
  const normalized = String(value).trim();
  if (!normalized) return null;
  if (normalized.length > max) throw new RangeError(`text exceeds ${max} characters`);
  return normalized;
}

function member(value, allowed, label) {
  const normalized = String(value ?? '').trim();
  if (!allowed.includes(normalized)) throw new RangeError(`Unsupported ${label}: ${normalized}`);
  return normalized;
}

function normalizeProgress(value, authoritative) {
  if (value == null) {
    return Object.freeze({
      requested: false,
      authoritative: authoritative === true,
      value: null,
      withheldWithoutAuthority: false
    });
  }
  if (typeof value !== 'number' || !Number.isFinite(value) || value < 0 || value > 1) {
    throw new RangeError('progress must be a finite number from 0 through 1');
  }
  if (authoritative !== true) {
    return Object.freeze({
      requested: true,
      authoritative: false,
      value: null,
      withheldWithoutAuthority: true
    });
  }
  return Object.freeze({
    requested: true,
    authoritative: true,
    value,
    withheldWithoutAuthority: false
  });
}

function normalizeActions(actions, availabilityAuthoritative) {
  if (actions == null) return Object.freeze([]);
  if (!Array.isArray(actions)) throw new TypeError('actions must be an array');
  return Object.freeze(actions.slice(0, 8).map((action, index) => {
    if (!plainObject(action)) throw new TypeError(`action ${index} must be a plain object`);
    const id = requiredText(action.id, `action ${index} id`, 80);
    const label = requiredText(action.label, `action ${index} label`, 120);
    const requestedAvailable = action.available === true;
    return Object.freeze({
      id,
      label,
      requestedAvailable,
      available: availabilityAuthoritative === true && requestedAvailable,
      availabilityAuthoritative: availabilityAuthoritative === true,
      requestedAvailabilityWithheldWithoutAuthority:
        requestedAvailable && availabilityAuthoritative !== true,
      executionPerformedByGlaze: false
    });
  }));
}

export function resolveGlazeNotificationActivitySurface(input = {}) {
  if (!plainObject(input)) {
    throw new TypeError('Notification/activity input must be a plain object');
  }

  const component = member(input.component, COMPONENTS, 'notification/activity component');
  const profile = member(
    input.profile,
    glazeV17FormFactorProfilesDevelopmentContract.profiles,
    'form-factor profile'
  );

  const itemId = requiredText(input.itemId, 'itemId', 160);
  const sourceId = requiredText(input.sourceId, 'sourceId', 160);
  const requestedState = member(input.semanticState, SEMANTIC_STATES, 'notification/activity state');
  const truthAuthoritative = input.truthAuthoritative === true;
  const acceptedState = truthAuthoritative ? requestedState : null;
  const title = truthAuthoritative ? requiredText(input.title, 'title', 240) : null;
  const body = truthAuthoritative ? optionalText(input.body, 2000) : null;
  const progress = normalizeProgress(input.progress, input.progressAuthoritative);
  const actions = normalizeActions(input.actions, input.actionAvailabilityAuthoritative);

  const dismissalRequested = input.dismissible === true;
  const dismissalAvailable =
    dismissalRequested && input.dismissalAvailabilityAuthoritative === true;

  const profileResolution = resolveGlazeFormFactorProfile({
    profile,
    posture: input.posture,
    accessibilityProfiles: input.accessibilityProfiles,
    availableInputs: input.availableInputs,
    inputCapabilityAuthoritative: input.inputCapabilityAuthoritative,
    unsafeRegionIds: input.unsafeRegionIds,
    semanticSurfaceId: itemId,
    surfaceRole: 'status',
    constrained: input.constrained
  });

  const continuity = resolveGlazeTaskContinuity({
    environmentChange: 'multi-pane-recomposition',
    previous: input.previousTaskState,
    incoming: input.incomingTaskState,
    stateClasses: input.stateClasses,
    clearFields: input.clearFields,
    clearAuthoritative: input.clearAuthoritative,
    temporaryDisposableFields: input.temporaryDisposableFields,
    lossDirectedFields: input.lossDirectedFields,
    providerAuthoritativeFields: input.providerAuthoritativeFields,
    recoveryStateFields: input.recoveryStateFields
  });

  const protectedState = acceptedState != null && PROTECTED_STATES.includes(acceptedState);
  const stateRequiresProgress =
    acceptedState === 'user-requested-progress' || component === 'GlzProgressSurface';

  return Object.freeze({
    version: '1.7.0-dev.7',
    lifecycle: 'development',
    stableBaseline: '1.6.0',
    consumerEligible: false,
    component,
    itemId,
    sourceId,
    profile,
    providerTruth: Object.freeze({
      requestedState,
      acceptedState,
      authoritative: truthAuthoritative,
      withheldWithoutAuthority: !truthAuthoritative,
      title,
      body,
      securityStateInferredByGlaze: false,
      privacyStateInferredByGlaze: false
    }),
    presentation: Object.freeze({
      form: PROFILE_PRESENTATION[profile],
      profileExpectations: profileResolution.expectations,
      presentable: truthAuthoritative,
      semanticIdentityPreserved: true,
      attentionRole: acceptedState ? ATTENTION_BY_STATE[acceptedState] : null,
      protectedSemanticState: protectedState,
      colorAloneSufficient: false,
      readableTextRequired: true,
      stateNameExposed: true,
      unavailableTruthExplanationRequired: !truthAuthoritative
    }),
    progress: Object.freeze({
      ...progress,
      requiredBySemanticPresentation: stateRequiresProgress,
      generatedByGlaze: false
    }),
    actions,
    dismissal: Object.freeze({
      requested: dismissalRequested,
      available: dismissalAvailable,
      availabilityAuthoritative: input.dismissalAvailabilityAuthoritative === true,
      executionPerformedByGlaze: false
    }),
    taskState: continuity.state,
    stateClasses: continuity.stateClasses,
    continuity: Object.freeze({
      ...continuity.continuity,
      itemIdentityPreserved: true,
      sourceIdentityPreserved: true,
      providerTruthPreserved: true,
      taskMayBeResetByPresentationChange: false
    }),
    authority: Object.freeze({
      presentationOnly: true,
      notificationTruthOwnedByProvider: true,
      activityTruthOwnedByProvider: true,
      securityTruthOwnedByProvider: true,
      privacyTruthOwnedByProvider: true,
      notificationPostedByGlaze: false,
      activityGeneratedByGlaze: false,
      backgroundWorkStartedByGlaze: false,
      backgroundWorkStoppedByGlaze: false,
      progressGeneratedByGlaze: false,
      securityStateInferredByGlaze: false,
      privacyStateInferredByGlaze: false,
      dismissalExecutedByGlaze: false,
      actionExecutedByGlaze: false,
      persistencePerformedByGlaze: false,
      crossDeviceSyncEstablished: false,
      consequentialExecutionAutomatic: false
    })
  });
}

export const glazeV17NotificationActivityDevelopmentContract = Object.freeze({
  version: '1.7.0-dev.7',
  lifecycle: 'development',
  stableBaseline: '1.6.0',
  consumerEligible: false,
  components: COMPONENTS,
  semanticStates: SEMANTIC_STATES,
  protectedSemanticStates: PROTECTED_STATES,
  profiles: glazeV17FormFactorProfilesDevelopmentContract.profiles,
  providerTruthRequired: true,
  sourceIdentityRequired: true,
  presentationOnly: true,
  notificationPostedByGlaze: false,
  backgroundExecutionPerformedByGlaze: false,
  securityPrivacyTruthInferredByGlaze: false,
  persistencePerformedByGlaze: false,
  crossDeviceSyncEstablished: false
});
