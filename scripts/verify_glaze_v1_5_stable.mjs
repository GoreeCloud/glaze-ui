import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

import {
  resolveGlazeInterface,
  summarizeGlazeInterfaceResolution
} from '../js/glaze-v1.5-resolution.dev.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');

function read(rel) {
  return fs.readFileSync(path.join(root, rel), 'utf8');
}

function json(rel) {
  return JSON.parse(read(rel));
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

const expectedAnchor = 'ee1032a0822ab8e103f8afe48e5c1859fde65cc9';
const deferred = [
  'performance-representative-budget',
  'platform-posture-continuity'
];

assert(read('VERSION').trim() === '1.5.0', 'VERSION must be 1.5.0');

const lifecycle = json('registry/lifecycle.json');
assert(lifecycle.currentOfficial === '1.5.0', 'currentOfficial must be 1.5.0');
assert(lifecycle.currentStable === '1.5.0', 'currentStable must be 1.5.0');
assert(lifecycle.activeCandidate === null, 'activeCandidate must be null');
assert(lifecycle.plannedNext === '1.5.1', 'plannedNext must be 1.5.1');

const release = lifecycle.releases.find(item => item.version === '1.5.0');
assert(release, 'lifecycle must contain V1.5.0 release');
assert(release.status === 'stable', 'V1.5.0 lifecycle status must be stable');
assert(release.consumerEligible === true, 'V1.5.0 must be consumer eligible');
assert(release.stableBaseline === '1.4.1', 'V1.5.0 Stable baseline must be 1.4.1');
assert(release.runtimeEntrypoint === 'js/glaze-v1.5.0.mjs', 'V1.5.0 runtime entrypoint mismatch');
assert(release.sourceQualificationAnchor === expectedAnchor, 'V1.5.0 source qualification anchor mismatch');
assert(release.deferredFollowUp === 'GLAZE_UI_V1_5_1_HARDENING.md', 'V1.5.1 follow-up must be declared');

const scope = json('contracts/v1.5/stable-scope.json');
assert(scope.version === '1.5.0', 'Stable scope version mismatch');
assert(scope.lifecycle === 'stable', 'Stable scope lifecycle mismatch');
assert(scope.reviewedImplementationAnchor === expectedAnchor, 'Stable scope reviewed anchor mismatch');
assert(scope.qualifiedObligationCount === 16, 'V1.5.0 must contain exactly 16 qualified obligations');
assert(scope.qualifiedObligations.length === 16, 'Qualified-obligation list must contain 16 entries');
assert(scope.deferredObligationCount === 2, 'Exactly two obligations must be deferred to V1.5.1');
assert(scope.deferredToV151.length === 2, 'Deferred-obligation list must contain two entries');
assert(
  JSON.stringify(scope.deferredToV151.map(item => item.id).sort()) === JSON.stringify([...deferred].sort()),
  'Deferred V1.5.1 obligations mismatch'
);
assert(scope.stableClaims.numericPerformanceBudgetV10Measured === false, 'V1.5.0 must not claim numeric Performance Budget v1.0 measurement');
assert(scope.stableClaims.foldablePostureTargetRuntimeAccepted === false, 'V1.5.0 must not claim foldable/posture target-runtime acceptance');
assert(scope.continuityPolicy.presentationBehaviorChangePermittedByPromotion === false, 'Promotion must not permit presentation behavior change');
assert(scope.continuityPolicy.authorizationBehaviorChangePermittedByPromotion === false, 'Promotion must not permit authorization behavior change');

const consumers = json('consumers/registry.json');
assert(consumers.schemaVersion === 8, 'Consumer registry must retain governed schema version 8');
assert(consumers.officialBaseline === '1.5.0', 'Consumer registry official baseline must be 1.5.0');
assert(consumers.requiredConsumerVersion === '1.5.0', 'Consumer registry required version must be 1.5.0');
assert(consumers.officialProductLabel === lifecycle.officialProductLabel, 'Consumer registry label must match lifecycle authority');
assert(consumers.consumers.every(item => item.requiredTargetVersion === '1.5.0'), 'Every registered consumer must require 1.5.0');
assert(consumers.consumers.every(item => item.productionEligible === false), 'Stable design-system promotion must not auto-certify consumers');

const consumerSchema = json('schemas/consumer-registry.schema.json');
assert(consumerSchema.properties?.schemaVersion?.const === 8, 'Consumer registry schema must retain version 8');
assert(String(consumerSchema.title).includes('V1.5'), 'Consumer registry schema title must identify V1.5');

for (const file of ['README.md', 'STABILITY.md', 'ACCEPTANCE.md', 'CONFORMANCE.md', 'CONSUMERS.md']) {
  const text = read(file);
  assert(text.includes('1.5.0'), `${file} must identify V1.5.0 current authority`);
  assert(!text.includes('V1.4 (`1.4.1`) is the current Stable'), `${file} contains stale V1.4.1 current-Stable authority`);
}

// The public Stable entrypoint inherits browser-oriented historical modules, so the
// Node authority verifier checks its release wrapper statically while executing the
// exact reviewed V1.5 resolver directly. The workflow separately proves that the
// reviewed V1.5 behavior sources are byte-identical to the human-reviewed anchor.
const stableRuntime = read('js/glaze-v1.5.0.mjs');
assert(stableRuntime.includes("version: '1.5.0'"), 'Stable runtime must identify version 1.5.0');
assert(stableRuntime.includes("lifecycle: 'stable'"), 'Stable runtime must identify stable lifecycle');
assert(stableRuntime.includes(expectedAnchor), 'Stable runtime must name reviewed implementation anchor');
assert(stableRuntime.includes("'performance-representative-budget'"), 'Stable runtime must disclose deferred performance qualification');
assert(stableRuntime.includes("'platform-posture-continuity'"), 'Stable runtime must disclose deferred posture qualification');
assert(stableRuntime.includes('numericPerformanceBudgetV10AcceptanceClaimed: false'), 'Stable runtime must preserve performance non-claim');
assert(stableRuntime.includes('foldablePostureAcceptanceClaimed: false'), 'Stable runtime must preserve posture non-claim');
assert(stableRuntime.includes("from './glaze-v1.5-resolution.dev.mjs'"), 'Stable runtime must delegate to reviewed V1.5 resolver');
assert(stableRuntime.includes('promoteStableIdentity'), 'Stable runtime must contain bounded Stable identity promotion');

const resolved = resolveGlazeInterface({
  providers: [
    {
      id: 'stable-platform',
      authority: 'platform',
      context: {
        layout: {category: 'expanded'},
        input: {primary: 'keyboard'},
        connectivity: {class: 'online'}
      },
      capabilities: [
        {id: 'connectivity.network', domain: 'connectivity', state: 'available'}
      ]
    },
    {
      id: 'stable-app',
      authority: 'application',
      context: {task: {kind: 'composing'}},
      capabilities: [
        {id: 'application.compose', domain: 'application', state: 'available'}
      ]
    },
    {
      id: 'stable-privacy',
      authority: 'privacy',
      capabilities: [
        {id: 'authorization.data-use', domain: 'authorization', state: 'permission-required'}
      ]
    }
  ],
  actions: [
    {id: 'compose', label: 'Compose', primary: true, requiredCapabilities: ['application.compose']},
    {id: 'sensitive', label: 'Sensitive action', requiredCapabilities: ['authorization.data-use'], consequential: true}
  ],
  destinations: [{id: 'home', label: 'Home'}],
  currentDestinationId: 'home',
  intent: {supportsMultiPane: true}
});

assert(resolved.version === '1.5.0-dev.1', 'Reviewed resolver identity must remain Development at the exact implementation layer');
assert(resolved.lifecycle === 'development', 'Reviewed resolver lifecycle must remain Development at the implementation layer');
assert(resolved.authority.authorizationInferred === false, 'Reviewed resolver must not infer authorization');
assert(resolved.authority.permissionGranted === false, 'Reviewed resolver must not grant permission');
assert(resolved.authority.automaticNavigationAllowed === false, 'Reviewed resolver must not allow automatic navigation');
assert(resolved.authority.automaticPermissionRequestAllowed === false, 'Reviewed resolver must not allow automatic permission requests');
assert(resolved.authority.automaticConsequentialExecutionAllowed === false, 'Reviewed resolver must not allow automatic consequential execution');
assert(resolved.authority.automaticFallbackExecutionAllowed === false, 'Reviewed resolver must not allow automatic fallback execution');
assert(resolved.continuity.taskStateReset === false, 'Reviewed resolver must preserve task state');
assert(resolved.continuity.pageReloadRequired === false, 'Reviewed resolver must not require page reload');

const sensitive = resolved.actions.actions.find(action => action.id === 'sensitive');
assert(sensitive?.state === 'permission-required', 'Privacy-sensitive action must remain permission-required');
assert(sensitive?.enabled === false, 'Privacy-sensitive action must remain disabled');

const summary = summarizeGlazeInterfaceResolution(resolved);
assert(summary.version === '1.5.0-dev.1', 'Reviewed resolver summary identity must remain Development');
assert(summary.lifecycle === 'development', 'Reviewed resolver summary lifecycle must remain Development');
assert(summary.operationalAuthorityGranted === false, 'Reviewed resolver summary must not grant operational authority');

const acceptance = read('acceptance/v1.5-stable.md');
assert(acceptance.includes(expectedAnchor), 'Stable acceptance must name reviewed implementation anchor');
assert(acceptance.includes('performance-representative-budget'), 'Stable acceptance must disclose deferred performance measurement');
assert(acceptance.includes('platform-posture-continuity'), 'Stable acceptance must disclose deferred posture qualification');

const followUp = read('GLAZE_UI_V1_5_1_HARDENING.md');
for (const id of deferred) assert(followUp.includes(id), `V1.5.1 follow-up must contain ${id}`);

console.log('GLAZE UI V1.5.0 Stable authority verification: PASS');
