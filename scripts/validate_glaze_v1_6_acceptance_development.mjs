#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {
  createGlazeV16AcceptanceMatrix,
  describeGlazeV16CorePillars,
  describeGlazeV16GoverningPrinciple,
  glazeV16AcceptanceDevelopmentContract
} from '../js/glaze-v1.6-acceptance.dev.mjs';
import {glazeV16Development} from '../js/glaze-v1.6-development.mjs';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=rel=>fs.readFileSync(path.join(root,rel),'utf8');
const json=rel=>JSON.parse(read(rel));
const assert=(v,m)=>{if(!v)throw new Error(m);};

const contract=json('contracts/v1.6/acceptance.dev.json');
const schema=json('schemas/v1.6-acceptance.schema.json');
const lifecycle=json('registry/lifecycle.json');
const spec=read('GLAZE_UI_V1_6_PLANNED.md');
const acceptance=read('acceptance/v1.6-development.md');

assert(read('VERSION').trim()==='1.5.1','Stable VERSION must remain 1.5.1');
assert(lifecycle.currentOfficial==='1.5.1'&&lifecycle.currentStable==='1.5.1','Stable lifecycle must remain 1.5.1');
assert(lifecycle.activeCandidate===null&&lifecycle.plannedNext===null&&lifecycle.activePatchReleaseCandidate===null,'dev.11 must not mutate lifecycle');
for(const n of [98,99,100])assert(spec.includes(`# ${n}.`),`planned specification missing section ${n}`);

assert(schema.$schema==='https://json-schema.org/draft/2020-12/schema','schema version mismatch');
assert(contract.version==='1.6.0-dev.11'&&contract.lifecycle==='Development'&&contract.consumerEligible===false,'contract boundary mismatch');
assert(JSON.stringify(contract.implementedSpecificationSections)===JSON.stringify([98,99,100]),'implemented section set mismatch');
assert(contract.acceptance.laneCount===24,'acceptance lane count mismatch');
assert(contract.acceptance.exactRevisionRequired===true,'exact revision must be required');
assert(contract.acceptance.missingEvidenceMayInferPass===false,'missing evidence must not pass');
assert(contract.acceptance.revisionMismatchMayPass===false,'revision mismatch must not pass');
assert(contract.acceptance.matrixCompletionEqualsStablePromotion===false,'matrix completion must not equal Stable promotion');
assert(contract.corePillars.length===8,'core pillar count mismatch');
assert(contract.authority.lifecyclePromotionAutomatic===false&&contract.authority.stableStatusGranted===false,'contract must not promote lifecycle');
assert(acceptance.includes('No V1.6 qualification lane is accepted by this document merely because the lane exists.'),'acceptance record must preserve evidence boundary');

assert(glazeV16AcceptanceDevelopmentContract.version==='1.6.0-dev.11','runtime contract version mismatch');
assert(glazeV16AcceptanceDevelopmentContract.acceptanceLanes.length===24,'runtime lane count mismatch');
assert(glazeV16AcceptanceDevelopmentContract.corePillars.length===8,'runtime pillar count mismatch');
assert(glazeV16AcceptanceDevelopmentContract.missingEvidenceMayInferPass===false,'runtime missing evidence must not pass');

assert(glazeV16Development.version==='1.6.0-dev.11','aggregate must identify dev.11');
assert(glazeV16Development.lifecycle==='development'&&glazeV16Development.consumerEligible===false,'aggregate boundary mismatch');
for(let n=1;n<=100;n++)assert(glazeV16Development.implementedSpecificationSections.includes(n),`aggregate missing section ${n}`);

const empty=createGlazeV16AcceptanceMatrix({});
assert(empty.laneCount===24,'empty matrix lane count mismatch');
assert(empty.qualificationEvidenceComplete===false,'matrix without revision/evidence must not complete');
assert(empty.unverifiedCount===24,'empty matrix should leave all lanes unverified');
assert(empty.authority.missingEvidenceInferredPassing===false,'missing evidence must not infer pass');

const revision='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa';
const wrongRevision='bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb';

const mismatch=createGlazeV16AcceptanceMatrix({
  exactRevision:revision,
  evidence:[{
    id:'source-implementation',verified:true,revision:wrongRevision,
    evidenceType:'machine',reference:'CI run 1'
  }]
});
const mismatchLane=mismatch.lanes.find(x=>x.id==='source-implementation');
assert(mismatchLane.status==='unverified','mismatched evidence must remain unverified');
assert(mismatchLane.failureReason==='evidence-revision-mismatch','revision mismatch reason missing');

const wrongType=createGlazeV16AcceptanceMatrix({
  exactRevision:revision,
  evidence:[{
    id:'performance',verified:true,revision,
    evidenceType:'machine',reference:'synthetic source test'
  }]
});
const performanceLane=wrongType.lanes.find(x=>x.id==='performance');
assert(performanceLane.status==='unverified','machine-only performance record must not satisfy representative performance');
assert(performanceLane.failureReason==='evidence-type-not-allowed','wrong performance evidence type reason missing');

const noJustification=createGlazeV16AcceptanceMatrix({
  exactRevision:revision,
  applicability:{'form-factor-transitions':false}
});
const naLane=noJustification.lanes.find(x=>x.id==='form-factor-transitions');
assert(naLane.status==='unverified','not-applicable without justification must remain unverified');

const justifiedNA=createGlazeV16AcceptanceMatrix({
  exactRevision:revision,
  applicability:{'form-factor-transitions':false},
  notApplicableJustifications:{'form-factor-transitions':'No form-factor transition support is claimed for this qualification scope.'}
});
assert(justifiedNA.lanes.find(x=>x.id==='form-factor-transitions').status==='not-applicable','justified N/A disposition should be explicit');
assert(justifiedNA.qualificationEvidenceComplete===false,'one N/A disposition cannot complete otherwise missing evidence');

const evidenceTypeByLane={
  'source-implementation':'machine','design-tokens':'machine','skeleton-system':'machine','loading-behavior':'machine',
  'accessibility':'human','semantic-colors':'machine','reduced-motion':'human','reduced-transparency':'human',
  'increased-contrast':'human','large-text':'human','keyboard-navigation':'human','assistive-technology':'assistive-technology',
  'responsive-layouts':'rendered','form-factor-transitions':'device','performance':'performance','layout-stability':'performance',
  'offline-behavior':'machine','degraded-behavior':'machine','loading-escalation':'machine','component-state-completeness':'machine',
  'privacy-boundaries':'human','authority-boundaries':'human','regression-testing':'machine','representative-rendering':'rendered'
};
const fixtureEvidence=contract.lanes.map((id,index)=>({
  id,verified:true,revision,evidenceType:evidenceTypeByLane[id],reference:`test-fixture-${index+1}`
}));
const completeFixture=createGlazeV16AcceptanceMatrix({exactRevision:revision,evidence:fixtureEvidence});
assert(completeFixture.qualificationEvidenceComplete===true,'complete valid fixture should complete evidence matrix');
assert(completeFixture.readyForGovernedQualificationReview===true,'complete evidence matrix should be review-ready');
assert(completeFixture.authority.lifecyclePromotionAutomatic===false,'complete matrix must not auto-promote lifecycle');
assert(completeFixture.authority.stableStatusGranted===false,'complete matrix must not grant Stable');

const pillars=describeGlazeV16CorePillars();
assert(pillars.count===8&&pillars.summaryOnly===true&&pillars.lifecycleAuthority===false,'pillar summary boundary mismatch');

const principle=describeGlazeV16GoverningPrinciple();
assert(principle.states.length===10,'governing-principle state coverage mismatch');
assert(principle.accessibilityPrecedence===true,'governing principle must preserve accessibility precedence');
assert(principle.performancePrecedenceOverDecoration===true,'governing principle must preserve performance precedence');
assert(principle.truthPreservationRequired===true,'governing principle must preserve truth');

console.log('GLAZE UI V1.6 acceptance-control Development foundation: PASS');
console.log('Implemented sections: 98-100');
console.log('Aggregate implemented sections: 1-100');
console.log('Acceptance lanes: 24');
console.log('Core pillars: 8');
console.log('Stable baseline preserved: 1.5.1');
console.log('Consumer eligible: false');
console.log('Stable promotion automatic: false');
