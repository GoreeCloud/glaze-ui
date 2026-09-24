#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

import {
  resolveGlazeNativeCapability,
  resolveGlazeNativeKit,
  glazeV17NativeGlazeKitsDevelopmentContract
} from '../js/glaze-v1.7-native-glaze-kits.dev.mjs';
import {glazeV17Development} from '../js/glaze-v1.7-development.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const read = rel => fs.readFileSync(path.join(root, rel), 'utf8');
const json = rel => JSON.parse(read(rel));
const assert = (condition, message) => { if (!condition) throw new Error(message); };

const contract = json('contracts/v1.7/native-glaze-kits.dev.json');
const schema = json('schemas/v1.7-native-glaze-kits.schema.json');
const tokens = json('tokens/glaze-v1.7-native-glaze-kits.dev.json');
const lifecycle = json('registry/lifecycle.json');
const stable = read('VERSION').trim();
const spec = read('GLAZE_UI_V1_7_PLANNED.md');
const planned = read('PLANNED-FEATURES.md');
const implemented = read('IMPLEMENTED-FEATURES.md');
const changelog = read('CHANGELOGS.md');

const platforms = ['android-compose','apple-swiftui','web','linux-native'];
const roles = ['surface','action','navigation','focus','input','state','progress','recovery','privacy','security'];

assert(stable === '1.6.0', 'V1.7 dev.8 must preserve GLAZE UI V1.6 / 1.6.0 as current Stable');
assert(lifecycle.currentOfficial === stable && lifecycle.currentStable === stable, 'VERSION/current Stable authority must agree');
assert(lifecycle.activeCandidate === null, 'V1.7 dev.8 must not create an active Candidate');
assert(lifecycle.activePatchReleaseCandidate === null, 'V1.7 dev.8 must not create a patch RC');
assert(lifecycle.plannedNext === null, 'V1.7 dev.8 must not mutate lifecycle plannedNext');

assert(spec.includes('## 9. Native Glaze Kits'), 'V1.7 specification missing Native Glaze Kits section');
for (const phrase of [
  'Android / Jetpack Compose',
  'Apple / SwiftUI',
  'Web',
  'Supported Linux native UI environments',
  'preserve the same semantic vocabulary',
  'platform-native controls and behaviors',
  'mapping of Glaze semantics rather than a visual imitation'
]) {
  assert(spec.includes(phrase), `V1.7 specification missing Section 9 requirement: ${phrase}`);
}

assert(schema.$schema === 'https://json-schema.org/draft/2020-12/schema', 'schema must use JSON Schema 2020-12');
assert(contract.$schema === '../../schemas/v1.7-native-glaze-kits.schema.json', 'contract schema binding mismatch');
assert(contract.version === '1.7.0-dev.8', 'contract version mismatch');
assert(contract.lifecycle === 'Development', 'contract must remain Development');
assert(contract.stableBaseline === '1.6.0', 'contract Stable baseline mismatch');
assert(contract.consumerEligible === false, 'contract must remain non-consumer-eligible');
assert(JSON.stringify(contract.implementedSpecificationSections) === JSON.stringify([9]), 'implemented section set mismatch');
assert(JSON.stringify(contract.platforms) === JSON.stringify(platforms), 'platform catalog mismatch');
assert(JSON.stringify(contract.semanticVocabulary) === JSON.stringify(roles), 'semantic vocabulary mismatch');
assert(Object.keys(contract.platformMappings).length === 4, 'contract must contain four platform mappings');

for (const platform of platforms) {
  const mapping = contract.platformMappings[platform];
  assert(typeof mapping.framework === 'string' && mapping.framework.length > 0, `framework missing: ${platform}`);
  assert(mapping.supportedProfiles.length >= 1, `profile mapping missing: ${platform}`);
  assert(mapping.controlPolicy.includes('native') || platform === 'web', `native/web control policy missing: ${platform}`);
}
for (const required of [
  'platformCapabilityAuthorityRequired',
  'nativeControlMappingAuthorityRequired',
  'privacyAuthorityRequired',
  'securityAuthorityRequired',
  'permissionAuthorityRequired',
  'consentAuthorityRequired',
  'availabilityAuthorityRequired',
  'executionAuthorityRequired'
]) {
  assert(contract.authority[required] === true, `required authority gate missing: ${required}`);
}
for (const denied of [
  'platformCapabilityCreatedByGlaze',
  'nativeControlAvailabilityCreatedByGlaze',
  'privacyTruthCreatedByGlaze',
  'securityTruthCreatedByGlaze',
  'permissionGrantedByGlaze',
  'consentGrantedByGlaze',
  'availabilityTruthCreatedByGlaze',
  'actionExecutionPerformedByGlaze',
  'nativeCertificationImplied',
  'downstreamAdoptionAutomatic',
  'consequentialExecutionAutomatic'
]) {
  assert(contract.authority[denied] === false, `authority boundary weakened: ${denied}`);
}
for (const requirement of [
  'nativeDeviceAcceptanceRequired',
  'renderedAcceptanceRequired',
  'assistiveTechnologyAcceptanceRequired',
  'performanceAcceptanceRequired'
]) {
  assert(contract.acceptanceBoundary[requirement] === true, `acceptance boundary missing: ${requirement}`);
}
for (const source of Object.values(contract.integrationFoundations)) {
  assert(fs.existsSync(path.join(root, source)), `integration foundation missing: ${source}`);
}
for (const source of contract.sourceAuthorities) {
  assert(fs.existsSync(path.join(root, source)), `source authority missing: ${source}`);
}

assert(tokens.version === '1.7.0-dev.8', 'token version mismatch');
assert(tokens.lifecycle === 'Development', 'tokens must remain Development');
assert(tokens.stableBaseline === '1.6.0', 'token Stable baseline mismatch');
assert(tokens.consumerEligible === false, 'tokens must remain non-consumer-eligible');
assert(Object.keys(tokens.platformRoles).length === 4, 'token map must expose four platform roles');
assert(Object.keys(tokens.semanticRoles).length === 10, 'token map must expose ten semantic roles');
assert(tokens.mappingPolicy.semanticVocabulary === 'preserve', 'semantic vocabulary must be preserved');
assert(tokens.mappingPolicy.nativeControlPreference === 'prefer-when-semantics-preserved', 'native control preference mismatch');
assert(tokens.mappingPolicy.crossPlatformVisualImitation === 'not-required', 'native kits must not require cross-platform visual imitation');
assert(tokens.boundaries.presentationOnly === true, 'tokens must remain presentation-only');
assert(tokens.boundaries.nativeCertificationImplied === false, 'tokens must not imply native certification');
assert(tokens.boundaries.downstreamAdoptionAutomatic === false, 'tokens must not manufacture downstream adoption');

const withheld = resolveGlazeNativeCapability({state:'available', authoritative:false});
assert(withheld.acceptedState === 'unknown', 'untrusted native capability must fail closed');
assert(withheld.presentAsAvailable === false, 'untrusted native capability must not present as available');

const previousTaskState = {
  navigationDestination:'settings',
  focusId:'appearance-toggle',
  draftText:'preserve this draft',
  query:'native',
  paneState:{activePane:'detail'}
};

for (const platform of platforms) {
  const mapping = contract.platformMappings[platform];
  const profile = mapping.supportedProfiles[0];
  const resolved = resolveGlazeNativeKit({
    platform,
    profile,
    semanticRole:'surface',
    nativeControl:'PlatformNativeControl',
    nativeControlMappingAuthoritative:true,
    capabilityState:'available',
    capabilityAuthoritative:true,
    previousTaskState
  });

  assert(resolved.platform === platform, `platform mismatch: ${platform}`);
  assert(resolved.mapping.profile === profile, `profile mismatch: ${platform}`);
  assert(resolved.mapping.nativeControl === 'PlatformNativeControl', `native control mapping lost: ${platform}`);
  assert(resolved.mapping.crossPlatformVisualImitationRequired === false, `visual imitation boundary weakened: ${platform}`);
  assert(resolved.capability.presentAsAvailable === true, `authoritative capability lost: ${platform}`);
  assert(resolved.taskState.navigationDestination === 'settings', `navigation continuity lost: ${platform}`);
  assert(resolved.taskState.focusId === 'appearance-toggle', `focus continuity lost: ${platform}`);
  assert(resolved.taskState.draftText === 'preserve this draft', `draft continuity lost: ${platform}`);
  assert(resolved.authority.platformCapabilityCreatedByGlaze === false, `capability authority weakened: ${platform}`);
  assert(resolved.authority.permissionGrantedByGlaze === false, `permission authority weakened: ${platform}`);
  assert(resolved.authority.actionExecutionPerformedByGlaze === false, `execution boundary weakened: ${platform}`);
  assert(resolved.acceptanceBoundary.nativeDeviceAcceptanceRequired === true, `native acceptance boundary lost: ${platform}`);
}

const withheldControl = resolveGlazeNativeKit({
  platform:'android-compose',
  profile:'mobile',
  semanticRole:'action',
  nativeControl:'Button',
  nativeControlMappingAuthoritative:false,
  capabilityState:'unknown'
});
assert(withheldControl.mapping.nativeControl === null, 'untrusted native control mapping must be withheld');
assert(withheldControl.mapping.nativeControlWithheldWithoutAuthority === true, 'withheld native control should be explicit');

for (const input of [
  {platform:'invented-platform',profile:'mobile',semanticRole:'surface'},
  {platform:'linux-native',profile:'mobile',semanticRole:'surface'},
  {platform:'web',profile:'desktop',semanticRole:'invented-role'}
]) {
  let failed = false;
  try { resolveGlazeNativeKit(input); } catch { failed = true; }
  assert(failed, `unsupported native-kit input must fail closed: ${JSON.stringify(input)}`);
}

assert(glazeV17NativeGlazeKitsDevelopmentContract.version === '1.7.0-dev.8', 'runtime contract version mismatch');
assert(glazeV17NativeGlazeKitsDevelopmentContract.lifecycle === 'development', 'runtime contract must remain Development');
assert(glazeV17NativeGlazeKitsDevelopmentContract.stableBaseline === '1.6.0', 'runtime Stable baseline mismatch');
assert(glazeV17NativeGlazeKitsDevelopmentContract.consumerEligible === false, 'runtime must remain non-consumer-eligible');
assert(JSON.stringify(glazeV17NativeGlazeKitsDevelopmentContract.platforms) === JSON.stringify(platforms), 'runtime platform set mismatch');
assert(JSON.stringify(glazeV17NativeGlazeKitsDevelopmentContract.semanticVocabulary) === JSON.stringify(roles), 'runtime semantic vocabulary mismatch');
assert(glazeV17NativeGlazeKitsDevelopmentContract.nativeDeviceAcceptanceImplied === false, 'runtime must not imply native-device acceptance');

assert(glazeV17Development.version === '1.7.0-dev.8', 'aggregate version mismatch');
assert(glazeV17Development.lifecycle === 'development', 'aggregate must remain Development');
assert(glazeV17Development.stableBaseline === '1.6.0', 'aggregate Stable baseline mismatch');
assert(glazeV17Development.consumerEligible === false, 'aggregate must remain non-consumer-eligible');
assert(JSON.stringify(glazeV17Development.implementedSpecificationSections) === JSON.stringify([1,2,3,4,5,6,7,8,9]), 'aggregate section set mismatch');
assert(glazeV17Development.nativeGlazeKitsFoundation === 'js/glaze-v1.7-native-glaze-kits.dev.mjs', 'aggregate missing Section 9 foundation');
assert(glazeV17Development.providerTruthManufactured === false, 'aggregate must preserve provider-truth boundary');

assert(planned.includes('1.7.0-dev.8') && planned.includes('sections to 1–9'), 'planned-feature control must describe dev.8 state');
assert(implemented.includes('Native Glaze Kits — `1.7.0-dev.8`'), 'implemented-feature control missing dev.8');
assert(changelog.includes('1.7.0-dev.8') && changelog.includes('Native Glaze Kits'), 'changelog missing dev.8');

console.log('GLAZE UI V1.7 Native Glaze Kits Development foundation: PASS');
console.log('Implemented section: 9');
console.log('Platform mappings: 4');
console.log('Semantic roles: 10');
console.log('Stable baseline preserved: 1.6.0');
console.log('Consumer eligible: false');
