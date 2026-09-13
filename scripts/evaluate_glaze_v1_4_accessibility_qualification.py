#!/usr/bin/env python3
"""Fail-closed Glaze UI V1.4 accessibility qualification evaluator.

Governed output invariant: "acceptedForLifecycleGate": False
"""
from __future__ import annotations
import argparse, copy, json, re, unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
DEFAULT_PLAN=ROOT/'contracts'/'v1.4'/'accessibility-qualification.candidate.json'
HEX40=re.compile(r'^[0-9a-f]{40}$'); ZERO='0'*40
EVIDENCE_REFERENCE=re.compile(r'^evidence\+sha256:[0-9a-f]{64}:[A-Za-z0-9][A-Za-z0-9._+-]*(?::[A-Za-z0-9][A-Za-z0-9._+-]*)*(?:/[A-Za-z0-9][A-Za-z0-9._+-]*(?::[A-Za-z0-9][A-Za-z0-9._+-]*)*)*$')
EXPECTED_PRODUCT='Glaze UI V1.4 — Optical Material and Chromatic Depth'; EXPECTED_VERSION='1.4.0-candidate'
EXPECTED_RECORD_KIND='glaze-v1.4-accessibility-qualification-evidence-candidate'
STATUSES={'in-progress','review-ready','passed','failed','superseded'}; REVIEW_MODES={'human','combined','automated'}
HUMAN={'pending','accepted','rejected'}; PLATFORMS={'web','android','linux','other'}
ASSISTIVE={'screen-reader','voice-control','switch-control','keyboard','other'}
SCENARIO_RESULTS={'pass','fail','not-tested','not-applicable'}; PREF_STATES={'tested-active','tested-inactive','not-supported','not-tested'}
SEVERITIES={'info','low','medium','high','critical'}; BLOCKING={'high','critical'}
RECORD_FIELDS={'schemaVersion','recordKind','target','status','observedAt','reviewAuthority','environment','supportClaims','preferenceCoverage','scenarioResults','issues','disposition'}
TARGET_FIELDS={'product','targetVersion','sourceRevision','sourceTreeRevision'}; REVIEW_FIELDS={'mode','authority','humanReviewStatus'}
PROVENANCE_FIELDS={'authorityEvidence','reviewEvidence','reviewedAt'}; DISPOSITION_FIELDS={'evaluatorDisposition','acceptedForAccessibilityQualification','acceptedForLifecycleGate','notes'}
ENV_FIELDS={'platformFamily','operatingSystem','browser','physicalDevice','assistiveTechnologies','evidenceReferences'}
SCENE_FIELDS={'id','result','evidenceReferences','notes'}; PREF_FIELDS={'state','evidenceReferences'}


def load(path:Path)->dict[str,Any]:
    value=json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(value,dict): raise ValueError(f'{path} must contain a JSON object')
    return value

def text(v:Any,n:int,allow_none=False)->str|None:
    if v is None and allow_none:return None
    if not isinstance(v,str) or not v or v!=v.strip() or len(v)>n:return None
    if any(unicodedata.category(c).startswith('C') for c in v):return None
    return v

def evidence(v:Any)->str|None:
    v=text(v,256)
    if v is None or not EVIDENCE_REFERENCE.fullmatch(v):return None
    return None if v[len('evidence+sha256:'):].split(':',1)[0]==('0'*64) else v

def refs(v:Any,n:int)->bool:
    if not isinstance(v,list) or len(v)>n:return False
    normalized=[evidence(x) for x in v]
    return all(x is not None for x in normalized) and len(set(normalized))==len(normalized)

def stamp(v:Any)->datetime|None:
    if not isinstance(v,str) or not v or v!=v.strip():return None
    try:p=datetime.fromisoformat(v[:-1]+'+00:00' if v.endswith('Z') else v)
    except ValueError:return None
    return None if p.tzinfo is None or p.utcoffset() is None else p.astimezone(timezone.utc)

def result(kind:str,reasons:list[str],required:list[str],missing:list[str],failed:list[str])->dict[str,Any]:
    return {'evaluatorDisposition':kind,'acceptedForAccessibilityQualification':kind=='accepted','acceptedForLifecycleGate':False,'reasons':sorted(set(reasons)),'requiredScenarioIds':required,'missingScenarioIds':sorted(set(missing)),'failedScenarioIds':sorted(set(failed))}

def evaluate_record(record:Any,plan:dict[str,Any],*,expected_source_revision:str|None=None,expected_source_tree_revision:str|None=None,evaluation_time:datetime|None=None)->dict[str,Any]:
    record=copy.deepcopy(record); reasons=[]; missing=[]; failed=[]; blocked=False; qrefs:set[str]=set()
    now=evaluation_time or datetime.now(timezone.utc)
    if now.tzinfo is None or now.utcoffset() is None:raise ValueError('evaluation_time must include timezone information')
    now=now.astimezone(timezone.utc)
    if not isinstance(record,dict):return result('blocked',['record-shape-invalid'],list(plan.get('requiredScenarios',[])),missing,failed)
    base=set(plan.get('requiredScenarios',[])); conditional=plan.get('claimConditionalScenarios',{}); conditional_ids=set(conditional.values()); allowed=base|conditional_ids
    claims=record.get('supportClaims') if isinstance(record.get('supportClaims'),dict) else {}; required=list(plan.get('requiredScenarios',[]))
    for key,sid in conditional.items():
        if claims.get(key) is True:required.append(sid)
    disp=record.get('disposition') if isinstance(record.get('disposition'),dict) else {}
    if disp.get('acceptedForLifecycleGate') is not False:return result('failed',['accessibility-evidence-may-not-grant-lifecycle-gate'],required,missing,failed)
    fields=set(record)
    if not RECORD_FIELDS.issubset(fields) or not fields.issubset(RECORD_FIELDS|{'reviewProvenance'}):reasons.append('record-fields-invalid');blocked=True
    if record.get('schemaVersion')!=1:reasons.append('record-schema-version-invalid');blocked=True
    if record.get('recordKind')!=EXPECTED_RECORD_KIND:reasons.append('record-kind-invalid');blocked=True
    observed=stamp(record.get('observedAt'))
    if observed is None:reasons.append('observation-time-invalid');blocked=True
    elif observed>now:reasons.append('observation-time-from-future');blocked=True
    target=record.get('target') if isinstance(record.get('target'),dict) else {}
    if set(target)!=TARGET_FIELDS:reasons.append('target-fields-invalid');blocked=True
    if target.get('product')!=EXPECTED_PRODUCT:reasons.append('target-product-invalid');blocked=True
    if target.get('targetVersion')!=EXPECTED_VERSION:reasons.append('target-version-invalid');blocked=True
    sr=target.get('sourceRevision'); tr=target.get('sourceTreeRevision')
    if not isinstance(sr,str) or not HEX40.fullmatch(sr) or sr==ZERO:reasons.append('exact-source-revision-missing-or-placeholder')
    if not isinstance(tr,str) or not HEX40.fullmatch(tr) or tr==ZERO:reasons.append('exact-source-tree-revision-missing-or-placeholder')
    if expected_source_revision is not None and sr!=expected_source_revision:reasons.append('source-revision-does-not-match-expected-revision')
    if expected_source_tree_revision is not None and tr!=expected_source_tree_revision:reasons.append('source-tree-revision-does-not-match-expected-tree')
    status=record.get('status')
    if status not in STATUSES:reasons.append('record-status-invalid');blocked=True
    review=record.get('reviewAuthority') if isinstance(record.get('reviewAuthority'),dict) else {}
    if set(review)!=REVIEW_FIELDS:reasons.append('review-authority-fields-invalid');blocked=True
    mode=review.get('mode'); human=review.get('humanReviewStatus')
    if mode not in REVIEW_MODES or text(review.get('authority'),240) is None:reasons.append('review-authority-invalid');blocked=True
    if human not in HUMAN:reasons.append('human-review-status-invalid');blocked=True
    if status=='superseded':reasons.append('record-is-superseded')
    if not isinstance(record.get('supportClaims'),dict) or set(claims)!=set(conditional) or any(claims.get(k) not in {True,False} for k in conditional):reasons.append('support-claims-invalid');blocked=True
    if set(disp)!=DISPOSITION_FIELDS:reasons.append('disposition-fields-invalid');blocked=True
    d=disp.get('evaluatorDisposition'); accepted=disp.get('acceptedForAccessibilityQualification')
    if d not in {'blocked','review-ready','failed','accepted'}:reasons.append('disposition-value-invalid');blocked=True
    if accepted not in {True,False}:reasons.append('accessibility-disposition-invalid');blocked=True
    if text(disp.get('notes'),4000) is None:reasons.append('disposition-notes-invalid');blocked=True
    if status=='passed':
        if d!='accepted' or accepted is not True:reasons.append('passed-record-disposition-inconsistent');blocked=True
    elif status in STATUSES and (d=='accepted' or accepted is not False):reasons.append('non-passed-record-disposition-inconsistent');blocked=True
    if status=='failed' or human=='rejected':reasons.append('record-or-human-review-explicitly-failed');return result('failed',reasons,required,missing,failed)

    env=record.get('environment')
    if not isinstance(env,dict):reasons.append('environment-missing');blocked=True
    else:
        if set(env)!=ENV_FIELDS:reasons.append('environment-fields-invalid');blocked=True
        pf=env.get('platformFamily')
        if pf not in PLATFORMS:reasons.append('platform-family-invalid');blocked=True
        os=env.get('operatingSystem')
        if not isinstance(os,dict) or set(os)!={'name','version'} or text(os.get('name'),120) is None or text(os.get('version'),120) is None:reasons.append('operating-system-evidence-invalid');blocked=True
        browser=env.get('browser')
        browser_ok=isinstance(browser,dict) and set(browser)=={'name','version'} and text(browser.get('name'),120) is not None and text(browser.get('version'),120) is not None
        if (pf=='web' and not browser_ok) or (pf!='web' and browser is not None and not browser_ok):reasons.append('browser-evidence-invalid');blocked=True
        if env.get('physicalDevice') not in {True,False}:reasons.append('physical-device-field-invalid');blocked=True
        ats=env.get('assistiveTechnologies')
        if not isinstance(ats,list) or len(ats)>50:reasons.append('assistive-technology-inventory-invalid');blocked=True
        else:
            seen=set()
            for item in ats:
                ok=isinstance(item,dict) and set(item)=={'name','version','mode'} and text(item.get('name'),120) is not None and text(item.get('version'),120) is not None and item.get('mode') in ASSISTIVE
                if not ok:reasons.append('assistive-technology-inventory-invalid');blocked=True;continue
                key=(item['name'],item['version'],item['mode'])
                if key in seen:reasons.append('duplicate-assistive-technology');blocked=True
                seen.add(key)
        er=env.get('evidenceReferences')
        if not refs(er,100):reasons.append('environment-evidence-references-invalid');blocked=True
        else:qrefs.update(er)

    scenarios=record.get('scenarioResults'); scene_map={}; duplicates=set()
    if not isinstance(scenarios,list) or not scenarios or len(scenarios)>100:reasons.append('scenario-results-invalid');blocked=True
    else:
        for e in scenarios:
            if not isinstance(e,dict) or set(e)!=SCENE_FIELDS:reasons.append('invalid-scenario-entry');blocked=True;continue
            sid=e.get('id')
            if text(sid,160) is None or sid not in allowed:reasons.append('invalid-scenario-id');blocked=True;continue
            if e.get('result') not in SCENARIO_RESULTS:reasons.append(f'invalid-scenario-result:{sid}');blocked=True
            rr=e.get('evidenceReferences')
            if not refs(rr,100):reasons.append(f'scenario-evidence-references-invalid:{sid}');blocked=True
            else:qrefs.update(rr)
            if text(e.get('notes'),4000) is None:reasons.append(f'scenario-notes-invalid:{sid}');blocked=True
            if sid in scene_map:duplicates.add(sid)
            else:scene_map[sid]=e
    if duplicates:reasons.append('duplicate-scenario-ids')
    for sid in required:
        e=scene_map.get(sid)
        if e is None:missing.append(sid);continue
        state=e.get('result'); rr=e.get('evidenceReferences')
        if state=='fail':failed.append(sid)
        elif state in (None,'not-tested'):missing.append(sid)
        elif state=='not-applicable':
            if sid in base:missing.append(sid);reasons.append(f'required-scenario-cannot-be-not-applicable:{sid}')
            elif sid in conditional_ids:missing.append(sid);reasons.append(f'claimed-assistive-scenario-cannot-be-not-applicable:{sid}')
        elif state=='pass' and (not refs(rr,100) or not rr):missing.append(sid);reasons.append(f'passing-scenario-missing-evidence:{sid}')
        elif state not in SCENARIO_RESULTS:missing.append(sid);reasons.append(f'invalid-scenario-result:{sid}')

    prefs=record.get('preferenceCoverage'); required_prefs=list(plan.get('preferenceEvidence',{}).get('requiredPreferences',[]))
    if not isinstance(prefs,dict) or set(prefs)!=set(required_prefs):reasons.append('preference-coverage-fields-invalid');blocked=True;prefs=prefs if isinstance(prefs,dict) else {}
    for name in required_prefs:
        p=prefs.get(name)
        if not isinstance(p,dict) or set(p)!=PREF_FIELDS:reasons.append(f'preference-evidence-shape-invalid:{name}');blocked=True;continue
        state=p.get('state'); rr=p.get('evidenceReferences')
        if state not in PREF_STATES:reasons.append(f'invalid-preference-state:{name}');blocked=True;continue
        if not refs(rr,25):reasons.append(f'preference-evidence-references-invalid:{name}');blocked=True;continue
        qrefs.update(rr)
        if state=='not-tested':reasons.append(f'preference-not-tested:{name}')
        elif state=='not-supported' and not rr:reasons.append(f'unsupported-preference-missing-evidence:{name}')
        elif state in {'tested-active','tested-inactive'} and not rr:reasons.append(f'tested-preference-missing-evidence:{name}')

    provenance=record.get('reviewProvenance')
    if human=='accepted':
        if not isinstance(provenance,dict) or set(provenance)!=PROVENANCE_FIELDS:reasons.append('accepted-human-review-provenance-missing-or-invalid');blocked=True
        else:
            ae=evidence(provenance.get('authorityEvidence')); re_=evidence(provenance.get('reviewEvidence'))
            if ae is None or re_ is None:reasons.append('accepted-human-review-evidence-not-content-addressed');blocked=True
            elif ae==re_:reasons.append('review-authority-and-attestation-evidence-must-be-distinct');blocked=True
            elif ae in qrefs or re_ in qrefs:reasons.append('review-evidence-must-be-distinct-from-qualification-evidence');blocked=True
            rt=stamp(provenance.get('reviewedAt'))
            if rt is None:reasons.append('review-time-invalid');blocked=True
            else:
                if observed is not None and rt<observed:reasons.append('review-time-precedes-observation');blocked=True
                if rt>now:reasons.append('review-time-from-future');blocked=True
    elif provenance is not None and (not isinstance(provenance,dict) or set(provenance)!=PROVENANCE_FIELDS):reasons.append('review-provenance-fields-invalid');blocked=True

    issues=record.get('issues'); unresolved=[]
    if not isinstance(issues,list) or len(issues)>100:reasons.append('issues-array-invalid');blocked=True
    else:
        for issue in issues:
            ok=isinstance(issue,dict) and {'summary','severity','resolved'}<=set(issue)<={'summary','severity','resolved','reference'} and text(issue.get('summary'),1000) is not None and issue.get('severity') in SEVERITIES and issue.get('resolved') in {True,False} and (issue.get('reference') is None or text(issue.get('reference'),1000) is not None)
            if not ok:reasons.append('invalid-issue-entry');blocked=True;continue
            if issue['severity'] in BLOCKING and issue['resolved'] is not True:unresolved.append(issue['summary'])
    if unresolved:reasons.append('unresolved-high-or-critical-issue')
    if failed:reasons.append('required-or-claimed-scenario-failed');return result('failed',reasons,required,missing,failed)
    prefix_block=any(r.startswith(('exact-source-','source-revision-does-not-match','source-tree-revision-does-not-match','preference-','unsupported-preference-','tested-preference-','invalid-preference-','scenario-results-','invalid-scenario-','duplicate-scenario-')) for r in reasons)
    if blocked or missing or duplicates or unresolved or prefix_block or status=='superseded':return result('blocked',reasons,required,missing,failed)
    if human!='accepted':reasons.append('human-review-acceptance-pending');return result('review-ready',reasons,required,missing,failed)
    if mode not in {'human','combined'}:reasons.append('automated-only-review-cannot-accept-accessibility-qualification');return result('review-ready',reasons,required,missing,failed)
    if status!='passed' or d!='accepted' or accepted is not True:reasons.append('explicit-passed-record-and-accessibility-disposition-required');return result('review-ready',reasons,required,missing,failed)
    return result('accepted',reasons,required,missing,failed)

def main()->None:
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('record',type=Path);ap.add_argument('--plan',type=Path,default=DEFAULT_PLAN);ap.add_argument('--expected-source-revision');ap.add_argument('--expected-source-tree-revision');a=ap.parse_args()
    print(json.dumps(evaluate_record(load(a.record),load(a.plan),expected_source_revision=a.expected_source_revision,expected_source_tree_revision=a.expected_source_tree_revision),indent=2,sort_keys=True))
if __name__=='__main__':main()