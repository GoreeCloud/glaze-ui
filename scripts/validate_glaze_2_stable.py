#!/usr/bin/env python3
"""Validate the promoted Glaze UI 2.0 Stable contract and preserved Candidate provenance."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def req(c,m):
    if not c: raise SystemExit(f'Glaze UI 2.0 Stable validation failed: {m}')
def txt(p): return (ROOT/p).read_text(encoding='utf-8')
def main():
    required=(
        'GLAZE_UI_2_STABLE.md','GLAZE_UI_2.md','VERSION','tokens/glaze.tokens.json','tokens/glaze-2.candidate.json',
        'css/glaze-2.candidate.css','js/glaze-2.candidate.js','css/glaze-2.foldable.candidate.css',
        'css/glaze-2.emerging.candidate.css','js/glaze-2.emerging.candidate.js','acceptance/2.0-candidate.md',
        'reference/candidate-2.0.html','reference/candidate-2.0-acceptance.html','reference/candidate-2.0-resilience.html',
        'reference/candidate-2.0-resilience-acceptance.html','reference/candidate-2.0-emerging.html',
        'reference/candidate-2.0-emerging-acceptance.html','scripts/validate_candidate_2_rendered.py',
        'scripts/validate_candidate_2_resilience.py','scripts/validate_candidate_2_emerging.py','scripts/validate_candidate_2_contrast.mjs'
    )
    for p in required: req((ROOT/p).is_file(),f'missing required artifact {p}')
    version=txt('VERSION').strip(); req(version=='2.0.0','VERSION must be 2.0.0')
    stable=txt('GLAZE_UI_2_STABLE.md')
    for marker in (
        'Lifecycle status:** Stable','Stable semantic version:** 2.0.0','Previous Stable implementation baseline:** Glaze UI 1.6.0',
        'Make interaction feel tangible.','Canvas / Surface / Soft Glaze / Glaze / Deep Glaze / Live Glaze',
        'No downstream application is promoted by declaration','application-specific native or real-device acceptance'
    ): req(marker in stable,f'Stable contract missing {marker}')
    candidate=json.loads(txt('tokens/glaze-2.candidate.json')); meta=candidate['meta']
    req(meta['version']=='2.0.0' and meta['status']=='Candidate','Candidate token snapshot lifecycle drifted')
    req(meta['stableImplementationBaseline']=='1.6.0','Candidate snapshot previous Stable drifted')
    req(meta['productionEligible'] is False and meta['requiresStablePromotion'] is True,'Candidate provenance boundary drifted')
    canonical=json.loads(txt('tokens/glaze.tokens.json'))
    req(canonical['meta']['version']=='2.0.0' and canonical['meta']['status']=='Stable','canonical Stable tokens are not 2.0 Stable')
    current=canonical.get('currentContract',{})
    req(current.get('materialLevels')==['Canvas','Surface','Soft Glaze','Glaze','Deep Glaze','Live Glaze'],'current material levels drifted')
    req(current.get('clarityModes')==['clear','balanced','solid'],'clarity modes drifted')
    req(current.get('appearanceModes')==['light','dark','deep-dark'],'appearance modes drifted')
    req(current.get('expressionModes')==['calm','balanced','expressive'],'expression modes drifted')
    req(current.get('touchMinimum')==48 and current.get('tvMinimum')==56,'Stable target floors drifted')
    req(current.get('motionAliasesMs')=={'fast':140,'standard':280,'expressive':520},'Stable motion aliases drifted')
    for k in ('connectedTransformation','foldableFirstClass','wearableRotationalNavigation','spatialFloatingSurfaces','advancedEffectsOptional'):
        req(current.get(k) is True,f'current Stable invariant {k} missing')
    req(current.get('presentationCreatesDomainTruth') is False,'presentation must not create domain truth')
    acceptance=txt('acceptance/2.0-candidate.md')
    for marker in ('prefers-contrast: more','View Transition API','1114×834','wearable','spatial'):
        req(marker in acceptance,f'Candidate acceptance provenance missing {marker}')
    print('Glaze UI 2.0 Stable contract and preserved Candidate provenance validated')
if __name__=='__main__': main()
