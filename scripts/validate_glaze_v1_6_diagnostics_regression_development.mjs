#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

import {
  evaluateGlazeDeveloperDiagnostics,
  evaluateGlazeAccessibilityDiagnostics,
  evaluateGlazeSkeletonDiagnostics,
  evaluateGlazeVisualRegression,
  evaluateGlazeSemanticRegression,
  evaluateGlazePerformanceRegression,
  evaluateGlazeLayoutStability,
  resolveGlazeGracefulDegradation,
  glazeV16DiagnosticsRegressionDevelopmentContract
} from '../js/glaze-v1.6-diagnostics-regression.dev.mjs';
import {glazeV16Development} from '../js/glaze-v1.6-development.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const read = rel => fs.readFileSync(path.join(root, rel), 'utf8');
const json = rel => JSON.parse(read(rel));
const assert = (condition, message) => { if (!condition) throw new Error(message); };

const contract = json('contracts/v1.6/diagnostics-regression.dev.json');
const schema = json('schemas/v1.6-diagnostics-regression.schema.json');
const tokens = json('tokens/glaze-v1.6-diagnostics-regression.dev.json');
const lifecycle = json('registry/lifecycle.json');
const stable = read('VERSION').trim();
const spec = read('GLAZE_UI_V1_6_PLANNED.md');

const sections = [80,81,82,83,84,85,86,87];

assert(stable === '1.5.1', 'current Stable VERSION must remain 1.5.1');
assert(lifecycle.currentOfficial === '1.5.1', 'currentOfficial must remain 1.5.1');
assert(lifecycle.currentStable === '1.5.1', 'currentStable must remain 1.5.1');
assert(lifecycle.activeCandidate === null, 'V1.6 Development must not create active Candidate');
assert(lifecycle.activePatchReleaseCandidate === null, 'V1.6 Development must not create patch RC');
assert(lifecycle.plannedNext === null, 'V1.6 Development must not mutate plannedNext');

for (const number of sections) {
  assert(spec.includes(`# ${number}.`), `planned specification missing section ${number}`);
}

assert(schema.$schema === 'https://json-schema.org/draft/2020-12/schema', 'schema must use JSON Schema 2020-12');
assert(contract.$schema === '../../schemas/v1.6-diagnostics-regression.schema.json', 'contract schema binding mismatch');
assert(contract.version === '1.6.0-dev.9', 'contract version mismatch');
assert(contract.lifecycle === 'Development', 'contract must remain Development');
assert(contract.stableBaseline === '1.5.1', 'contract Stable baseline mismatch');
assert(contract.consumerEligible === false, 'contract must remain non-consumer-eligible');
assert(JSON.stringify(contract.implementedSpecificationSections) === JSON.stringify(sections), 'implemented section set mismatch');
assert(contract.developerDiagnostics.missingChecksFailClosed === true, 'developer diagnostics must fail closed');
assert(contract.accessibilityDiagnostics.assistiveTechnologyAcceptanceInferred === false, 'AT acceptance must not be inferred');
assert(contract.skeletonDiagnostics.referenceBudgetsDevelopmentOnly === true, 'skeleton diagnostic budgets must remain Development reference only');
assert(contract.visualRegression.deterministicReferenceScenesRequired === true, 'visual regression must require deterministic scenes');
assert(contract.semanticRegression.themeMayChangeMeaning === false, 'theme must not change semantic meaning');
assert(contract.performanceRegression.thresholdsInventedByResolver === false, 'performance thresholds must not be invented');
assert(contract.layoutStability.unnecessaryWholePagePushAllowed === false, 'unnecessary layout push must be rejected');
assert(contract.gracefulDegradation.semanticMeaningPreserved === true, 'degradation must preserve meaning');
assert(contract.authority.acceptanceInferred === false, 'acceptance must not be inferred');

assert(tokens.version === '1.6.0-dev.9', 'token map version mismatch');
assert(tokens.lifecycle === 'Development', 'token map must remain Development');
assert(tokens.stableBaseline === '1.5.1', 'token map Stable baseline mismatch');
assert(tokens.consumerEligible === false, 'token map must remain non-consumer-eligible');
assert(tokens.boundaries.missingDiagnosticsFailClosed === true, 'token map must fail closed');
assert(tokens.boundaries.renderedAcceptanceManufactured === false, 'token map must not manufacture rendered acceptance');
assert(tokens.boundaries.performanceThresholdsInvented === false, 'token map must not invent performance thresholds');
assert(tokens.referenceSkeletonBudgets.developmentReferenceOnly === true, 'reference skeleton budgets must remain Development-only');

for (const source of tokens.sourceAuthorities || []) {
  assert(fs.existsSync(path.join(root, source)), `token source authority missing: ${source}`);
}

assert(glazeV16DiagnosticsRegressionDevelopmentContract.version === '1.6.0-dev.9', 'runtime contract version mismatch');
assert(glazeV16DiagnosticsRegressionDevelopmentContract.lifecycle === 'development', 'runtime contract must remain Development');
assert(glazeV16DiagnosticsRegressionDevelopmentContract.consumerEligible === false, 'runtime contract must remain non-consumer-eligible');
assert(glazeV16DiagnosticsRegressionDevelopmentContract.renderedAcceptanceManufactured === false, 'runtime must not manufacture rendered acceptance');
assert(glazeV16DiagnosticsRegressionDevelopmentContract.performanceThresholdsInvented === false, 'runtime must not invent performance thresholds');
assert(glazeV16DiagnosticsRegressionDevelopmentContract.advancedEffectsRequireSimpleFallbacks === true, 'runtime must require simple fallbacks');

assert(glazeV16Development.version === '1.6.0-dev.9', 'aggregate must identify dev.9');
assert(glazeV16Development.lifecycle === 'development', 'aggregate must remain Development');
assert(glazeV16Development.stableBaseline === '1.5.1', 'aggregate Stable baseline mismatch');
assert(glazeV16Development.consumerEligible === false, 'aggregate must remain non-consumer-eligible');
for (const number of sections) {
  assert(glazeV16Development.implementedSpecificationSections.includes(number), `aggregate missing diagnostics section ${number}`);
}
for (const retained of [1,6,10,15,29,41,55,60,70,71,73,74,79,88,93]) {
  assert(glazeV16Development.implementedSpecificationSections.includes(retained), `aggregate lost prior section ${retained}`);
}

const allDeveloperChecks = Object.fromEntries(contract.developerDiagnostics.checks.map(id => [id, true]));
const developer = evaluateGlazeDeveloperDiagnostics({checks:allDeveloperChecks});
assert(developer.complete === true, 'complete developer diagnostics should pass');
assert(developer.failures.length === 0, 'complete developer diagnostics should have no failures');
assert(developer.diagnostics.renderedEvidenceManufactured === false, 'developer diagnostics must not manufacture rendered evidence');

const missingDeveloper = evaluateGlazeDeveloperDiagnostics({checks:{contrast:true}});
assert(missingDeveloper.complete === false, 'missing developer diagnostics must fail closed');
assert(missingDeveloper.failures.includes('loading-recovery'), 'missing loading recovery check must be reported');

const allAccessibilityChecks = Object.fromEntries(contract.accessibilityDiagnostics.checks.map(id => [id, true]));
const accessibility = evaluateGlazeAccessibilityDiagnostics({checks:allAccessibilityChecks});
assert(accessibility.complete === true, 'complete accessibility diagnostics should pass');
assert(accessibility.rules.colorOnlyStatusAllowed === false, 'accessibility diagnostics must reject color-only status');
assert(accessibility.authority.assistiveTechnologyAcceptanceInferred === false, 'accessibility diagnostics must not infer AT acceptance');

const skeletonGood = evaluateGlazeSkeletonDiagnostics({
  contentReady:false,
  skeletonActive:true,
  reducedMotion:true,
  continuousSkeletonMotion:false,
  simultaneousShimmerCount:3,
  layoutShift:0.02,
  loadingSemanticsPresent:true,
  failureEscalationPresent:true,
  activeDurationMs:2500,
  focusLostDuringReplacement:false
});
assert(skeletonGood.complete === true, 'healthy skeleton diagnostics should pass');
assert(skeletonGood.budgets.developmentReferenceOnly === true, 'skeleton budgets must remain Development-only');

const skeletonBad = evaluateGlazeSkeletonDiagnostics({
  contentReady:true,
  skeletonActive:true,
  reducedMotion:true,
  continuousSkeletonMotion:true,
  simultaneousShimmerCount:30,
  layoutShift:0.5,
  loadingSemanticsPresent:false,
  failureEscalationPresent:false,
  activeDurationMs:20000,
  focusLostDuringReplacement:true
});
assert(skeletonBad.complete === false, 'bad skeleton diagnostics must fail');
for (const failure of [
  'removed-when-content-ready','reduced-motion-compatible','simultaneous-shimmer-budget',
  'layout-stability','loading-semantics','failure-escalation','bounded-duration','focus-continuity'
]) {
  assert(skeletonBad.failures.includes(failure), `skeleton failure not detected: ${failure}`);
}

const visualAll = Object.fromEntries(contract.visualRegression.scenarios.map(id => [id, true]));
const visual = evaluateGlazeVisualRegression({scenarios:visualAll});
assert(visual.complete === true, 'full visual regression matrix should pass');
assert(visual.determinism.humanVisualAcceptanceInferred === false, 'visual regression must not infer human acceptance');

const visualMissing = evaluateGlazeVisualRegression({scenarios:{light:true,dark:true}});
assert(visualMissing.complete === false, 'missing visual scenarios must fail closed');

const semanticAll = Object.fromEntries(contract.semanticRegression.invariants.map(id => [id, true]));
const semantic = evaluateGlazeSemanticRegression({invariants:semanticAll});
assert(semantic.complete === true, 'semantic invariants should pass');
assert(semantic.rules.themeMayChangeMeaning === false, 'theme may not change semantic meaning');

const semanticBroken = evaluateGlazeSemanticRegression({
  invariants:{
    'error-remains-error-across-themes':false,
    'focus-distinct-from-selection':true,
    'loading-not-announced-as-completion':true,
    'restricted-distinct-from-disabled':true,
    'offline-distinct-from-generic-failure':true
  }
});
assert(semanticBroken.failures.includes('error-remains-error-across-themes'), 'semantic error regression must be detected');

const performance = evaluateGlazePerformanceRegression({
  measurements:{
    'frame-stability':99,
    'layout-stability':0.04,
    'animation-cost':4,
    'blur-cost':5,
    'loading-cost':7,
    'skeleton-cost':3,
    'memory-pressure':20,
    'large-list-behavior':12
  },
  budgets:{
    'frame-stability':95,
    'layout-stability':0.1,
    'animation-cost':8,
    'blur-cost':10,
    'loading-cost':10,
    'skeleton-cost':8,
    'memory-pressure':30,
    'large-list-behavior':16
  },
  directions:{'frame-stability':'minimum'}
});
assert(performance.complete === true, 'performance inputs within caller-owned budgets should pass');
assert(performance.authority.thresholdsInventedByResolver === false, 'performance evaluator must not invent thresholds');
assert(performance.authority.representativeDeviceAcceptanceInferred === false, 'performance evaluator must not infer device acceptance');

const performanceMissing = evaluateGlazePerformanceRegression({
  measurements:{'frame-stability':99},
  budgets:{'frame-stability':95},
  directions:{'frame-stability':'minimum'}
});
assert(performanceMissing.complete === false, 'missing performance measurements/budgets must fail closed');
assert(performanceMissing.failures.includes('layout-stability'), 'missing layout performance evidence must be reported');

const layout = evaluateGlazeLayoutStability({
  measuredShift:0.03,
  budget:0.1,
  skeletonMeasured:true,
  imagesMeasured:true,
  dynamicControlsMeasured:true,
  asynchronousContentMeasured:true
});
assert(layout.verified === true && layout.passed === true, 'layout stability within supplied budget should pass');
assert(layout.rules.unnecessaryWholePagePushAllowed === false, 'whole-page push must remain disallowed');
assert(layout.authority.layoutAcceptanceInferred === false, 'layout evaluator must not infer acceptance');

const layoutUnknown = evaluateGlazeLayoutStability({measuredShift:0.03});
assert(layoutUnknown.verified === false && layoutUnknown.passed === false, 'missing layout budget must remain unverified');

const blurFallback = resolveGlazeGracefulDegradation({
  effect:'blur',
  supportedModes:['translucent-solid','opaque-solid']
});
assert(blurFallback.selected === 'translucent-solid', 'blur should choose strongest supported simpler fallback');
assert(blurFallback.rules.semanticMeaningPreserved === true, 'degradation must preserve semantic meaning');
assert(blurFallback.authority.fallbackExecutionAutomatic === false, 'degradation resolver must not execute fallback');

const skeletonFallback = resolveGlazeGracefulDegradation({
  effect:'animated-skeleton',
  supportedModes:[]
});
assert(skeletonFallback.selected === 'static-skeleton', 'unsupported animated skeleton must fail closed to static skeleton');

for (const [effect, expectedLast] of [
  ['morph','immediate-state-change'],
  ['dynamic-environmental-effect','ordinary-semantic-surface'],
  ['complex-transition','direct-replacement']
]) {
  const resolved = resolveGlazeGracefulDegradation({effect,supportedModes:[]});
  assert(resolved.selected === expectedLast, `fallback chain mismatch: ${effect}`);
}

let invalidFallback=false;
try { resolveGlazeGracefulDegradation({effect:'magic-glow'}); } catch { invalidFallback=true; }
assert(invalidFallback, 'unknown degradable effect must fail closed');

console.log('GLAZE UI V1.6 diagnostics/regression Development foundation: PASS');
console.log('Developer diagnostics: 11');
console.log('Accessibility diagnostics: 10');
console.log('Skeleton diagnostics: 8');
console.log('Visual regression scenarios: 14');
console.log('Semantic invariants: 5');
console.log('Performance dimensions: 8');
console.log('Implemented sections: 80-87');
console.log('Stable baseline preserved: 1.5.1');
console.log('Consumer eligible: false');
