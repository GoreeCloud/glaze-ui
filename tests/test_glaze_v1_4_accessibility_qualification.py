from __future__ import annotations
import copy, hashlib, importlib.util, json, sys, unittest
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; P=ROOT/'scripts'/'evaluate_glaze_v1_4_accessibility_qualification.py'
S=importlib.util.spec_from_file_location('a11y_eval',P); assert S and S.loader
E=importlib.util.module_from_spec(S);sys.modules[S.name]=E;S.loader.exec_module(E)
PLAN=json.loads((ROOT/'contracts'/'v1.4'/'accessibility-qualification.candidate.json').read_text())
TEMPLATE=json.loads((ROOT/'evidence'/'v1.4'/'templates'/'accessibility-qualification-record.candidate.json').read_text())
SOURCE='a'*40;TREE='b'*40

def ref(name):return f"evidence+sha256:{hashlib.sha256(name.encode()).hexdigest()}:{name}"
def accepted():
 r=copy.deepcopy(TEMPLATE);r['target'].update(sourceRevision=SOURCE,sourceTreeRevision=TREE);r['status']='passed';r['observedAt']='2026-09-12T00:00:00Z'
 r['reviewAuthority']={'mode':'combined','authority':'Authorized GoreeCloud accessibility reviewer plus repository validation','humanReviewStatus':'accepted'}
 r['reviewProvenance']={'authorityEvidence':ref('review-authority.json'),'reviewEvidence':ref('review-attestation.json'),'reviewedAt':'2026-09-12T00:30:00Z'}
 r['environment']={'platformFamily':'web','operatingSystem':{'name':'Test OS','version':'1'},'browser':{'name':'Test Browser','version':'1'},'physicalDevice':True,'assistiveTechnologies':[{'name':'Keyboard','version':'system','mode':'keyboard'}],'evidenceReferences':[ref('environment.json')]}
 for n,p in r['preferenceCoverage'].items():p['state']='tested-active';p['evidenceReferences']=[ref(f'preference-{n}.json')]
 for s in r['scenarioResults']:
  if s['id'] in PLAN['requiredScenarios']:s['result']='pass';s['evidenceReferences']=[ref(f"scenario-{s['id']}.json")]
  else:s['result']='not-applicable';s['evidenceReferences']=[]
 r['issues']=[];r['disposition']={'evaluatorDisposition':'accepted','acceptedForAccessibilityQualification':True,'acceptedForLifecycleGate':False,'notes':'Explicit bounded accessibility qualification acceptance only.'};return r

def ev(r,**kw):return E.evaluate_record(r,PLAN,**kw)
class Tests(unittest.TestCase):
 def blocked(self,r,reason=None):
  x=ev(r);self.assertEqual(x['evaluatorDisposition'],'blocked');self.assertFalse(x['acceptedForAccessibilityQualification']);self.assertFalse(x['acceptedForLifecycleGate']);
  if reason:self.assertIn(reason,x['reasons'])
 def test_non_objects(self):
  for r in (None,[],'x',7):self.blocked(r,'record-shape-invalid')
 def test_template_blocked(self):self.blocked(copy.deepcopy(TEMPLATE))
 def test_accepted_slice_only(self):
  x=ev(accepted(),expected_source_revision=SOURCE,expected_source_tree_revision=TREE);self.assertEqual(x['evaluatorDisposition'],'accepted');self.assertTrue(x['acceptedForAccessibilityQualification']);self.assertFalse(x['acceptedForLifecycleGate'])
 def test_root_target_review_disposition_hidden_fields(self):
  cases=[]
  r=accepted();r['stableApproved']=True;cases.append((r,'record-fields-invalid'))
  r=accepted();r['target']['productionAccepted']=True;cases.append((r,'target-fields-invalid'))
  r=accepted();r['reviewAuthority']['autoAccepted']=True;cases.append((r,'review-authority-fields-invalid'))
  r=accepted();r['disposition']['acceptedForStable']=True;cases.append((r,'disposition-fields-invalid'))
  for r,reason in cases:self.blocked(r,reason)
 def test_disposition_consistency(self):
  r=accepted();r['disposition']['evaluatorDisposition']='stable-approved';self.blocked(r,'disposition-value-invalid')
  r=accepted();r['disposition']['evaluatorDisposition']='review-ready';self.blocked(r,'passed-record-disposition-inconsistent')
  r=accepted();r['status']='review-ready';r['reviewAuthority']['humanReviewStatus']='pending';self.blocked(r,'non-passed-record-disposition-inconsistent')
 def test_support_scenario_preference_hidden_fields(self):
  r=accepted();r['supportClaims']['automaticConformanceClaimed']=True;self.blocked(r,'support-claims-invalid')
  r=accepted();r['scenarioResults'][0]['acceptedForStable']=True;self.blocked(r,'invalid-scenario-entry')
  r=accepted();r['preferenceCoverage']['reducedMotion']['autoAccepted']=True;self.blocked(r,'preference-evidence-shape-invalid:reducedMotion')
 def test_unknown_preference(self):
  r=accepted();r['preferenceCoverage']['futureAutoQualification']={'state':'tested-active','evidenceReferences':[ref('future.json')]};self.blocked(r,'preference-coverage-fields-invalid')
 def test_issue_shape_and_limits(self):
  r=accepted();r['issues']=[{'summary':'x','severity':'info','resolved':True,'reference':'issue:1','override':True}];self.blocked(r,'invalid-issue-entry')
  r=accepted();r['issues']=[{'summary':str(i),'severity':'info','resolved':True,'reference':f'issue:{i}'} for i in range(101)];self.blocked(r,'issues-array-invalid')
 def test_observation_time(self):
  r=accepted();r['observedAt']='2026-09-12T00:00:00';self.blocked(r,'observation-time-invalid')
  r=accepted();r['observedAt']=' 2026-09-12T00:00:00Z';self.blocked(r,'observation-time-invalid')
  r=accepted();r['observedAt']='2026-09-12T10:00:00.001Z';x=ev(r,evaluation_time=datetime(2026,9,12,10,0,tzinfo=timezone.utc));self.assertEqual(x['evaluatorDisposition'],'blocked');self.assertIn('observation-time-from-future',x['reasons'])
 def test_content_addressed_environment_preference_scenario(self):
  r=accepted();r['environment']['evidenceReferences']=['artifact:environment.json'];self.blocked(r,'environment-evidence-references-invalid')
  r=accepted();r['preferenceCoverage']['reducedMotion']['evidenceReferences']=['artifact:preference.json'];self.blocked(r,'preference-evidence-references-invalid:reducedMotion')
  r=accepted();next(s for s in r['scenarioResults'] if s['id']=='keyboard-focus-order')['evidenceReferences']=['artifact:keyboard.json'];x=ev(r);self.assertEqual(x['evaluatorDisposition'],'blocked');self.assertIn('keyboard-focus-order',x['missingScenarioIds'])
 def test_whitespace_and_duplicate_evidence(self):
  r=accepted();r['environment']['evidenceReferences']=[' '+ref('environment.json')];self.blocked(r,'environment-evidence-references-invalid')
  r=accepted();r['environment']['evidenceReferences']*=2;self.blocked(r,'environment-evidence-references-invalid')
 def test_environment_and_at_inventory(self):
  r=accepted();r['environment'].pop('browser');self.blocked(r,'environment-fields-invalid')
  r=accepted();r['environment']['automaticQualification']=True;self.blocked(r,'environment-fields-invalid')
  r=accepted();r['environment']['assistiveTechnologies']*=2;self.blocked(r,'duplicate-assistive-technology')
  r=accepted();r['environment']['assistiveTechnologies'][0]['mode']='auto';self.blocked(r,'assistive-technology-inventory-invalid')
 def test_pending_human_is_review_ready(self):
  r=accepted();r['status']='review-ready';r['reviewAuthority']['humanReviewStatus']='pending';r['disposition']['evaluatorDisposition']='review-ready';r['disposition']['acceptedForAccessibilityQualification']=False;x=ev(r);self.assertEqual(x['evaluatorDisposition'],'review-ready');self.assertIn('human-review-acceptance-pending',x['reasons'])
 def test_scenario_coverage(self):
  r=accepted();r['scenarioResults']=[s for s in r['scenarioResults'] if s['id']!='keyboard-focus-order'];x=ev(r);self.assertEqual(x['evaluatorDisposition'],'blocked');self.assertIn('keyboard-focus-order',x['missingScenarioIds'])
  r=accepted();r['supportClaims']['screenReaderClaimed']=True;x=ev(r);self.assertIn('screen-reader-semantics-and-announcements',x['missingScenarioIds'])
  r=accepted();s=next(s for s in r['scenarioResults'] if s['id']=='forced-colors-system-color-path');s['result']='fail';x=ev(r);self.assertEqual(x['evaluatorDisposition'],'failed');self.assertIn(s['id'],x['failedScenarioIds'])
 def test_source_mismatch(self):
  x=ev(accepted(),expected_source_revision='c'*40,expected_source_tree_revision=TREE);self.assertEqual(x['evaluatorDisposition'],'blocked');self.assertIn('source-revision-does-not-match-expected-revision',x['reasons'])
 def test_blocking_issue(self):
  r=accepted();r['issues']=[{'summary':'Blocking accessibility defect','severity':'high','resolved':False,'reference':'issue:1'}];self.blocked(r,'unresolved-high-or-critical-issue')
 def test_lifecycle_claim_fails(self):
  r=accepted();r['disposition']['acceptedForLifecycleGate']=True;x=ev(r);self.assertEqual(x['evaluatorDisposition'],'failed');self.assertIn('accessibility-evidence-may-not-grant-lifecycle-gate',x['reasons'])
 def test_automated_only_cannot_accept(self):
  r=accepted();r['reviewAuthority']['mode']='automated';x=ev(r);self.assertEqual(x['evaluatorDisposition'],'review-ready');self.assertFalse(x['acceptedForAccessibilityQualification'])
 def test_review_provenance_required(self):
  r=accepted();r.pop('reviewProvenance');self.blocked(r,'accepted-human-review-provenance-missing-or-invalid')
 def test_review_provenance_content_addressed(self):
  r=accepted();r['reviewProvenance']['authorityEvidence']='artifact:authority';self.blocked(r,'accepted-human-review-evidence-not-content-addressed')
 def test_review_provenance_distinct(self):
  r=accepted();r['reviewProvenance']['reviewEvidence']=r['reviewProvenance']['authorityEvidence'];self.blocked(r,'review-authority-and-attestation-evidence-must-be-distinct')
  r=accepted();r['reviewProvenance']['reviewEvidence']=r['environment']['evidenceReferences'][0];self.blocked(r,'review-evidence-must-be-distinct-from-qualification-evidence')
 def test_review_time(self):
  r=accepted();r['reviewProvenance']['reviewedAt']='2026-09-11T23:59:59Z';self.blocked(r,'review-time-precedes-observation')
  r=accepted();r['reviewProvenance']['reviewedAt']='2026-09-12T10:00:00.001Z';x=ev(r,evaluation_time=datetime(2026,9,12,10,0,tzinfo=timezone.utc));self.assertEqual(x['evaluatorDisposition'],'blocked');self.assertIn('review-time-from-future',x['reasons'])
 def test_no_mutation(self):
  r=accepted();orig=copy.deepcopy(r);ev(r);self.assertEqual(r,orig)
if __name__=='__main__':unittest.main()
