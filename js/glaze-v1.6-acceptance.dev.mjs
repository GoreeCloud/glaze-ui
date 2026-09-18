/* GLAZE UI V1.6 — Development acceptance-control foundation.
 *
 * This module defines the V1.6 acceptance matrix and final design principles.
 * It is non-consumer-eligible Development source. It evaluates supplied,
 * revision-bound evidence; it does not manufacture evidence or promote lifecycle.
 */

const ACCEPTANCE_LANES = Object.freeze([
  ['source-implementation',['machine']],
  ['design-tokens',['machine']],
  ['skeleton-system',['machine','rendered']],
  ['loading-behavior',['machine','rendered']],
  ['accessibility',['machine','human','assistive-technology']],
  ['semantic-colors',['machine','rendered']],
  ['reduced-motion',['machine','rendered','human']],
  ['reduced-transparency',['machine','rendered','human']],
  ['increased-contrast',['machine','rendered','human']],
  ['large-text',['machine','rendered','human']],
  ['keyboard-navigation',['machine','human']],
  ['assistive-technology',['assistive-technology']],
  ['responsive-layouts',['machine','rendered','device']],
  ['form-factor-transitions',['device','rendered']],
  ['performance',['performance']],
  ['layout-stability',['machine','performance','rendered']],
  ['offline-behavior',['machine','rendered']],
  ['degraded-behavior',['machine','rendered']],
  ['loading-escalation',['machine','rendered']],
  ['component-state-completeness',['machine','rendered']],
  ['privacy-boundaries',['machine','human']],
  ['authority-boundaries',['machine','human']],
  ['regression-testing',['machine','rendered']],
  ['representative-rendering',['rendered','device','human']]
].map(([id,evidenceTypes])=>Object.freeze({id,evidenceTypes:Object.freeze(evidenceTypes)})));

const CORE_PILLARS = Object.freeze([
  'skeleton-motion',
  'perceived-performance',
  'state-clarity',
  'accessibility-expansion',
  'motion-coherence',
  'material-intelligence',
  'interaction-continuity',
  'design-system-enforcement'
]);

const GOVERNING_PRINCIPLE = 'Waiting, changing, adapting, loading, failing, recovering, and transitioning must be as intentionally designed as the final static interface.';

function plainObject(v){return Boolean(v)&&typeof v==='object'&&!Array.isArray(v)&&Object.getPrototypeOf(v)===Object.prototype;}
function text(v){return String(v??'').trim();}
function validRevision(v){return /^[0-9a-f]{40}$/.test(text(v));}
function recordsById(records){
  const out=new Map();
  if(!Array.isArray(records))return out;
  for(const raw of records.slice(0,500)){
    if(!plainObject(raw))continue;
    const id=text(raw.id);
    if(id&&!out.has(id))out.set(id,raw);
  }
  return out;
}

export function createGlazeV16AcceptanceMatrix(input={}){
  if(!plainObject(input))throw new TypeError('Acceptance-matrix input must be a plain object');

  const exactRevision=validRevision(input.exactRevision)?text(input.exactRevision):null;
  const evidence=recordsById(input.evidence);
  const applicability=plainObject(input.applicability)?input.applicability:{};
  const notApplicableJustifications=plainObject(input.notApplicableJustifications)?input.notApplicableJustifications:{};

  const lanes=ACCEPTANCE_LANES.map(def=>{
    const applicable=applicability[def.id]!==false;
    const record=evidence.get(def.id);
    const justification=text(notApplicableJustifications[def.id]);

    if(!applicable){
      return Object.freeze({
        id:def.id,
        applicable:false,
        status:justification?'not-applicable':'unverified',
        allowedEvidenceTypes:def.evidenceTypes,
        evidenceReference:null,
        evidenceType:null,
        evidenceRevision:null,
        failureReason:justification?null:'not-applicable-requires-justification'
      });
    }

    if(!record){
      return Object.freeze({
        id:def.id,applicable:true,status:'unverified',allowedEvidenceTypes:def.evidenceTypes,
        evidenceReference:null,evidenceType:null,evidenceRevision:null,failureReason:'missing-evidence'
      });
    }

    const evidenceRevision=validRevision(record.revision)?text(record.revision):null;
    const evidenceType=text(record.evidenceType).toLowerCase();
    const reference=text(record.reference);
    const revisionMatches=Boolean(exactRevision&&evidenceRevision===exactRevision);
    const typeAllowed=def.evidenceTypes.includes(evidenceType);
    const verified=record.verified===true&&revisionMatches&&typeAllowed&&Boolean(reference);

    let failureReason=null;
    if(record.verified!==true)failureReason='evidence-not-verified';
    else if(!exactRevision)failureReason='matrix-exact-revision-missing';
    else if(!evidenceRevision)failureReason='evidence-revision-invalid';
    else if(!revisionMatches)failureReason='evidence-revision-mismatch';
    else if(!typeAllowed)failureReason='evidence-type-not-allowed';
    else if(!reference)failureReason='evidence-reference-missing';

    return Object.freeze({
      id:def.id,applicable:true,status:verified?'verified':'unverified',
      allowedEvidenceTypes:def.evidenceTypes,
      evidenceReference:reference||null,evidenceType:evidenceType||null,
      evidenceRevision,failureReason
    });
  });

  const blocking=lanes.filter(lane=>!['verified','not-applicable'].includes(lane.status));
  const qualificationEvidenceComplete=Boolean(exactRevision)&&blocking.length===0;

  return Object.freeze({
    version:'1.6.0-dev.11',
    lifecycle:'development',
    stableBaseline:'1.5.1',
    consumerEligible:false,
    exactRevision,
    lanes:Object.freeze(lanes),
    laneCount:lanes.length,
    verifiedCount:lanes.filter(l=>l.status==='verified').length,
    notApplicableCount:lanes.filter(l=>l.status==='not-applicable').length,
    unverifiedCount:lanes.filter(l=>l.status==='unverified').length,
    qualificationEvidenceComplete,
    readyForGovernedQualificationReview:qualificationEvidenceComplete,
    blockingLaneIds:Object.freeze(blocking.map(l=>l.id)),
    authority:Object.freeze({
      evidenceManufactured:false,
      staleEvidenceAccepted:false,
      mismatchedRevisionAccepted:false,
      missingEvidenceInferredPassing:false,
      lifecyclePromotionAutomatic:false,
      stableStatusGranted:false,
      consumerAcceptanceAutomatic:false,
      deploymentAcceptanceAutomatic:false,
      productionAcceptanceAutomatic:false
    })
  });
}

export function describeGlazeV16CorePillars(){
  return Object.freeze({
    version:'1.6.0-dev.11',
    lifecycle:'development',
    pillars:CORE_PILLARS,
    count:CORE_PILLARS.length,
    summaryOnly:true,
    lifecycleAuthority:false
  });
}

export function describeGlazeV16GoverningPrinciple(){
  return Object.freeze({
    version:'1.6.0-dev.11',
    lifecycle:'development',
    principle:GOVERNING_PRINCIPLE,
    states:Object.freeze([
      'before-content-loads','while-content-loads','after-content-loads',
      'while-content-updates','connectivity-lost','capability-unavailable',
      'operation-failed','accessibility-simplified','form-factor-changed',
      'resources-constrained'
    ]),
    desiredQualities:Object.freeze([
      'alive-without-distraction','adaptive-without-unpredictability',
      'beautiful-without-sacrificing-clarity',
      'sophisticated-without-sacrificing-accessibility-or-performance'
    ]),
    accessibilityPrecedence:true,
    performancePrecedenceOverDecoration:true,
    truthPreservationRequired:true
  });
}

export const glazeV16AcceptanceDevelopmentContract=Object.freeze({
  version:'1.6.0-dev.11',
  lifecycle:'development',
  stableBaseline:'1.5.1',
  consumerEligible:false,
  acceptanceLanes:ACCEPTANCE_LANES,
  corePillars:CORE_PILLARS,
  governingPrinciple:GOVERNING_PRINCIPLE,
  exactRevisionRequired:true,
  evidenceReferenceRequired:true,
  notApplicableRequiresJustification:true,
  missingEvidenceMayInferPass:false,
  revisionMismatchMayPass:false,
  lifecyclePromotionAutomatic:false,
  authorityBoundary:'qualification-control-only'
});
