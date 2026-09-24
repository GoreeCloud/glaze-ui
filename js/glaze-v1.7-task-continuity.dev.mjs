/* GLAZE UI V1.7 — Task Continuity Development foundation.
 *
 * Development-only presentation resolver. GLAZE UI V1.6 / 1.6.0 remains
 * the current Official Stable consumer target.
 */

const STATE_CLASSES = Object.freeze([
  'durable',
  'session-scoped',
  'presentation-only',
  'provider-owned',
  'temporary',
  'recoverable',
  'non-restorable'
]);

const CONTINUITY_FIELDS = Object.freeze([
  'navigationDestination',
  'focusId',
  'selectionIds',
  'scrollPositionKey',
  'expandedRegionIds',
  'draftText',
  'formState',
  'activeFilters',
  'query',
  'paneState',
  'mediaState',
  'pendingInteractions',
  'workingContext'
]);

const ENVIRONMENT_CHANGES = Object.freeze([
  'window-resize',
  'device-rotation',
  'foldable-posture',
  'compact-expanded-layout',
  'input-method',
  'accessibility-mode',
  'appearance',
  'capability-degradation',
  'connectivity',
  'multi-pane-recomposition',
  'form-factor'
]);

const PROFILES = Object.freeze([
  'mobile',
  'tablet',
  'desktop',
  'foldable',
  'tv',
  'wearable'
]);

const PRESENTATIONS = Object.freeze([
  'bottom-sheet',
  'side-pane',
  'secondary-pane',
  'floating-panel',
  'full-screen-step',
  'far-view-panel'
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

function uniqueStrings(values, max = 200) {
  if (!Array.isArray(values)) return Object.freeze([]);
  return Object.freeze(
    [...new Set(values.map(value => String(value ?? '').trim()).filter(Boolean))].slice(0, max)
  );
}

function cloneJsonLike(value) {
  if (value == null) return value;
  if (Array.isArray(value)) return Object.freeze(value.map(cloneJsonLike));
  if (plainObject(value)) {
    const copy = {};
    for (const [key, item] of Object.entries(value)) copy[key] = cloneJsonLike(item);
    return Object.freeze(copy);
  }
  if (['string', 'number', 'boolean'].includes(typeof value)) return value;
  throw new TypeError('Continuity state values must be JSON-like primitives, arrays, or plain objects');
}

function validateStateClass(value) {
  const stateClass = semanticId(value);
  if (!STATE_CLASSES.includes(stateClass)) {
    throw new RangeError(`Unsupported task-state class: ${stateClass}`);
  }
  return stateClass;
}

function validateEnvironmentChange(value) {
  const change = semanticId(value);
  if (!ENVIRONMENT_CHANGES.includes(change)) {
    throw new RangeError(`Unsupported environment change: ${change}`);
  }
  return change;
}

function validateProfile(value) {
  const profile = semanticId(value);
  if (!PROFILES.includes(profile)) {
    throw new RangeError(`Unsupported form-factor profile: ${profile}`);
  }
  return profile;
}

function stateClassPolicy(stateClass) {
  const policies = {
    'durable': {
      restoreAcrossEnvironmentChanges: true,
      restoreAcrossApplicationRestart: true,
      callerRecoveryRequired: false,
      mayRecompute: false,
      mayDiscardWithoutExplicitCallerDirection: false
    },
    'session-scoped': {
      restoreAcrossEnvironmentChanges: true,
      restoreAcrossApplicationRestart: false,
      callerRecoveryRequired: false,
      mayRecompute: false,
      mayDiscardWithoutExplicitCallerDirection: false
    },
    'presentation-only': {
      restoreAcrossEnvironmentChanges: false,
      restoreAcrossApplicationRestart: false,
      callerRecoveryRequired: false,
      mayRecompute: true,
      mayDiscardWithoutExplicitCallerDirection: true
    },
    'provider-owned': {
      restoreAcrossEnvironmentChanges: true,
      restoreAcrossApplicationRestart: false,
      callerRecoveryRequired: false,
      mayRecompute: false,
      mayDiscardWithoutExplicitCallerDirection: false
    },
    'temporary': {
      restoreAcrossEnvironmentChanges: true,
      restoreAcrossApplicationRestart: false,
      callerRecoveryRequired: false,
      mayRecompute: false,
      mayDiscardWithoutExplicitCallerDirection: false
    },
    'recoverable': {
      restoreAcrossEnvironmentChanges: true,
      restoreAcrossApplicationRestart: true,
      callerRecoveryRequired: true,
      mayRecompute: false,
      mayDiscardWithoutExplicitCallerDirection: false
    },
    'non-restorable': {
      restoreAcrossEnvironmentChanges: true,
      restoreAcrossApplicationRestart: false,
      callerRecoveryRequired: false,
      mayRecompute: false,
      mayDiscardWithoutExplicitCallerDirection: false
    }
  };
  return Object.freeze({...policies[stateClass]});
}

export function classifyGlazeTaskState(input = {}) {
  if (!plainObject(input)) throw new TypeError('Task-state classification input must be a plain object');

  const stateClass = validateStateClass(input.stateClass);
  const policy = stateClassPolicy(stateClass);

  return Object.freeze({
    version: '1.7.0-dev.1',
    lifecycle: 'development',
    stableBaseline: '1.6.0',
    stateClass,
    semanticRole: `continuity.state.${stateClass}`,
    restoration: policy,
    safeguards: Object.freeze({
      explicitDisposableRequiredForTemporaryDiscard: stateClass === 'temporary',
      explicitLossDirectionRequiredForNonRestorable: stateClass === 'non-restorable',
      providerReplacementRequiresAuthoritativeInput: stateClass === 'provider-owned',
      recoverableStateRequiresCallerSuppliedRecoveryState: stateClass === 'recoverable'
    }),
    authority: Object.freeze({
      presentationOnly: true,
      taskTruthOwnedByApplication: true,
      providerTruthOwnedByProvider: true,
      persistenceClaimCreatedByGlaze: false,
      authorizationGrantedByGlaze: false,
      permissionGrantedByGlaze: false,
      consentGrantedByGlaze: false
    })
  });
}

function normalizeClassMap(value) {
  const source = plainObject(value) ? value : {};
  const normalized = {};
  for (const field of CONTINUITY_FIELDS) {
    normalized[field] = validateStateClass(source[field] ?? 'session-scoped');
  }
  return Object.freeze(normalized);
}

function normalizedTaskState(value) {
  const source = plainObject(value) ? value : {};
  const state = {};
  for (const field of CONTINUITY_FIELDS) {
    if (Object.prototype.hasOwnProperty.call(source, field)) {
      state[field] = cloneJsonLike(source[field]);
    }
  }
  return Object.freeze(state);
}

export function resolveGlazeTaskContinuity(input = {}) {
  if (!plainObject(input)) throw new TypeError('Task continuity input must be a plain object');

  const environmentChange = validateEnvironmentChange(input.environmentChange);
  const previous = normalizedTaskState(input.previous);
  const incoming = normalizedTaskState(input.incoming);
  const stateClasses = normalizeClassMap(input.stateClasses);
  const clearFields = new Set(uniqueStrings(input.clearFields, CONTINUITY_FIELDS.length));
  const clearAuthoritative = input.clearAuthoritative === true;
  const temporaryDisposableFields = new Set(uniqueStrings(input.temporaryDisposableFields, CONTINUITY_FIELDS.length));
  const lossDirectedFields = new Set(uniqueStrings(input.lossDirectedFields, CONTINUITY_FIELDS.length));

  const resolved = {};
  const decisions = {};
  let blockedByContinuityRisk = false;

  for (const field of CONTINUITY_FIELDS) {
    const stateClass = stateClasses[field];
    const hasPrevious = Object.prototype.hasOwnProperty.call(previous, field);
    const hasIncoming = Object.prototype.hasOwnProperty.call(incoming, field);
    const wantsClear = clearFields.has(field);

    if (wantsClear) {
      if (!clearAuthoritative) {
        if (hasPrevious) resolved[field] = previous[field];
        decisions[field] = 'preserved-clear-not-authoritative';
        continue;
      }
      if (stateClass === 'provider-owned') {
        if (hasPrevious) resolved[field] = previous[field];
        decisions[field] = 'preserved-provider-owned';
        blockedByContinuityRisk = true;
        continue;
      }
      if (stateClass === 'temporary' && !temporaryDisposableFields.has(field)) {
        if (hasPrevious) resolved[field] = previous[field];
        decisions[field] = 'preserved-temporary-not-disposable';
        blockedByContinuityRisk = true;
        continue;
      }
      if (stateClass === 'non-restorable' && !lossDirectedFields.has(field)) {
        if (hasPrevious) resolved[field] = previous[field];
        decisions[field] = 'preserved-non-restorable-loss-not-directed';
        blockedByContinuityRisk = true;
        continue;
      }
      decisions[field] = 'cleared-by-authoritative-caller';
      continue;
    }

    if (hasIncoming) {
      resolved[field] = incoming[field];
      decisions[field] = stateClass === 'provider-owned'
        ? 'accepted-authoritative-provider-input'
        : 'accepted-caller-input';
      continue;
    }

    if (hasPrevious) {
      resolved[field] = previous[field];
      decisions[field] = 'preserved-existing-task-state';
      continue;
    }

    decisions[field] = stateClass === 'presentation-only'
      ? 'presentation-may-recompute'
      : 'no-state-supplied';
  }

  return Object.freeze({
    version: '1.7.0-dev.1',
    lifecycle: 'development',
    stableBaseline: '1.6.0',
    environmentChange,
    state: Object.freeze(resolved),
    stateClasses,
    decisions: Object.freeze(decisions),
    continuity: Object.freeze({
      taskStateResetOnRecompositionAllowed: false,
      preserveWhenIncomingStateIsAbsent: true,
      clearRequiresAuthoritativeCallerDirection: true,
      providerOwnedClearAllowedByGlaze: false,
      blockedByContinuityRisk
    }),
    authority: Object.freeze({
      presentationOnly: true,
      taskTruthOwnedByApplication: true,
      providerTruthOwnedByProvider: true,
      capabilityTruthOwnedByProvider: true,
      connectivityTruthOwnedByProvider: true,
      securityTruthOwnedByProvider: true,
      privacyTruthOwnedByProvider: true,
      providerTruthManufactured: false,
      consequentialExecutionAutomatic: false
    })
  });
}

function defaultPresentation(profile, surfaceRole, posture, constrained) {
  if (constrained) return 'full-screen-step';
  if (profile === 'wearable') return 'full-screen-step';
  if (profile === 'tv') return 'far-view-panel';
  if (profile === 'mobile') return surfaceRole === 'detail' ? 'bottom-sheet' : 'full-screen-step';
  if (profile === 'tablet') return 'side-pane';
  if (profile === 'desktop') return surfaceRole === 'floating-tool' ? 'floating-panel' : 'secondary-pane';
  if (profile === 'foldable') return posture === 'folded' ? 'full-screen-step' : 'side-pane';
  return 'full-screen-step';
}

export function resolveGlazeAdaptiveComposition(input = {}) {
  if (!plainObject(input)) throw new TypeError('Adaptive composition input must be a plain object');

  const profile = validateProfile(input.profile);
  const semanticSurfaceId = String(input.semanticSurfaceId ?? '').trim();
  if (!semanticSurfaceId) throw new TypeError('semanticSurfaceId is required');

  const surfaceRole = semanticId(input.surfaceRole, 'task');
  const posture = semanticId(input.posture, 'unknown');
  const accessibilityProfiles = uniqueStrings(input.accessibilityProfiles, 20).map(value => value.toLowerCase());
  const constrained = input.constrained === true
    || accessibilityProfiles.includes('large-text')
    || accessibilityProfiles.includes('extra-large-text');

  const presentation = defaultPresentation(profile, surfaceRole, posture, constrained);
  if (!PRESENTATIONS.includes(presentation)) {
    throw new RangeError(`Unsupported adaptive presentation: ${presentation}`);
  }

  return Object.freeze({
    version: '1.7.0-dev.1',
    lifecycle: 'development',
    stableBaseline: '1.6.0',
    semanticSurfaceId,
    surfaceRole,
    profile,
    posture,
    presentation,
    accessibilityProfiles: Object.freeze(accessibilityProfiles),
    preservation: Object.freeze({
      semanticIdentityPreserved: true,
      focusPreserved: true,
      selectionPreserved: true,
      scrollStatePreserved: true,
      navigationStatePreserved: true,
      draftStatePreserved: true,
      accessibilitySemanticsPreserved: true,
      providerTruthPreserved: true,
      taskStateResetOnRecompositionAllowed: false
    }),
    compositionRules: Object.freeze({
      widthAloneIsAuthority: false,
      deviceBrandBreakpointAuthority: false,
      accessibilityMaySimplifyComposition: true,
      constrainedPresentationMayBecomeFullScreen: true,
      presentationChangeDoesNotGrantCapability: true
    }),
    authority: Object.freeze({
      presentationOnly: true,
      capabilityTruthOwnedByProvider: true,
      authorizationGrantedByGlaze: false,
      permissionGrantedByGlaze: false,
      consentGrantedByGlaze: false,
      providerTruthManufactured: false,
      navigationExecutedByGlaze: false
    })
  });
}

export const glazeV17TaskContinuityDevelopmentContract = Object.freeze({
  version: '1.7.0-dev.1',
  lifecycle: 'development',
  stableBaseline: '1.6.0',
  consumerEligible: false,
  implementedSpecificationSections: Object.freeze([1, 4]),
  stateClasses: STATE_CLASSES,
  continuityFields: CONTINUITY_FIELDS,
  environmentChanges: ENVIRONMENT_CHANGES,
  profiles: PROFILES,
  presentations: PRESENTATIONS,
  presentationOnly: true,
  taskStateResetOnRecompositionAllowed: false,
  providerTruthManufactured: false,
  authorizationGrantedByGlaze: false,
  permissionGrantedByGlaze: false,
  consentGrantedByGlaze: false,
  consequentialExecutionAutomatic: false
});
