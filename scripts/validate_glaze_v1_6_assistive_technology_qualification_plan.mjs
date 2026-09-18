#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

import {
  glazeV16Development,
  resolveGlazeAccessibilityProfiles,
  resolveGlazeCapabilityPresentation,
  resolveGlazeCapabilityControl,
  resolveGlazePrivacyPresentation,
  resolveGlazeResponsiveLayout,
  resolveGlazeFocusPresentation,
  resolveGlazeStateContinuity
} from '../js/glaze-v1.6-development.mjs';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=rel=>fs.readFileSync(path.join(root,rel),'utf8');
const json=rel=>JSON.parse(read(rel));
const assert=(value,message)=>{if(!value)throw new Error(message);};

const plan=json('contracts/v1.6/qualification.assistive-technology.plan.json');
const schema=json('schemas/v1.6-assistive-technology-qualification-plan.schema.json');
const acceptance=json('contracts/v1.6/acceptance.dev.json');
const lifecycle=json('registry/lifecycle.json');
const harness=read('reference/v1.6/assistive-technology-qualification.html');
const prepare=read('scripts/prepare_glaze_v1_6_assistive_technology_qualification.py');

assert(read('VERSION').trim()==='1.5.1','Stable VERSION must remain 1.5.1');
assert(lifecycle.currentOfficial==='1.5.1'&&lifecycle.currentStable==='1.5.1','Stable lifecycle must remain 1.5.1');
assert(lifecycle.activeCandidate===null&&lifecycle.plannedNext===null&&lifecycle.activePatchReleaseCandidate===null,'AT tooling must not promote lifecycle');

assert(schema.$schema==='https://json-schema.org/draft/2020-12/schema','AT plan schema dialect mismatch');
assert(plan.schemaVersion===1,'AT plan schemaVersion drifted');
assert(plan.lifecycle==='DevelopmentQualification','AT plan lifecycle mismatch');
assert(plan.sourceRevision==='c7509c79256b04b0aa67cb9dd0737d7588e0ae4a','AT plan must remain bound to frozen V1.6 source');
assert(plan.acceptanceModelVersion==='1.6.0-dev.12','AT acceptance model mismatch');
assert(plan.stableBaseline==='1.5.1'&&plan.consumerEligible===false,'AT Stable/consumer boundary drifted');
assert(plan.evidenceType==='assistive-technology','AT plan evidence type drifted');
assert(plan.primaryLane==='assistive-technology','AT plan primary lane drifted');
assert(JSON.stringify(plan.eligibleSecondaryLanes)==='["accessibility"]','AT secondary lane eligibility drifted');

assert(JSON.stringify(acceptance.evidenceRequirements['assistive-technology'])==='[["assistive-technology"]]','AT acceptance lane requirement drifted');
assert(JSON.stringify(acceptance.evidenceRequirements.accessibility)==='[["machine"],["human","assistive-technology"]]','Accessibility grouped evidence drifted');
assert(JSON.stringify(plan.existingEvidencePrerequisites.accessibility)==='["machine"]','Accessibility prerequisite must remain machine evidence');
assert(Array.isArray(plan.existingEvidencePrerequisites['assistive-technology'])&&plan.existingEvidencePrerequisites['assistive-technology'].length===0,'AT primary lane must not invent a prerequisite');

assert(plan.execution.repositoryLocalOnly===true,'AT review must remain repository-local');
assert(plan.execution.telemetryRequired===false&&plan.execution.remoteAnalysisRequired===false,'AT review must not require telemetry or remote analysis');
assert(plan.execution.realAssistiveTechnologyRequired===true,'real AT must remain required');
assert(plan.execution.assistiveTechnologyNameAndVersionRequired===true,'AT identity must remain required');
assert(plan.execution.reviewerObservationRequired===true,'reviewer observation must remain required');
assert(plan.execution.syntheticSpeechMayQualify===false,'synthetic speech must not qualify');
assert(plan.execution.browserAutomationMayQualify===false,'browser automation must not qualify');
assert(plan.execution.reviewFindingsMustBeRecordedOutsideHarness===true,'AT findings must remain external to the harness');
assert(plan.execution.generatedEvidenceAutomatic===false,'AT evidence generation must remain non-automatic');

for(const key of [
  'assistiveTechnologyEvidenceClaimedByPlan','humanEvidenceClaimed','physicalDeviceEvidenceClaimed',
  'performanceEvidenceClaimed','lifecyclePromotionAutomatic','candidateStatusGranted',
  'releaseCandidateStatusGranted','stableStatusGranted','consumerAcceptanceAutomatic',
  'deploymentAcceptanceAutomatic','productionAcceptanceAutomatic'
]) assert(plan.evidenceBoundary[key]===false,'AT authority boundary must remain false: '+key);

assert(harness.includes("const SOURCE='c7509c79256b04b0aa67cb9dd0737d7588e0ae4a'"),'AT harness frozen source binding missing');
assert(harness.includes("fetch('../../qualification-source.json'"),'AT harness must verify prepared source manifest');
assert(harness.includes('Real assistive-technology review surface only — not acceptance evidence.'),'AT non-evidence notice missing');
assert(harness.includes('cannot detect whether a screen reader or other assistive technology is active'),'AT harness must disclaim AT detection');
assert(harness.includes('aria-live="polite"')&&harness.includes('role="status"'),'AT harness live status semantics missing');
assert(harness.includes('aria-describedby="capability-explanation"'),'AT harness accessible relationship missing');
assert(harness.includes('aria-disabled'), 'AT harness state semantics missing');
assert(harness.includes(':focus-visible'),'AT harness visible focus styling missing');
assert(harness.includes('screenReaderOptimized:true'),'screen-reader optimized profile exercise missing');
assert(harness.includes('resolveGlazeFocusPresentation'),'AT focus semantics exercise missing');
assert(harness.includes('resolveGlazeStateContinuity'),'AT state-continuity exercise missing');
assert(harness.includes('resolveGlazePrivacyPresentation'),'AT privacy semantics exercise missing');
assert(harness.includes('resolveGlazeCapabilityControl'),'AT capability semantics exercise missing');
assert(!/speechSynthesis|SpeechSynthesis|webkitSpeech|SpeechRecognition/i.test(harness),'synthetic speech must not be used as AT evidence');
assert(!/<script[^>]+src\s*=\s*["']https?:\/\//i.test(harness),'AT harness must not load remote scripts');
assert(!/<link[^>]+href\s*=\s*["']https?:\/\//i.test(harness),'AT harness must not load remote styles');
assert(!/<img[^>]+src\s*=\s*["']https?:\/\//i.test(harness),'AT harness must not load remote images');
assert(!/XMLHttpRequest|WebSocket|sendBeacon|navigator\.mediaDevices|getUserMedia/i.test(harness),'AT harness must not emit telemetry or capture media');
assert(!/localStorage|sessionStorage|indexedDB/i.test(harness),'AT reviewer scratch notes must not persist');
assert(!/download\s*=|Blob\s*\(|URL\.createObjectURL/i.test(harness),'AT harness must not create evidence files');
assert(!/evidenceType\s*[:=]\s*['"]assistive-technology['"]/i.test(harness),'AT harness must not manufacture AT evidence');

assert(prepare.includes('SOURCE_REVISION = "c7509c79256b04b0aa67cb9dd0737d7588e0ae4a"'),'AT preparation source binding missing');
assert(prepare.includes('"archive", "--format=tar"'),'AT preparation must materialize frozen source through git archive');
assert(prepare.includes('"assistiveTechnologyEvidenceClaimed": False'),'AT preparation must not claim AT evidence');
assert(prepare.includes('"humanEvidenceClaimed": False'),'AT preparation must not claim human evidence');
assert(prepare.includes('"performanceEvidenceClaimed": False'),'AT preparation must not claim performance evidence');

assert(glazeV16Development.version==='1.6.0-dev.12'&&glazeV16Development.lifecycle==='development','V1.6 aggregate identity mismatch');
assert(glazeV16Development.stableBaseline==='1.5.1'&&glazeV16Development.consumerEligible===false,'V1.6 aggregate Stable/consumer boundary drifted');

const profiles=resolveGlazeAccessibilityProfiles({preferences:{
  screenReaderOptimized:true,strongFocus:true,keyboardFirst:true,largeText:true,reducedMotion:true
}});
assert(profiles.profiles.includes('screen-reader-optimized'),'screen-reader optimized profile missing');
assert(profiles.presentation.screenReaderOptimized===true,'screen-reader optimized presentation flag missing');
assert(profiles.presentation.strongFocusRequired===true,'AT profile must require strong focus');
assert(profiles.presentation.largeTextReflowRequired===true,'AT + large text must require reflow');
assert(profiles.presentation.continuousDecorativeMotionAllowed===false,'AT + Reduced Motion must suppress decorative motion');

const permission=resolveGlazeCapabilityPresentation({state:'permission-required'});
assert(permission.interactive===false&&permission.semanticState==='pending','permission-required must remain semantically pending/noninteractive');
assert(permission.permissionRequestedAutomatically===false&&permission.authority.permissionGranted===false,'AT surface must not imply permission grant');

const restricted=resolveGlazeCapabilityControl({state:'restricted',essential:true,explanationAvailable:true});
assert(restricted.control.visible===true&&restricted.control.enabled===false,'restricted essential control must remain visible but unavailable');
assert(restricted.control.permissionRequestAutomatic===false&&restricted.control.retryAutomatic===false,'AT control must not auto-request or auto-retry');
assert(restricted.authority.consequentialExecutionAutomatic===false,'AT control must not auto-execute');

const untrustedPrivate=resolveGlazePrivacyPresentation({state:'private',authoritative:false});
assert(untrustedPrivate.acceptedState==='unknown','positive privacy state without authority must fail closed');
assert(untrustedPrivate.authority.permissionGrantedByGlaze===false&&untrustedPrivate.authority.consentGrantedByGlaze===false,'privacy semantics must not manufacture consent or permission');

const focus=resolveGlazeFocusPresentation({modality:'assistive-input',focused:true,focusVisible:true,requestedRestoreTarget:'apply',restoreTargetValid:true,material:'glass'});
assert(focus.focus.visible===true&&focus.focus.strongIndicator===true,'assistive-input focus must remain visible and strong');
assert(focus.continuity.focusStealingAllowed===false,'Glaze must not steal assistive-input focus');
assert(focus.continuity.restoration.automaticExecutionByGlaze===false,'Glaze must not automatically execute focus restoration');

const continuity=resolveGlazeStateContinuity({fromState:'before',toState:'after',conceptualIdentitySame:true,accessibilityProfiles:profiles.profiles});
assert(continuity.requirements.preserveFocus===true,'state continuity must preserve focus');
assert(continuity.requirements.preserveAccessibleNameOrUpdateSemantically===true,'state continuity must preserve or semantically update accessible names');
assert(continuity.accessibility.motionRequiredToUnderstandState===false,'motion must not be required to understand AT-reviewed state');

for(const environment of ['compact','expanded']){
  const layout=resolveGlazeResponsiveLayout({
    environment,viewingDistance:'near',inputMode:'assistive-input',
    posture:environment==='compact'?'folded':'flat',contentDensity:'standard',
    task:'editing',accessibilityProfiles:profiles.profiles
  });
  assert(layout.continuity.currentLocationPreserved===true&&layout.continuity.userEnteredDataPreserved===true,'AT responsive review must preserve task continuity: '+environment);
  assert(layout.continuity.focusPreservedWherePractical===true,'AT responsive review must preserve focus where practical: '+environment);
  assert(layout.authority.presentationOnly===true,'responsive layout must remain presentation-only: '+environment);
}

console.log('GLAZE UI V1.6 assistive-technology qualification review control: PASS');
console.log('Frozen source: '+plan.sourceRevision);
console.log('Primary lane: assistive-technology');
console.log('Eligible secondary lane: accessibility');
console.log('Real assistive technology required: true');
console.log('Synthetic speech qualifies: false');
console.log('Browser automation qualifies: false');
console.log('Automatic AT evidence generation: false');
console.log('Stable baseline preserved: 1.5.1');
