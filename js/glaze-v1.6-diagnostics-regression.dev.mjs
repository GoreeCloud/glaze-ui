/* GLAZE UI V1.6 — Development diagnostics, regression, layout-stability,
 * and graceful-degradation foundation.
 *
 * Machine/source diagnostics only. Caller/provider-owned measurements remain
 * authoritative; this module does not manufacture rendered/native evidence.
 */

const DEVELOPER_CHECKS = Object.freeze([
  'contrast',
  'unsupported-token-overrides',
  'missing-component-states',
  'excessive-blur',
  'excessive-animation',
  'target-size',
  'accessible-names',
  'nested-materials',
  'semantic-state-consistency',
  'skeleton-duration',
  'loading-recovery'
]);

const ACCESSIBILITY_CHECKS = Object.freeze([
  'contrast',
  'focus-visibility',
  'logical-focus-order',
  'minimum-target-size',
  'reduced-motion',
  'reduced-transparency',
  'large-text-reflow',
  'semantic-announcements',
  'screen-reader-labeling',
  'color-independent-status'
]);

const SKELETON_CHECKS = Object.freeze([
  'removed-when-content-ready',
  'reduced-motion-compatible',
  'simultaneous-shimmer-budget',
  'layout-stability',
  'loading-semantics',
  'failure-escalation',
  'bounded-duration',
  'focus-continuity'
]);

const VISUAL_SCENARIOS = Object.freeze([
  'light',
  'dark',
  'high-contrast',
  'reduced-motion',
  'reduced-transparency',
  'large-text',
  'loading',
  'skeleton-loading',
  'offline',
  'degraded',
  'errors',
  'empty-states',
  'responsive-layouts',
  'multiple-input-methods'
]);

const SEMANTIC_INVARIANTS = Object.freeze([
  'error-remains-error-across-themes',
  'focus-distinct-from-selection',
  'loading-not-announced-as-completion',
  'restricted-distinct-from-disabled',
  'offline-distinct-from-generic-failure'
]);

const PERFORMANCE_DIMENSIONS = Object.freeze([
  'frame-stability',
  'layout-stability',
  'animation-cost',
  'blur-cost',
  'loading-cost',
  'skeleton-cost',
  'memory-pressure',
  'large-list-behavior'
]);

const FALLBACKS = Object.freeze({
  blur:['blur','translucent-solid','opaque-solid'],
  morph:['morph','fade','immediate-state-change'],
  'animated-skeleton':['animated-skeleton','static-skeleton'],
  'dynamic-environmental-effect':['dynamic-environmental-effect','ordinary-semantic-surface'],
  'complex-transition':['complex-transition','direct-replacement']
});

function plainObject(value) {
  return Boolean(value)
    && typeof value === 'object'
    && !Array.isArray(value)
    && Object.getPrototypeOf(value) === Object.prototype;
}

function bool(value) {
  return value === true;
}

function numberOrNull(value) {
  const n = Number(value);
  return Number.isFinite(n) ? n : null;
}

function uniqueStrings(values) {
  if (!Array.isArray(values)) return Object.freeze([]);
  return Object.freeze([...new Set(values.map(value => String(value ?? '').trim()).filter(Boolean))]);
}

function resultEntry(id, passed, detail = null) {
  return Object.freeze({
    id,
    passed: passed === true,
    detail: detail == null ? null : String(detail)
  });
}

function evaluateBooleanChecks(required, supplied) {
  const source = plainObject(supplied) ? supplied : {};
  return Object.freeze(required.map(id => resultEntry(id, source[id] === true)));
}

export function evaluateGlazeDeveloperDiagnostics(input = {}) {
  if (!plainObject(input)) throw new TypeError('Developer diagnostics input must be a plain object');

  const supplied = plainObject(input.checks) ? input.checks : {};
  const results = evaluateBooleanChecks(DEVELOPER_CHECKS, supplied);
  const failures = results.filter(item => !item.passed).map(item => item.id);

  return Object.freeze({
    version:'1.6.0-dev.9',
    lifecycle:'development',
    stableBaseline:'1.5.1',
    checks:results,
    failures:Object.freeze(failures),
    complete:failures.length === 0,
    diagnostics:Object.freeze({
      sourceOrMeasurementBackedOnly:true,
      renderedEvidenceManufactured:false,
      missingChecksFailClosed:true,
      warningSuppressionMayHideFailure:false
    }),
    authority:Object.freeze({
      measurementsOwnedByCallerOrTooling:true,
      findingsPresentationOnly:true
    })
  });
}

export function evaluateGlazeAccessibilityDiagnostics(input = {}) {
  if (!plainObject(input)) throw new TypeError('Accessibility diagnostics input must be a plain object');

  const results = evaluateBooleanChecks(ACCESSIBILITY_CHECKS, input.checks);
  const failures = results.filter(item => !item.passed).map(item => item.id);

  return Object.freeze({
    version:'1.6.0-dev.9',
    lifecycle:'development',
    checks:results,
    failures:Object.freeze(failures),
    complete:failures.length === 0,
    rules:Object.freeze({
      colorOnlyStatusAllowed:false,
      missingScreenReaderLabelsAllowed:false,
      focusVisibilityOptional:false,
      reducedMotionCompatibilityOptional:false,
      reducedTransparencyCompatibilityOptional:false,
      largeTextReflowOptional:false
    }),
    authority:Object.freeze({
      assistiveTechnologyAcceptanceInferred:false,
      platformAccessibilityEvidenceOwnedByTestEnvironment:true
    })
  });
}

export function evaluateGlazeSkeletonDiagnostics(input = {}) {
  if (!plainObject(input)) throw new TypeError('Skeleton diagnostics input must be a plain object');

  const maxSimultaneousShimmer = Number.isInteger(Number(input.maxSimultaneousShimmer))
    ? Math.max(0, Number(input.maxSimultaneousShimmer))
    : 12;
  const maxDurationMs = Number.isFinite(Number(input.maxDurationMs))
    ? Math.max(0, Number(input.maxDurationMs))
    : 10000;
  const shiftBudget = Number.isFinite(Number(input.layoutShiftBudget))
    ? Math.max(0, Number(input.layoutShiftBudget))
    : 0.1;

  const checks = {
    'removed-when-content-ready': !(bool(input.contentReady) && bool(input.skeletonActive)),
    'reduced-motion-compatible': !(bool(input.reducedMotion) && bool(input.continuousSkeletonMotion)),
    'simultaneous-shimmer-budget': Number(input.simultaneousShimmerCount || 0) <= maxSimultaneousShimmer,
    'layout-stability': Number(input.layoutShift || 0) <= shiftBudget,
    'loading-semantics': input.loadingSemanticsPresent === true,
    'failure-escalation': input.failureEscalationPresent === true,
    'bounded-duration': Number(input.activeDurationMs || 0) <= maxDurationMs,
    'focus-continuity': input.focusLostDuringReplacement !== true
  };

  const results = evaluateBooleanChecks(SKELETON_CHECKS, checks);
  const failures = results.filter(item => !item.passed).map(item => item.id);

  return Object.freeze({
    version:'1.6.0-dev.9',
    lifecycle:'development',
    checks:results,
    failures:Object.freeze(failures),
    complete:failures.length === 0,
    budgets:Object.freeze({
      maxSimultaneousShimmer,
      maxDurationMs,
      layoutShiftBudget:shiftBudget,
      developmentReferenceOnly:true
    }),
    authority:Object.freeze({
      contentReadinessOwnedByApplication:true,
      measuredLayoutShiftOwnedByHarness:true,
      focusEvidenceOwnedByHarness:true
    })
  });
}

export function evaluateGlazeVisualRegression(input = {}) {
  if (!plainObject(input)) throw new TypeError('Visual regression input must be a plain object');

  const outcomes = plainObject(input.scenarios) ? input.scenarios : {};
  const results = Object.freeze(VISUAL_SCENARIOS.map(id => resultEntry(id, outcomes[id] === true)));
  const failures = results.filter(item => !item.passed).map(item => item.id);

  return Object.freeze({
    version:'1.6.0-dev.9',
    lifecycle:'development',
    scenarios:results,
    failures:Object.freeze(failures),
    complete:failures.length === 0,
    determinism:Object.freeze({
      referenceScenesRequired:true,
      screenshotsGeneratedByResolver:false,
      humanVisualAcceptanceInferred:false
    })
  });
}

export function evaluateGlazeSemanticRegression(input = {}) {
  if (!plainObject(input)) throw new TypeError('Semantic regression input must be a plain object');

  const outcomes = plainObject(input.invariants) ? input.invariants : {};
  const results = Object.freeze(SEMANTIC_INVARIANTS.map(id => resultEntry(id, outcomes[id] === true)));
  const failures = results.filter(item => !item.passed).map(item => item.id);

  return Object.freeze({
    version:'1.6.0-dev.9',
    lifecycle:'development',
    invariants:results,
    failures:Object.freeze(failures),
    complete:failures.length === 0,
    rules:Object.freeze({
      themeMayChangeMeaning:false,
      loadingMayPresentAsCompletion:false,
      restrictedMayCollapseToDisabled:false,
      offlineMayCollapseToGenericFailure:false
    })
  });
}

export function evaluateGlazePerformanceRegression(input = {}) {
  if (!plainObject(input)) throw new TypeError('Performance regression input must be a plain object');

  const measurements = plainObject(input.measurements) ? input.measurements : {};
  const budgets = plainObject(input.budgets) ? input.budgets : {};
  const directions = plainObject(input.directions) ? input.directions : {};

  const results = PERFORMANCE_DIMENSIONS.map(id => {
    const measured = numberOrNull(measurements[id]);
    const budget = numberOrNull(budgets[id]);
    const direction = directions[id] === 'minimum' ? 'minimum' : 'maximum';
    if (measured === null || budget === null) {
      return Object.freeze({id, measured, budget, direction, passed:false, verified:false});
    }
    const passed = direction === 'minimum' ? measured >= budget : measured <= budget;
    return Object.freeze({id, measured, budget, direction, passed, verified:true});
  });
  const failures = results.filter(item => !item.passed).map(item => item.id);

  return Object.freeze({
    version:'1.6.0-dev.9',
    lifecycle:'development',
    dimensions:Object.freeze(results),
    failures:Object.freeze(failures),
    complete:failures.length === 0,
    authority:Object.freeze({
      measurementsOwnedByPerformanceHarness:true,
      budgetsOwnedByGovernedAcceptanceProfile:true,
      thresholdsInventedByResolver:false,
      representativeDeviceAcceptanceInferred:false
    })
  });
}

export function evaluateGlazeLayoutStability(input = {}) {
  if (!plainObject(input)) throw new TypeError('Layout stability input must be a plain object');

  const measuredShift = numberOrNull(input.measuredShift);
  const budget = numberOrNull(input.budget);
  const verified = measuredShift !== null && budget !== null;
  const passed = verified && measuredShift <= budget;

  return Object.freeze({
    version:'1.6.0-dev.9',
    lifecycle:'development',
    measuredShift,
    budget,
    verified,
    passed,
    sources:Object.freeze({
      skeleton:bool(input.skeletonMeasured),
      images:bool(input.imagesMeasured),
      dynamicControls:bool(input.dynamicControlsMeasured),
      asynchronousContent:bool(input.asynchronousContentMeasured)
    }),
    rules:Object.freeze({
      preserveSpaceWherePractical:true,
      unnecessaryWholePagePushAllowed:false,
      dynamicContentMayEraseFocus:false
    }),
    authority:Object.freeze({
      measurementsOwnedByLayoutHarness:true,
      layoutAcceptanceInferred:false
    })
  });
}

export function resolveGlazeGracefulDegradation(input = {}) {
  if (!plainObject(input)) throw new TypeError('Graceful degradation input must be a plain object');

  const effect = String(input.effect ?? '').trim().toLowerCase();
  const chain = FALLBACKS[effect];
  if (!chain) throw new RangeError(`Unsupported degradable effect: ${effect}`);

  const supported = new Set(uniqueStrings(input.supportedModes).map(value => value.toLowerCase()));
  const selected = chain.find(mode => supported.has(mode)) || chain[chain.length - 1];

  return Object.freeze({
    version:'1.6.0-dev.9',
    lifecycle:'development',
    effect,
    fallbackChain:chain,
    selected,
    rules:Object.freeze({
      usabilityPreserved:true,
      semanticMeaningPreserved:true,
      advancedEffectRequiredForComprehension:false,
      unsupportedEffectMayFailClosedToSimplestMode:true
    }),
    authority:Object.freeze({
      capabilityTruthOwnedByCallerOrPlatform:true,
      fallbackExecutionAutomatic:false,
      selectionPresentationOnly:true
    })
  });
}

export const glazeV16DiagnosticsRegressionDevelopmentContract = Object.freeze({
  version:'1.6.0-dev.9',
  lifecycle:'development',
  stableBaseline:'1.5.1',
  consumerEligible:false,
  developerChecks:DEVELOPER_CHECKS,
  accessibilityChecks:ACCESSIBILITY_CHECKS,
  skeletonChecks:SKELETON_CHECKS,
  visualScenarios:VISUAL_SCENARIOS,
  semanticInvariants:SEMANTIC_INVARIANTS,
  performanceDimensions:PERFORMANCE_DIMENSIONS,
  degradationFallbacks:FALLBACKS,
  missingDiagnosticsFailClosed:true,
  renderedAcceptanceManufactured:false,
  assistiveTechnologyAcceptanceInferred:false,
  performanceThresholdsInvented:false,
  visualRegressionRequiresDeterministicScenes:true,
  semanticMeaningMayRegressAcrossThemes:false,
  advancedEffectsRequireSimpleFallbacks:true,
  authorityBoundary:'evidence-evaluation-only'
});
