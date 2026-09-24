/* GLAZE UI V1.7 — System Shell Continuity Development foundation.
 *
 * Development-only shell continuity resolver. GLAZE UI V1.6 / 1.6.0
 * remains the current Official Stable consumer target.
 */

import {resolveGlazeTaskContinuity} from './glaze-v1.7-task-continuity.dev.mjs';
import {resolveGlazeFormFactorProfile} from './glaze-v1.7-form-factor-profiles.dev.mjs';

const SHELL_REGIONS = Object.freeze([
  'workspace',
  'navigation',
  'universal-search',
  'control-center',
  'notification-activity',
  'critical-system'
]);

const TRANSITION_KINDS = Object.freeze([
  'compact-expanded-navigation',
  'split-view',
  'multi-window',
  'window-restoration',
  'application-system-handoff',
  'task-switch',
  'shell-overlay',
  'control-center',
  'search-continuity'
]);

const PLATFORM_CAPABILITIES = Object.freeze([
  'multi-window',
  'split-view',
  'window-restoration',
  'application-system-handoff',
  'task-switch',
  'shell-overlay',
  'persistent-control-center-layout',
  'system-search',
  'notification-activity'
]);

const CAPABILITY_STATES = Object.freeze([
  'available',
  'unavailable',
  'unsupported',
  'restricted',
  'permission-required',
  'temporarily-unavailable',
  'unknown'
]);

const ACTIVITY_PRIORITIES = Object.freeze([
  'informational',
  'background',
  'required-attention',
  'warning',
  'critical',
  'progress',
  'recoverable-failure',
  'security',
  'privacy',
  'unknown'
]);

const PROFILE_PRESENTATIONS = Object.freeze({
  mobile: 'compact-shell-stack',
  tablet: 'adaptive-split-shell',
  desktop: 'workspace-multi-window-shell',
  foldable: 'posture-aware-shell',
  tv: 'far-view-shell',
  wearable: 'glanceable-shell'
});

const TASK_CONTINUITY_CHANGE_BY_SHELL_TRANSITION = Object.freeze({
  'compact-expanded-navigation': 'compact-expanded-layout',
  'split-view': 'multi-pane-recomposition',
  'multi-window': 'multi-pane-recomposition',
  'window-restoration': 'window-resize',
  'application-system-handoff': 'form-factor',
  'task-switch': 'multi-pane-recomposition',
  'shell-overlay': 'multi-pane-recomposition',
  'control-center': 'multi-pane-recomposition',
  'search-continuity': 'compact-expanded-layout'
});

const SHELL_STATE_FIELDS = Object.freeze([
  'activeWindowId',
  'windowContextKey',
  'splitViewId',
  'overlayIds',
  'controlCenterLayoutId',
  'searchScope',
  'taskSwitchContext',
  'handoffContext'
]);

function plainObject(value) {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) return false;
  const proto = Object.getPrototypeOf(value);
  return proto === Object.prototype || proto === null;
}

function semanticId(value, fallback = null) {
  const normalized = String(value ?? '').trim().toLowerCase();
  return normalized || fallback;
}

function requiredId(value, label) {
  const normalized = String(value ?? '').trim();
  if (!normalized) throw new TypeError(`${label} is required`);
  return normalized;
}

function validateMember(value, allowed, label, fallback = null) {
  const normalized = semanticId(value, fallback);
  if (!allowed.includes(normalized)) {
    throw new RangeError(`Unsupported ${label}: ${normalized}`);
  }
  return normalized;
}

function uniqueStrings(values, max = 100) {
  if (!Array.isArray(values)) return Object.freeze([]);
  return Object.freeze(
    [...new Set(values.map(value => String(value ?? '').trim()).filter(Boolean))].slice(0, max)
  );
}

function cloneJsonLike(value) {
  if (value == null) return value;
  if (Array.isArray(value)) return Object.freeze(value.map(cloneJsonLike));
  if (plainObject(value)) {
    const out = {};
    for (const [key, item] of Object.entries(value)) out[key] = cloneJsonLike(item);
    return Object.freeze(out);
  }
  if (['string','number','boolean'].includes(typeof value)) return value;
  throw new TypeError('Shell continuity values must be JSON-like');
}

function normalizeShellState(value) {
  const source = plainObject(value) ? value : {};
  const out = {};
  for (const field of SHELL_STATE_FIELDS) {
    if (field === 'overlayIds') {
      out[field] = uniqueStrings(source[field], 50);
      continue;
    }
    out[field] = source[field] == null ? null : cloneJsonLike(source[field]);
  }
  return Object.freeze(out);
}

function shellStateForTransition(previous, incoming, authoritative) {
  if (!authoritative) return previous;
  const out = {};
  for (const field of SHELL_STATE_FIELDS) {
    if (field === 'overlayIds') {
      out[field] = incoming.overlayIds.length > 0 ? incoming.overlayIds : previous.overlayIds;
      continue;
    }
    out[field] = incoming[field] != null ? incoming[field] : previous[field];
  }
  return Object.freeze(out);
}

export function resolveGlazeShellCapability(input = {}) {
  if (!plainObject(input)) throw new TypeError('Shell capability input must be a plain object');

  const capability = validateMember(input.capability, PLATFORM_CAPABILITIES, 'shell capability');
  const requestedState = validateMember(input.state, CAPABILITY_STATES, 'shell capability state', 'unknown');
  const authoritative = input.authoritative === true;
  const acceptedState = authoritative ? requestedState : 'unknown';

  return Object.freeze({
    version: '1.7.0-dev.6',
    lifecycle: 'development',
    stableBaseline: '1.6.0',
    capability,
    requestedState,
    acceptedState,
    authoritative,
    available: acceptedState === 'available',
    requestedStateWithheldWithoutAuthority: !authoritative && requestedState !== 'unknown',
    authority: Object.freeze({
      presentationOnly: true,
      platformCapabilityOwnedByApplicationOrPlatform: true,
      capabilityCreatedByGlaze: false,
      systemPrivilegeGrantedByGlaze: false,
      permissionGrantedByGlaze: false,
      consequentialExecutionAutomatic: false
    })
  });
}

function normalizeCapabilities(value) {
  const source = plainObject(value) ? value : {};
  const result = {};
  for (const capability of PLATFORM_CAPABILITIES) {
    const raw = source[capability];
    if (plainObject(raw)) {
      result[capability] = resolveGlazeShellCapability({
        capability,
        state: raw.state,
        authoritative: raw.authoritative
      });
    } else {
      result[capability] = resolveGlazeShellCapability({
        capability,
        state: 'unknown',
        authoritative: false
      });
    }
  }
  return Object.freeze(result);
}

export function resolveGlazeSystemShellContext(input = {}) {
  if (!plainObject(input)) throw new TypeError('System Shell context input must be a plain object');

  const profile = validateMember(
    input.profile,
    ['mobile','tablet','desktop','foldable','tv','wearable'],
    'shell profile'
  );

  const profileResolution = resolveGlazeFormFactorProfile({
    profile,
    posture: input.posture,
    accessibilityProfiles: input.accessibilityProfiles,
    availableInputs: input.availableInputs,
    inputCapabilityAuthoritative: input.inputCapabilityAuthoritative,
    unsafeRegionIds: input.unsafeRegionIds,
    semanticSurfaceId: 'system-shell',
    surfaceRole: 'shell'
  });

  const capabilities = normalizeCapabilities(input.capabilities);
  const shellState = normalizeShellState(input.shellState);

  return Object.freeze({
    version: '1.7.0-dev.6',
    lifecycle: 'development',
    stableBaseline: '1.6.0',
    semanticSurfaceId: 'system-shell',
    profile,
    presentation: PROFILE_PRESENTATIONS[profile],
    regions: SHELL_REGIONS,
    profileExpectations: profileResolution.expectations,
    shellState,
    capabilities,
    composition: Object.freeze({
      compactExpandedNavigationUsesFormFactorProfile: true,
      splitViewRequiresAuthoritativeCapability: !capabilities['split-view'].available,
      multiWindowRequiresAuthoritativeCapability: !capabilities['multi-window'].available,
      persistentControlCenterRequiresAuthoritativeCapability:
        !capabilities['persistent-control-center-layout'].available,
      contextualCommandSurfaceComponent: 'GlzCommandSurface',
      contextualCommandSurfaceDelegated: true
    }),
    continuity: Object.freeze({
      activeTaskPreservedUnlessAuthoritativeTaskChange: true,
      shellReconfigurationMayResetTaskByItself: false,
      navigationPreserved: true,
      focusPreserved: true,
      selectionPreserved: true,
      draftsPreserved: true,
      queryAndFiltersPreserved: true,
      paneAndWindowContextPreserved: true,
      safePendingInteractionsPreserved: true,
      providerOwnedTruthPreserved: true
    }),
    authority: Object.freeze({
      presentationOnly: true,
      shellConfigurationOwnedByApplicationOrPlatform: true,
      platformCapabilityOwnedByApplicationOrPlatform: true,
      windowingSupportCreatedByGlaze: false,
      systemPrivilegeGrantedByGlaze: false,
      notificationTruthCreatedByGlaze: false,
      searchAuthorityCreatedByGlaze: false,
      navigationExecutedByGlaze: false,
      handoffExecutedByGlaze: false,
      windowRestorationExecutedByGlaze: false,
      taskSwitchExecutedByGlaze: false,
      consequentialExecutionAutomatic: false
    })
  });
}

export function resolveGlazeShellTransition(input = {}) {
  if (!plainObject(input)) throw new TypeError('Shell transition input must be a plain object');

  const transitionKind = validateMember(input.transitionKind, TRANSITION_KINDS, 'shell transition kind');
  const previousTaskId = input.previousTaskId == null ? null : String(input.previousTaskId).trim() || null;
  const incomingTaskId = input.incomingTaskId == null ? null : String(input.incomingTaskId).trim() || null;
  const taskIdentityAuthoritative = input.taskIdentityAuthoritative === true;

  let acceptedTaskId = previousTaskId;
  let taskIdentityChanged = false;
  let requestedTaskChangeWithheldWithoutAuthority = false;

  if (incomingTaskId && incomingTaskId !== previousTaskId) {
    if (taskIdentityAuthoritative) {
      acceptedTaskId = incomingTaskId;
      taskIdentityChanged = true;
    } else {
      requestedTaskChangeWithheldWithoutAuthority = true;
    }
  } else if (!previousTaskId && incomingTaskId && taskIdentityAuthoritative) {
    acceptedTaskId = incomingTaskId;
    taskIdentityChanged = true;
  }

  const previousShellState = normalizeShellState(input.previousShellState);
  const incomingShellState = normalizeShellState(input.incomingShellState);
  const shellStateAuthoritative = input.shellStateAuthoritative === true;
  const shellState = shellStateForTransition(previousShellState, incomingShellState, shellStateAuthoritative);

  const continuity = resolveGlazeTaskContinuity({
    environmentChange: TASK_CONTINUITY_CHANGE_BY_SHELL_TRANSITION[transitionKind],
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

  return Object.freeze({
    version: '1.7.0-dev.6',
    lifecycle: 'development',
    stableBaseline: '1.6.0',
    transitionKind,
    continuityEnvironmentChange: TASK_CONTINUITY_CHANGE_BY_SHELL_TRANSITION[transitionKind],
    task: Object.freeze({
      previousTaskId,
      requestedTaskId: incomingTaskId,
      acceptedTaskId,
      taskIdentityAuthoritative,
      taskIdentityChanged,
      requestedTaskChangeWithheldWithoutAuthority
    }),
    shellState,
    shellStateAuthoritative,
    taskState: continuity.state,
    stateClasses: continuity.stateClasses,
    decisions: continuity.decisions,
    continuity: Object.freeze({
      ...continuity.continuity,
      activeTaskPreservedUnlessAuthoritativeTaskChange: true,
      shellReconfigurationMayResetTaskByItself: false,
      paneAndWindowContextPreserved: true,
      transitionsPredictable: true,
      transitionsReversible: true,
      reversalRequiresCallerSuppliedShellState: true
    }),
    authority: Object.freeze({
      presentationOnly: true,
      shellConfigurationOwnedByApplicationOrPlatform: true,
      taskIdentityOwnedByApplicationOrPlatform: true,
      providerTruthOwnedByProvider: true,
      navigationExecutedByGlaze: false,
      handoffExecutedByGlaze: false,
      windowRestorationExecutedByGlaze: false,
      taskSwitchExecutedByGlaze: false,
      consequentialExecutionAutomatic: false
    })
  });
}

export function resolveGlazeControlCenterContinuity(input = {}) {
  if (!plainObject(input)) throw new TypeError('Control Center continuity input must be a plain object');

  const previousModuleIds = uniqueStrings(input.previousModuleIds, 100);
  const incomingModuleIds = uniqueStrings(input.incomingModuleIds, 100);
  const layoutAuthoritative = input.layoutAuthoritative === true;
  const requestedPersistentLayout = input.requestedPersistentLayout === true;

  const persistenceCapability = resolveGlazeShellCapability({
    capability: 'persistent-control-center-layout',
    state: input.persistenceCapabilityState,
    authoritative: input.persistenceCapabilityAuthoritative
  });

  const moduleIds = layoutAuthoritative && incomingModuleIds.length > 0
    ? incomingModuleIds
    : previousModuleIds;

  return Object.freeze({
    version: '1.7.0-dev.6',
    lifecycle: 'development',
    stableBaseline: '1.6.0',
    layoutId: input.layoutId == null ? null : String(input.layoutId).trim() || null,
    previousModuleIds,
    incomingModuleIds,
    moduleIds,
    layoutAuthoritative,
    moduleOrderStableUnlessAuthoritativeLayoutChange: true,
    requestedIncomingOrderWithheldWithoutAuthority:
      !layoutAuthoritative && incomingModuleIds.length > 0,
    persistence: Object.freeze({
      requested: requestedPersistentLayout,
      capability: persistenceCapability,
      effective: requestedPersistentLayout && persistenceCapability.available
        ? 'platform-persistent'
        : 'session-only',
      performedByGlaze: false,
      crossDeviceSyncEstablished: false
    }),
    authority: Object.freeze({
      presentationOnly: true,
      layoutTruthOwnedByApplicationOrPlatform: true,
      platformPersistenceOwnedByApplicationOrPlatform: true,
      persistencePerformedByGlaze: false,
      capabilityCreatedByGlaze: false
    })
  });
}

export function resolveGlazeShellActivityPresentation(input = {}) {
  if (!plainObject(input)) throw new TypeError('Shell activity presentation input must be a plain object');

  const requestedPriority = validateMember(input.priority, ACTIVITY_PRIORITIES, 'activity priority', 'unknown');
  const authoritative = input.authoritative === true;
  const sourceId = input.sourceId == null ? null : String(input.sourceId).trim() || null;
  const eventId = input.eventId == null ? null : String(input.eventId).trim() || null;
  const acceptedPriority = authoritative ? requestedPriority : 'unknown';

  return Object.freeze({
    version: '1.7.0-dev.6',
    lifecycle: 'development',
    stableBaseline: '1.6.0',
    shellRegion: 'notification-activity',
    requestedPriority,
    acceptedPriority,
    sourceId: authoritative ? sourceId : null,
    eventId: authoritative ? eventId : null,
    authoritative,
    presentation: Object.freeze({
      shellPresentationSupported: true,
      fullSection8ComponentSystemEstablished: false,
      sourceRequired: true,
      eventRequired: true,
      priorityInventedByGlaze: false,
      criticalStateRequiresAuthoritativeSource: true,
      criticalPresentationAllowed: authoritative && acceptedPriority === 'critical'
    }),
    authority: Object.freeze({
      presentationOnly: true,
      truthOwnedByCallerOrProvider: true,
      truthGeneratedByGlaze: false,
      notificationTruthCreatedByGlaze: false,
      actionAvailabilityCreatedByGlaze: false,
      consequentialExecutionAutomatic: false
    })
  });
}

export const glazeV17SystemShellContinuityDevelopmentContract = Object.freeze({
  version: '1.7.0-dev.6',
  lifecycle: 'development',
  stableBaseline: '1.6.0',
  consumerEligible: false,
  implementedSpecificationSections: Object.freeze([7]),
  shellRegions: SHELL_REGIONS,
  transitionKinds: TRANSITION_KINDS,
  platformCapabilities: PLATFORM_CAPABILITIES,
  capabilityStates: CAPABILITY_STATES,
  activityPriorities: ACTIVITY_PRIORITIES,
  profilePresentations: PROFILE_PRESENTATIONS,
  activeTaskPreservedUnlessAuthoritativeTaskChange: true,
  shellReconfigurationMayResetTaskByItself: false,
  transitionsPredictable: true,
  transitionsReversible: true,
  fullSection8ComponentSystemEstablished: false,
  nativeShellParityEstablished: false,
  presentationOnly: true,
  consequentialExecutionAutomatic: false
});
