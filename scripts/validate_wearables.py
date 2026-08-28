#!/usr/bin/env python3
"""Validate Glaze UI 2.0 Stable wearable semantics and historical native-evidence separation."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'WEARABLES.md'; COMPONENTS=ROOT/'WEARABLE_COMPONENTS.md'; VERSION=(ROOT/'VERSION').read_text().strip()
CANDIDATE_TOKENS=ROOT/'tokens/glaze-2.candidate.json'; CANDIDATE_CSS=ROOT/'css/glaze-2.emerging.candidate.css'; CANDIDATE_RUNTIME=ROOT/'js/glaze-2.emerging.candidate.js'; CANDIDATE_REFERENCE=ROOT/'reference/candidate-2.0-emerging.html'; CANDIDATE_VALIDATOR=ROOT/'scripts/validate_candidate_2_emerging.py'; STABLE=ROOT/'GLAZE_UI_2_STABLE.md'
LEGACY_TOKENS=ROOT/'tokens/wearable.candidate.tokens.json'; LEGACY_CSS=ROOT/'css/glaze.wearable.candidate.css'; LEGACY_REFERENCE=ROOT/'reference/wearable-candidate.html'; LEGACY_EVIDENCE=ROOT/'acceptance/wearable-native-evidence.template.json'; WEAR_OS_REFERENCE=ROOT/'reference/native/wear-os'; WATCH_OS_REFERENCE=ROOT/'reference/native/watchos'; WEAR_OS_WORKFLOW=ROOT/'.github/workflows/wear-os-emulator.yml'; STABLE_CSS=ROOT/'css/glaze.css'; CORE_CANDIDATE_CSS=ROOT/'css/glaze-2.candidate.css'
def req(c,m):
    if not c: raise SystemExit(f'wearable lifecycle validation failed: {m}')
def phrases(path,items,label):
    body=path.read_text(encoding='utf-8')
    for item in items: req(item in body,f'{label} missing: {item}')
def main():
    for p in (DOC,COMPONENTS,CANDIDATE_TOKENS,CANDIDATE_CSS,CANDIDATE_RUNTIME,CANDIDATE_REFERENCE,CANDIDATE_VALIDATOR,STABLE,LEGACY_TOKENS,LEGACY_CSS,LEGACY_REFERENCE,LEGACY_EVIDENCE,WEAR_OS_WORKFLOW,STABLE_CSS,CORE_CANDIDATE_CSS): req(p.exists(),f'missing {p.relative_to(ROOT)}')
    req(WEAR_OS_REFERENCE.is_dir() and WATCH_OS_REFERENCE.is_dir(),'historical native reference directories missing')
    req(VERSION=='2.0.0','current Stable VERSION must be 2.0.0')
    phrases(DOC,('Current Stable design contract: **Glaze UI 2.0.0**','compact rotational navigation','not a shrunken phone UI','historical 1.x native evidence','does not certify a Wear OS crown, watchOS Digital Crown','application-specific native or real-device acceptance'),'WEARABLES.md')
    phrases(COMPONENTS,('Glaze UI 2.0.0 is the current Stable contract','rendered interactive region below that floor','Exactly one rotational-navigation item should be current/focusable at a time','Canvas / Surface / Soft Glaze / Glaze / Deep Glaze / Live Glaze','historical evidence only','representative real-device operation'),'WEARABLE_COMPONENTS.md')
    phrases(STABLE,('Wearable rotational navigation','application-specific native or real-device acceptance'),'Stable contract')
    data=json.loads(CANDIDATE_TOKENS.read_text()); meta=data['meta']
    req(meta['version']=='2.0.0' and meta['status']=='Candidate','pre-promotion Candidate snapshot drifted')
    req(meta['productionEligible'] is False,'Candidate snapshot production boundary drifted')
    nav=data['layout']['navigationTransform']; req(nav['wearable']=='compact-rotational-navigation','wearable navigation transform drifted'); req(nav['spatial']=='floating-control-surface','spatial transform drifted')
    css=CANDIDATE_CSS.read_text()
    for m in ('--glaze-wearable-target: 48px','--glaze-spatial-target: 56px','.glaze-wearable-rotary-nav','.glaze-spatial-stage','prefers-reduced-motion','forced-colors','@supports not (transform-style: preserve-3d)'): req(m in css,f'promoted emerging CSS missing {m}')
    runtime=CANDIDATE_RUNTIME.read_text()
    for m in ('bindRotaryNavigation','setRotarySelection','setSpatialDepth','setSpatialFlat'): req(m in runtime,f'emerging runtime missing {m}')
    ref=CANDIDATE_REFERENCE.read_text(); req('GlazeUI2Emerging.bindRotaryNavigation' in ref,'wearable reference runtime binding missing'); req('GlazeUI2Emerging.setSpatialFlat' in ref,'spatial flat fallback binding missing')
    legacy=json.loads(LEGACY_TOKENS.read_text()); req(legacy['glaze']['wearableCandidate']['status']['$value']=='development-candidate','historical wearable token lifecycle drifted')
    req('glaze.wearable.candidate.css' not in STABLE_CSS.read_text(),'historical wearable CSS imported into legacy Stable CSS')
    req('glaze.wearable.candidate.css' not in CORE_CANDIDATE_CSS.read_text(),'historical 1.x wearable CSS imported by 2.0 core')
    workflow=WEAR_OS_WORKFLOW.read_text(); req('workflow_dispatch' in workflow and 'Deferred Manual Validation' in workflow,'historical Wear OS workflow must remain manual/deferred')
    evidence=json.loads(LEGACY_EVIDENCE.read_text()); req(evidence.get('status')=='template-only','historical native evidence must remain template-only'); req(evidence.get('promotion',{}).get('stableEligible') is False,'historical native evidence must remain promotion-ineligible')
    print('Glaze UI wearable lifecycle validated: 2.0 Stable platform-neutral mapping active, historical 1.x native evidence isolated, product native-device acceptance still separate')
if __name__=='__main__': main()
