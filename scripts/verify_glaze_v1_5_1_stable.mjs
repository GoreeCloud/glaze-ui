#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

import {
  resolveGlazeInterface as resolveReviewedGlazeInterface,
  summarizeGlazeInterfaceResolution as summarizeReviewedGlazeInterfaceResolution
} from '../js/glaze-v1.5-resolution.dev.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const read = rel => fs.readFileSync(path.join(root, rel), 'utf8');
const json = rel => JSON.parse(read(rel));
const assert = (condition, message) => { if (!condition) throw new Error(message); };

const reviewedImplementationAnchor = 'ee1032a0822ab8e103f8afe48e5c1859fde65cc9';
const qualifiedAnchor = '5b59d0e36950d737dba35b58ae58058684e0831b';
const qualificationIntegrationCommit = 'f7ef915f0aabea6cf92748018f2220a99e3a9c92';
const rcIntegrationCommit = 'a9c93506dd062d29c6c894940b71d060e8c39110';

assert(read('VERSION').trim() === '1.5.1', 'VERSION must identify GLAZE UI 1.5.1 Stable');

const lifecycle = json('registry/lifecycle.json');
assert(lifecycle.currentOfficial === '1.5.1', 'lifecycle currentOfficial must be 1.5.1');
assert(lifecycle.currentStable === '1.5.1', 'lifecycle currentStable must be 1.5.1');
assert(lifecycle.activeCandidate === null, 'Stable lifecycle must not retain an active Candidate');
assert(lifecycle.activePatchReleaseCandidate === null, 'Stable lifecycle must not retain an active patch RC');

const stable = lifecycle.releases.find(item => item.version === '1.5.1');
assert(stable, 'lifecycle must contain 1.5.1');
assert(stable.status === 'stable', '1.5.1 lifecycle status must be stable');
assert(stable.consumerEligible === true, '1.5.1 must be consumer eligible as a shared Stable release');
assert(stable.stableBaseline === '1.5.0', '1.5.1 Stable baseline must be 1.5.0');
assert(stable.contract === 'GLAZE_UI_V1_5.md', '1.5.1 must retain the V1.5 family contract');
assert(stable.qualification === 'contracts/v1.5.1/stable-scope.json', '1.5.1 qualification authority mismatch');
assert(stable.acceptance === 'acceptance/v1.5.1-stable.md', '1.5.1 acceptance authority mismatch');
assert(stable.runtimeEntrypoint === 'js/glaze-v1.5.1.mjs', '1.5.1 runtime entrypoint mismatch');
assert(stable.sourceQualificationAnchor === qualifiedAnchor, '1.5.1 qualification anchor mismatch');

const priorStable = lifecycle.releases.find(item => item.version === '1.5.0');
assert(priorStable?.status === 'stable', '1.5.0 must remain retained Stable rollback provenance');
assert(priorStable?.consumerEligible === true, '1.5.0 historical Stable record must remain consumer-eligible history');
assert(priorStable?.sourceQualificationAnchor === reviewedImplementationAnchor, '1.5.0 reviewed implementation anchor drift');

const rc = lifecycle.releases.find(item => item.version === '1.5.1-rc.1');
assert(rc?.status === 'superseded-release-candidate', '1.5.1-rc.1 must be retained as superseded Release Candidate history');
assert(rc?.consumerEligible === false, 'historical RC must remain non-consumer-eligible');
assert(rc?.sourceQualificationAnchor === qualifiedAnchor, 'historical RC qualification anchor drift');

const scope = json('contracts/v1.5.1/stable-scope.json');
assert(scope.version === '1.5.1', 'Stable scope version mismatch');
assert(scope.releaseLifecycle === 'Stable', 'Stable scope lifecycle mismatch');
assert(scope.stableBaseline === '1.5.0', 'Stable scope rollback baseline mismatch');
assert(scope.consumerEligible === true, 'Stable scope consumer eligibility mismatch');
assert(scope.reviewedImplementationAnchor === reviewedImplementationAnchor, 'Stable scope reviewed implementation anchor mismatch');
assert(scope.sourceQualificationAnchor === qualifiedAnchor, 'Stable scope qualification anchor mismatch');
assert(scope.qualificationIntegrationCommit === qualificationIntegrationCommit, 'Stable scope qualification integration mismatch');
assert(scope.releaseCandidateIntegrationCommit === rcIntegrationCommit, 'Stable scope RC integration mismatch');
assert(scope.runtimeEntrypoint === 'js/glaze-v1.5.1.mjs', 'Stable scope runtime mismatch');
assert(scope.qualification?.inheritedV150ObligationCount === 16, 'Stable scope must retain 16 inherited V1.5.0 obligations');
assert(scope.qualification?.v151AcceptedObligationCount === 2, 'Stable scope must contain two accepted V1.5.1 obligations');
assert(scope.qualification?.totalAcceptedObligationCount === 18, 'Stable scope must contain 18 total accepted obligations');
const accepted = scope.qualification?.v151AcceptedObligations;
assert(Array.isArray(accepted) && accepted.length === 2, 'Stable scope must enumerate exactly two V1.5.1 obligations');
for (const id of ['performance-representative-budget', 'platform-posture-continuity']) {
  const item = accepted.find(entry => entry.id === id);
  assert(item?.status === 'accepted', `${id} must be accepted in Stable scope`);
  assert(item?.boundRevision === qualifiedAnchor, `${id} exact revision mismatch`);
}
assert(accepted.find(item => item.id === 'performance-representative-budget')?.reviewRecord === 'PR #230 comment 5697516074', 'Performance review provenance mismatch');
const posture = accepted.find(item => item.id === 'platform-posture-continuity');
assert(posture?.reviewRecord === 'PR #230 comment 5705230782', 'Posture review provenance mismatch');
assert(posture?.approvalReference === 'GCU-ADR-GLAZE-V151-POSTURE-TR-001', 'Posture target-runtime approval mismatch');
assert(scope.continuity?.qualifiedV151SourceChangedByStablePromotion === false, 'Stable promotion must not claim qualified source change');
assert(scope.continuity?.v150PresentationBehaviorChanged === false, 'Stable promotion must not change reviewed V1.5 presentation behavior');
assert(scope.continuity?.authorizationBehaviorChanged === false, 'Stable promotion must not change authorization behavior');
assert(scope.continuity?.qualificationEvidenceReboundToStableRevision === false, 'Qualification evidence must remain bound to its real source revision');
assert(scope.stableClaims?.downstreamConsumerAcceptanceAutomatic === false, 'Stable must not auto-accept downstream consumers');
assert(scope.stableClaims?.tagPublicationAutomatic === false, 'Stable must not auto-publish a tag');
assert(scope.stableClaims?.githubReleasePublicationAutomatic === false, 'Stable must not auto-publish a GitHub Release');
assert(scope.stableClaims?.deploymentAcceptanceAutomatic === false, 'Stable must not auto-accept deployment');
assert(scope.stableClaims?.productionAcceptanceAutomatic === false, 'Stable must not auto-accept production');

const consumers = json('consumers/registry.json');
assert(consumers.officialBaseline === '1.5.1', 'Consumer registry officialBaseline must be 1.5.1');
assert(consumers.requiredConsumerVersion === '1.5.1', 'Consumer registry requiredConsumerVersion must be 1.5.1');
assert(consumers.consumers.every(item => item.requiredTargetVersion === '1.5.1'), 'Every consumer must require current Stable 1.5.1');
assert(consumers.consumers.every(item => item.productionEligible === false), 'Shared Stable promotion must not make any consumer production eligible');

const acceptance = read('acceptance/v1.5.1-stable.md');
for (const token of [reviewedImplementationAnchor, qualifiedAnchor, qualificationIntegrationCommit, rcIntegrationCommit, '5697516074', '5705230782', 'GCU-ADR-GLAZE-V151-POSTURE-TR-001']) {
  assert(acceptance.includes(token), `Stable acceptance missing provenance ${token}`);
}
assert(acceptance.includes('does not establish an immutable `v1.5.1` tag'), 'Stable acceptance must preserve publication boundary');

const hardening = read('GLAZE_UI_V1_5_1_HARDENING.md');
assert(hardening.includes('**Lifecycle:** Stable qualification record'), 'V1.5.1 hardening record must reflect Stable qualification state');
assert(hardening.includes(qualifiedAnchor), 'V1.5.1 hardening record must preserve qualification anchor');
assert(hardening.includes('5697516074') && hardening.includes('5705230782'), 'V1.5.1 hardening record must preserve review provenance');

const readme = read('README.md');
assert(readme.includes('Machine version: **1.5.1**'), 'README must identify 1.5.1');
assert(readme.includes('js/glaze-v1.5.1.mjs'), 'README must identify current Stable runtime');
assert(readme.includes('1.5.0') && readme.includes('rollback'), 'README must preserve 1.5.0 rollback boundary');

const features = read('FEATURES.md');
assert(features.includes('# GLAZE UI V1.5 — Features'), 'FEATURES.md must identify the current V1.5 Stable family');
assert(features.includes('machine version `1.5.1`'), 'FEATURES.md must identify current Stable machine version 1.5.1');
assert(features.includes('contracts/v1.5.1/stable-scope.json'), 'FEATURES.md must identify current V1.5.1 Stable scope');
assert(!features.includes('# GLAZE UI V1.1 — Features'), 'FEATURES.md must not retain the obsolete V1.1 current heading');

const specifications = read('SPECIFICATIONS.md');
assert(specifications.includes('# GLAZE UI V1.5 — Specifications'), 'SPECIFICATIONS.md must identify the current V1.5 Stable family');
assert(specifications.includes('**Machine version:** `1.5.1`'), 'SPECIFICATIONS.md must identify current Stable machine version 1.5.1');
assert(specifications.includes('contracts/v1.5.1/stable-scope.json'), 'SPECIFICATIONS.md must identify current V1.5.1 Stable scope');
assert(!specifications.includes('# GLAZE UI V1.2 — Specifications'), 'SPECIFICATIONS.md must not retain the obsolete V1.2 current heading');

const contributing = read('CONTRIBUTING.md');
assert(contributing.includes("GLAZE UI V1.5 (`1.5.1`) is GoreeCloud's current Official, Stable"), 'CONTRIBUTING.md must identify current Stable 1.5.1');
assert(contributing.includes('V1.5.0 is the immediate known-good Stable rollback baseline'), 'CONTRIBUTING.md must preserve 1.5.0 rollback baseline');

const adoption = read('ADOPTION.md');
assert(adoption.includes('current Glaze UI adoption target is **GLAZE UI V1.5** (`1.5.1`)'), 'ADOPTION.md must identify current 1.5.1 adoption target');
assert(adoption.includes('V1.5.0 (`1.5.0`) is the immediate known-good Stable rollback baseline'), 'ADOPTION.md must preserve 1.5.0 rollback baseline');

const enforcement = read('ENFORCEMENT.md');
assert(enforcement.includes('current Glaze UI enforcement and consumer-conformance target is **GLAZE UI V1.5** (`1.5.1`)'), 'ENFORCEMENT.md must identify current 1.5.1 enforcement target');
assert(enforcement.includes('contracts/v1.5.1/stable-scope.json'), 'ENFORCEMENT.md must identify current V1.5.1 Stable scope');

const websiteReadme = read('website/README.md');
assert(websiteReadme.includes('current Stable Glaze UI product identity is **GLAZE UI V1.5 — Contextual + Capability Awareness** (`1.5.1`)'), 'website/README.md must identify current Stable 1.5.1');
assert(websiteReadme.includes('V1.5.0 / `1.5.0` is the retained immediate Stable rollback baseline'), 'website/README.md must preserve 1.5.0 rollback baseline');

const iconConstruction = read('ICON_CONSTRUCTION.md');
assert(iconConstruction.includes('**Current Stable product authority:** GLAZE UI V1.5 / `1.5.1`.'), 'ICON_CONSTRUCTION.md must identify current Stable 1.5.1 product authority');
assert(iconConstruction.includes('Current product lifecycle authority is `1.5.1`'), 'ICON_CONSTRUCTION.md must separate subsystem revision from current product lifecycle');

const iconIdentity = read('ICON_IDENTITY.md');
assert(iconIdentity.includes('**Current Stable product authority:** GLAZE UI V1.5 / `1.5.1`.'), 'ICON_IDENTITY.md must identify current Stable 1.5.1 product authority');
assert(iconIdentity.includes('Current product lifecycle authority is `1.5.1`'), 'ICON_IDENTITY.md must separate subsystem revision from current product lifecycle');

const stability = read('STABILITY.md');
assert(stability.includes('`1.5.1`'), 'STABILITY.md must identify current Stable 1.5.1');
assert(stability.includes('`1.5.0`'), 'STABILITY.md must identify 1.5.0 rollback baseline');

const conformance = read('CONFORMANCE.md');
assert(conformance.includes('`1.5.1`'), 'CONFORMANCE.md must identify current 1.5.1 target');
assert(conformance.includes('eighteen') || conformance.includes('18'), 'CONFORMANCE.md must identify complete shared qualification count');

const consumersGuide = read('CONSUMERS.md');
assert(consumersGuide.includes('(`1.5.1`)'), 'CONSUMERS.md must identify current 1.5.1 target');
assert(consumersGuide.includes('Fresh repository-local V1.5 adoption and acceptance evidence is required'), 'CONSUMERS.md must preserve repository-local acceptance boundary');

// The public Stable runtime inherits browser-oriented V1.4.1 modules through V1.5.0.
// Do not execute that browser entrypoint in a Node-only CI process. Validate the
// wrapper contract statically, then exercise the exact reviewed V1.5 resolver
// directly using the same Node-safe pattern as the retained V1.5.0 verifier.
const stableRuntime = read('js/glaze-v1.5.1.mjs');
for (const token of [
  "export * from './glaze-v1.5.0.mjs'",
  "from './glaze-v1.5.0.mjs'",
  "version: '1.5.1'",
  "lifecycle: 'stable'",
  "stableBaseline: '1.5.0'",
  'qualifiedStabilizationObligations: 18',
  `reviewedImplementationAnchor: REVIEWED_IMPLEMENTATION_ANCHOR`,
  `sourceQualificationAnchor: V151_QUALIFICATION_ANCHOR`,
  'authorizationInferred: false',
  'permissionRequestAutomatic: false',
  'automaticNavigationAllowed: false',
  'consequentialExecutionAutomatic: false',
  'fallbackExecutionAutomatic: false',
  'downstreamConsumerAcceptanceAutomatic: false',
  "if (key === 'version' && candidate === '1.5.0')",
  "promoted[key] = '1.5.1'"
]) {
  assert(stableRuntime.includes(token), `Stable runtime wrapper missing required contract token: ${token}`);
}
assert(stableRuntime.includes(reviewedImplementationAnchor), 'Stable runtime wrapper reviewed implementation anchor mismatch');
assert(stableRuntime.includes(qualifiedAnchor), 'Stable runtime wrapper qualification anchor mismatch');
assert(stableRuntime.includes(qualificationIntegrationCommit), 'Stable runtime wrapper qualification integration mismatch');
assert(stableRuntime.includes(rcIntegrationCommit), 'Stable runtime wrapper RC integration mismatch');

const reviewedResolved = resolveReviewedGlazeInterface({
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

assert(reviewedResolved.version === '1.5.0-dev.1', 'Reviewed implementation identity must remain Development beneath Stable wrappers');
assert(reviewedResolved.lifecycle === 'development', 'Reviewed implementation lifecycle must remain Development beneath Stable wrappers');
assert(reviewedResolved.authority.authorizationInferred === false, 'Reviewed resolver must not infer authorization');
assert(reviewedResolved.authority.permissionGranted === false, 'Reviewed resolver must not grant permission');
assert(reviewedResolved.authority.automaticNavigationAllowed === false, 'Reviewed resolver must not allow automatic navigation');
assert(reviewedResolved.authority.automaticPermissionRequestAllowed === false, 'Reviewed resolver must not allow automatic permission requests');
assert(reviewedResolved.authority.automaticConsequentialExecutionAllowed === false, 'Reviewed resolver must not allow automatic consequential execution');
assert(reviewedResolved.authority.automaticFallbackExecutionAllowed === false, 'Reviewed resolver must not allow automatic fallback execution');
assert(reviewedResolved.continuity.taskStateReset === false, 'Reviewed resolver must preserve task state');
assert(reviewedResolved.continuity.pageReloadRequired === false, 'Reviewed resolver must not require page reload');

const sensitive = reviewedResolved.actions.actions.find(action => action.id === 'sensitive');
assert(sensitive?.state === 'permission-required', 'Privacy-sensitive action must remain permission-required');
assert(sensitive?.enabled === false, 'Privacy-sensitive action must remain disabled');

const reviewedSummary = summarizeReviewedGlazeInterfaceResolution(reviewedResolved);
assert(reviewedSummary.operationalAuthorityGranted === false, 'Reviewed resolver summary must not grant operational authority');

console.log('GLAZE UI V1.5.1 Stable authority verification: PASS');
console.log(`Reviewed V1.5 implementation anchor: ${reviewedImplementationAnchor}`);
console.log(`V1.5.1 qualification anchor: ${qualifiedAnchor}`);
console.log('Accepted shared qualification obligations: 18');
console.log('Immediate rollback baseline: 1.5.0');
console.log('Downstream consumer acceptance automatic: false');
console.log('Tag/GitHub Release publication automatic: false');