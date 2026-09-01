#!/usr/bin/env python3
"""Focused fail-closed validation for the Glaze UI 2.1.0 Stable promotion.

A later non-consumer Candidate may coexist with the 2.1 Stable release. This
validator protects the 2.1 Stable record and consumer boundary rather than
assuming that no future Candidate can ever be active.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def req(c,m):
    if not c: raise SystemExit(f'Glaze UI 2.1 Stable promotion validation failed: {m}')
def text(p):
    q=ROOT/p; req(q.is_file(),f'missing {p}'); return q.read_text(encoding='utf-8')
def main():
    req(text('VERSION').strip()=='2.1.0','VERSION must be 2.1.0')
    lifecycle=json.loads(text('registry/lifecycle.json'))
    req(lifecycle.get('currentStable')=='2.1.0','currentStable must remain 2.1.0')
    releases=lifecycle.get('releases',[])
    stable=[r for r in releases if isinstance(r,dict) and r.get('version')=='2.1.0']
    req(len(stable)==1 and stable[0].get('status')=='stable' and stable[0].get('consumerEligible') is True,'2.1.0 Stable release record')
    active=lifecycle.get('activeCandidate')
    if active is not None:
        candidate=[r for r in releases if isinstance(r,dict) and r.get('version')==active]
        req(len(candidate)==1 and candidate[0].get('status')=='candidate' and candidate[0].get('consumerEligible') is False,'active Candidate must be separately registered and non-consumer-eligible')
        req(active!='2.1.0','active Candidate must not replace Stable 2.1.0')
    for cap in ('visual-excellence-gate','material-budgets','accessibility-resolution-matrix','canonical-reference-flows-2.1','visual-regression-2.1','android-native-reference-2.1'):
        req(lifecycle.get('capabilities',{}).get(cap,{}).get('status')=='stable',f'{cap} not Stable')
    manifest=json.loads(text('contracts/regression/visual-baselines.json')); req(manifest.get('baselineRevision')=='5b46903c18660ae78e7f1aaea39a93136efacda7','approved visual baseline revision')
    thresholds=manifest.get('thresholds',{}); req(thresholds.get('perChannelTolerance')==12 and thresholds.get('maxChangedPixelRatio')==0.0075 and thresholds.get('maxMeanAbsoluteChannelDelta')==1.5,'visual thresholds changed')
    accept=text('acceptance/2.1-stable.md'); req('Approve Visual Excellence' in accept,'human Visual Excellence acceptance')
    stable_doc=text('GLAZE_UI_2_1_STABLE.md'); req('Content is solid. Interaction is glazed.' in stable_doc,'core material rule')
    req('Reduced Transparency' in stable_doc and 'Forced Colors' in stable_doc,'accessibility precedence')
    req('No downstream application is promoted by declaration' in stable_doc,'consumer boundary')
    print(f"Glaze UI 2.1.0 focused Stable promotion validation passed with activeCandidate={active!r}")
if __name__=='__main__': main()
