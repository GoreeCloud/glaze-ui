#!/usr/bin/env python3
"""Fail-closed validation for the Glaze UI V1.4 accessibility qualification support slice."""
from __future__ import annotations
import importlib.util, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PLAN=ROOT/"contracts"/"v1.4"/"accessibility-qualification.candidate.json"
SCHEMA=ROOT/"contracts"/"v1.4"/"accessibility-qualification-evidence.schema.candidate.json"
COMPOSITION=ROOT/"contracts"/"v1.4"/"accessibility-composition.candidate.json"
EVALUATOR=ROOT/"scripts"/"evaluate_glaze_v1_4_accessibility_qualification.py"
PACKET_GENERATOR=ROOT/"scripts"/"prepare_glaze_v1_4_accessibility_qualification_packet.py"
OBSERVATION_CAPTURE=ROOT/"js"/"glaze-v1.4-accessibility-observation-capture.candidate.mjs"
OBSERVATION_REFERENCE=ROOT/"reference"/"glaze-v1.4-accessibility-observation-capture.candidate.html"
OBSERVATION_REFERENCE_RUNTIME=ROOT/"reference"/"glaze-v1.4-accessibility-observation-capture.candidate.mjs"
TEMPLATE=ROOT/"evidence"/"v1.4"/"templates"/"accessibility-qualification-record.candidate.json"
REGRESSION=ROOT/"tests"/"test_glaze_v1_4_accessibility_qualification.py"
PACKET_REGRESSION=ROOT/"tests"/"test_glaze_v1_4_accessibility_qualification_packet.py"
OBSERVATION_REGRESSION=ROOT/"tests"/"glaze-v1.4-accessibility-observation-capture.test.mjs"
DOCUMENTATION=ROOT/"docs"/"GLAZE_UI_V1_4_ACCESSIBILITY_QUALIFICATION.md"
VERSION=ROOT/"VERSION"
REQUIRED_SCENARIOS=["source-and-runtime-identity","multi-preference-composition","reduced-transparency-solid-fallback","increased-contrast-separation","reduced-motion-motion-suppression","forced-colors-system-color-path","large-text-zoom-reflow","keyboard-focus-order","color-independent-semantic-state"]
CONDITIONAL={"screenReaderClaimed":"screen-reader-semantics-and-announcements","voiceControlClaimed":"voice-control-purpose-and-operation","switchControlClaimed":"switch-control-operability"}
SOURCE_ARTIFACTS={"accessibilityComposition":"contracts/v1.4/accessibility-composition.candidate.json","evidenceSchema":"contracts/v1.4/accessibility-qualification-evidence.schema.candidate.json","evaluator":"scripts/evaluate_glaze_v1_4_accessibility_qualification.py","packetGenerator":"scripts/prepare_glaze_v1_4_accessibility_qualification_packet.py","observationCaptureRuntime":"js/glaze-v1.4-accessibility-observation-capture.candidate.mjs","observationCaptureReference":"reference/glaze-v1.4-accessibility-observation-capture.candidate.html","observationCaptureReferenceRuntime":"reference/glaze-v1.4-accessibility-observation-capture.candidate.mjs","validator":"scripts/validate_glaze_v1_4_accessibility_qualification.py","recordTemplate":"evidence/v1.4/templates/accessibility-qualification-record.candidate.json","regression":"tests/test_glaze_v1_4_accessibility_qualification.py","packetRegression":"tests/test_glaze_v1_4_accessibility_qualification_packet.py","observationCaptureRegression":"tests/glaze-v1.4-accessibility-observation-capture.test.mjs","documentation":"docs/GLAZE_UI_V1_4_ACCESSIBILITY_QUALIFICATION.md"}
EVIDENCE_PATTERN=r"^evidence\+sha256:[0-9a-f]{64}:[A-Za-z0-9][A-Za-z0-9._+-]*(?::[A-Za-z0-9][A-Za-z0-9._+-]*)*(?:/[A-Za-z0-9][A-Za-z0-9._+-]*(?::[A-Za-z0-9][A-Za-z0-9._+-]*)*)*$"

def fail(m): raise SystemExit(f"Glaze UI V1.4 accessibility qualification validation failed: {m}")
def load(path):
    try:v=json.loads(path.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as e:fail(f"{path.relative_to(ROOT)} is unreadable or invalid JSON: {e}")
    if not isinstance(v,dict):fail(f"{path.relative_to(ROOT)} must contain a JSON object")
    return v
def true(c,k,s):
    if c.get(k) is not True:fail(f"{s}.{k} must remain true")
def false(c,k,s):
    if c.get(k) is not False:fail(f"{s}.{k} must remain false")

def validate_plan(p):
    expected={"schemaVersion":1,"id":"goreecloud.glaze-ui.v1.4.accessibility-qualification.candidate","targetVersion":"1.4.0-candidate","releaseLifecycle":"proposed","artifactLifecycle":"qualification-support-candidate","lifecycleAuthority":False,"consumerEligible":False,"sourceStable":"1.3.0","qualificationApiStability":"candidate-not-frozen"}
    for k,v in expected.items():
        if p.get(k)!=v:fail(f"{k} drifted from candidate qualification boundary")
    if p.get("sourceArtifacts")!=SOURCE_ARTIFACTS:fail("sourceArtifacts drifted from governed qualification support artifacts")
    if p.get("evaluatorDispositions")!=["blocked","review-ready","failed","accepted"]:fail("evaluator disposition vocabulary drifted")
    if p.get("requiredScenarios")!=REQUIRED_SCENARIOS:fail("required scenario vocabulary drifted")
    if p.get("claimConditionalScenarios")!=CONDITIONAL:fail("claim-conditional scenario mapping drifted")
    policy=p.get("evaluationPolicy",{})
    for k in ("exactSourceRevisionRequired","exactSourceTreeRevisionRequired","sourceAndTreeMustBeNonPlaceholderForReviewReadyOrAccepted","deterministicEvaluation","failClosed","humanOrCombinedReviewRequiredForAcceptance","unresolvedHighOrCriticalIssueBlocksAcceptance","passScenarioRequiresEvidenceReferences","contentAddressedEvidenceReferencesRequired","acceptedHumanReviewRequiresImmutableAuthorityEvidence","acceptedHumanReviewRequiresImmutableReviewEvidence","reviewEvidenceDistinctFromQualificationEvidenceRequired","acceptedHumanReviewTimestampRequired","reviewCannotPredateObservation","futureDatedReviewRejected","allRequiredScenariosMustPass","allClaimedAssistiveTechnologyScenariosMustPass","acceptedAccessibilityQualificationDoesNotGrantLifecycleGate"):true(policy,k,"evaluationPolicy")
    for k in ("evaluatorMayMutateEvidence","evaluatorMayGrantHumanAcceptance","evaluatorMayGrantLifecycleStatus","automatedFeatureDetectionIsQualificationEvidence","automatedRegressionPassingIsQualificationEvidence"):false(policy,k,"evaluationPolicy")
    packet=p.get("packetPreparationPolicy",{})
    for k in ("exactSourceRevisionRequired","exactSourceTreeRevisionRequired","outputRestrictedToQualificationDraftArea","claimedAssistiveTechnologyScenarioStartsNotTested","unclaimedAssistiveTechnologyScenarioStartsNotApplicable","acceptedEvidenceRequiresSeparateGovernedReview"):true(packet,k,"packetPreparationPolicy")
    for k in ("preparedAcceptedForAccessibilityQualification","preparedAcceptedForLifecycleGate","preparedPacketMayFabricateEvidenceReferences","preparedPacketMayFabricateScenarioPassOrFail"):false(packet,k,"packetPreparationPolicy")
    if packet.get("preparedStatus")!="in-progress" or packet.get("preparedHumanReviewStatus")!="pending" or packet.get("preparedEvaluatorDisposition")!="blocked":fail("prepared packet fail-closed state drifted")
    capture=p.get("observationCapturePolicy",{})
    for k in ("preparedOrInProgressExactBoundRecordRequired","localDetectionMayOnlyProvideHints","reviewerConfirmationRequiredForTestedPreference","reviewerEvidenceReferenceRequiredForTestedOrUnsupportedPreference","reviewerEvidenceReferenceRequiredForScenarioPassOrFail","exportRequiresExplicitUserAction"):true(capture,k,"observationCapturePolicy")
    for k in ("sourceRevisionMutable","sourceTreeRevisionMutable","localDetectionIsQualificationEvidence","automaticPreferenceAcceptanceAllowed","automaticScenarioPassAllowed","automaticHumanAcceptanceAllowed","automaticAccessibilityQualificationAllowed","automaticLifecycleAcceptanceAllowed","browserIdentitySniffingAllowed","networkAccessRequired","telemetryRequired","analyticsRequired","persistentStorageRequired","capturedAcceptedForAccessibilityQualification","capturedAcceptedForLifecycleGate"):false(capture,k,"observationCapturePolicy")
    if capture.get("capturedStatus")!="in-progress" or capture.get("capturedHumanReviewStatus")!="pending" or capture.get("capturedEvaluatorDisposition")!="blocked":fail("captured observation fail-closed state drifted")
    a=p.get("acceptanceRules",{})
    if a.get("recordStatus")!="passed" or a.get("reviewAuthorityModes")!=["human","combined"] or a.get("humanReviewStatus")!="accepted":fail("accepted evidence human-review boundary drifted")
    for k in ("immutableReviewProvenanceRequired","reviewAuthorityAndAttestationEvidenceMustBeDistinct","reviewEvidenceMustBeDistinctFromQualificationEvidence","reviewTimestampMustNotPredateObservation","reviewTimestampMustNotBeFutureDated","acceptedForAccessibilityQualification","noUnresolvedHighOrCriticalIssues"):true(a,k,"acceptanceRules")
    false(a,"acceptedForLifecycleGate","acceptanceRules")
    if a.get("allRequiredAndClaimedScenarios")!="pass" or a.get("allRequiredPreferenceEvidence")!="tested-or-evidenced-not-supported":fail("accepted evidence completeness boundary drifted")
    b=p.get("nonPromotionBoundary",{})
    for k in ("acceptedAccessibilitySliceIsStableV1_4","acceptedAccessibilitySliceIsConsumerConformance","acceptedAccessibilitySliceIsBrowserMatrixQualification","acceptedAccessibilitySliceIsPhysicalDeviceQualification","acceptedAccessibilitySliceIsProductionPerformanceQualification","acceptedAccessibilitySliceIsNativeRendererParity"):false(b,k,"nonPromotionBoundary")
    for k in ("lifecyclePromotionRequiresSeparateGovernedDecision","downstreamConsumerAcceptanceRemainsIndependent"):true(b,k,"nonPromotionBoundary")
    needed={"stable-v1.4-release","consumer-v1.4-conformance","frozen-v1.4-accessibility-qualification-api","browser-matrix-v1.4-qualification","assistive-technology-v1.4-qualification","physical-device-v1.4-qualification","production-v1.4-performance-budgets","native-v1.4-renderer-parity","ecosystem-wide-v1.4-adoption"}
    if not isinstance(p.get("notEstablished"),list) or not needed.issubset(p["notEstablished"]):fail("qualification support must preserve every non-established boundary")

def ref_array(node):return node.get("items",{}).get("$ref")=="#/$defs/evidenceReference" and node.get("uniqueItems") is True

def validate_schema(s):
    if s.get("$schema")!="https://json-schema.org/draft/2020-12/schema" or s.get("additionalProperties") is not False:fail("evidence schema root boundary drifted")
    required=s.get("required",[])
    for f in ("schemaVersion","recordKind","target","status","observedAt","reviewAuthority","environment","supportClaims","preferenceCoverage","scenarioResults","issues","disposition"):
        if f not in required:fail(f"evidence schema missing required field {f}")
    props=s.get("properties",{})
    if props.get("schemaVersion",{}).get("const")!=1 or props.get("recordKind",{}).get("const")!="glaze-v1.4-accessibility-qualification-evidence-candidate":fail("evidence schema identity drifted")
    if props.get("disposition",{}).get("properties",{}).get("acceptedForLifecycleGate",{}).get("const") is not False:fail("evidence schema must make lifecycle-gate acceptance impossible")
    if props.get("status",{}).get("enum")!=["in-progress","review-ready","passed","failed","superseded"]:fail("evidence status vocabulary drifted")
    defs=s.get("$defs",{});er=defs.get("evidenceReference",{})
    if er.get("pattern")!=EVIDENCE_PATTERN or er.get("minLength")!=82 or er.get("maxLength")!=256:fail("content-addressed evidence-reference definition drifted")
    if not ref_array(props.get("environment",{}).get("properties",{}).get("evidenceReferences",{})):fail("environment evidence must remain content-addressed")
    if not ref_array(defs.get("preferenceObservation",{}).get("properties",{}).get("evidenceReferences",{})):fail("preference evidence must remain content-addressed")
    if not ref_array(defs.get("scenarioResult",{}).get("properties",{}).get("evidenceReferences",{})):fail("scenario evidence must remain content-addressed")
    rp=props.get("reviewProvenance",{})
    if rp.get("additionalProperties") is not False or set(rp.get("required",[]))!={"authorityEvidence","reviewEvidence","reviewedAt"}:fail("review provenance shape drifted")
    rpp=rp.get("properties",{})
    if rpp.get("authorityEvidence",{}).get("$ref")!="#/$defs/evidenceReference" or rpp.get("reviewEvidence",{}).get("$ref")!="#/$defs/evidenceReference":fail("review provenance evidence must remain content-addressed")
    if rpp.get("reviewedAt",{}).get("format")!="date-time":fail("review provenance timestamp contract drifted")
    ids=defs.get("scenarioResult",{}).get("properties",{}).get("id",{}).get("enum",[])
    if ids!=REQUIRED_SCENARIOS+list(CONDITIONAL.values()):fail("evidence schema scenario vocabulary drifted")
    passed=False
    for rule in s.get("allOf",[]):
        if rule.get("if",{}).get("properties",{}).get("status",{}).get("const")=="passed":
            passed=True
            if "reviewProvenance" not in rule.get("then",{}).get("required",[]):fail("passed evidence must require reviewProvenance")
    if not passed:fail("passed evidence conditional boundary missing")

def validate_sources(plan):
    for path in (PLAN,SCHEMA,COMPOSITION,EVALUATOR,PACKET_GENERATOR,OBSERVATION_CAPTURE,OBSERVATION_REFERENCE,OBSERVATION_REFERENCE_RUNTIME,TEMPLATE,REGRESSION,PACKET_REGRESSION,OBSERVATION_REGRESSION,DOCUMENTATION,VERSION):
        if not path.is_file():fail(f"governed artifact missing: {path.relative_to(ROOT)}")
    if VERSION.read_text(encoding="utf-8").strip()!="1.3.0":fail("Stable VERSION must remain 1.3.0 while V1.4 qualification support is a candidate")
    q=load(COMPOSITION).get("qualificationBoundary",{})
    if q.get("sourceBehaviorVerifiedByAutomatedTests") is not True:fail("source behavior automation boundary drifted")
    for k in ("browserMatrixQualificationEstablished","assistiveTechnologyQualificationEstablished","physicalDeviceQualificationEstablished","productionPerformanceQualificationEstablished"):false(q,k,"accessibilityComposition.qualificationBoundary")
    et=EVALUATOR.read_text(encoding="utf-8")
    for token in ("def evaluate_record(","acceptedForLifecycleGate","human-review-acceptance-pending","automated-only-review-cannot-accept-accessibility-qualification","EVIDENCE_REFERENCE","accepted-human-review-provenance-missing-or-invalid","accepted-human-review-evidence-not-content-addressed","review-authority-and-attestation-evidence-must-be-distinct","review-evidence-must-be-distinct-from-qualification-evidence","review-time-precedes-observation","review-time-from-future"):
        if token not in et:fail(f"evaluator missing governed boundary: {token}")
    gt=PACKET_GENERATOR.read_text(encoding="utf-8")
    for token in ("def build_record(","def build_checklist(","def assert_prepared_fail_closed(","accessibility-qualification-drafts",'humanReviewStatus": "pending"','evaluatorDisposition": "blocked"','acceptedForAccessibilityQualification": False','acceptedForLifecycleGate": False',"prepared scenarios may not claim pass/fail results","prepared scenarios must not fabricate evidence references"):
        if token not in gt:fail(f"packet generator missing governed fail-closed boundary: {token}")
    ct=OBSERVATION_CAPTURE.read_text(encoding="utf-8")
    for token in ("glaze-v1.4-accessibility-observation-capture-candidate","localDetectionIsQualificationEvidence: false","automaticPreferenceAcceptanceAllowed: false","automaticScenarioPassAllowed: false","automaticHumanAcceptanceAllowed: false","automaticAccessibilityQualificationAllowed: false","automaticLifecycleAcceptanceAllowed: false","networkAccessRequired: false","telemetryRequired: false","analyticsRequired: false","persistentStorageRequired: false","browserIdentitySniffingAllowed: false","acceptedForAccessibilityQualification: false","acceptedForLifecycleGate: false","humanReviewStatus = 'pending'","scenarioResults must not contain duplicate scenario ids","requires explicit reviewer evidence references"):
        if token not in ct:fail(f"observation capture runtime missing governed boundary: {token}")
    rt=OBSERVATION_REFERENCE_RUNTIME.read_text(encoding="utf-8");ht=OBSERVATION_REFERENCE.read_text(encoding="utf-8")
    for pattern in ("fetch(","XMLHttpRequest","sendBeacon","WebSocket","localStorage","sessionStorage","indexedDB","navigator.userAgent","navigator.userAgentData","navigator.platform","getUserMedia","getDisplayMedia","http://","https://"):
        if pattern in ct or pattern in rt or pattern in ht:fail(f"observation capture must not introduce remote/persistent/identity/capture path: {pattern}")
    for token in ("file.text()","new Blob","URL.createObjectURL","URL.revokeObjectURL","no state is auto-confirmed","no qualification or lifecycle acceptance was granted"):
        if token not in rt:fail(f"observation capture reference runtime missing local/manual boundary: {token}")
    for token in ("Local capture aid only.","does not auto-pass scenarios","export happens only when you choose the export action"):
        if token not in ht:fail(f"observation capture reference HTML missing disclosure: {token}")
    dt=DOCUMENTATION.read_text(encoding="utf-8")
    for token in ("Development / qualification infrastructure only","evidence+sha256:","reviewProvenance","authorityEvidence","reviewEvidence","reviewedAt","Automated-only review cannot grant acceptance","acceptedForLifecycleGate: false","does **not** prove that the named reviewer is genuinely authorized","Real evidence still required"):
        if token not in dt:fail(f"accessibility qualification documentation missing governed boundary: {token}")
    template=load(TEMPLATE)
    if template.get("status")!="in-progress":fail("qualification template must remain in-progress")
    false(template.get("disposition",{}),"acceptedForAccessibilityQualification","template.disposition")
    false(template.get("disposition",{}),"acceptedForLifecycleGate","template.disposition")
    spec=importlib.util.spec_from_file_location("glaze_v14_accessibility_qualification_evaluator",EVALUATOR)
    if not spec or not spec.loader:fail("qualification evaluator could not be loaded")
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
    outcome=module.evaluate_record(template,plan)
    if outcome.get("evaluatorDisposition")!="blocked" or outcome.get("acceptedForAccessibilityQualification") is not False or outcome.get("acceptedForLifecycleGate") is not False:fail("draft qualification template must deterministically remain blocked and non-promoting")

def main():
    p=load(PLAN);validate_plan(p);validate_schema(load(SCHEMA));validate_sources(p)
    print("Glaze UI V1.4 accessibility qualification support validation passed")
if __name__=="__main__":main()