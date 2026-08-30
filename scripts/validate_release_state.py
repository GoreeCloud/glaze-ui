#!/usr/bin/env python3
"""Fail closed when the canonical Glaze UI 2.1 Stable release state drifts."""
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def req(c,m):
    if not c: raise SystemExit(f'Glaze UI release-state validation failed: {m}')
def text(p): return (ROOT/p).read_text(encoding='utf-8')
def main():
    version=text('VERSION').strip(); req(version=='2.1.0','current Stable VERSION must be 2.1.0')
    req(re.fullmatch(r'\d+\.\d+\.\d+',version) is not None,'VERSION must be semantic')
    lifecycle=json.loads(text('registry/lifecycle.json'))
    req(lifecycle.get('currentStable')==version,'lifecycle currentStable differs from VERSION')
    req(lifecycle.get('activeCandidate') is None,'2.1 promotion must leave no active Candidate')
    releases=lifecycle.get('releases',[])
    stable=[r for r in releases if isinstance(r,dict) and r.get('version')==version]
    req(len(stable)==1 and stable[0].get('status')=='stable' and stable[0].get('consumerEligible') is True,'2.1 Stable release record missing')
    req(stable[0].get('promotedFromCandidate')=='2.1.0-candidate.1','promotion-source Candidate missing')
    old=[r for r in releases if isinstance(r,dict) and r.get('version')=='2.0.0']
    req(len(old)==1 and old[0].get('status')=='historical','2.0 must be historical')
    req((ROOT/'GLAZE_UI_2_1_STABLE.md').is_file() and (ROOT/'acceptance/2.1-stable.md').is_file(),'2.1 Stable contract/acceptance missing')
    req((ROOT/'css/glaze-2.1.0.css').is_file() and (ROOT/'js/glaze-2.1.0.mjs').is_file(),'versioned Stable entrypoints missing')
    stable_doc=text('GLAZE_UI_2_1_STABLE.md')
    for marker in ('Lifecycle status:** Stable','Stable semantic version:** 2.1.0','Previous Stable implementation baseline:** Glaze UI 2.0.0','Content is solid. Interaction is glazed.','Approve Visual Excellence','No downstream application is promoted by declaration'):
        req(marker in stable_doc,f'2.1 Stable contract missing {marker}')
    acceptance=text('acceptance/2.1-stable.md')
    for marker in ('Approve Visual Excellence','5b46903c18660ae78e7f1aaea39a93136efacda7','a21601691dc412baa6a889533d6fa5b3a7996dc2','48 dp','56 dp'):
        req(marker in acceptance,f'2.1 Stable acceptance missing {marker}')
    registry=json.loads(text('consumers/registry.json'))
    req(registry.get('stableBaseline')==version and registry.get('requiredConsumerVersion')==version,'consumer mandatory Stable target differs from VERSION')
    req('2.0.0' in registry.get('historicalStableVersions',[]),'2.0 must be historical consumer baseline')
    for c in registry.get('consumers',[]):
        req(c.get('requiredTargetVersion')==version,f"{c.get('repository')} required target must be 2.1.0")
        req(c.get('productionEligible') is False,'promotion must not auto-promote downstream consumers')
    enforcement=json.loads(text('tokens/enforcement.json'))
    req(enforcement.get('meta',{}).get('currentStable')==version,'enforcement currentStable differs from VERSION')
    print('Glaze UI 2.1.0 Stable release state validated; downstream consumers remain separately gated')
if __name__=='__main__': main()
